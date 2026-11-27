"""Tests for the gate that refuses a changed Skill without a new version.

Two pull requests that raise the same Skill to the same version change the
`skills-lock.json` line identically, so Git merges them without a conflict and
one change lands under a version whose immutable tag does not contain it. The
gate compares a branch with the current base: a changed Skill needs a version
above the base's and one no tag has taken yet.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check-version-bumps.py"

_spec = importlib.util.spec_from_file_location("check_version_bumps", SCRIPT)
assert _spec and _spec.loader
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def _write(repo: Path, versions: dict[str, str], texts: dict[str, str]) -> None:
    lock = {
        "version": 1,
        "skills": {
            name: {
                "source": "local",
                "sourceType": "path",
                "skillPath": f"skills/demo/{name}/SKILL.md",
                "version": version,
            }
            for name, version in versions.items()
        },
    }
    (repo / "skills-lock.json").write_text(json.dumps(lock, indent=2) + "\n")
    for name, text in texts.items():
        path = repo / "skills" / "demo" / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def _commit(repo: Path, message: str) -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)


class ChangedSkillNeedsANewVersion(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.repo = Path(self._dir.name)
        _git(self.repo, "init", "-q", "-b", "main")
        _git(self.repo, "config", "user.email", "test@example.invalid")
        _git(self.repo, "config", "user.name", "Test")
        _write(self.repo, {"alpha": "1.0.0", "beta": "2.0.0"}, {"alpha": "a\n", "beta": "b\n"})
        _commit(self.repo, "base")
        _git(self.repo, "branch", "base")

    def tearDown(self) -> None:
        self._dir.cleanup()

    def test_a_changed_skill_at_the_base_version_is_refused(self) -> None:
        # Given a branch that changes alpha's text but keeps its version
        _write(self.repo, {"alpha": "1.0.0", "beta": "2.0.0"}, {"alpha": "a2\n"})
        _commit(self.repo, "change alpha")

        # When the gate compares it with the base
        found = gate.problems(self.repo, "base")

        # Then alpha is named, and beta, untouched, is not
        self.assertEqual(len(found), 1)
        self.assertIn("alpha", found[0])

    def test_a_changed_skill_with_a_higher_version_passes(self) -> None:
        # Given a branch that changes alpha and raises its version
        _write(self.repo, {"alpha": "1.1.0", "beta": "2.0.0"}, {"alpha": "a2\n"})
        _commit(self.repo, "change alpha")

        # When the gate compares it with the base, then nothing is refused
        self.assertEqual(gate.problems(self.repo, "base"), [])

    def test_a_version_whose_tag_exists_is_refused(self) -> None:
        # Given a tag that already took alpha 1.1.0, and a branch raising alpha to it
        _git(self.repo, "tag", "alpha-v1.1.0", "base")
        _write(self.repo, {"alpha": "1.1.0", "beta": "2.0.0"}, {"alpha": "a2\n"})
        _commit(self.repo, "change alpha")

        # When the gate compares it with the base
        found = gate.problems(self.repo, "base")

        # Then it names the taken tag
        self.assertEqual(len(found), 1)
        self.assertIn("alpha-v1.1.0", found[0])

    def test_the_same_bump_merged_first_on_the_base_is_refused(self) -> None:
        # Given another change that raised alpha to 1.1.0 on the base first
        _git(self.repo, "checkout", "-q", "-b", "mine")
        _write(self.repo, {"alpha": "1.1.0", "beta": "2.0.0"}, {"alpha": "mine\n"})
        _commit(self.repo, "my change")
        _git(self.repo, "checkout", "-q", "base")
        _write(self.repo, {"alpha": "1.1.0", "beta": "2.0.0"}, {"alpha": "theirs\nshared\n"})
        _commit(self.repo, "their change")

        # When my branch is brought up to date with the base, as before a merge
        _git(self.repo, "checkout", "-q", "mine")
        _git(self.repo, "merge", "-q", "-X", "ours", "base", "-m", "update")

        # Then the gate refuses: my change sits at a version the base already has
        found = gate.problems(self.repo, "base")
        self.assertEqual(len(found), 1)
        self.assertIn("alpha", found[0])


if __name__ == "__main__":
    unittest.main()
