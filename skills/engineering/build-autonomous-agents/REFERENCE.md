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

Checked against the official Flue documentation and package metadata
(`@flue/runtime` and `@flue/cli`, npm `latest` dist-tag `2.1.1`) on 2026-09-28.
Flue 2.0 (2026-08-01) was a breaking rewrite of the `1.0.0-beta.9` line
reviewed previously: `defineAgent`, `defineWorkflow`, `invoke()`, and Actions
are gone entirely, not renamed. Resolve live versions again before adoption or
upgrade; a `2.2.0-next.1` prerelease exists on the `next` tag, do not adopt it
merely because it is newer.

Current public concepts:

| Concept | Use |
|---|---|
| `'use agent'` function | the agent is the exported, capitalized function itself; continuing stateful conversation |
| `defineTool` / `useTool` | bounded typed function available to the model (`harness: true` covers what Actions used to do) |
| `defineSubagent` / `useSubagent` | focused delegate with its own context; only its final answer returns |
| `init()` | get an application-owned handle to one agent conversation (scripts, cron, workflow steps) |
| `dispatch()` | submit a message to an agent conversation: `handle.dispatch()` returns a durable receipt, the top-level export fires channel or schedule input without waiting |

Important boundaries:

- Registration comes from a build-time `'use agent'` file scan, not a route
  export: any registered agent is reachable from server-side `dispatch(...)`
  with no mount at all. A mounted agent has no built-in authentication either;
  the conversation id is a caller-chosen path segment, not a secret, so the
  application owns both authentication and per-conversation authorization.
- A conversation id is not a credential; conversation history may contain
  sensitive inputs, results, and model activity.
- Flue does not prescribe the scheduler. Each target pairs its own cron
  mechanism with the same `dispatch()` surface; use a durable workflow engine
  (Cloudflare Workflows, Inngest, Temporal, or similar) when a multi-step
  script around several sends must itself survive a crash between steps.
- Durability covers one accepted submission end to end, not the script that
  issues it. A script that dies between two dispatches re-runs from its start
  unless each dispatch is checkpointed by a durable workflow engine.
- Virtual sandboxes are ephemeral and rebuilt on every recovery attempt, not
  network isolation. Local host sandboxes execute with host authority and are
  suitable only for trusted work.
- Conversation persistence (the database), workspace persistence (a durable
  sandbox adapter keyed on the agent instance id), and domain persistence are
  three separate design decisions; a durable database does not make a sandbox
  durable.
- The `'use agent'` scan registers every exported, capitalized function in any
  marked file. Keep tests and other non-agent code out of files carrying the
  directive.

Use the installed CLI documentation because public APIs changed across the
2.0 rewrite:

```bash
flue docs search "workflows"
flue docs read guide/workflows
flue docs search "durability"
flue docs search "sandboxes"
```

`flue docs read` also accepts the website URL or path directly
(`/docs/guide/durability/`, `guide/durability`), and reads from the locally
installed CLI, not the live site, so results match the installed version.
Use exact paths reported by `flue docs search`; do not assume the examples
above remain unchanged.

## Flue Migration Review

When reviewing an older integration, search for:

- `@flue/runtime/internal` (not a documented public boundary in any version)
- `defineAgent`, `defineWorkflow`, `invoke()`, or `defineAction`/Actions —
  removed in 2.0; an Action becomes a tool, commonly with `harness: true`
- removed configuration sentinels such as `model: false`
- direct in-process runtime bridges that bypass public `dispatch`, `init`,
  HTTP, or SDK boundaries
- model output applied without schema validation
- business persistence or credentials owned by the agent runtime
- test files accidentally carrying the `'use agent'` directive
- schedules or driving scripts assumed to survive process restarts without a
  durable workflow engine
- retries without idempotency protection
- mounted agent routes without resource-specific authentication and
  authorization on the conversation id

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
- [Flue durability](https://flueframework.com/docs/guide/durability/)
- [Flue sandboxes](https://flueframework.com/docs/guide/sandboxes/)
- [Flue schedules](https://flueframework.com/docs/guide/schedules/)
- [Flue channels](https://flueframework.com/docs/guide/channels/)
- [Flue evals](https://flueframework.com/docs/guide/evals/)
- [Flue observability](https://flueframework.com/docs/guide/observability/)
- [Flue CLI documentation](https://flueframework.com/docs/cli/docs/)
