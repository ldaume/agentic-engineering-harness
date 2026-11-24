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
audit tier over a width sweep (every 32 px from 360 to 1592 px, light, plus
the screenshot widths), because wrapping makes the drift width-dependent; `where` names
the failing bands, e.g. `1024-1072 px`. In each viewport: for 3 or more same-width siblings in one visual
row, each with 2 or more block children, the same child (title, text, divider,
footnote) must sit within 4 px of its twin, or share a bottom edge. A wrapped
row is compared per visual row; cards built differently are skipped. The usual
fix is CSS subgrid (`grid-row: span N; grid-template-rows: subgrid`). The Jev tier asks the same
question of the screenshots as `tell.misaligned-cards`, for pages with no DOM
to measure; the DOM rule stays the exact check. Worked
fixtures: `tests/fixtures/align-drift.html` (fails), `align-subgrid.html`,
`align-equal.html` and `align-wrapped.html` (pass); `align-nav-drift.html` (linked cards
in a list, a bordered footer pushed down with `margin-top: auto`, fails) and
`align-nav-subgrid.html` (pass); `align-band.html` (aligned at 1280 and 390 px, drifts in
a band between, found only by the sweep). A wrapper with one child is looked through, and a
divider is judged by its own top: equal bottoms do not excuse it.

## Type and layout craft

`scripts/design-loop.mjs` runs five more DOM rules in the audit tier, per screenshot
viewport and scheme (1280 and 390 px, light and dark), each reporting element, text,
observed, required, and where. They come from a spike on 8 app pages and 3 hand-written
clean references: a rule stayed only when at least 70 percent of its findings were real
and no clean reference was flagged. The measured text is every visible element with a text
node of its own.

| Rule | Fails when | Notes |
|---|---|---|
| `type.small-text` | rendered text is under 12 px | `display:none`, `visibility:hidden` and `aria-hidden` text, and a single character, are skipped |
| `type.scale-near-duplicate` | two adjacent font sizes (rounded to 0.5 px) are under 10 percent apart and each is used by 2 or more texts | reports the pair, both counts and an example of each; a size used once is a one-off, not a scale step |
| `type.widow` | the last line of a heading (`h1` to `h6`, `role=heading`) or of bold text (weight 600 or more) of 16 px or more is a single word | measured with Range rects over every word; runs in the width sweep (every 32 px from 360 to 1592 px) and names the failing bands; a heading of fewer than 3 words is skipped; text in `td`, `th`, `dt`, `dd`, `caption`, `figcaption`, `label`, `button` and `a` (unless a heading) and bold text in a box under 30ch of its own font are skipped; a last word that is a parenthetical or a capitalized abbreviation of up to 3 letters ("a)", "(1)", "Inc.") is skipped and the word before it judged; reported only when it occurs at 390 or 1280 px, with every band in `where` (a widow only between them is dropped). Fix: `text-wrap: balance` or `pretty` |
| `layout.edge-near-miss` | inside one landmark (`main`, `nav`, `aside`, `header`, `footer`, a `section` with a heading) text left edges are 1 to 6 px apart and each edge is shared by 2 or more texts | centered and right-aligned text, inline elements, and text in buttons, tabs, table cells and labels are skipped |
| `type.families` | more than 3 font families are rendered | the first face of each computed `font-family` |

The Jev tier adds one visual craft question, `tell.sparse`: "Is the page noticeably
sparse: large empty areas with little content?" It is a second Jev call of its own, with
only that question, the whitespace rules, one labeled NO and one labeled YES example
(`assets/examples/sparse-no.png`, `sparse-yes.png`, synthetic) and the three page shots cut
24 px below the last content, because a short page that ends early is normal. It is not in the
shared screenshot call: in a spike, rules plus labeled examples in the request pulled every
other score down (the hierarchy scores fell and 21 of 22 pages were flagged), and the shared
rules are calibrated without that context. The shared call stays byte for byte what it was in
1.6.0, with uncut shots; cutting them moved no answer by more than 0.11 on 5 pages (2 of 65
verdicts went from unsure to pass), which is still more than the shared rules were calibrated
for. The sparse call costs about $0.0004 per page, a little more than the shared call.
`tell.sparse` detects sparse only and never reports a cramped page: the spike's whitespace
answer separated sparse pages from the rest but not cramped ones. Thresholds (fail from 0.75,
pass up to 0.5, between goes to the model) come from 11 real pages, twice each, in the isolated
call: 0.77 to 0.87 on two real sparse pages, 0.6 on a third, 0.58 on a noisy one, at most 0.49 on
every page that is not sparse. That is a small sample tuned on its own pages, so treat a pass
as weak evidence.

Measured and dropped, so nobody re-adds them blindly: line length (14 of 14 findings were
narrow cards or phone width, 0 percent real), line height (34 hits on ordinary Tailwind
sizes, then no signal), a spacing grid (2, 6 and 10 px are half steps, not errors), the
count of distinct left edges (kanban columns and chat), the count of font weights, and
the Jev questions on hierarchy contrast (apps and references scored alike), focal point (40
percent real, references flagged) and grouping by proximity (0 of 3 real), and the kicker or
eyebrow rule (a small uppercase or tracked label, or a pill, above a heading): the DOM cannot
tell a functional chip (a status, a category, a step count) from a decorative eyebrow, so any
threshold either flagged real product labels or missed the decorative ones.
Worked fixtures, each rule with a failing and a passing page: `tests/fixtures/type-small-bad.html`
and `type-small-ok.html`, `type-scale-bad.html` and `type-scale-ok.html`, `type-widow-bad.html`
and `type-widow-ok.html`, `layout-edge-bad.html` and `layout-edge-ok.html`, `type-families-bad.html`
and `type-families-ok.html`; `type-widow-band.html` has a lone last word only at 1100 px and is not
reported; `type-widow-cells-ok.html`, `type-widow-labels-ok.html`, `type-widow-narrow-ok.html`
and `type-widow-paren-ok.html` pass; `type-widow-phone-bad.html` and `type-widow-narrow-bad.html` fail.

## Measured DOM rules

`measuredAudit` in `scripts/design-loop.mjs` adds seven rules that are exact colour and box
arithmetic, with the element in the finding. Ideas for them came from impeccable (Apache-2.0);
the code, thresholds and fixtures are our own. A rule was ported only when its findings were
all real and it flagged nothing on 2 real clean pages, the legit fixtures, 3 clean references and
12 live product-UI runs, and every synthetic positive was caught. Those samples are small and the
thresholds were tuned on them.

| Rule | Tier | Fails when | Exempt |
|---|---|---|---|
| `tell.glow` | dom, blocking | a coloured (chroma 0.25 or more, alpha 0.2 or more) `box-shadow` with blur 24 px or more and blur plus twice the spread, times alpha, at least 12, on a box of 48 px or more with an offset under 0.75 times the blur; a radial-gradient halo of 200 px or more that fades to transparent on a decorative layer; a `blur()` of 40 px or more on a coloured box of 200 px or more | inset shadows, small indicators (under 48 px), focus rings (no blur), neutral shadows |
| `tell.gray-on-color` | dom, blocking | text of chroma 0.08 or less and lightness 0.3 to 0.75 on a background of saturation 0.4 or more and lightness 0.08 to 0.8 | pale tints (lightness 0.8 or more), near-black, neutral gray backgrounds, images behind the text. It complements the WCAG contrast audit: gray text can pass the ratio and still look dull on colour |
| `tell.icon-tile` | dom, advisory | 2 or more identical tinted (chroma 0.05 or more) near-square tiles of 32 to 128 px, with an icon, rounded, directly above a heading | a single tile, neutral tiles |
| `tell.nested-cards` | dom, advisory | an opaque card (rounded 6 px or more, 120 x 56 px or more, bordered on all sides or shadowed) inside another card whose left padding is 20 px or more | a flat tinted note, a tight outer card, table and list parts |
| `render.hidden-at-rest` | audit, blocking | text of 3 or more characters in the layout with opacity under 0.02, `visibility: hidden`, or fully off-screen horizontally; run first, before any scrolling | `checkVisibility()` false, `hidden`, `aria-hidden`, collapsed `details`, tooltips, skip links, fixed ancestors, scroll containers |
| `render.broken-image` | audit, blocking | an `img` that finished loading with `naturalWidth` 0 and a `src` or `srcset` | an `img` without a source, images still loading |
| `render.text-occluded` | audit, blocking | an opaque box (alpha 0.95 or more, or an `img`, `video` or `canvas`) is on top of 2 of 5 sample points of a text, found with `elementFromPoint` after scrolling the text to mid screen; run last because it scrolls, and restores the position | a fixed or sticky coverer or ancestor, a coverer that contains the text or repeats it, translucent overlays |

`tell.icon-tile` and `tell.nested-cards` are advisory: they appear in the report with status
`advisory` and never set the exit code, because their thresholds rest on synthetic fixtures with
narrow margins (no real page was flagged and no real page confirmed them). Pinned chrome
covering text, such as a sticky header over a heading, is not caught by `render.text-occluded`,
because the exemption that keeps real fixed bars quiet also hides that defect. A page that
reveals content on scroll and keeps it hidden at rest is reported by `render.hidden-at-rest`;
a page that needs a click or a hover to show text is not a defect and is not reported when it
uses `hidden`, `aria-hidden`, `details` or a tooltip role.
Fixtures, all synthetic, each rule with a failing and a passing page: `tests/fixtures/tell-glow-bad.html`, `tests/fixtures/tell-glow-ok.html`, `tests/fixtures/tell-gray-on-color-bad.html`, `tests/fixtures/tell-gray-on-color-ok.html`, `tests/fixtures/tell-icon-tile-bad.html`, `tests/fixtures/tell-icon-tile-ok.html`, `tests/fixtures/tell-nested-cards-bad.html`, `tests/fixtures/tell-nested-cards-ok.html`, `tests/fixtures/render-hidden-bad.html`, `tests/fixtures/render-hidden-ok.html`, `tests/fixtures/render-broken-image-bad.html`, `tests/fixtures/render-broken-image-ok.html`, `tests/fixtures/render-occluded-bad.html`, `tests/fixtures/render-occluded-ok.html`.

## Vocabulary rules

Ten exact checks name the rule ids of `design-core` `references/vocabulary.md` (a term's Check cell
names its rule). They run in the audit tier of `scripts/design-loop.mjs`, each reporting element, text,
observed, required and where. Measured on 3 hand-written clean references, 6 real pages, 4 live product
pages, 21 synthetic fixtures (a failing and a passing page per rule) and the real pages again with a defect
injected (a heading ladder, tight spacing above headings, proportional figures, no outline, a fixed banner
over the page). A rule stayed when at least 70 percent of its findings were real, no clean page was flagged
for a reason that is not a true defect, every synthetic positive was caught, and it took at most two
threshold iterations. Only two rules found a real defect; the other eight found none on those pages,
caught every synthetic and injected defect, and so are `advisory` (reported, never failing the run)
until a real page confirms them, as `tell.icon-tile` was.

| Rule | Status | Fails when | Exempt |
|---|---|---|---|
| `type.heading-ladder` | advisory | the median size of a lower heading level is more than 5 percent larger than a higher level, or equal in size and at least 200 weight units heavier | a level that appears once is still compared; headings that are not visible |
| `layout.proximity` | advisory | a stacked heading has less than 0.75 times as much space above it as below it, measured from the ink of the neighbors (text and painted boxes, not their padding) | first and last children, side-by-side layouts, absolutely positioned neighbors, a one-line text smaller than the heading above it (a label or kicker; a one-line paragraph above a tight heading is missed) |
| `type.tabular-figures` | advisory | in a table column with 2 or more numeric cells the rendered widths of the digits 1, 0 and 8 differ by more than 0.5 px | a font whose digits are equal by default or through `font-variant-numeric: tabular-nums`; measured one digit at a time without kerning, because kerned repeated digits look proportional in fonts that are not |
| `wcag.non-text-contrast` | fail | an enabled text input, textarea, select or textbox has its border, fill and shadow all under 3:1 against the color behind it (the wrapper's border counts) | checkboxes, radios, buttons, disabled fields, an image behind the field. Chart lines are not checked: no chart in the sample produced a hit |
| `wcag.text-spacing` | advisory | with line height 1.5, letter spacing 0.12em, word spacing 0.16em and 2em paragraph spacing injected, HTML text is newly clipped by `overflow: hidden` or spills below the bottom of its painted box, or a horizontal scroll appears; the override is removed again | svg text, text in a box that already clips or scrolls (`line-clamp`, `truncate`, `overflow: auto`), `text-overflow: ellipsis`, anything that was already clipped before |
| `wcag.reflow` | fail | the page scrolls horizontally at 320 px wide; the widest element outside a scrolling or clipping box is named | a table or code block in its own `overflow-x: auto` box |
| `motion.reduced` | advisory | with `prefers-reduced-motion: reduce` emulated, a running animation of transform, translate, rotate, scale, position, margin or a scroll timeline, or `scroll-behavior: smooth`, remains | opacity and color animations; hidden targets |
| `perf.layout-shift` | advisory | Cumulative Layout Shift (the largest session window, shifts after input excluded) is above 0.1 over the load and one and a half seconds more | run before any resize or scroll; a page loaded by `setContent` counts its shifts as input, so test pages load by URL |
| `wcag.focus-visible` | advisory | tabbing (up to 40 stops) shows no change of outline, box shadow, border, background, color, underline, transform or filter on the focused element, its parent, its parent's children or its grandparent | a wrapper that draws the ring counts; focused boxes under 2 px |
| `wcag.focus-not-obscured` | advisory | all sample points of the visible part of the focused element lie under a fixed or sticky layer that does not contain it | a layer around the element; partly covered elements |

`wcag.reflow` and `wcag.non-text-contrast` are the two that found real defects: a horizontal scroll of
a few pixels at 320 px in two product pages and one static page, and text inputs with a 1.5:1 to 1.8:1
border in a product screen and in a hand-written reference. The reference is clean for every older rule and
fails WCAG 1.4.11, so the new rule stays and the reference is not clean for it.

Measured and dropped: none of the ten. Dropped part: the chart-line half of `wcag.non-text-contrast`
(strokes of 2 px or more against the chart background), because no sample held a chart line to test, so its
precision is unknown. Not measured: the ten other exact vocabulary terms (space scale, signifier, empty state,
error identification, status message, accessible name, resize text, pause stop hide, design token,
proportional ink) still name no rule id.

Fixtures, all synthetic, each rule with a failing and a passing page, plus the kicker and wrapper exemptions: `tests/fixtures/focus-obscured-bad.html`, `tests/fixtures/focus-obscured-ok.html`, `tests/fixtures/focus-visible-bad.html`, `tests/fixtures/focus-visible-ok.html`, `tests/fixtures/focus-visible-wrapper-ok.html`, `tests/fixtures/layout-proximity-bad.html`, `tests/fixtures/layout-proximity-kicker-ok.html`, `tests/fixtures/layout-proximity-ok.html`, `tests/fixtures/motion-reduced-bad.html`, `tests/fixtures/motion-reduced-ok.html`, `tests/fixtures/non-text-contrast-bad.html`, `tests/fixtures/non-text-contrast-ok.html`, `tests/fixtures/perf-shift-bad.html`, `tests/fixtures/perf-shift-ok.html`, `tests/fixtures/type-ladder-bad.html`, `tests/fixtures/type-ladder-ok.html`, `tests/fixtures/type-tabular-bad.html`, `tests/fixtures/type-tabular-ok.html`, `tests/fixtures/wcag-reflow-bad.html`, `tests/fixtures/wcag-reflow-ok.html`, `tests/fixtures/wcag-spacing-bad.html`, `tests/fixtures/wcag-spacing-ok.html`.

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
