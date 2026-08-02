---
name: backend-craft
description: Guides backend architecture, TypeScript boundaries, APIs, data models, PocketBase, Flue workflows, BullMQ queues, workers, AI integrations, provider secrets, security, tests, and operability. Use when designing or changing backend systems, runtime validation, migrations, job queues, workflow orchestration, LLM outputs, or deployment-sensitive code.
---

# Backend Craft

Use this for backend, data, AI workflow, queue, worker, TypeScript, security,
and platform changes.

## Project Fit Check

Before changing backend code:

1. Read repo instructions, ADRs, domain glossary, runbooks, package manifests,
   schemas, migrations, tests, and deployment notes.
2. Detect the actual runtime, framework, database, auth boundary, queue,
   workflow engine, and validation stack before applying technology-specific
   rules.
3. Apply PocketBase, Flue, and BullMQ sections only when the project uses those
   technologies or explicitly asks to adopt them.
4. If the project uses alternatives, translate the principles to the local stack
   instead of introducing PocketBase, Flue, or BullMQ by default.
5. If security or data ownership conventions are unclear, stop and identify the
   strongest existing boundary before implementing.

## Core Stance

- Backend code is where product promises become enforceable system behavior.
- TypeScript is not JavaScript with annotations; it is a way to make system
  boundaries, state, contracts, and failure modes visible.
- Runtime boundaries remain unsafe until validated. Compile-time safety does not
  replace input validation.
- Long-running or failure-prone work belongs in queues/workflows, not blocking
  request handlers.
- Use the boring reliable path unless complexity buys measurable leverage.
- Security, privacy, idempotency, observability, and rollback are design inputs,
  not cleanup tasks.

## Read First

1. Repo agent instructions and current changelog
2. Domain glossary and ADRs
3. Package manifests, scripts, tsconfig files, and runtime targets
4. Existing API contracts, schemas, repositories, migrations, hooks, and tests
5. Provider, queue, workflow, and deployment runbooks when relevant

Pair with `coding-discipline` for implementation and `completion-gate` before
claiming done when those Skills are available. This Skill remains usable on its
own.

## Architecture Defaults

- Validate at boundaries with Zod or an equivalent schema layer.
- Keep shared contracts in shared packages only when they cross package or app
  boundaries.
- Separate write DTOs, read models, domain models, and persistence records when
  they have different invariants.
- Keep business logic out of route glue.
- Prefer small deep modules over many pass-through wrappers.
- Make expected errors explicit and typed; unexpected errors are bugs.
- Persist provenance for AI or background actions when user trust depends on the
  result.

## End-to-end boundaries and data shape

- Keep user interfaces thin without turning them into passive renderers. The
  UI owns interaction and feedback; the backend owns reusable domain policy,
  authorization, durable decisions, and system invariants.
- Prefer task-shaped read models and intent-shaped mutation or command models
  over exposing persistence records or forcing every use case through generic
  CRUD.
- Do not add a generic repository abstraction by default. Keep domain language,
  query shape, authorization, concurrency, transactions, migrations, and
  observability visible at the boundary that owns them.
- Use hexagonal architecture, ports and adapters, CQRS, event-driven designs,
  or direct framework code only when the context benefits. None is a maturity
  requirement.
- Choose relational, document, graph, vector, or other storage from actual
  access patterns and operating constraints. Product vision matters, but do
  not buy speculative flexibility before evidence needs it.
- For a consequential choice, timebox a disposable spike and drive it with
  representative data volume and shape, concurrent clients, hot queries,
  retries and failures, memory, CPU, I/O, latency, recovery, migration, and
  cost. Keep the candidate only when the evidence and production hardening
  justify it.

## TypeScript Boundary Discipline

Use `unknown` at unsafe boundaries, then narrow:

- HTTP request bodies
- webhook payloads
- environment variables
- database records from loosely typed clients
- LLM outputs
- queue job payloads
- external API responses
- `catch` variables

Recommended strictness when the repo can support it:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "useUnknownInCatchVariables": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitReturns": true,
    "noUncheckedSideEffectImports": true
  }
}
```

Set `moduleResolution` from the stack, not habit:

- modern frontend/bundler apps: often `bundler`
- Node ESM without bundler: often `nodenext`
- legacy CommonJS: keep explicit and documented

Use advanced types only when they reduce real call-site complexity. Type-level
acrobatics that slow compilation or hide intent are a design smell.

## API And Data Rules

- Zod or equivalent at input boundaries.
- Stable error format with machine-readable code and human-readable message.
- Pagination, sorting, filtering, and limits must be explicit on list endpoints.
- Authorization belongs at the strongest available data boundary, not only in UI
  or route convenience code.
- Migrations need rollback or repair thinking, even when rollback is not
  automated.
- Data changes that affect access control need targeted tests.

## PocketBase Rules

When a project uses PocketBase:

- Treat collection API rules as the real authorization boundary.
- Use explicit, ownership-scoped rules for user data.
- Remember the footgun: `""` means public; `null` means superuser-only.
- Superuser auth is for trusted backends, migrations, and workers, not serving
  normal user requests.
- If rules can drift through Admin UI, keep a runtime reconciliation hook and the
  migration baseline in sync.
- Keep hooks syntax-checked and covered by targeted tests for security behavior.

## Flue And Workflow Rules

When a project uses Flue or similar workflow orchestration:

- Keep workflow input and output schemas explicit.
- Validate workflow/LLM output before persistence or side effects.
- Capture workflow name, version, step state, trigger, and job id when
  traceability matters.
- Keep deterministic workflow tests separate from files the workflow builder may
  discover as real workflows.
- Verify the installed Flue version and migration notes before copying patterns;
  beta APIs can move.
- Prefer attached/in-process invocation only when the project deliberately chose
  that runtime model.

## BullMQ And Worker Rules

- Job payloads should be compact: pass IDs, not large objects.
- Jobs must be idempotent. Retries and duplicate execution happen.
- Use explicit attempts, backoff, cleanup, concurrency, and timeout policy.
- Add failed and stalled job monitoring.
- Workers need graceful shutdown.
- Protect downstream services with conservative concurrency and rate limits.
- Do not await slow AI/background work in request handlers unless streaming is
  the product behavior.

## AI Backend Rules

- Separate system instructions from user content.
- Never interpolate untrusted input into privileged prompt instructions.
- Validate LLM output with schemas.
- Add retry/fallback behavior based on product criticality.
- Track token usage, latency, model/provider, and cost where it can matter.
- Prefer deterministic code over LLM calls for classification, parsing, or
  routing when deterministic code is clearer and safer.
- Stage or review meaning-changing AI results; auto-apply only low-risk,
  high-confidence operations with restore/undo/provenance.

## Provider And Secret Rules

- Never commit `.env` or print secrets.
- API keys and provider credentials come from environment or secret managers.
- Public config must be redacted.
- BYOK and managed-provider paths must be explicit and testable when both exist.
- Logs must not contain prompts, PII, or provider secrets unless the project has
  an explicit redaction policy.

## Verification

Choose checks by risk:

- typecheck for TypeScript contract changes
- unit tests for pure logic and schemas
- integration tests for repositories, migrations, auth, and queue handlers
- workflow fixture tests for AI/workflow behavior
- e2e or smoke tests for critical user-facing paths
- build checks for deployment-sensitive changes

## Red Flags

Stop and revise when you see:

- `any` escaping a boundary without justification
- LLM JSON parsed without schema validation
- auth enforced only in app code when a stronger data boundary exists
- a blank PocketBase rule
- superuser credentials used for a user-facing request
- large job payloads in Redis
- non-idempotent workers
- workflow side effects without provenance
- secrets printed in logs or returned in API responses
