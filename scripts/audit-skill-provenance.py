#!/usr/bin/env python3
"""Detect likely copied Markdown across local and public Skill packages."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORD_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)?")
FRONTMATTER_PATTERN = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
SHINGLE_SIZE = 5
MIN_WORDS = 80
MIN_SHARED_SHINGLES = 12
CONTAINMENT_LIMIT = 0.82
JACCARD_LIMIT = 0.55


@dataclass(frozen=True)
class Document:
    path: Path
    label: str
    normalized: str
    words: tuple[str, ...]
    shingles: frozenset[tuple[str, ...]]


def normalize(text: str) -> tuple[str, tuple[str, ...]]:
    body = FRONTMATTER_PATTERN.sub("", text.replace("\r\n", "\n"), count=1)
    words = tuple(WORD_PATTERN.findall(body.lower()))
    return " ".join(words), words


def document(path: Path, label: str) -> Document:
    normalized, words = normalize(path.read_text(encoding="utf-8"))
    shingles = frozenset(
        tuple(words[index : index + SHINGLE_SIZE])
        for index in range(max(0, len(words) - SHINGLE_SIZE + 1))
    )
    return Document(path, label, normalized, words, shingles)


def package_markdown(root: Path, label: str) -> list[Document]:
    package_dirs = {path.parent for path in root.rglob("SKILL.md")}
    paths = {
        path.resolve()
        for package_dir in package_dirs
        for path in package_dir.rglob("*.md")
        if ".git" not in path.parts and "node_modules" not in path.parts
    }
    return [document(path, label) for path in sorted(paths)]


def similarity(local: Document, upstream: Document) -> tuple[float, float, int]:
    shared = len(local.shingles & upstream.shingles)
    union = len(local.shingles | upstream.shingles)
    shorter = min(len(local.shingles), len(upstream.shingles))
    jaccard = shared / union if union else 0.0
    containment = shared / shorter if shorter else 0.0
    return jaccard, containment, shared


def likely_copy(local: Document, upstream: Document) -> tuple[bool, str]:
    if local.normalized and local.normalized == upstream.normalized:
        return True, "exact normalized content"

    if min(len(local.words), len(upstream.words)) < MIN_WORDS:
        return False, ""

    jaccard, containment, shared = similarity(local, upstream)
    if shared < MIN_SHARED_SHINGLES:
        return False, ""
    if containment >= CONTAINMENT_LIMIT:
        return True, f"{containment:.0%} shorter-document containment"
    if jaccard >= JACCARD_LIMIT:
        return True, f"{jaccard:.0%} shingle similarity"
    return False, ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare local Skill-package Markdown with one or more checked-out "
            "public Skill repositories."
        )
    )
    parser.add_argument(
        "upstream",
        nargs="+",
        type=Path,
        help="Checked-out public repository root containing SKILL.md files",
    )
    parser.add_argument(
        "--local",
        type=Path,
        default=ROOT / "skills",
        help="Local Skill root (default: this repository's skills/)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    local_root = args.local.resolve()
    if not local_root.is_dir():
        print(f"Local Skill root does not exist: {local_root}", file=sys.stderr)
        return 2

    local_docs = package_markdown(local_root, "local")
    upstream_docs: list[Document] = []
    invalid: list[Path] = []
    for upstream_root in args.upstream:
        resolved = upstream_root.resolve()
        if not resolved.is_dir():
            invalid.append(resolved)
            continue
        upstream_docs.extend(package_markdown(resolved, resolved.name))

    if invalid:
        for path in invalid:
            print(f"Upstream repository does not exist: {path}", file=sys.stderr)
        return 2
    if not upstream_docs:
        print("No upstream Skill-package Markdown found.", file=sys.stderr)
        return 2

    findings: list[tuple[Document, Document, str]] = []
    for local in local_docs:
        for upstream in upstream_docs:
            copied, reason = likely_copy(local, upstream)
            if copied:
                findings.append((local, upstream, reason))

    print(
        f"Compared {len(local_docs)} local Markdown files with "
        f"{len(upstream_docs)} public Skill-package Markdown files."
    )
    if findings:
        print(f"Provenance audit found {len(findings)} likely copy match(es):")
        for local, upstream, reason in findings:
            print(f"- {local.path}: {reason}")
            print(f"  upstream: {upstream.path}")
        return 1

    print("Provenance audit passed: no likely copied public Skill content.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
