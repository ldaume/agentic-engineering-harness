# Misreading Cases

Misreadings seen in reader tests and reviews, generalized; every figure below
is invented. Check new text against them. Format: text, misreading, fix.

## Match rate read as workload

- Text: "40% of support requests got a drafted answer that matched what the
  team sent."
- Misread as: 40% fewer requests reach a person.
- Fix: "A drafted answer matched what the team sent in 80 of 200 requests
  (40%). A person still checks every answer, so this saves time per request.
  It does not reduce the number of requests."

## Subset read as additive

- Text: "65% where the tool marks a draft likely right", shown next to the 40%.
- Misread as: an extra 65% on top of the 40%.
- Fix: "26 of the 40 drafts marked likely right are among the 80 matches, not
  extra." Name the set each figure comes from; when sample sizes differ, say
  which set each count covers and why.

## Number without its meaning

- Text: "70% of misses: the team's answer was in none of the 10 most similar
  earlier requests."
- Misread as: not understood.
- Fix: lead with the meaning: "70% of the misses had no earlier case to learn
  from: none of the 10 most similar earlier requests held the team's answer."
  Name the set the 70% is taken from.

## Method overstated

- Text: "replayed with only what was known on its own day."
- Misread as: a clean past-dated test.
- Fix: state what was cut and what was read in today's state: "Requests were
  cut to the state at creation. Status and assignee fields were read as of
  today."

## Point estimate judged against a target

- Text: "Subgroup rate: 60% (24 of 40). Target 50%: Reached."
- Misread as: the target is met. The 95% interval, about 45 to 74%, still
  includes 50%, so the sample cannot tell.
- Fix: "Likely, not proven: 24 of 40 (60%, 95% interval about 45 to 74%)
  against a proposed 50% target." Add a replication or a stricter target only
  with its own interval.

## Change without a baseline

- Text: "The outcome this work is about has not changed yet."
- Misread as: unclear. The reader asked "changed from what to what?"
- Fix: state the current value as the baseline, why it cannot have moved yet,
  and what is not measured: "Still at today's level: a median of 12 hours to
  a real answer, 50 of 100 the same working day. Nothing is live yet, so it
  cannot have moved. Reopened requests are not measured."

## Point estimate for the future

- Text: "The migration takes 3 weeks and costs 2,000 EUR." Also "Das dauert 3
  Wochen und kostet 2.000 EUR."
- Misread as: a commitment. The reader plans around the single value, and a
  miss reads as a broken promise.
- Fix: "Based on the last four migrations (2 to 4 weeks, 1,200 to 2,600 EUR),
  expect between 2 and 4 weeks and 1,200 to 2,600 EUR. A second database would
  move it to the upper end." A figure for the future is a range with its basis
  and what would change it.

## Statistical coefficient in running text

- Text: "Mehr Story Points heißen tendenziell mehr Code, mit vielen
  Ausnahmen (0,4 auf einer Skala bis 1)." Also "Team B's items cost about
  twice as much at the same size (95%: 0.9 to 4.5)."
- Misread as: unclear. A correlation coefficient means nothing to a manager.
  The second reads as a proven effect, but the interval starts below 1 (no
  effect is inside it).
- Fix: replace the coefficient with an example from the data ("an item with 3
  points often changes more lines than one with 5") and say the interval in
  words ("on average more expensive, about twice; with few items this is not
  certain: from the same cost to four times as much"). Formulas,
  coefficients, exponents and priors go to the method section only.

## Partial cost read as the whole cost

- Text: a headline gives one cost component as "the cost per order", and a
  footnote further down says the largest component is not included.
- Misread as: the headline figure is the full cost.
- Fix: name the part in the headline itself ("shipping cost per order,
  without production"). Give the missing part as an estimate with its basis,
  or say it is unknown.

## Cold-reader findings to check for

- Bare numbers side by side invite adding them up.
- Undefined terms (pull request, merged, go-ahead, internal team names).
- Relation between sample sizes left unexplained.
- A goal stated twice, in different words.
- A vague rule ("short") where a bound ("at most 250 characters") belongs.
