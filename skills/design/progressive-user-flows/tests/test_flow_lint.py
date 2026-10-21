import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from flow_lint import lint  # noqa: E402

COMPLETE = """# Flow: Invite a teammate

## Happy path
## Alternative paths
## Error and recovery
## Interruptions and resume
## States

```mermaid
stateDiagram-v2
    [*] --> Editing
    Editing --> Sending : submit
    Sending --> Sent : 200
    Sending --> Failed : network error
    Failed --> Editing : retry keeps input
    Sent --> [*]
```
"""


class FlowLint(unittest.TestCase):
    def test_given_complete_flow_when_linted_then_clean(self):
        errors, warnings = lint(COMPLETE)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_given_state_unreachable_from_start_when_linted_then_error(self):
        text = COMPLETE.replace("    Sent --> [*]", "    Sent --> [*]\n    Orphan --> Sent")
        errors, _ = lint(text)
        self.assertTrue(any("Orphan" in e and "unreachable" in e for e in errors))

    def test_given_dead_end_state_when_linted_then_error(self):
        text = COMPLETE.replace("    Failed --> Editing : retry keeps input\n", "")
        errors, _ = lint(text)
        self.assertTrue(any("Failed" in e and "no way out" in e for e in errors))

    def test_given_happy_path_only_when_linted_then_warns_about_errors_and_sections(self):
        text = "```mermaid\nstateDiagram-v2\n    [*] --> A\n    A --> B\n    B --> [*]\n```\n"
        errors, warnings = lint(text)
        self.assertEqual(errors, [])
        self.assertTrue(any("error or recovery state" in w for w in warnings))
        self.assertTrue(any("Interruptions" in w for w in warnings))

    def test_given_german_section_headings_when_linted_then_recognized(self):
        text = COMPLETE
        for en, de in [("Happy path", "Hauptweg"), ("Alternative paths", "Alternative Wege"),
                       ("Error and recovery", "Fehler und Wiederherstellung"),
                       ("Interruptions and resume", "Unterbrechung und Wiederaufnahme"), ("States", "Zustände")]:
            text = text.replace(f"## {en}", f"## {de}")
        self.assertEqual(lint(text)[1], [])

    def test_given_no_state_diagram_when_linted_then_error(self):
        errors, _ = lint("# Flow\n\nJust prose.")
        self.assertTrue(errors)

    def test_given_the_bundled_example_when_linted_then_clean(self):
        example = Path(__file__).resolve().parents[1] / "references" / "example-approval-flow.md"
        self.assertEqual(lint(example.read_text(encoding="utf-8")), ([], []))


if __name__ == "__main__":
    unittest.main()
