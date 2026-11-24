---
name: design-core
description: Use whenever a UI or UX task has no clearer owner, or spans several surfaces - framing a design problem, choosing between design options, writing a design decision record, defining motion or animation, scoring design quality, or refreshing UI/UX evidence (Designentscheidung, UX-Konzept, Motion, Animation). Routes flows, forms, product UI, websites, dashboards, slides and diagrams, design systems, research, and reviews to their design-* owner. Not for writing code; frontend-craft builds the screen.
license: MIT
---

# Design Core

Turn a design request into a decision about a person's outcome, backed by
evidence the reader can check. Start from who is trying to do what, in which
context, what friction exists today, and how you will know a change worked,
because a screen designed from "make it nicer" optimizes the wrong thing.

## Route first

Load the owner of the artifact, because each carries its own golden path and
the core alone stays generic. One primary owner per task; add a second only
when the task really has two deliverables.

| Task | Owner | Often with |
|---|---|---|
| discovery, interviews, usability tests, synthesis | `design-research` | - |
| a user flow, journey, states, edge cases | `design-flows` | `design-product-ui` |
| a form, validation, errors, submit, destructive actions | `design-forms` | `design-review` |
| SaaS or app screens, navigation, settings, AI-native UI | `design-product-ui` | `design-forms` |
| website, landing page, marketing or editorial site | `design-web` | `writing-marketing` for copy |
| dashboard, chart, table, metric view | `design-dataviz` | `plain-numbers` for figures |
| slides, deck, diagram, architecture or system map | `design-slides` | `writing-core` for the words |
| tokens, components, theming, component specs | `design-systems` | - |
| audit or critique of an existing UI, flow, deck | `design-review` | the artifact's owner |

Implementing the result is `frontend-craft`'s job; this family decides what to
build and how to verify it. Words on the screen, slide, or page belong to
the `writing-*` skills when installed: load `writing-core` with the design
skill whenever the artifact carries text a person reads, because the design
pass checks layout and the writing pass is what catches generated-sounding
text and translated terms.

## Intake

Infer from the repository, ticket, screenshots, and conversation first; ask
only when a missing answer would change the design, because a questionnaire
delays work the context could answer. Record an assumption instead and mark
it. See `references/intake-and-modes.md` for the context checklist and the
six modes (explore, design, build, review, improve, research refresh).

## Evidence discipline

Every material recommendation carries one level, because a reader must tell a
standard from a taste: `verified` (a standard or test you can check),
`supported` (several credible signals), `context-dependent` (helps here,
harms there), `hypothesis` (untested), `aesthetic` (a deliberate choice with
no claim of superiority). Cite the registry, `references/sources.json`, as
`[SRC-...]`. Never invent research results, user quotes, metrics, awards, or
test outcomes; write "not measured" instead. An award is a jury's subjective
score, usability included, not tested usability [SRC-WEB-024].

## Owner stance

Deliberate positions of the repository owner, set 2026-11-24. They choose
between options that evidence leaves open; they never override a test, a
standard, or a user's task. Each line carries its level.

- **Unique, not typical** (aesthetic; the detail failures of AI output, such
  as weak hierarchy, grouping, contrast, and spacing, are supported
  [SRC-WEB-031]). Aim for distinctive, award-level work that fits a world
  where agents are in daily use. Before any styling of a visual artifact,
  write the concept in one sentence and three to five constraints; a reviewer
  must be able to name what only this product could look like. Run the tells
  in `references/generic-tells.md` as a review gate.
- **Give people time instead of taking it** (supported for batching
  [SRC-PROD-033]; calm technology is a convention [SRC-PROD-034]). Attention
  is a budget. Classify every signal: act now (interrupt), act today
  (digest), FYI (in the product, no push). Quiet by default, one channel per
  urgency, controllable by the person. Push never hides state: status stays
  inspectable on demand.
- **Decide the default, then allow depth** (supported [SRC-PROD-032]). When
  the options are known, choose the default and record why; configurability
  is not a substitute for a decision, because most people never change it.
- **Support instead of silently disabling.** An action that cannot run yet
  stays reachable and says what is missing (owner position; mechanisms in
  `design-forms`).
- **Motion guides focus** (aesthetic; the job rules in `references/motion.md`
  are supported). Supportive motion is always considered and never decoration
  where everything moves. Its goal is to steer focus cleanly: show where
  something came from or went, what changed, what to look at next, and where
  focus now is.

## Quality model

Judge ten dimensions separately and show the profile, not one total, because
an average hides the one dimension that sinks the release: utility,
usability, clarity, accessibility, interaction quality, visual craft,
performance, trust, journey continuity, outcome. Scale and gate rules:
`references/quality-model.md`.

## Motion

Motion must do a job - feedback, orientation, continuity, attention - or it
goes, a missing transition where context changes is a defect too, and every
motion has a reduced-motion variant, because vestibular triggers and
distraction are real costs [SRC-WEB-002] [SRC-WEB-006]. Durations, easing,
focus, and per-surface rules: `references/motion.md`.

## Decisions

Write a design decision record for any choice a future reader would
question; template in `references/decision-records.md`.

## Done when

The owner skill's gates pass, the tells list has been run on any visual
artifact, each material recommendation has an evidence
level and source or is marked hypothesis, accessibility is checked against
WCAG 2.2 AA [SRC-A11Y-001], and what automation could not prove is listed for
manual review.

Baseline: WCAG 2.2 AA, the W3C Recommendation [SRC-A11Y-001]. AAA is not a
site-wide policy (WCAG 2.2 conformance note), though cheap AAA criteria are
welcome. WCAG 3 is a draft [SRC-A11Y-002] and APCA is not part of WCAG 2.2;
neither is a conformance basis. Regulators lag: EN 301 549 v4.1.1 moves the EU
web baseline to 2.2 [SRC-A11Y-026]; the US ADA Title II rule still cites 2.1
AA [SRC-A11Y-027].

## Maintaining the knowledge base

`references/sources.json` is the registry for every `design-*`
skill: id, URL, access date, findings, limits, evidence level, revisit
trigger. `references/research-refresh.md` is the update procedure. The
catalog's `scripts/check-knowledge.py` fails when a citation has no registry
entry. `tests/routing-cases.json` holds the activation cases, and
`tests/test_routing_cases.py` checks that every skill has one.
