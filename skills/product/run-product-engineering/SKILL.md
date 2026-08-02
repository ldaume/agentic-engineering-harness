---
name: run-product-engineering
description: Runs an evidence-driven product engineering system from signals and ideas through triage, problem framing, discovery, bets, small-batch implementation, validation, release, observability, incidents, bug fixing, outcome review, and evolution. Use when coordinating an end-to-end product lifecycle, designing a product operating model, connecting discovery with delivery and operations, or delegating bounded L5-L7 value streams to agents.
---

# Run Product Engineering

Operate a closed product loop. A release is an intervention, not completion;
production evidence must change the next product or engineering decision.

The loop is not a sequence of specification, implementation, testing, and
deployment handoffs. Domain discovery, examples, tests, security, operability,
delivery, and production learning advance together in the smallest useful
cycles.

Run only the loop the current decision needs. A task loop may sit inside a
repository loop, which may sit inside a stateful workflow or governed value
stream. Higher delegation wraps proven smaller loops; it does not require every
task to traverse a portfolio process.

For one isolated implementation or bug fix with no lifecycle decision, use the
relevant craft Skill, upstream **diagnosing-bugs**, **coding-discipline**, and
**completion-gate** directly.

## 1. Ground the Operating Domain

Read the target's product context, customer evidence, domain language, current
bets, architecture, delivery system, telemetry, incidents, support signals,
security and compliance obligations, and decision rights.

Identify:

- the product or value-stream owner
- canonical sources for signals, decisions, work state, and production evidence
- bounded contexts, ubiquitous language, invariants, domain events, public
  contracts, and their semantic owners
- current reliable harness level from `scaffold-harness/MATURITY.md`
- agent authority, human veto, budgets, and escalation paths
- the actual Fast Check, Full Gates, release, rollback, and incident controls

Preserve local vocabulary and tools. Do not create a new board, artifact set, or
cadence when the existing system already exposes the required state.

## 2. Admit Work as a Signal

Treat ideas, requests, telemetry, bugs, incidents, security findings, compliance
constraints, operational pain, and strategic opportunities as signals. Do not
promote a signal directly into delivery.

A backlog, when the target uses one, is a short visible pull queue for current
decisions. It is not a commitment inventory or a substitute for signal
provenance, triage, outcome evidence, or kill criteria.

Triage enough to establish:

- source, affected users or system, evidence strength, and urgency
- value, usability, feasibility, viability, security, compliance, and
  operability risk
- reversibility, blast radius, dependencies, and decision owner
- next action: discard, observe, investigate, contain, discover, deliver, or
  escalate

Incidents and urgent vulnerabilities may enter a contained recovery path
without waiting for normal discovery. They still return evidence to the same
product loop.

## 3. Frame the Smallest Decision

Use **product-craft** for problem framing, opportunities, bets, outcome
boundaries, and strategic trade-offs. Use **scaffold-distributed-context** for
cross-repository bounded contexts and upstream **domain-modeling** when shared
language is unclear.

Create or update only the target's smallest equivalent of:

- problem statement and evidence
- intended customer and business outcome
- riskiest assumptions and risk burn-down
- candidate intervention and explicit non-goals
- investment boundary, success, pivot, and kill criteria
- owner, review date, and decision rights

The work is ready for focus when the next investment decision is possible, not
when every implementation detail is specified.

Treat the domain model and solution concept as hypotheses that examples,
implementation, and production evidence may refine. Do not freeze a complete
up-front model or specification and hand it to delivery as presumed truth.

## 4. Define the Delivery and Learning Contract

Before building, connect the bet to the smallest useful delivery and learning
contract. This is not a comprehensive specification or stage gate. Include:

- one thin, releasable slice
- behavioral examples, negative or abuse cases, and deterministic acceptance
  boundaries
- risk-ranked test, eval, threat, operability, and evidence signals
- architecture, data, security, compliance, and operational constraints
- rollout, migration, rollback, support, and incident ownership
- product outcome, adoption, reliability, cost, and guardrail signals
- observation window and outcome review decision

Use **integrate-product-compliance** only when confirmed scope or obligations
apply. Compliance interpretation and risk acceptance remain with named human
owners.

## 5. Build, Validate, and Release

Route the slice to the relevant craft Skill, **coding-discipline**,
**testing-strategies**, an installed upstream **tdd** when it fits, and
**completion-gate**. Use **build-autonomous-agents** when the product capability
or value stream itself needs an agent runtime.

Burn down the next uncertainty before expanding the slice. When learning is
cheaper than production design, run a bounded experiment, prototype, or
technical spike with a hypothesis, timebox, isolation, and explicit exit. Mark
its code provisional; avoid production secrets, data, privileges, and effects.
End with discard, another experiment, or an explicit production decision.
Never let plausible spike code silently become the production implementation.

For production behavior, use a vertical TDD loop: express one domain example at
a public boundary, run the failing check, implement the minimum coherent
behavior, refactor while green, and update domain language or contracts when the
model changes. Security, privacy, accessibility, compliance, operability,
telemetry, and evidence are design inputs throughout the loop, not downstream
review departments.

Build quality, security, operability, accessibility, telemetry, and evidence
into the slice. Use a risk-based release policy with least privilege, isolation,
review, progressive exposure, rollback, and explicit approval where required.

The release completes only when the intended behavior, telemetry, rollback, and
ownership are live and inspectable.

## 6. Close the Production Loop

Observe customer outcome and system behavior together. Use traces, metrics,
logs, product analytics, support, revenue or retention signals, and qualitative
feedback only within their documented provenance and privacy boundaries.

Route production signals:

- **bug:** establish a reproduction loop, diagnose root cause, add a failing
  check, make the smallest fix, release, and watch the affected signal
- **incident:** contain, restore, investigate, remediate, verify recovery, and
  feed the learning into controls and product priorities
- **weak adoption or outcome:** inspect value, usability, distribution,
  reliability, and measurement assumptions before adding features
- **successful outcome:** decide whether to scale, standardize, continue,
  harvest, or stop

Use upstream **diagnosing-bugs** for the debugging loop. Do not let an agent
invent a root cause without a feedback loop.

## 7. Review Outcome and Evolve

At the agreed observation boundary, compare the actual outcome with the bet,
cost, risk, and externalities. End with one explicit decision:

- continue or scale
- iterate with a new bounded hypothesis
- rollback or remediate
- stop or retire
- change the product-engineering system

Use **agent-sync** to route durable evidence to its owning context, decision,
test, runbook, Skill, policy, or learning artifact. Do not maintain a parallel
AI-generated product memory.

When evidence changes domain meaning, update the owned ubiquitous language,
examples, invariants, contracts, and context map together with the implementing
slice. Do not let code, tests, and domain artifacts describe different models.

Read [references/operating-model.md](./references/operating-model.md) when
designing stages, metrics, exceptional paths, or L5-L7 agent ownership.

## 8. Expand Autonomy from Evidence

- At L1-L4, agents support bounded tasks, procedures, repository work, and
  grounded decisions.
- At L5, an agent workflow may coordinate a stable end-to-end procedure with
  state, recovery, evals, and exception handling.
- At L6, a governed agent system may operate a bounded value stream through
  production feedback under risk, policy, rollback, incident, and veto controls.
- At L7, agents may select signals, propose or run bounded experiments, and
  recommend investment changes only inside an accountable decision domain with
  trusted signals, budgets, kill criteria, audit, and a human stop path.

Expand one decision domain or risk class at a time. A capable agent does not
create product, security, legal, employment, financial, or strategic authority.
At department or company scale, explicitly connect product, engineering, data,
operations, support, customer success, sales, marketing, finance, security,
compliance, legal, and people responsibilities without erasing their distinct
accountability.

The loop is complete when signal, decision, slice, release, production evidence,
outcome, and next action are traceable; every artifact has an owner; and the
system learned without confusing activity, deployment, or agent output with
value.

## Related Skills

- **product-craft** - shape problems, opportunities, bets, and outcomes
- **integrate-product-compliance** - add confirmed control scope and evidence
- **build-autonomous-agents** - implement bounded product or SDLC agents
- **scaffold-distributed-context** - preserve DDD language and boundaries
- **coding-discipline**, **testing-strategies**, and upstream **tdd** - design
  and implement changeable slices through executable feedback
- **completion-gate** - verify before release or completion claims
- **agent-sync** - route durable production learning
- **scaffold-harness** - assess L1-L7 capability and oversight
