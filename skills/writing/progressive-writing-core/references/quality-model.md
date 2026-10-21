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

## Gates per artifact

| Artifact | Hard gate | Diagnostic only |
|---|---|---|
| Commit | subject and structure | no readability limit |
| PR | claims and sections | sentence length |
| Slack | length and next step | sentence length |
| Business email | subject and ask | Flesch, LIX |
| Hero | word count and claim support | no Flesch limit |
| Landing | claim support | Flesch, LIX per section |
| Docs | structure and links | readability, terminology |
| Executive | bottom line | LIX, Flesch, sentence length |
| Product docs | evidence and unknowns | readability secondary |

`scripts/quality_gate.py --artifact <type>` implements the deterministic part.
Known types: business_email, marketing_email, slack, hero, landing_page,
website_content, confluence, agile_status, fast_roadmap, agile_progress,
product_document, po_summary, executive_summary, pull_request, commit.
