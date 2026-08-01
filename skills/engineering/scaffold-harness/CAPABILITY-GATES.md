# Capability Gates: Context, Memory, and Discovery Tools

Use this gate whenever harness stewardship runs - not only when someone names
Graphify, Headroom, Context Mode, or a memory product.

Git-owned truth, checks, ADRs, Skills, and handoffs stay authoritative.
External tools improve findability, continuity, blast-radius analysis, or
context economy. They do not receive decision authority by default.

Detailed placement and economy rules live in
[CONTEXT-ARCHITECTURE.md](./CONTEXT-ARCHITECTURE.md). Distributed discovery
tools (Graphify, Zoekt, Sourcegraph, catalogs) also route through
`scaffold-distributed-context`.

## Always ask

On significant harness work, session start for a coordinator, or after repeated
friction, answer:

1. Which **information class** is failing (working, semantic, episodic,
   procedural)?
2. What is the **observed failure mode** (not a cool-tool desire)?
3. Does **Git + harness owners** already fix it if we improve them?
4. If not, which **smallest capability class** matches the failure?
5. What is the **authority, scope, read/write policy, and exit path**?
6. What **pilot evidence** would keep, change, or remove it?

If step 3 is yes, improve the owning artifact and stop. Do not add a service.

## Information-class tree

Run per class, not once for the whole agent:

1. Survive this turn? If no, keep it transient.
2. Survive this session? If no, working memory / short handoff is enough.
3. Stable fact vs event? Prefer semantic owners vs episodic records.
4. How retrieved later? Exact id, search, graph, or temporal query.
5. Promote to procedure? Only via reviewed Skill/script/check + evals.
6. Authority? `canonical` > `approved-reference` > `reviewed-learning` >
   `episodic-evidence` > `advisory-inference` > `raw-observation`.
7. Who may write and promote? Autonomous reads before autonomous shared writes.

## Failure mode to first candidate

| Observed failure | Prefer first | Not yet |
|---|---|---|
| Lost decisions / repeated failed fixes in one repo | Stronger LEARNINGS/STATUS/handoffs; then ProjectMem-class episodic log | Shared multi-tenant memory |
| Expensive re-exploration, symbol impact, blast radius | LSP/search; then Codemem-class code graph/memory | Org knowledge plane |
| Active context flooded by tool/file/web output | Context Mode (or RTK only if Context Mode unavailable) | Headroom as first move |
| Measured long-session / handoff request pressure after Context Mode | Headroom pilot | New memory product as substitute |
| Cross-repo relationship discovery is unreliable | CONTEXT-MAP + contracts; then Graphify/Zoekt/Sourcegraph-class index | Treating the graph as domain authority |
| Several agents need one bounded shared recall | Scoped memory service (Hindsight-class); curated writes | Global dump of all chats |
| Many sources, teams, ACLs, heterogeneous knowledge | Deferred until smaller scopes work; Cognee-class plane | Early platform build |
| "What was true when?" is recurring | Temporal graph (Graphiti-class) only with confirmed need | Default graph install |
| Procedures should improve from runs | Reviewed Skill promotion + evals; MemOS-class later | Unreviewed auto-evolution |

Default for a healthy L3 harness: **no new memory or graph product**. Stabilize
repository truth first.

## Progressive introduction

```text
Phase 0  Capture failure modes from real runs (no new service)
Phase 1  One repo, one failure mode (ProjectMem or Codemem class)
Phase 2  Optional shared-memory challenger on a curated corpus
Phase 3  Read-mostly shared service with source verification
Phase 4  Reviewed shared writes
Phase 5  Knowledge plane / temporal graph only with platform ownership
Phase 6  Adaptive procedural learning only with evals + rollback
```

Autonomous **reads** of approved scopes may come before autonomous **writes**.
Never auto-publish model inference as shared or canonical truth.

## Adoption record (minimum)

Before installing or enabling a capability, record in the target LEARNINGS,
STATUS, or an ADR:

- failure mode and frequency
- information classes in scope
- candidate and license
- read/write/approve scopes
- pilot tasks and success signals
- export/delete/rollback path
- decision: START | CONTINUE | CHANGE | REMOVE | PARK

## Stewardship checklist (copy into loops)

- [ ] Failure mode is observed, not speculative
- [ ] Git/harness owners considered first
- [ ] Capability class matched (economy vs episodic vs code-graph vs shared
      memory vs knowledge plane vs temporal)
- [ ] Authority order preserved
- [ ] Pilot + exit path defined
- [ ] Human README / TOOLS / CONTEXT-MAP updated if the operator surface changes

## Sources

Research digest checked 2026-07-30 (owner research on agent memory candidates).
Re-check licenses, MCP support, and primary docs before any install. Product
pages and repos change; this file owns the **gate**, not frozen vendor claims.
