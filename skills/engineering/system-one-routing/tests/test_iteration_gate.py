import importlib.util
import json
import sys
import types
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "iteration-gate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("iteration_gate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def noul(value, confidence=0.9):
    return {"type": "noul", "noul": value, "confidence": confidence}


def score(value, confidence=0.9):
    return {"type": "score", "score": value, "confidence": confidence}


def choice(value, confidence=0.9):
    return {"type": "choice", "choice": value, "confidence": confidence}


def hypothesis_payload(falsifiable=0.8, measurable=0.8, smallest_increment=0.8, reversible=0.8,
                        teach_decisive=2.5, teach_confidence=0.9):
    return {
        "answers": {
            "falsifiable": noul(falsifiable),
            "measurable": noul(measurable),
            "smallest_increment": noul(smallest_increment),
            "reversible": noul(reversible),
            "teach_decisive": score(teach_decisive, teach_confidence),
        },
        "usage": {"input_tokens": 300, "output_tokens": 30},
    }


def continue_payload(moved=0.8, moved_confidence=0.9, distance=2.0, next_step="continue", next_confidence=0.9):
    return {
        "answers": {
            "moved": noul(moved, moved_confidence),
            "distance": score(distance),
            "next_step": choice(next_step, next_confidence),
        },
        "usage": {"input_tokens": 350, "output_tokens": 20},
    }


class HypothesisTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_all_nouls_pass_and_confident_is_ready(self):
        # Given all four nouls are at or above 0.6 and confidence is adequate
        decision = self.mod.decide_hypothesis(hypothesis_payload())
        # When the hypothesis is decided
        # Then the verdict is ready
        self.assertEqual(decision["verdict"], "ready")
        self.assertEqual(decision["reasons"], [])

    def test_one_failing_noul_yields_grill_and_names_it(self):
        # Given the increment is not the smallest observable step
        decision = self.mod.decide_hypothesis(hypothesis_payload(smallest_increment=0.3))
        # Then the verdict is grill and the failing criterion is named
        self.assertEqual(decision["verdict"], "grill")
        self.assertIn("smallest_increment", " ".join(decision["reasons"]))

    def test_low_confidence_yields_grill_even_with_passing_nouls(self):
        # Given every noul passes but Jev is not confident about the score
        decision = self.mod.decide_hypothesis(hypothesis_payload(teach_confidence=0.2))
        # Then the verdict is grill
        self.assertEqual(decision["verdict"], "grill")
        self.assertFalse(decision["confident"])

    def test_exit_codes_ready_and_grill(self):
        self.assertEqual(self.mod.EXIT_READY, 0)
        self.assertEqual(self.mod.EXIT_GRILL, 3)


class ContinueTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_movement_toward_goal_continues(self):
        # Given the latest iteration moved a measured value and Jev recommends continue
        log = [
            {"summary": "a", "measurements": {"score": 1}, "checks": {}},
            {"summary": "b", "measurements": {"score": 2}, "checks": {}},
        ]
        decision = self.mod.decide_continue(continue_payload(), log)
        # Then the verdict is continue
        self.assertEqual(decision["verdict"], "continue")

    def test_switch_choice_at_adequate_confidence_switches(self):
        # Given Jev recommends switching hypotheses at confidence above 0.6
        log = [{"summary": "a", "measurements": {"score": 1}, "checks": {}}]
        decision = self.mod.decide_continue(continue_payload(next_step="switch", next_confidence=0.8), log)
        # Then the verdict is switch
        self.assertEqual(decision["verdict"], "switch")

    def test_switch_choice_below_confidence_does_not_switch(self):
        # Given Jev leans switch but is not confident
        log = [{"summary": "a", "measurements": {"score": 1}, "checks": {}}]
        decision = self.mod.decide_continue(continue_payload(next_step="switch", next_confidence=0.4), log)
        # Then the verdict falls back to continue
        self.assertEqual(decision["verdict"], "continue")

    def test_distance_at_lowest_level_stops(self):
        # Given the outcome is already at or past shippable (lowest distance band)
        log = [{"summary": "a", "measurements": {"score": 1}, "checks": {}}]
        decision = self.mod.decide_continue(continue_payload(distance=0.5), log)
        # Then the verdict is stop
        self.assertEqual(decision["verdict"], "stop")

    def test_two_consecutive_stagnant_iterations_stop_at_high_confidence(self):
        # Given the last two iterations show no change in any measured value
        # and Jev is highly confident the latest did not move
        log = [
            {"summary": "a", "measurements": {"score": 1}, "checks": {}},
            {"summary": "b", "measurements": {"score": 1}, "checks": {}},
            {"summary": "c", "measurements": {"score": 1}, "checks": {}},
        ]
        decision = self.mod.decide_continue(continue_payload(moved=0.1, moved_confidence=0.9, distance=2.0), log)
        # Then the verdict is stop
        self.assertEqual(decision["verdict"], "stop")

    def test_two_consecutive_stagnant_but_low_confidence_does_not_stop(self):
        # Given the same flat history but Jev is not confident about it
        log = [
            {"summary": "a", "measurements": {"score": 1}, "checks": {}},
            {"summary": "b", "measurements": {"score": 1}, "checks": {}},
            {"summary": "c", "measurements": {"score": 1}, "checks": {}},
        ]
        decision = self.mod.decide_continue(continue_payload(moved=0.1, moved_confidence=0.3, distance=2.0), log)
        # Then the verdict does not stop on stagnation alone
        self.assertEqual(decision["verdict"], "continue")

    def test_no_measurements_are_counted_and_warned(self):
        # Given two of three iterations carry no measurements at all
        log = [
            {"summary": "a", "measurements": {}, "checks": {}},
            {"summary": "b", "measurements": None, "checks": {}},
            {"summary": "c", "measurements": {"score": 1}, "checks": {}},
        ]
        decision = self.mod.decide_continue(continue_payload(), log)
        # Then the count is reported and the caller is warned Jev judges prose, not progress
        self.assertEqual(decision["no_measurement_count"], 2)
        self.assertIn("judges prose, not progress", " ".join(decision["reasons"]))

    def test_exit_codes_continue_switch_stop(self):
        self.assertEqual(self.mod.EXIT_CONTINUE, 0)
        self.assertEqual(self.mod.EXIT_SWITCH, 4)
        self.assertEqual(self.mod.EXIT_STOP, 5)


class RankTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_equal_weights_ranks_higher_value_lower_effort_first(self):
        # Given one candidate is high value and low effort, the other low value and high effort
        per_candidate = [
            {"id": "a", "text": "A", "answers": {
                "value": score(3), "urgency": score(1), "risk": score(0), "effort": score(0)}},
            {"id": "b", "text": "B", "answers": {
                "value": score(0), "urgency": score(1), "risk": score(3), "effort": score(3)}},
        ]
        # When ranked with equal weights
        ranked = self.mod.rank_candidates(per_candidate, (1, 1, 1, 1))
        # Then the stronger candidate ranks first
        self.assertEqual(ranked[0]["id"], "a")
        self.assertGreater(ranked[0]["combined"], ranked[1]["combined"])

    def test_weights_override_changes_ranking(self):
        # Given a candidate that is low effort but also low value, and one balanced
        per_candidate = [
            {"id": "low-effort", "text": "X", "answers": {
                "value": score(1), "urgency": score(1), "risk": score(1), "effort": score(0)}},
            {"id": "balanced", "text": "Y", "answers": {
                "value": score(2), "urgency": score(1), "risk": score(1), "effort": score(2)}},
        ]
        # When effort is weighted heavily
        ranked = self.mod.rank_candidates(per_candidate, (1, 1, 1, 5))
        # Then the low-effort candidate outranks the higher-value one
        self.assertEqual(ranked[0]["id"], "low-effort")

    def test_exit_code_unavailable(self):
        self.assertEqual(self.mod.EXIT_RANK_UNAVAILABLE, 2)


class FailOpenTests(unittest.TestCase):
    def test_hypothesis_unreachable_exits_zero(self):
        # Given the TypeSafe API cannot be reached
        mod = load_module()
        mod.load_api_key = lambda: "key"
        mod.evaluate = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("TypeSafe API unreachable: timed out"))
        args = argparse_namespace(goal="g", hypothesis="h", measure="m", increment="i", min_confidence=0.6, json=False, no_record=True)
        # When the hypothesis gate runs
        exit_code = mod.run_hypothesis(args)
        # Then it prints gate unavailable and exits 0 so the agent decides itself
        self.assertEqual(exit_code, 0)

    def test_no_credentials_anywhere_exits_zero(self):
        # Given jev_client finds no key at all (it exits rather than raising)
        mod = load_module()
        mod.jev = types.SimpleNamespace(load_credentials=lambda root: sys.exit("no Jev credentials"))
        args = argparse_namespace(goal="g", hypothesis="h", measure="m", increment="i", min_confidence=0.6, json=False, no_record=True)
        # When the hypothesis gate runs, then it still exits 0 and the agent decides
        self.assertEqual(mod.run_hypothesis(args), 0)

    def test_continue_unreachable_exits_zero(self, tmp_log=None):
        import tempfile
        mod = load_module()
        mod.load_api_key = lambda: "key"
        mod.evaluate = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("TypeSafe API unreachable: timed out"))
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump([{"summary": "a", "measurements": {"x": 1}, "checks": {}}], fh)
            path = Path(fh.name)
        try:
            args = argparse_namespace(goal="g", log=path, json=False, no_record=True)
            exit_code = mod.run_continue(args)
            self.assertEqual(exit_code, 0)
        finally:
            path.unlink()

    def test_rank_unreachable_exits_two(self):
        import tempfile
        mod = load_module()
        mod.load_api_key = lambda: "key"
        mod.evaluate = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("TypeSafe API unreachable: timed out"))
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump([{"id": "a", "text": "A"}], fh)
            path = Path(fh.name)
        try:
            args = argparse_namespace(candidates=path, goal="g", weights="1,1,1,1", json=False, no_record=True)
            exit_code = mod.run_rank(args)
            self.assertEqual(exit_code, 2)
        finally:
            path.unlink()


class NoMeasurementsTests(unittest.TestCase):
    def test_latest_iteration_without_measurements_or_checks_refuses_without_a_jev_call(self):
        # Given the latest iteration carries neither a measurement nor a check (2026-09-20 pilot: 71 percent
        # of judged state was infra failure text with zero signal)
        mod = load_module()
        called = []
        mod.evaluate = lambda *a, **k: called.append(1) or (_ for _ in ()).throw(AssertionError("Jev should not be called"))
        log = [{"summary": "a", "measurements": {}, "checks": {}}]
        args = argparse_namespace(goal="g", log=Path("unused"), json=False, no_record=True)
        # When continue runs, using the log directly (avoid file IO)
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(log, fh)
            path = Path(fh.name)
        try:
            args = argparse_namespace(goal="g", log=path, json=False, no_record=True)
            exit_code = mod.run_continue(args)
        finally:
            path.unlink()
        # Then it exits 6 with a no-measurements verdict and never calls Jev
        self.assertEqual(exit_code, mod.EXIT_NO_MEASUREMENTS)
        self.assertEqual(called, [])

    def test_a_check_alone_is_enough_signal_to_proceed(self):
        # Given the latest iteration has a check but no numeric measurement
        mod = load_module()
        mod.load_api_key = lambda: "key"
        mod.evaluate = lambda *a, **k: (continue_payload(), 5)
        log = [{"summary": "a", "measurements": {}, "checks": {"tests": "pass"}}]
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(log, fh)
            path = Path(fh.name)
        try:
            args = argparse_namespace(goal="g", log=path, json=False, no_record=True)
            exit_code = mod.run_continue(args)
        finally:
            path.unlink()
        # Then Jev is asked and a normal verdict comes back
        self.assertNotEqual(exit_code, mod.EXIT_NO_MEASUREMENTS)


class RecordingTests(unittest.TestCase):
    def test_decisions_are_appended_as_one_json_line_with_an_empty_outcome(self):
        # Given a hypothesis decision is made
        mod = load_module()
        mod.load_api_key = lambda: "key"
        mod.evaluate = lambda *a, **k: (hypothesis_payload(), 5)
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            mod.LOG_PATH = Path(tmp) / "harness" / "jev-iteration-log.jsonl"
            args = argparse_namespace(goal="g", hypothesis="h", measure="m", increment="i", min_confidence=0.6, json=False, no_record=False)
            # When the hypothesis gate runs
            mod.run_hypothesis(args)
            # Then one JSON line is appended with timestamp, command, verdict, confidences, and an empty outcome
            lines = mod.LOG_PATH.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            entry = json.loads(lines[0])
            self.assertEqual(entry["command"], "hypothesis")
            self.assertEqual(entry["verdict"], "ready")
            self.assertIsNone(entry["outcome"])
            self.assertIn("timestamp", entry)
            self.assertIn("teach_decisive", entry["confidences"])

    def test_no_record_flag_skips_the_log(self):
        # Given --no-record is passed
        mod = load_module()
        mod.load_api_key = lambda: "key"
        mod.evaluate = lambda *a, **k: (hypothesis_payload(), 5)
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            mod.LOG_PATH = Path(tmp) / "harness" / "jev-iteration-log.jsonl"
            args = argparse_namespace(goal="g", hypothesis="h", measure="m", increment="i", min_confidence=0.6, json=False, no_record=True)
            # When the hypothesis gate runs
            mod.run_hypothesis(args)
            # Then no log file is created
            self.assertFalse(mod.LOG_PATH.exists())


def argparse_namespace(**kwargs):
    import argparse
    return argparse.Namespace(**kwargs)


class RequestShapeTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_hypothesis_request_has_four_nouls_and_one_score(self):
        request = self.mod.build_request(
            {"goal": "g", "hypothesis": "h", "measure": "m", "increment": "i"},
            self.mod.HYPOTHESIS_QUESTIONS, "key-1")
        body = json.loads(request.data)
        self.assertEqual(request.full_url, "https://api.typesafe.ai/v1/systemone")
        self.assertEqual(body["model"], "jev-latest")
        self.assertEqual(set(body["questions"]), {"falsifiable", "measurable", "smallest_increment", "reversible", "teach_decisive"})
        types = {name: q["type"] for name, q in body["questions"].items()}
        self.assertEqual(sum(1 for t in types.values() if t == "noul"), 4)
        self.assertEqual(types["teach_decisive"], "score")

    def test_continue_request_has_noul_score_and_choice(self):
        request = self.mod.build_request({"goal": "g", "log": []}, self.mod.CONTINUE_QUESTIONS, "key-1")
        body = json.loads(request.data)
        types = {name: q["type"] for name, q in body["questions"].items()}
        self.assertEqual(types, {"moved": "noul", "distance": "score", "next_step": "choice"})

    def test_rank_request_has_four_score_questions(self):
        request = self.mod.build_request({"goal": "g", "candidate": "text"}, self.mod.RANK_QUESTIONS, "key-1")
        body = json.loads(request.data)
        self.assertEqual(set(body["questions"]), {"value", "urgency", "risk", "effort"})
        self.assertTrue(all(q["type"] == "score" for q in body["questions"].values()))


if __name__ == "__main__":
    unittest.main()
