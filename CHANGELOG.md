# Changelog

This repository versions each Skill independently. See `VERSIONING.md` and
`skills-lock.json` for the canonical versions.

## Unreleased

- `scaffold-harness` 2.10.1: the Claude Code activation hooks template is
  reachable. 2.9.0 added `templates/claude-hooks.md` - the settings, the four
  moments, and what each check looks for - and referenced it from nowhere: not
  from the prose describing the mechanism, not from the Templates table listing
  fifteen other artifacts. A reader was told to put routing in a Hook and left
  to write it, with the finished template beside the file. On hosts that read
  instruction files as behavior this cost nothing; on a host that selects
  Skills as tools it was the one piece that mattered.

- `audit-skills.py`: a bundled file that no Markdown in its own Skill names
  now fails the audit, which is the check that would have caught the above.
  Candidates come from git rather than a filesystem walk, so local artifacts
  like `.DS_Store` are not judged.

- `audit-skills.py`: `SKIP_DIRS` was matched against absolute path parts, so a
  checkout under `.../.worktrees/<task>/` - the isolation default this
  catalog's own harness prescribes - skipped every file in every file-level
  validator while still printing "passed". Measured before the fix: 0 of 83
  Markdown files inspected. CI never saw it, because CI checks out at an
  ordinary path. The filter now decides by the path relative to the repository
  root.

- `scaffold-harness` 2.10.0: the harness template answers whose work an
  artifact is, and where that stops. Cross-agent non-interference covered
  checkouts and said nothing about work items, pull requests, review comments
  or progress values - so a repository wrote its own version from one seat,
  naming its owner and listing everybody else as untouchable. That tells every
  other person's session that its own work is off limits, and a green pull
  request then has nobody who will merge it. Ownership is written from the seat
  now. The carve-out ships with it: code is not owned that way, an end-to-end
  change takes what it needs and leaves every place it touches better than it
  found it, and a genuine hands-off area is a different rule that a repository
  names and justifies separately.

- `documentation-and-adrs` 1.2.0: a claim is checked against the system before
  it is written, a document that has outgrown its purpose is deleted rather
  than maintained, and reading an artifact that states a mechanism is not
  checking it. An audit written to catch false documentation claims produced
  two of its own, both confirmed by reading a code comment that was wrong. The
  test that catches them: name the command that would falsify the sentence, or
  you have not checked it.

- `completion-gate` 1.4.0: after merging, check continuous integration on the
  branch that was merged into. Three pull requests, each green on its own head,
  merged in sequence and left the target branch red while the deployment stayed
  healthy the whole time - so every item of the deployment check passed and the
  session reported the work as fine.
- `testing-strategies` 1.4.0: synchronize on the work rather than on a
  duration, and give a negative assertion an instrument that would notice the
  positive. A test that slept 100 ms after starting a stream whose producer
  keeps writing passed at 95 ms and lost the race in CI at 100 ms - a foreign
  key violation, a missing row, and an upstream call it had claimed would not
  happen. That last claim could not have failed either way: the fake upstream
  threw when reached, and the code under test catches one failure and reports
  it as an ordinary outcome, so the throw was swallowed. Counting reaches and
  asserting zero is what made the assertion real.
- `completion-gate` 1.3.0: a change that deploys is done when its deployment
  has been checked, not when it merges. Adds the deployment step - the
  deployment serves the merged commit, the touched surface works when used,
  the error reporting is quiet since that deploy - and the environment
  prerequisite class: a schema change, a variable, a credential, anything CI
  does for itself that a hosted environment does not, applied wherever the
  change is deployed and named in the pull request. Scoped: a change that
  deploys nothing gets no deployment check.
- `api-design` 1.1.0: read every module the contract touches before drafting
  it, and keep outcomes distinct when their causes differ. An inventory taken
  after the first draft produced a contract that was wrong about its own abuse
  control; flattening "not attempted" into "failed" records a failure that
  never happened and can suppress the retry that would have worked.
- `completion-gate` 1.2.0: done means observed against real data, not green
  tests. A real run is where the finding no plan predicted shows up; where a
  run is impossible, say so rather than letting the suite stand in for it.
- `coding-discipline` 1.5.0: one rule with several call sites is one unit of
  work. Fixing only the site the request names leaves the rule half-applied,
  and the siblings stay broken in a way the request will not mention again.
- `documentation-and-adrs` 1.1.0: when a decision lands, re-read and correct
  the plan documents written before it. Nothing in a decision record shows
  which plan it contradicted, so a superseded instruction survives in a plan
  and is followed later as if it were current.
- `write-a-skill` 1.5.0: a new Skill carries a `license` field, and an existing
  one gains it when changed for another reason - a Skill is copied out of a
  catalog more often than installed from it, and the repository LICENSE does
  not travel with a single directory.
- `write-a-skill` 1.4.1: state the activation guidance for a Skill installed on
  its own. The description decides where no instruction file exists, which is
  the common case; hooks are a few lines of host configuration rather than a
  harness.
- `write-a-skill` 1.4.0: activation is host-shaped and installed is not used.
  Design the description to carry the trigger on its own for hosts that select
  a Skill as a tool, keep host wiring target-local, and confirm a real session
  loads the Skill on each declared host rather than assuming it does.
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
