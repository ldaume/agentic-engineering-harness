---
name: progressive-design-core
description: Use whenever a UI or UX task has no clearer owner, or spans several surfaces - framing a design problem, choosing between design options, writing a design decision record, defining motion or animation, scoring design quality, or refreshing UI/UX evidence (Designentscheidung, UX-Konzept, Motion, Animation). Routes flows, forms, product UI, websites, dashboards, slides and diagrams, design systems, research, and reviews to their progressive-* owner. Not for writing code; frontend-craft builds the screen.
license: MIT
---

# Progressive Design Core

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
| discovery, interviews, usability tests, synthesis | `progressive-ux-research` | - |
| a user flow, journey, states, edge cases | `progressive-user-flows` | `progressive-product-interfaces` |
| a form, validation, errors, submit, destructive actions | `progressive-forms-interactions` | `progressive-design-review` |
| SaaS or app screens, navigation, settings, AI-native UI | `progressive-product-interfaces` | `progressive-forms-interactions` |
| website, landing page, marketing or editorial site | `progressive-web-experiences` | `progressive-marketing-ux` for copy |
| dashboard, chart, table, metric view | `progressive-data-visualization` | `plain-numbers` for figures |
| slides, deck, diagram, architecture or system map | `progressive-slides-diagrams` | - |
| tokens, components, theming, component specs | `progressive-design-systems` | - |
| audit or critique of an existing UI, flow, deck | `progressive-design-review` | the artifact's owner |

Implementing the result is `frontend-craft`'s job; this family decides what to
build and how to verify it. Words on the screen belong to the
`progressive-writing` skills when installed.

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

## Quality model

Judge ten dimensions separately and show the profile, not one total, because
an average hides the one dimension that sinks the release: utility,
usability, clarity, accessibility, interaction quality, visual craft,
performance, trust, journey continuity, outcome. Scale and gate rules:
`references/quality-model.md`.

## Motion

Motion must do a job - feedback, orientation, continuity, attention - or it
goes, and every motion has a reduced-motion variant, because vestibular
triggers and distraction are real costs [SRC-WEB-002] [SRC-WEB-006]. Durations, easing,
and per-surface rules: `references/motion.md`.

## Decisions

Write a design decision record for any choice a future reader would
question; template in `references/decision-records.md`.

## Done when

The owner skill's gates pass, each material recommendation has an evidence
level and source or is marked hypothesis, accessibility is checked against
WCAG 2.2 AA [SRC-A11Y-001], and what automation could not prove is listed for
manual review.

## Maintaining the knowledge base

`references/sources.json` is the registry for every `progressive-*` design
skill: id, URL, access date, findings, limits, evidence level, revisit
trigger. `references/research-refresh.md` is the update procedure. The
catalog's `scripts/check-knowledge.py` fails when a citation has no registry
entry. `tests/routing-cases.json` holds the activation cases, and
`tests/test_routing_cases.py` checks that every skill has one.
