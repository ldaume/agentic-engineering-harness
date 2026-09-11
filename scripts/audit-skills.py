#!/usr/bin/env python3
"""Validate this repository's portable Agent Skills without extra packages."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
LOCK_PATH = ROOT / "skills-lock.json"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
FIELD_PATTERN = re.compile(r"^([a-z][a-z0-9-]*):\s*(.*)$")
LINK_PATTERN = re.compile(r"\[[^\]]*]\(([^)]+)\)")
STANDARD_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}

# The plain punctuation table has one owner: scripts/verify-plain-punctuation.py.
# This audit reuses it rather than keeping a second, narrower copy. The previous
# inline copy listed twelve characters and missed primes, guillemets, the rest of
# the dash family, exotic spaces, bidi controls, and decorative separators.
_PUNCTUATION_GATE = importlib.util.spec_from_file_location(
    "verify_plain_punctuation", Path(__file__).with_name("verify-plain-punctuation.py")
)
assert _PUNCTUATION_GATE and _PUNCTUATION_GATE.loader
punctuation = importlib.util.module_from_spec(_PUNCTUATION_GATE)
_PUNCTUATION_GATE.loader.exec_module(punctuation)
TEXT_EXTS = {".md", ".py", ".yml", ".yaml", ".json", ".txt", ".sh", ".toml"}
SKIP_DIRS = {".git", ".local", ".serena", "node_modules", ".worktrees", "worktrees"}

def is_skipped(path: Path) -> bool:
    """Decide by location inside the repository, not by absolute path.

    `SKIP_DIRS` was matched against a path's absolute parts. A checkout under
    `<somewhere>/.worktrees/<task>/` - the isolation default this catalog's own
    harness prescribes - therefore matched on the parent directory, and every
    file-level validator skipped every file while the audit still printed
    "passed". Measured at the time of the fix: 0 of 83 Markdown files
    inspected. CI never saw it, because CI checks out at an ordinary path.
    """
    try:
        relative = path.resolve().relative_to(ROOT)
    except ValueError:
        return True
    return any(part in SKIP_DIRS for part in relative.parts)

PROSE_SLOP_PATTERNS = {
    "stock model verb": re.compile(r"\bdelv(?:e|es|ed|ing) into\b", re.IGNORECASE),
    "empty friction claim": re.compile(
        r"\b(?:seamless (?:experience|integration|journey|transition|workflow|"
        r"collaboration|solution|process)|seamlessly (?:integrat(?:e|es|ed|ing)|"
        r"connect(?:s|ed|ing)?|transition(?:s|ed|ing)?))\b",
        re.IGNORECASE,
    ),
    "hype claim": re.compile(
        r"\b(?:game[- ]chang(?:er|ing)|cutting[- ]edge)\b", re.IGNORECASE
    ),
    "generic trend setup": re.compile(
        r"\b(?:ever-evolving (?:world|landscape|environment)|in today'?s "
        r"(?:(?:digital|fast-paced|ever-changing|rapidly changing) "
        r"(?:world|landscape|environment)|world))\b",
        re.IGNORECASE,
    ),
    "generic potential claim": re.compile(
        r"\bunlock(?:s|ed|ing)? (?:the )?(?:full )?(?:power|potential)\b",
        re.IGNORECASE,
    ),
    "generic metaphor": re.compile(
        r"\b(?:(?:rich )?tapestry of|testament to)\b", re.IGNORECASE
    ),
    "generic complexity claim": re.compile(
        r"\bnavigat(?:e|es|ed|ing) the complexit(?:y|ies) of\b", re.IGNORECASE
    ),
    "empty transformation claim": re.compile(
        r"\brevolutioni[sz](?:e|es|ed|ing)\b", re.IGNORECASE
    ),
    "filler aside": re.compile(
        r"\b(?:at its core|in the realm of|(?:it is )?important to note|"
        r"(?:it is|it's) worth noting)\b",
        re.IGNORECASE,
    ),
    "culture filler": re.compile(
        r"\bfoster(?:s|ed|ing)? (?:a |the )?culture of\b", re.IGNORECASE
    ),
    "power filler": re.compile(r"\bleverage the power of\b", re.IGNORECASE),
    "journey filler": re.compile(r"\btransformative journey\b", re.IGNORECASE),
}
PROSE_AUDIT_ALLOW = "<!-- prose-audit: allow -->"
INLINE_CODE_PATTERN = re.compile(r"(?P<ticks>`+).*?(?P=ticks)")
FENCE_PATTERN = re.compile(r"^\s{0,3}(?P<marker>`{3,}|~{3,})")
PROSE_SLOP_POSITIVE_SAMPLES = {
    "stock model verb": "We delve into the topic.",
    "empty friction claim": "Create a seamless experience.",
    "hype claim": "This cutting-edge platform is a game changer.",
    "generic trend setup": "In today's world, teams need more speed.",
    "generic potential claim": "Unlock the full potential of AI.",
    "generic metaphor": "A rich tapestry of tools supports the work.",
    "generic complexity claim": "Navigate the complexities of delivery.",
    "empty transformation claim": "This will revolutionize engineering.",
    "filler aside": "At its core, the platform is simple.",
    "culture filler": "Foster a culture of innovation.",
    "power filler": "Leverage the power of automation.",
    "journey filler": "Begin a transformative journey.",
}
PROSE_SLOP_NEGATIVE_SAMPLES = (
    "Use `seamless-immutable` for this package.",
    "Use ``cutting-edge`` as the exact identifier.",
    "Connect the Tapestry service.",
    "Use the Delve debugger.",
    "> The source calls it cutting-edge.",
    "The source calls it cutting-edge. <!-- prose-audit: allow -->",
    "Name the problem, trade-off, and next step.",
)
PROSE_FENCE_NEGATIVE_SAMPLES = (
    "```text\ncutting-edge\n```",
    "~~~text\ncutting-edge\n~~~",
)


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def frontmatter(path: Path, text: str, errors: list[str]) -> dict[str, str]:
    relative = path.relative_to(ROOT)
    if not text.startswith("---\n"):
        errors.append(f"{relative}: missing YAML frontmatter")
        return {}

    parts = text.split("---", 2)
    if len(parts) != 3:
        errors.append(f"{relative}: unclosed YAML frontmatter")
        return {}

    fields: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line or line[0].isspace():
            continue
        match = FIELD_PATTERN.match(line)
        if match:
            fields[match.group(1)] = scalar(match.group(2))

    unknown = sorted(set(fields) - STANDARD_FIELDS)
    if unknown:
        errors.append(
            f"{relative}: non-standard frontmatter fields: " + ", ".join(unknown)
        )
    if re.search(r"^\s+triggers:\s*$", parts[1], re.MULTILINE):
        errors.append(f"{relative}: duplicate trigger list; use description")
    return fields


def validate_skill(path: Path, errors: list[str]) -> str | None:
    text = path.read_text(encoding="utf-8")
    fields = frontmatter(path, text, errors)
    relative = path.relative_to(ROOT)
    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        errors.append(f"{relative}: missing name")
    elif not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        errors.append(f"{relative}: invalid name {name!r}")
    elif name != path.parent.name:
        errors.append(f"{relative}: name does not match directory")

    if not description:
        errors.append(f"{relative}: missing single-line description")
    elif len(description) > 1024:
        errors.append(f"{relative}: description exceeds 1024 characters")

    if len(text.splitlines()) > 500:
        errors.append(f"{relative}: SKILL.md exceeds 500 lines")

    if not (path.parent.parent / "README.md").exists():
        errors.append(f"{relative}: category README.md is missing")

    return name or None


def validate_markdown_links(errors: list[str]) -> None:
    root = ROOT.resolve()
    for path in sorted(ROOT.rglob("*.md")):
        if is_skipped(path):
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for target in LINK_PATTERN.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            local_target = target.split("#", 1)[0]
            if not local_target:
                continue
            resolved = (path.parent / local_target).resolve()
            # Out-of-repository pointers are layout docs, not checkout
            # artifacts - CI only has this repository.
            try:
                resolved.relative_to(root)
            except ValueError:
                continue
            if not resolved.exists():
                errors.append(f"{relative}: missing reference {target}")


def validate_bundled_files_are_named(errors: list[str]) -> None:
    """Every bundled file is named by some Markdown in its own Skill.

    `validate_markdown_links` checks the other direction: that a reference
    resolves. Nothing checked that a shipped file is mentioned at all, so
    `templates/claude-hooks.md` sat unnamed from the release that added it -
    the prose described the mechanism, the finished template was next to it,
    and no reader could get from one to the other.

    Deliberately weaker than true reachability: a mention anywhere in the
    Skill's Markdown counts, by Skill-relative path or by bare file name, and
    the corpus is not walked from `SKILL.md`. Two orphans naming each other
    would pass, and a bare name that is also a common word could pass
    incidentally. A transitive walk costs more than the defect is worth; this
    catches the file nobody mentions at all, which is the one that shipped.

    Bare names count because a mention is not always a link: a script invoked
    as `scripts/harvest.sh` inside a code fence is named, not linked.

    Candidates come from git, not from a filesystem walk - otherwise
    `.DS_Store` and `__pycache__` become audit failures with an instruction
    nobody can follow.
    """
    known = set(repository_paths())
    for skill in sorted(SKILLS_ROOT.rglob("SKILL.md")):
        root = skill.parent
        prose = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(root.rglob("*.md"))
            if path in known and not is_skipped(path)
        )
        for path in sorted(root.rglob("*")):
            if path not in known or not path.is_file():
                continue
            if path.name == "SKILL.md" or is_skipped(path):
                continue
            relative = path.relative_to(root).as_posix()
            if relative in prose or path.name in prose:
                continue
            errors.append(
                f"{skill.parent.name}: bundled file is named by no Markdown in "
                f"this Skill ({relative}); mention it from the Skill, or remove it"
            )


def validate_plain_punctuation(errors: list[str]) -> None:
    """Flag banned typography using the canonical table.

    The rule is not "ASCII only": natural-language letters, arrows, box
    drawing, and math or currency signs stay allowed. Run
    `python3 scripts/verify-plain-punctuation.py --list-policy` for the exact
    table, or `--fix` to rewrite offenders.
    """
    for path in sorted(ROOT.rglob("*")):
        if is_skipped(path):
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTS:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for line, column, code in punctuation.findings(text):
            category, name, replacement = punctuation.BANNED[code]
            spelling = f"use {replacement!r}" if replacement else "remove it"
            errors.append(
                f"{relative}:{line}:{column}: {category} U+{code:04X} ({name}); "
                f"{spelling}"
            )


def prose_slop_matches(line: str) -> list[tuple[str, re.Match[str]]]:
    if PROSE_AUDIT_ALLOW in line or line.lstrip().startswith(">"):
        return []
    prose = INLINE_CODE_PATTERN.sub("", line)
    return [
        (label, match)
        for label, pattern in PROSE_SLOP_PATTERNS.items()
        if (match := pattern.search(prose))
    ]


def markdown_prose_lines(text: str):
    fence_char = ""
    fence_length = 0
    for line_number, line in enumerate(text.splitlines(), 1):
        fence = FENCE_PATTERN.match(line)
        if fence_char:
            if fence:
                marker = fence.group("marker")
                if (
                    marker[0] == fence_char
                    and len(marker) >= fence_length
                    and not line[fence.end() :].strip()
                ):
                    fence_char = ""
                    fence_length = 0
            continue
        if fence:
            marker = fence.group("marker")
            fence_char = marker[0]
            fence_length = len(marker)
            continue
        yield line_number, line


def validate_prose_matcher(errors: list[str]) -> None:
    for expected_label, sample in PROSE_SLOP_POSITIVE_SAMPLES.items():
        labels = {label for label, _ in prose_slop_matches(sample)}
        if expected_label not in labels:
            errors.append(
                "scripts/audit-skills.py: prose matcher missed positive sample "
                f"for {expected_label!r}: {sample!r}"
            )
    for sample in PROSE_SLOP_NEGATIVE_SAMPLES:
        matches = prose_slop_matches(sample)
        if matches:
            labels = ", ".join(label for label, _ in matches)
            errors.append(
                "scripts/audit-skills.py: prose matcher rejected negative sample "
                f"{sample!r}: {labels}"
            )
    for sample in PROSE_FENCE_NEGATIVE_SAMPLES:
        if any(prose_slop_matches(line) for _, line in markdown_prose_lines(sample)):
            errors.append(
                "scripts/audit-skills.py: prose matcher scanned fenced code "
                f"in {sample!r}"
            )


def repository_paths(pattern: str = "*") -> list[Path]:
    """Files git knows about: tracked, plus untracked that is not ignored.

    Walking the filesystem instead would pick up `.DS_Store`, `__pycache__`,
    and every other local artifact, and no validator wants to judge those.
    """
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
            "--",
            pattern,
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode == 0:
        return [
            ROOT / path.decode("utf-8")
            for path in result.stdout.split(b"\0")
            if path
        ]
    return sorted(ROOT.rglob(pattern))


def repository_markdown_paths() -> list[Path]:
    return repository_paths("*.md")


def validate_prose_style(errors: list[str]) -> None:
    for path in repository_markdown_paths():
        if not path.is_file() or is_skipped(path):
            continue
        relative = path.relative_to(ROOT)
        for line_number, line in markdown_prose_lines(
            path.read_text(encoding="utf-8")
        ):
            for label, match in prose_slop_matches(line):
                errors.append(
                    f"{relative}:{line_number}: AI-slop phrase "
                    f"{match.group(0)!r} ({label}); name the concrete effect"
                )


def validate_lock(skill_paths: list[Path], errors: list[str]) -> None:
    try:
        entries = json.loads(LOCK_PATH.read_text(encoding="utf-8"))["skills"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        errors.append(f"skills-lock.json: invalid: {exc}")
        return

    discovered = {
        path.parent.name: path.relative_to(ROOT).as_posix() for path in skill_paths
    }
    indexed = {
        name: entry.get("skillPath")
        for name, entry in entries.items()
        if isinstance(entry, dict)
    }

    for name in sorted(discovered.keys() - indexed.keys()):
        errors.append(f"skills-lock.json: missing skill {name}")
    for name in sorted(indexed.keys() - discovered.keys()):
        errors.append(f"skills-lock.json: orphaned skill {name}")
    for name in sorted(discovered.keys() & indexed.keys()):
        if indexed[name] != discovered[name]:
            errors.append(
                f"skills-lock.json: {name} points to {indexed[name]!r}, "
                f"expected {discovered[name]!r}"
            )
        version = entries[name].get("version")
        if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
            errors.append(
                f"skills-lock.json: {name} has invalid semantic version {version!r}"
            )


def main() -> int:
    errors: list[str] = []
    skill_paths = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    names = [validate_skill(path, errors) for path in skill_paths]
    present_names = [name for name in names if name]
    for name in sorted({name for name in present_names if present_names.count(name) > 1}):
        errors.append(f"duplicate skill name: {name}")

    validate_markdown_links(errors)
    validate_bundled_files_are_named(errors)
    validate_plain_punctuation(errors)
    validate_prose_matcher(errors)
    validate_prose_style(errors)
    validate_lock(skill_paths, errors)

    if errors:
        print(f"Skill audit failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    description_lengths = [
        len(frontmatter(path, path.read_text(encoding="utf-8"), []).get("description", ""))
        for path in skill_paths
    ]
    print(
        f"Skill audit passed: {len(skill_paths)} skills; "
        f"{sum(description_lengths)} description characters "
        f"(longest {max(description_lengths, default=0)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
