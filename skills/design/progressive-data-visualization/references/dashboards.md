# Dashboards

## Intent

Design a dashboard as an instrument for named decisions: who looks, how
often, what they decide, and what they do next. A dashboard that reports
everything the warehouse holds supports no decision and trains people to
stop looking.

## Trigger

A new dashboard, KPI page, scorecard, monitoring or anomaly view, executive
overview, or a request to "add a chart" to an existing one.

## Required context

- Two or three decisions the dashboard serves and the role that makes each.
- Cadence: glanced continuously, checked daily, reviewed weekly or monthly.
- The data contract per metric: definition, source, refresh interval, known
  gaps, owner.
- What happens after a signal: who acts, where, with which tool.

## Decision tree

- Act within seconds or minutes on a live signal -> operations or anomaly
  dashboard (below).
- Review a period and decide on priorities or money -> executive dashboard
  (below).
- Explore open questions with filters and pivots -> an analytical workbench;
  the one-screen rule does not hold there, so design it as a product screen
  with `progressive-product-interfaces` (context-dependent) [SRC-VIZ-005].
- Several of these at once -> split into separate views per decision; a
  shared page for all three serves none, because density and cadence differ
  (hypothesis).

## Workflow - the golden path

1. **Decision questions.** Write each as the question the role asks ("Do we
   need to add on-call capacity this week?"), because a metric without a
   question has no threshold and no layout priority. Use task analysis to
   find them, not a list of available metrics (supported) [SRC-FLOW-022].
2. **Data quality first.** For each metric record definition, source,
   freshness, and gaps, and show freshness on the dashboard ("as of",
   "data delayed"). A stale number shown as live is worse than no number
   (hypothesis).
3. **Audience.** Name the reader's numeracy and domain knowledge; experts
   read intervals and distributions, mixed audiences need the message in
   words next to the chart, because poor cognitive fit raises errors and
   time (supported) [SRC-VIZ-019].
4. **Comparisons.** Every headline number gets the comparison that tells the
   reader whether to act: target, prior period, same period last year, peer
   group. A lone number is the classic missing-context failure
   (context-dependent) [SRC-VIZ-016].
5. **Encoding.** Choose each tile with `chart-choice.md`: position and length
   for comparisons, lines for trends, bullet charts instead of radial
   gauges, no 3D, no color for magnitude (supported) [SRC-VIZ-005].
6. **Hierarchy and density.** The tiles for the most frequent decision sit
   top left in reading order; group related tiles with proximity and
   borders first, color second (supported) [SRC-VIZ-005] [SRC-VIZ-029].
   A monitoring or decision dashboard fits one screen (supported)
   [SRC-VIZ-005]; NN/g argues this for quick action, while Few lists
   exceeding one screen as a pitfall from 2006-era BI practice
   (context-dependent) [SRC-VIZ-016] - keep the rule for glance views, drop it
   for workbenches. Show the precision the decision needs, not the precision
   the database has (context-dependent) [SRC-VIZ-016].
7. **Drill-down.** Summary first, detail on demand: each tile links to the
   view that explains it, filtered to the same scope and period, because the
   reader's next question is "why?" (supported) [SRC-PROD-006]. Keep the
   filter state visible and shareable in the URL (hypothesis).
8. **Uncertainty and gaps.** Show intervals or ranges where the metric is an
   estimate or a forecast (supported) [SRC-VIZ-018]; show missing data as a
   visible gap with a reason, never as zero (hypothesis). Loading uses a
   spinner per tile, because a dashboard card is one module (context-dependent)
   [SRC-PROD-007], and a skeleton only for the whole first page load; an empty tile says why and what to do
   (context-dependent) [SRC-PROD-013] [SRC-PROD-012]. Screen states are
   implemented per `frontend-craft`.
9. **Accessible alternatives.** Every tile has a text summary of its state
   and a data table or export; status is never color alone. Details in
   `accessible-charts.md` (verified) [SRC-VIZ-007] [SRC-VIZ-011].
10. **Task-based testing.** Give three to five people from each role their
    real decision question and the dashboard, and observe: can they answer
    it, how long, which tile they misread (context-dependent) [SRC-FLOW-023]
    [SRC-FLOW-001]. A dashboard "looks clear" is not a result.

## Operations and anomaly dashboards

Job: notice a deviation, judge severity, hand off to the person who fixes
it. Design the triage workflow, not a wall of graphs (hypothesis):

1. **Detect.** Each signal has a threshold or anomaly rule written next to
   it, so the reader knows why it is flagged. Status combines at least text
   and color, and ideally shape or icon; Carbon asks for three of symbol,
   shape, color, and type (context-dependent) [SRC-PROD-016] (verified for
   "not color alone") [SRC-VIZ-007].
2. **Triage.** Sort flagged items by severity and impact, show since when
   and how many are affected, and group duplicates of one cause together,
   because twenty red tiles for one outage hide the second outage
   (hypothesis).
3. **Hand off.** Each flagged item links to the runbook, the owning team,
   and the detailed trace or log view with the time window preselected
   (hypothesis).
4. **Acknowledge and resolve.** Show who acknowledged what, so two people do
   not work the same alert, and keep resolved items visible for a short
   period with their resolution (hypothesis).

Live updating: auto-updating content shown alongside other content needs a
way to pause it or control the update frequency (verified, WCAG 2.2.2 level A)
[SRC-WEB-003]. Animate a changed value at most with a brief highlight that
does not move layout, and under reduced motion show the change without
movement; timings come from `progressive-design-core/references/motion.md`.
Never flash; WCAG 2.3.1 sets the threshold (verified) [SRC-WEB-001].

## Executive dashboards

Job: decide priorities, budget, or escalation for a period. Defaults
(hypothesis unless cited):

- Lead with the three to five outcomes the organization committed to, each
  with target, current value, trend, and a one-sentence read written by the
  metric owner; a number without the owner's read invites the wrong story.
- Title each tile with its message, as in a chart (supported)
  [SRC-VIZ-006].
- Show the period, the data cutoff, and what changed since the last review.
- Status ("on track", "at risk") is a claim; link it to the evidence and the
  owner, and make "not measured" a visible status rather than a blank.
- Wording of figures in summaries follows `plain-numbers` when installed.

## Anti-patterns

- Metrics chosen because the data exists; no decision named (supported)
  [SRC-FLOW-022].
- Gauges, 3D, decorative imagery, meaningless variety of chart types
  (supported) [SRC-VIZ-005] (context-dependent) [SRC-VIZ-016].
- Red/green status as the only cue (verified) [SRC-VIZ-007].
- Auto-refreshing panels with no pause (verified) [SRC-WEB-003].
- Missing data drawn as zero; no data timestamp (hypothesis).

## Example

An on-call dashboard for an online shop's platform team.

- Decision questions: "Is checkout degraded right now?" and "Who needs to
  act?"
- Top row: checkout error rate and latency against their thresholds, each a
  line of the last 6 hours with the threshold labeled; status as text plus
  icon plus color.
- Triage list: flagged services sorted by customer impact, with since-when,
  owner, runbook link, acknowledge button.
- Labels EN / DE: "Checkout degraded since 14:05" / "Checkout gestört seit
  14:05"; "Acknowledge" / "Bestätigen"; "Data as of 14:12" / "Datenstand
  14:12"; "Pause updates" / "Aktualisierung pausieren".
- Not included: monthly revenue (executive view), a world map of traffic
  (no decision here).

## Validation

- Each tile maps to a written decision question; tiles without one are cut.
- Every metric shows freshness; missing data is visible.
- Task test done per role, with observed misreads recorded.
- Accessibility checks from `accessible-charts.md` passed or listed as open.

## Evidence gaps

- Stephen Few's pitfall-level text was read only at table-of-contents level
  [SRC-VIZ-016].
- No source in the registry tests operations triage layouts or executive
  dashboard structure; both sections are hypotheses to validate with the
  task test.
