"""Check a skill family's knowledge base: source registry and citations.

Usage: check-knowledge.py [FAMILY_DIR ...]   (default: every family in skills/)

A family keeps its registry at `<core>/references/sources.json`; its Markdown
cites sources as `[SRC-DOMAIN-NNN]`. A rule that cites a missing source, or a
source that cannot be re-checked, makes the golden path untrustworthy without
anyone noticing, so both are errors. A registered source nothing cites is a
warning: it may be kept on purpose for a planned rule.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITATION = re.compile(r"\bSRC-[A-Z0-9]+-\d{3}\b")
DATE = re.compile(r"^\d{4}(-\d{2}){0,2}$")
REQUIRED = ("id", "title", "url", "publisher", "published", "accessed", "type",
            "domains", "findings", "limits", "evidence_level", "revisit")
LEVELS = {"verified", "supported", "context-dependent", "hypothesis", "aesthetic"}
# A rule may claim its source's level or a weaker one, never a stronger one,
# because "verified" next to a context-dependent source misleads the reader.
RANK = {"verified": 4, "supported": 3, "context-dependent": 2, "hypothesis": 1, "aesthetic": 1}
LEVELED = re.compile(
    r"\((verified|supported|context-dependent|hypothesis|aesthetic)\b[^)]*\)\s*((?:\[SRC-[A-Z0-9]+-\d{3}\]\s*)+)"
)


def registries(family: Path) -> list[Path]:
    return sorted(family.glob("*/references/sources.json"))


def check(family: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    known: dict[str, Path] = {}
    levels: dict[str, str] = {}
    for registry in registries(family):
        for entry in json.loads(registry.read_text(encoding="utf-8")).get("sources", []):
            sid = entry.get("id", "<no id>")
            for field in REQUIRED:
                if entry.get(field) in (None, "", []):
                    errors.append(f"{registry.name}: {sid} lacks {field}")
            if entry.get("evidence_level") not in LEVELS:
                errors.append(f"{registry.name}: {sid} has evidence_level {entry.get('evidence_level')!r}")
            if entry.get("accessed") and not DATE.match(str(entry["accessed"])):
                errors.append(f"{registry.name}: {sid} accessed is not a date")
            published = str(entry.get("published", ""))
            if published and published != "unknown" and not DATE.match(published):
                errors.append(f"{registry.name}: {sid} published is not a date or 'unknown'")
            if sid in known:
                errors.append(f"{registry.name}: duplicate source id {sid}")
            known[sid] = registry
            levels[sid] = entry.get("evidence_level")

    cited: set[str] = set()
    for md in sorted(family.glob("*/**/*.md")):
        text = md.read_text(encoding="utf-8")
        for sid in CITATION.findall(text):
            cited.add(sid)
            if sid not in known:
                errors.append(f"{md.relative_to(family)}: cites {sid}, which no registry lists")
        for written, group in LEVELED.findall(re.sub(r"\s+", " ", text)):
            ids = [sid for sid in CITATION.findall(group) if levels.get(sid) in RANK]
            # Several sources may back one rule; the strongest of them sets the ceiling.
            if ids and RANK[written] > max(RANK[levels[sid]] for sid in ids):
                strongest = max(ids, key=lambda sid: RANK[levels[sid]])
                errors.append(f"{md.relative_to(family)}: claims ({written}) for {', '.join(ids)}, "
                              f"stronger than the strongest registry level ({levels[strongest]})")
    for sid in sorted(set(known) - cited):
        warnings.append(f"{sid} is registered but cited nowhere")
    return sorted(set(errors)), warnings


def main(argv: list[str]) -> int:
    families = [Path(a) for a in argv] or sorted({r.parents[2] for r in (ROOT / "skills").rglob("references/sources.json")})
    failed = False
    for family in families:
        errors, warnings = check(family)
        for line in errors:
            print(f"ERROR {family.name}: {line}")
        for line in warnings:
            print(f"warn  {family.name}: {line}")
        failed = failed or bool(errors)
        print(f"{family.name}: {'FAILED' if errors else 'ok'} ({len(errors)} errors, {len(warnings)} warnings)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
