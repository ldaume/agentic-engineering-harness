# Agent Context Architecture

## Objective

Make the right evidence available at the right time, shape, authority, and
cost. Context architecture covers knowledge placement, retrieval, persistence,
actions, and context economy; it is not a synonym for a large context window.

Optimize cost, latency, and risk per correctly completed task. A lower token
count is useful only when task success, grounding, verification, and recovery
stay at least as strong.

## Design Dimensions

Classify every important source or capability:

| Dimension | Question |
|---|---|
| Authority | Which system owns the truth, and who may change it? |
| Freshness | How quickly can it change, and what invalidates a cached result? |
| Availability | Must work continue offline or when the external system fails? |
| Locality | Is it versioned locally, projected locally, indexed, or remote-only? |
| Shape | Does the consumer need concise Markdown, typed JSON, a schema, a graph, a diff, or binary content? |
| Granularity | What is the smallest useful resource, query, symbol, issue, page, or contract? |
| Activation | Is it always needed, branch-specific, retrieved by query, or invoked as an action? |
| Persistence | Is it session state, durable project truth, a decision, a learning, or a rebuildable cache? |
| Control | Is the behavior probabilistic guidance or deterministic enforcement? |
| Access | Which identity, permissions, secrets, tenant, and audit boundary apply? |
| Economics | What context load, latency, retries, failure impact, and maintenance does it add? |
| Verification | How can an agent or human detect stale, incomplete, or incorrect context? |

Choose placement after these dimensions are known. File format alone does not
establish authority or freshness.

## MCP's Role

MCP standardizes how a host connects to servers that expose resources, prompts,
and tools. It makes external context and capabilities reachable; it does not
decide:

- which source is authoritative
- what belongs in the active model context
- when information should be fetched or refreshed
- what persists across sessions
- whether a remote result becomes repository truth
- how Rules, Skills, Hooks, memory, or RAG use the result
- which external action is authorized

Resources provide contextual data, prompts provide reusable interaction
templates, and tools retrieve information or perform actions. The host still
owns context aggregation, permissions, consent, and model interaction.

Treat tool and server descriptions as routing hints, not trusted proof. Tool
discovery and schemas also consume context, so expose the smallest relevant
server and capability set for the active workspace.

## Placement Model

| Placement | Best fit | Required metadata or control |
|---|---|---|
| Local versioned artifact | Stable, high-reuse, session-critical truth such as domain language, contracts, accepted decisions, commands, and checks | Owner, review path, Git history |
| Local projection of an external source | Remote truth is needed reliably across sessions or by deterministic checks | Source URI, source revision or timestamp, checked-at, expiry or refresh trigger, owner, sync command |
| On-demand MCP resource or read tool | Volatile, access-controlled, large, or infrequently used information | Narrow query, permissions, freshness evidence, pagination, failure handling |
| MCP action tool | A live external mutation is required | Explicit authority, preview or proposal when possible, validation, idempotency, audit, recovery |
| RAG, code graph, or search index | Discovery and retrieval across material too large for direct loading | Rebuild path, source revision, access boundary; never treat the index as authority |
| Session memory or workflow state | Temporary progress, resumability, or bounded execution state | Scope, retention, identity, recovery, deletion |

Keep stable routing and essential project truth local. Fetch live status and
perform actions only when the current task needs them. Local-first does not mean
copy everything: it means the agent can begin correctly without rediscovering
the operating system through remote calls.

## Repository Context Stack

| Concern | Typical owner |
|---|---|
| Stable agent scope, language, permissions, and routing | Concise `AGENTS.md` or local equivalent |
| Domain language, invariants, and confirmed distinctions | `CONTEXT.md` or canonical domain source |
| Source authority and relationships | `CONTEXT-MAP.md` |
| Accepted consequential decision | ADR |
| Repeated probabilistic procedure | Skill |
| Scoped behavioral guidance | Rule or agent instruction |
| Deterministic event or enforcement | Hook, test, CI, policy, or platform control |
| Durable evidence-backed observation | `LEARNINGS.md` |
| Large-scale discovery | Search, RAG, or graph derived from named sources |
| Live external information or action | Narrow MCP resource or tool |

MCP is one delivery mechanism in this stack, not the stack itself.

## Session Pattern

1. Load concise local routing and the smallest canonical local sources.
2. Determine the task branch and identify missing evidence.
3. Query local code, contracts, and projections at the lowest sufficient
   resolution.
4. Use MCP only for required live information or external action.
5. Keep transient results transient. Route accepted decisions, changed
   contracts, and durable learnings to their owning artifacts.
6. Refresh projections from their source trigger rather than on every prompt.

The session is grounded when the agent knows what is local, what is derived,
what must be fetched live, and which source wins on conflict.

## Context Economy Ladder

Stop at the first reliable rung:

1. Query the smallest authoritative source with repository search, an LSP, or
   semantic symbol navigation.
2. Batch independent reads and commands. Process large results outside the
   model context and return only the derived evidence.
3. Keep stable instructions concise. Disclose branch-specific references,
   templates, and examples only when that branch runs.
4. Pass bounded evidence and decisions between agents, not chat transcripts.
5. Use one filtering or compression layer for the affected data path.
6. Add request-level compression only after the remaining context pressure is
   measured.

Preserve exact errors, relevant code, sources, and verification evidence.
Omitted detail needs a retrieval or re-query path when it could change the
decision.

## Context Tool Roles

| Capability | Use when | Boundary |
|---|---|---|
| Native search, LSP, or semantic navigation | The needed fact can be resolved precisely from code or a small source | Not a substitute for cross-repository ownership or external evidence |
| Context Mode | Large files, tool output, web results, logs, or repeated reads would flood the active context | Process or index raw material outside the active context and surface only relevant evidence |
| RTK | Context Mode is unavailable and a small set of known shell commands produces noisy output | A CLI filter only; it does not manage files, APIs, session continuity, or request history |
| Headroom | Long sessions, large histories, repeated agent handoffs, or a controlled gateway still have measured request-context pressure | Pilot routing, quality, cache behavior, retrieval, privacy, and failure handling before adoption |
| Code graph / impact memory (Codemem-class) | Re-exploration and blast-radius analysis are repeatedly expensive after native search | Index is discovery, not architecture authority |
| Repo episodic memory (ProjectMem-class) | Decisions and failed attempts are lost across sessions despite LEARNINGS/STATUS | Local event log; not a shared org brain |
| Shared memory service (Hindsight-class) | Several agents need one bounded, curated recall scope | Reads before shared writes; inference is advisory |
| Relationship discovery (Graphify / Zoekt / Sourcegraph-class) | Cross-repo or large-codebase relationship lookup fails with maps alone | Never promote graph output to domain truth |
| Knowledge plane / temporal graph | Confirmed multi-team, ACL, or "what was true when" needs | Deferred until smaller scopes work |

For the full failure-mode matrix, promotion phases, and adoption record, use
[CAPABILITY-GATES.md](./CAPABILITY-GATES.md). Run that gate during stewardship
even when no tool was requested.

Headroom memory, Context Mode indexes, RAG stores, and compression caches are
operational stores, not the sole authority for durable product or architecture
truth.

## Audit, Propose, or Apply

Match action to authority:

- **Audit:** map sources, data paths, dimensions, context load, failure modes,
  and gaps without changing the target.
- **Propose:** present the smallest viable option plus alternatives,
  trade-offs, permissions, reversibility, and expected evidence.
- **Apply:** configure only the accepted repository or host scope, preserve
  passthrough and rollback, and verify the full path with representative work.

Global installation, credentials, remote writes, broader data access, and
shared gateways require their normal authority.

## Adoption Gate

For an MCP server, projection, RAG layer, or context-economy tool:

1. Identify the observed context, freshness, availability, or cost failure.
2. Confirm the canonical source, consumer, host integration, and exact data
   path.
3. Define representative tasks and a disconnected, passthrough, or removal
   path.
4. Check schemas, pagination, permissions, storage, retention, tenant
   boundaries, secrets, telemetry, and supply-chain ownership.
5. Measure task success, first-pass checks, tokens, latency, retries, tool
   failures, review findings, and recovery.
6. Keep, change, or remove the mechanism from the evidence.

Adoption is complete only when source authority and freshness are visible,
routing is verified end to end, omitted detail remains recoverable where
required, and successful-task economics improve without a material quality or
security regression.

## Current Primary Sources

Checked on 2026-07-30. Re-open before installation or configuration:

- [MCP architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)
- [MCP resources specification](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)
- [MCP tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
- [Context Mode repository](https://github.com/mksglu/context-mode)
- [RTK repository](https://github.com/rtk-ai/rtk)
- [Headroom repository](https://github.com/headroomlabs-ai/headroom)
- [Headroom proxy documentation](https://headroomlabs-ai.github.io/headroom/proxy/)
