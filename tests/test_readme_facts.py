"""The README states the catalog size and Skill versions; these checks keep them true."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def stated_count(readme: str) -> int:
    return int(re.search(r"\| (\d+) Skills for ", readme).group(1))


def stated_versions(readme: str) -> dict[str, str]:
    return dict(re.findall(r"\[`([a-z-]+)`\]\([^)]*\) (\d+\.\d+\.\d+)", readme))


def latest_tag(skill: str) -> str | None:
    tags = subprocess.run(["git", "tag", "--list", f"{skill}-v*", "--sort=-v:refname"],
                          cwd=ROOT, capture_output=True, text=True).stdout.split()
    return tags[0].removeprefix(f"{skill}-v") if tags else None


class ReadmeFacts(unittest.TestCase):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_given_the_catalog_then_the_readme_states_its_size(self):
        # Given every Skill directory with a SKILL.md
        actual = len(list((ROOT / "skills").glob("*/*/SKILL.md")))
        # Then the README names that many Skills
        self.assertEqual(stated_count(self.readme), actual)

    def test_given_release_tags_then_each_stated_version_is_the_latest(self):
        versions = stated_versions(self.readme)
        self.assertTrue(versions)
        for skill, stated in versions.items():
            tag = latest_tag(skill)
            if tag is None:
                self.skipTest("no release tags in this checkout")
            # Then the README version is the newest release of that Skill
            self.assertEqual(stated, tag, skill)

    def test_given_released_versions_then_the_changelog_does_not_call_them_unreleased(self):
        # Given the changelog entries listed under "Unreleased"
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        section = re.search(r"## Unreleased\n(.*?)(?=\n## |\Z)", changelog, re.S)
        entries = re.findall(r"- `([a-z-]+)` (\d+\.\d+\.\d+):", section.group(1)) if section else []
        for skill, version in entries:
            # Then none of them already has its release tag
            tags = subprocess.run(["git", "tag", "--list", f"{skill}-v{version}"],
                                  cwd=ROOT, capture_output=True, text=True).stdout.split()
            self.assertFalse(tags, f"{skill} {version} is tagged but listed as unreleased")

    def test_given_a_stale_readme_then_the_checks_see_it(self):
        # Given a README written for an older catalog
        stale = "| 45 Skills for x |\n[`agent-sync`](./a.md) 1.0.0"
        # Then the parsed facts differ from the current ones
        self.assertEqual(stated_count(stale), 45)
        self.assertEqual(stated_versions(stale), {"agent-sync": "1.0.0"})


if __name__ == "__main__":
    unittest.main()
