---
name: writing-core
description: Use whenever asked to rewrite, edit, tighten, proofread, or translate a German or English text, or when it sounds generated or like AI slop (umschreiben, redigieren, kürzen, übersetzen, natives Deutsch), including the words on slides, pages, and docs. Loads house style and claim checks. Email, marketing, product docs, PRs, and commits go to their writing-* skill. Not for code.
license: MIT
---

# Writing Core

Write for reader change, not for text production: a text is good when it asks
the least cognitive work of its reader without losing meaning, uncertainty, or
precision.

## Route first

When the artifact has an owner, load it now, in this turn, before the first
sentence, because each owner carries the golden path for that format and this
core alone stays generic. Being named alone ("use writing-core") is the same
request: route by the artifact, then follow both.

| Artifact | Load |
|---|---|
| email, Slack, decision request, follow-up, PO or executive summary | `writing-editorial` |
| hero, landing or web page, marketing email, campaign copy | `writing-marketing` |
| status update, roadmap, FaST, progress report, product brief | `writing-product` |
| PR description, commit message, Confluence or technical doc | `writing-engineering` |
| a text that carries percentages, counts, or metrics | `plain-numbers` as well |
| a rewrite, translation, or review with no owner above | this core alone |

## Frame before drafting

Reconstruct from the repository, ticket, diff, conversation, or documents:
artifact, language, primary audience and what it already knows, intent, the
reader's desired change (decide, understand, act), facts and evidence, real
unknowns, tone, channel, and the terms this audience uses daily, English or German
(their emails, tickets, wiki, code, the standard they work by; not instinct),
because a term the writer translates is one the reader must translate back. Every term, acronym or internal name this audience may not know is
explained at first use or kept in a glossary, because the writer's own
vocabulary is invisible to the writer. Ask only when a missing answer would change the
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
   numbers, links), then the AI-tell pass (`references/ai-tells.md`). Separate
   passes, because one combined pass fixes commas and misses a wrong order,
   and a line edit tightens a tell instead of removing it.
   `references/vocabulary.md` lists the field's terms for authors and check
   scripts; a review does not load it.
5. Verify: classify each claim as sourced fact, inference, recommendation, or
   unknown. Re-check time-sensitive or externally published facts at the
   source. For AI-assisted text, fact-check body and metadata by hand
   (`references/verification.md`).
6. Gate: from this skill's directory run `python3 scripts/quality_gate.py --artifact <type> --lang <de|en> FILE`
   with `--artifact slides` for deck text and `--artifact prose` for any other
   running text when no closer type is listed, and `--facts` holding the
   audience `terms`; fix every error, judge each warning. A page's diagram
   captions and legends count as prose; a sentence telling readers how to
   operate the page (swipe, scroll, click here) is a warning: fix the design.
   For client-facing or public text add `--jev --audience "<who reads it>"`:
   an advisory tier asks TypeSafe Jev typed questions per section (UI
   instruction, three AI tells, contradiction, universal claim, target as
   built, provoking content). A `jev:` warning means reread that section; it
   never fails the gate, and "Jev tier skipped: <reason>" means no key or no
   answer (`references/quality-model.md`).
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

- `references/ai-tells.md`: the patterns that make text read as generated,
  the AI-tell pass, and the audience-term rule. Load for every draft.
- `references/editorial-model.md`: the FRAME to SHIP loop, edit passes, the
  universal golden paths per artifact family.
- `references/agent-readers.md`: writing for agents (AGENTS.md, Skill
  descriptions, subagent briefs, prompts). Load when the reader is a model.
- `references/de-style.md`, `references/en-style.md`: house style per language.
- `references/verification.md`: claim classes, fact checks, test fixtures.
- `references/quality-model.md`: 0 to 4 rubric, gate thresholds, readability
  formulas, per-artifact gates and the reference-page profile. Both scripts
  read HTML (`.html` or `--html`, `--lang-class`, `--sections`);
  `--lang-class auto` checks both languages and their twin parity in one run.

## Done when

The reader finds the point quickly, the required action or meaning is
unambiguous, no unsupported fact was added, the language reads native, the
structure fits artifact and audience, and remaining uncertainty is stated.

## Maintaining these skills

Golden outputs in the domain references double as fixtures: each sits after a
`<!-- golden: <artifact> <de|en> -->` marker, and `tests/run_evals.py golden`
gates all of them. `tests/test_quality_gate.py`, `tests/test_jev_tier.py` (Jev stubbed) and `tests/test_evals.py` run
in CI. `tests/run_evals.py routing --host claude|codex` replays
`tests/routing-cases.json` in fresh headless sessions to show which skill a
host actually loads; run it after changing any description.

`references/sources.json` is the evidence registry for all five writing
skills (71 sources checked on 2026-10-21 and 2026-11-24, each with access date, findings,
limits, evidence level, and a revisit trigger); rules cite it as
`[SRC-WRITE-NNN]`, and the catalog's `scripts/check-knowledge.py` fails on a
citation without an entry.
