import importlib.util
import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "route-subagent.py"


def load_module():
    spec = importlib.util.spec_from_file_location("route_subagent", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def answers(task_class, ambiguous=0.1, consequential=0.1, depth=0.5, confidence=0.9, top=0.9):
    other = {c: (1 - top) / 5 for c in ["mechanical", "implementation", "research", "review", "critique", "integration"] if c != task_class}
    return {
        "answers": {
            "task_class": {"type": "choice", "choice": task_class, "confidence": confidence, "probabilities": {task_class: top, **other}},
            "ambiguous": {"type": "noul", "noul": ambiguous},
            "consequential": {"type": "noul", "noul": consequential},
            "depth": {"type": "score", "score": depth, "confidence": confidence},
        },
        "usage": {"input_tokens": 400, "output_tokens": 40},
    }


class DecideTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_mechanical_task_routes_efficient_low(self):
        # Given a clearly mechanical, unambiguous, reversible task
        # When the decision runs
        decision = self.mod.decide(answers("mechanical"))
        # Then the efficient tier at low effort is chosen with confidence
        self.assertEqual((decision["tier"], decision["effort"]), ("efficient", "low"))
        self.assertTrue(decision["confident"])

    def test_critique_routes_frontier_high(self):
        decision = self.mod.decide(answers("critique"))
        self.assertEqual((decision["tier"], decision["effort"]), ("frontier", "high"))

    def test_consequential_implementation_escalates_to_frontier(self):
        decision = self.mod.decide(answers("implementation", consequential=0.85))
        self.assertEqual(decision["tier"], "frontier")
        self.assertIn("consequential", " ".join(decision["reasons"]))

    def test_ambiguous_deep_research_escalates(self):
        decision = self.mod.decide(answers("research", ambiguous=0.8, depth=2.4))
        self.assertEqual((decision["tier"], decision["effort"]), ("frontier", "high"))

    def test_mildly_underspecified_mechanical_task_stays_efficient(self):
        decision = self.mod.decide(answers("mechanical", ambiguous=0.6))
        self.assertEqual(decision["tier"], "efficient")
        self.assertEqual(self.mod.decide(answers("mechanical", ambiguous=0.9))["tier"], "balanced")

    def test_review_routes_balanced_high(self):
        decision = self.mod.decide(answers("review"))
        self.assertEqual((decision["tier"], decision["effort"]), ("balanced", "high"))

    def test_low_confidence_falls_back_to_balanced_medium(self):
        decision = self.mod.decide(answers("mechanical", confidence=0.4, top=0.45))
        self.assertEqual((decision["tier"], decision["effort"]), ("balanced", "medium"))
        self.assertFalse(decision["confident"])


class ResolveTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()
        self.models = self.mod.DEFAULT_HOST_MODELS

    def test_host_adapters_map_tiers_to_default_models(self):
        cases = {
            ("claude", "efficient", "low"): "haiku",
            ("claude", "balanced", "medium"): "sonnet",
            ("claude", "frontier", "high"): "opus",
            ("codex", "efficient", "low"): "gpt-5.6-luna",
            ("codex", "balanced", "high"): "gpt-5.6-terra",
            ("codex", "frontier", "high"): "gpt-5.6-sol",
            ("cursor", "efficient", "low"): "composer-2.5",
            ("cursor", "balanced", "medium"): "cursor-grok-4.6-medium",
            ("cursor", "balanced", "high"): "cursor-grok-4.6-high",
            ("cursor", "frontier", "high"): "cursor-grok-4.6-high",
            ("cursor", "balanced", "low"): "cursor-grok-4.6-medium",
            ("gemini", "efficient", "low"): "gemini-flash-lite",
            ("gemini", "balanced", "medium"): "gemini-flash",
            ("gemini", "frontier", "high"): "gemini-pro",
        }
        for (host, tier, effort), model in cases.items():
            with self.subTest(host=host, tier=tier):
                self.assertEqual(self.mod.resolve(host, tier, effort, self.models)["model"], model)

    def test_never_resolves_a_fast_route(self):
        for host in self.models:
            for tier in ("efficient", "balanced", "frontier"):
                for effort in ("low", "medium", "high"):
                    self.assertNotIn("fast", self.mod.resolve(host, tier, effort, self.models)["model"].lower())

    def test_models_override_file_replaces_only_named_host(self):
        # Given a consumer override file naming only claude
        with tempfile.TemporaryDirectory() as tmp:
            override = Path(tmp) / "models.json"
            override.write_text(json.dumps({"claude": {"balanced": "custom-model"}}), encoding="utf-8")
            # When the host model table loads with that override
            models = self.mod.load_host_models(override)
            # Then claude balanced changes but other hosts and tiers keep the built-in default
            self.assertEqual(models["claude"]["balanced"], "custom-model")
            self.assertEqual(models["claude"]["efficient"], "haiku")
            self.assertEqual(models["codex"]["balanced"], "gpt-5.6-terra")

    def test_missing_override_file_uses_built_in_defaults(self):
        # No config file is required for the router to work
        models = self.mod.load_host_models(None)
        self.assertEqual(models, self.mod.DEFAULT_HOST_MODELS)

    def test_env_var_override_is_honored(self):
        with tempfile.TemporaryDirectory() as tmp:
            override = Path(tmp) / "models.json"
            override.write_text(json.dumps({"gemini": {"frontier": "gemini-ultra"}}), encoding="utf-8")
            old = os.environ.get("ROUTE_SUBAGENT_MODELS")
            os.environ["ROUTE_SUBAGENT_MODELS"] = str(override)
            try:
                models = self.mod.load_host_models(None)
                self.assertEqual(models["gemini"]["frontier"], "gemini-ultra")
            finally:
                if old is None:
                    del os.environ["ROUTE_SUBAGENT_MODELS"]
                else:
                    os.environ["ROUTE_SUBAGENT_MODELS"] = old


class OutageTests(unittest.TestCase):
    def test_unreachable_api_yields_default_route_without_failing(self):
        mod = load_module()
        mod.load_api_key = lambda: "key"
        mod.evaluate = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("TypeSafe API unreachable: timed out"))
        result = mod.route("Anything", "codex")
        self.assertEqual((result["model"], result["effort"], result["confident"]), ("gpt-5.6-terra", "medium", False))
        self.assertIn("router unavailable", result["reasons"][0])

    def test_malformed_answer_yields_default_route(self):
        mod = load_module()
        mod.load_api_key = lambda: "key"
        mod.evaluate = lambda *a, **k: ({"answers": {}}, 5)
        self.assertFalse(mod.route("Anything", "claude")["confident"])

    def test_missing_api_key_still_yields_default_route_without_raising(self):
        # Given no TYPESAFE_API_KEY is configured anywhere (a bare install, no key)
        mod = load_module()

        def raise_missing_key():
            raise RuntimeError("TYPESAFE_API_KEY is not set (environment, ~/.config/typesafe/api-key, or .env)")
        mod.load_api_key = raise_missing_key
        # When the parent routes a task with no key present
        result = mod.route("Do something", "claude")
        # Then it still returns a usable default route instead of crashing the caller
        self.assertEqual((result["model"], result["effort"]), ("sonnet", "medium"))
        self.assertFalse(result["confident"])
        self.assertIn("router unavailable", result["reasons"][0])

    def test_no_credentials_anywhere_still_yields_default_route(self):
        # Given jev_client finds no key at all (it exits rather than raising)
        mod = load_module()
        mod.jev = types.SimpleNamespace(load_credentials=lambda root: sys.exit("no Jev credentials"))
        # When the parent routes a task
        result = mod.route("Do something", "claude")
        # Then the Balanced default still comes back instead of a SystemExit escaping
        self.assertEqual((result["model"], result["effort"]), ("sonnet", "medium"))
        self.assertIn("router unavailable", result["reasons"][0])


class RequestTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_request_targets_typesafe_systemone_endpoint(self):
        request = self.mod.build_request("Rename a variable in one file", {"repo": "x"}, "key-1")
        self.assertEqual(request.full_url, "https://api.typesafe.ai/v1/systemone")
        self.assertEqual(request.get_header("Authorization"), "Bearer key-1")
        body = json.loads(request.data)
        self.assertEqual(body["model"], "jev-latest")
        self.assertEqual(set(body["questions"]), {"task_class", "ambiguous", "consequential", "depth"})
        self.assertEqual({q["type"] for q in body["questions"].values()}, {"choice", "noul", "score"})
        self.assertIn("Rename a variable", json.dumps(body["state"]))

    def test_cost_uses_typesafe_input_price(self):
        self.assertAlmostEqual(self.mod.cost_usd({"input_tokens": 1_000_000, "output_tokens": 5}), 0.042)


if __name__ == "__main__":
    unittest.main()


class BriefTests(unittest.TestCase):
    def test_every_route_carries_the_consider_jev_brief(self):
        """Given any routed or fail-open decision, when the parent reads it,
        then it carries the standing brief for the child."""
        routed_mod = load_module()
        routed_mod.load_api_key = lambda: "key"
        routed_mod.evaluate = lambda *a, **k: (answers("mechanical"), 5)
        routed = routed_mod.route("rename a helper", "claude")
        fallen_mod = load_module()
        fallen_mod.load_api_key = lambda: "key"
        fallen_mod.evaluate = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("TypeSafe API unreachable"))
        fallen = fallen_mod.route("rename a helper", "claude")
        for result in (routed, fallen):
            self.assertTrue(result["brief"].startswith("Consider Jev: "))
            self.assertIn("iteration-gate.py", result["brief"])
