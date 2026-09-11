"""Tests for the audit's file selection.

`is_skipped` exists because `SKIP_DIRS` was matched against absolute path
parts: a checkout under `.../.worktrees/<task>/` - the isolation default this
catalog's own harness prescribes - made every file-level validator skip every
file while the audit still printed "passed".

Continuous integration cannot catch a regression of that: it checks out at an
ordinary path, where the rule is a no-op whether it is right or wrong. These
assertions are the only guard, and the bug shipped once already.
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit-skills.py"

_spec = importlib.util.spec_from_file_location("audit_skills", SCRIPT)
assert _spec and _spec.loader
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)


class IsSkipped(unittest.TestCase):
    def test_an_ordinary_repository_file_is_inspected(self) -> None:
        self.assertFalse(audit.is_skipped(audit.ROOT / "skills" / "x" / "SKILL.md"))

    def test_a_skipped_directory_inside_the_repository_is_skipped(self) -> None:
        for part in sorted(audit.SKIP_DIRS):
            with self.subTest(part=part):
                self.assertTrue(audit.is_skipped(audit.ROOT / part / "t" / "a.md"))

    def test_a_path_outside_the_repository_is_skipped(self) -> None:
        self.assertTrue(audit.is_skipped(Path("/definitely/outside/a.md")))

    def test_a_checkout_under_a_skipped_name_is_still_inspected(self) -> None:
        # The regression itself, constructed rather than depended on: the
        # repository root may live under a directory whose name is in
        # SKIP_DIRS. Only the path inside the repository may decide.
        original = audit.ROOT
        audit.ROOT = Path("/tmp/ws/.worktrees/catalog-task").resolve()
        try:
            self.assertFalse(audit.is_skipped(audit.ROOT / "skills" / "a" / "SKILL.md"))
            self.assertTrue(audit.is_skipped(audit.ROOT / ".worktrees" / "t" / "a.md"))
        finally:
            audit.ROOT = original

    def test_every_markdown_file_in_this_checkout_is_inspected(self) -> None:
        files = [p for p in audit.ROOT.rglob("*.md") if not audit.is_skipped(p)]
        self.assertEqual(len(files), len(list(audit.ROOT.rglob("*.md"))))


class BundledFilesAreNamed(unittest.TestCase):
    def test_the_catalog_has_no_unnamed_bundled_file(self) -> None:
        errors: list[str] = []
        audit.validate_bundled_files_are_named(errors)
        self.assertEqual(errors, [])

    def test_untracked_local_artifacts_are_not_candidates(self) -> None:
        # A filesystem walk would judge `.DS_Store` and tell the contributor to
        # mention it from the Skill, which is not a thing anyone can do.
        known = set(audit.repository_paths())
        self.assertTrue(known, "git file selection returned nothing")
        self.assertNotIn(audit.ROOT / ".DS_Store", known)


if __name__ == "__main__":
    unittest.main()
