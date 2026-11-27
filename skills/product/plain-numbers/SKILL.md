---
name: plain-numbers
description: Writes and reviews numbers for readers who were not in the work, so a manager, client, or stakeholder reads each figure the way it was measured. Use when writing or checking a status update, weekly or check-in page, results summary, dashboard, report, or slide that carries percentages, counts, or other metrics. Not for code docs, agent instructions, marketing copy without metrics, or a chat reply to the person who did the work.
license: MIT
---

# Plain Numbers

A figure is read without its author. The reader supplies the meaning, so a
number with no stated meaning gets the most flattering or the most familiar one.
This Skill makes the text carry the meaning, and proves it with a reader who
knows nothing else.

## Write

Name the reader first (for example "a manager at the client who joins the
meeting"). Then apply to every number:

1. One idea per sentence. Meaning first, then the number with its raw counts:
   "The drafted answer matched what the team sent in 80 of 200 requests (40%)."
   A statement about change names its baseline (from what) and, where known,
   its target (to what): "still at today's level", never "has not changed yet".
2. State what it does not mean when a likely misreading exists. A match rate is
   not fewer requests; a sample share is not a population share.
3. State how numbers on one page relate: part of, extra to, or a different set.
   Name the set each comes from ("26 of 40, part of the 80, not extra").
4. Define each term a cold reader cannot know on first use, or use an everyday
   word instead. Names for internal tools, processes, and jargon count. A
   statistical coefficient (correlation, exponent, sigma, a prior) is jargon:
   in running text replace it with an example from the data and keep the
   number for the method section.
5. Put each caveat in its own sentence. An aside in brackets is skipped.
6. State the goal once. Use a measurable bound instead of a vague word:
   "at most 250 characters", not "short".
7. Trace every number to a measurement or a merged change. Otherwise write
   "estimate" and show the formula.
8. Claim no more than the method does. If a replay cuts the data to a past date
   but reads some fields in today's state, say exactly what was cut and what was
   not.
9. Judge a verdict against a target (reached, above, below) by the interval,
   not the point estimate. When the interval contains the target, write
   "likely, not proven" and show the interval and the sample size.
10. Prefer a numeric range to a verbal hedge: "between 30% and 44%" over
    "fairly uncertain". In experiments, a numeric range cost little trust and a
    verbal hedge cost more (van der Bles et al., PNAS 2020, abstract read on
    2026-11-24; verified) [SRC-WRITE-045].
    A number about the future (effort, cost, date, volume) is always a range,
    never a point estimate: "between 3 and 5 weeks", "1,500 to 2,500 EUR". Say
    what the range rests on and what would change it. A forecast computed from
    measured throughput or cost data beats a guess; show the data and the
    formula (`estimate-with-uncertainty` owns computing it). Where the decision does not need the estimate, define the value
    and the boundary instead (an outcome and the most the team will spend on
    it).
11. State the denominator and the absolute change before any relative change:
    "from 40 to 50 of 200 requests (20% to 25%, +5 points, 25% more)", never
    "+25%" alone.
12. Write numbers in the language's own format. German: decimal comma,
    thousands point, an ordinary space before the percent sign ("37 %",
    "1.500", "2,5"); English: decimal point, thousands comma, no space
    ("37%", "1,500"). Always an ordinary space, never a no-break space (the
    plain-punctuation rule).

Check the figures against the source data before writing prose around them.

## Reader test

Run it before the text goes out, and after any change to a number or its
framing. Fill `reader-test.md` with the reader and the rendered text, and hand
it to a fresh agent with no other context: not the data, not the thread, not
your explanation.

Complete when every number is restated correctly, every likely-misreading
question is answered correctly, the hypothesis and next steps come back right,
and no unclear item blocks. Fix a misread number or a blocking unclear item and
rerun with a fresh agent. Keep an unclear item only on purpose, and say so in
your report. After three rounds without convergence, the text is carrying too
much: cut numbers rather than add explanation.

## Improve

When a person or the reader test misreads something real, add a case to
`evals.md` (input text, the misreading, the fixed text) and read the file
before writing. Keep it to real cases, one short entry each; merge entries that
teach the same lesson.

## Boundaries

Pair with a humanizer for tone and with a charting Skill for visuals. This
Skill owns whether the reader gets the figure right, not how the page looks.
