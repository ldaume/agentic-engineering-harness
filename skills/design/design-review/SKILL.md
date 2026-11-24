---
name: design-review
description: Use whenever auditing or critiquing an existing interface, website, flow, form, dashboard, or deck - UX audit, accessibility audit, heuristic review, visual QA, Playwright and axe checks - into a prioritized backlog (UX-Audit, Design-Review, Barrierefreiheit prüfen). Not for code correctness, which code review owns; frontend-craft fixes the findings.
license: MIT
---

# Design Review

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

## Design loop after every UI change

`scripts/design-loop.mjs <url>` screenshots the page at 1280 and 390 px, light
and dark, then checks it cheapest first: generic-look tells from the DOM, the
reading audit, typed Jev questions on the screenshots, and a vision model
only for the rules Jev is unsure about. The page screenshots stop at 1568 px,
so each diagram (a large `svg`, `canvas`, `figure`, or `[role=img]`, up to 6)
gets its own shot with sticky layers hidden and clipping containers opened,
and is checked for clipped text, stacked labels, lines through boxes, and
small text: exactly from the SVG geometry where it is inline SVG, otherwise
by Jev and the model. On 7 synthetic diagrams Jev caught every clipped title,
stacked label, and small text and passed the clean one, but stayed unsure on
a line through an empty part of a box, which goes to the model. The visible
page text (headings, paragraphs, list items, captions, up to 80 blocks) is
checked for sentences that tell the reader how to operate the page ("swipe the
diagram sideways", "click here", "siehe unten"): exactly by pattern first,
otherwise by one typed Jev question on the text alone and the model when Jev
is unsure. On 16 synthetic pages Jev scored such sentences 0.73 to 0.97 and
product descriptions at most 0.44, except a how-to step inside a product
(up to 0.81), so a fail needs 0.85. It also measures type and layout craft from the DOM (text under 12 px, near-duplicate font
sizes, a lone last word in a heading or bold text, text edges a few pixels off one another, more
than 3 font families) and asks Jev whether the page is noticeably sparse; the rules, thresholds and
the ones that were measured and dropped are in `references/browser-verification.md`.
It writes `.design-loop/design-loop.json`
(findings with rule, tier, confidence, evidence, cost) and exits 1 on a
failure. Run it before calling any UI change done, because the agent that
built the page is the worst judge of how it looks; serve the page on
127.0.0.1. Keys and limits: the script header. Measured on 8 pages against a
vision-model reviewer with the same rules (thresholds tuned on those pages):
it found 21 of the 22 rule
failures the reviewer found at about 2% of its cost, and half the pages
needed no model beyond Jev.
Tests with model calls stubbed: `tests/design-loop.spec.mjs` with the
fixtures `tests/fixtures/generic.html`, `diagram-broken.html`, `text-instructions.html` and the
`type-*-bad.html` and `layout-edge-bad.html` files (must be flagged) and `clean.html` and `diagram-clean.html` (must pass).

## Load when

- `references/review-method.md` - always: dimensions, finding format,
  classification, severity, prioritization, backlog.
- `references/browser-verification.md` - whenever the product can be opened
  in a browser; its "Reading pages" section for long-form pages (contrast in
  light and dark, line height, line length, target size, overflow).

## Done when

Every finding has location, observation, impact, evidence, confidence,
severity, recommendation, and validation; the automated gate ran or its
absence is stated; the design loop ran on every changed page or screen; the
manual checks are done or assigned.
