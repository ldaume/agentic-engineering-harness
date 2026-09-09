# Changelog

This repository versions each Skill independently. See `VERSIONING.md` and
`skills-lock.json` for the canonical versions.

## Unreleased

- `scaffold-harness` 2.9.0: match activation to how each host selects behavior.
  Where a host picks a Skill as a tool from its description, routing belongs in
  a Hook at the moment of the decision - session start, first edit, commit, and
  after a merge - not only in an instruction file. Adds a
  `templates/claude-hooks.md` with the four moments, what each check looks for,
  and the member-local-wins rule for a user-scope copy.
- `start-gate` 1.0.0: new pre-work gate and counterpart to `completion-gate` -
  inspect the tree, preserve foreign work in progress, fast-forward the default
  branch, claim an isolated branch or worktree, match the environment to the
  branch, and know what green means before changing it.
- `agent-sync` 1.18.0: session start is a currency gate; current harness and
  pinned Skills come before "only what the task needs"; close-out leaves the
  host workspace on local default.
- `scaffold-harness` 2.4.0: templates require session currency (current
  harness and pins) and a clean git loop before claiming done.

- `scaffold-harness` 2.3.0: close the git loop on remote **and** local default;
  fast-forward primary after merge; move the session root off a task worktree
  before deleting it; grill before involving the human for ordinary close-out.

- `scaffold-harness` 2.2.0: prefer first-party portable Skills before
  project-local duplicates; keep Never Fast Mode on parents and children with
  cancel/re-spawn if a host defaults Fast; subagents remain allowed.
- `coding-discipline` 1.4.0: prefer harness-referenced or catalog
  `coding-discipline` for TDD; follow a project-local `tdd` Skill only as a
  thin wrapper with real local deltas, not a portable TDD duplicate.
- `scaffold-harness` 2.1.0: Never enable premium Fast Mode for parents or
  spawned workers; Efficient remains a cheaper capability tier only. Align
  templates, CURRENTNESS, and MULTI-REPO-HARNESS with that hard rule.
- `build-autonomous-agents` 2.0.0: require test-first deterministic seams,
  eval-first agent judgment, durable checkpoints, automatic wake or
  reconciliation, explicit stall detection, and recoverable waiting states.
  Existing workload contracts must add the new continuity and completion
  fields before adopting this major version.
- `scaffold-harness` 2.0.0: add no-silent-stall runtime contracts, human
  contribution without routine scheduling gates, an evidence-gated
  FAST-inspired fluid allocation pilot, and separate Efficient/Balanced/Frontier
  capability tiers from premium speed service tiers that remain off by default.
  Existing orchestration policies must rename the former Fast capability tier
  and add the new continuity requirements before adopting this major version.

- `update-harness` 1.5.1: require managed Skill manifests to bind the exact
  per-Skill tag, resolved commit, tagged Skill identity, source path, and
  installed tree.

- `agent-sync` 1.17.1: gate autonomous PR merge on repository policy
  authorization; record a named blocker when merge is disallowed.

- `scaffold-harness` 1.37.0: future harnesses default to commit/push/merge for
  session-owned ready PRs/MRs (green checks, no conflicts; no force-merge past
  red required checks).
- `agent-sync` 1.17.0: completion requires closing the integration loop,
  including autonomous merge of session-owned ready PRs/MRs or a named blocker.

- Kept `frontend-craft` and `backend-craft` independently installable while
  adding shared end-to-end discipline for thin UIs, task-shaped reads,
  intent-shaped mutations, context-driven architecture, and representative
  technology spikes.
- Made Given/When/Then semantics the framework-neutral default for behavioral
  tests without requiring comments or a GWT library.
- Added latest-supported-LTS or current-stable runtime policy, routine update
  cooldowns, security bypass, pinned action guidance, and deprecation
  annotation failure handling for current and future harnesses.
- Added `.serena/` to the future harness ignore baseline.
- Made shared understanding and proportional grilling universal: autonomous
  fact-finding, fresh-agent critique for resolved material work, and human
  grilling only for genuinely unresolved branches while explicit authorization
  remains at named external-risk boundaries.
- Defined one-owner learning routes for portable public methods, shared private
  procedures, cross-repository coordination, and member-local truth.
- Added honest Now/Next/Later/Never investment horizons, value-defined issue
  rules, and explicit milestone and date semantics to `product-craft` and the
  generated harness baseline.
- Connected the public README to Lenny and the future GitHub installation path.
- Documented the nested task, procedure, repository, workflow, value-stream,
  and product loops and their relationship to L1-L7 delegation.
- Defined public, private organization or team, coordinator, project-local, and
  global Skill source ownership without moving target authority.
- Prepared a standalone public repository with a fresh Git history.
- Added GitHub validation, contribution, security, licensing, and publication
  boundaries.
- Reframed the catalog as a stack-neutral method core plus explicit technology
  profiles and adapters.
- Kept earlier private development history outside the public repository.
