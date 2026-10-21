# Chart choice

## Intent

Pick the table or chart that answers the reader's decision question with the
least effort and the least room for misreading, then check it for the axis,
encoding, and color failures that make a correct number look wrong.

## Trigger

Choosing a chart for a report, page, dashboard tile, or slide; reviewing an
existing chart; replacing a pie, gauge, donut, 3D, or dual-axis chart.

## Required context

- The decision question in the reader's words and the one-sentence message.
- The data shape: categories or time, how many series, units, value range,
  whether zero is meaningful, missing periods, uncertainty available.
- The reader: lookup or gist, expert or mixed, screen or print, time to read.

## Decision tree

Start from the question, not from the data or a chart gallery, because the
same table answers several questions and each wants a different form
(supported) [SRC-VIZ-006] [SRC-VIZ-001]. The Financial Times Visual
Vocabulary is a useful index of forms by relationship; it is all rights
reserved, so cite and link it, never copy its poster or layout
[SRC-VIZ-001].

**0. Table or chart?**
- The reader looks up exact values, compares across mixed units, or needs a
  few numbers precisely -> table: right-aligned numbers, consistent decimals,
  units in the header. A well-structured table can communicate as well as a
  chart (supported) [SRC-VIZ-006].
- The reader needs a pattern, a trend, an outlier, or a gap -> chart, and
  ship the table as its accessible alternative anyway.

**1. Magnitude - "How big is A compared with B?"**
Bars on a zero baseline, horizontal when labels are long. Many close values
-> dot plot on a shared axis, which keeps position and drops the zero
requirement (hypothesis; position encodes the value, by analogy to
[SRC-VIZ-021]). Against a target or
average -> bars or dots with a labeled reference line (supported)
[SRC-VIZ-006].

**2. Ranking - "Which is first, which last?"**
Bars or a dot plot (supported) [SRC-VIZ-006], sorted by the value the
question names, not alphabetically, because the reader reads order from
position (hypothesis). Rank change between two dates -> slope chart (hypothesis).

**3. Change over time - "How has it changed?"**
Line chart; highlight the series that carries the message and grey the rest;
label line ends directly (supported) [SRC-VIZ-006]. Many series or a
comparison across groups -> small multiples on a shared scale, which beat
animated playback for analysis (verified, single study) [SRC-VIZ-003].
Few discrete periods -> columns are acceptable.

**4. Part-to-whole - "How is the total divided?"**
One stacked or 100% bar with about four segments at most; a pie only for
five or fewer categories with one dominant share; no donut (supported)
[SRC-VIZ-006] [SRC-VIZ-005]. Composition over time -> stacked area or
stacked columns, with the important segment on the baseline because only the
baseline segment can be compared by position (hypothesis).

**5. Distribution - "How are values spread?"**
Histogram, box plot, or dot/strip plot; show the individual points when n is
small, because a summary hides clusters and outliers (hypothesis).

**6. Relation - "Do A and B move together?"**
Scatter plot (supported) [SRC-VIZ-005]; add a fitted line only when the
audience reads one, otherwise state the relation in a sentence, and say that
correlation is not cause where a reader could act on it (hypothesis).

**7. Flow - "Where does it go, through which stages?"**
Funnel or stacked bar for a linear sequence; Sankey or labeled flow diagram
for branching flows; every arrow labeled, as the C4 checklist asks of
diagrams (supported, applied by analogy) [SRC-VIZ-031]. A user
journey flowchart is a design artifact, not data - `progressive-user-flows`.

**8. Geography - "Where?"**
A map only when spatial position matters to the decision; otherwise a ranked
bar of regions, because the area of a region on a map shows land size, not
the value (hypothesis).

**9. Uncertainty - "How sure is this, what is the range?"**
Show it in a form people can count or read off: quantile dot plot or CDF for
a decision under risk; interval bars with the stated level for experts. Text
alone and bounded shapes such as cones are misread - a cone reads as growth
(supported) [SRC-VIZ-018] [SRC-VIZ-019]. The evidence base is thin and
mostly measures accuracy rather than decision quality (supported)
[SRC-VIZ-017].

**If the main comparison needs precision**, use the highest encoding
available: position on a common scale, then length, angle, area, color
intensity (supported) [SRC-VIZ-015].

## Misleading axes

- Bar and column axes start at zero, because the bar length is the value
  (supported) [SRC-VIZ-006] [SRC-VIZ-021].
- A line may use a non-zero range - position, not length, encodes the value -
  when the range is marked and described. Keep zero when the data sit near
  zero or zero is the target, because truncation then exaggerates the change
  (supported) [SRC-VIZ-021].
- No dual-axis line charts; use two aligned panels with their own labeled
  scales (supported) [SRC-VIZ-006].
- Same scale across small multiples unless the panels say otherwise in their
  titles, because readers compare heights across panels (hypothesis).
- Time on the horizontal axis at even intervals; gaps in the data stay gaps,
  not a line bridging missing periods (hypothesis).

## Color

- Color is never the only cue: pair it with a direct label, shape, pattern,
  dash style, or position. A lightness difference of 3:1 also counts as a
  second cue (verified) [SRC-VIZ-007].
- Graphical objects needed to read the chart - lines, bar edges, slice
  boundaries, markers - reach 3:1 against adjacent colors, unless the values
  are also shown as text (verified) [SRC-VIZ-008].
- Do not encode magnitude with hue; use position or length and keep color
  for highlighting one series (supported) [SRC-VIZ-005] [SRC-VIZ-006].
- Palette values, ordering, and dark mode belong to the `dataviz` skill or
  the design system.

## Anti-patterns

- Truncated bar axis; dual-axis line chart (supported) [SRC-VIZ-006].
- Pie with many similar slices, donut, radial gauge, 3D (supported)
  [SRC-VIZ-005].
- Legend far from the data when direct labels fit (supported) [SRC-VIZ-014].
- A topic as title ("Revenue") instead of the message (supported)
  [SRC-VIZ-006].
- Continuous animation as the way to find a trend (verified, single study)
  [SRC-VIZ-003].

## Example

Question: "Did the support backlog get back under target after the hiring
round?" Data: weekly open tickets, one target line, three teams.

- Form: line chart, one line per team in small multiples sharing one scale,
  target as a labeled reference line, the team that missed in color, the
  others grey.
- Title EN: "Two of three teams are back under the backlog target since
  week 38" / DE: "Zwei von drei Teams liegen seit KW 38 wieder unter dem
  Backlog-Ziel".
- Subtitle EN: "Open tickets per week, by team, weeks 30-42" / DE: "Offene
  Tickets pro Woche, nach Team, KW 30-42".
- Not chosen: a stacked area of all teams (hides each team against the
  target), a gauge per team (no trend).

## Agent prompt

"Before drawing: state the decision question and the message in one
sentence each. Choose table or chart from the decision tree in
chart-choice.md, name the alternative you rejected and why, check the axis
and color rules, then hand the spec to the `dataviz` skill or
`frontend-craft` for rendering."

## Evidence gaps

- The Cleveland and McGill and Heer and Bostock papers were read only through
  a course summary [SRC-VIZ-015].
- Datawrapper Academy chart-choice and bars-at-zero pages were unavailable;
  not cited.
- No controlled study ties chart-by-question selection to decision quality;
  the tree rests on practice guidance.
