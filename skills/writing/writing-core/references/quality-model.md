# Quality Model

Four test layers: deterministic structure, linguistic diagnostics, semantic
rubric, and human or owner judgment for high-impact artifacts. Not every
quality dimension is deterministic; scripts check structure, the agent judges
meaning.

## Semantic rubric (0 to 4)

| Dimension | 0 | 2 | 4 |
|---|---|---|---|
| Truthfulness | invented or misleading | minor uncertainty | clean, facts marked |
| Purpose fit | misses the purpose | partial | fully serves it |
| Audience fit | wrong context | usable | precisely tailored |
| Information architecture | hard to reconstruct | understandable | immediate decision path |
| Specificity | generic | mixed | concrete, close to evidence |
| Native language | translated, unnatural | acceptable | idiomatic |
| Actionability | unclear | implicit | next step unambiguous |
| Compression | loses meaning or redundant | okay | maximally dense without loss |
| Voice | wrong | neutral | deliberately fitting |
| Artifact fit | wrong format | partial | artifact golden path |

Gate: no dimension below 2. Truthfulness must be 4 for externally published
factual copy. Average at least 3.2 for normal production, at least 3.6 for
public hero, landing, and executive material. These are local targets, not
validated benchmarks.

## Errors and warnings

Errors (fix before shipping): unsupported factual claim, required section
missing, claimed test not evidenced, wrong artifact owner.

Warnings (judge, do not obey blindly): long sentences, high LIX, low Flesch,
repeated terminology, passive-heavy passage, very long section. A correct term
or a necessary complex statement beats a better score.

## Readability formulas

Scores are sensors. `scripts/readability.py` implements them dependency-free
with vowel-group syllable heuristics.

- Flesch Reading Ease (EN): 206.835 - 1.015 x words/sentences - 84.6 x
  syllables/words.
- Flesch after Amstad (DE): 180 - words/sentences - 58.5 x syllables/words.
  Word length dominates it, so German compounds score as hard even when
  they are the clearest term; use it as a weak screen, never a gate
  (supported) [SRC-WRITE-032].
- Flesch-Kincaid Grade (EN): 0.39 x words/sentences + 11.8 x syllables/words
  - 15.59.
- LIX: words/sentences + 100 x long_words/words, long word = more than six
  letters.
- SMOG (EN): 1.043 x sqrt(polysyllables x 30 / sentences) + 3.1291.

The Hohenheim comprehensibility index (HIX) combines several formulas with
unpublished benchmark mappings. Never label a local composite "HIX"; call it
`hix_proxy` if one is ever added.

Rough orientation: Flesch DE above 60 or EN above 60 reads easily for a broad
audience; LIX below 40 is plain, above 50 is dense specialist prose.

## Reference-page profile (local targets)

For reader-facing reference pages and documentation, these are local working
values, not values from a standard (hypothesis) [SRC-WRITE-037]. ISO 24495-1
gives principles (relevant, findable, understandable, usable) and asks to test
with readers; it sets no word counts or formulas. The one published number
close to them is GOV.UK's "Try to split up sentences that are over 25 words
long" (verified) [SRC-WRITE-042]. They are sensors that find passages to
reread, not pass marks; a correct term or a necessary complex statement beats
a better score. For legal communication ISO 24495-2:2025 builds on part 1
(supported) [SRC-WRITE-039]. A mean-sentence limit can reward choppy text and a formula
penalizes lists and necessary terms: judge, do not chase the number.

- German: mean sentence length at most 15 words, no sentence over 25. LIX at
  most about 45, Flesch after Amstad at least about 50.
- English: mean sentence length at most 20, no sentence over 30 (the maximum
  is a local working value); Flesch Reading Ease at least about 50.
- The gate applies the language's own limits and warns, never fails.
- One statement per sentence; a paragraph of at most 3 to 4 sentences.
- Three or more parallel, independent items (options, steps, requirements,
  findings) become a list. Causes, trade-offs and arguments stay in sentences,
  one claim per sentence. No bold label in front of each bullet unless readers
  look items up by that label. No chains of commas or semicolons (the gate
  warns on a chain of four or more short items and on two or more semicolons).
- A heading or subhead at least every 150 to 300 words.
- Report the values per section before and after the edit:
  `python3 scripts/readability.py --lang de --lang-class l-de --sections PAGE.html`.
- The real test is a reader-based check, because the sensors cannot see
  meaning (supported) [SRC-WRITE-043]: a fresh reader who restates the point,
  a highlighter test (readers mark what they do not understand), or a short
  comprehension task with 5 people from the target group.

Bilingual pages: `--lang` defaults to the suffix of `--lang-class` (`l-de` is
German), and an explicit `--lang` wins. `--lang-class auto` (both scripts)
measures every language class found in one report, each with its own formulas
and limits. It also warns when an element has no adjacent twin in the other
language, and when twins differ in word count by more than about 2x.

HTML input counts prose in p, li and dd only. Table cells, script, style and
diagram source (class contains `mermaid`) are skipped; each block ends a
sentence, so nested list items stay separate.

## Gates per artifact

What `scripts/quality_gate.py` decides (errors) and flags (warnings); the
agent check column stays with the semantic review, because a script cannot
judge it.

| Artifact | Script errors | Script warnings | Agent check |
|---|---|---|---|
| Commit | empty or generic subject, over 72 chars, no blank line before body | subject over 50 chars | one coherent change, reason when not obvious |
| PR | no why or context heading, no validation heading | - | claimed tests have evidence |
| Slack | - | email salutation, over 200 words, long sentences | next step and owner |
| Business email | - | no subject line, over 180 words, long sentences | one clear ask |
| Marketing email | no subject or preview, preview repeats subject | over 400 words | one CTA, specific value |
| Hero | no H1, H1 over 12 words | - | every claim supported |
| Landing, website | - | long sentences | claim support, message match |
| Confluence | no purpose, no owner or status | long sentences | current truth first |
| Status | a missing signal, outcome, learning, risk, or next label | velocity or story points | outcome, not activity |
| Roadmap | no strategic intent, outcome, now, confidence, investment boundary | - | later is not a commitment |
| Progress | no goal, current state, next; percent complete | - | uncertainty change |
| Product docs | no problem, evidence, unknowns | - | smallest artifact |
| PO, executive summary | - | over 300 words, no bottom-line label in 40 words, long sentences | decision relevance |
| Any artifact | a forbidden claim from `--facts`, a preferred-term variant | a percentage no fact contains, near-duplicate sentences, one label with two figures, an acronym without expansion, chat residue, copula avoidance, vague attribution | no invented fact, no restated or contradicted claim |

`scripts/quality_gate.py --artifact <type>` implements the deterministic part.
Known types: business_email, marketing_email, slack, hero, landing_page,
website_content, confluence, agile_status, fast_roadmap, agile_progress,
product_document, po_summary, executive_summary, pull_request, commit.
