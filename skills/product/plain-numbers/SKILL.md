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
   "The prepared answer matched what the desk did in 85 of 227 requests (37%)."
2. State what it does not mean when a likely misreading exists. A match rate is
   not fewer requests; a sample share is not a population share.
3. State how numbers on one page relate: part of, extra to, or a different set.
   Name the set each comes from ("26 of 43, part of the 85, not extra").
4. Define each term a cold reader cannot know on first use, or use an everyday
   word instead. Names for internal tools, processes, and jargon count.
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
