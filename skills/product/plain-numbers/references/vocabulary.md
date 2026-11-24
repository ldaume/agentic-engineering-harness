# Numbers Vocabulary

The terms statisticians, risk communicators, and data journalists use when they
judge how a figure is reported, so a review names the misreading a number
invites. Authors and check scripts use it; reviews do not load it by default.
Prose terms (sentence length, claim class, restating) live in writing-core's
`references/vocabulary.md`; chart marks (proportional ink, direct labeling) in
design-core's. Check: `exact`, `jev`, or `judge`; no check script ships these
rules yet, so every row is `judge` until one does.

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Denominator | The whole a share is taken from, stated next to the share. | [SRC-WRITE-071] [SRC-WRITE-070] | A percentage with no "of N" and no raw counts ("37%" instead of "85 of 227 (37%)"). | judge |
| Natural frequency | A count out of a stated whole instead of a conditional probability or a bare rate. | [SRC-WRITE-071] | A rate or probability that only a reader with the formula can turn back into cases. | judge |
| Absolute change | The size of a change in the unit itself, given before any relative change. | [SRC-WRITE-071] [SRC-WRITE-070] | "+25%" or "a quarter fewer" with no from and to values. | judge |
| Percentage point | The difference between two percentages, which is not the relative change between them. | [SRC-WRITE-070] [SRC-WRITE-071] | "rose 5%" where the share went from 20% to 25% (5 points, 25% more). | judge |
| Baseline | The value and period a change is measured against. | [SRC-WRITE-070] | "improved", "has not changed yet" with no starting value or comparison period. | judge |
| Range estimate | An uncertain or future figure given as a range with what it rests on. | [SRC-WRITE-070] [SRC-WRITE-045] | A point forecast ("ready in 4 weeks", "2,000 EUR") or a verbal hedge ("fairly uncertain") instead of a range. | judge |
| Estimate label | A figure that comes from a model, sample, or guess says so and shows its basis. | [SRC-WRITE-070] | A modeled or extrapolated number written like a count, without "estimate" or its formula. | judge |
| Broadly stable | A change inside the noise is reported as no change, not as a rise or fall. | [SRC-WRITE-070] | "rose from 37% to 38%" on a sample whose interval covers both values. | judge |
| Interval verdict | A verdict against a target follows the interval, not the point estimate. | [SRC-WRITE-070] [SRC-WRITE-045] | "target reached" when the interval still contains values below the target. | judge |
| Chart relationship | The relationship the numbers show (deviation, correlation, ranking, distribution, change over time, part-to-whole, magnitude, spatial, flow) picks the chart. | [SRC-VIZ-001] [SRC-VIZ-006] | A chart type that does not match the stated message: a pie for change over time, a line for a ranking. | judge |

## Not admitted

- "Always round to whole percentages": rounding hides a change the decision
  turns on; round to what the sample size supports and keep the raw counts.
- A relative change alone as the headline ("cuts the risk by 25%"): it makes
  a small absolute effect look large [SRC-WRITE-071].
