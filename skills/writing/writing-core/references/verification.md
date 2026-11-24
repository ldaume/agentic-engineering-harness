# Verification

Generated prose must not add facts.

## Claim classes

Assign each statement, at least mentally:

- SOURCE FACT: stated by the user, repository, ticket, or a checked source.
- INFERENCE: follows from facts; phrase it as such ("this suggests").
- RECOMMENDATION: your proposal; phrase it as one ("my recommendation").
- RHETORICAL FRAMING: emphasis or ordering, adds no fact.
- UNKNOWN: not established; either omit or state as open.

## When to check sources

Re-check when a claim is time-sensitive (prices, versions, dates, people's
roles), externally published, high-impact, or explicitly needs evidence. For
public web copy, make expertise and factual accuracy visible; do not write for
rankings.

## AI-assisted text

Generated text is judged by the value it adds and by its accuracy, not by
whether a model wrote it: fact-check the body and the metadata - titles,
meta descriptions, structured data, alt text - by hand before publishing
(verified) [SRC-WRITE-006]. Put the truth layer before the language layer:
give the model the verified facts, the unknowns, the terms, and the output
contract, then draft (hypothesis; a working method, not a measured
result).

## Claim ledger pass

Before a text counts as done, list each claim once with its source: a file and
line, a merged change, a measurement, a document. Then read the ledger, not the
text, for two things:

- Duplicates: one claim in two places in other words. Keep one home.
- Contradictions: two claims that cannot both hold (a figure, a date, a
  decided against an open status). Fix the one the source does not back.

Claims must rest on facts or code in both directions. Overclaiming says more
than the code, data or merged change shows. Underclaiming describes as planned,
partial or missing what is already implemented and merged. Both are errors.
Check each claim about a system against the current state, not memory: read a
claim about code from the code at the current default branch, and a status from
the tracker or the merge, not from an earlier draft.

## Receiver cost of AI-assisted drafts

Before sending an AI-assisted draft, check that it moves the reader's task
forward and does not shift work downstream: a reader who must verify, complete
or decode it pays for the writer's shortcut. Polish without substance costs
trust. HBR named the pattern "workslop" in a survey-based article by BetterUp
Labs and the Stanford Social Media Lab (survey; supported) [SRC-WRITE-053].

## Never invent

Facts, customer evidence, metrics, percentages, decisions, test execution,
deadlines, quotes, testimonials, logos, certifications, or certainty. If the
artifact needs one that does not exist, write around it specifically and tell
the user what proof would strengthen it.

## Fact fixture for tests

```json
{
  "facts": ["Security review is complete.", "Three pilot customers are planned."],
  "unknown": ["The feature reduces support requests by 30%.", "Customers prefer CSV."],
  "forbidden_claims": ["30% fewer support requests", "customers prefer CSV"]
}
```

Paraphrase is allowed; stating anything from `unknown` as fact is not.
`scripts/quality_gate.py --facts facts.json` errors on a forbidden claim and
warns on any percentage that no fact contains.
