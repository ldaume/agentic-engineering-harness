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


if __name__ == "__main__":
    unittest.main()
