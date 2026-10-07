import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify-agent-attribution.py"


def load_module():
    spec = importlib.util.spec_from_file_location("verify_agent_attribution", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AgentAttributionTests(unittest.TestCase):
    def setUp(self):
        self.find = load_module().agent_attribution

    def test_an_agent_co_author_trailer_is_reported(self):
        # Given a commit message with a host's default co-author trailer
        message = "Fix the cache\n\nCo-Authored-By: Claude Opus <noreply@anthropic.com>"
        # Then exactly that trailer is reported
        self.assertEqual(self.find(message), ["Co-Authored-By: Claude Opus <noreply@anthropic.com>"])

    def test_a_generated_with_footer_is_reported(self):
        # Given a pull request body ending in a host-appended footer
        body = "## Checks\n\n- green\n\nGenerated with [Claude Code](https://claude.com/claude-code)"
        # Then the footer is reported
        self.assertEqual(self.find(body), ["Generated with [Claude Code](https://claude.com/claude-code)"])

    def test_other_agents_and_session_trailers_are_reported(self):
        # Given trailers from three other agents and a session link
        message = "\n".join([
            "Fix it",
            "",
            "Co-authored-by: Codex <codex@openai.com>",
            "Co-authored-by: Cursor Agent <cursoragent@cursor.com>",
            "Made with Cursor",
            "Claude-Session: https://claude.ai/code/session_01",
        ])
        # Then each one is reported
        self.assertEqual(len(self.find(message)), 4)

    def test_a_human_co_author_passes(self):
        # Given a pairing trailer naming a person
        message = "Pair on the switch\n\nCo-authored-by: Ada Lovelace <ada@example.com>"
        # Then nothing is reported
        self.assertEqual(self.find(message), [])

    def test_prose_about_the_tooling_passes(self):
        # Given a change whose subject is the tooling itself
        body = "Turns off Claude Code's co-author trailer in the checked-in settings."
        # Then nothing is reported: only the stamp is chrome
        self.assertEqual(self.find(body), [])


if __name__ == "__main__":
    unittest.main()
