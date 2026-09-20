"""Shared Jev (TypeSafe System One) client for route-subagent.py and iteration-gate.py.

Two backends, same questions, same normalized answer shape:

- typesafe: POST https://api.typesafe.ai/v1/systemone with TYPESAFE_API_KEY.
  Question types choice, noul, score; answers carry `choice` plus
  `probabilities`, `noul`, or `score`, each with `confidence`; usage in
  `input_tokens`; $0.042 per million input tokens (list price 2026-09-20).
- gateway: POST https://ai-gateway.vercel.sh/v4/ai/evaluation-model with
  VERCEL_AI_GATEWAY_API_KEY, model `typesafe-ai/jev`, protocol headers as the
  `@ai-sdk/gateway` provider sends them (4.0.87, read 2026-09-20). The
  gateway calls a noul question `boolean` and answers with `probability`;
  confidence lives in `providerMetadata.typesafe.confidence`; usage in
  `inputTokens`; $0.04 per million input tokens.

Credential order: JEV_BACKEND forces a backend; otherwise a key in the
repository's own `.env` wins (the checkout decides how it pays), then the
environment, then the user-level files. A repository that keeps only the
Vercel key in its `.env` therefore routes every Jev call through the gateway
even on a machine that also holds a TypeSafe key.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

TYPESAFE_URL = "https://api.typesafe.ai/v1/systemone"
TYPESAFE_MODEL = "jev-latest"
GATEWAY_URL = "https://ai-gateway.vercel.sh/v4/ai/evaluation-model"
GATEWAY_MODEL = "typesafe-ai/jev"
USD_PER_INPUT_TOKEN = {"typesafe": 0.042 / 1_000_000, "gateway": 0.04 / 1_000_000}

KEY_NAMES = {"typesafe": "TYPESAFE_API_KEY", "gateway": "VERCEL_AI_GATEWAY_API_KEY"}
KEY_FILES = {
    "typesafe": Path.home() / ".config" / "typesafe" / "api-key",
    "gateway": Path.home() / ".config" / "vercel" / "ai-gateway-key",
}


def _dotenv(root: Path) -> dict[str, str]:
    env_file = root / ".env"
    values: dict[str, str] = {}
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                name, value = line.split("=", 1)
                values[name.strip()] = value.strip().strip('"').strip("'")
    return values


def load_credentials(root: Path) -> tuple[str, str]:
    """Return (backend, api_key). Exits with a key-free message when nothing is configured."""
    forced = os.environ.get("JEV_BACKEND")
    order = [forced] if forced in KEY_NAMES else ["typesafe", "gateway"]
    dotenv = _dotenv(root)
    for source in (dotenv.get, os.environ.get, lambda name: None):
        for backend in order:
            key = source(KEY_NAMES[backend])
            if key:
                return backend, key
    for backend in order:
        key_file = KEY_FILES[backend]
        if key_file.is_file():
            key = key_file.read_text(encoding="utf-8").strip()
            if key:
                return backend, key
    sys.exit(
        "no Jev credentials: set TYPESAFE_API_KEY or VERCEL_AI_GATEWAY_API_KEY "
        f"(environment, .env in {root}, ~/.config/typesafe/api-key, or ~/.config/vercel/ai-gateway-key)"
    )


def build_request(state: dict, questions: dict, backend: str, api_key: str) -> urllib.request.Request:
    if backend == "gateway":
        translated = {
            name: {**question, "type": "boolean"} if question.get("type") == "noul" else question
            for name, question in questions.items()
        }
        body = {"state": json.dumps(state, ensure_ascii=False), "questions": translated}
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "ai-gateway-protocol-version": "0.0.1",
            "ai-evaluation-model-specification-version": "4",
            "ai-model-id": GATEWAY_MODEL,
        }
        url = GATEWAY_URL
    else:
        body = {"state": json.dumps(state, ensure_ascii=False), "model": TYPESAFE_MODEL, "questions": questions}
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        url = TYPESAFE_URL
    return urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST", headers=headers)


def normalize(payload: dict, backend: str) -> dict:
    """Bring a gateway answer into the TypeSafe shape the deciders read."""
    if backend != "gateway":
        return payload
    confidence = ((payload.get("providerMetadata") or {}).get("typesafe") or {}).get("confidence") or {}
    answers = {}
    for name, answer in (payload.get("answers") or {}).items():
        normalized = dict(answer)
        if answer.get("type") == "boolean":
            normalized["noul"] = answer.get("probability")
        if name in confidence:
            normalized["confidence"] = confidence[name]
        answers[name] = normalized
    usage = payload.get("usage") or {}
    return {
        **payload,
        "answers": answers,
        "usage": {"input_tokens": usage.get("inputTokens", 0), "output_tokens": usage.get("outputTokens", 0)},
    }


def evaluate(state: dict, questions: dict, backend: str, api_key: str, timeout: float = 30.0) -> tuple[dict, int]:
    """Call Jev. Raises RuntimeError with a short, key-free message on any failure."""
    started = time.monotonic()
    label = "Vercel AI Gateway" if backend == "gateway" else "TypeSafe API"
    try:
        with urllib.request.urlopen(build_request(state, questions, backend, api_key), timeout=timeout) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"{label} {error.code}: {error.read().decode('utf-8', 'replace')[:200]}") from None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
        raise RuntimeError(f"{label} unreachable: {str(error)[:200]}") from None
    return normalize(payload, backend), int((time.monotonic() - started) * 1000)


def cost_usd(usage: dict | None, backend: str = "typesafe") -> float:
    return float((usage or {}).get("input_tokens", 0)) * USD_PER_INPUT_TOKEN[backend]
