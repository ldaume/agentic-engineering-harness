# Agent Runtime Reference

## Purpose

Use this reference when a target needs agents outside an interactive coding
session: CI or delivery jobs, scheduled or overnight work, durable services,
specialist agents, chat channels, or production observability.

An agent framework is not a default harness layer. First check whether the
existing agent CLI, CI scheduler, scripts, and repository controls already run
the bounded task reliably.

This reference selects a runtime. Use **build-autonomous-agents** to define and
implement the portable workload contract after the gate passes.

## Runtime Gate

Adopt a runtime only when the target names:

- a repeated job or continuing interaction
- owner, trigger, input, output, and completion condition
- allowed repositories, tools, network, secrets, and side effects
- isolation, maximum duration, token and spend budget, and concurrency
- retry, idempotency, recovery, rollback, and cancellation
- deterministic checks and outcome evals
- observability, audit, alerting, and incident ownership
- human approval and stop points

Do not run an open-ended "overnight agent." Run a bounded workflow during an
overnight window.

## Smallest Execution Choice

| Need | First choice |
|---|---|
| One finite repository task | Existing agent CLI or script under local checks |
| Finite CI or scheduled task | CI workflow with explicit timeout, permissions, artifact, and failure state |
| Reusable typed agent workflow | Flue workflow or equivalent after a representative pilot |
| Continuing conversation or event-driven agent | Authenticated agent service with durable state |
| Specialized subagent inside a durable application | Eve, Flue, or the existing runtime only when task isolation and evals justify it |
| Organization-wide autonomous delivery | L6 controls in [MATURITY.md](./MATURITY.md), not a framework installation |

Prefer the first row that meets the need. Keep scheduling in the existing
platform when it already provides triggers, concurrency, secrets, cancellation,
retention, and audit.

## Open-Source-First Gate

Before calling a runtime open-source and portable:

1. Verify the current license of the framework and every required adapter.
2. Prove the required path without a mandatory managed control plane.
3. Run a self-hosted smoke test using target-owned compute, persistence, and
   sandboxing.
4. Confirm state, logs, eval data, and configuration can be exported and
   restored.
5. Keep model, sandbox, persistence, channel, and telemetry dependencies
   replaceable where the workload requires portability.
6. Record security maintenance, upgrade, backup, and incident ownership.

No software license fee does not mean zero operating cost. Model inference,
compute, storage, network traffic, observability retention, and external
channel providers may still cost money. Record both monetary and operational
cost.

## Flue

Current fit: primary candidate for TypeScript teams that need a harness-first
runtime across local execution, Node.js, containers, CI, or other documented
targets.

Relevant capabilities include:

- finite workflows for background, review, and CI work
- continuing agents and subagents
- typed tools, actions, inputs, and outputs
- local or remote sandbox adapters
- schedules and channel integrations
- runtime events and OpenTelemetry-compatible observability
- Node.js deployment that can run in a container, VM, CI runner, or managed
  service

The upstream repository is Apache-2.0. Verify the current Flue version,
required adapters, and deployment target before adoption; framework and
integration APIs can change.

For CI, use the runner as the isolation boundary only when that is an explicit
security decision. Grant the minimum job permissions and secrets, validate
structured output, retain useful run evidence, and let deterministic CI gates
decide whether a result may proceed.

## Eve

Current fit: bounded pilot candidate for filesystem-first durable agents,
specialist subagents, schedules, human approvals, sandboxed execution, evals,
and multi-channel delivery.

Eve's framework repository is Apache-2.0. Current upstream material documents a
self-hosted path using replaceable backends, Postgres-backed durability, Docker
sandboxing, and target-owned deployment, so Vercel hosting is not technically
required for that path.

Eve is currently beta. Before production use:

- verify the exact packages and beta terms that apply
- prove the complete self-hosted path without required Vercel services
- test upgrades, state migration, recovery, and adapter replacement
- evaluate a specialist agent against known tasks and a simpler alternative
- keep a removal or migration path

Do not adopt Eve only because subagents are available. A specialist agent needs
a narrow responsibility, bounded tools, representative evals, budget, stop
condition, and a parent that can verify and integrate its result.

## Scheduled and Overnight Work

Every scheduled run should declare:

- immutable input revision and working branch or isolated workspace
- maximum runtime, model and spend budget, and concurrency policy
- idempotency key or duplicate-run behavior
- checkpoint or resumability requirement
- allowed side effects and approval gates
- Fast Check, Full Gates, and artifact retention
- success, partial success, blocked, and failed states
- notification and human takeover path

Default to a proposed change or report. Do not auto-merge, deploy, publish, or
write to external systems unless the target explicitly grants that authority
and its deterministic gates, rollback, and oversight are proven.

## Chat and Channels

Treat chat as an external trust boundary:

- verify provider signatures and map external identity to local authority
- isolate tenants, repositories, sessions, and secrets
- define which messages can trigger tools or side effects
- defend against prompt injection through messages and retrieved content
- rate-limit, redact, retain, and delete according to target policy
- require approval for consequential actions
- provide visible cancellation and escalation

Channel availability does not establish authentication, authorization, or safe
tool access.

## Observability

Capture only what changes operation or evaluation:

- run, session, parent, worker, tool, and source-revision correlation
- model and provider, latency, retries, usage, and cost
- tool inputs and results after secrets and sensitive data are redacted
- checkpoints, approvals, policy decisions, errors, and stop reasons
- deterministic gate and outcome-eval results

Prefer OpenTelemetry or another target-owned export path over a mandatory
vendor dashboard. Define retention, access, sampling, redaction, alerting, and
incident ownership before production traffic.

## Current Primary Sources

Checked on 2026-08-01. Re-open at adoption:

- [Flue repository and license](https://github.com/withastro/flue)
- [Flue design and deployment principles](https://flueframework.com/docs/introduction/why-flue/)
- [Flue workflows](https://flueframework.com/docs/guide/workflows/)
- [Flue agents and subagents](https://flueframework.com/docs/guide/building-agents/)
- [Flue Agent API](https://flueframework.com/docs/api/agent-api/)
- [Flue on GitHub Actions](https://flueframework.com/docs/ecosystem/deploy/github-actions/)
- [Flue runtime events](https://flueframework.com/docs/api/events-reference/)
- [Eve repository, license, and beta status](https://github.com/vercel/eve)
- [Eve managed and self-hosted architecture](https://eve.dev/)
- [Vercel's Eve introduction](https://vercel.com/blog/introducing-eve)

These sources establish candidates, not target approval. Use
[CURRENTNESS.md](./CURRENTNESS.md) to record live versions, terms, costs, and
representative evidence.
