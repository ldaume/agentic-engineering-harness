---
name: progressive-design-review
description: Use whenever auditing, critiquing, or verifying an existing interface, website, user flow, form, dashboard, slide deck, or diagram - UX audit, accessibility audit, heuristic review, design critique, visual QA, browser verification with Playwright and axe, and turning findings into a prioritized improvement backlog (UX-Audit, Design-Review, Barrierefreiheit prüfen, Usability-Review). Every finding names an observation, impact, evidence, and how to validate it. Not for reviewing code correctness, which code review owns. Fixing what it finds belongs to frontend-craft.
license: MIT
---

# Progressive Design Review

Find what stops people from reaching their goal, show the evidence, and turn
it into changes ranked by impact. "The design feels dated" helps nobody; "the
primary action sits below the fold at 360 px, so mobile visitors miss it" can
be fixed and checked.

## Golden path

1. Name the person, the task, and the journey under review; a review without
   a task becomes a taste contest.
2. Walk the task end to end in the real product, desktop and mobile, with
   keyboard only, and with a screen reader for critical paths.
3. Run the automated gate (`references/browser-verification.md`): axe WCAG
   2.2 A/AA, overflow at key widths, console errors, screenshots per state.
   Automation finds candidates, not conformance: axe states it finds about
   57% of WCAG issues (verified) [SRC-TOOL-001].
4. Check the artifact-specific list from its owner skill (forms, flows,
   product UI, web, dashboards, slides and diagrams, design system).
5. Write each finding in the format of `references/review-method.md`, with a
   classification and confidence.
6. Prioritize by user impact, frequency, severity, journey criticality,
   accessibility risk, effort, uncertainty, and learning value.
7. Hand over a backlog: smallest valuable change first, each with its
   validation.

## Rules that change the result

- Separate what was observed from what is inferred; a likely problem is
  labeled as such until a test or data confirms it.
- An accessibility violation cites the WCAG 2.2 success criterion
  (verified) [SRC-A11Y-001]; WCAG 3 is a working draft and is not a
  conformance basis (verified) [SRC-A11Y-002].
- Aesthetic findings state the observation, the effect on the person, and an
  alternative; otherwise they are dropped.
- A green automated run never closes the review; the manual list in
  `references/browser-verification.md` stays open until someone checks it.

## Load when

- `references/review-method.md` - always: dimensions, finding format,
  classification, severity, prioritization, backlog.
- `references/browser-verification.md` - whenever the product can be opened
  in a browser.

## Done when

Every finding has location, observation, impact, evidence, confidence,
severity, recommendation, and validation; the automated gate ran or its
absence is stated; the manual checks are done or assigned.
