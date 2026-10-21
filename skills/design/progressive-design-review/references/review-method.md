# Review Method

## Dimensions

Task fit, journey continuity, information architecture, interaction logic,
feedback and recovery, accessibility, visual hierarchy, typography,
composition, responsiveness, content clarity, performance, consistency,
trust, product outcome. Score them with the profile in
`progressive-design-core/references/quality-model.md`.

## Finding format

```text
Finding ID: R-012
Location: /settings/billing, "Cancel plan" dialog, 360 px
Observed issue: Focus starts on "Cancel plan", the destructive button.
User impact: A keyboard user pressing Enter to dismiss cancels the subscription.
Evidence: APG says focusing the least destructive action may be advisable before an irreversible step (supported) [SRC-A11Y-021]; Radix AlertDialog focuses Cancel by default [SRC-PROD-025]; reproduced with keyboard in Chromium.
Classification: likely usability problem
Confidence: high (reproduced)
Severity: 3 of 4
Recommended change: Initial focus on "Keep plan"; name the consequence in the dialog text.
Trade-offs: One extra key press for people who do want to cancel.
How to validate: Keyboard walkthrough; Playwright test asserting initial focus.
```

## Classification

| Class | Meaning |
|---|---|
| Verified defect | Reproduced; behaves contrary to spec or intent |
| Accessibility violation | Fails a named WCAG 2.2 success criterion |
| Likely usability problem | Strong evidence or reproduction, not yet tested with users |
| Inconsistency | Same thing done two ways without a reason |
| Craft opportunity | Works, could be clearer or better made |
| Untested hypothesis | Plausible; needs a test before investment |

## Severity

| Level | Meaning |
|---|---|
| 4 | Blocks the task or excludes a group of people |
| 3 | Causes errors or data loss risk, or costs most people significant time |
| 2 | Slows people or causes confusion they recover from |
| 1 | Polish |

## Prioritization

Rank by severity times frequency on the critical journey, raise
accessibility violations of level A, and weigh effort, uncertainty, and
learning value. A cheap change with high learning value can go before a
larger certain one.

## Backlog

```text
Change | Findings | Expected effect | Validation | Effort | Owner
```

## Reviewing other artifacts

Use the owner's checklist: forms (`progressive-forms-interactions`), flows
(`progressive-user-flows` and its lint), product screens
(`progressive-product-interfaces`), websites (`progressive-web-experiences`),
dashboards (`progressive-data-visualization`), decks and diagrams
(`progressive-slides-diagrams`), tokens and components
(`progressive-design-systems`).

## Anti-patterns

Verdicts without observation ("looks dated"); counting heuristics instead of
impact; treating a clean axe run as accessible; findings without a way to
validate the fix.
