#!/usr/bin/env python3
"""Fail on typographic characters that do not belong in tracked plain text.

Scope: the small set of quotes, dashes, ellipses, exotic spaces, invisible
format characters, and decorative separators that editors, terminals, and
diffs render ambiguously. Those characters are also the most common tell that
prose was pasted out of a rich-text or model surface instead of written into
the repository.

Not in scope: every non-ASCII character. Functional symbols (arrows, box
drawing, math, currency) and natural-language letters (umlauts, accents) stay
allowed. Ban a character here only when its ASCII spelling is strictly better.

Usage:

    python3 scripts/verify-plain-punctuation.py               # repo at cwd
    python3 <catalog>/scripts/verify-plain-punctuation.py     # from any repo
    python3 scripts/verify-plain-punctuation.py PATH [PATH..] # named repos
    python3 scripts/verify-plain-punctuation.py --fix
    python3 scripts/verify-plain-punctuation.py --list-policy

Default scope is Git-tracked files. `--include-untracked` adds untracked files
that are not ignored. Binary files are skipped.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# code point -> (category, name, ASCII replacement)
# Never write a banned character literally in this file; use escapes.
BANNED: dict[int, tuple[str, str, str]] = {}


def _ban(category: str, entries: dict[int, tuple[str, str]]) -> None:
    for code, (name, replacement) in entries.items():
        BANNED[code] = (category, name, replacement)


_ban(
    "quote",
    {
        0x2018: ("LEFT SINGLE QUOTATION MARK", "'"),
        0x2019: ("RIGHT SINGLE QUOTATION MARK", "'"),
        0x201A: ("SINGLE LOW-9 QUOTATION MARK", "'"),
        0x201B: ("SINGLE HIGH-REVERSED-9 QUOTATION MARK", "'"),
        0x201C: ("LEFT DOUBLE QUOTATION MARK", '"'),
        0x201D: ("RIGHT DOUBLE QUOTATION MARK", '"'),
        0x201E: ("DOUBLE LOW-9 QUOTATION MARK", '"'),
        0x201F: ("DOUBLE HIGH-REVERSED-9 QUOTATION MARK", '"'),
        0x2032: ("PRIME", "'"),
        0x2033: ("DOUBLE PRIME", '"'),
        0x00AB: ("LEFT-POINTING DOUBLE ANGLE QUOTATION MARK", '"'),
        0x00BB: ("RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK", '"'),
    },
)
# Em dash, en dash, figure dash, horizontal bar and the multi-em dashes are
# deliberately absent. They were banned as the common tell that prose came out
# of a model; they are also ordinary correct typography, an em dash in English
# most of all, and the tell has stopped being reliable. A reader sees a
# considered choice, so this gate has no business calling it a defect
# (owner decision, 2026-09-11).
#
# What stays is the look-alike group: a reader cannot tell these from `-`, and
# every tool can. `U+2010` in "well-known" makes the word unfindable by the
# spelling everyone types, and the diff that introduced it shows nothing. That
# is a different problem from typography and it keeps its own justification.
_ban(
    "dash look-alike",
    {
        0x2010: ("HYPHEN", "-"),
        0x2011: ("NON-BREAKING HYPHEN", "-"),
        0x2212: ("MINUS SIGN", "-"),
    },
)
_ban("ellipsis", {0x2026: ("HORIZONTAL ELLIPSIS", "...")})
_ban(
    "space",
    {
        0x00A0: ("NO-BREAK SPACE", " "),
        0x1680: ("OGHAM SPACE MARK", " "),
        0x2000: ("EN QUAD", " "),
        0x2001: ("EM QUAD", " "),
        0x2002: ("EN SPACE", " "),
        0x2003: ("EM SPACE", " "),
        0x2004: ("THREE-PER-EM SPACE", " "),
        0x2005: ("FOUR-PER-EM SPACE", " "),
        0x2006: ("SIX-PER-EM SPACE", " "),
        0x2007: ("FIGURE SPACE", " "),
        0x2008: ("PUNCTUATION SPACE", " "),
        0x2009: ("THIN SPACE", " "),
        0x200A: ("HAIR SPACE", " "),
        0x202F: ("NARROW NO-BREAK SPACE", " "),
        0x205F: ("MEDIUM MATHEMATICAL SPACE", " "),
        0x3000: ("IDEOGRAPHIC SPACE", " "),
    },
)
_ban(
    "invisible",
    {
        0x00AD: ("SOFT HYPHEN", ""),
        0x180E: ("MONGOLIAN VOWEL SEPARATOR", ""),
        0x200B: ("ZERO WIDTH SPACE", ""),
        0x200C: ("ZERO WIDTH NON-JOINER", ""),
        0x200D: ("ZERO WIDTH JOINER", ""),
        0x200E: ("LEFT-TO-RIGHT MARK", ""),
        0x200F: ("RIGHT-TO-LEFT MARK", ""),
        0x2060: ("WORD JOINER", ""),
        0x2061: ("FUNCTION APPLICATION", ""),
        0x2062: ("INVISIBLE TIMES", ""),
        0x2063: ("INVISIBLE SEPARATOR", ""),
        0x2064: ("INVISIBLE PLUS", ""),
        0xFEFF: ("ZERO WIDTH NO-BREAK SPACE / BOM", ""),
        0x061C: ("ARABIC LETTER MARK", ""),
        0x2028: ("LINE SEPARATOR", "\n"),
        0x2029: ("PARAGRAPH SEPARATOR", "\n"),
        0x202A: ("LEFT-TO-RIGHT EMBEDDING", ""),
        0x202B: ("RIGHT-TO-LEFT EMBEDDING", ""),
        0x202C: ("POP DIRECTIONAL FORMATTING", ""),
        0x202D: ("LEFT-TO-RIGHT OVERRIDE", ""),
        0x202E: ("RIGHT-TO-LEFT OVERRIDE", ""),
        0x2066: ("LEFT-TO-RIGHT ISOLATE", ""),
        0x2067: ("RIGHT-TO-LEFT ISOLATE", ""),
        0x2068: ("FIRST STRONG ISOLATE", ""),
        0x2069: ("POP DIRECTIONAL ISOLATE", ""),
    },
)
_ban(
    "separator",
    {
        0x00B7: ("MIDDLE DOT", "-"),
        0x2022: ("BULLET", "-"),
        0x2023: ("TRIANGULAR BULLET", "-"),
        0x2043: ("HYPHEN BULLET", "-"),
        0x2219: ("BULLET OPERATOR", "-"),
        0x25CF: ("BLACK CIRCLE", "-"),
    },
)

BINARY_SNIFF_BYTES = 8192


def repo_root(start: Path) -> Path | None:
    proc = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return Path(proc.stdout.strip())


def repo_files(root: Path, include_untracked: bool) -> list[Path]:
    command = ["git", "-C", str(root), "ls-files", "-z"]
    if include_untracked:
        command += ["--cached", "--others", "--exclude-standard"]
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return []
    return [
        root / name
        for name in proc.stdout.split("\0")
        if name and (root / name).is_file()
    ]


def read_text(path: Path) -> str | None:
    """Return file text, or None when the file is binary or undecodable."""
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\0" in raw[:BINARY_SNIFF_BYTES]:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def findings(text: str) -> list[tuple[int, int, int]]:
    """Return (line, column, code point) for every banned character."""
    hits: list[tuple[int, int, int]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for column, char in enumerate(line, start=1):
            if ord(char) in BANNED:
                hits.append((line_number, column, ord(char)))
    return hits


def repair(text: str, *, json_string_escaping: bool = False) -> str:
    """Substitute banned characters. Never rewrite the words around them.

    `json_string_escaping` is for a file whose text is JSON: a straight double
    quote inside a JSON string value has to be escaped, so writing `"` there
    turns a valid document into a broken one. Found the hard way - a run over
    a translation file produced `"Suggestion for "{title}""`, which a pre-commit
    hook rejected and a less careful pipeline would have committed.
    """
    for code, (_category, _name, replacement) in BANNED.items():
        char = chr(code)
        if char not in text:
            continue
        if json_string_escaping:
            # Inside a JSON string a quote and a newline are both syntax: one
            # ends the string, the other is an illegal raw control character.
            # Write the escape the format spells them with.
            replacement = {'"': '\\"', "\n": "\\n"}.get(replacement, replacement)
        text = text.replace(char, replacement)
    return text


def repair_file_text(text: str, relative: str) -> tuple[str, str | None]:
    """Repair one file's text, or refuse and say why.

    A repair that produces a file the parser rejects is worse than the finding
    it fixed. `--fix` is a convenience, never a license to corrupt.

    Two defenses, because the second one cannot always run. Characters that
    are syntax inside a JSON string - the double quote, and the newline that
    replaces a line separator - are written as the escape the format spells
    them with, so the repair stays inside the string it belongs to. Then the
    result is re-parsed and the original kept if it no longer loads. A
    `.jsonc` file has comments, so it is not JSON and cannot be re-parsed:
    there the escaping is the only defense, which is why it has to be right
    rather than merely backed up.
    """
    is_json = relative.endswith((".json", ".jsonc"))
    fixed = repair(text, json_string_escaping=is_json)
    if is_json and not relative.endswith(".jsonc"):
        import json as _json

        try:
            _json.loads(fixed)
        except ValueError as exc:
            return text, f"{relative}: refused, the repair would not parse as JSON ({exc})"
    return fixed, None


def describe(code: int) -> str:
    category, name, replacement = BANNED[code]
    shown = "remove" if replacement == "" else f'use "{replacement}"'
    if replacement == "\n":
        shown = "use a newline"
    return f"U+{code:04X} {name} ({category}); {shown}"


def scan_repo(
    root: Path, include_untracked: bool, fix: bool
) -> tuple[list[str], list[str], int, int]:
    """Return (errors, fixed relative paths, checked count, skipped count)."""
    errors: list[str] = []
    fixed: list[str] = []
    checked = 0
    skipped = 0
    for path in sorted(repo_files(root, include_untracked)):
        text = read_text(path)
        if text is None:
            skipped += 1
            continue
        checked += 1
        hits = findings(text)
        if not hits:
            continue
        relative = path.relative_to(root).as_posix()
        if fix:
            repaired, refusal = repair_file_text(text, str(relative))
            if refusal:
                errors.append(refusal)
                continue
            path.write_text(repaired, encoding="utf-8")
            fixed.append(relative)
            continue
        for line_number, column, code in hits:
            errors.append(f"{relative}:{line_number}:{column}: {describe(code)}")
    return errors, fixed, checked, skipped


def print_policy() -> None:
    print("Banned in tracked plain text (ASCII spelling is canonical):")
    for code in sorted(BANNED):
        category, name, replacement = BANNED[code]
        shown = "(remove)" if replacement == "" else repr(replacement)
        print(f"  U+{code:04X}  {category:10s}  {name}  -> {shown}")
    print()
    print("Allowed: arrows, box drawing, math and currency symbols, and")
    print("natural-language letters such as umlauts and accents.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        help="Repository paths to scan (default: the repository at cwd)",
    )
    parser.add_argument(
        "--include-untracked",
        action="store_true",
        help="Also scan untracked files that are not ignored",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Rewrite offending files with the ASCII spelling",
    )
    parser.add_argument(
        "--list-policy",
        action="store_true",
        help="Print the banned character table and exit",
    )
    args = parser.parse_args()

    if args.list_policy:
        print_policy()
        return 0

    starts = [Path(p) for p in args.paths] or [Path.cwd()]
    errors: list[str] = []
    fixed: list[str] = []
    checked = skipped = 0
    roots: list[Path] = []
    for start in starts:
        if not start.is_dir():
            errors.append(f"not a directory: {start}")
            continue
        root = repo_root(start)
        if root is None:
            errors.append(f"not a Git repository: {start}")
            continue
        if root in roots:
            continue
        roots.append(root)
        repo_errors, repo_fixed, repo_checked, repo_skipped = scan_repo(
            root, args.include_untracked, args.fix
        )
        label = root.name
        errors += [f"{label}: {item}" for item in repo_errors]
        fixed += [f"{label}: {item}" for item in repo_fixed]
        checked += repo_checked
        skipped += repo_skipped

    if fixed:
        print(f"PLAIN PUNCTUATION FIXED ({len(fixed)} file(s))")
        for item in fixed:
            print(f"  - {item}")

    if errors:
        print("PLAIN PUNCTUATION FAIL")
        for item in errors:
            print(f"  - {item}")
        return 1

    print(f"PLAIN PUNCTUATION OK ({checked} file(s) checked, {skipped} binary)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
