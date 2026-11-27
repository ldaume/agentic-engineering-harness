import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from quality_gate import check  # noqa: E402
from readability import diagnostics, html_blocks, html_sections, sentences  # noqa: E402


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


class GenderFormTest(unittest.TestCase):
    def test_given_gender_colon_or_star_when_checked_then_no_error_or_warning(self):
        text = "Alle Nutzer:innen und Entwickler*innen sehen den Export. Wir prüfen ihn heute."
        result = check(text, "prose", "de")
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


class AiTellGateTest(unittest.TestCase):
    """Patterns that made reviewed decks read as generated (2026-11-05 review)."""

    def test_given_german_nicht_x_sondern_y_when_checked_then_ai_tell_warning(self):
        text = "Die Garantie liegt nicht im Token, sondern im Code."
        result = check(text, "slides", "de")
        self.assertTrue(any("not X but Y" in w for w in result["warnings"]))

    def test_given_english_not_just_x_but_y_when_checked_then_ai_tell_warning(self):
        text = "It is not just a search, but a decision aid."
        result = check(text, "prose", "en")
        self.assertTrue(any("not X but Y" in w for w in result["warnings"]))

    def test_given_english_its_not_x_its_y_when_checked_then_ai_tell_warning(self):
        result = check("It's not a tool, it's a mirror.", "prose", "en")
        self.assertTrue(any("not X but Y" in w for w in result["warnings"]))

    def test_given_german_reversed_x_nicht_y_when_checked_then_ai_tell_warning(self):
        for text in ("Die Garantie liegt im Code, nicht im Token.",
                     "Die Qualität hängt am Wissen, nicht an der Suche.",
                     "Quellen stehen als Daten im Prompt, nicht als Anweisung."):
            warnings = check(text, "slides", "de")["warnings"]
            self.assertTrue(any("not X but Y" in w for w in warnings), text)

    def test_given_german_scope_or_list_negation_when_checked_then_no_warning(self):
        for text in ("Gemessen bis zur Prüfung, nicht bis zum Merge.",
                     "Kann nicht pushen, nicht mergen.",
                     "Gemergt wird in fester Reihenfolge, nicht atomar."):
            warnings = check(text, "slides", "de")["warnings"]
            self.assertFalse(any("not X but Y" in w for w in warnings), text)

    def test_given_english_reversed_x_not_y_when_checked_then_ai_tell_warning(self):
        warnings = check("Quality depends on the knowledge, not the search.", "prose", "en")["warnings"]
        self.assertTrue(any("not X but Y" in w for w in warnings))

    def test_given_stock_german_filler_when_checked_then_each_is_named(self):
        text = "Heute bewusst schlank. Die Checks kommen über ihre Prüfungen ins Spiel."
        warnings = check(text, "slides", "de")["warnings"]
        self.assertTrue(any("bewusst schlank" in w for w in warnings))
        self.assertTrue(any("ins Spiel" in w for w in warnings))

    def test_given_stock_english_filler_when_checked_then_warning(self):
        warnings = check("Caching plays a pivotal role in the landscape.", "prose", "en")["warnings"]
        self.assertTrue(any("pivotal" in w for w in warnings))

    def test_given_plain_statement_when_checked_then_no_ai_tell_warning(self):
        text = "Nichts wird in Jira geschrieben. Code und Tests sichern das ab."
        result = check(text, "slides", "de")
        self.assertFalse(any(w.startswith("ai-tell") for w in result["warnings"]))

    def test_given_ai_tell_in_any_artifact_when_checked_then_warning_not_error(self):
        result = check("Fix the export.\n\nNot a patch, but a rewrite.", "commit", "en")
        self.assertEqual(result["errors"], [])
        self.assertTrue(any(w.startswith("ai-tell") for w in result["warnings"]))


class TermGateTest(unittest.TestCase):
    """The audience's own term wins over a translation the writer invented."""

    def test_given_avoided_variant_when_checked_then_error_names_the_preferred_term(self):
        facts = {"terms": {"Knowledge Store": ["Wissensspeicher"]}}
        result = check("Der Wissensspeicher liefert Treffer.", "slides", "de", facts)
        self.assertTrue(any("Knowledge Store" in e and "Wissensspeicher" in e for e in result["errors"]))

    def test_given_preferred_term_when_checked_then_clean(self):
        facts = {"terms": {"Knowledge Store": ["Wissensspeicher"]}}
        result = check("Der Knowledge Store liefert Treffer.", "slides", "de", facts)
        self.assertEqual(result["errors"], [])

    def test_given_variant_inside_a_longer_word_when_checked_then_still_caught(self):
        facts = {"terms": {"Rate Limit": ["Abfragelimit"]}}
        result = check("Das Abfragelimits greift.", "slides", "de", facts)
        self.assertTrue(result["errors"])


PAGE = """<html><body>
<section id="intro"><h2>Intro</h2>
<div class="chips"><span>Chip one</span></div>
<p><span class="l-en">The export is ready.</span> <span class="l-de">Der Export ist bereit.</span></p>
<ul><li>Outer item <ul><li>Inner item one</li><li>Inner item two</li></ul> tail</li></ul>
<table><tr><td>Cell alpha</td><td>Cell beta</td></tr></table>
<script>var s = "Script words here.";</script>
<div class="mermaid">graph TD; A-->B;</div>
<p class="mermaid-legend">Legend under the diagram.</p>
<figure><svg></svg><figcaption>Caption of the figure.</figcaption></figure>
</section>
<section id="detail"><h2>Detail</h2><dl><dd>One more sentence.</dd></dl></section>
</body></html>"""


class HtmlInputTest(unittest.TestCase):
    def test_given_page_when_extracted_then_only_prose_blocks_remain(self):
        blocks = [b for _, b in html_blocks(PAGE)]
        joined = " ".join(blocks)
        for noise in ("Cell alpha", "Script words", "graph TD", "Chip one"):
            self.assertNotIn(noise, joined)
        self.assertIn("The export is ready. Der Export ist bereit.", blocks)

    def test_given_diagram_caption_or_legend_when_extracted_then_it_is_prose(self):
        blocks = [b for _, b in html_blocks(PAGE)]
        self.assertIn("Legend under the diagram.", blocks)
        self.assertIn("Caption of the figure.", blocks)

    def test_given_nested_lists_when_extracted_then_items_stay_separate(self):
        blocks = [b for _, b in html_blocks(PAGE)]
        self.assertIn("Outer item", blocks)
        self.assertIn("Inner item one", blocks)
        self.assertIn("Inner item two", blocks)
        self.assertIn("tail", blocks)

    def test_given_language_class_when_extracted_then_other_language_is_dropped(self):
        text = " ".join(b for _, b in html_blocks(PAGE, lang_class="l-de"))
        self.assertIn("Der Export ist bereit.", text)
        self.assertNotIn("The export is ready.", text)

    def test_given_page_when_reported_per_section_then_each_section_has_counts(self):
        report = {r["section"]: r for r in html_sections(PAGE, "en", "l-en")}
        self.assertEqual(set(report), {"intro", "detail"})
        self.assertEqual(report["detail"]["words"], 3)
        self.assertEqual(report["intro"]["words"], 4 + 2 + 3 + 3 + 1 + 4 + 4)
        self.assertIn("lix", report["intro"])


class EnumerationGateTest(unittest.TestCase):
    def test_given_enumeration_chain_when_checked_then_list_warning(self):
        result = check("We ship the parser, the gate, the report and the tests.", "prose", "en")
        self.assertTrue(any("enumeration" in w for w in result["warnings"]))

    def test_given_two_semicolons_when_checked_then_list_warning(self):
        result = check("The gate reads text; it counts words; it prints a report.", "prose", "en")
        self.assertTrue(any("semicolons" in w for w in result["warnings"]))

    def test_given_german_decimals_and_pair_when_checked_then_no_warning(self):
        text = "Der Wert liegt bei 1,5 und 2,5 oder 3,5. Wir prüfen Text und Tabellen."
        result = check(text, "prose", "de")
        self.assertFalse([w for w in result["warnings"] if "list" in w])


class LangDefaultTest(unittest.TestCase):
    HTML = '<p class="l-de">Der Export ist bereit. Wir starten den Pilot.</p><p class="l-en">The cat sat.</p>'

    def run_cli(self, script, *args):
        import json
        import subprocess

        out = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / script), *args],
            input=self.HTML, capture_output=True, text=True,
        )
        return json.loads(out.stdout)

    def test_given_lang_class_de_and_no_lang_when_measured_then_german_formulas(self):
        result = self.run_cli("readability.py", "--html", "--lang-class", "l-de")
        self.assertIn("flesch_de", result)
        self.assertNotIn("flesch_en", result)

    def test_given_explicit_lang_when_lang_class_differs_then_explicit_wins(self):
        result = self.run_cli("readability.py", "--html", "--lang-class", "l-de", "--lang", "en")
        self.assertIn("flesch_en", result)

    def test_given_lang_class_de_and_no_lang_when_gated_then_language_is_de(self):
        result = self.run_cli("quality_gate.py", "--artifact", "prose", "--html", "--lang-class", "l-de")
        self.assertEqual(result["language"], "de")

    def test_given_no_lang_and_no_lang_class_when_measured_then_english(self):
        result = self.run_cli("readability.py", "--html")
        self.assertIn("flesch_en", result)


class LimitsTest(unittest.TestCase):
    def test_given_28_word_german_sentence_when_gated_then_over_german_max(self):
        text = " ".join(["Wort"] * 28) + "."
        warnings = check(text, "website_content", "de")["warnings"]
        self.assertTrue(any("over 25 words" in w for w in warnings))

    def test_given_28_word_english_sentence_when_gated_then_no_max_warning(self):
        text = " ".join(["word"] * 28) + "."
        warnings = check(text, "website_content", "en")["warnings"]
        self.assertFalse(any("readability: 1 sentence" in w for w in warnings))

    def test_given_31_word_english_sentence_when_gated_then_over_english_max(self):
        text = " ".join(["word"] * 31) + "."
        warnings = check(text, "website_content", "en")["warnings"]
        self.assertTrue(any("over 30 words" in w for w in warnings))

    def test_given_german_mean_16_when_gated_then_mean_warning(self):
        text = " ".join(" ".join(["Wort"] * 16) + "." for _ in range(3))
        warnings = check(text, "website_content", "de")["warnings"]
        self.assertTrue(any("mean sentence length" in w and "15" in w for w in warnings))

    def test_given_english_mean_16_when_gated_then_no_mean_warning(self):
        text = " ".join(" ".join(["word"] * 16) + "." for _ in range(3))
        warnings = check(text, "website_content", "en")["warnings"]
        self.assertFalse(any("mean sentence length" in w for w in warnings))


class SplitterTest(unittest.TestCase):
    CASES = [
        ("Wir nutzen z. B. Tabellen und Listen heute.", 1),
        ("Das heißt d. h. wir starten heute.", 1),
        ("Es gibt u. a. drei Optionen hier.", 1),
        ("Wir liefern A bzw. B am Montag.", 1),
        ("Es kostet ca. 5 Euro im Monat.", 1),
        ("Siehe Nr. 5 im Anhang dazu.", 1),
        ("Wir treffen uns am 20. November im Büro.", 1),
        ("Use tools, e.g. a linter, daily.", 1),
        ("That is, i.e. the plan, final.", 1),
        ("Compare A vs. B before you ship.", 1),
        ("The U.S. team ships on Monday.", 1),
        ("Der Wert ist 1,5 und der Rest 2,5 Prozent.", 1),
        ("The value is 1.5 and the rest 2.5 percent.", 1),
        ("Install v1.2.3 before you start.", 1),
        ("Der Export ist bereit. Wir starten den Pilot.", 2),
    ]

    def test_given_abbreviation_decimal_or_version_when_split_then_no_false_break(self):
        for text, expected in self.CASES:
            with self.subTest(text=text):
                self.assertEqual(len(sentences(text)), expected)


class BilingualTest(unittest.TestCase):
    PAGE = (
        '<div><p class="l-de">Der Export ist bereit. Wir starten heute.</p>'
        '<p class="l-en">The export is ready. We start today.</p>'
        '<p class="l-de">Nur deutsch hier.</p>'
        '<p class="l-de">Eins.</p><p class="l-en">One two three four five six seven eight nine ten.</p></div>'
    )

    def test_given_bilingual_page_when_auto_then_each_language_has_own_formulas(self):
        from readability import bilingual_report

        report = bilingual_report(self.PAGE)
        self.assertIn("flesch_de", report["languages"]["de"])
        self.assertIn("flesch_en", report["languages"]["en"])
        self.assertNotIn("flesch_en", report["languages"]["de"])

    def test_given_missing_twin_when_audited_then_parity_warning(self):
        from readability import bilingual_report

        warnings = bilingual_report(self.PAGE)["parity"]
        self.assertTrue(any("no twin" in w and "Nur deutsch" in w for w in warnings))

    def test_given_lopsided_twin_when_audited_then_parity_warning(self):
        from readability import bilingual_report

        warnings = bilingual_report(self.PAGE)["parity"]
        self.assertTrue(any("word counts" in w and "Eins" in w for w in warnings))

    def test_given_clean_pair_when_audited_then_no_parity_warning(self):
        from readability import bilingual_report

        page = '<div><p class="l-de">Der Export ist bereit.</p><p class="l-en">The export is ready.</p></div>'
        self.assertEqual(bilingual_report(page)["parity"], [])

    def test_given_auto_when_gate_runs_then_report_per_language(self):
        import json
        import subprocess

        out = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "quality_gate.py"),
             "--artifact", "website_content", "--html", "--lang-class", "auto"],
            input=self.PAGE, capture_output=True, text=True,
        )
        result = json.loads(out.stdout)
        self.assertEqual(sorted(result["languages"]), ["de", "en"])
        self.assertEqual(result["languages"]["de"]["language"], "de")
        self.assertTrue(any("no twin" in w for w in result["warnings"]))


def warned(text, lang="en", facts=None, artifact="prose"):
    return check(text, artifact, lang, facts)["warnings"]


class RepetitionTest(unittest.TestCase):
    def test_given_point_restated_in_other_words_when_checked_then_near_duplicate_warning(self):
        text = ("The export job checks the audit permission before it creates the file. "
                "Teams agree on the rollout date next week. "
                "Before it creates the file, the export job checks the audit permission.")
        self.assertTrue(any(w.startswith("repetition:") for w in warned(text)))

    def test_given_identical_sentence_twice_when_checked_then_warning(self):
        s = "The export job rejects unauthorized requests before any data is read."
        self.assertTrue(any(w.startswith("repetition:") for w in warned(f"{s} Other things happen too. {s}")))

    def test_given_two_different_sentences_on_same_topic_when_checked_then_no_warning(self):
        text = ("The export job checks the audit permission before it creates the file. "
                "The export job writes every result into a signed archive with a retention label.")
        self.assertFalse(any(w.startswith("repetition:") for w in warned(text)))

    def test_given_one_sentence_repeated_in_every_section_when_checked_then_one_warning_with_count(self):
        s = "Without reprint and self-publishing houses the list keeps most of its titles."
        text = " ".join(f"{s} Section {n} has its own facts here." for n in range(6))
        repeated = [w for w in warned(text) if w.startswith("repetition:")]
        self.assertEqual(len(repeated), 1)
        self.assertIn("6 sentences", repeated[0])

    def test_given_short_repeated_sentences_when_checked_then_no_warning(self):
        self.assertFalse(any(w.startswith("repetition:") for w in warned("Thanks a lot. Thanks a lot.")))

    def test_given_german_restatement_when_checked_then_warning(self):
        text = ("Der Export prüft die Berechtigung des Audits vor dem Anlegen der Datei. "
                "Wir sprechen nächste Woche über den Termin. "
                "Vor dem Anlegen der Datei prüft der Export die Berechtigung des Audits.")
        self.assertTrue(any(w.startswith("repetition:") for w in warned(text, "de")))


class FigureConsistencyTest(unittest.TestCase):
    def test_given_same_label_with_two_amounts_when_checked_then_warning(self):
        text = "The annual license costs 919 USD for one seat. Later the annual license costs 920 USD."
        self.assertTrue(any(w.startswith("figures:") for w in warned(text)))

    def test_given_same_label_and_same_amount_when_checked_then_no_warning(self):
        text = "The annual license costs 919 USD. Later the annual license costs 919 USD."
        self.assertFalse(any(w.startswith("figures:") for w in warned(text)))

    def test_given_different_labels_when_checked_then_no_warning(self):
        text = "The setup fee is 919 USD. The monthly fee is 920 USD."
        self.assertFalse(any(w.startswith("figures:") for w in warned(text)))


class CurrentTellsTest(unittest.TestCase):
    def test_given_chat_residue_when_checked_then_ai_tell(self):
        for t, lang in (("Here is the plan. I hope this helps!", "en"), ("Let me know if you need more.", "en"),
                        ("Natürlich! Hier ist der Plan.", "de"), ("Ich hoffe, das hilft dir weiter.", "de")):
            self.assertTrue(any("chat residue" in w for w in warned(t, lang)), t)

    def test_given_copula_avoidance_when_checked_then_ai_tell(self):
        for t, lang in (("The library serves as a bridge between teams.", "en"), ("The town boasts a market.", "en"),
                        ("Das Modul stellt eine zentrale Schnittstelle dar.", "de"), ("Es fungiert als Vermittler.", "de")):
            self.assertTrue(any("copula" in w for w in warned(t, lang)), t)

    def test_given_vague_attribution_when_checked_then_ai_tell(self):
        for t, lang in (("Experts argue that the method scales.", "en"), ("Experten sind sich einig, dass es skaliert.", "de")):
            self.assertTrue(any("vague attribution" in w for w in warned(t, lang)), t)

    def test_given_plain_copula_and_named_source_when_checked_then_no_tell(self):
        t = "The library is a bridge between teams. The ETH study measured a 20 percent cost increase."
        self.assertFalse(any(w.startswith("ai-tell") for w in warned(t)))


# Synthetic sentences. Positives tell the reader how to operate the page itself;
# negatives describe product UI behavior or instruct inside the product, which
# technical docs do legitimately.
UI_INSTRUCTIONS = [
    ("Auf dem Handy lässt sich das Diagramm seitlich wischen.", "de"),
    ("Die Tabelle lässt sich auf kleinen Bildschirmen waagerecht scrollen.", "de"),
    ("Zum Vergrößern auf das Bild tippen.", "de"),
    ("Klicken Sie hier, um den Bericht zu öffnen.", "de"),
    ("Scrollen Sie nach unten für die Details.", "de"),
    ("Weitere Zahlen siehe unten.", "de"),
    ("Fahren Sie mit der Maus über einen Balken, um den Wert zu sehen.", "de"),
    ("Auf dem Smartphone kann man die Grafik seitlich wischen.", "de"),
    ("On a phone, swipe the diagram sideways.", "en"),
    ("Scroll horizontally to see the whole table.", "en"),
    ("Tap to zoom.", "en"),
    ("Click here for the full report.", "en"),
    ("Hover over a bar to see its value.", "en"),
    ("Scroll down to the results.", "en"),
    ("See below for the numbers.", "en"),
    ("Click on the image to enlarge it.", "en"),
]
UI_DESCRIPTIONS = [
    ("Der Nutzer klickt auf Freigeben, dann startet der Export.", "de"),
    ("Die Liste scrollt automatisch zum neuen Eintrag.", "de"),
    ("Klicken Sie auf Speichern, um den Entwurf zu sichern.", "de"),
    ("Bei Klick auf Exportieren erzeugt das System ein PDF.", "de"),
    ("Das Diagramm zeigt den Ablauf von links nach rechts.", "de"),
    ("Die App erkennt Wischgesten und Zoomen mit zwei Fingern.", "de"),
    ("Der Speicher lässt sich später vergrößern.", "de"),
    ("Der Bericht lässt sich als PDF exportieren.", "de"),
    ("The user clicks Approve and the export starts.", "en"),
    ("The list scrolls to the newest item.", "en"),
    ("Click Approve to publish the release.", "en"),
    ("Users swipe left to archive a message.", "en"),
    ("Hover states use the accent color.", "en"),
    ("Tap targets are at least 44 px.", "en"),
    ("Scrolling performance improved after the fix.", "en"),
    ("The carousel lets shoppers swipe through products.", "en"),
    ("See the runbook for the restore steps.", "en"),
    ('Link text names its target, never "click here".', "en"),
    ('Ein Link sagt nie "hier klicken", sondern nennt sein Ziel.', "de"),
]


class UiInstructionTest(unittest.TestCase):
    def test_given_instruction_how_to_operate_the_page_when_checked_then_ai_tell(self):
        for t, lang in UI_INSTRUCTIONS:
            self.assertTrue(any("UI operating instruction" in w for w in warned(t, lang)), t)

    def test_given_product_ui_described_or_instructed_when_checked_then_no_ui_tell(self):
        for t, lang in UI_DESCRIPTIONS:
            self.assertFalse(any("UI operating instruction" in w for w in warned(t, lang)), t)


class AcronymTest(unittest.TestCase):
    def test_given_unexplained_acronym_when_checked_then_warning_once(self):
        ws = [w for w in warned("RLS guards every table. RLS also covers views.") if w.startswith("acronym:")]
        self.assertEqual(len(ws), 1)

    def test_given_expanded_acronym_when_checked_then_no_warning(self):
        for t in ("Row-Level Security (RLS) guards every table.", "RLS (Row-Level Security) guards every table."):
            self.assertFalse(any(w.startswith("acronym:") for w in warned(t)), t)

    def test_given_known_terms_entry_when_checked_then_no_warning(self):
        facts = {"known_terms": ["RLS"]}
        self.assertFalse(any(w.startswith("acronym:") for w in warned("RLS guards every table.", facts=facts)))

    def test_given_terms_key_when_checked_then_no_warning(self):
        facts = {"terms": {"RLS": ["Zeilenrechte"]}}
        self.assertFalse(any(w.startswith("acronym:") for w in warned("RLS guards every table.", facts=facts)))

    def test_given_common_acronyms_when_checked_then_no_warning(self):
        t = "OK, the EU and US teams send a PDF with the URL of the API."
        self.assertFalse(any(w.startswith("acronym:") for w in warned(t)))


# One text per rule id, each producing that finding and keeping the message
# prefix existing readers match on.
RULE_FIXTURES = {
    "ai-tell.not-x-but-y": ("prose", "It is not a tool, but a habit."),
    "ai-tell.justifying-filler": ("prose", "Die Seite ist bewusst schlank gehalten."),
    "ai-tell.filler-phrase": ("prose", "Hier kommt der Cache ins Spiel."),
    "ai-tell.inflated-role": ("prose", "The cache plays a pivotal role here."),
    "ai-tell.stock-word": ("prose", "We delve into the logs."),
    "ai-tell.staged-opener": ("prose", "Here's the thing about logs."),
    "ai-tell.vague-value": ("prose", "The export adds real value."),
    "ai-tell.chat-residue": ("prose", "The export is ready. I hope this helps."),
    "ai-tell.copula-avoidance": ("prose", "The table serves as the index."),
    "ai-tell.vague-attribution": ("prose", "Experts agree the export is ready."),
    "ai-tell.ui-instruction": ("prose", "Scroll down to see the chart."),
    "readability.long-sentence": ("prose", " ".join(["word"] * 35) + "."),
    "readability.mean-sentence-length": ("prose", " ".join(["word"] * 28) + "."),
    "list.enumeration": ("prose", "We test exports, imports, reports and audits."),
    "list.semicolons": ("prose", "We test exports; then imports; then reports."),
    "acronym.first-use": ("prose", "RLS guards every table."),
    "repetition.near-duplicate": ("prose", "The export job writes every audit record nightly to storage. "
                                           "The export job writes every audit record nightly to storage."),
    "figures.conflict": ("prose", "Match rate 37 % in March. Later the match rate 41 % again."),
    "term.avoided-variant": ("prose", "The ticket is open."),
    "claim.forbidden": ("prose", "The export is certified."),
    "claim.unsourced-percent": ("prose", "Usage rose 12 % this week."),
    "commit.generic-subject": ("commit", "fixes"),
    "commit.subject-length": ("commit", "Check audit permission before creating the export job now"),
    "commit.blank-line": ("commit", "Check audit permission\nReject early."),
    "artifact.missing-part": ("pull_request", "Adds the export."),
    "artifact.word-ceiling": ("slack", " ".join(["word"] * 201)),
    "artifact.bottom-line": ("executive_summary", "Some context first."),
    "artifact.percent-complete": ("agile_progress", "# Goal\nExport\nCurrent state: 80% complete\nNext: audit"),
}
FACTS = {"terms": {"work item": ["ticket"]}, "forbidden_claims": ["certified"], "facts": []}


class RuleIdTest(unittest.TestCase):
    def test_given_each_fixture_when_checked_then_its_rule_id_is_reported(self):
        for rule, (artifact, text) in RULE_FIXTURES.items():
            with self.subTest(rule=rule):
                self.assertIn(rule, check(text, artifact, "en", FACTS)["rules"])

    def test_given_clean_text_when_checked_then_no_rule_ids(self):
        self.assertEqual(check("The export runs at night.", "prose", "en")["rules"], [])

    def test_given_vocabulary_when_read_then_every_gate_rule_it_names_is_known(self):
        import re
        from quality_gate import RULE_IDS
        known = {rule for rule, _ in RULE_IDS} | {"diagnostics.lix"}
        text = (Path(__file__).resolve().parents[1] / "references" / "vocabulary.md").read_text(encoding="utf-8")
        named = {rule for row in text.splitlines() if row.startswith("| ") and row.rstrip().endswith("|")
                 for rule in re.findall(r"`([a-z][\w-]*\.[\w.-]+)`", row.split("|")[-2]) if "exact" in row.split("|")[-2]}
        self.assertTrue(named)
        self.assertFalse(named - known, named - known)


if __name__ == "__main__":
    unittest.main()
