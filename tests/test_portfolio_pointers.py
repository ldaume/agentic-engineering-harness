"""Tests for the portfolio pointer gate.

This catalog is public and portable. It must not know the maintainer's
private coordinators, workspaces, machine paths, company, or member
repositories: a pointer to any of them is a leak for every consumer and a
dead reference for all but one machine.
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit-skills.py"

_spec = importlib.util.spec_from_file_location("audit_skills_pointers", SCRIPT)
assert _spec and _spec.loader
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)


class PortfolioPointerLines(unittest.TestCase):
    def test_given_a_pointer_into_a_portfolio_when_scanned_then_it_is_named(self) -> None:
        for line in (
            "read ../private-harness/HARNESS.md",
            "see lennys-harness for the company rules",
            "cd /Users/someone/dev/private/wsp/thing",
            "the workspace under ~/dev/ws/ holds the members",
            "origin ssh://gitea.example.internal:2221/x/y is fine but gitea.daume.dev is not",
            "coordinated by OH-SO-Digital",
            "log hours through craft-gauge",
        ):
            with self.subTest(line=line):
                self.assertTrue(audit.portfolio_pointer_reasons(line), line)

    def test_given_ordinary_catalog_prose_when_scanned_then_nothing_is_named(self) -> None:
        for line in (
            "npx skills add ldaume/agentic-engineering-harness --list",
            "I am Leonard Daume (https://www.daume.dev).",
            "a private repository stays private",
            "the harness coordinator lists its members in CONTEXT-MAP.md",
            "run it from the workspace root",
        ):
            with self.subTest(line=line):
                self.assertEqual(audit.portfolio_pointer_reasons(line), [], line)


class ThisCatalog(unittest.TestCase):
    def test_the_catalog_itself_is_clean(self) -> None:
        errors: list[str] = []
        audit.validate_no_portfolio_pointers(errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
