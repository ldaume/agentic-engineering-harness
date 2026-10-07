"""Tests for the portfolio pointer gate.

This catalog is public and portable. It must not know the maintainer's
private coordinators, workspaces, machine paths, company, or member
repositories: a pointer to any of them is a leak for every consumer and a
dead reference for all but one machine. The gate holds those names only as
hashes, so the gate itself does not publish them; these tests use stand-in
names.
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

STAND_INS = ("acme-coordinator", "forge.acme.example", "acme", "workspace7")


class PortfolioPointerLines(unittest.TestCase):
    def setUp(self) -> None:
        self._real = audit.PORTFOLIO_NAME_HASHES
        audit.PORTFOLIO_NAME_HASHES = frozenset(audit.portfolio_hash(n) for n in STAND_INS)

    def tearDown(self) -> None:
        audit.PORTFOLIO_NAME_HASHES = self._real

    def test_given_a_pointer_into_a_portfolio_when_scanned_then_it_is_named(self) -> None:
        for line in (
            "read ../acme-coordinator/HARNESS.md",
            "see ACME-Coordinator for the company rules",
            "cd /Users/someone/thing",
            "the members live under ~/dev/private/workspace7/",
            "origin ssh://git@forge.acme.example:2221/x/y",
            "coordinated by ACME-Digital",
            "deploy the acme-hub member",
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
            "acmeish names and forge.example.org are not on the list",
        ):
            with self.subTest(line=line):
                self.assertEqual(audit.portfolio_pointer_reasons(line), [], line)

    def test_the_reason_does_not_repeat_the_hidden_name(self) -> None:
        reasons = audit.portfolio_pointer_reasons("see acme-coordinator")
        self.assertTrue(reasons)
        self.assertFalse(any("acme" in reason for reason in reasons), reasons)


class TheGateItself(unittest.TestCase):
    def test_the_gate_carries_hashes_not_names(self) -> None:
        self.assertTrue(audit.PORTFOLIO_NAME_HASHES)
        for digest in audit.PORTFOLIO_NAME_HASHES:
            self.assertRegex(digest, r"^[0-9a-f]{64}$")


class ThisCatalog(unittest.TestCase):
    def test_the_catalog_itself_is_clean(self) -> None:
        errors: list[str] = []
        audit.validate_no_portfolio_pointers(errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
