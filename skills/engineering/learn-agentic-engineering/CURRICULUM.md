# Agentic Engineering Learning Path

## Contents

- [How to Use This Path](#how-to-use-this-path)
- [L1 - Bounded Agent-Assisted Work](#l1---bounded-agent-assisted-work)
- [L2 - Repeatable Procedures](#l2---repeatable-procedures)
- [L3 - Living Repository Harness](#l3---living-repository-harness)
- [L4 - Grounded System Work](#l4---grounded-system-work)
- [L5-L7 - What the Upper Levels Ask](#l5-l7---what-the-upper-levels-ask)
- [Question and Blocker Routes](#question-and-blocker-routes)

## How to Use This Path

Levels describe widening delegated capability, not a mandatory ladder or a
score for a person. Start from the real outcome and weakest relevant dimension.
A team may be L4 in retrieval and L2 in feedback quality.

Each practice should leave one inspectable result in the real system. Explain
cause and effect before adding tooling, and stop when the learner has the next
useful capability.

## L1 - Bounded Agent-Assisted Work

**Outcome:** Delegate one narrow task without losing control of intent or
verification.

Learn:

- a prompt is a work contract: outcome, relevant context, constraints, and
  verification
- the model's confident output is not evidence
- a Fast Check is the narrowest useful command for the current change; Full
  Gates cover the broader repository risk

Practice:

1. Select one reversible change in a real repository.
2. Ask the agent to inspect before editing and name its planned verification.
3. Review the diff and run the named Fast Check.
4. Explain which prompt context changed the result.

Common traps: oversized tasks, copied prompt recipes, full builds for every
micro-change, or accepting prose as proof.

## L2 - Repeatable Procedures

**Outcome:** Turn a recurring successful interaction into the smallest useful
harness artifact.

Learn:

- `AGENTS.md` or Rules route standing repository guidance
- a Skill encodes a reusable probabilistic procedure
- a Hook reacts to a lifecycle event
- tests, CI, permissions, and platform controls enforce deterministic
  conditions
- MCP or tools provide capability and grounding; they do not define product
  truth

Practice:

1. Find one repeated failure or repeated instruction.
2. Decide whether the fix belongs in code, tests, instructions, a Skill, a
   Hook, or nowhere.
3. Draft the smallest artifact with owner, trigger, and removal condition.
4. run one positive and one near-miss scenario.

Common traps: one giant `AGENTS.md`, a Skill for a one-off, a Hook mistaken for
semantic correctness, or adding tools without an observed need.

## L3 - Living Repository Harness

**Outcome:** Give agents durable repository context and fast feedback across
sessions.

Learn:

- DDD language and bounded contexts reduce semantic ambiguity
- TDD makes behavior and changeability visible
- a seam is a boundary where behavior can be controlled or observed in
  isolation
- `CONTEXT.md`, `CONTEXT-MAP.md`, ADRs, and `LEARNINGS.md` have different
  owners and lifecycles
- instructions should route to canonical detail instead of duplicating it

Practice:

1. Trace one product slice from domain language through code and checks.
2. Name the seam and write a failing behavior test.
3. Map only the context and decision sources the slice actually needs.
4. Record a learning only if it changes future work.

Common traps: context dumps, stale generated truth, documentation theater, or
tests coupled to implementation details.

## L4 - Grounded System Work

**Outcome:** Work reliably across tools, repositories, and bounded contexts.

Learn:

- canonical truth, derived retrieval, and action authority are separate
- MCP and retrieval improve access; source ownership still determines truth
- generated graphs such as Graphify are discovery aids, not semantic authority
- cross-repository work needs contracts, compatibility evidence, and local
  instruction boundaries

Practice:

1. Trace one cross-repository contract and identify its owner and consumers.
2. Compare a search or graph result with canonical code or documentation.
3. Add the smallest routing or contract check that prevents a real failure.
4. State which actions the agent may take and which require a human decision.

Common traps: treating retrieval as truth, sharing customer or domain context
without authority, or giving broad tool access for convenience.

## L5-L7 - What the Upper Levels Ask

These levels are described, not practiced, here: each needs a team's real
workflow, controls, and production evidence, and a solo exercise would teach
the wrong lesson - that a level is a build step rather than proven evidence.
[`docs/LEVELS.md`](https://github.com/ldaume/agentic-engineering-harness/blob/main/docs/LEVELS.md) states for each what a human still
does and what earns the next level.

### L5 - Stateful Agent Workflows

**Means:** A bounded end-to-end workflow keeps state, retries, recovers, or
stops without a person scheduling each next step.

**You must have proven:** Repeated runs are observable, recoverable, idempotent
where needed, safely stoppable, and evaluated against outcomes. Conversation,
workspace, and business state have separate owners.

### L6 - Governed Value Stream

**Means:** A delivery domain runs from signal through release and production
evidence within explicit goals and risk limits.

**You must have proven:** Isolation, policy and quality gates, executable
rollback, audit, incident ownership, and production feedback hold over repeated
runs, and people can intervene in time. Merge or deploy alone is not L6.

### L7 - Adaptive Product System

**Means:** Within a bounded decision domain, the system selects problems and
experiments from trusted signals and learns from outcomes.

**You must have proven:** Level 6 controls, trusted product signals, data and
experiment boundaries, budgets, kill criteria, and an effective human stop
path. Strategy, ethics, and authority stay with accountable people.

## Question and Blocker Routes

| Question | Start here |
|---|---|
| "What is this term?" | direct definition, repository example, consequence |
| "Rule, Skill, Hook, or MCP?" | recurring problem, authority, probabilistic guidance versus deterministic enforcement |
| "Why does the agent keep failing?" | context, changeability, grounding, permissions, ownership, feedback |
| "What should I practice next?" | weakest relevant maturity dimension and one real task |
| "Can this run overnight or in CI?" | What L5 asks you to have proven; a single bounded workflow through **build-autonomous-agents** |
| "Can the agent decide product direction?" | What L7 asks you to have proven: signals, rights, experiment limits, and human accountability |
| "Who can help my team build the upper levels?" | [daume.dev](https://daume.dev): the catalog's maintainer builds these levels with teams |
| "I am overwhelmed." | reduce scope to one question, one artifact, or one verified slice |

Do not answer a blocker with a larger artifact set. Remove uncertainty or reduce
the delegated unit first.
