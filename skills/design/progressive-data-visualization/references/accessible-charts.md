# Accessible charts

## Intent

Every reader gets the chart's message and its data: through sight, a screen
reader, a keyboard, zoom, or print. The chart is one way in; the text and
the table are two more, and they carry the same information.

## Trigger

Any chart that ships on the web, in a document, or in a report; any
accessibility review of a chart or dashboard.

## Desired outcome

- A short text alternative that names the chart and its message.
- A long description with scales, values, relationships, and trend.
- A data table or download with the same numbers.
- Visual encodings that survive color blindness, grayscale print, and
  forced colors.
- Keyboard and screen-reader access for interactive charts.

## Workflow

1. **Short alternative.** Name the chart type and subject (verified)
   [SRC-VIZ-011], and add the message in one clause, so a reader who stops
   there gets what a sighted reader gets at a glance (hypothesis). Information carried by color must appear in the text too;
   leaving it out is WCAG failure F13 (verified) [SRC-VIZ-007].
2. **Long description, visible to everyone.** Scales, ranges, the key values,
   the relationship or trend, and notable exceptions. Put it in the page,
   for example in the figure caption or below the chart, because hidden-only
   descriptions help few and are discouraged (verified) [SRC-VIZ-011]
   (supported) [SRC-VIZ-013]. Summarize the key point in the surrounding
   text as well (verified) [SRC-VIZ-011].
3. **Data table.** Ship a captioned table with the chart's data, in the same
   `figure` as the chart, or a download (supported) [SRC-VIZ-006]. Prefer
   `figure` and `figcaption` over `aria-describedby` for anything with
   structure, because `aria-describedby` flattens headings and tables into
   one string (verified) [SRC-VIZ-011]. Tiny slices or marks a library does
   not render are reachable only through the table (supported)
   [SRC-VIZ-014].
4. **Second cue beside color.** Direct labels first, then shape, pattern,
   dash style, or marker; a 3:1 lightness difference also counts as a second
   cue (verified) [SRC-VIZ-007]. Test in grayscale.
5. **Non-text contrast.** Lines, bar edges, slice boundaries, markers, and
   focus indicators needed to read the chart reach 3:1 against adjacent
   colors; text in the chart reaches 4.5:1 (verified) [SRC-VIZ-008]. If every
   value is also shown as a text label, the graphical objects are not
   required for understanding and the 3:1 rule relaxes for them (verified)
   [SRC-VIZ-008].
6. **Keyboard and screen reader for interactive charts.** Tooltips, filters,
   and drill-down work with the keyboard; focus moves through series and
   points in a predictable order; each point announces its series, category,
   and value. Use a library that provides this - without an accessibility
   module, Highcharts exposes the chart as an image labeled by its title
   (supported) [SRC-VIZ-013] - and verify it rather than trusting the
   feature list.
7. **Motion.** A chart transition triggered by interaction can be turned
   off: under `prefers-reduced-motion`, jump to the end state (verified,
   AAA) [SRC-VIZ-010]. Auto-playing animation over 5 seconds needs pause,
   stop, or hide (verified, level A) [SRC-VIZ-009]. Timings come from
   `progressive-design-core/references/motion.md`.
8. **Audit.** Run the Chartability critical heuristics - a quick pass
   covers visual, keyboard, screen reader, cognitive, and context - and
   count an inconclusive result as a failure (supported) [SRC-VIZ-012].
   Chartability complements a WCAG 2.2 AA check of the page
   [SRC-A11Y-001]; it does not replace it.

## Patterns

- **Static chart in a report or page**: `figure` > chart image or SVG with
  short alt > `figcaption` with title, long description, source > table
  (or a disclosure that reveals it). The source and title stay real text,
  not part of the image, so they can be read, translated, and searched
  (hypothesis).
- **Inline SVG chart**: `role="img"` with an accessible name on the SVG, the
  long description and table as page content; mark decorative gridlines
  hidden from assistive technology (hypothesis for the exact markup; verify
  with a screen reader).
- **Interactive chart**: library accessibility module on; visible data table
  toggle; keyboard focus order across series; announced values
  (supported) [SRC-VIZ-013].
- **Dashboard tile**: tile title states the status in words; the number and
  its comparison are text; the sparkline is decorative unless described.
- **Chart in a PDF or slide**: alt text on the image, the message in the
  headline or caption, the table in an appendix or handout.

## Quality gates

- Automated: contrast of series and marks (3:1) and chart text (4.5:1), and
  an axe scan of the host page through `frontend-craft`'s test setup. axe
  cannot judge whether a description is correct or useful.
- Manual: the short alternative states the message; the long description
  and table match the chart; grayscale test; keyboard-only pass; one screen
  reader pass (VoiceOver or NVDA); 200% zoom without lost labels; Chartability
  critical heuristics.

## Anti-patterns

- Chart as an image with no text alternative or table (supported)
  [SRC-VIZ-006].
- Alt text that names no chart and no subject, such as "Chart" (verified)
  [SRC-VIZ-011].
- Legend colors as the only way to tell series apart (verified)
  [SRC-VIZ-007].
- Hidden-only description as the sole description (supported)
  [SRC-VIZ-013].
- Tooltip-only values that need a mouse (hypothesis).

## Example

Line chart of open support tickets per week for three teams.

- Alt EN: "Line chart: open tickets per week for teams A, B, and C, weeks
  30-42. Teams A and B are below target since week 38; team C stays above."
- Alt DE: "Liniendiagramm: offene Tickets pro Woche für die Teams A, B und
  C, KW 30-42. Die Teams A und B liegen seit KW 38 unter dem Ziel, Team C
  bleibt darüber."
- Long description: the target value, each team's start and end value, the
  week each crossed the target, and the exception.
- Table: weeks as rows, teams as columns, target in its own column; caption
  "Open tickets per week by team" / "Offene Tickets pro Woche nach Team".
- Second cue: team C solid and in color, A and B dashed and grey, each line
  labeled at its end.

## Agent prompt

"For this chart, write the short alt (type, subject, message), the long
description (scales, key values, trend, exceptions), and the data table.
Check that no information is carried by color alone and that marks meet 3:1.
List what still needs a keyboard and screen-reader pass."

## Evidence gaps

- chartability.fyi and chartability.com did not load; only the GitHub
  repository was read [SRC-VIZ-012].
- Carbon's data-visualization palette page was not read [SRC-VIZ-014].
- No source here tests screen-reader behavior of specific chart libraries
  beyond their own documentation.
