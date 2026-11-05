import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from contrast import check_pairs, ratio, resolve  # noqa: E402

TOKENS = {
    "color": {
        "gray": {
            "900": {"$type": "color", "$value": "#111111"},
            "500": {"$type": "color", "$value": "#949494"},
            "0": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [1, 1, 1]}},
        },
        "text": {"default": {"$value": "{color.gray.900}"}, "muted": {"$value": "{color.gray.500}"}},
        "surface": {"default": {"$value": "{color.gray.0}"}},
    }
}


class Contrast(unittest.TestCase):
    def test_given_black_on_white_when_measured_then_ratio_is_21(self):
        self.assertAlmostEqual(ratio("#000000", "#ffffff"), 21.0, places=2)

    def test_given_known_gray_when_measured_then_matches_wcag_example(self):
        # #767676 on white is the commonly cited lightest gray that passes 4.5:1.
        self.assertGreaterEqual(ratio("#767676", "#ffffff"), 4.5)
        self.assertLess(ratio("#777777", "#ffffff"), 4.5)

    def test_given_dtcg_alias_and_srgb_object_when_resolved_then_hex(self):
        self.assertEqual(resolve(TOKENS, "color.text.default"), "#111111")
        self.assertEqual(resolve(TOKENS, "color.surface.default"), "#ffffff")

    def test_given_pairs_when_checked_then_text_threshold_applies_by_use(self):
        pairs = [
            {"fg": "color.text.default", "bg": "color.surface.default", "use": "text"},
            {"fg": "color.text.muted", "bg": "color.surface.default", "use": "text"},
            {"fg": "color.text.muted", "bg": "color.surface.default", "use": "ui"},
        ]
        results = check_pairs(TOKENS, pairs)
        self.assertEqual([r["pass"] for r in results], [True, False, True])

    def test_given_alias_cycle_when_resolved_then_value_error(self):
        tokens = {"a": {"$value": "{b}"}, "b": {"$value": "{a}"}}
        with self.assertRaises(ValueError):
            resolve(tokens, "a")


if __name__ == "__main__":
    unittest.main()
