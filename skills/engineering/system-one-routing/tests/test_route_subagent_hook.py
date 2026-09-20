import importlib.util
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "route-subagent-hook.py"


def load_module():
    spec = importlib.util.spec_from_file_location("route_subagent_hook", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HookRoutingTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_missing_router_falls_open_to_balanced_default(self):
        # Given the router script cannot be found
        self.mod.ROUTER = Path("/nonexistent/route-subagent.py")
        # When the hook routes a prompt
        decision = self.mod.route("Do something")
        # Then it falls open to the Balanced default and says why
        self.assertEqual((decision["model"], decision["effort"]), ("sonnet", "medium"))
        self.assertIn("router unavailable", decision["reasons"][0])

    def test_router_timeout_falls_open(self):
        # Given the router call times out
        self.mod.ROUTER = SCRIPT  # any existing file passes the is_file check
        self.mod.subprocess.run = lambda *a, **k: (_ for _ in ()).throw(subprocess.TimeoutExpired(cmd="x", timeout=20))
        # When the hook routes a prompt
        decision = self.mod.route("Do something")
        # Then it falls open to the Balanced default
        self.assertEqual((decision["model"], decision["effort"]), ("sonnet", "medium"))

    def test_router_returning_a_fast_route_is_rejected(self):
        # Given the router (misconfigured) returns a fast route
        self.mod.ROUTER = SCRIPT

        class Done:
            returncode = 0
            stdout = json.dumps({"model": "sonnet-fast", "effort": "low"})
            stderr = ""
        self.mod.subprocess.run = lambda *a, **k: Done()
        # When the hook routes a prompt
        decision = self.mod.route("Do something")
        # Then it never returns the fast route, falling open instead
        self.assertNotIn("fast", decision["model"].lower())


class HookEventTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()
        self.mod.route = lambda prompt: {"model": "sonnet", "effort": "medium", "tier": "balanced",
                                          "task_class": "implementation", "confident": True, "reasons": ["stub"]}
        self.mod.LOG = Path("/tmp/route-subagent-hook-test.log")

    def _run(self, event):
        import io
        import sys
        old_stdin, old_stdout = sys.stdin, sys.stdout
        sys.stdin = io.StringIO(json.dumps(event))
        sys.stdout = io.StringIO()
        try:
            self.mod.main()
            return sys.stdout.getvalue()
        finally:
            sys.stdin, sys.stdout = old_stdin, old_stdout

    def test_fork_subagent_passes_through_untouched(self):
        # Given a fork spawn, which ignores model
        event = {"tool_input": {"subagent_type": "fork", "prompt": "Continue the prior task"}}
        # When the hook runs
        out = self._run(event)
        # Then nothing is printed and the spawn is left alone
        self.assertEqual(out, "")

    def test_already_routed_prompt_passes_through_untouched(self):
        # Given a prompt that already carries a Routed: header
        event = {"tool_input": {"prompt": "Routed: model=opus effort=high tier=frontier.\n\nDo the thing"}}
        out = self._run(event)
        self.assertEqual(out, "")

    def test_plain_spawn_gets_model_and_header_rewritten(self):
        # Given an ordinary Agent spawn with no routing yet
        event = {"tool_input": {"description": "rename a variable", "prompt": "Rename x to y in file.py"}}
        # When the hook runs
        out = self._run(event)
        # Then it emits an updated tool_input with the routed model and a Routed: header prepended
        payload = json.loads(out)
        updated = payload["hookSpecificOutput"]["updatedInput"]
        self.assertEqual(updated["model"], "sonnet")
        self.assertTrue(updated["prompt"].startswith("Routed: model=sonnet effort=medium"))
        self.assertIn("Rename x to y", updated["prompt"])


if __name__ == "__main__":
    unittest.main()
