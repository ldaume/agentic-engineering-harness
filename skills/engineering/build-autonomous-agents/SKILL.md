---
name: build-autonomous-agents
description: Designs and implements bounded autonomous agent systems for product features and software or product SDLC automation with runtime-neutral contracts. Use when building an agent, finite workflow, subagent, scheduled or overnight job, CI agent, chat or channel integration, observable agent service, adding Flue to an application, or migrating an older Flue integration.
---

# Build Autonomous Agents

Build the smallest autonomous system that can produce and verify the intended
outcome. Keep the workload contract portable even when Flue is the selected
runtime.

## 1. Ground the Workload

Read the target's instructions, domain context, architecture, tests, delivery
controls, security boundaries, and existing runtime integration.

State:

- the user or operational outcome
- whether the workload is a product capability or SDLC automation
- trigger, owner, input, output, and completion condition
- allowed data, tools, repositories, network access, secrets, and side effects
- required human approval, cancellation, and rollback points

First test whether deterministic code, an existing application service, a
script, or a CI job can solve the problem. Do not add an agent when those are
sufficient.

## 2. Select the Smallest Unit

| Need | Unit |
|---|---|
| Deterministic operation | Function or application service |
| Bounded capability the model may call | Tool |
| Reusable application-controlled orchestration | Action |
| Finite inspectable operation | Workflow |
| Continuing stateful interaction | Agent |
| Focused separable responsibility | Subagent |

Use a subagent only when its independent context, tools, or evaluation boundary
improves the result enough to justify delegation.

## 3. Write the Execution Contract

Define before implementation:

- validated input and output schemas
- model-visible context, Skills, and tools
- deterministic validation and application of results
- work identity, deduplication key, state owner, and retention
- isolation and permission boundary
- timeout, token or spend budget, concurrency, and stop condition
- retry, idempotency, recovery, duplicate-effect handling, and failure owner
- durable checkpoint, next wake condition, progress deadline, and reconciliation
- eval cases, telemetry, alerts, and incident owner

Separate probabilistic judgment from deterministic effects. Prefer a typed
proposal that application code validates and applies over letting model output
mutate business state directly.

## 4. Select and Verify the Runtime

Use the target's existing runtime when it meets the contract. For a TypeScript
system that needs a harness-first agent runtime, Flue is the current default
candidate, not part of the product contract.

Before adopting or changing Flue:

1. Detect the installed version, package manager, deployment target, and
   existing integration.
2. Use the installed CLI's `flue docs search` and `flue docs read` commands
   first because those docs match the installed version.
3. Check official upstream docs, changelog, package metadata, and types when
   adopting or upgrading.
4. Prefer the latest reviewed stable release. Do not adopt a nightly merely
   because it is newer.
5. Read [REFERENCE.md](./REFERENCE.md) for current Flue boundaries and migration
   hazards.

Do not copy imports from `@flue/runtime/internal`; they are not a portable
public integration boundary.

## 5. Implement One Vertical Slice

For a product capability:

- keep authentication, authorization, business data, provider credentials,
  persistence, and application of results application-owned
- expose meaningful queued, running, review, success, and failure states
- make any consequential result reviewable before application where risk
  requires it

For SDLC automation:

- pin the repository revision and use an isolated worktree or sandbox
- grant the minimum repository, network, and secret permissions
- produce a reviewable patch, report, or other bounded artifact
- run the repository's Fast Check and relevant Full Gates
- never merge, deploy, or publish without explicit authority

Start deterministic seams with a failing behavior test and agent judgment with
a representative failing eval case. Implement the narrowest path from input
through verified outcome before adding channels, schedules, subagents, or
generalized abstractions.

## 6. Prove Safety and Recovery

- Treat local host execution as trusted execution, not isolation.
- Keep conversation state, workspace state, and business state distinct.
- Do not assume an interrupted finite workflow resumes at an arbitrary
  TypeScript step.
- Persist every useful increment and the next eligible action outside the live
  model session. Every routine non-terminal state must have a wake condition or
  a reconciler that owns progress; a human prompt is not a scheduler. A required
  human response waits on a durable correlated event with a deadline and
  escalation; it is never inferred or auto-approved.
- Detect expired claims and missed progress deadlines. Inspect retained state
  and external effects before a bounded requeue; alert the named failure owner
  when safe recovery is not possible.
- Put external side effects behind application-owned idempotency keys.
- Use a durable external orchestrator when step-level resumability is required.
- Keep model-visible data, logs, traces, and run history free of unnecessary
  secrets and personal data.

## 7. Evaluate and Observe

Test representative success, refusal, malformed output, tool failure, timeout,
retry, duplicate delivery, cancellation, and permission-denied cases. Assert
schemas, tool calls, side effects, latency, and cost where relevant.

Emit enough structured evidence to answer:

- what triggered the run
- which version and configuration ran
- what tools and effects occurred
- why it stopped
- whether the outcome passed deterministic checks and evals

Complete the work only when the bounded outcome works end to end, failure and
recovery behavior is demonstrated, permissions and budgets are explicit, and
the runtime can be replaced without changing the product contract. An idle
system has no admissible signal; a paused, blocked, or partial run exposes its
reason, owner, retained checkpoint, and next wake or escalation condition.

## Related Skills

- **scaffold-harness** - assess maturity and runtime need
- **coding-discipline** - implement the smallest safe change
- **completion-gate** - verify before claiming completion
- **product-craft** - define product value and human oversight
- **scaffold-distributed-context** - coordinate contracts across repositories
- upstream **tdd** - drive deterministic seams from behavior
