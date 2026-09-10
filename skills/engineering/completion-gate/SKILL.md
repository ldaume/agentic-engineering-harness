---
name: completion-gate
description: Pre-finish review gate for code changes - correctness, patterns, security, tests, verification, and checking the deployment a change targets before claiming work complete. Use when finishing a task, creating commits, opening PRs, merging, or preparing to claim work complete.
---

# Completion Gate

A diff that compiles is not done. Treat staged, unstaged, and committed changes as **one system change**. Loop until technically sound.

## Project Fit Check

Before running this gate:

1. Read the repo's completion rules from `AGENTS.md`, `CLAUDE.md`,
   `.cursor/rules/`, contributing docs, CI config, package scripts, Makefile, or
   equivalents.
2. Use the repo's own verify commands and required checks. Do not invent
   `pnpm verify`, `npm test`, or `make test` when the project documents another
   path.
3. If no verification path exists, infer the smallest credible checks from the
   stack and say the command choice was inferred.
4. If `LEARNINGS.md` or `agent-sync` is not part of this repo, use the
   repo's existing learning log or explicitly say no durable sync target exists.

## Before claiming complete

### 1. Sync and scope

- [ ] If default branch moved: rebase or merge and re-verify
- [ ] Diff scope matches the request - no drive-by changes

### 2. Correctness and design

- [ ] Solves the **actual** problem, not an adjacent one
- [ ] Fits existing architecture (read `AGENTS.md`, `CONTEXT.md`, relevant ADRs)
- [ ] Readable; better naming over explanatory comments
- [ ] Language and terminology match the target repository and intended audience
- [ ] No new dead code; no orphaned docs

### 3. Quality bar

- [ ] Observed working against real data, not only green tests - a real run is
      where the finding no plan predicted shows up. If a run is impossible here,
      say so rather than letting the suite stand in for it
- [ ] Typed boundaries at API/package edges (no silent `any` escapes)
- [ ] Tests match risk - unit for logic, e2e/integration for user flows
- [ ] **Security/privacy**: no secrets in code; auth and data access respected

### 4. Regression

- [ ] Unintended behavior changes identified and accepted or fixed
- [ ] Existing tests pass; new behavior has coverage where risk warrants

### 5. Verify (run what applies)

Read verify commands from **`AGENTS.md`** or the repo's package scripts (`package.json`, `Makefile`, etc.). Typical examples:

```bash
# adapt to this repo - do not guess if AGENTS.md lists commands
<lint>
<typecheck>
<unit tests for changed areas>
<build>
<e2e if UI or critical flows changed>
```

If verification fails: fix and re-run this gate.

Once merged, check continuous integration on the branch you merged into. A
pull request runs against its own head; the target branch runs against the
merge, so pull requests that were each green can merge in sequence and leave it
red. A healthy deployment answers neither question - a failing test does not
stop a deploy.

### 6. Deployed surfaces (only if this change deploys)

Merging is not deploying, and deploying is not working. Where the change
reaches a deployed environment, it is done when that environment has been
checked - by you, in the same session, not by whoever notices later:

- [ ] The deployment finished and is serving the commit that was merged
- [ ] The surface the change touched was used and did what it should
- [ ] The platform's error reporting shows nothing new in the window since
      that deploy - a failure logged where nobody looks is an unnoticed
      outage, not a handled one
- [ ] Every **environment prerequisite** the change introduced is applied
      wherever the change is deployed, and the pull request names the
      environments that still need it. The class is anything the local and CI
      environments do for themselves that a hosted one does not: a schema
      change, a new environment variable, a credential, a queue or bucket, a
      one-time backfill. Whoever merges it is the only person who knows it
      exists

The build passing is not this check. A bundle that compiles can still fail on
first execution, and that failure only appears when the deployed code runs.

Scope, so this does not become ceremony: a change that touches nothing
deployed gets no deployment check. Say which it was.

**If the check fails:** revert or roll forward immediately, then investigate -
the value here is the short broken window, not the noticing.

### 7. Agent sync (significant sessions)

- [ ] Durable learnings merged per skill **agent-sync** (or explicitly none)
- [ ] The repository's learning artifact updated if durable evidence changed

## Required closing statement

Before finishing non-trivial work, tell the user:

1. **What changed** - concrete, scoped summary
2. **How verified** - commands run and outcomes, plus the deployment check or
   why the change deployed nothing
3. **Uncertain or risky** - gaps, follow-ups, assumptions
4. **Agent sync** - what durable evidence was persisted (or "nothing durable")

## Do not

- Claim "done" without running applicable checks
- Call a deploying change done at merge, before its environment was checked
- Add documentation the user did not need
- Skip the closing statement on non-trivial work
