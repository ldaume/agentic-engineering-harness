import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from quality_gate import check  # noqa: E402
from readability import diagnostics  # noqa: E402


class ReadabilityTest(unittest.TestCase):
    def test_given_simple_english_when_measured_then_flesch_is_high(self):
        result = diagnostics("The cat sat on the mat. It was warm.", "en")
        self.assertEqual(result["words"], 9)
        self.assertEqual(result["sentences"], 2)
        self.assertGreater(result["flesch_en"], 90)

    def test_given_german_text_when_measured_then_amstad_flesch_and_lix_are_reported(self):
        result = diagnostics("Der Export ist bereit. Wir starten den Pilot.", "de")
        self.assertIn("flesch_de", result)
        self.assertIn("lix", result)
        self.assertNotIn("flesch_en", result)

    def test_given_no_terminal_punctuation_when_measured_then_one_sentence_is_counted(self):
        self.assertEqual(diagnostics("just words here", "en")["sentences"], 1)


class CommitGateTest(unittest.TestCase):
    def test_given_generic_subject_when_checked_then_error(self):
        self.assertTrue(check("fixes", "commit", "en")["errors"])

    def test_given_long_subject_when_checked_then_warning_only(self):
        result = check("Check audit permission before creating the export job now", "commit", "en")
        self.assertFalse(result["errors"])
        self.assertTrue(result["warnings"])

    def test_given_body_without_blank_line_when_checked_then_error(self):
        self.assertTrue(check("Check audit permission\nReject early.", "commit", "en")["errors"])

    def test_given_good_commit_when_checked_then_clean(self):
        text = "Check audit permission before export\n\nReject unauthorized requests early."
        result = check(text, "commit", "en")
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])


class ArtifactGateTest(unittest.TestCase):
    def test_given_marketing_email_without_preview_when_checked_then_error(self):
        self.assertTrue(check("Subject: New export\n\nHi,\n\nbody", "marketing_email", "en")["errors"])

    def test_given_preview_repeating_subject_when_checked_then_error(self):
        text = "Subject: New export\nPreview: New export\n\nbody"
        self.assertTrue(check(text, "marketing_email", "en")["errors"])

    def test_given_hero_headline_over_twelve_words_when_checked_then_error(self):
        text = "# " + " ".join(["word"] * 13) + "\n\nSubhead."
        self.assertTrue(check(text, "hero", "en")["errors"])

    def test_given_pr_without_validation_when_checked_then_error(self):
        self.assertTrue(check("## Why\n\nBecause.\n\n## What changed\n\nStuff.", "pull_request", "en")["errors"])

    def test_given_german_status_with_all_sections_when_checked_then_clean(self):
        text = "Signal: gut\nOutcome: x\nGelernt: y\nRisiko: z\nNächster Fokus: w"
        self.assertEqual(check(text, "agile_status", "de")["errors"], [])

    def test_given_status_reporting_velocity_when_checked_then_error(self):
        text = "Signal: ok\nOutcome: velocity 42\nLearned: a\nRisk: b\nNext: c"
        self.assertTrue(check(text, "agile_status", "en")["warnings"])

    def test_given_progress_as_percent_complete_when_checked_then_error(self):
        text = "## Goal\nX\n## Current state\n70% complete\n## Next breakthrough\nY"
        self.assertTrue(check(text, "agile_progress", "en")["errors"])

    def test_given_forbidden_claim_when_checked_then_error(self):
        facts = {"forbidden_claims": ["30% fewer support requests"]}
        result = check("It gives you 30% fewer support requests.", "website_content", "en", facts)
        self.assertTrue(result["errors"])

    def test_given_unsourced_percentage_when_checked_then_warning(self):
        result = check("Teams ship 40% faster.", "website_content", "en", {"facts": []})
        self.assertFalse(result["errors"])
        self.assertTrue(any("40%" in w for w in result["warnings"]))

    def test_given_percentage_in_facts_when_checked_then_no_warning(self):
        facts = {"facts": ["Pilot reduced tickets by 40%."]}
        result = check("Pilot reduced tickets by 40%.", "website_content", "en", facts)
        self.assertFalse(any("40%" in w for w in result["warnings"]))

    def test_given_status_mentioning_next_only_in_prose_when_checked_then_missing_next_focus(self):
        text = "Signal: ok\nOutcome: a\nLearned: b\nRisk: c\nWe hope the next release helps."
        self.assertTrue(any("next" in e for e in check(text, "agile_status", "en")["errors"]))

    def test_given_german_label_naechsten_schritte_when_checked_then_next_focus_found(self):
        text = "**Signal:** ok\n**Outcome:** a\n**Gelernt:** b\n**Risiko:** c\n**Nächsten Schritte:** d"
        self.assertEqual(check(text, "agile_status", "de")["errors"], [])

    def test_given_status_negating_velocity_when_checked_then_warning_not_error(self):
        text = "Signal: ok\nOutcome: we do not report velocity\nLearned: b\nRisk: c\nNext: d"
        result = check(text, "agile_status", "en")
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["warnings"])

    def test_given_slack_greeting_when_checked_then_warning_not_error(self):
        result = check("Hallo Team,\n\nbitte kurz schauen.", "slack", "de")
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["warnings"])

    def test_given_two_word_generic_commit_when_checked_then_error(self):
        for subject in ("Fix bug", "fix: typo", "Update stuff", "Anpassungen"):
            self.assertTrue(check(subject, "commit", "en")["errors"], subject)

    def test_given_spaced_or_german_percent_when_fact_has_it_then_no_warning(self):
        facts = {"facts": ["Tickets fell by 3,5%."]}
        result = check("Tickets fell by 3.5 Prozent.", "website_content", "de", facts)
        self.assertFalse(any("3" in w for w in result["warnings"]))

    def test_given_112_percent_when_fact_has_12_percent_then_warning(self):
        result = check("Up 112%.", "website_content", "en", {"facts": ["Up 12%."]})
        self.assertTrue(any("112" in w for w in result["warnings"]))

    def test_given_accented_words_when_counted_then_each_is_one_word(self):
        self.assertEqual(diagnostics("Café naïve São.", "en")["words"], 3)

    def test_given_pr_with_motivation_and_test_plan_when_checked_then_clean(self):
        text = "## Motivation\n\nBecause.\n\n## Test plan\n\nRan unit tests."
        self.assertEqual(check(text, "pull_request", "en")["errors"], [])

    def test_given_status_as_bullet_list_when_checked_then_sections_found(self):
        text = "- Signal: ok\n- Outcome: a\n- Learned: b\n- Risks: c\n- Next: d"
        self.assertEqual(check(text, "agile_status", "en")["errors"], [])

    def test_given_german_label_with_leading_words_when_checked_then_learning_found(self):
        text = "Signal: ok\nErgebnis: a\nWas wir gelernt haben: b\nRisiko: c\nNächste Schritte: d"
        self.assertEqual(check(text, "agile_status", "de")["errors"], [])

    def test_given_reply_email_without_subject_when_checked_then_warning_not_error(self):
        result = check("Hi Anna,\n\nthanks, Friday works.\n\nAlex", "business_email", "en")
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["warnings"])

    def test_given_german_abbreviations_and_ordinals_when_measured_then_one_sentence(self):
        self.assertEqual(diagnostics("Wir starten z. B. am 3. Oktober u. a. mit Tests, d. h. früh.", "de")["sentences"], 1)

    def test_given_markdown_headings_and_bullets_when_measured_then_each_line_is_a_sentence(self):
        text = "# Status\n\n- Export bereit\n- Pilot startet\n- Review danach"
        self.assertEqual(diagnostics(text, "de")["sentences"], 4)

    def test_given_unknown_artifact_when_checked_then_value_error(self):
        with self.assertRaises(ValueError):
            check("x", "poem", "en")


if __name__ == "__main__":
    unittest.main()
