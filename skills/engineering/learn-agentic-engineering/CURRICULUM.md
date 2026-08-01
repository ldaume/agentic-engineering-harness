# Agentic Engineering Learning Path

## Contents

- [How to Use This Path](#how-to-use-this-path)
- [L1 - Bounded Agent-Assisted Work](#l1--bounded-agent-assisted-work)
- [L2 - Repeatable Procedures](#l2--repeatable-procedures)
- [L3 - Living Repository Harness](#l3--living-repository-harness)
- [L4 - Grounded System Work](#l4--grounded-system-work)
- [L5 - Stateful Agent Workflows](#l5--stateful-agent-workflows)
- [L6 - Governed Value Stream](#l6--governed-value-stream)
- [L7 - Adaptive Product System](#l7--adaptive-product-system)
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

## L5 - Stateful Agent Workflows

**Outcome:** Run bounded product or SDLC agents with state, recovery, evals, and
observability.

Learn:

- agents serve continuing contexts; workflows serve finite operations
- conversation, workspace, and business state have different owners
- retries require idempotency and known duplicate-effect behavior
- evals measure representative behavior; deterministic checks protect
  invariants
- orchestration needs admission, budgets, cancellation, and recovery

Practice:

1. Use **build-autonomous-agents** to define one execution contract.
2. Implement one typed vertical slice with a proposal/application boundary.
3. Test malformed output, tool failure, retry, and cancellation.
4. Inspect a run from trigger through verified outcome.

Common traps: framework-first design, open-ended overnight agents, hidden
failure behind a spinner, or assuming a runtime checkpoints arbitrary code.

## L6 - Governed Value Stream

**Outcome:** Delegate parts of delivery while preserving policy, accountability,
and safe intervention.

Learn:

- risk classes determine permissions and human approval points
- human-on-the-loop requires reliable telemetry, alerts, budgets, and kill
  controls
- parent and worker models are selected from live capability and total outcome
  cost, not token price alone
- production feedback and incidents must change checks, context, or authority

Practice:

1. Select one delivery step with stable inputs and measurable outcomes.
2. Define admission, isolation, policy gates, rollback, and incident owner.
3. Run a representative pilot without automatic merge or deployment.
4. Review escaped failures and either improve, narrow, pause, or remove the
   automation.

Common traps: autonomy as a permission shortcut, unconditional review loops,
or measuring throughput while ignoring rework and failure impact.

## L7 - Adaptive Product System

**Outcome:** Use governed agents in product sensing, experiments, and decisions
without hiding strategic accountability.

Learn:

- product autonomy depends on trustworthy signals, explicit decision rights,
  experimentation, and stop criteria
- local optimization can damage customers, portfolios, or organizational
  incentives
- agents may propose and execute bounded experiments; accountable humans still
  own consequential strategy, ethics, and authority transitions
- technical change becomes operating-model and organizational transformation

Practice:

1. Choose one reversible product hypothesis with a measurable customer outcome.
2. Define data provenance, decision boundary, budget, kill condition, and
   affected stakeholders.
3. Let the system propose or run only the authorized experiment.
4. Review outcome, externalities, and whether authority should expand, remain,
   narrow, or stop.

Common traps: calling automated backlog generation L7, optimizing proxy metrics,
or expanding autonomy without change leadership and governance.

## Question and Blocker Routes

| Question | Start here |
|---|---|
| "What is this term?" | direct definition, repository example, consequence |
| "Rule, Skill, Hook, or MCP?" | recurring problem, authority, probabilistic guidance versus deterministic enforcement |
| "Why does the agent keep failing?" | context, changeability, grounding, permissions, ownership, feedback |
| "What should I practice next?" | weakest relevant maturity dimension and one real task |
| "Can this run overnight or in CI?" | L5 execution contract, then L6 governance if effects widen |
| "Can the agent decide product direction?" | L7 signals, rights, experiment limits, and human accountability |
| "I am overwhelmed." | reduce scope to one question, one artifact, or one verified slice |

Do not answer a blocker with a larger artifact set. Remove uncertainty or reduce
the delegated unit first.
