#!/usr/bin/env python3
"""Gate spikes, iterations, and learning loops with Jev typed decisions.

Calls Jev, TypeSafe AI's System One model, to answer typed questions about a
hypothesis, an iteration log, or a set of candidate iterations. The verdict
itself lives in code below. See SKILL.md for the behavior contract.

Three subcommands:
  hypothesis  --goal --hypothesis --measure --increment
      Before a spike: is the smallest increment worth building.
  continue    --goal --log FILE
      After an iteration: did it move, how far, continue/switch/stop.
  rank        --candidates FILE [--weights v,u,r,e]
      Choosing among candidate iterations or work items: rank them.

Quickstart (no config file needed):
    export TYPESAFE_API_KEY=sk-...
    python3 iteration-gate.py hypothesis --goal "..." --hypothesis "..." \\
        --measure "..." --increment "..."

Without a key, `hypothesis` and `continue` still run: they print a "gate
unavailable" verdict, exit 0, and tell the caller to decide for itself.
`rank` has no code-only fallback and exits 2 instead.

Two backends, one key: `scripts/jev_client.py` calls TypeSafe directly with
`TYPESAFE_API_KEY`, or the Vercel AI Gateway (model `typesafe-ai/jev`) with
`VERCEL_AI_GATEWAY_API_KEY`, same as route-subagent.py. Keys are read from a
`.env` beside this Skill first, then the environment, then
`~/.config/typesafe/api-key` or `~/.config/vercel/ai-gateway-key`;
`JEV_BACKEND` forces one backend. Every decision (including `no-measurements` and
`unavailable`) is appended as one JSON line to
`~/.harness/jev-iteration-log.jsonl` -- timestamp, command, verdict,
confidences, and an `outcome` field left empty for later evidence to fill
in; pass `--no-record` to skip.

`continue` refuses to spend a Jev call when the latest iteration carries no
measurements and no checks at all: verdict `no-measurements`, exit 6, fix the
log entry first. Rating "distance to shippable" from prose the model cannot
verify is asking it to rate its own writing -- see SKILL.md for the
observed evidence behind this rule and the confidence thresholds below.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jev_client as jev  # noqa: E402  (same directory; the Skill ships both files)

ROOT = Path(__file__).resolve().parents[1]
BACKEND = "typesafe"  # set by load_api_key(); "gateway" when the Vercel AI Gateway key is used
LOG_PATH = Path.home() / ".harness" / "jev-iteration-log.jsonl"

NOUL_READY_THRESHOLD = 0.6
HIGH_CONFIDENCE = 0.7
DISTANCE_LOWEST_LEVEL = 1.0  # score band 0: at or past a shippable outcome now

EXIT_READY, EXIT_GRILL = 0, 3
EXIT_CONTINUE, EXIT_SWITCH, EXIT_STOP = 0, 4, 5
EXIT_RANK_UNAVAILABLE = 2
EXIT_NO_MEASUREMENTS = 6


def _record(args: argparse.Namespace, command: str, verdict: str, confidences: dict) -> None:
    """Append one JSON-line decision to the pilot log. Never blocks the caller."""
    if getattr(args, "no_record", False):
        return
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": command,
        "verdict": verdict,
        "confidences": confidences,
        "outcome": None,
    }
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass  # recording is best-effort evidence, never a reason to fail the gate


def _confidences(answers: dict) -> dict:
    return {name: ans["confidence"] for name, ans in answers.items() if "confidence" in ans}


# --- shared: request, call, key loading (mirrors route-subagent.py) ---

def build_request(state: dict, questions: dict, api_key: str):
    return jev.build_request(state, questions, BACKEND, api_key)


def evaluate(state: dict, questions: dict, api_key: str, timeout: float = 30.0) -> tuple[dict, int]:
    """Call Jev on the selected backend. Raises RuntimeError with a short, key-free message on any failure."""
    return jev.evaluate(state, questions, BACKEND, api_key, timeout)


def cost_usd(usage: dict | None) -> float:
    return jev.cost_usd(usage, BACKEND)


def load_api_key() -> str:
    """Pick the backend and key per jev_client.load_credentials (a `.env` beside
    the Skill first). Raises RuntimeError when no key is configured; every caller
    here catches it and fails open (see module docstring)."""
    global BACKEND
    try:
        BACKEND, key = jev.load_credentials(ROOT)
    except SystemExit as error:
        raise RuntimeError(str(error)) from None
    return key


# --- hypothesis: before a spike ---

HYPOTHESIS_NOULS = {
    "falsifiable": "The hypothesis is stated so a result could prove it wrong; it is not vague enough to always look confirmed.",
    "measurable": "A concrete measurable outcome is named: a metric, a check, or an observable result, not just a feeling.",
    "smallest_increment": "The increment described is the smallest step that could teach something, not a larger batch of work bundled in.",
    "reversible": "The increment is reversible or cheap to discard if it teaches the wrong thing: a deleted branch, not a migration.",
}

HYPOTHESIS_QUESTIONS = {
    **{name: {"type": "noul", "instructions": text} for name, text in HYPOTHESIS_NOULS.items()},
    "teach_decisive": {
        "type": "score",
        "instructions": "How likely is this increment to teach something decisive toward the goal?",
        "criteria": [
            "Unlikely: the result will not change what happens next either way.",
            "Somewhat likely: it narrows things a little but leaves the real question open.",
            "Likely: the result plausibly settles the next concrete step.",
            "Very likely: the result directly decides whether to continue, switch, or stop.",
        ],
    },
}


def decide_hypothesis(payload: dict, min_confidence: float = 0.6) -> dict:
    answers = payload["answers"]
    nouls = {name: answers[name]["noul"] for name in HYPOTHESIS_NOULS}
    failing = [name for name, value in nouls.items() if value < NOUL_READY_THRESHOLD]
    score = answers["teach_decisive"]["score"]
    score_confidence = answers["teach_decisive"].get("confidence", 1.0)
    confident = score_confidence >= min_confidence
    reasons: list[str] = []
    if failing:
        reasons.append("failing criteria: " + ", ".join(failing))
    if not confident:
        reasons.append(f"low confidence on teach_decisive ({score_confidence})")
    verdict = "ready" if (not failing and confident) else "grill"
    return {"verdict": verdict, "nouls": nouls, "teach_decisive": score, "confident": confident, "reasons": reasons,
            "confidences": _confidences(answers)}


def run_hypothesis(args: argparse.Namespace) -> int:
    state = {"goal": args.goal, "hypothesis": args.hypothesis, "measure": args.measure, "increment": args.increment}
    try:
        payload, latency_ms = evaluate(state, HYPOTHESIS_QUESTIONS, load_api_key())
        decision = decide_hypothesis(payload, args.min_confidence)
    except (RuntimeError, KeyError, TypeError) as error:
        return _print_unavailable(
            args, "hypothesis",
            "gate unavailable: Jev could not be reached; decide yourself whether this is ready or needs grilling, and say so.",
            str(error), EXIT_READY,
        )
    result = {**decision, "latency_ms": latency_ms, "usage": payload.get("usage"), "cost_usd": round(cost_usd(payload.get("usage")), 6)}
    _record(args, "hypothesis", decision["verdict"], decision["confidences"])
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"verdict: {result['verdict']}")
        for name, value in result["nouls"].items():
            flag = "ok" if value >= NOUL_READY_THRESHOLD else "fails"
            print(f"  - {name}: {value:.2f} ({flag})")
        print(f"  - teach_decisive: {result['teach_decisive']:.2f} (confident: {result['confident']})")
        for reason in result["reasons"]:
            print(f"  reason: {reason}")
        print(f"  jev {result['latency_ms']} ms, {result['usage']}, ${result['cost_usd']}")
    return EXIT_READY if decision["verdict"] == "ready" else EXIT_GRILL


# --- continue: after an iteration ---

CONTINUE_QUESTIONS = {
    "moved": {
        "type": "noul",
        "instructions": "Did the latest iteration move a measured value toward the stated goal, not just produce activity or prose.",
    },
    "distance": {
        "type": "score",
        "instructions": "How far is this work from a shippable outcome right now?",
        "criteria": [
            "At or past a shippable outcome: ship or park it now.",
            "Close: one or two more iterations from a decision.",
            "Some distance: direction is plausible but real work remains.",
            "Far: no shippable outcome in sight; direction is unclear.",
        ],
    },
    "next_step": {
        "type": "choice",
        "instructions": "What should happen next?",
        "criteria": {
            "continue": "Keep testing the same hypothesis; the last iteration still taught something useful.",
            "switch": "Abandon this hypothesis for a different one; this direction stopped teaching anything new.",
            "stop": "Stop iterating: ship the result or park the effort.",
        },
    },
}


def _iteration_moved(prev: dict, current: dict) -> bool | None:
    """Code-only, deterministic: did any named measurement change value. None if incomparable."""
    if not current:
        return None
    for key, value in current.items():
        if key not in prev:
            return True
        try:
            if float(value) != float(prev[key]):
                return True
        except (TypeError, ValueError):
            if value != prev[key]:
                return True
    return False


def _two_consecutive_no_movement(log: list[dict]) -> bool:
    if len(log) < 3:
        return False
    latest = _iteration_moved(log[-2].get("measurements") or {}, log[-1].get("measurements") or {})
    prior = _iteration_moved(log[-3].get("measurements") or {}, log[-2].get("measurements") or {})
    return latest is False and prior is False


def decide_continue(payload: dict, log: list[dict]) -> dict:
    answers = payload["answers"]
    moved = answers["moved"]["noul"]
    moved_confidence = answers["moved"].get("confidence", 1.0)
    distance = answers["distance"]["score"]
    choice = answers["next_step"]["choice"]
    choice_confidence = answers["next_step"].get("confidence", 1.0)

    stagnant = _two_consecutive_no_movement(log)
    high_confidence_no_movement = moved < 0.5 and moved_confidence >= HIGH_CONFIDENCE
    no_measurement_count = sum(1 for entry in log if not entry.get("measurements"))

    reasons: list[str] = []
    if distance < DISTANCE_LOWEST_LEVEL:
        verdict = "stop"
        reasons.append("distance to a shippable outcome is at the lowest level")
    elif stagnant and high_confidence_no_movement:
        verdict = "stop"
        reasons.append("two consecutive iterations show no movement, at high confidence")
    elif choice == "switch" and choice_confidence >= 0.6:
        verdict = "switch"
        reasons.append(f"Jev recommends switch at confidence {choice_confidence}")
    else:
        verdict = "continue"
        reasons.append(f"Jev recommends {choice}" if choice != "continue" else "the last iteration kept teaching something")

    if no_measurement_count:
        reasons.append(
            f"{no_measurement_count} of {len(log)} iterations carry no measurements; "
            "Jev then judges prose, not progress"
        )

    return {
        "verdict": verdict, "moved": moved, "distance": distance, "next_step": choice,
        "no_measurement_count": no_measurement_count, "iterations": len(log), "reasons": reasons,
        "confidences": _confidences(answers),
    }


def _latest_iteration_has_no_signal(log: list[dict]) -> bool:
    """Refuse to spend a Jev call when the latest iteration carries neither a
    measurement nor a check -- see SKILL.md for the observed evidence."""
    if not log:
        return True
    latest = log[-1]
    return not latest.get("measurements") and not latest.get("checks")


def run_continue(args: argparse.Namespace) -> int:
    log = json.loads(args.log.read_text(encoding="utf-8"))
    if _latest_iteration_has_no_signal(log):
        _record(args, "continue", "no-measurements", {})
        message = "no-measurements: the latest iteration carries no measurement and no check; add one before asking Jev to judge progress."
        if args.json:
            print(json.dumps({"verdict": "no-measurements", "message": message}, ensure_ascii=False, indent=2))
        else:
            print(f"verdict: no-measurements\n  reason: {message}")
        return EXIT_NO_MEASUREMENTS
    state = {"goal": args.goal, "log": log}
    try:
        payload, latency_ms = evaluate(state, CONTINUE_QUESTIONS, load_api_key())
        decision = decide_continue(payload, log)
    except (RuntimeError, KeyError, TypeError) as error:
        return _print_unavailable(
            args, "continue",
            "gate unavailable: Jev could not be reached; decide yourself whether to continue, switch, or stop, and say so.",
            str(error), EXIT_CONTINUE,
        )
    result = {**decision, "latency_ms": latency_ms, "usage": payload.get("usage"), "cost_usd": round(cost_usd(payload.get("usage")), 6)}
    _record(args, "continue", decision["verdict"], decision["confidences"])
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"verdict: {result['verdict']}")
        print(f"  moved: {result['moved']:.2f}  distance: {result['distance']:.2f}  next_step: {result['next_step']}")
        for reason in result["reasons"]:
            print(f"  reason: {reason}")
        print(f"  jev {result['latency_ms']} ms, {result['usage']}, ${result['cost_usd']}")
    return {"continue": EXIT_CONTINUE, "switch": EXIT_SWITCH, "stop": EXIT_STOP}[decision["verdict"]]


# --- rank: choosing among candidates ---

RANK_QUESTIONS = {
    "value": {
        "type": "score",
        "instructions": "How much value would this candidate add toward the stated goal?",
        "criteria": ["Little to none", "Some", "Substantial", "Decisive"],
    },
    "urgency": {
        "type": "score",
        "instructions": "How urgent is this candidate right now?",
        "criteria": ["Can wait indefinitely", "Can wait a while", "Should happen soon", "Blocking or time-critical"],
    },
    "risk": {
        "type": "score",
        "instructions": "How risky is it if this candidate turns out to be the wrong bet?",
        "criteria": ["Negligible, cheap to discard", "Minor rework", "Real cost, recoverable", "Hard to reverse or costly"],
    },
    "effort": {
        "type": "score",
        "instructions": "How much effort would this candidate take?",
        "criteria": ["Trivial", "Small", "Moderate", "Large"],
    },
}


def _combined_score(scores: dict, weights: tuple[float, float, float, float]) -> float:
    v_w, u_w, r_w, e_w = weights
    raw = v_w * scores["value"] + u_w * scores["urgency"] - r_w * scores["risk"] - e_w * scores["effort"]
    lo = -(r_w + e_w) * 3.0
    hi = (v_w + u_w) * 3.0
    return 0.0 if hi == lo else (raw - lo) / (hi - lo)


def rank_candidates(per_candidate: list[dict], weights: tuple[float, float, float, float]) -> list[dict]:
    ranked = []
    for candidate in per_candidate:
        scores = {name: candidate["answers"][name]["score"] for name in RANK_QUESTIONS}
        confidences = {name: candidate["answers"][name].get("confidence", 1.0) for name in RANK_QUESTIONS}
        combined = _combined_score(scores, weights)
        ranked.append({"id": candidate["id"], "text": candidate["text"], "combined": combined, "scores": scores, "confidences": confidences})
    ranked.sort(key=lambda row: row["combined"], reverse=True)
    return ranked


def _print_rank_table(ranked: list[dict]) -> None:
    header = f"{'rank':>4}  {'id':<12}  {'combined':>8}  {'value':>6}  {'urgency':>7}  {'risk':>6}  {'effort':>6}  text"
    print(header)
    for i, row in enumerate(ranked, start=1):
        s = row["scores"]
        text = row["text"] if len(row["text"]) <= 40 else row["text"][:37] + "..."
        print(f"{i:>4}  {row['id']:<12}  {row['combined']:>8.3f}  {s['value']:>6.2f}  {s['urgency']:>7.2f}  {s['risk']:>6.2f}  {s['effort']:>6.2f}  {text}")


def run_rank(args: argparse.Namespace) -> int:
    candidates = json.loads(args.candidates.read_text(encoding="utf-8"))
    weights = tuple(float(x) for x in args.weights.split(","))
    if len(weights) != 4:
        sys.exit("--weights needs exactly 4 comma-separated numbers: v,u,r,e")
    try:
        api_key = load_api_key()
        per_candidate = []
        total_usage = {"input_tokens": 0, "output_tokens": 0}
        total_latency = 0
        for candidate in candidates:
            state = {"goal": args.goal, "candidate": candidate["text"]}
            payload, latency_ms = evaluate(state, RANK_QUESTIONS, api_key)
            per_candidate.append({"id": candidate["id"], "text": candidate["text"], "answers": payload["answers"]})
            usage = payload.get("usage") or {}
            total_usage["input_tokens"] += usage.get("input_tokens", 0)
            total_usage["output_tokens"] += usage.get("output_tokens", 0)
            total_latency += latency_ms
    except (RuntimeError, KeyError, TypeError) as error:
        _record(args, "rank", "unavailable", {})
        print("gate unavailable: Jev could not be reached; ranking needs a decision per candidate, so this cannot fall back.")
        print(f"  reason: {error}")
        return EXIT_RANK_UNAVAILABLE
    ranked = rank_candidates(per_candidate, weights)
    _record(args, "rank", "ranked", {row["id"]: row["confidences"] for row in ranked})
    if args.json:
        print(json.dumps({"ranked": ranked, "usage": total_usage, "latency_ms": total_latency,
                           "cost_usd": round(cost_usd(total_usage), 6)}, ensure_ascii=False, indent=2))
    else:
        _print_rank_table(ranked)
        print(f"  jev {total_latency} ms, {total_usage}, ${round(cost_usd(total_usage), 6)}")
    return 0


# --- shared unavailable path ---

def _print_unavailable(args: argparse.Namespace, command: str, message: str, error: str, exit_code: int) -> int:
    _record(args, command, "unavailable", {})
    if args.json:
        print(json.dumps({"verdict": "unavailable", "command": command, "message": message, "error": error}, ensure_ascii=False, indent=2))
    else:
        print(message)
        print(f"  reason: {error}")
    return exit_code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p_hyp = sub.add_parser("hypothesis", help="before a spike: is the smallest increment ready or does it need grilling")
    p_hyp.add_argument("--goal", required=True)
    p_hyp.add_argument("--hypothesis", required=True)
    p_hyp.add_argument("--measure", required=True)
    p_hyp.add_argument("--increment", required=True)
    p_hyp.add_argument("--min-confidence", type=float, default=0.6)
    p_hyp.add_argument("--json", action="store_true")
    p_hyp.add_argument("--no-record", action="store_true", help="skip the ~/.harness/jev-iteration-log.jsonl entry")
    p_hyp.set_defaults(func=run_hypothesis)

    p_cont = sub.add_parser("continue", help="after an iteration: continue, switch, or stop")
    p_cont.add_argument("--goal", required=True)
    p_cont.add_argument("--log", required=True, type=Path)
    p_cont.add_argument("--json", action="store_true")
    p_cont.add_argument("--no-record", action="store_true", help="skip the ~/.harness/jev-iteration-log.jsonl entry")
    p_cont.set_defaults(func=run_continue)

    p_rank = sub.add_parser("rank", help="rank candidate iterations or work items")
    p_rank.add_argument("--candidates", required=True, type=Path)
    p_rank.add_argument("--goal", default="")
    p_rank.add_argument("--weights", default="1,1,1,1")
    p_rank.add_argument("--json", action="store_true")
    p_rank.add_argument("--no-record", action="store_true", help="skip the ~/.harness/jev-iteration-log.jsonl entry")
    p_rank.set_defaults(func=run_rank)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
