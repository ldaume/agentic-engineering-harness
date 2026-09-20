import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "jev_client.py"


def load_module():
    spec = importlib.util.spec_from_file_location("jev_client", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CredentialTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.mod.KEY_FILES = {"typesafe": self.root / "no-ts", "gateway": self.root / "no-gw"}

    def tearDown(self):
        self.tmp.cleanup()

    def test_repository_dotenv_with_only_the_gateway_key_selects_the_gateway(self):
        """Given a checkout whose .env holds only VERCEL_AI_GATEWAY_API_KEY and a
        machine that also exports TYPESAFE_API_KEY, when credentials load, then the
        checkout's gateway key wins."""
        (self.root / ".env").write_text('VERCEL_AI_GATEWAY_API_KEY="vck_test"\n', encoding="utf-8")
        with mock.patch.dict(os.environ, {"TYPESAFE_API_KEY": "ts_env"}, clear=False):
            self.assertEqual(self.mod.load_credentials(self.root), ("gateway", "vck_test"))

    def test_environment_typesafe_key_wins_when_the_checkout_has_no_dotenv(self):
        with mock.patch.dict(os.environ, {"TYPESAFE_API_KEY": "ts_env", "VERCEL_AI_GATEWAY_API_KEY": "vck_env"}, clear=False):
            self.assertEqual(self.mod.load_credentials(self.root), ("typesafe", "ts_env"))

    def test_jev_backend_forces_the_gateway(self):
        with mock.patch.dict(os.environ, {"TYPESAFE_API_KEY": "ts_env", "VERCEL_AI_GATEWAY_API_KEY": "vck_env", "JEV_BACKEND": "gateway"}, clear=False):
            self.assertEqual(self.mod.load_credentials(self.root), ("gateway", "vck_env"))

    def test_user_level_key_file_is_the_last_resort(self):
        (self.root / "no-gw").write_text("vck_file\n", encoding="utf-8")
        env = {k: v for k, v in os.environ.items() if k not in ("TYPESAFE_API_KEY", "VERCEL_AI_GATEWAY_API_KEY", "JEV_BACKEND")}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(self.mod.load_credentials(self.root), ("gateway", "vck_file"))


class GatewayRequestTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()
        self.questions = {
            "task_class": {"type": "choice", "instructions": "Which?", "criteria": {"a": "A", "b": "B"}},
            "ambiguous": {"type": "noul", "instructions": "Unclear?"},
            "depth": {"type": "score", "instructions": "How deep?", "criteria": ["none", "some"]},
        }

    def test_gateway_request_translates_noul_to_boolean_and_sets_the_protocol_headers(self):
        """Given the harness questions, when the gateway request is built, then noul
        becomes boolean, choice and score pass through, and the gateway headers name
        the model and protocol."""
        request = self.mod.build_request({"task": "x"}, self.questions, "gateway", "vck")
        body = json.loads(request.data)
        self.assertEqual(request.full_url, self.mod.GATEWAY_URL)
        self.assertEqual(body["questions"]["ambiguous"]["type"], "boolean")
        self.assertEqual(body["questions"]["task_class"]["criteria"], {"a": "A", "b": "B"})
        self.assertEqual(body["questions"]["depth"]["criteria"], ["none", "some"])
        self.assertNotIn("model", body)
        self.assertEqual(request.get_header("Ai-model-id"), "typesafe-ai/jev")
        self.assertEqual(request.get_header("Ai-gateway-protocol-version"), "0.0.1")
        self.assertEqual(request.get_header("Ai-evaluation-model-specification-version"), "4")
        self.assertEqual(request.get_header("Authorization"), "Bearer vck")

    def test_typesafe_request_keeps_the_direct_shape(self):
        request = self.mod.build_request({"task": "x"}, self.questions, "typesafe", "ts")
        body = json.loads(request.data)
        self.assertEqual(request.full_url, self.mod.TYPESAFE_URL)
        self.assertEqual(body["model"], "jev-latest")
        self.assertEqual(body["questions"]["ambiguous"]["type"], "noul")
        self.assertIsNone(request.get_header("Ai-model-id"))

    def test_gateway_answers_normalize_to_the_typesafe_shape(self):
        """Given a gateway answer (2026-09-20 shape), when normalized, then boolean
        becomes noul, confidence moves onto each answer, and usage uses input_tokens."""
        payload = {
            "answers": {
                "task_class": {"type": "choice", "choice": "a", "probabilities": {"a": 0.9, "b": 0.1}},
                "ambiguous": {"type": "boolean", "probability": 0.24},
                "depth": {"type": "score", "score": 1.92, "probabilities": {"0": 0.1, "1": 0.9}},
            },
            "usage": {"inputTokens": 455, "outputTokens": 97},
            "providerMetadata": {"typesafe": {"confidence": {"task_class": 1, "depth": 0.59}}},
        }
        normalized = self.mod.normalize(payload, "gateway")
        self.assertEqual(normalized["answers"]["ambiguous"]["noul"], 0.24)
        self.assertEqual(normalized["answers"]["task_class"]["confidence"], 1)
        self.assertEqual(normalized["answers"]["depth"]["confidence"], 0.59)
        self.assertNotIn("confidence", normalized["answers"]["ambiguous"])
        self.assertEqual(normalized["usage"], {"input_tokens": 455, "output_tokens": 97})
        self.assertIs(self.mod.normalize(payload, "typesafe"), payload)

    def test_cost_uses_each_backend_list_price(self):
        usage = {"input_tokens": 1_000_000}
        self.assertAlmostEqual(self.mod.cost_usd(usage, "typesafe"), 0.042)
        self.assertAlmostEqual(self.mod.cost_usd(usage, "gateway"), 0.04)


if __name__ == "__main__":
    unittest.main()
