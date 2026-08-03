# Agent Instructions

## Start

- Read `README.md`, `CONTEXT-MAP.md` when present, and the sources it routes to.
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
- Before editing: follow **Git Working Tree Hygiene** in `HARNESS.md`
  (`git status`, worktree list, no silent overwrite of foreign WIP).
- Use existing repository conventions and commands before adding new ones.

## Harness

- Follow `HARNESS.md`; improve the smallest owning artifact when current work
  provides evidence.
- Before finish: ask whether durable lessons must manifest in this harness
  and, if portable, also in the upstream `scaffold-harness` templates /
  `agent-sync` so future harnesses inherit them.
- Establish shared understanding for significant work. Use
  `grill-harness-with-docs` for unresolved material decisions in any topic.
- Keep stable instructions here and reference detailed sources.

## Commands

| Task | Command |
|---|---|
| Fast Check | `<smallest reliable command for narrow changes>` |
| Full Gates | `<test, lint, typecheck, build, or repository verify command>` |

## Boundaries

- Preserve repository-local product, architecture, ownership, and security
  authority.
- Ask when intent or authority is unresolved, or an action is external,
  irreversible, sensitive, or materially risky.
- Execute authorized routine completion without asking again. When repository
  policy makes commit/push the default, perform it after checks pass; escalate
  only a named exception or blocker.
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
- Finish git footprint per **Git Working Tree Hygiene** in `HARNESS.md`.
- Answer the Stewardship dual-route questions before claiming done.
- Use `agent-sync` to retain durable evidence and harness improvements.
