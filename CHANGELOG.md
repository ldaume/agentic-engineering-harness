# Changelog

This repository versions each Skill independently. See `VERSIONING.md` and
`skills-lock.json` for the canonical versions.

## Unreleased

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
