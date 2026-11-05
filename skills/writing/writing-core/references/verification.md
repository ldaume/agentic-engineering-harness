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
