# Agent Instructions

This is the public, standalone source for portable Agent Skills and harness
blueprints. It does not depend on a private coordinator or another repository.

## Start

- Use `CONTEXT-MAP.md` to select only the sources needed for the current task.
  Load the relevant `HARNESS.md` sections when the task touches stewardship,
  authority, review, context architecture, or completion; do not preload every
  routed source.
- Read `VOICE.md` before writing or materially revising repository prose.
- When changing a Skill, read its complete `SKILL.md`, the nearby category
  `README.md`, `VERSIONING.md`, and `skills/engineering/write-a-skill/SKILL.md`.
- Inspect `git status` and `git worktree list` before editing. Preserve foreign
  work and never silently overwrite or delete it.
- Use existing repository patterns and commands before adding anything new.

## Autonomy and communication

- Infer the intended outcome and execute routine, reversible, in-scope work
  autonomously. Do not ask for permission at every implementation step.
- Commit and push coherent ready work when relevant checks pass and repository
  policy or the current task already grants that authority. Do not ask again
  for an authorized routine push. A matching GitHub Release for a newly created
  per-Skill tag that completed `VERSIONING.md` is routine completion. Historical
  release backfill, remote creation, a repo-wide release, a new publication
  channel, deploy, force-push, permission increase, or irreversible operation
  still requires explicit authority.
- Ask when consequential intent, ownership, semantics, security, sensitive
  data, legal meaning, or blast radius cannot be resolved from evidence.
- Establish shared understanding for significant work. Use fresh-context
  review for every resolved material decision or change, and
  `grill-harness-with-docs` for genuinely unresolved material branches.
- Communicate with the user in their preferred language when known. Write
  persistent repository artifacts in US English unless the user explicitly
  requests another language.
- Use ASCII punctuation in tracked text. No curly quotes, em/en dashes,
  ellipsis characters, or odd spaces.

## Repository boundaries

- Keep Skills reusable. Target product facts, customer data, private paths,
  credentials, membership maps, and workflow state belong in their owning
  repositories.
- Portable does not mean stack-neutral. Keep generic methods in core Skills and
  make technology-specific assumptions explicit in profiles or adapters.
- Do not copy public/community Skills into this repository as original work.
  Reference or install upstream capabilities and verify provenance.
- Treat Git-tracked repository sources as memory. Chat is not a durable source
  of truth.

## Repository shape

| Path | Role |
|---|---|
| `skills/engineering/` | Implementation, harness, context, agent, and Skill workflows |
| `skills/product/` | Product discovery, delivery, outcomes, and compliance workflows |
| `skills/frontend/` | Frontend and UX profile |
| `skills/backend/` | API, backend, and data profiles |
| `skills/infrastructure/` | CI, container, hosting, and automation adapters |
| `skills/testing/` | Test strategy and browser automation |
| `scripts/` | Dependency-free repository validation |
| `skills-lock.json` | Canonical installable Skill index |

Each Skill lives at `skills/<category>/<name>/SKILL.md`.

## Skill authoring

- `name` must match the Skill directory.
- Frontmatter `description` is the portable invocation contract. Keep it
  trigger-rich and concise.
- Keep every-run behavior in `SKILL.md`. Load references only for a named
  conditional branch.
- Keep `SKILL.md` under 500 lines. Move detail only when it improves execution
  or reuse.
- Give fragile multi-step work explicit checks, stop conditions, and recovery.
- Update `skills-lock.json` and the relevant human catalog when adding,
  renaming, moving, or changing a Skill version.
- Follow `VOICE.md`; remove hype, filler, fake certainty, and prose that changes
  no decision or behavior.

## Checks

Fast Check:

```bash
python3 scripts/audit-skills.py
```

For each new or materially changed Skill:

1. Run the Fast Check.
2. Run `scripts/audit-skill-provenance.py` against the relevant checked-out
   public sources.
3. Install-test the changed Skill in a temporary target with the supported
   client or clients.
4. Review the diff against scope, non-goals, private boundaries, and versioning.

## Completion

- Run relevant checks and review the final diff.
- Run the **Website Projection** check in `HARNESS.md` for every change and
  finish with an applied and verified website update, a named handoff, or an
  explicit evidence-backed no-change result.
- Route durable evidence to the smallest owning artifact. Use `LEARNINGS.md`
  only for public, reproducible evidence that changes future work.
- Update `scaffold-harness` or `agent-sync` when a portable harness lesson must
  reach future repositories.
- Finish the Git footprint: integrate coherent ready work, clean up only
  session-created worktrees, and report foreign orphans without deleting them.
- Complete the authorized routine Git footprint. Do not create a remote or
  perform a first publication without explicit authority.
