"""Tests for the knowledge-base check.

A golden path is only as trustworthy as the source behind each rule. These
tests pin the two failure modes that make a knowledge base silently rot: a
rule citing a source that is not in the registry, and a registry entry that
cannot be re-checked because it lacks an access date or revisit trigger.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
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

    def test_given_citation_registered_in_another_family_when_checked_then_resolved(self) -> None:
        own = {**SOURCE, "id": "SRC-EST-001"}
        errors, _ = ck.check(family([own], "[SRC-EST-001] and (verified) [SRC-A11Y-001]."),
                             catalog={"SRC-A11Y-001": "verified"})
        self.assertEqual(errors, [])

    def test_given_stronger_claim_for_another_familys_source_when_checked_then_error(self) -> None:
        own = {**SOURCE, "id": "SRC-EST-001"}
        errors, _ = ck.check(family([own], "[SRC-EST-001] and (verified) [SRC-A11Y-001]."),
                             catalog={"SRC-A11Y-001": "supported"})
        self.assertTrue(any("SRC-A11Y-001" in e for e in errors))

    def test_given_the_catalog_when_checked_then_every_registry_passes(self) -> None:
        catalog = ck.catalog_levels(ROOT / "skills")
        for registry in sorted((ROOT / "skills").rglob("references/sources.json")):
            errors, _ = ck.check(registry.parents[2], catalog=catalog)
            self.assertEqual(errors, [], registry)


HEADER = "| Term | Definition | Source | Marker | Check |\n|---|---|---|---|---|\n"
ROW = "| Measure | Characters per line. | [SRC-A11Y-001] | Median characters per line of body text. | exact `wcag.lineLength` |\n"


def skill(root: Path, name: str, frontmatter: str = "", body: str = "", vocabulary: str | None = None) -> Path:
    directory = root / "design" / name
    (directory / "references").mkdir(parents=True, exist_ok=True)
    (directory / "SKILL.md").write_text(f"---\nname: {name}\ndescription: x\n{frontmatter}---\n\n{body}\n")
    if vocabulary is not None:
        (directory / "references" / "vocabulary.md").write_text(vocabulary)
    return directory


class CheckVocabulary(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.known = {"SRC-A11Y-001"}

    def check(self, directory: Path) -> tuple[list[str], list[str]]:
        return ck.check_vocabulary(directory, self.known)

    def test_given_complete_rows_when_checked_then_no_findings(self) -> None:
        errors, warnings = self.check(skill(self.root, "design-core", vocabulary=HEADER + ROW))
        self.assertEqual((errors, warnings), ([], []))

    def test_given_row_missing_a_cell_when_checked_then_error(self) -> None:
        row = "| Leading | Baseline distance. | [SRC-A11Y-001] | | jev |\n"
        errors, _ = self.check(skill(self.root, "design-core", vocabulary=HEADER + row))
        self.assertTrue(any("Leading" in e and "cell" in e for e in errors), errors)

    def test_given_unknown_source_when_checked_then_error(self) -> None:
        row = ROW.replace("SRC-A11Y-001", "SRC-A11Y-404")
        errors, _ = self.check(skill(self.root, "design-core", vocabulary=HEADER + row))
        self.assertTrue(any("SRC-A11Y-404" in e for e in errors), errors)

    def test_given_row_without_source_when_checked_then_error(self) -> None:
        row = ROW.replace("[SRC-A11Y-001]", "Butterick")
        errors, _ = self.check(skill(self.root, "design-core", vocabulary=HEADER + row))
        self.assertTrue(any("source" in e for e in errors), errors)

    def test_given_bad_check_value_when_checked_then_error(self) -> None:
        row = ROW.replace("exact `wcag.lineLength`", "DOM")
        errors, _ = self.check(skill(self.root, "design-core", vocabulary=HEADER + row))
        self.assertTrue(any("Check" in e for e in errors), errors)

    def test_given_more_than_forty_rows_when_checked_then_error(self) -> None:
        rows = "".join(ROW.replace("Measure", f"Term {i}") for i in range(41))
        errors, _ = self.check(skill(self.root, "design-core", vocabulary=HEADER + rows))
        self.assertTrue(any("41 terms" in e for e in errors), errors)

    def test_given_more_than_eighty_lines_when_checked_then_error(self) -> None:
        errors, _ = self.check(skill(self.root, "design-core", vocabulary=HEADER + ROW + "\n" * 80))
        self.assertTrue(any("lines" in e for e in errors), errors)

    def test_given_duplicate_term_when_checked_then_error(self) -> None:
        errors, _ = self.check(skill(self.root, "design-core", vocabulary=HEADER + ROW + ROW.replace("Measure", "measure")))
        self.assertTrue(any("duplicate" in e for e in errors), errors)

    def test_given_exact_row_without_rule_id_when_checked_then_warning(self) -> None:
        row = ROW.replace("exact `wcag.lineLength`", "exact")
        errors, warnings = self.check(skill(self.root, "design-core", vocabulary=HEADER + row))
        self.assertEqual(errors, [])
        self.assertTrue(any("Measure" in w and "rule id" in w for w in warnings), warnings)

    def test_given_skill_without_vocabulary_or_exemption_when_checked_then_warning(self) -> None:
        errors, warnings = self.check(skill(self.root, "design-web"))
        self.assertEqual(errors, [])
        self.assertTrue(any("vocabulary" in w for w in warnings), warnings)

    def test_given_vendor_exemption_when_checked_then_no_findings(self) -> None:
        directory = skill(self.root, "gitea-tea", frontmatter="metadata:\n  vocabulary: vendor\n")
        self.assertEqual(self.check(directory), ([], []))

    def test_given_metadata_naming_a_sibling_with_a_vocabulary_when_checked_then_no_findings(self) -> None:
        skill(self.root, "design-core", vocabulary=HEADER + ROW)
        directory = skill(self.root, "design-web", frontmatter="metadata:\n  vocabulary: design-core\n")
        self.assertEqual(self.check(directory), ([], []))

    def test_given_metadata_naming_a_sibling_without_a_vocabulary_when_checked_then_warning(self) -> None:
        directory = skill(self.root, "design-web", frontmatter="metadata:\n  vocabulary: design-nope\n")
        _, warnings = self.check(directory)
        self.assertTrue(any("vocabulary" in w for w in warnings), warnings)

    def test_given_only_a_body_pointer_to_a_sibling_vocabulary_when_checked_then_warning(self) -> None:
        # Reviews no longer load the vocabulary, so a load-it pointer is not coverage.
        skill(self.root, "design-core", vocabulary=HEADER + ROW)
        directory = skill(self.root, "design-web", body="Load `design-core/references/vocabulary.md` before judging.")
        _, warnings = self.check(directory)
        self.assertTrue(any("vocabulary" in w for w in warnings), warnings)

    def test_given_source_accessed_over_a_year_ago_when_checked_then_warning(self) -> None:
        old = {**SOURCE, "accessed": "2025-11-01"}
        fresh = {**SOURCE, "id": "SRC-A11Y-002", "accessed": "2026-11"}
        warnings = ck.stale_sources(family([old, fresh], ""), today=ck.date(2026, 11, 24))
        self.assertEqual(len(warnings), 1)
        self.assertIn("SRC-A11Y-001", warnings[0])

    def test_given_errors_when_run_without_strict_then_exit_zero(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ck.main(["--vocabulary"]), 0)

    def run_root(self, *flags: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = ck.main(["--vocabulary", "--root", str(self.root), *flags])
        return code, out.getvalue()

    def test_given_a_root_with_one_skill_without_vocabulary_when_checked_then_one_warning(self) -> None:
        skill(self.root / "skills", "html-decks")
        code, out = self.run_root()
        self.assertEqual(code, 0)
        self.assertEqual(out.count("warn "), 1, out)
        self.assertIn("html-decks: no references/vocabulary.md", out)
        self.assertIn("1 skills without a vocabulary", out)

    def test_given_a_skill_without_vocabulary_when_run_strict_then_exit_one(self) -> None:
        skill(self.root / "skills", "html-decks")
        code, _ = self.run_root("--strict")
        self.assertEqual(code, 1)

    def test_given_only_exact_rows_without_rule_id_when_run_strict_then_exit_zero(self) -> None:
        row = ROW.replace("exact `wcag.lineLength`", "exact")
        skill(self.root / "skills", "design-core", vocabulary=HEADER + row)
        (self.root / "skills" / "design" / "design-core" / "references" / "sources.json").write_text(
            json.dumps({"sources": [{**SOURCE, "accessed": ck.date.today().isoformat()}]}))
        code, out = self.run_root("--strict")
        self.assertEqual(code, 0, out)
        self.assertIn("rule id", out)

    def test_given_the_catalog_when_checked_then_every_vocabulary_file_is_valid(self) -> None:
        known = set(ck.catalog_levels(ROOT / "skills"))
        for vocabulary in sorted((ROOT / "skills").rglob("references/vocabulary.md")):
            errors, _ = ck.check_vocabulary(vocabulary.parents[1], known)
            self.assertEqual(errors, [], vocabulary)


if __name__ == "__main__":
    unittest.main()
