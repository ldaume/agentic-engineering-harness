---
name: progressive-product-agile
description: Use whenever writing or revising a product status report or update, an adaptive Now/Next/Later or FaST-compatible roadmap, a progress update, a problem brief, bet brief, experiment card, product decision record, or outcome review (Statusbericht, Roadmap, Fortschritt, Problem Brief). Carries the outcome, evidence, uncertainty, risk, and learning structure instead of ticket activity, velocity, or ceremony. Not for deciding what to build; that is a product decision, not a document.
license: MIT
---

# Progressive Product & Agile Writing

Make the actual state of a product visible: software development is product
and system evolution under uncertainty, so the text reports changed reality
and learning, not motion. This skill writes the document; deciding what is
worth building belongs to `product-craft` when installed.

## Stance

Prefer outcome over output, evidence over backlog weight, flow over
utilization, learning over false certainty, explicit investment boundaries,
shared ownership, visible risk, built-in quality. Do not introduce Scrum,
SAFe, story points, velocity, fixed teams, or ceremonies as a default, because
they answer a process question the reader did not ask.

## Problem before solution

Keep distinct: signal, problem, opportunity, candidate bet, focus, delivery,
adoption and outcome, learning. Do not collapse them into "feature", because
a roadmap of features hides which problem each one is a bet on.

## FaST

FaST-compatible artifacts show collective product direction and visible work.
Never imply that FaST assigns fixed teams or requires team-specific long-term
feature roadmaps.

## Route

- status report: `references/status.md`
- FaST planning: `references/fast.md`
- adaptive roadmap: `references/roadmaps.md`
- progress update: `references/progress.md`
- problem brief, bet brief, experiment card, decision record, outcome review:
  `references/product-docs.md`

## Gate

From this skill's directory, run
`python3 ../progressive-writing-core/scripts/quality_gate.py --artifact <type>
--lang <de|en> FILE` with type one of `agile_status|fast_roadmap|agile_progress|product_document`.
If the file is missing (this skill was installed alone), check the
artifact's checklist in its reference by hand. Fix every error; judge each
warning, because warnings are heuristics, not rules.

## Done when

A reader can name the desired outcome, the current state, the evidence, the
uncertainty or risk, the decision or investment boundary, and the next
learning or delivery step.
