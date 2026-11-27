import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify-agent-ready.py"


def load_module():
    spec = importlib.util.spec_from_file_location("verify_agent_ready", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AgentReadyTests(unittest.TestCase):
    def setUp(self):
        module = load_module()
        self.find = module.findings
        self.glossary = module.glossary
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, relative, text=""):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def skill(self, name, linked=False):
        self.write(f".agents/skills/{name}/SKILL.md", f"---\nname: {name}\n---\n")
        if linked:
            (self.root / ".claude/skills").mkdir(parents=True, exist_ok=True)
            os.symlink(f"../../.agents/skills/{name}", self.root / ".claude/skills" / name)

    def bridged(self, agents_text=""):
        self.write("AGENTS.md", agents_text)
        self.write("CLAUDE.md", "@AGENTS.md\n")

    def test_a_ready_repository_has_no_findings(self):
        # Given a root and a nested app, each with AGENTS.md and a CLAUDE.md that imports it,
        # a referenced script that exists, and a repository Skill linked into .claude/skills
        self.bridged("Run `scripts/check.sh` before a commit.\n")
        self.write("scripts/check.sh", "true\n")
        self.write("apps/catalog/AGENTS.md", "See `README.md`.\n")
        self.write("apps/catalog/CLAUDE.md", "@AGENTS.md\n")
        self.write("apps/catalog/README.md")
        self.skill("team-review", linked=True)
        # Then nothing is reported
        self.assertEqual(self.find(self.root), [])

    def test_an_agents_file_without_a_claude_bridge_is_reported(self):
        # Given a root AGENTS.md with no CLAUDE.md beside it, while the app has one
        self.write("AGENTS.md")
        self.write("apps/catalog/AGENTS.md")
        self.write("apps/catalog/CLAUDE.md", "@AGENTS.md\n")
        # Then only the root is reported as a missing bridge
        self.assertEqual(self.find(self.root), [("bridge", "AGENTS.md", "no CLAUDE.md beside it imports @AGENTS.md")])

    def test_a_claude_file_that_does_not_import_agents_is_reported(self):
        # Given a CLAUDE.md with its own text and no import of AGENTS.md
        self.write("AGENTS.md")
        self.write("CLAUDE.md", "Use pnpm.\n")
        # Then the bridge is reported
        self.assertEqual([kind for kind, _, _ in self.find(self.root)], ["bridge"])

    def test_a_repository_skill_without_a_claude_entry_is_reported(self):
        # Given a Skill in .agents/skills and no .claude/skills entry for it
        self.bridged()
        self.skill("team-review")
        # Then the Skill is reported as invisible to Claude Code
        self.assertEqual(self.find(self.root), [("skill-link", ".agents/skills/team-review", "no .claude/skills/team-review entry")])

    def test_a_skill_named_like_a_host_built_in_is_reported(self):
        # Given a linked repository Skill whose name is a built-in command of a host
        self.bridged()
        self.skill("security-review", linked=True)
        # Then the name collision is reported
        self.assertEqual([kind for kind, _, _ in self.find(self.root)], ["name"])

    def test_a_built_in_name_whose_description_names_the_command_passes(self):
        # Given a Skill named like a built-in whose description names the built-in command,
        # because automation finds the Skill by that name and a rename would break it
        self.bridged()
        self.skill("review", linked=True)
        self.write(".agents/skills/review/SKILL.md",
                   "---\nname: review\ndescription: Review against the work item. Not the host's built-in /review.\n---\n")
        # Then nothing is reported
        self.assertEqual(self.find(self.root), [])

    def test_a_referenced_file_that_does_not_exist_is_reported(self):
        # Given AGENTS.md naming one existing and one missing file in backticks
        self.bridged("Read `docs/GLOSSARY.md` and run `python3 scripts/gone.py --fast`.\n")
        self.write("docs/GLOSSARY.md")
        # Then only the missing file is reported
        self.assertEqual(self.find(self.root), [("missing", "AGENTS.md", "scripts/gone.py")])

    def test_a_path_from_one_persons_machine_is_reported(self):
        # Given AGENTS.md pointing at a home-directory path
        self.bridged("Load `~/notes/team.md` first.\n")
        # Then the machine path is reported
        self.assertEqual(self.find(self.root), [("machine-path", "AGENTS.md", "~/notes/team.md")])

    def test_placeholders_urls_and_flags_are_not_paths(self):
        # Given backticked text that only looks like a path
        self.bridged(
            "Use `origin/<default>`, `origin/main`, `https://example.com/a.md`, `--fix`, `src/**/*.ts`,"
            " `v1.2.3`, `/fast`, `user.email`, and each Skill's `SKILL.md`.\n"
        )
        # Then nothing is reported
        self.assertEqual(self.find(self.root), [])

    def test_web_routes_and_fenced_examples_are_not_checked(self):
        # Given an API route in backticks and a fenced example naming a file that does not exist
        self.bridged("Call `/api/v1/items.json`.\n\n```\ncat `examples/gone.md`\n```\n")
        # Then nothing is reported
        self.assertEqual(self.find(self.root), [])

    def test_a_claude_file_linked_to_agents_reports_each_finding_once(self):
        # Given CLAUDE.md as a symlink to an AGENTS.md that names a missing file
        self.write("AGENTS.md", "Run `scripts/gone.sh`.\n")
        os.symlink("AGENTS.md", self.root / "CLAUDE.md")
        # Then the missing file is reported once
        self.assertEqual(self.find(self.root), [("missing", "AGENTS.md", "scripts/gone.sh")])

    def test_a_dangling_or_undecodable_instruction_file_does_not_crash(self):
        # Given a dangling CLAUDE.md symlink and an AGENTS.md that is not UTF-8
        (self.root / "AGENTS.md").write_bytes(b"caf\xe9 `scripts/gone.sh`\n")
        os.symlink("nowhere.md", self.root / "CLAUDE.md")
        # Then the bridge and the missing file are reported
        self.assertEqual([kind for kind, _, _ in self.find(self.root)], ["bridge", "missing"])

    def test_a_longer_command_in_the_description_does_not_count_as_the_neighbour(self):
        # Given a Skill named review whose description names only /reviewer
        self.bridged()
        self.skill("review", linked=True)
        self.write(".agents/skills/review/SKILL.md", "---\nname: review\ndescription: Pairs with /reviewer.\n---\n")
        # Then the collision is still reported
        self.assertEqual([kind for kind, _, _ in self.find(self.root)], ["name"])

    def test_the_glossary_is_found_under_its_name_or_the_older_one(self):
        # Given one repository with GLOSSARY.md, one with only CONTEXT.md, and one with neither
        self.write("a/GLOSSARY.md")
        self.write("b/CONTEXT.md")
        self.write("c/AGENTS.md")
        # Then the first two resolve to their file and the third to none
        self.assertEqual(self.glossary(self.root / "a"), "GLOSSARY.md")
        self.assertEqual(self.glossary(self.root / "b"), "CONTEXT.md")
        self.assertIsNone(self.glossary(self.root / "c"))

    def test_a_glossary_under_its_old_name_gets_a_rename_note_without_failing(self):
        # Given a ready repository whose glossary is still CONTEXT.md
        self.bridged()
        self.write("CONTEXT.md", "# Glossary\n")
        # When the script runs on it
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.root)], capture_output=True, text=True)
        # Then it exits 0 and notes the rename to GLOSSARY.md
        self.assertEqual(result.returncode, 0)
        self.assertIn("git mv CONTEXT.md GLOSSARY.md", result.stdout)

    def test_the_command_exits_non_zero_on_findings(self):
        # Given a repository with a missing bridge and no glossary
        self.write("AGENTS.md")
        # When the script runs on it
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.root)], capture_output=True, text=True)
        # Then it exits 1, prints the finding, and notes the missing glossary
        self.assertEqual(result.returncode, 1)
        self.assertIn("bridge", result.stdout)
        self.assertIn("GLOSSARY.md", result.stdout)

    def test_a_missing_glossary_alone_does_not_fail(self):
        # Given a ready repository without a glossary
        self.bridged()
        # When the script runs on it
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.root)], capture_output=True, text=True)
        # Then it exits 0: a glossary is written only for confirmed language
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
