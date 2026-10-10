# Agent Context Architecture

## Objective

Make the right evidence available at the right time, shape, authority, and
cost. Context architecture covers knowledge placement, retrieval, persistence,
actions, and context economy; it is not a synonym for a large context window.

Optimize cost, latency, and risk per correctly completed task. A lower token
count is useful only when task success, grounding, verification, and recovery
stay at least as strong.

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

MCP is one delivery mechanism in this stack, not the stack itself. Classify
each source's authority, freshness, and access before choosing where it lives,
because file format alone does not establish either.

## Startup Context Budget

The unconditional payload is the cost every session pays before work starts, so
measure it instead of estimating it. Sum, in bytes:

- the entry chain: `CLAUDE.md`, `AGENTS.md`, local untracked notes such as
  `CLAUDE.local.md`, every @-import, and the same files in parent directories
- the stdout of each session-start hook
- plugin and Skill listings (name plus description of every installed Skill)
- tool lists, including MCP tool schemas

Then set a byte budget per part from those numbers, a little above today's
measured chain, so growth fails loudly instead of drifting. Put a small
dependency-free script in the repository's fast check that reads the chain
(following imports, each file once), runs the repository's session-start hooks
and counts their stdout, and exits non-zero over budget with a per-file
breakdown. Host-local inputs such as user settings do not exist in CI; run that
check only where they do. Add the Startup Context Budget section to the target
`HARNESS.md`.

Keep every hook output under the host's inline limit (Claude Code persists a
larger hook output to a file and shows the agent a 2 KB preview, so the bytes
are paid and not seen). Hooks print a pointer and Skill names; Skills and
reference documents load on demand, behind a trigger. When a part is over
budget, move branch-specific text to a document the entry file links by
section, shorten the listing descriptions, or drop the part. The numbers
belong to the repository that measured them: record the measurement date and
values next to the budget, and do not copy another repository's limits.

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

When a context, memory, or discovery tool is proposed, run
[CAPABILITY-GATES.md](./CAPABILITY-GATES.md) first.
