import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import quality_gate  # noqa: E402
from quality_gate import JEV_DATA, jev_keys, jev_request, jev_tier, text_sections  # noqa: E402

GATEWAY = {"VERCEL_AI_GATEWAY_API_KEY": "gw-test"}
DIRECT = {"TYPESAFE_API_KEY": "ts-test"}
SECTIONS = [("Export", "Der Export legt Dateien als Archiv ab."), ("Rollen", "Heute bewusst schlank, damit wir schnell lernen.")]


def stub(probabilities, calls):
    """A Jev stand-in: records each request and answers every question with its probability (default 0.1)."""
    def post(url, headers, body):
        calls.append((url, headers, body))
        questions = body.get("questions", {})
        return {"answers": {q: {"probability": probabilities.get(q, 0.1)} for q in questions}, "usage": {"inputTokens": 1000},
                "providerMetadata": {"gateway": {"cost": "0.0008"}}}
    return post


class JevDataTest(unittest.TestCase):
    def test_given_data_file_when_loaded_then_every_question_has_threshold_rule_and_two_examples(self):
        for qid, q in JEV_DATA["questions"].items():
            self.assertTrue(q["question"] and q["rule"], qid)
            self.assertEqual([e.split(":")[0] for e in q["examples"]], ["YES", "NO"], qid)
            self.assertTrue(q["threshold"] is None or 0.5 <= q["threshold"] < 1, qid)

    def test_given_pilot_result_when_loaded_then_unusable_questions_stay_in_the_bundle_unreported_and_universal_claim_is_stricter(self):
        qs = JEV_DATA["questions"]
        self.assertIsNone(qs["repetition"]["threshold"])
        self.assertIsNone(qs["unexplained_term"]["threshold"])
        self.assertEqual(qs["universal_claim"]["threshold"], 0.8)
        self.assertEqual(qs["tell_filler"]["threshold"], 0.7)


class JevKeysTest(unittest.TestCase):
    def test_given_gateway_and_direct_keys_when_resolved_then_gateway_wins(self):
        self.assertEqual(jev_keys({**GATEWAY, **DIRECT}), ("gateway", "gw-test"))
        self.assertEqual(jev_keys({"AI_GATEWAY_API_KEY": "a"}), ("gateway", "a"))

    def test_given_only_direct_key_when_resolved_then_direct(self):
        self.assertEqual(jev_keys(DIRECT), ("typesafe", "ts-test"))

    def test_given_no_key_when_resolved_then_none(self):
        self.assertIsNone(jev_keys({}))


class JevRequestTest(unittest.TestCase):
    def test_given_gateway_key_when_built_then_boolean_questions_private_routing_and_arm_c_state(self):
        url, headers, body = jev_request(SECTIONS[1], SECTIONS, "Readers", ("gateway", "gw"))
        self.assertTrue(url.endswith("/v4/ai/decision-model"))
        self.assertEqual(headers["ai-model-id"], "typesafe-ai/jev")
        self.assertEqual(body["providerOptions"]["gateway"], {"zeroDataRetention": True, "disallowPromptTraining": True, "only": ["typesafe-ai"]})
        self.assertEqual({q["type"] for q in body["questions"].values()}, {"boolean"})
        parts = [p["text"] for p in body["stateParts"]]
        self.assertTrue(parts[0].startswith("labeled_examples"))
        self.assertTrue(parts[1].startswith("skill_rules"))
        self.assertIn("section_heading: Rollen", parts)
        others = next(p for p in parts if p.startswith("other_sections"))
        self.assertIn("Export", others)
        self.assertNotIn("bewusst schlank", others)

    def test_given_direct_key_when_built_then_text_only_call_without_image_opt_in_or_assets(self):
        url, headers, body = jev_request(SECTIONS[0], SECTIONS, "Readers", ("typesafe", "ts"))
        self.assertIn("api.typesafe.ai", url)
        self.assertNotIn("TypeSafe-Danger-Zone-Images", headers)
        self.assertNotIn("assets", body)
        self.assertEqual({q["type"] for q in body["questions"].values()}, {"noul"})
        self.assertEqual(body["state"]["section_heading"], "Export")


class JevTierTest(unittest.TestCase):
    def test_given_no_key_when_run_then_skipped_without_a_call(self):
        calls = []
        result = jev_tier(SECTIONS, "Readers", {}, post=stub({}, calls))
        self.assertEqual(calls, [])
        self.assertEqual(result["warnings"], [])
        self.assertTrue(result["note"].startswith("Jev tier skipped: no key"))

    def test_given_hit_above_threshold_when_run_then_one_tagged_warning_per_section(self):
        calls = []
        result = jev_tier(SECTIONS, "Readers", GATEWAY, post=stub({"tell_filler": 0.83}, calls))
        self.assertEqual(len(calls), 2)
        self.assertEqual(len(result["warnings"]), 2)
        self.assertTrue(all(w.startswith("jev: tell_filler p=0.83") for w in result["warnings"]))
        self.assertIn("'Rollen'", result["warnings"][1])
        self.assertAlmostEqual(result["cost_usd"], 0.0016)

    def test_given_universal_claim_between_0_7_and_0_8_when_run_then_no_warning(self):
        result = jev_tier(SECTIONS[:1], "Readers", GATEWAY, post=stub({"universal_claim": 0.75, "contradiction": 0.75}, []))
        self.assertEqual([w.split()[1] for w in result["warnings"]], ["contradiction"])

    def test_given_unreported_question_answered_yes_when_run_then_no_warning(self):
        result = jev_tier(SECTIONS[:1], "Readers", GATEWAY, post=stub({"repetition": 0.99, "unexplained_term": 0.99}, []))
        self.assertEqual(result["warnings"], [])

    def test_given_jev_fails_when_run_then_fails_open_with_reason(self):
        def broken(url, headers, body):
            raise OSError("HTTP 503")
        result = jev_tier(SECTIONS, "Readers", GATEWAY, post=broken)
        self.assertEqual(result["warnings"], [])
        self.assertIn("Jev tier skipped", result["note"])
        self.assertIn("HTTP 503", result["note"])


class SectionsTest(unittest.TestCase):
    def test_given_markdown_with_headings_when_split_then_one_section_per_heading(self):
        text = "Intro line.\n\n## Export\nDer Export.\n\n## Rollen\nZwei Rollen."
        self.assertEqual(text_sections(text), [("", "Intro line."), ("Export", "Der Export."), ("Rollen", "Zwei Rollen.")])

    def test_given_html_section_with_table_when_split_then_cells_count_and_h2_names_it(self):
        page = ('<section id="todo"><h2><span class="l-de">Offen</span><span class="l-en">Open</span></h2>'
                '<p class="l-de">Zwei Punkte sind offen.</p><p class="l-en">Two items are open.</p>'
                '<table><tr><th>Punkt</th><th>Status</th></tr><tr><td>Export</td><td>geplant</td></tr></table>'
                '<script>var x = 1;</script></section><section id="b"><h2>Zweiter</h2><p>Text.</p></section>')
        sections = quality_gate.html_page_sections(page, "l-de")
        self.assertEqual([h for h, _ in sections], ["Offen", "Zweiter"])
        body = sections[0][1]
        self.assertIn("Export | geplant", body)
        self.assertIn("Zwei Punkte sind offen.", body)
        self.assertNotIn("Two items", body)
        self.assertNotIn("var x", body)

    def test_given_text_without_headings_when_split_then_one_section(self):
        self.assertEqual(text_sections("Just one paragraph."), [("", "Just one paragraph.")])


class CliTest(unittest.TestCase):
    def run_main(self, argv, env, post):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict("os.environ", env, clear=True), mock.patch.object(quality_gate, "jev_post", post), redirect_stdout(out), redirect_stderr(err):
            code = quality_gate.main(argv)
        return code, json.loads(out.getvalue()), err.getvalue()

    def test_given_key_but_no_flag_when_gated_then_no_jev_call(self):
        calls = []
        with mock.patch("sys.stdin", io.StringIO("## A\nText.")):
            code, result, _ = self.run_main(["--artifact", "prose", "--lang", "de"], GATEWAY, stub({}, calls))
        self.assertEqual(calls, [])
        self.assertNotIn("jev", result)

    def test_given_flag_and_hit_when_gated_then_warning_but_exit_zero(self):
        with mock.patch("sys.stdin", io.StringIO("## A\nText.")):
            code, result, _ = self.run_main(["--artifact", "prose", "--lang", "de", "--jev"], GATEWAY, stub({"provoking": 0.9}, []))
        self.assertEqual(code, 0)
        self.assertTrue(any(w.startswith("jev: provoking p=0.90") for w in result["warnings"]))
        self.assertEqual(result["jev"]["calls"], 1)

    def test_given_flag_without_key_when_gated_then_skip_note_on_stderr(self):
        with mock.patch("sys.stdin", io.StringIO("## A\nText.")):
            code, result, err = self.run_main(["--artifact", "prose", "--lang", "de", "--jev"], {}, stub({}, []))
        self.assertEqual(code, 0)
        self.assertIn("Jev tier skipped: no key", err)
        self.assertIn("Jev tier skipped: no key", result["jev"]["note"])

    def test_given_bilingual_page_with_auto_when_gated_then_each_language_asks_per_section(self):
        page = '<h2>Export</h2><p class="l-de">Der Export legt Dateien ab.</p><p class="l-en">The export stores files.</p>'
        calls = []
        with mock.patch("sys.stdin", io.StringIO(page)):
            code, result, _ = self.run_main(["--artifact", "prose", "--html", "--lang-class", "auto", "--jev"], GATEWAY, stub({"tell_closer": 0.95}, calls))
        self.assertEqual(len(calls), 2)
        self.assertEqual(sorted(w.split(":")[0] for w in result["warnings"] if "jev:" in w), ["de", "en"])
        self.assertEqual(result["languages"]["de"]["jev"]["calls"], 1)


if __name__ == "__main__":
    unittest.main()
