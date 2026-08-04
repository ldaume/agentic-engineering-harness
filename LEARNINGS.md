# Public Learnings

This log starts with the public repository candidate. Earlier private
development history is intentionally not reproduced here.

Add an entry only when reproducible evidence from this repository changes how
future work should run. Promote stable rules to the owning Skill, harness file,
test, or workflow instead of duplicating them here.

Use this shape:

```markdown
## YYYY-MM-DD - Short finding

- Signal:
- Evidence:
- Decision or change:
- Re-check trigger:
```

## 2026-08-04 - Branch gate, worktree default, ordinary names

- Signal: Agents edited shared branches and used tool-prefixed names such as
  `codex/...`; isolation was optional and often skipped.
- Evidence: Owner requires a mandatory pre-edit branch check, worktree as the
  default isolation path, and ordinary descriptive branch names in every
  harness including future scaffolds.
- Decision or change: Strengthen `Git Working Tree Hygiene` in scaffold
  templates, catalog `HARNESS.md` / `AGENTS.md`, `MULTI-REPO-HARNESS.md`, and
  `agent-sync` routing. Bump `agent-sync` and `scaffold-harness` minor
  versions in `skills-lock.json`.
- Re-check trigger: New scaffolds still say "isolate only when needed"; agents
  create `codex/` or `claude/` branches; non-trivial edits land on `main`.

## 2026-08-04 - Same-loop Skill release is routine completion

- Signal: skills-lock bumps reached main without tags/Releases, so consumers
  stayed on stale pins.
- Evidence: Owner instruction that agents must finish this autonomously;
  Release Sequence already routine for matching GitHub Releases.
- Decision or change: Completion and VERSIONING forbid claiming done after a
  lock bump until the validated commit has its per-Skill tag and GitHub
  Release, or a named blocker is recorded.
- Re-check trigger: Version bump lands without tag/Release; agents ask for
  confirmation to publish a routine per-Skill Release.

## 2026-08-04 - Consume-only for third-party harnesses

- Signal: Scaffold stewardship told consumer agents to update "this public
  catalog," which would write third-party harness lessons back here.
- Evidence: Owner instruction: other users building harnesses from this
  upstream must not write back; external contribution PRs are not supported.
- Decision or change: Templates and `agent-sync` port only within owned
  authority and forbid write-back to foreign public upstreams including this
  one. `CONTRIBUTING.md` is consume-and-adapt. Maintainer work in this
  repository remains the only supported change path. Bump `agent-sync` to
  1.15.0 and `scaffold-harness` to 1.31.0.
- Re-check trigger: Consumer agent opens a PR here from stewardship; templates
  again point ports at this upstream for non-maintainers.

## 2026-08-04 - Always check portable port after harness changes

- Signal: Stewardship "Port to future harnesses" was soft; consumers could
  leave portable harness lessons only in one live repository.
- Evidence: Coordinator owner instruction that "future harnesses" means this
  public upstream, and every harness change must decide whether a generalized
  portable variant belongs here.
- Decision or change: Strengthen stewardship in `HARNESS.md`, `AGENTS.md`,
  `agent-sync`, and `scaffold-harness` templates: always decide in the same
  loop; port autonomously when portable; ask only when public vs private
  placement is ambiguous or the port would leak private authority. Bump
  `agent-sync` to 1.14.0 and `scaffold-harness` to 1.30.0.
- Re-check trigger: Harness change ships without a same-loop port decision;
  agents ask for confirmation on unambiguous portable ports.
