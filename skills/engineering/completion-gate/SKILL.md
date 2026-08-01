---
name: completion-gate
description: Pre-finish review gate for code changes - correctness, patterns, security, tests, and verification before claiming work complete. Use when finishing a task, creating commits, opening PRs, or preparing to claim work complete.
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

- [ ] End-to-end path works where product intent requires it
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

### 6. Agent sync (significant sessions)

- [ ] Durable learnings merged per skill **agent-sync** (or explicitly none)
- [ ] The repository's learning artifact updated if durable evidence changed

## Required closing statement

Before finishing non-trivial work, tell the user:

1. **What changed** - concrete, scoped summary
2. **How verified** - commands run and outcomes
3. **Uncertain or risky** - gaps, follow-ups, assumptions
4. **Agent sync** - what durable evidence was persisted (or "nothing durable")

## Do not

- Claim "done" without running applicable checks
- Add documentation the user did not need
- Skip the closing statement on non-trivial work
