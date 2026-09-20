#!/usr/bin/env python3
"""Claude Code PreToolUse hook for the Agent tool: route every subagent spawn.

Runs route-subagent.py on the child's prompt and rewrites the spawn: `model`
becomes the routed alias and the prompt gets a first line
"Routed: model=... effort=... ..." so the child works at the routed effort
and the parent can see what was chosen. The parent's own model never sets
the child's route; the typed router does.

Fail-open by design: a missing router, a missing key, a timeout, or a broken
answer yields the Balanced default (sonnet, medium) and says so. Spawns that
already carry a "Routed:" line, forks (they ignore model), and sessions with
CLAUDE_CODE_SUBAGENT_MODEL set pass through untouched.

Install: see templates/settings.snippet.json in this Skill for the
settings.json PreToolUse entry, and SKILL.md for the one-command install.
Set ROUTE_SUBAGENT_SCRIPT if route-subagent.py does not sit next to this
file (the default assumption when both are installed together).
"""

from __future__ import annotations  # this file must run on Python 3.9

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROUTER = Path(os.environ.get("ROUTE_SUBAGENT_SCRIPT", Path(__file__).resolve().parent / "route-subagent.py"))
LOG = Path.home() / ".claude" / "hooks" / "route-subagent.log"
FALLBACK = {"model": "sonnet", "effort": "medium", "tier": "balanced", "task_class": "unknown", "confident": False}


def route(prompt: str) -> dict:
    if not ROUTER.is_file():
        return {**FALLBACK, "reasons": [f"router unavailable (missing {ROUTER})"]}
    try:
        done = subprocess.run(
            [sys.executable, str(ROUTER), "--host", "claude", "--json", prompt[:4000]],
            capture_output=True, text=True, timeout=20,
        )
        result = json.loads(done.stdout)
        if done.returncode != 0 or not {"model", "effort"} <= set(result):
            raise ValueError(done.stderr.strip()[:120] or "bad router output")
        if "fast" in str(result["model"]).lower():
            raise ValueError("router returned a fast route")
        return result
    except (subprocess.TimeoutExpired, ValueError, OSError, json.JSONDecodeError) as error:
        return {**FALLBACK, "reasons": [f"router unavailable ({type(error).__name__}: {str(error)[:120]})"]}


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    tool_input = event.get("tool_input") or {}
    prompt = tool_input.get("prompt") or tool_input.get("instructions") or ""
    if not prompt or prompt.startswith("Routed:"):
        return 0
    if tool_input.get("subagent_type") == "fork" or os.environ.get("CLAUDE_CODE_SUBAGENT_MODEL"):
        return 0

    started = time.monotonic()
    decision = route(prompt)
    model = decision["model"] if decision.get("confident") or not tool_input.get("model") else tool_input["model"]
    header = (
        f"Routed: model={model} effort={decision['effort']} tier={decision.get('tier')} "
        f"class={decision.get('task_class')} confident={str(bool(decision.get('confident'))).lower()}. "
        f"Work at {decision['effort']} effort."
    )
    updated = dict(tool_input)
    updated["model"] = model
    updated["prompt" if "prompt" in tool_input or "instructions" not in tool_input else "instructions"] = f"{header}\n\n{prompt}"
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as log:
            log.write(json.dumps({
                "at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "model": model,
                "effort": decision["effort"],
                "task_class": decision.get("task_class"),
                "confident": bool(decision.get("confident")),
                "hook_ms": int((time.monotonic() - started) * 1000),
                "description": str(tool_input.get("description", ""))[:80],
                "reason": (decision.get("reasons") or [""])[0][:120],
            }) + "\n")
    except OSError:
        pass
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "updatedInput": updated,
        "additionalContext": header,
    }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
