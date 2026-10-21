import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import run_evals  # noqa: E402

SIBLINGS = {p.name for p in run_evals.SKILLS.glob("progressive-*") if p.is_dir()}


class EvalsTest(unittest.TestCase):
    def test_given_references_when_golden_outputs_gated_then_all_pass(self):
        self.assertGreaterEqual(len(run_evals.golden_outputs()), 20)
        self.assertEqual(run_evals.golden(), 0)

    def test_given_routing_cases_when_loaded_then_they_name_only_existing_skills(self):
        cases = json.loads((HERE / "routing-cases.json").read_text())["cases"]
        self.assertGreaterEqual(len(cases), 10)
        for case in cases:
            named = set(case.get("should_activate", [])) | set(case.get("should_not_activate", []))
            self.assertTrue(named, case["id"])
            self.assertLessEqual(named, SIBLINGS, case["id"])

    def test_given_claude_events_when_parsed_then_only_skill_tool_calls_count(self):
        out = "\n".join([
            '{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Skill","input":{"skill":"progressive-writing:progressive-editorial"}}]}}',
            '{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Bash","input":{"command":"ls .claude/skills/progressive-design-core/SKILL.md"}}]}}',
            '{"type":"user","message":{"content":[{"type":"tool_result","content":".claude/skills/progressive-ux-research/SKILL.md"}]}}',
            '{"type":"system","subtype":"status","message":"compacting"}',
            '{"type":"assistant","message":{"content":"plain text content"}}',
        ])
        self.assertEqual(run_evals.loaded_skills("claude", out), {"progressive-editorial"})

    def test_given_codex_events_when_parsed_then_only_reading_a_skill_file_counts(self):
        out = "\n".join([
            '{"type":"item.started","item":{"type":"command_execution","command":"/bin/zsh -lc \'cat .agents/skills/progressive-ux-research/SKILL.md\'"}}',
            '{"type":"item.started","item":{"type":"command_execution","command":"/bin/zsh -lc \'ls .agents/skills\'","aggregated_output":"progressive-design-core/SKILL.md"}}',
        ])
        self.assertEqual(run_evals.loaded_skills("codex", out), {"progressive-ux-research"})


if __name__ == "__main__":
    unittest.main()
