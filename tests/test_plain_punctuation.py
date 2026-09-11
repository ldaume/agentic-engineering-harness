"""Tests for the plain punctuation gate.

Banned characters are written as escapes here on purpose: the gate scans its
own repository, so a literal sample would fail the check it is testing.
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify-plain-punctuation.py"

_spec = importlib.util.spec_from_file_location("verify_plain_punctuation", SCRIPT)
assert _spec and _spec.loader
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)

EM_DASH = "\u2014"        # allowed since 2026-09-11: ordinary typography
EN_DASH = "\u2013"        # allowed for the same reason
NB_HYPHEN = "\u2011"      # banned: indistinguishable from "-" to a reader
LEFT_DOUBLE = "\u201c"
RIGHT_DOUBLE = "\u201d"
RIGHT_SINGLE = "\u2019"
ELLIPSIS = "\u2026"
NO_BREAK_SPACE = "\u00a0"
ZERO_WIDTH = "\u200b"
BOM = "\ufeff"
LTR_MARK = "\u200e"
ARROW = "\u2192"
UMLAUT_U = "\u00fc"


class BannedTable(unittest.TestCase):
    def test_covers_the_common_model_typography(self) -> None:
        for code in (
            0x2011,  # non-breaking hyphen, a look-alike for "-"
            0x2018,  # left single quote
            0x2019,  # right single quote
            0x201C,  # left double quote
            0x201D,  # right double quote
            0x2026,  # ellipsis
            0x00A0,  # no-break space
            0x200B,  # zero width space
            0xFEFF,  # BOM
            0x00B7,  # middle dot separator
        ):
            self.assertIn(code, gate.BANNED, f"U+{code:04X} must stay banned")

    def test_keeps_functional_symbols_and_letters_allowed(self) -> None:
        """Pin the allow-list, so "not ASCII only" stays enforced, not promised.

        The rule bans a short closed list where the ASCII spelling is strictly
        better. Everything here must stay out of the table; see
        docs/adr/0002 **What the rule does not ban**.
        """
        for code in (
            # arrows
            0x2192,  # rightwards arrow
            0x2194,  # left right arrow
            0x21D2,  # rightwards double arrow
            0x2191,  # upwards arrow
            0x2193,  # downwards arrow
            # box drawing and functional geometry
            0x2502,  # box drawings light vertical
            0x2500,  # box drawings light horizontal
            0x2514,  # box drawings light up and right
            0x25BC,  # black down-pointing triangle
            # natural-language letters
            0x00E4,  # a with diaeresis
            0x00F6,  # o with diaeresis
            0x00FC,  # u with diaeresis
            0x00C4,  # capital A with diaeresis
            0x00D6,  # capital O with diaeresis
            0x00DC,  # capital U with diaeresis
            0x00DF,  # sharp s
            0x00E9,  # e with acute
            0x00E8,  # e with grave
            0x00E7,  # c with cedilla
            0x00F1,  # n with tilde
            0x00E5,  # a with ring above
            # math, logic, and currency
            0x2264,  # less-than or equal to
            0x2265,  # greater-than or equal to
            0x2260,  # not equal to
            0x00B1,  # plus-minus sign
            0x00D7,  # multiplication sign
            0x00F7,  # division sign
            0x00B0,  # degree sign
            0x221E,  # infinity
            0x2211,  # n-ary summation
            0x20AC,  # euro sign
            0x00A3,  # pound sign
        ):
            self.assertNotIn(code, gate.BANNED, f"U+{code:04X} must stay allowed")

    def test_three_dots_are_the_canonical_ellipsis(self) -> None:
        """`...` is the replacement the rule prescribes, so it can never fail."""
        self.assertEqual(gate.BANNED[0x2026][2], "...")
        for char in "...":
            self.assertNotIn(ord(char), gate.BANNED)

    def test_every_entry_is_complete_and_ascii_spellable(self) -> None:
        for code, (category, name, replacement) in gate.BANNED.items():
            self.assertTrue(category, f"U+{code:04X} lacks a category")
            self.assertTrue(name, f"U+{code:04X} lacks a name")
            self.assertTrue(
                replacement.isascii(),
                f"U+{code:04X} replacement must be ASCII",
            )

    def test_gate_sources_are_free_of_banned_characters(self) -> None:
        """The tables must be spelled with escapes, never literal samples."""
        for path in (SCRIPT, Path(__file__)):
            self.assertEqual(
                gate.findings(path.read_text(encoding="utf-8")),
                [],
                f"{path.name} must not contain banned characters literally",
            )


class Findings(unittest.TestCase):
    def test_reports_line_and_column(self) -> None:
        text = f"clean line\nbroken {NB_HYPHEN} line\n"
        self.assertEqual(gate.findings(text), [(2, 8, 0x2011)])

    def test_accepts_arrows_and_umlauts(self) -> None:
        text = f"provider {ARROW} consumer, gepr{UMLAUT_U}ft"
        self.assertEqual(gate.findings(text), [])

    def test_accepts_a_document_full_of_allowed_characters(self) -> None:
        """End to end: real German prose, arrows, math, and `...` all pass.

        The per-code-point check above proves the table is right. This proves
        the scanner agrees on real text, which is what a human actually asks
        about.
        """
        text = "\n".join(
            (
                "Umlaute: \u00c4pfel, \u00d6l, \u00dcber, Stra\u00dfe, sch\u00f6n, f\u00fcr.",
                "Akzente: caf\u00e9, na\u00efve, se\u00f1or, \u00c5ngstr\u00f6m, gar\u00e7on.",
                "Pfeile: -> <- => und \u2192 \u2190 \u2194 \u21d2 \u2191 \u2193.",
                "Diagramm: \u251c\u2500\u2500 \u2514\u2500\u2500 \u2502",
                "Mathe: \u2264 \u2265 \u2260 \u00b1 \u00d7 \u00f7 \u00b0 \u221e \u2211",
                "Waehrung: \u20ac \u00a3 \u00a5",
                "Auslassung: warte mal ... und weiter ...",
                "Bindestrich und Zitat: gut-genug, \"so\", 'so'.",
            )
        )
        self.assertEqual(gate.findings(text), [])

    def test_flags_an_invisible_character(self) -> None:
        self.assertEqual(gate.findings(f"a{ZERO_WIDTH}b"), [(1, 2, 0x200B)])


class Repair(unittest.TestCase):
    def test_an_em_dash_survives_repair(self) -> None:
        # Ordinary typography, so `--fix` must not reword a sentence that
        # chose it.
        text = f"a sentence {EM_DASH} with an aside"
        self.assertEqual(gate.repair(text), text)

    def test_rewrites_quotes_lookalike_hyphens_and_ellipsis(self) -> None:
        text = (
            f"{LEFT_DOUBLE}value{RIGHT_SINGLE}s{RIGHT_DOUBLE}"
            f" {NB_HYPHEN} wait{ELLIPSIS}"
        )
        self.assertEqual(gate.repair(text), '"value\'s" - wait...')

    def test_removes_invisible_characters(self) -> None:
        self.assertEqual(gate.repair(f"a{ZERO_WIDTH}{BOM}b"), "ab")

    def test_collapses_exotic_spaces_to_one_space(self) -> None:
        self.assertEqual(gate.repair(f"a{NO_BREAK_SPACE}b"), "a b")

    def test_leaves_allowed_characters_untouched(self) -> None:
        text = f"provider {ARROW} consumer, gepr{UMLAUT_U}ft"
        self.assertEqual(gate.repair(text), text)

    def test_repaired_text_passes_the_gate(self) -> None:
        text = (
            f"{LEFT_DOUBLE}a{RIGHT_DOUBLE} {EN_DASH} b{ELLIPSIS}"
            f" c{NO_BREAK_SPACE}d{LTR_MARK}"
        )
        self.assertEqual(gate.findings(gate.repair(text)), [])


class Describe(unittest.TestCase):
    def test_names_the_ascii_spelling(self) -> None:
        self.assertIn('use "-"', gate.describe(0x2011))
        self.assertIn("NON-BREAKING HYPHEN", gate.describe(0x2011))

    def test_says_remove_for_invisible_characters(self) -> None:
        self.assertIn("remove", gate.describe(0x200B))


class Files(unittest.TestCase):
    def test_binary_content_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "blob.bin"
            path.write_bytes(b"\x00\x01\x02")
            self.assertIsNone(gate.read_text(path))

    def test_utf8_text_is_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "note.md"
            path.write_text(f"gepr{UMLAUT_U}ft\n", encoding="utf-8")
            self.assertEqual(gate.read_text(path), f"gepr{UMLAUT_U}ft\n")


class JsonRepair(unittest.TestCase):
    """A repair must not turn a valid document into a broken one.

    A run over a translation file produced `"Suggestion for "{title}""`: a
    straight quote inside a JSON string value is syntax, not text. A pre-commit
    hook rejected it; a less careful pipeline would have committed
    syntactically invalid JSON on behalf of a typography rule.
    """

    def test_a_quote_inside_a_json_string_is_escaped(self) -> None:
        source = '{"k": "Suggestion for ' + LEFT_DOUBLE + '{t}' + RIGHT_DOUBLE + '"}'
        fixed, refusal = gate.repair_file_text(source, "messages/en.json")
        self.assertIsNone(refusal)
        self.assertEqual(json.loads(fixed)["k"], 'Suggestion for "{t}"')

    def test_prose_outside_json_keeps_the_bare_quote(self) -> None:
        self.assertEqual(
            gate.repair("He said " + LEFT_DOUBLE + "hello" + RIGHT_DOUBLE),
            'He said "hello"',
        )

    def test_a_repair_that_would_not_parse_is_refused(self) -> None:
        source = '{"k": "unterminated ' + LEFT_DOUBLE + '}'
        fixed, refusal = gate.repair_file_text(source, "broken.json")
        self.assertEqual(fixed, source)
        self.assertIn("would not parse as JSON", refusal or "")

    def test_jsonc_is_escaped_but_not_parsed(self) -> None:
        source = '// note\n{"k": "a ' + LEFT_DOUBLE + 'b' + RIGHT_DOUBLE + '"}'
        fixed, refusal = gate.repair_file_text(source, "tsconfig.jsonc")
        self.assertIsNone(refusal)
        self.assertIn('\\"b\\"', fixed)


if __name__ == "__main__":
    unittest.main()
