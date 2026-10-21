---
name: progressive-writing-core
description: Use whenever asked to rewrite, edit, tighten, proofread, or translate a professional German or English text, or to make it sound natural or native (umschreiben, redigieren, kürzen, übersetzen, Text verbessern, natural US English, natives Deutsch), and for cross-format editorial, factual, or readability review. Loads the house style, DE/EN rules, and claim checks. Hand off email, Slack, summaries, marketing copy, product docs, PRs, and commits to the matching progressive-* skill. Not for code changes.
license: MIT
---

# Progressive Writing Core

Write for reader change, not for text production: a text is good when it asks
the least cognitive work of its reader without losing meaning, uncertainty, or
precision.

Hand off when the artifact has an owner, because each owner carries the golden
path for that format: email, Slack, PO and executive summaries to
`progressive-editorial`; marketing email, hero, landing and web pages to
`progressive-marketing-ux`; status, roadmaps, FaST, progress and product briefs
to `progressive-product-agile`; Confluence and technical docs, PRs and commits
to `progressive-engineering`.

## Frame before drafting

Reconstruct from the repository, ticket, diff, conversation, or documents:
artifact, language, primary audience and what it already knows, intent, the
reader's desired change (decide, understand, act), facts and evidence, real
unknowns, tone, channel. Ask only when a missing answer would change the
artifact, because most gaps are recoverable from context and a question costs
the user a round trip.

Never invent facts, customer evidence, metrics, decisions, test runs,
deadlines, quotes, or certainty. Mark a gap instead, because one fabricated
detail destroys the trust the rest of the text earned.

## Workflow

1. Frame (above).
2. Shape the information architecture before sentences, because order decides
   whether the reader finds the point.
3. Draft from meaning: specificity over polish, verbs over abstractions,
   evidence over adjectives, one idea per sentence.
4. Edit in separate passes: structure (matches the reader's decision path?),
   meaning (every claim precise, uncertainty honest?), line (shorter, more
   concrete), language-native, copy (terms, spelling, dates), proof (names,
   numbers, links). Separate passes, because one combined pass fixes commas
   and misses a wrong order.
5. Verify: classify each claim as sourced fact, inference, recommendation, or
   unknown. Re-check time-sensitive or externally published facts at the
   source. For AI-assisted text, fact-check body and metadata by hand
   (`references/verification.md`).
6. Gate: from this skill's directory run `python3 scripts/quality_gate.py --artifact <type> --lang <de|en> FILE`
   when the artifact type is listed there; fix every error, judge each warning.
7. Return the finished artifact, without commentary unless asked.

## Language

Translation is meaning-preserving rewriting, never sentence-by-sentence
substitution: rebuild meaning, relationship, intent, hierarchy, and action,
then write natively in the target language.

- English: idiomatic US English unless the project says otherwise; active
  voice where responsibility matters; contractions in conversational text.
- German: current official orthography; concrete verbs over Nominalstil; one
  consistent form of address (du, Sie, or neutral); main point early; no
  literal English idioms or pseudo-English marketing syntax.

Details: `references/de-style.md`, `references/en-style.md`.

## Editing priorities

Preserve in this order: truth, intended meaning, decision-relevant nuance,
information architecture, audience fit, voice, brevity. Never shorten by
deleting necessary uncertainty or evidence, because a short wrong text is
worse than a long right one.

Readability scores are sensors, not objectives: a low Flesch or high LIX
triggers a second look, never a rewrite that loses a needed term.

## References

Load only what the task needs:

- `references/editorial-model.md`: the FRAME to SHIP loop, edit passes, the
  universal golden paths per artifact family.
- `references/de-style.md`, `references/en-style.md`: house style per language.
- `references/verification.md`: claim classes, fact checks, test fixtures.
- `references/quality-model.md`: 0 to 4 rubric, gate thresholds, readability
  formulas and per-artifact gates.

## Done when

The reader finds the point quickly, the required action or meaning is
unambiguous, no unsupported fact was added, the language reads native, the
structure fits artifact and audience, and remaining uncertainty is stated.

## Maintaining these skills

Golden outputs in the domain references double as fixtures: each sits after a
`<!-- golden: <artifact> <de|en> -->` marker, and `tests/run_evals.py golden`
gates all of them. `tests/test_quality_gate.py` and `tests/test_evals.py` run
in CI. `tests/run_evals.py routing --host claude|codex` replays
`tests/routing-cases.json` in fresh headless sessions to show which skill a
host actually loads; run it after changing any description.

`references/sources.json` is the evidence registry for all five writing
skills (36 sources opened on 2026-10-21, each with access date, findings,
limits, evidence level, and a revisit trigger); rules cite it as
`[SRC-WRITE-NNN]`, and the catalog's `scripts/check-knowledge.py` fails on a
citation without an entry.
