---
name: grill-harness-with-docs
description: Grounds uncertain Agentic Engineering harness changes in repository evidence, resolves genuine decisions with a human, and persists the outcome in the owning artifact. Use when harness work involving AGENTS.md, context, Rules, Skills, Hooks, MCP, memory, evals, cross-repository coordination, or oversight transitions encounters unresolved intent, authority, semantics, or trade-offs.
---

# Grill Harness With Docs

## 1. Ground

1. Identify the repository-local or cross-repository scope.
2. Read the applicable instruction hierarchy, harness contract, context map,
   and the sources they route to.
3. Investigate discoverable facts through repository evidence, tools, and
   primary sources.
4. Surface conflicting evidence with its sources and owning authority.

Complete grounding when each discoverable fact is established or represented
as an explicit source conflict.

## 2. Route

Classify each remaining uncertainty:

- reversible evidence-backed maintenance -> update autonomously
- bounded low-risk hypothesis -> run the smallest useful experiment
- unresolved intent, priority, semantics, architecture, governance, authority,
  model budget, autonomy, blast radius, or material risk -> keep a human in the
  loop

Complete routing when only genuine human decisions remain.

## 3. Grill

Resolve dependent decisions one at a time:

1. State the decision and why evidence cannot resolve it.
2. Present two or three distinct options, including no change when meaningful.
3. State impact, trade-offs, reversibility, and evidence for each option.
4. Recommend one option with confidence and explicit assumptions.
5. Make the veto boundary explicit: no dependent branch runs until the human
   accepts an option.
6. Ask only this decision and wait.
7. Continue only after the answer.

Do not implement an unresolved branch. Complete grilling when the human
confirms shared understanding or the remaining branch is explicitly blocked.

## 4. Persist

Update one owning artifact:

- stable agent behavior -> concise agent instructions
- domain language or invariant -> domain context
- source or relationship routing -> context map
- accepted consequential trade-off -> ADR
- repeated probabilistic procedure -> Skill
- deterministic enforcement -> Hook, CI, test, or platform control
- durable evidence-backed observation -> learning log

Reference owning sources instead of duplicating them. Preserve the target
repository's language and artifact conventions.

## 5. Verify and Hand Off

1. Run the smallest relevant checks.
2. Review the diff for stale, duplicated, speculative, or unowned layers.
3. Keep the workflow human-in-the-loop until it has explicit scope,
   permissions, meaningful checks or evals, recovery, rollback, observability,
   and repeated evidence.
4. Propose human-on-the-loop with remaining risks, exception handling, and a
   recommendation.

Complete the run only when:

- every fact is grounded or marked as a source conflict,
- every decision is resolved or explicitly blocked,
- no unresolved branch was implemented,
- each change has one owning artifact,
- verification results are reported,
- the oversight mode and next transition trigger are explicit.
