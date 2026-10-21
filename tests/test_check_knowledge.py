"""Tests for the knowledge-base check.

A golden path is only as trustworthy as the source behind each rule. These
tests pin the two failure modes that make a knowledge base silently rot: a
rule citing a source that is not in the registry, and a registry entry that
cannot be re-checked because it lacks an access date or revisit trigger.
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("check_knowledge", ROOT / "scripts" / "check-knowledge.py")
assert _spec and _spec.loader
ck = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ck)

SOURCE = {
    "id": "SRC-A11Y-001",
    "title": "Web Content Accessibility Guidelines 2.2",
    "url": "https://www.w3.org/TR/WCAG22/",
    "publisher": "W3C",
    "published": "2024-12-12",
    "accessed": "2026-10-21",
    "type": "standard",
    "domains": ["accessibility"],
    "findings": ["3.3.1 requires identifying an input error in text."],
    "limits": "Conformance criteria, not usability evidence.",
    "evidence_level": "verified",
    "revisit": "WCAG 3 reaches Candidate Recommendation.",
}


def family(sources: list[dict], reference: str) -> Path:
    root = Path(tempfile.mkdtemp())
    core = root / "progressive-x-core" / "references"
    core.mkdir(parents=True)
    (core / "sources.json").write_text(json.dumps({"version": 1, "sources": sources}))
    (core / "rules.md").write_text(reference)
    return root


class CheckKnowledge(unittest.TestCase):
    def test_given_cited_and_complete_source_when_checked_then_no_errors(self) -> None:
        errors, warnings = ck.check(family([SOURCE], "Show errors in text [SRC-A11Y-001]."))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_given_citation_missing_from_registry_when_checked_then_error(self) -> None:
        errors, _ = ck.check(family([SOURCE], "Rule [SRC-A11Y-001] and [SRC-A11Y-404]."))
        self.assertTrue(any("SRC-A11Y-404" in e for e in errors))

    def test_given_source_without_access_date_when_checked_then_error(self) -> None:
        broken = {k: v for k, v in SOURCE.items() if k != "accessed"}
        errors, _ = ck.check(family([broken], "[SRC-A11Y-001]"))
        self.assertTrue(any("accessed" in e for e in errors))

    def test_given_unknown_evidence_level_when_checked_then_error(self) -> None:
        errors, _ = ck.check(family([{**SOURCE, "evidence_level": "obvious"}], "[SRC-A11Y-001]"))
        self.assertTrue(any("evidence_level" in e for e in errors))

    def test_given_duplicate_id_when_checked_then_error(self) -> None:
        errors, _ = ck.check(family([SOURCE, SOURCE], "[SRC-A11Y-001]"))
        self.assertTrue(any("duplicate" in e for e in errors))

    def test_given_uncited_source_when_checked_then_warning_only(self) -> None:
        other = {**SOURCE, "id": "SRC-A11Y-002"}
        errors, warnings = ck.check(family([SOURCE, other], "[SRC-A11Y-001]"))
        self.assertEqual(errors, [])
        self.assertTrue(any("SRC-A11Y-002" in w for w in warnings))

    def test_given_written_level_stronger_than_registry_when_checked_then_error(self) -> None:
        weak = {**SOURCE, "evidence_level": "context-dependent"}
        errors, _ = ck.check(family([weak], "Do this (verified) [SRC-A11Y-001]."))
        self.assertTrue(any("stronger" in e for e in errors))

    def test_given_mixed_group_when_checked_then_strongest_source_sets_the_ceiling(self) -> None:
        weak = {**SOURCE, "id": "SRC-A11Y-002", "evidence_level": "context-dependent"}
        errors, _ = ck.check(family([SOURCE, weak], "Rule (verified) [SRC-A11Y-001] [SRC-A11Y-002]."))
        self.assertEqual(errors, [])

    def test_given_written_level_equal_or_weaker_when_checked_then_no_error(self) -> None:
        errors, _ = ck.check(family([SOURCE], "Do this (supported) [SRC-A11Y-001] and\nthat (verified for the rule)\n[SRC-A11Y-001]."))
        self.assertEqual(errors, [])

    def test_given_the_catalog_when_checked_then_every_registry_passes(self) -> None:
        for registry in sorted((ROOT / "skills").rglob("references/sources.json")):
            errors, _ = ck.check(registry.parents[2])
            self.assertEqual(errors, [], registry)


if __name__ == "__main__":
    unittest.main()
