---
name: grill-harness-with-docs
description: Grounds agent work in authoritative evidence, establishes shared understanding, critiques resolved material decisions and changes with a fresh agent, and resolves genuinely open decisions with a human. Use for resolved material work needing independent critique or for any product, domain, engineering, architecture, operations, security, compliance, or harness topic with unresolved intent, semantics, authority, consequential trade-offs, or material risk.
---

# Grill Work With Evidence

## 1. Ground Shared Understanding

1. Identify the outcome, scope, non-goals, and repository or system boundary.
2. Read the applicable instructions, domain sources, state, contracts, and
   checks.
3. Investigate discoverable facts through repository evidence, tools, and
   primary sources.
4. Name decision rights, assumptions, unknowns, success checks, stop
   conditions, and recovery.
5. Surface conflicting evidence with its sources and owning authority.

Grounding is complete when a human or fresh agent can state the same outcome,
evidence, boundaries, unresolved questions, and completion signal without
depending on chat inference.

## 2. Route the Branch

Classify each remaining uncertainty:

- reversible evidence-backed maintenance -> update autonomously
- bounded low-risk hypothesis -> run the smallest useful experiment
- resolved material decision or change -> run fresh-context agent critique
- unresolved intent, priority, semantics, architecture, governance, authority,
  model budget, blast radius, consequential trade-off, or material risk -> keep
  a human in the loop

Routing is complete when every dependent branch is resolved, assigned to the
right reviewer, or explicitly blocked.

## 3. Critique or Grill

For a resolved material branch, give a fresh-context agent the shared-
understanding frame, authoritative sources, diff or proposal, checks, and
non-goals. Ask it to find contradicted assumptions, missing evidence, boundary
violations, and failure paths. Tie findings to sources or checks, then keep,
change, remove, supersede, or rebuild the branch.

For a genuine human decision, resolve one dependent decision at a time:

1. State the decision and why evidence cannot resolve it.
2. Present two or three distinct options, including no change when meaningful.
3. State impact, trade-offs, reversibility, evidence, and blast radius.
4. Recommend one option with confidence and explicit assumptions.
5. Make the veto boundary explicit: no dependent branch runs until the human
   accepts an option.
6. Ask only this decision and wait.
7. Continue only after the answer restores shared understanding.

Do not send discoverable facts back to a human as questions. Do not implement
an unresolved branch. Proportional grilling is still required for every
significant topic; narrow reversible work may close through grounding,
self-review, and deterministic checks without a separate reviewer.

## 4. Persist Once

Update the smallest owning artifact:

- stable agent behavior -> concise agent instructions
- domain language or invariant -> domain context
- source or relationship routing -> context map
- accepted consequential trade-off -> ADR
- repeated probabilistic procedure -> Skill
- deterministic enforcement -> Hook, CI, test, or platform control
- durable evidence-backed observation -> learning log

Route portable public methods to their public upstream, shared non-public
procedures to the private organization or team catalog, cross-repository policy
to its coordinator, and product or service truth to the owning repository.
Reference owners instead of copying the same learning across repositories.

## 5. Verify and Hand Off

1. Re-state the resolved outcome, boundaries, decision owner, checks, and stop
   condition.
2. Run the smallest relevant deterministic checks.
3. Review the diff or decision against sources, scope, and non-goals.
4. Keep a workflow human-in-the-loop until explicit scope, permissions,
   meaningful checks or evals, recovery, rollback, observability, and repeated
   evidence justify another oversight mode.
5. Record the next re-check trigger only when future evidence could change the
   decision.

Complete the run only when every fact is grounded or marked as a source
conflict, every decision is resolved or blocked, each change has one owner,
verification is reported, and the oversight mode is explicit.
