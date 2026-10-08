# Misreading Cases

Real misreadings from reader tests and reviews. Check new text against them.
Format: text, misreading, fix. Origin of the first four: a weekly project page,
2026-10-08, generalized.

## Match rate read as workload

- Text: "37% of change requests got a prepared answer that matched what the desk
  did."
- Misread as: 37% fewer tickets reach a person.
- Fix: "A prepared answer matched what the desk did in 85 of 227 requests (37%).
  A person still checks every answer, so this saves time per request. It does
  not reduce the number of requests."

## Subset read as additive

- Text: "60% where the board marks a suggestion likely right", shown next to the
  37%.
- Misread as: an extra 60% on top of the 37%.
- Fix: "26 of the 43 suggestions marked likely right are among the 85 matches,
  not extra." Name the set each figure comes from; sample sizes (422, 227, 96)
  differ, so say which set each count covers and why.

## Number without its meaning

- Text: "72% of misses: the desk's answer was in none of the 10 most similar
  earlier tickets."
- Misread as: not understood.
- Fix: lead with the meaning: "72% of the misses had no earlier case to learn
  from: in none of the 10 most similar earlier tickets was the desk's answer
  present." Name the set the 72% is taken from.

## Method overstated

- Text: "replayed with only what was known on its own day."
- Misread as: a clean past-dated test.
- Fix: state what was cut and what was read in today's state: "Tickets were
  cut to the state at creation. Status and assignee fields were read as of
  today."

## Point estimate judged against a target

- Text: "Subgroup rate: 60% (26 of 43). Target 50%: Reached."
- Misread as: the target is met. The 95% interval, 46 to 74%, still includes
  50%, so the sample cannot tell. A person caught it by checking the math.
- Fix: "Likely, not proven: 26 of 43 (60%, 95% interval 46 to 74%) against a
  proposed 50% target. An independent replication gave 22 of 37 (43 to 74%).
  A stricter self-set 70% target was missed."

## Cold-reader findings to check for

- Bare numbers side by side invite adding them up.
- Undefined terms (pull request, merged, go-ahead, desk).
- Relation between sample sizes left unexplained.
- A goal stated twice, in different words.
- A vague rule ("short") where a bound ("at most 250 characters") belongs.
