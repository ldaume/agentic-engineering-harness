# Autonomous Agent Runtime Reference

## Contents

- [Portable Architecture](#portable-architecture)
- [Product Capability Pattern](#product-capability-pattern)
- [SDLC Automation Pattern](#sdlc-automation-pattern)
- [Flue Implementation Notes](#flue-implementation-notes)
- [Flue Migration Review](#flue-migration-review)
- [Verification Checklist](#verification-checklist)
- [Primary Sources](#primary-sources)

## Portable Architecture

Keep these layers independent:

1. **Workload contract:** outcome, trigger, schemas, authority, budgets, and
   completion.
2. **Domain application:** authentication, business rules, persistence, and
   deterministic side effects.
3. **Agent harness:** context, model, Skills, tools, workspace, and delegation.
4. **Execution runtime:** admission, state, scheduling, recovery, and delivery.
5. **Evidence:** evals, checks, traces, costs, and human decisions.

The runtime may implement several layers, but it does not become the authority
for product semantics or consequential business decisions.

## Product Capability Pattern

```text
authenticated request or event
  -> application validates authority and input
  -> agent or workflow produces typed proposal
  -> application validates proposal and current domain state
  -> human approval when risk requires it
  -> deterministic application service applies an idempotent effect
  -> product records outcome and operational evidence
```

Prefer an asynchronous workflow for finite transforms, reviews, or generation.
Use a continuing agent when later messages or events must share one canonical
conversation. Keep provider secrets behind an application-owned gateway or
adapter; never place raw credentials in prompts, tool results, or run history.

Product UI should expose the states a user can act on. A generic spinner hides
queues, partial failure, review needs, and stale results.

## SDLC Automation Pattern

```text
trusted trigger
  -> immutable repository revision
  -> isolated workspace with bounded tools and credentials
  -> agent produces patch or report
  -> Fast Check and relevant Full Gates
  -> review or policy gate
  -> authorized merge, release, or no action
```

The scheduler should own admission, concurrency, deadlines, cancellation,
retention, and notifications when it already provides them. An overnight
window is a schedule, not an authorization expansion. The job still needs a
bounded objective, budget, stop condition, and recoverable artifact.

## Flue Implementation Notes

Checked against the official Flue documentation and package metadata on
2026-07-30. The reviewed stable package line was `1.0.0-beta.9`; upstream also
published newer nightlies. Resolve live versions again before adoption or
upgrade.

Current public concepts:

| Concept | Use |
|---|---|
| `defineAgent` | continuing stateful context |
| `defineWorkflow` | finite operation with run, result, and event history |
| Action | reusable application-controlled input, output, and handler |
| Tool | bounded typed function available to the model |
| `invoke()` | start a workflow from application-owned code |
| `dispatch()` | continue a persistent agent conversation |

Important boundaries:

- A discovered workflow is private unless its route or run access is explicitly
  exported and authenticated.
- A run identifier is not a credential; run data may contain sensitive inputs,
  results, and model activity.
- Flue does not prescribe the scheduler. Use the platform scheduler or a durable
  queue when production recovery, replicas, or step orchestration require it.
- Continuing agent persistence and finite workflow recovery are different.
  Do not assume arbitrary TypeScript workflow execution is checkpointed.
- Virtual sandboxes are not network isolation. Local host sandboxes execute
  with host authority and are suitable only for trusted work.
- Conversation persistence, workspace persistence, and domain persistence are
  separate design decisions.
- Keep tests outside directories whose files are auto-discovered as workflows
  or agents unless the installed version documents a safe convention.

Use the installed CLI documentation because public APIs changed during beta:

```bash
flue docs search "workflows"
flue docs read guide/workflows
flue docs search "durability"
flue docs search "sandboxes"
```

Use exact paths reported by `flue docs search`; do not assume the examples above
remain unchanged.

## Flue Migration Review

When reviewing an older integration, search for:

- `@flue/runtime/internal`
- removed configuration sentinels such as `model: false`
- direct in-process runtime bridges that bypass public `invoke`, `dispatch`,
  HTTP, or SDK boundaries
- model output applied without schema validation
- business persistence or credentials owned by the agent runtime
- test files accidentally placed in discovered module directories
- schedules assumed to survive process restarts
- retries without idempotency protection
- exposed workflow or run routes without resource-specific authentication

Do not rewrite a working integration from memory. Compare its installed docs,
types, tests, and changelog; migrate one representative vertical slice and
retain a rollback path.

## Verification Checklist

- A deterministic solution was considered first.
- The selected unit is no larger than the workload.
- Input, output, authority, budget, timeout, and stop condition are explicit.
- Product and runtime contracts are separate.
- Application code owns authentication and consequential side effects.
- Untrusted execution is isolated; trusted local execution is named as such.
- Retries and duplicate delivery cannot repeat harmful effects.
- Representative evals and deterministic checks cover the outcome.
- Traces and run records are access-controlled and sanitized.
- Cancellation, recovery, rollback, and incident ownership are demonstrated.
- Current runtime version, public API, license, and deployment path are
  re-verified.

## Primary Sources

- [Flue repository and Apache-2.0 license](https://github.com/withastro/flue)
- [Flue workflows](https://flueframework.com/docs/guide/workflows/)
- [Flue agents](https://flueframework.com/docs/guide/building-agents/)
- [Flue durable execution](https://flueframework.com/docs/concepts/durable-execution/)
- [Flue sandboxes](https://flueframework.com/docs/guide/sandboxes/)
- [Flue schedules](https://flueframework.com/docs/guide/schedules/)
- [Flue channels](https://flueframework.com/docs/guide/channels/)
- [Flue evals](https://flueframework.com/docs/guide/evals/)
- [Flue observability](https://flueframework.com/docs/guide/observability/)
- [Flue CLI documentation](https://flueframework.com/docs/cli/docs/)
