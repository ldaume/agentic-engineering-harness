---
name: start-gate
description: Pre-work gate for code changes - inspect the working tree, preserve foreign work in progress, get the default branch current, and claim an isolated branch or worktree before the first edit. Use when starting a task, resuming a session, picking up an issue, or when the state of the checkout is unknown.
---

# Start Gate

The counterpart to **completion-gate**. That one runs before you call work
done; this one runs before you touch anything. Work started on a stale or
foreign tree produces a diff nobody can review: an unrelated change rides
along, someone else's uncommitted work is destroyed, or the change is written
against a version of the code that no longer exists.

Cost is a few commands. The failure it prevents is discovered at push time, or
by the person whose work disappeared.

## Project Fit Check

Before running this gate:

1. Read the repo's own rules from `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`,
   contributing docs, or equivalents. Branch naming, worktree conventions,
   lease or claim files, and protected branches are project truth and win over
   the defaults below.
2. Detect the version control system, default branch, package manager, and
   setup commands from project files. Do not assume `main`, `git`, or any
   particular package manager.
3. In a repository with no remote, skip the fetch steps and say so, rather than
   reporting a missing origin as a blocker.

## Before the first edit

### 1. Look before you touch

```bash
git status --short --branch
git worktree list
```

Read that output before deciding anything:

- **Uncommitted changes you did not make** belong to someone else, possibly
  another agent session. Never stash, reset, check out over, or commit them.
  Ask whose they are, or work in a separate worktree that leaves that checkout
  alone.
- **A checkout already on a task branch** may be an active session. Leave it
  and open your own worktree.
- **Your own leftovers from an earlier session** get committed or explicitly
  discarded now, as their own decision, never folded into the new task.
- **A lease, claim, or status file** the repository uses to mark an occupied
  checkout is checked here, and honored.

### 2. Get current

```bash
git fetch origin
git switch <default-branch>
git merge --ff-only origin/<default-branch>
```

Fast-forward only. A refused fast-forward means the local default branch has
diverged: resolve that as its own task. Do not `git reset --hard` a branch
whose contents you have not inspected, and do not start on the diverged tip
and hope.

### 3. Claim an isolated place to work

One task, one branch, off the freshly updated default:

```bash
git switch -c <short-descriptive-name>
# or, to leave the primary checkout untouched:
git worktree add ../<repo>-<task> -b <short-descriptive-name>
```

Prefer a worktree when the primary checkout is in use, when several tasks run
in parallel, or when the repository's own rules say so. Name the branch after
the change, not the tool or model that writes it: no agent or product prefixes,
and no producer chrome in commit messages or pull request descriptions.

### 4. Make the environment match the branch

Install dependencies with the project's own manager and its lockfile, using the
frozen or immutable variant so a moved lockfile fails loudly instead of
drifting. Start only the services this task actually needs.

A lockfile that moved on the default branch is the usual cause of an
inexplicable local failure minutes later.

### 5. Know what "green" means before you change it

Read the verification commands from the repository - `AGENTS.md`, package
scripts, `Makefile`, CI config - so the finishing gate is not improvised later.
Run them now when the suite is fast, or when the checkout was already dirty,
inherited, or long unused: a failure that was there before your first edit is
cheap to recognize now and expensive to diagnose after.

## Stop and ask when

- Uncommitted or unpushed work in the checkout is not yours and its owner is
  unknown.
- The default branch has diverged locally, or history was rewritten upstream.
- The task requires committing directly to a protected branch.
- Setup requires credentials, secrets, or an external resource you were not
  given.

## Do not

- Stash, reset, clean, check out over, or commit work you did not write
- Start editing on the default branch, or on a stale tip you did not fetch
- Delete or move another session's worktree
- Encode the agent, model, or tool in a branch name, commit, or PR surface
- Treat a green result from a checkout you never inspected as a baseline
