"""Deterministic quality gate for Progressive Writing artifacts.

Checks only what a script can decide: required parts, length, forbidden or
unsourced claims, artifact-specific anti-patterns. Meaning, tone, and native
phrasing stay with the agent's semantic review.

Usage:
    quality_gate.py --artifact commit --lang en [--facts facts.json] [FILE|-]

facts.json: {"facts": [...], "forbidden_claims": [...]}
Exit code 1 when any error is found; warnings never fail.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from readability import WORD_RE, diagnostics  # noqa: E402

# Each required part is a regex that may match DE or EN wording.
WHY = r"(?im)^#+\s*(why|warum|context|kontext|hintergrund|motivation|problem)\b"
VALIDATION = r"(?im)^#+\s*(validation|validierung|tests?|testing|test plan|how tested|verification|verifikation|prüfung|getestet|qa)\b"
SUBJECT = r"(?im)^(subject|betreff)\s*:"
PREVIEW = r"(?im)^(preview|vorschau(text)?)\s*:"
# A status label starts a line, optionally after Markdown heading or bold marks,
# so a word in prose ("the next release") does not count as the section.
LABEL = r"(?im)^[#*\s]*"

ARTIFACTS: dict[str, dict] = {
    "business_email": {"required": {"subject line": SUBJECT}, "warn_words": 180, "sentences": True},
    "marketing_email": {"required": {"subject line": SUBJECT, "preview line": PREVIEW}, "warn_words": 400},
    "slack": {
        "warn_words": 200,
        "sentences": True,
        "warn": {"email-style salutation line; Slack usually starts with the point": r"(?i)\A\s*(hi|hey|hello|dear|hallo|moin|servus|guten (morgen|tag)|liebe[rs]?|sehr geehrte[rs]?)\b[^\n]*,\s*\n"},
    },
    "hero": {"headline_max_words": 12},
    "landing_page": {"sentences": True},
    "website_content": {"sentences": True},
    "confluence": {
        "required": {
            "purpose": r"(?i)\b(purpose|zweck)\b",
            "owner or status": r"(?i)\b(owner|verantwortlich|status)\b",
        },
        "sentences": True,
    },
    "agile_status": {
        "required": {
            "signal": LABEL + r"signal\b",
            "outcome": LABEL + r"(outcome|ergebnis)\b",
            "learning": LABEL + r"(learned|learning|gelernt|erkenntnis)",
            "risk": LABEL + r"(risks?|risiken|risiko)\b",
            "next focus": LABEL + r"(next|nächste\w*)\b",
        },
        # Warn, not error: a status may say it deliberately does not report velocity.
        "warn": {"velocity or story points; check they are not presented as the outcome": r"(?i)\b(velocity|story points?)\b"},
    },
    "fast_roadmap": {
        "required": {
            "strategic intent": r"(?i)(strategic intent|strategische[rs]? (intent|ziel|absicht))",
            "outcome": r"(?i)\b(outcomes?|ergebnis)",
            "now": r"(?im)^#+\s*(now|jetzt)\b",
            "confidence or uncertainty": r"(?i)(confidence|uncertain|zuversicht|unsicher|konfidenz)",
            "investment boundary": r"(?i)(investment boundary|appetite|investitionsgrenze|budgetgrenze)",
        },
    },
    "agile_progress": {
        "required": {
            "goal": r"(?im)^#+\s*(goal|ziel)\b",
            "current state": r"(?i)(current state|aktueller stand|ist-stand)",
            "next breakthrough": LABEL + r"(next|nächste\w*)\b",
        },
        "reject": {"percent complete without a model": r"(?i)\d+\s?(%|prozent|percent)\s*(complete|done|finished|fertig|erledigt|abgeschlossen)"},
    },
    "product_document": {
        "required": {
            "problem": r"(?i)\bproblem\b",
            "evidence": r"(?i)\b(evidence|evidenz|belege)\b",
            "unknowns": r"(?i)\b(unknowns?|unbekannt|offene fragen|annahmen|assumptions)\b",
        },
    },
    "po_summary": {"warn_words": 300, "sentences": True},
    "executive_summary": {"warn_words": 300, "bottom_line_within_words": 40, "sentences": True},
    "pull_request": {"required": {"why or context": WHY, "validation": VALIDATION}},
    "commit": {},
}

GENERIC_COMMIT = re.compile(
    r"(?i)^(\w+(\(.+\))?:\s*)?"
    r"(update[sd]?|fix(es|ed)?|bugfix|changes?|wip|misc|stuff|tweaks?|cleanup|änderungen|anpassungen|korrekturen)"
    r"(\s+(bugs?|typos?|stuff|things|code|it|readme))?\.?$"
    r"|^(\w+(\(.+\))?:\s*)?(typo|bug)s?\.?$"
)
BOTTOM_LINE = re.compile(r"(?i)(bottom line|kurzfassung|fazit|tl;dr|kernaussage)")
PERCENT = re.compile(r"(?i)(?<![\d.,])(\d+(?:[.,]\d+)?)\s?(?:%|prozent|percent)")


def words(text: str) -> int:
    return len(WORD_RE.findall(text))


def check_commit(text: str, errors: list[str], warnings: list[str]) -> None:
    lines = text.strip("\n").splitlines()
    subject = lines[0].strip() if lines else ""
    if not subject:
        errors.append("commit: empty subject")
        return
    if GENERIC_COMMIT.match(subject):
        errors.append(f"commit: generic subject {subject!r} does not name the change")
    if len(subject) > 72:
        errors.append(f"commit: subject is {len(subject)} chars, tools truncate past 72")
    elif len(subject) > 50:
        warnings.append(f"commit: subject is {len(subject)} chars, aim for 50")
    if len(lines) > 1 and lines[1].strip():
        errors.append("commit: second line must be blank before the body")


def check_claims(text: str, facts: dict | None, errors: list[str], warnings: list[str]) -> None:
    if not facts:
        return
    lowered = text.lower()
    for claim in facts.get("forbidden_claims", []):
        if claim.lower() in lowered:
            errors.append(f"claim: forbidden or unknown claim stated as fact: {claim!r}")
    # Compare numbers, not strings: "3,5 %", "3.5%" and "3.5 Prozent" are one claim.
    sourced = {n.replace(",", ".") for n in PERCENT.findall(" ".join(facts.get("facts", [])))}
    for pct in sorted({n.replace(",", ".") for n in PERCENT.findall(text)}):
        if pct not in sourced:
            warnings.append(f"claim: {pct}% has no matching source fact; verify or remove")


def check(text: str, artifact: str, language: str, facts: dict | None = None) -> dict:
    if artifact not in ARTIFACTS:
        raise ValueError(f"unknown artifact {artifact!r}; known: {', '.join(sorted(ARTIFACTS))}")
    rules = ARTIFACTS[artifact]
    errors: list[str] = []
    warnings: list[str] = []

    for label, pattern in rules.get("required", {}).items():
        if not re.search(pattern, text):
            errors.append(f"{artifact}: missing {label}")
    for label, pattern in rules.get("reject", {}).items():
        if re.search(pattern, text):
            errors.append(f"{artifact}: {label}")
    for label, pattern in rules.get("warn", {}).items():
        if re.search(pattern, text):
            warnings.append(f"{artifact}: {label}")

    if artifact == "commit":
        check_commit(text, errors, warnings)

    if artifact == "marketing_email":
        subj = re.search(r"(?im)^(?:subject|betreff)\s*:\s*(.+)$", text)
        prev = re.search(r"(?im)^(?:preview|vorschau(?:text)?)\s*:\s*(.+)$", text)
        if subj and prev and subj.group(1).strip().lower() == prev.group(1).strip().lower():
            errors.append("marketing_email: preview repeats the subject instead of adding to it")

    if "headline_max_words" in rules:
        h1 = re.search(r"(?m)^#\s+(.+)$", text)
        if not h1:
            errors.append(f"{artifact}: missing '# ' headline")
        elif words(h1.group(1)) > rules["headline_max_words"]:
            errors.append(f"{artifact}: headline has {words(h1.group(1))} words, max {rules['headline_max_words']}")

    if "bottom_line_within_words" in rules:
        m = BOTTOM_LINE.search(text)
        if not m or words(text[: m.start()]) > rules["bottom_line_within_words"]:
            warnings.append(f"{artifact}: no bottom line label in the first {rules['bottom_line_within_words']} words")

    total = words(text)
    if "warn_words" in rules and total > rules["warn_words"]:
        warnings.append(f"{artifact}: {total} words, default ceiling {rules['warn_words']}")

    check_claims(text, facts, errors, warnings)

    diag = diagnostics(text, language) if rules.get("sentences") else {}
    if diag.get("long_sentences"):
        warnings.append(f"readability: {diag['long_sentences']} sentence(s) over 25 words")

    return {"artifact": artifact, "language": language, "errors": errors, "warnings": warnings, "diagnostics": diag}


def main(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--artifact", required=True, choices=sorted(ARTIFACTS))
    parser.add_argument("--lang", default="en")
    parser.add_argument("--facts", help="JSON file with facts and forbidden_claims")
    parser.add_argument("file", nargs="?", default="-")
    args = parser.parse_args(argv)
    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    facts = json.loads(Path(args.facts).read_text(encoding="utf-8")) if args.facts else None
    result = check(text, args.artifact, args.lang, facts)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
