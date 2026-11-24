# Browser Verification

A successful build is not evidence of a good experience. Open the real
product and check it.

## Gate stack (verified 2026-11-24)

| Package | Version | License | Role |
|---|---|---|---|
| `@playwright/test` | 1.65.1 | Apache-2.0 | Browser runner, viewports, screenshots [SRC-TOOL-003] |
| `@axe-core/playwright` | 4.14.0 | MPL-2.0 | WCAG A/AA scan inside Playwright [SRC-TOOL-002] |
| `lighthouse` | 13.6.0 | Apache-2.0 | Optional lab performance smoke [SRC-TOOL-004] |

Versions checked against npm on 2026-11-24 (axe 4.14.0 is still the latest).
Playwright 1.65 no longer tests on Node.js 20 (use 22, 24 or 26; npm engines
still say `>=20`), and text the browser does not render, such as text inside a
closed `<details>`, is no longer part of accessible names and aria snapshots:
re-check `getByRole` names and `toMatchAriaSnapshot` assertions that rely on
it (release notes read 2026-11-24). Lighthouse 13.6.0 needs Node `>=22.19`.
The catalog CI runs Node 24.

```bash
npm install -D --save-exact @playwright/test@1.65.1 @axe-core/playwright@4.14.0
npx playwright install --with-deps chromium
npx playwright test
```

The worked pattern is `design-forms/tests/registration.spec.mjs`:
behavior tests per state, keyboard-only completion, overflow at 360, 768,
and 1280 px, and axe with tags `wcag2a`, `wcag2aa`, `wcag21aa`, `wcag22aa` in
every meaningful state, not only the initial render. Scan settled states:
wait until `document.getAnimations()` has nothing running, because a scan
during a fade measures the half-transparent text as a contrast failure (this
failed in CI on a 160 ms fade that a faster machine never caught).

## Reading pages

axe's A/AA tags do not check AAA contrast, line height (1.4.8) or the 44 px
target (2.5.5), and none of them measure line length. For a long-form
documentation or reading page run `scripts/reading-audit.js`: one dependency-free
function that returns JSON per check. The caller sets the color scheme and
viewport; run it for light and dark, and at 390 px for overflow.

```js
const fn = fs.readFileSync("skills/design/design-review/scripts/reading-audit.js", "utf8");
for (const colorScheme of ["light", "dark"]) {
  await page.emulateMedia({ colorScheme });
  const r = await page.evaluate(`(${fn})({ level: "aa" })`);   // or "aaa"
}
```

In a browser console paste `(` + the file + `)({ level: "aa" })`. The default
level is `aa`: contrast 4.5:1 (3:1 for large text, 24 px or 18.66 px bold),
targets 24 px outside inline text, no overflow. Text size 16 px, line height
1.5 on p/li/dd/td and 45 to 75 characters per line come back as `notes`.
Level `aaa` makes text size and line height failures, raises contrast to 7:1
(4.5:1 large) and targets to 44 px, and fails a line above 80 characters, the
limit of 1.4.8; a line of 76 to 80 characters is a note, "above the 45-75
reading target". A target is the largest box among an input and its labels, so
a visually hidden radio inside a 44 px label (a segmented control) is the
label's size. Line height 1.5 is 1.4.8, a different criterion from 1.4.12,
which is about surviving user overrides. Diagram sources (`.mermaid`), script
and style are skipped; background images are not composited. Worked tests:
`tests/reading-audit.spec.mjs` with `tests/playwright.config.mjs` (`npx playwright test -c skills/design/design-review/tests`).

## Card rows

`scripts/design-loop.mjs` also runs `layout.alignment` (`alignmentAudit`) in the
audit tier at every viewport: for 3 or more same-width siblings in one visual
row, each with 2 or more block children, the same child (title, text, divider,
footnote) must sit within 4 px of its twin, or share a bottom edge. A wrapped
row is compared per visual row; cards built differently are skipped. The usual
fix is CSS subgrid (`grid-row: span N; grid-template-rows: subgrid`). The Jev tier asks the same
question of the screenshots as `tell.misaligned-cards`, for pages with no DOM
to measure; the DOM rule stays the exact check. Worked
fixtures: `tests/fixtures/align-drift.html` (fails), `align-subgrid.html`,
`align-equal.html` and `align-wrapped.html` (pass); `align-nav-drift.html` (linked cards
in a list, a bordered footer pushed down with `margin-top: auto`, fails) and
`align-nav-subgrid.html` (pass). A wrapper with one child is looked through, and a
divider is judged by its own top: equal bottoms do not excuse it.

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
  `incomplete` results need a person (verified) [SRC-TOOL-001]. The 57% is
  Deque's own study from March 2021 (about 13,000 pages, counted by issue
  volume, not by WCAG criterion), a vendor figure; independent estimates are
  reported lower (hypothesis, not confirmed in this run). Treat it as an upper
  orientation, not a coverage promise.
- Meaningful alt text, link purpose, reading and focus order, real screen
  reader announcements, cognitive load, plain language, message helpfulness,
  motion comfort, touch use in real hands, visual hierarchy.
- Performance in the field: lab runs use one synthetic device; Core Web
  Vitals pass or fail on field data (supported) [SRC-TOOL-004]
  [SRC-WEB-012].
- A visual baseline proves "unchanged", never "correct".

## Without a browser

State it in the review, run the static checks that remain (HTML semantics,
contrast with `design-systems/scripts/contrast.py`, flow lint),
and list the browser checks as open.
