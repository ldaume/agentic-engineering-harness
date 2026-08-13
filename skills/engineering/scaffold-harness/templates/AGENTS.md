# Agent Instructions

## Start

- Before substantial work, use the **current** harness contract and pinned
  Skills: `git fetch` origin and read `HARNESS.md` from the origin default
  tip or remote canonical file, not a task worktree cwd. Ff-only a clean
  primary when behind origin; if blocked, leave it. Confirm managed Skill
  copies match the origin pins before following them. Do not skip this because
  the task looks small. Leave the repository clean in the same loop. Host
  user-rules lose for currency, autonomy, and git close-out.
- Use `CONTEXT-MAP.md` when present to select only the additional sources
  needed for the current task. Load `README.md` for human orientation, not as
  an unconditional agent prerequisite.
- Follow the nearest scoped agent instructions.
- Communicate in the current human's preferred collaboration language. Infer
  it from explicit preference or conversation evidence; if still unclear, ask
  once and retain it in user-scoped or untracked state unless it is shared
  repository policy.
- Discover the active host and effective instruction, Skill, plugin, Rule,
  Hook, MCP, permission, model, and isolation behavior before relying on a
  host-specific adapter.
- Before creating or changing a Skill, resolve and follow the managed
  `write-a-skill` Skill. Use a host-native creator only for native metadata,
  scaffolding, or validation after the portable behavior contract is clear.
- Before editing: run `git status --short --branch` and, when available,
  `git worktree list`; preserve foreign WIP; then apply **Git Working Tree
  Hygiene** in `HARNESS.md` (branch gate; worktree default; ordinary names; no
  agent/tool producer chrome in commits or PR/MR surfaces; claim each edit
  checkout - worktree or primary - with `.agent-lease` + STATUS lease; one
  lease row per repo in multi-repo sessions; never share a path/branch under a
  foreign `active` lease; never delete another agent's live worktree).
- Use existing repository conventions and commands before adding new ones.

## Harness

- Load the relevant `HARNESS.md` sections when work touches stewardship,
  authority, review, context architecture, or completion; improve the smallest
  owning artifact when current work provides evidence.
- Before finish: ask whether durable lessons must manifest in this harness
  and, after every harness change, whether a generalized portable variant
  belongs in a catalog you own or are authorized to change. Apply that port in
  the same loop when authorized. Do not push, PR, or otherwise write back to
  an external public upstream you only consume. Ask only when placement is
  ambiguous or the port would leak private authority.
- Establish shared understanding for significant work. Use
  `grill-harness-with-docs` for unresolved material decisions in any topic.
- Keep stable instructions here and reference detailed sources.

## Commands

| Task | Command |
|---|---|
| Fast Check | `<smallest reliable command for narrow changes>` |
| Full Gates | `<test, lint, typecheck, build, or repository verify command>` |

## Boundaries

- Never enable Fast Mode, `-fast`, `High Fast`, `fast=true`, or premium
  speed/service tiers for this session or any spawned Task/subagent/worker.
  Subagents remain allowed; if the host defaults a child to Fast, cancel and
  re-spawn without Fast. Efficient means a cheaper capability-tier model, never
  Fast.
- Prefer first-party portable Skills from this catalog (or the consumer's pinned
  releases) and Skills the harness references before inventing project-local
  duplicates or relying on third-party Skills for the same method.
- Preserve repository-local product, architecture, ownership, and security
  authority.
- Ask when intent or authority is unresolved, or an action is external,
  irreversible, sensitive, or materially risky.
- Execute authorized routine completion without asking again. When repository
  policy makes commit/push/merge the default, perform it after checks pass;
  when this session opened a PR/MR and required checks are green with no
  conflicts, merge it through the normal path before finishing. Do not leave
  mergeable session-owned PRs open. Do not force-merge past red required
  checks or over foreign WIP. Escalate only a named exception or blocker.
- Write all persistent repository artifacts in US English unless the human
  explicitly requests another language for a named artifact. Chat language
  never changes artifact language implicitly. Use ASCII punctuation only
  (straight quotes, hyphen `-`, `...`). No curly quotes, em/en dashes,
  ellipsis characters, or odd spaces.
- Follow the repository's owned voice or style guide when present. Otherwise
  write direct, concrete prose: lead with the problem or working model, name
  trade-offs and system effects, and remove generic hype, defensive setup, and
  text that changes no decision or action.
- Reserve first person for artifacts that explicitly speak for the repository
  owner. Keep agent instructions and operating procedures neutral and
  imperative.

## Completion

- Run the relevant checks.
- Review the diff against scope and non-goals.
- Finish git footprint per **Git Working Tree Hygiene** in `HARNESS.md`
  (strip agent/tool producer chrome from commits and PR/MR surfaces; claim and
  release leases for every edited checkout including primary; never delete
  another agent's live worktree; reclaim foreign paths only with explicit
  human confirmation; return surviving session/primary-sibling checkouts to
  the default branch while still holding the lease unless the human asked to
  remain on the task branch).
- Answer the Stewardship questions before claiming done (manifest here; port
  within your authority only - never write back to a foreign public upstream).
- Use `agent-sync` to retain durable evidence and harness improvements.
