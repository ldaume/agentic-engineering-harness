# Member or consumer sync

Use in a coordinating repository when several repos must discover shared
oversight without copying local truth.

## Discovery

Each listed member `AGENTS.md`, including experiments, should point at this
coordinator and require a read of its `HARNESS.md` (and sync doc) before
substantial work. Keep the pointer thin; do not paste full policy into members.

This sync document is the stable member route to the coordinator's canonical
`CONTEXT-MAP.md`. Before a member selects another working root, shared source
owner, or cross-repository scope, route it to the local map and a stable remote
fallback such as `<stable-coordinator-context-map-url>`. Do not add a parallel
`HARNESS-MAP.md`.

When members share a canonical Private system snippet, Full Gates should detect
drift between that snippet and every listed member section. Session discovery
does not grant unattended autonomy.

## Working root

| Work | Open |
|---|---|
| Local product / ops change | that member |
| Membership, autonomy policy, cross-repo STATUS | this coordinator |
| Portable Skill source files | the Skills catalog |
| Multi-member Skill placement / hygiene | this coordinator first |

A Skills catalog is a capability supplier, not this control plane.

## Shared capability sources

The coordinator owns approved public and private organization or team sources,
compatibility and adoption policy, and allowed version ranges when needed.
Each consuming project owns its exact ref and resolved commit in its target
manifest; the source catalog owns release metadata. The coordinator does not
copy Skill text. Projects retain local wrappers, domain semantics, commands,
checks, and permissions. Keep only a small bootstrap global and let the active
host's verified precedence determine how sources are loaded.

## Admit or graduate a member

Compose member-local `scaffold-harness` with coordinator inventory:

1. Create or open the sibling; give it a local agent entrypoint immediately and
   name the available Fast Check / Full Gates without inventing missing checks.
2. Add a `CONTEXT-MAP.md` row (`experimental` until git, checks, and pointer
   exist).
3. Copy the canonical Private system snippet into the member `AGENTS.md`.
4. Update volatile `STATUS.md` while mid-flight.
5. Run coordinator Full Gates; commit coordinator and member separately.

## Sibling awareness

Keep the member map truthful. Coordinator verify should fail on missing mapped
paths and on unlisted repo-like siblings beside the coordinator. Member
sessions read the context map before choosing another repository, then
deep-dive siblings only when work crosses repositories.

## Fan-out checklist (same loop)

| Kind of change | Fan-out required? | Same-loop actions |
|---|---|---|
| Coordinator policy only (`HARNESS.md`, sync prose, learnings, status) | No member file edits | Members pick it up via the pointer next session. |
| Discovery / snippet / session entry obligations | Yes | Update the canonical snippet, refresh every listed member Private system section, run Full Gates. |
| Portable harness default for future scaffolds | Yes (catalog) | Also update `scaffold-harness` templates / `agent-sync`. Templates do not auto-rewrite live members. |
| Member-local harness only | No siblings | Keep it local unless a second member needs the same fact. |

Parent sessions own fan-out after subagent work. No standing sync daemon.

## Write-back

Route cross-cutting durable changes to owners here (`CONTEXT-MAP.md`,
`HARNESS.md`, `STATUS.md`, `LEARNINGS.md`). Keep member product facts in the
member. Prefer hard adaptations over soft memory when the lesson is a rule.

For multi-team systems, route domain and implementation decisions to the owning
team; route shared policy, public contract relationships, compatibility state,
and cross-team escalation to the coordinator. Version shared Skills and policy
so teams can adopt them with explicit compatibility evidence.
