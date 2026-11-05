"""Lint a user-flow spec: its Mermaid state diagram and its required sections.

Usage: flow_lint.py FLOW.md

Errors (exit 1): no `stateDiagram` block, a state unreachable from the start,
a state with no way out (it never reaches an end), because both mean the
flow, as drawn, strands a person. Warnings: no error or recovery state, or a
missing section, because a flow drawn only as the happy path hides the cases
engineering will meet first.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

BLOCK = re.compile(r"```mermaid\s*\n\s*stateDiagram(?:-v2)?\s*\n(.*?)```", re.S)
EDGE = re.compile(r"^\s*(\[\*\]|[\w.-]+)\s*-->\s*(\[\*\]|[\w.-]+)\s*(?::\s*(.*))?$")
ERRORISH = re.compile(r"(?i)error|fail|timeout|expired|denied|conflict|offline|invalid|rejected|fehler|abgelaufen")
SECTIONS = {
    "Happy path": r"happy path|hauptweg|hauptpfad",
    "Alternative paths": r"alternative (paths?|wege?)",
    "Error and recovery": r"error|recovery|fehler|wiederherstellung",
    "Interruptions and resume": r"interruption|resume|unterbrechung|wiederaufnahme",
    "States": r"states|zustände",
}
START, END = "[*]", "[*]"


def lint(text: str) -> tuple[list[str], list[str]]:
    blocks = BLOCK.findall(text)
    if not blocks:
        return ["no ```mermaid stateDiagram-v2 block found"], []
    out: dict[str, set[str]] = defaultdict(set)
    rev: dict[str, set[str]] = defaultdict(set)
    states: set[str] = set()
    labels: list[str] = []
    for line in "\n".join(blocks).splitlines():
        m = EDGE.match(line)
        if not m:
            continue
        a, b, label = m.group(1), m.group(2), m.group(3) or ""
        # [*] on the left is the start, on the right the end; keep them apart.
        a = "__start__" if a == START else a
        b = "__end__" if b == END else b
        out[a].add(b)
        rev[b].add(a)
        states |= {a, b}
        labels.append(f"{a} {b} {label}")
    states -= {"__start__", "__end__"}

    def walk(seed: str, graph: dict[str, set[str]]) -> set[str]:
        seen, stack = set(), [seed]
        while stack:
            for nxt in graph[stack.pop()]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    errors = [f"state {s} is unreachable from the start" for s in sorted(states - walk("__start__", out))]
    errors += [f"state {s} has no way out to an end" for s in sorted(states - walk("__end__", rev))]

    warnings = []
    if not any(ERRORISH.search(x) for x in labels):
        warnings.append("no error or recovery state or transition; add the failure cases")
    headings = " ".join(re.findall(r"(?m)^#+\s*(.+)$", text)).lower()
    for name, pattern in SECTIONS.items():
        if not re.search(pattern, headings):
            warnings.append(f"missing section: {name}")
    return errors, warnings


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 2
    errors, warnings = lint(Path(argv[0]).read_text(encoding="utf-8"))
    for e in errors:
        print(f"ERROR {e}")
    for w in warnings:
        print(f"warn  {w}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
