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

## 2026-10-10 - The public line covers one repository

- Signal: The public catalog carried the full multi-repository operating
  system, so it was both a build plan for the upper levels and hard to start
  from for a single repository.
- Evidence: Eight operating-system Skills and two root blueprints totaled
  about 55k words; most first uses stay on one repository.
- Decision or change: `scaffold-harness`, `agent-sync`, `update-harness`,
  `build-autonomous-agents`, `run-product-engineering`, and
  `learn-agentic-engineering` took major versions scoped to one repository;
  `system-one-routing` and `scaffold-distributed-context` were retired;
  `MULTI-REPO-HARNESS.md` and `HARNESS-OPERATIONS.md` were replaced by
  `docs/BEYOND-ONE-REPOSITORY.md`, and `docs/LEVELS.md` shows L1-L7 for
  people. Earlier entries below that name the retired files describe what was
  true at their date.
- Re-check trigger: Consumers repeatedly need multi-repository guidance the
  public line no longer gives, or a reduced Skill no longer runs a real
  single-repository harness end to end.

## 2026-10-07 - A leak guard must not hold the names it guards

- Signal: The audit gate that keeps the maintainer's private names out of this
  public catalog listed those names as plain-text patterns, so the gate itself
  published them and every clone carried them in history.
- Evidence: `scripts/audit-skills.py` and `tests/test_portfolio_pointers.py`
  exempted themselves from the scan "by construction"; a history rewrite of
  50 per-Skill tags was needed to remove the names afterwards.
- Decision or change: The gate compares SHA-256 digests of token runs; its
  tests use stand-in names. Only generic patterns, such as a machine path,
  stay readable and keep a narrow self-exemption.
- Re-check trigger: A new guard, test fixture, or example needs a private name
  in a world-readable file.

## 2026-08-07 - Port Gitea CI traps into gitea-actions

- Signal: CI hit three portable traps that future Gitea harnesses would
  relearn if they were recorded nowhere public.
- Evidence: sparse-checkout omitted CI helpers (exit 127 after successful
  deploy); `docker/build-push-action` Complete job `CreateArtifact` timeouts on
  self-hosted Gitea; automated step injection de-indented workflow YAML.
- Decision or change: Expand public `gitea-actions` Workflow Rules and Red
  Flags; minor-bump to 1.1.0. Keep target-specific notification and summary
  scripts out of the public Skill.
- Re-check trigger: New Gitea consumers still hit Complete-job artifact hangs,
  sparse exit 127, or merge-breaking workflow YAML after bulk edits.

## 2026-08-05 - Sibling onboarding and relevance

- Decision or change: The multi-repository line these entries shaped is no
  longer part of this catalog (see the 2026-10-10 entry).

## 2026-08-04 - Ban agent/tool producer chrome on review surfaces

- Signal: Branch-name bans were live, but PR bodies and commits still carried
  host-injected producer chrome.
- Evidence: PR #8 ended with `Made with Cursor`; Cursor `Co-authored-by`
  trailers still appeared in consuming history; docs had no explicit ban.
- Decision or change: Extend Git Working Tree Hygiene with Review-surface
  attribution (forbid and strip). Port into scaffold templates; minor-bump
  `scaffold-harness` to 1.33.0. Keep human co-authors, license attribution,
  and subject-matter tool mentions.
- Re-check trigger: New PRs still show Made-with / Generated-by footers; new
  commits carry AI tool co-author trailers; a jurisdiction requires mandatory
  AI disclosure on integration surfaces.

## 2026-08-04 - Worktree placement and fan-out branch hygiene

- Signal: Nested or `.worktrees/` checkouts broke sibling discovery via
  `ROOT.parent`; fan-out onto foreign WIP left member `main` stale.
- Evidence: Full Gates false failures during branch-gate roll-out; snippet
  commits on leftover product tips; Prettier drift required re-sync.
- Decision or change: Prefer `../.worktrees/<repo>-<task>/` beside the primary
  checkout; run Full Gates from the primary checkout when parent is wrong;
  fan-out on dedicated branches from `main` and re-verify after formatters.
  Harden the scaffold `HARNESS.md` template accordingly. Patch-bump
  `scaffold-harness` to 1.32.3.
- Re-check trigger: In-repo nested worktrees again; fan-out on `codex/` or
  product WIP; green claimed without primary Full Gates.

## 2026-08-04 - Skill audit must skip local worktrees

- Signal: Live `.worktrees/` checkouts made `audit-skills.py` fail on
  incomplete nested trees (missing sibling links), even when ignored by Git.
- Evidence: Repeated Fast Check failures during harness sessions while a live
  or leftover worktree existed under `.worktrees/`.
- Decision or change: Add `.worktrees` and `worktrees` to audit `SKIP_DIRS`.
  Ignore rules alone are not enough because the audit walks the filesystem.
  Patch-bump
  `scaffold-harness` to 1.32.2.
- Re-check trigger: Audit fails again because of a local worktree path; new
  isolation directory names appear outside the skip set.

## 2026-08-04 - Worktree leases

- Decision or change: Checkout leases belong to the multi-repository line,
  which is no longer part of this catalog (see the 2026-10-10 entry).

## 2026-08-04 - Branch gate, worktree default, ordinary names

- Signal: Agents edited shared branches and used tool-prefixed names such as
  `codex/...`; isolation was optional and often skipped.
- Evidence: Owner requires a mandatory pre-edit branch check, worktree as the
  default isolation path, and ordinary descriptive branch names in every
  harness including future scaffolds.
- Decision or change: Strengthen `Git Working Tree Hygiene` in scaffold
  templates, catalog `HARNESS.md` / `AGENTS.md`, and `agent-sync` routing.
  Bump `agent-sync` and `scaffold-harness` minor versions in
  `skills-lock.json`.
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
- Evidence: Owner instruction that "future harnesses" means this
  public upstream, and every harness change must decide whether a generalized
  portable variant belongs here.
- Decision or change: Strengthen stewardship in `HARNESS.md`, `AGENTS.md`,
  `agent-sync`, and `scaffold-harness` templates: always decide in the same
  loop; port autonomously when portable; ask only when public vs private
  placement is ambiguous or the port would leak private authority. Bump
  `agent-sync` to 1.14.0 and `scaffold-harness` to 1.30.0.
- Re-check trigger: Harness change ships without a same-loop port decision;
  agents ask for confirmation on unambiguous portable ports.
