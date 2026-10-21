# Browser Verification

A successful build is not evidence of a good experience. Open the real
product and check it.

## Gate stack (verified 2026-10-21)

| Package | Version | License | Role |
|---|---|---|---|
| `@playwright/test` | 1.64.1 | Apache-2.0 | Browser runner, viewports, screenshots [SRC-TOOL-003] |
| `@axe-core/playwright` | 4.14.0 | MPL-2.0 | WCAG A/AA scan inside Playwright [SRC-TOOL-002] |
| `lighthouse` | 13.5.0 | Apache-2.0 | Optional lab performance smoke [SRC-TOOL-004] |

```bash
npm install -D --save-exact @playwright/test@1.64.1 @axe-core/playwright@4.14.0
npx playwright install --with-deps chromium
npx playwright test
```

The worked pattern is `progressive-forms-interactions/tests/registration.spec.mjs`:
behavior tests per state, keyboard-only completion, overflow at 360, 768,
and 1280 px, and axe with tags `wcag2a`, `wcag2aa`, `wcag21aa`, `wcag22aa` in
every meaningful state, not only the initial render. Scan settled states:
wait until `document.getAnimations()` has nothing running, because a scan
during a fade measures the half-transparent text as a contrast failure (this
failed in CI on a 160 ms fade that a faster machine never caught).

## Checklist

- Desktop and mobile widths; the breakpoints the layout actually uses.
- Each state: loading, empty, error, success, no permission, offline.
- Keyboard: every action reachable, order logical, focus visible and never
  hidden by sticky UI (2.4.11).
- Error messages and recovery for each failure the flow spec lists.
- Console: no errors or failed requests during the task.
- Screenshots per state for the review record.
- Visual regression baselines only on the CI operating system, because fonts
  and rendering differ across systems (supported) [SRC-TOOL-003].

## What automation cannot prove

- WCAG conformance: axe states it finds about 57% of issues on average;
  `incomplete` results need a person (verified) [SRC-TOOL-001].
- Meaningful alt text, link purpose, reading and focus order, real screen
  reader announcements, cognitive load, plain language, message helpfulness,
  motion comfort, touch use in real hands, visual hierarchy.
- Performance in the field: lab runs use one synthetic device; Core Web
  Vitals pass or fail on field data (supported) [SRC-TOOL-004]
  [SRC-WEB-012].
- A visual baseline proves "unchanged", never "correct".

## Without a browser

State it in the review, run the static checks that remain (HTML semantics,
contrast with `progressive-design-systems/scripts/contrast.py`, flow lint),
and list the browser checks as open.
