#!/usr/bin/env python3
"""Refuse a branch that changes a Skill without giving it a new version.

Two pull requests that raise the same Skill to the same version change its
`skills-lock.json` line identically, so Git merges both without a conflict and
one change lands under a version whose immutable tag does not contain it. Run
against the current base of a pull request: every Skill whose files the branch
changed needs a version above the base's, and one no tag has taken yet.

Usage: python3 scripts/check-version-bumps.py [--base origin/main]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = "skills-lock.json"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def _lock_at(repo: Path, ref: str) -> dict[str, dict[str, str]]:
    try:
        text = _git(repo, "show", f"{ref}:{LOCK}")
    except subprocess.CalledProcessError:
        return {}
    skills: dict[str, dict[str, str]] = json.loads(text).get("skills", {})
    return skills


def _version(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in text.split("."))


def problems(repo: Path, base: str) -> list[str]:
    """What the branch at HEAD gets wrong about versions, compared with `base`."""
    head, at_base = _lock_at(repo, "HEAD"), _lock_at(repo, base)
    # Files the branch itself changed: from where it left the base, so a change
    # that landed on the base meanwhile is not counted as the branch's.
    fork = _git(repo, "merge-base", base, "HEAD")
    changed = _git(repo, "diff", "--name-only", fork, "HEAD").splitlines()
    found: list[str] = []
    for name, entry in sorted(head.items()):
        if entry.get("source") != "local" or "skillPath" not in entry:
            continue
        folder = str(Path(entry["skillPath"]).parent) + "/"
        if not any(path.startswith(folder) for path in changed):
            continue
        version = entry.get("version", "")
        before = at_base.get(name, {}).get("version")
        # Against the base as it is now, not as the branch found it: the race is
        # another change raising the same Skill to the same version first.
        if before is not None and _version(version) <= _version(before):
            found.append(
                f"{name}: files changed but version {version} is not above {before} on {base};"
                " raise it in skills-lock.json"
            )
            continue
        tag = f"{name}-v{version}"
        if _git(repo, "tag", "--list", tag):
            found.append(f"{name}: tag {tag} already exists; raise the version past it")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default="origin/main", help="the branch the change merges into")
    args = parser.parse_args()
    found = problems(ROOT, args.base)
    for problem in found:
        print(problem, file=sys.stderr)
    if found:
        return 1
    print(f"VERSION BUMPS OK against {args.base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
