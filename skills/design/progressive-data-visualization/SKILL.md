---
name: progressive-data-visualization
description: Use whenever deciding what a chart, graph, table, KPI view, or dashboard should show and why - picking the chart for a decision question, designing a decision, operations, or executive dashboard, fixing a misleading axis, showing uncertainty, or making a chart accessible with alt text and a data table (Diagramm, Dashboard, Kennzahlen, Datenvisualisierung, Grafik, Auswertung). Not for chart code, palettes, or rendering - the dataviz or frontend-craft skill draws it; not for slides or architecture diagrams, which progressive-slides-diagrams owns.
license: MIT
---

# Progressive Data Visualization

Decide what a chart, table, or dashboard shows, for which decision, and how
a reader can check it. This skill owns the choice and the reasoning. The
drawing - library, palette, marks, tooltips, rendering - belongs to the
host's `dataviz` skill when present, otherwise to `frontend-craft`, because
two owners of the same pixels give two answers. Figures and labels in prose
around the chart follow `plain-numbers` when installed. Evidence levels, the
quality model, and motion rules live in `progressive-design-core`; cite them,
do not restate them.

## Golden path

1. **Write the decision question and the message.** One question the reader
   must answer, one sentence they should take away. The question picks the
   chart; if the message does not fit in one or two sentences, simplify the
   analysis before charting (supported) [SRC-VIZ-006].
2. **Check the data before the design.** Source, period, freshness, gaps,
   definition changes, sample size. A clean chart of broken data misleads
   with authority, and the reader cannot see the break (hypothesis).
3. **Choose table or chart, then the form**, with
   `references/chart-choice.md`. Exact lookup or mixed units wants a table;
   a pattern wants a chart (supported) [SRC-VIZ-006].
4. **Encode the key comparison with position or length**, color only as a
   secondary cue, because elementary judgments of position are the most
   accurate and color intensity the least (supported) [SRC-VIZ-015]
   [SRC-VIZ-005].
5. **Title the message, label directly.** The title states the finding, the
   subtitle states subject, place, and period; labels sit on the data instead
   of a distant legend (supported) [SRC-VIZ-006] [SRC-VIZ-014].
6. **Add the context the number needs** - target, prior period, benchmark,
   uncertainty - because a lone number cannot say whether to act
   (context-dependent) [SRC-VIZ-016].
7. **Ship the text alternative with the chart**: short alt, long
   description, data table (verified) [SRC-VIZ-011]. Details in
   `references/accessible-charts.md`.
8. **Test with the task.** Ask someone from the audience to answer the
   decision question from the chart alone and note where they hesitate or
   misread; it is the most direct check that the chart does its job, applied
   from usability testing by analogy (context-dependent) [SRC-FLOW-023].

## Decision rules

- Bars start at zero, because length encodes the value; a line may use a
  narrower range when the break is marked and the data are not near zero or
  near a meaningful zero target (supported) [SRC-VIZ-006] [SRC-VIZ-021].
- Avoid dual-axis line charts; use two aligned panels, because the reader
  infers a relation from an arbitrary scale ratio (supported) [SRC-VIZ-006].
- Color is never the only cue for a series, state, or threshold; add a
  label, shape, pattern, or position (verified) [SRC-VIZ-007].
- Animated transitions between two views of the same data (sort, filter,
  chart type change) may help readers track objects when short and staged -
  rescale axes first, then move marks; the gain is not universal and error
  rises with object count (verified, for the tested tasks) [SRC-VIZ-002].
- For trend analysis, show small multiples or traces, not playback:
  animation was fastest for presentation but slowest and least accurate for
  analysis
  (verified, single study) [SRC-VIZ-003]. Timings and the reduced-motion
  variant (jump to the end state) come from
  `progressive-design-core/references/motion.md`.
- Show uncertainty the reader can count (quantile dots or CDFs as tested;
  intervals with a stated level by extension) rather than hiding it or writing it only in text
  (supported) [SRC-VIZ-018].

## Load when

- `references/chart-choice.md` - picking a chart or table for a question,
  reviewing a chart's axis, encoding, or color, or replacing a pie, gauge,
  or 3D chart.
- `references/dashboards.md` - any dashboard, KPI page, scorecard,
  monitoring or anomaly view, or executive overview.
- `references/accessible-charts.md` - any chart that ships on the web, in a
  document, or in a report someone may read with a screen reader, keyboard,
  or zoom; and every accessibility review of a chart.

Charts on a slide: pick the chart here, the slide structure in
`progressive-slides-diagrams`. An audit of an existing dashboard pairs with
`progressive-design-review`.

## Gates

- Automated: series, marks, and reference lines against their background at
  3:1 and chart text at 4.5:1 (verified) [SRC-VIZ-008], for example with
  `progressive-design-systems/scripts/contrast.py` when installed; an axe
  scan of the page the chart sits in, through `frontend-craft`'s test setup.
- Manual: the message matches the data; no truncated bar axis; the task test
  in step 8; a keyboard and screen-reader pass with the Chartability
  critical heuristics (supported) [SRC-VIZ-012]. Automation cannot judge
  whether a chart answers the question.

## Done when

The decision question and message are written; the chart or table answers
it for a reader from the audience; every axis, color, and threshold passes
the decision rules; the text alternative and data table ship with the chart;
each material choice carries an evidence level; and what was not tested is
listed for manual review.
