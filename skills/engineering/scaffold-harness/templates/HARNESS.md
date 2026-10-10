# Agentic Engineering Harness

## Operating Level

Level: L3 - Living repository; scope: <repository>; chosen <YYYY-MM-DD> by <owner>; pending gates: none

This line is the single record of the chosen level; change it only through the
`scaffold-harness` `MATURITY.md` **Choosing and Switching the Operating
Level** procedure. Add wider delegation only from observed evidence.

- **Commit / push / merge:** when repository policy authorizes routine git
  completion, do it by default after checks pass. Closing the git loop is part
  of finishing - do not wait for a human reminder, and do not re-ask for
  ordinary commit, push, or merge. Closed means the change is on the remote
  default branch **and** the session's local default-branch checkout matches
  that tip. Do not claim done from a task worktree unless the human explicitly
  asked to remain on that branch (then leave the worktree; remote+primary
  match is still required). Do not remove a task worktree until the **host
  session/workspace root** (not merely shell cwd) is a surviving checkout on
  local default. When this session opened a PR/MR and
  required checks are green with no conflicts, merge it through the
  repository's normal path before claiming done. Do not leave mergeable
  session-owned PRs open for a human reminder. Do not force-merge past red
  required checks or over foreign WIP. Standing IDE/global ask-before-commit
  preferences lose to this policy for routine ready work; an explicit
  in-session human hold or stop still wins. Ask only for unusually critical
  git operations (secrets in the tree, force-push, rewriting shared history,
  unclear blast radius on a shared branch). If unsure whether to involve the
  human, grill the remaining uncertainty first; involve them only when that
  routing requires it.
- **Decision rights:** for routine implementation taste, agents resolve
  reversible choices from repository conventions and current evidence. Do not
  ask humans to choose naming, casing, formatting, or equivalent preferences.
  All other uncertainty follows **Uncertainty** and **Shared Understanding and
  Grilling** below: investigate, then spike or grill (whichever answers
  faster; `grill-harness-with-docs` when material), then act. Involve the
  human only for what this document reserves for them (name that list here
  as the repository's current default), and then with options and one
  recommendation, never with a bare offer or a wait. "Not worth doing" is a
  recorded decision with a reason, never a silent drop, because a silent drop
  looks the same as a forgotten one.
- **Host block is not a handoff:** when the host's permission layer (auto
  mode classifier, permission rule, hook) denies a routine close-out command
  such as `gh pr merge`, that denial is a tooling blocker, not a decision for
  the human to make. Name the exact blocked command and the rule that would
  allow it, keep watching the PR or check that is waiting on it, and continue
  automatically once it clears. Do not end the turn with "merge it yourself"
  or "tell me when it is merged". Ask the human only when the block is on an
  action this document already reserves for them.
- **Autonomy is declared where it is enforced:** the operating level granted
  here binds only the agent's instructions. The host enforces permissions
  separately, per workspace, so declare the same delegation in the host's
  permission or safety-classifier context: trusted repositories and
  organizations, cloud projects, and delegated routine actions (spawning
  subagents, using local credentials inline without printing them).
  Otherwise the classifier reads delegated routine work as a bypass and the
  level silently degrades to asking the owner. A permission block is not a
  stop: continue with the rest, narrow the blocked task to a form the rules
  allow, escalate only what stays blocked, and record the missing rule for
  the owner in one line. Never widen around a block in a way that defeats its
  intent.

## Session currency

Before substantial work, use the current harness contract and pinned Skills
for this repository, not a remembered copy or a task worktree cwd. Do not
skip this because the task looks small. Git close-out stays in **On finish**.

1. Fetch origin and read `HARNESS.md` from the origin default tip or the
   remote canonical file. Do not treat `./HARNESS.md` in a task worktree as
   current unless that tree is the origin default tip.
2. Ff-only a clean primary when behind origin; if blocked, leave it.
3. Confirm managed Skill copies match the origin pins before following them.
   Host or IDE ask-before-commit user-rules lose to this contract for
   currency, autonomy, and git close-out.

## Stewardship

Harness stewardship is part of every agent task:

```text
Observe -> Diagnose -> Route -> Change -> Verify -> Keep / Change / Remove
```

Improve a reversible owning artifact without waiting for a separate prompt.
Leave the harness unchanged when no observed problem justifies a change.

After every significant task, and before claiming done, agents must ask and
answer in the same loop:

1. **Manifest here?** Should this evidence become or update a hard owner in
   this repository's harness (`HARNESS.md`, `AGENTS.md`, checks, Hook, Skill,
   LEARNINGS)? Prefer a hard adaptation when the same mistake would
   otherwise recur. Explicit no-change is valid when the signal is transient.
2. **Port within your authority?** After every harness change, decide in the
   same loop whether a generalized portable variant belongs in a catalog you
   own or are authorized to change (for example your org or team Skill
   catalog). If yes, update that owner without waiting for a separate prompt.
   Do not push, open a pull request, or otherwise write back to an external
   public upstream you only consume - including
   `https://github.com/ldaume/agentic-engineering-harness` - unless you are
   that upstream's maintainer with explicit write authority for this change.
   Explicit no-port is valid when the change is target-private or when you
   have no owned shared catalog - harden locally instead; still never write
   back to a foreign public upstream. Ask only when placement is ambiguous or
   a port would leak private authority.
3. After changes to purpose, autonomy, working roots, git hygiene, or the
   harness cycle: does the human `README.md` still teach a new reader?

## Git Working Tree Hygiene

Applies to every edit an agent makes in this repository, no matter which host
spawned the session. Goal: branch and isolation gates before edits, ordinary
branch names, review surfaces free of agent/tool producer chrome, and a
session that leaves nothing of its own behind - without touching work it did
not create.

### Before editing

1. Run `git status --short --branch` and, when available, `git worktree list`.
2. Note dirty paths, current branch, and existing worktrees.
3. If the tree is dirty or unexpected worktrees exist: report them. Do not
   silently overwrite unrelated WIP, because it is someone's unsaved work. Ask
   when ownership of the dirt is unclear.
4. **Branch gate (mandatory before any edit):** Confirm the current branch is
   the correct place for this work.
  - Do not edit shared integration branches (`main`, `master`, the repository
     default branch, or other protected shared branches) in place - including
     typo and docs fixes. Create or check out a dedicated task branch first,
     so every change passes the same review and checks.
  - If already on the correct task branch for this work, continue. If on the
     wrong branch, stop and move to the right branch before editing.
  - Name branches with ordinary descriptive names (kebab-case or the
     repository's existing convention). Do not use agent or tool names as a
     path segment or name prefix (for example `codex/...`, `codex-...`,
     `claude-...`, `cursor-...`, `gpt-...`, `copilot-...`, `agent-...`).
5. **Review-surface attribution:** Git review surfaces describe the change, not
   which agent or coding tool produced it. Producer chrome does not improve
   review quality or agent quality. This item is the scaffold default; an owner
   who wants attribution removes it, with its enforcement, at scaffold time.
  - Commits: do not add AI/tool producer credit in subjects, bodies, or
     trailers. Strip it before push when a host injected it. Forbidden examples
     include `Co-authored-by:` trailers that name Cursor, Claude, Codex,
     Copilot, GPT, or similar agents/tools. Keep legitimate human co-author
     trailers. If the host rewrites the message on `git commit`, rebuild the
     commit without that chrome (for example `git commit-tree`) before push.
  - Pull or merge requests: do not add producer chrome in titles or bodies.
     After create, re-read title and body; strip host-appended footers such as
     `Made with Cursor`, `Generated by Claude`, `via Codex`, or equivalent
     signatures immediately.
  - Allowed: the tool or agent is the subject of the change; third-party
     license or copyright attribution; explicit human request for disclosure.
  - Enforcement, in the repository rather than in one contributor's user
     scope, because a rule held only in prose or a personal hook does not reach
     the next contributor's session: turn the host's attribution off in its
     checked-in settings where the host has one; run
     `scripts/verify-agent-attribution.py` from `scaffold-harness` as the
     `commit-msg` hook; and run it again in CI over every commit of a pull
     request and its body (`--range base..head` with `PR_BODY`). The CI job is
     the layer `--no-verify` cannot skip; keep it inside the required gate and
     make it a no-op rather than skipped on pushes that are not pull requests.
6. **Isolation default:** Default to an isolated workspace for edit work.
   Prefer the host's native worktree or isolation tool when available.
   Otherwise use a project-local git worktree under an ignored `.worktrees/`
   beside the primary checkout (for example `../.worktrees/<repo>-<task>/`),
   not nested inside the repository tree, because in-repo nests break scripts
   that resolve paths from the checkout. Stay put only when already in a linked worktree or host-isolated workspace
   on the correct branch. Narrow exception: a trivial single-path edit on an
   already-correct task branch in a clean tree may stay in place. Do not nest
   worktrees. Do not fight an already-isolated host workspace with a second
   `git worktree add`.

### Whose work is it

Leaving foreign WIP alone is above; this is the same rule one level up, at the
record of a decision. A session acts for one human, and some artifacts carry
an owner: a work item names one, a pull request belongs to whoever opened it,
a review comment to whoever wrote it, a progress value to whoever set it.
Change what your person owns - merging their ready pull requests included -
and read the rest, leaving it exactly as found, down to its position in an
ordered list. Editing another person's entry silently rewrites what they
decided, and a board where anyone may tidy anyone else's entries stops being a
record of who decided what.

**Code is not owned that way.** An end-to-end change takes whatever it needs,
including code someone else wrote, and leaves every place it touches better
than it found it. A rule that stops a session at a file boundary buys tidy
attribution and pays in half-finished slices and somebody else's follow-up.
Where a repository does hold a hands-off area it names it and gives the reason
- mirrored external behavior, a client-authored surface - and that is a
different rule from this one, with a different justification.

Write ownership from the seat, never for a name. A rule that names one person
tells every other person's session that its own work is off limits. Two ways
that fails: nobody merges a green pull request, or a session notices the rule
cannot be meant for it, concludes the file belongs to someone else, and stops
reading the parts that do apply. A roster of names is the same defect once
removed: such a list goes stale the first time the team changes, and it is
already wrong for the seat reading it.

A finding about work that is not your person's goes where the repository keeps
coordination notes, with the date and the evidence, for its owner to decide
on. Recording is not raising.

### On finish (this session's footprint)

1. Integrate ready work via the repository's commit/push/merge or PR policy.
   When that policy authorizes routine completion, perform commit and push
   after checks pass without asking again. Strip any review-surface producer
   chrome from the commit and from any PR/MR title or body before and after
   create. Do not send a completion that still asks the human to merge, pull,
   or confirm ordinary git close-out; that turns a finished task into a chore.
2. **Close the integration loop in the same session.** Merge session-owned
   PRs/MRs when required checks are green and there are no conflicts. Green
   means every required job named for this repository explicitly reports pass;
   "no checks reported", pending, and a missing job are not green, because a
   check that never ran proves nothing. Use the repository's normal merge path
   and never force-push shared history. After the remote merge, update the
   local default-branch checkout with `git fetch` and **ff-only**; never reset
   or rebase it to force the match. If merge or ff-only is blocked (red checks,
   conflicts, foreign WIP, diverged history), report the named blocker with a
   next action. A host permission denial is not one of these: monitor and
   resume, per **Host block is not a handoff** above.
3. **Return to the default branch.** Leave the session working root on the
   default branch with a clean tree at the merged tip, unless the human asked
   to remain on the task branch. Keep remote task branches that still back
   open PRs or unmerged work.
4. Remove only the worktrees this session created, after moving the session
   off them. If a directory survives `git worktree remove` (ignored files such
   as `node_modules` often do), delete that one path; never `rm -rf` the parent
   `.worktrees/` directory, never delete a path `git worktree list` still
   names, and never delete a worktree this session did not create, because it
   may hold another session's live work.
5. Leave the repository no worse for your own artifacts than you found it. Do
   not clean another session's footprint on the way out.

## Cleanup Is Part of Done

A change that creates something on a host, a registry, or a checkout is done
only when that thing has a cleanup path. The class: images built, pulled,
pushed, or pre-pulled; containers, volumes, networks, build cache; worktrees,
branches, temp files, caches, backup copies, and test infrastructure.

- **One-off artifacts** this session made are removed before it claims done,
  or the change names who removes them and when.
- **Recurring artifacts** (one per deploy, run, build, or session) get an
  automated cleanup in the same change: retention in the script that creates
  them, or a scheduled job that prunes them, with a dry run and with
  protection for whatever a rollback still needs (pinned digests, declared
  rollback targets, the newest backups behind a verified restore). A note
  that someone should clean up is not a cleanup path.
- **Never by cleanup:** data volumes, backups without a verified restore,
  pinned or declared rollback artifacts, foreign worktrees, or registry
  packages outside their retention job.
- A disk, registry, or checkout that fills up because a path leaves copies
  behind is a missing gate; closing it comes first.

Enforce it where it runs, not only here: name in this section the job or
check that owns each recurring artifact class (host image and cache
retention, registry retention, a check that names abandoned worktrees), and
keep the **completion-gate** cleanup item in the finish path.

## Agent-Native Design

Optimize sources, contracts, state, and checks for reliable agent navigation.
Canonical artifacts are designed for agents first: explicit ownership,
machine-discoverable routes, executable commands, bounded context, structured
state, and actionable failures. Human README and reference views explain the
system without forcing agent workflows to imitate human ceremony. Human review
surfaces stay legible and no agent-facing mechanism may hide risk, authority,
or rationale.

## Language Contract

Communicate with each human in their preferred collaboration language. Infer it
from explicit preference or conversation evidence; if still unclear, ask once
and retain it in user-scoped or untracked state unless it is shared repository
policy.

Write persistent repository artifacts in US English unless the human explicitly
requests another language for a named artifact. The language used in chat does
not implicitly change code, documentation, schemas, prompts, tests, commits, or
other persisted output.

## Host Portability

Keep canonical semantics in host-neutral repository owners. Use root
`AGENTS.md` plus thin `CLAUDE.md`, `GEMINI.md`, and Antigravity bridges as the
portable interactive baseline; Codex, Cursor, and Pi load `AGENTS.md`
directly. Discover each active host's effective Skill, plugin, Rule, Hook, MCP,
permission, model, and isolation behavior. Add other adapters only for hosts
the target actually uses, reference canonical owners instead of copying
policy, verify precedence and behavior per host, and remove stale adapters.

Non-interactive CI or agent runtimes require a bounded workload contract, least
privilege, secrets policy, cancellation, deterministic gates, telemetry,
retained checkpoints, automatic wake or reconciliation, failure ownership, and
stall alerts. Routine progress must not depend on a later human prompt. Required
human decisions remain durable correlated waits with deadlines and escalation;
they are never auto-approved. That is L5 work; a runtime framework is optional
and enters only for one bounded, repeated workload.

## Progressive Product Engineering

Product work is a closed learning loop, not a specification -> implementation
-> testing -> deployment handoff. Route end-to-end work through
`run-product-engineering` and the target's local craft Skills.

- Evolve ubiquitous language, bounded contexts, examples, contracts, tests, and
  code together; do not freeze a complete domain model up front.
- Shift quality, security, privacy, accessibility, compliance, operability,
  telemetry, and recovery into framing and every implementation slice.
- Mark prototypes and technical spikes as bounded learning work. Discard them
  or make an explicit production investment; never promote them silently.
- Use vertical TDD for production behavior and feed bugs, incidents, adoption,
  control effectiveness, cost, and outcome evidence back into triage.
- Express behavioral tests with Given/When/Then semantics using the target
  framework's normal structure. Do not require comments or a GWT library.
- Keep UIs thin and use task-shaped reads plus intent-shaped mutations when
  they expose the domain more clearly than persistence-shaped CRUD. Treat
  architecture styles, languages, frameworks, and databases as context-bound
  tools; settle consequential uncertainty with bounded representative spikes.
- For product work that uses shared investment or issue tracking, at any level,
  keep an outcome-oriented Now/Next/Later/Never investment view. Horizons are
  not dates; keep Later coarse, record Never with rationale and a revisit
  trigger, and create decision or delivery issues only for sharp Now or Next
  work. Raw intake records may remain without becoming commitments. The level
  determines who maintains and approves these decisions, not whether the
  semantics apply.
- Prefer Git-owned decisions, controls, and generated evidence. Preserve any
  official form or assurance path required by the applicable authority.
- Keep repeatable infrastructure desired state in version control and route
  changes through reviewable plans, policy checks, protected state, controlled
  apply, drift detection, runtime verification, and credible recovery. Name
  GitOps, GitOps-near, or bounded IaC honestly; do not add a controller only to
  improve the label.
- Encode stable enforceable controls as tested policy close to their inputs and
  enforcement point. Named humans retain interpretation, scope, risk acceptance,
  exceptions, and assurance claims.

## Shared Understanding and Grilling

- Start significant work by aligning outcome, scope, non-goals, authoritative
  sources, decision rights, assumptions, unknowns, checks, stop conditions,
  and recovery.
- Investigate discoverable facts and test bounded reversible hypotheses before
  asking a human.
- Use `grill-harness-with-docs` when intent, semantics, authority,
  consequential trade-offs, or material risk remain unresolved.
- Close with the same frame so another human or agent can independently state
  what is true, what changed, why it is complete, and what remains open.

## Review Loops

- Select and run the applicable review loop without asking the human to choose
  the reviewer; human escalation remains governed by `AGENTS.md` boundaries.
- Self-review significant work and run the relevant deterministic checks.
- Use fresh-context independent review for every resolved material decision or
  change, including public methods and Skill semantics.
- Review the harness after repeated friction or a harness change.
- Refresh volatile model, pricing, platform, or community evidence when a
  decision consumes it or an active adapter no longer matches observed host
  behavior. Expiry marks evidence stale; it does not trigger research alone.
- Review controls and human oversight before expanding autonomy or blast radius.
- Treat dependency-bot PRs (Renovate or similar) as evidence-gated merges - never
  merge on green CI alone. See **Dependency bot PRs** below.

Every review ends with keep, change, remove, supersede, rebuild, or no action.

### Dependency bot PRs

When Renovate (or a similar bot) opens a dependency PR, do not silent-merge and
do not silent-ignore:

1. Inspect the version jump against this repository's usage (changelog, release
   notes, breaking changes that affect call sites here).
2. Run the relevant Fast Check / Full Gates. Add a feature-level smoke when the
   bump touches runtime behavior. A build tool counts as runtime behavior when
   the shipped artifact is built with it: a package manager, bundler, or base
   image the container build invokes is exercised by that build and by nothing
   the Fast Check runs, so its bump is verified by building the artifact, not
   by a green test suite.
3. Merge only with evidence the jump is safe for this repo.
4. If not merging (major, risk, red CI, unclear impact, or deliberately
   deferred): leave a clear PR comment with rationale and unblock criteria.

Supply-chain cooldowns (`minimumReleaseAge` and related Renovate settings) are
config, not a substitute for this review.

Use the latest supported stable LTS runtime line where the ecosystem offers
one; use the current stable release otherwise. Pin exact versions, action
commits, and image digests where reproducibility or supply-chain integrity
requires it, then let the configured dependency bot propose updates after its
routine cooldown. Security updates bypass routine cooldowns. A deprecation or
forced-runtime annotation is a currentness failure: update the owning action,
runtime, or adapter instead of suppressing the warning.

A future LTS candidate may run in a separate preview lane before promotion.
Keep that lane non-production and non-blocking unless the repository explicitly
accepts the risk. Promote it only after upstream marks the line LTS, the used
ecosystem passes representative checks, and the normal cooldown has elapsed.

## Uncertainty

- Investigate discoverable facts from repository and primary sources.
- Run a bounded experiment for a reversible low-risk hypothesis.
- Use `grill-harness-with-docs` for unresolved intent, authority, trade-offs,
  product semantics, architecture, governance, or material risk.
- Implement only resolved branches.

## Oversight

Keep consequential workflows human-in-the-loop until scope, permissions,
checks or evals, recovery, rollback, observability, and repeated evidence
support a confirmed human-on-the-loop transition.

For a material human-in-the-loop branch, present two or three options,
including no change when meaningful, with evidence, trade-offs, blast radius,
reversibility, and a recommendation. The human may veto the branch.

Moving a change class from human-in-the-loop to human-on-the-loop is outside
this harness; [the levels](https://github.com/ldaume/agentic-engineering-harness/blob/main/docs/LEVELS.md) describe what it takes.

## Startup Context Budget

An agent pays for every byte it receives before the first prompt. Measure what
a session actually starts with: the entry chain (`CLAUDE.md`, `AGENTS.md`,
`CLAUDE.local.md`, their @-imports, and parent-directory instruction files),
the stdout of every session-start hook, plugin and Skill listings, and tool
lists. Set a byte budget from the measured numbers, just above today's chain,
and keep a script in the fast check that fails when the chain or any hook
output exceeds it. Keep each hook output under the host's inline limit; above
it the host persists the output and shows the agent only a short preview, so
the cost is paid and the content is not read. A hook prints a pointer plus
Skill names, not Skill bodies. Load Skills and reference material on demand.
Raise a budget only with the measurement that justifies it.

## Agent Context Architecture

Optimize cost, latency, and risk per correctly completed task. Retrieve the
smallest authoritative source, process large raw output outside the active
context when supported, load branch-specific reference only when needed, and
pass bounded evidence rather than chat transcripts.

Treat the applicable repository agent instructions, including any nearest
scoped instructions, as the only unconditional repository payload. Load README,
harness, context, status, learning, template, and Skill owners only when the
active branch needs them; route to a section or query before reading a full
large file.

Keep stable session-critical routing and truth local. Use MCP for required live
information or external actions; it does not replace source authority,
freshness, persistence, or context selection.

Use one filtering or compression owner per data path. Add a new layer only for
a measured problem and keep it only when representative tasks preserve quality,
retrieval, privacy, routing, and recovery.

During stewardship, re-check whether discovery, memory, or context-economy
tools (Graphify-class indexes, Headroom, Context Mode, episodic memory, and
similar) should start, stay parked, or be removed. Prefer Git owners first.
Follow the installed `scaffold-harness` capability gate when present.

## Ownership

| Concern | Owner |
|---|---|
| Whose work an artifact is, who may change or merge it, and why code is not owned that way | `HARNESS.md` (Whose work is it) |
| Agent behavior and scope | `AGENTS.md` |
| Domain language | `CONTEXT.md` |
| Source routing | `CONTEXT-MAP.md` |
| Git working-tree start/finish hygiene (branch gate, worktree default, ordinary names, review-surface attribution, return to default branch) | `HARNESS.md` (Git Working Tree Hygiene); ADR when accepted |
| Accepted trade-offs | ADR |
| Durable observations | `LEARNINGS.md` |
| Repeated probabilistic procedure | Skill |
| Portable shared defaults | Your org/team catalog if you own one; never a foreign public upstream |
| Deterministic enforcement | Test, Hook, CI, or platform control |
| Infrastructure desired state and drift | Target infrastructure repository and platform owners |
| Compliance scope and policy semantics | Target ISMS or GRC system and named control owners |

Reference the owner instead of duplicating its content.

Prefer an existing implementation, native capability, or installed dependency
before adding code or another layer. Never simplify away validation at trust
boundaries, security, accessibility, data integrity, recovery, or necessary
error handling.
