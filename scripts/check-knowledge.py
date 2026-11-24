"""Check a skill family's knowledge base: source registry and citations.

Usage: check-knowledge.py [FAMILY_DIR ...]   (default: every family in skills/)
       check-knowledge.py --vocabulary [--strict] [--root DIR]

A family keeps its registry at `<core>/references/sources.json`; its Markdown
cites sources as `[SRC-DOMAIN-NNN]`. A rule that cites a missing source, or a
source that cannot be re-checked, makes the golden path untrustworthy without
anyone noticing, so both are errors. A registered source nothing cites is a
warning: it may be kept on purpose for a planned rule.

`--vocabulary` checks every Skill's expert vocabulary,
`references/vocabulary.md`: one table row per term with a definition, a
registered source, an observable marker, and how it is checked. A Skill that
judges quality without one, and a source not re-read for a year, are warnings;
a malformed table is an error. The mode exits 0 unless `--strict`, which
fails on errors and on Skills without a vocabulary or a metadata declaration;
an `exact` row without a rule id and a stale source stay warnings, because
they are the backlog for the next check, not a broken contract.

`--root DIR` checks another catalog laid out as `DIR/skills/<category>/<name>/`
(default: this repository), so a private catalog runs the same contract.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
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


# A vocabulary is loaded into context while judging, so its size is a budget.
MAX_TERMS = 40
MAX_LINES = 80
CHECKS = {"exact", "jev", "judge"}
RULE_ID = re.compile(r"`[a-z0-9]+(?:[.-][A-Za-z0-9-]+)+`")
# metadata.vocabulary: vendor or house exempts a Skill; a sibling Skill name
# (design-core) borrows that sibling's file, so a family keeps one copy.
DECLARED = re.compile(r"^metadata:\s*\n(?:[ \t]+.*\n)*?[ \t]+vocabulary:\s*[\"']?([a-z0-9-]+)[\"']?\s*$", re.M)
STALE_DAYS = 365


def registries(family: Path) -> list[Path]:
    return sorted(family.glob("*/references/sources.json"))


def catalog_levels(skills: Path) -> dict[str, str]:
    """Every registered source id in the catalog with its level.

    A Skill may cite a source another family registered (one paper backs a rule
    in two families); resolving it there keeps one entry instead of two that drift.
    """
    levels: dict[str, str] = {}
    for registry in sorted(skills.rglob("references/sources.json")):
        for entry in json.loads(registry.read_text(encoding="utf-8")).get("sources", []):
            levels.setdefault(entry.get("id", ""), entry.get("evidence_level"))
    return levels


def check(family: Path, catalog: dict[str, str] | None = None) -> tuple[list[str], list[str]]:
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

    foreign = {sid: level for sid, level in (catalog or {}).items() if sid not in known}
    levels = {**foreign, **levels}
    cited: set[str] = set()
    for md in sorted(family.glob("*/**/*.md")):
        text = md.read_text(encoding="utf-8")
        for sid in CITATION.findall(text):
            cited.add(sid)
            if sid not in known and sid not in foreign:
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


def check_vocabulary(skill: Path, known: set[str]) -> tuple[list[str], list[str]]:
    """Errors and warnings for one Skill's expert vocabulary."""
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1] + "\n" if text.startswith("---") else ""
    declared = DECLARED.search(frontmatter)
    if declared and declared.group(1) in {"vendor", "house"}:
        return [], []
    vocabulary = skill / "references" / "vocabulary.md"
    if not vocabulary.exists():
        # Coverage is declared in metadata, not by a pointer the reviewer would load:
        # loading the vocabulary into reviews lowered recall outside it (2026-11-24).
        if declared and (skill.parent / declared.group(1) / "references" / "vocabulary.md").exists():
            return [], []
        return [], ["no references/vocabulary.md or metadata.vocabulary: vendor|house|<sibling skill>"]

    errors: list[str] = []
    warnings: list[str] = []
    lines = vocabulary.read_text(encoding="utf-8").splitlines()
    if len(lines) > MAX_LINES:
        errors.append(f"vocabulary.md has {len(lines)} lines, over {MAX_LINES}")
    terms: list[str] = []
    in_table = False
    for line in lines:
        if not line.startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "Term":
            in_table = True
            continue
        if not in_table or set("".join(cells)) <= set("-: "):
            continue
        term = cells[0] or "<no term>"
        terms.append(term)
        if len(cells) != 5 or not all(cells):
            errors.append(f"{term}: needs 5 filled cells (Term, Definition, Source, Marker, Check)")
            continue
        ids = CITATION.findall(cells[2])
        if not ids:
            errors.append(f"{term}: names no [SRC-...] source")
        for sid in ids:
            if sid not in known:
                errors.append(f"{term}: cites {sid}, which no registry lists")
        kind = cells[4].split()[0]
        if kind not in CHECKS:
            errors.append(f"{term}: Check is {kind!r}, not one of {', '.join(sorted(CHECKS))}")
        elif kind == "exact" and not RULE_ID.search(cells[4]):
            warnings.append(f"{term}: exact check names no rule id yet")
    if len(terms) > MAX_TERMS:
        errors.append(f"vocabulary.md has {len(terms)} terms, over {MAX_TERMS}")
    seen: set[str] = set()
    for term in terms:
        if term.lower() in seen:
            errors.append(f"{term}: duplicate term")
        seen.add(term.lower())
    return errors, warnings


def stale_sources(family: Path, today: date | None = None) -> list[str]:
    """Sources nobody has re-read for a year; their findings may have moved."""
    today = today or date.today()
    warnings: list[str] = []
    for registry in registries(family):
        for entry in json.loads(registry.read_text(encoding="utf-8")).get("sources", []):
            accessed = str(entry.get("accessed", ""))
            if not DATE.match(accessed):
                continue
            parts = [int(p) for p in accessed.split("-")] + [1, 1]
            if (today - date(parts[0], parts[1], parts[2])).days > STALE_DAYS:
                warnings.append(f"{entry.get('id')}: accessed {accessed}, over {STALE_DAYS} days ago")
    return warnings


def vocabulary_main(strict: bool, root: Path = ROOT) -> int:
    skills = root / "skills"
    known = set(catalog_levels(skills))
    errors = warnings = missing = 0
    for path in sorted(skills.glob("*/*/SKILL.md")):
        errs, warns = check_vocabulary(path.parent, known)
        for line in errs:
            print(f"ERROR {path.parent.name}: {line}")
        for line in warns:
            print(f"warn  {path.parent.name}: {line}")
        errors += len(errs)
        warnings += len(warns)
        missing += any(w.startswith("no references/vocabulary.md") for w in warns)
    for family in sorted({r.parents[2] for r in skills.rglob("references/sources.json")}):
        for line in stale_sources(family):
            print(f"warn  {family.name}: {line}")
            warnings += 1
    print(f"vocabulary: {errors} errors, {warnings} warnings, {missing} skills without a vocabulary"
          f"{'' if strict else ' (warn-only; --strict fails on errors and missing vocabularies)'}")
    return 1 if strict and (errors or missing) else 0


def main(argv: list[str]) -> int:
    if "--vocabulary" in argv:
        root = Path(argv[argv.index("--root") + 1]) if "--root" in argv else ROOT
        return vocabulary_main("--strict" in argv, root)
    families = [Path(a) for a in argv] or sorted({r.parents[2] for r in (ROOT / "skills").rglob("references/sources.json")})
    catalog = catalog_levels(ROOT / "skills")
    failed = False
    for family in families:
        errors, warnings = check(family, catalog)
        for line in errors:
            print(f"ERROR {family.name}: {line}")
        for line in warnings:
            print(f"warn  {family.name}: {line}")
        failed = failed or bool(errors)
        print(f"{family.name}: {'FAILED' if errors else 'ok'} ({len(errors)} errors, {len(warnings)} warnings)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
