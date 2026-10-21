---
name: progressive-engineering
description: Use whenever writing a commit message, a pull request description, a Confluence technical page, developer or operational documentation, or an engineering decision summary (Commit-Message, PR-Beschreibung, technische Doku). Use it even for a one-line commit; it carries the subject rules, why-before-what, and honest validation reporting. Not for implementing or fixing code, or for deciding whether a change needs an ADR.
license: MIT
---

# Progressive Engineering Writing

Technical writing shortens the distance between intent and correct action.
Writing code is not this skill's job; describing it is. For ADR policy and
when a decision needs a record, `documentation-and-adrs` owns the decision;
this skill owns the prose.

## Repository truth first

Before writing from code, read the repository instructions, the relevant diff
or code, the tests, and any linked issue, ADR, or docs; keep established
naming and conventions (commit style included), because reviewers check the
text against the code and the house style.

## Principles

Clear actor, active voice where responsibility matters, consistent
terminology, one concept per section, explicit prerequisites, verifiable
steps, exact claims. Never claim tests, benchmarks, incidents, deployments,
or validation without evidence from the repository or user; write "not
tested" instead, because a reviewer trusts the validation section to decide
how hard to look.

## Route

- Confluence, durable technical docs: `references/confluence.md` and
  `references/technical-writing.md`
- pull request description: `references/pull-requests.md`
- commit message: `references/commits.md`

## Gate

From this skill's directory, run
`python3 ../progressive-writing-core/scripts/quality_gate.py --artifact <type>
--lang <de|en> FILE` with type one of `pull_request|commit|confluence`.
If the file is missing (this skill was installed alone), check the
artifact's checklist in its reference by hand. Fix every error; judge each
warning, because warnings are heuristics, not rules.

## Done when

The text states the behavior, the reason, the relevant constraints, and the
actual validation at the level its reader needs.
