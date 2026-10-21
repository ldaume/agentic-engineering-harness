---
name: progressive-editorial
description: Use whenever drafting or revising an email, a Slack message, a decision request, a follow-up, or a summary for a PO, manager, C-level, or customer, in German or English (Mail schreiben, Slack-Nachricht, Zusammenfassung, Executive Summary, Management-Update). Use it even for a two-line mail or ping; it carries the point-context-ask structure, tone rules, and golden examples. Not for marketing copy, product status or roadmaps, PRs, or commits.
license: MIT
---

# Progressive Editorial

Move a relationship or a decision forward with the least reading effort. Not
for marketing campaigns or web copy (`progressive-marketing-ux`), product
status or roadmaps (`progressive-product-agile`), or PRs and commits
(`progressive-engineering`), because those formats have different jobs.

## Shared contract

Apply `progressive-writing-core` when it is installed; in short: purpose before
prose, one primary reader change, direct and specific language, no defensive
explanation, no invented facts, idiomatic target language (US English by
default, native German, never translated).

## Route

- Email (personal, business, request, follow-up, decline, escalation):
  read `references/emails.md`.
- Slack: read `references/slack.md`.
- PO, management, C-level, or customer summary: read `references/summaries.md`.

## Communication model

Default order: observation, meaning, implication, recommendation, next step.
For sensitive messages keep observation and inference visibly apart, because
a reader who feels judged stops reading the facts.

## Compression

Cut a detail only when it does not change decision, risk, timing, cost,
ownership, customer impact, reversibility, or uncertainty. Executive writing
is decision compression, not just a shorter technical text.

## Gate

From this skill's directory, run
`python3 ../progressive-writing-core/scripts/quality_gate.py --artifact <type>
--lang <de|en> FILE` with type one of `business_email|slack|po_summary|executive_summary`.
If the file is missing (this skill was installed alone), check the
artifact's checklist in its reference by hand. Fix every error; judge each
warning, because warnings are heuristics, not rules.

## Done when

The reader knows what matters and what happens next, who does it, and by
when, without reconstructing it from background.
