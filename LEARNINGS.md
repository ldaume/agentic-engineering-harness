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

## 2026-08-05 - No dedicated sibling-onboarding Skill

- Signal: Temptation to add an onboarding Skill so agents know multi-repo vs
  multi-team and how to admit siblings.
- Evidence: Topology prompts, `scaffold-harness`, coordinator `SYNC` admit
  checklist, and Find Sibling already cover the path; Skill Placement forbids
  one-off Skills without repeated failure evidence.
- Decision or change: Document compose path in README prompts and
  HARNESS-OPERATIONS; explicitly reject a dedicated onboarding Skill until
  repeated failure with examples and checks appears.
- Re-check trigger: Agents repeatedly mis-detect topology or skip admit despite
  these docs; then reconsider a Skill with real examples.

## 2026-08-05 - Document demand-driven sibling and team relevance

- Signal: Humans could not reconstruct from the public catalog alone how a
  member session finds siblings and decides task relevance; ownership tables
  existed, but the SYNC -> CONTEXT-MAP match step was private-narrative only.
- Evidence: Public `MULTI-REPO-HARNESS.md` / scaffold REFERENCE named map and
  sync owners without a multi-repo and multi-team relevance walkthrough.
- Decision or change: Add **Find Sibling Scope and Decide Relevance**; mirror
  concisely in scaffold REFERENCE and SYNC / CONTEXT-MAP templates; minor-bump
  `scaffold-harness` to 1.34.0. Keep one coordinator inventory; no member
  Private system reinforcement.
- Re-check trigger: New readers still ask which files to open; scaffolds omit
  the relevance match; teams preload every repository despite map owners.

## 2026-08-04 - Ban agent/tool producer chrome on review surfaces

- Signal: Branch-name bans were live, but PR bodies and commits still carried
  host-injected producer chrome.
- Evidence: PR #8 ended with `Made with Cursor`; Cursor `Co-authored-by`
  trailers still appeared in consuming history; docs had no explicit ban.
- Decision or change: Extend Git Working Tree Hygiene with Review-surface
  attribution (forbid and strip). Port into scaffold templates; minor-bump
  `scaffold-harness` to 1.33.0. Keep human co-authors, license attribution,
  lease/STATUS host fields, and subject-matter tool mentions.
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
  Harden scaffold `HARNESS.md` / `SYNC.md` templates accordingly. Patch-bump
  `scaffold-harness` to 1.32.3.
- Re-check trigger: In-repo nested worktrees again; fan-out on `codex/` or
  product WIP; green claimed without primary Full Gates.

## 2026-08-04 - Skill audit must skip local worktrees

- Signal: Live `.worktrees/` checkouts made `audit-skills.py` fail on
  incomplete nested trees (missing sibling links), even when ignored by Git.
- Evidence: Repeated Fast Check failures during harness sessions while a leased
  or leftover worktree existed under `.worktrees/`.
- Decision or change: Add `.worktrees` and `worktrees` to audit `SKIP_DIRS`.
  Ignore rules alone are not enough because the audit walks the filesystem.
  Also ignore `.agent-lease` in catalog and scaffold `.gitignore`. Patch-bump
  `scaffold-harness` to 1.32.2.
- Re-check trigger: Audit fails again because of a local worktree path; new
  isolation directory names appear outside the skip set.

## 2026-08-04 - Worktree leases over runtime registries

- Signal: Concurrent agents destroyed each other's live worktrees; owner
  rejected SQLite/BullMQ for this class and chose Git-native leases.
- Evidence: Grill of prose vs STATUS+`.agent-lease` vs SQLite/hooks vs Redis;
  throwaway prototypes showed both B and C are advisory against `rm -rf`.
- Decision or change: Scaffold `HARNESS.md` requires `.agent-lease` + STATUS
  lease rows, cross-agent non-interference, and human-gated foreign reclaim.
  Record the trade-off in `docs/adr/` when accepted in a live repo.
- Re-check trigger: Systematic lease ignore; pressure to add SQLite/hooks
  without that evidence; silent TTL deletes.

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
