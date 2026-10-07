#!/usr/bin/env python3
"""Reject agent attribution on review surfaces: commit messages and pull request bodies.

Template HARNESS.md, Review-surface attribution. Run it in two places: as the
commit-msg hook (fast feedback) and in CI over every commit of a pull request
plus its body, because a hook skipped with --no-verify skips nothing in CI.

  verify-agent-attribution.py --message-file <path>
  verify-agent-attribution.py --range <base>..<head>   (PR_BODY from the environment)

Exit 0 when clean, 1 when attribution was found, 2 on usage errors.
"""

import argparse
import os
import re
import subprocess
import sys

AGENTS = r"claude|anthropic|codex|openai|cursor|copilot|gemini|devin|aider|gpt"
PATTERNS = [
    re.compile(rf"^co-authored-by:.*\b({AGENTS})\b", re.IGNORECASE),
    re.compile(r"(generated|made|created) (with|by|via) \[?(claude|codex|cursor|copilot|gemini)", re.IGNORECASE),
    re.compile(r"^claude-session:", re.IGNORECASE),
]


def agent_attribution(text):
    """The lines of `text` that stamp it as an agent's work."""
    lines = (line.strip() for line in text.splitlines())
    return [line for line in lines if any(p.search(line) for p in PATTERNS)]


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--message-file")
    group.add_argument("--range")
    args = parser.parse_args()

    sources = []
    if args.message_file:
        with open(args.message_file, encoding="utf-8") as handle:
            sources.append(("commit message", handle.read()))
    else:
        for commit in git("rev-list", "--no-merges", args.range).split():
            sources.append((f"commit {commit[:7]}", git("log", "-1", "--format=%B", commit)))
        sources.append(("pull request body", os.environ.get("PR_BODY", "")))

    offenders = [f"{where}: {line}" for where, text in sources for line in agent_attribution(text)]
    if offenders:
        print("Agent attribution found on a review surface; remove these lines:", file=sys.stderr)
        for offender in offenders:
            print(f"  {offender}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
