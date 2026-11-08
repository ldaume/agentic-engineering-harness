"""Given/When/Then checks for the multi-repository workspace templates.

A consumer who scaffolds a workspace copies these files into a workspace root,
a coordinator repository, and every member's `AGENTS.md`. Each test names the
piece a session would miss if the template lost it.
"""

import re
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
WORKSPACE = SKILL_DIR / "templates" / "workspace"

ROOT_AGENTS = WORKSPACE / "AGENTS.md"
CONTEXT_MAP = WORKSPACE / "coordinator" / "CONTEXT-MAP.md"
SYNC = WORKSPACE / "coordinator" / "SYNC.md"
STATUS = WORKSPACE / "coordinator" / "STATUS.md"
MEMBER_SNIPPET = WORKSPACE / "coordinator" / "MEMBER-SNIPPET.md"

ALL = (ROOT_AGENTS, CONTEXT_MAP, SYNC, STATUS, MEMBER_SNIPPET)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def headings(text: str) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r"^#{2,3} (.+)$", text, re.M)}


class WorkspaceTemplates(unittest.TestCase):
    def test_given_a_workspace_scaffold_when_templates_are_listed_then_every_file_exists(self):
        # Given a consumer scaffolding a workspace with several repositories
        # When the agent looks for the workspace templates
        missing = [str(p.relative_to(SKILL_DIR)) for p in ALL if not p.is_file()]
        # Then the root, coordinator, and member templates are all there
        self.assertEqual(missing, [])

    def test_given_the_skill_when_the_templates_table_is_read_then_it_links_each_workspace_template(self):
        # Given the Skill's Templates table
        skill = read(SKILL_DIR / "SKILL.md")
        # When each workspace template is looked up by its relative link
        unlinked = [
            str(p.relative_to(SKILL_DIR))
            for p in ALL
            if f"(./{p.relative_to(SKILL_DIR).as_posix()})" not in skill
        ]
        # Then none is left for the agent to discover by accident
        self.assertEqual(unlinked, [])

    def test_given_a_member_snippet_when_a_session_starts_in_a_member_then_it_reaches_every_coordinator_file(self):
        # Given the snippet pasted into a member AGENTS.md
        text = read(MEMBER_SNIPPET)
        # When a session starts in that member
        # Then the snippet routes it to the coordinator contract, sync rules, map, and status
        for name in ("HARNESS.md", "SYNC.md", "CONTEXT-MAP.md", "STATUS.md"):
            self.assertIn(name, text, name)
        self.assertIn("<coordinator>", text)

    def test_given_the_context_map_when_a_member_is_listed_then_it_has_a_full_remote_and_an_owner(self):
        # Given the coordinator's map of member repositories
        text = read(CONTEXT_MAP)
        # When the members table header is read
        header = next(line for line in text.splitlines() if line.startswith("| Path"))
        # Then each row records where it lives, how to reach it, who owns it, and its state
        for column in ("Path", "Remote", "Role", "Owner", "State", "Fast Check"):
            self.assertIn(column, header, column)
        self.assertIn("https://", text)

    def test_given_status_when_two_sessions_share_a_workspace_then_leases_are_visible(self):
        # Given the coordinator's volatile state
        text = read(STATUS)
        # When two sessions work in the same workspace
        # Then a lease table names checkout, session, and state
        self.assertIn("Worktree leases", headings(text))
        lease_header = next(line for line in text.splitlines() if line.startswith("| Path"))
        for column in ("Branch", "Repository", "Session", "State"):
            self.assertIn(column, lease_header, column)

    def test_given_sync_when_a_change_is_made_then_admission_fan_out_and_write_back_are_defined(self):
        # Given the coordinator's sync rules
        found = headings(read(SYNC))
        # When a session admits a member, changes a shared rule, or learns a lesson
        # Then each path has an owning section
        for section in ("Working root", "Admit a member", "Sibling awareness", "Fan-out", "Write-back"):
            self.assertIn(section, found, section)

    def test_given_the_workspace_root_when_any_session_opens_there_then_it_names_the_coordinator(self):
        # Given the root instructions every session in the workspace reads
        text = read(ROOT_AGENTS)
        # Then they point at the coordinator and require reading it first
        self.assertIn("<coordinator>", text)
        self.assertIn("SYNC.md", text)
        self.assertIn("CONTEXT-MAP.md", text)


if __name__ == "__main__":
    unittest.main()
