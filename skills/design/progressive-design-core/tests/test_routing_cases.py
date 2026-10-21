import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILY = HERE.parents[1]
SKILLS = {p.name for p in FAMILY.glob("progressive-*") if (p / "SKILL.md").exists()}


class RoutingCases(unittest.TestCase):
    def test_given_routing_cases_when_loaded_then_every_named_skill_exists(self):
        cases = json.loads((HERE / "routing-cases.json").read_text(encoding="utf-8"))["cases"]
        self.assertGreaterEqual(len(cases), 10)
        for case in cases:
            named = set(case.get("should_activate", [])) | set(case.get("should_not_activate", []))
            self.assertTrue(named, case["id"])
            self.assertLessEqual(named, SKILLS, case["id"])

    def test_given_every_design_skill_when_cases_are_read_then_each_has_a_positive_case(self):
        cases = json.loads((HERE / "routing-cases.json").read_text(encoding="utf-8"))["cases"]
        covered = {s for c in cases for s in c.get("should_activate", [])}
        self.assertEqual(SKILLS - covered, set())


if __name__ == "__main__":
    unittest.main()
