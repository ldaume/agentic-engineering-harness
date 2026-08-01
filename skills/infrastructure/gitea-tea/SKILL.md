---
name: gitea-tea
description: Uses the tea CLI to inspect and operate Gitea repositories, issues, pull requests, releases, branches, labels, and workflow-adjacent metadata from the terminal. Use when the user mentions tea, gitea cli, terminal-based Gitea operations, PR inspection, issue triage, release checks, or repository automation against Gitea.
---

# Gitea Tea

Use this when Gitea state should be inspected or changed through the `tea` CLI
instead of the browser.

## Project Fit Check

Before running commands:

1. Check whether `tea` is installed and which login/profile is active.
2. Read repo remotes and local branch state before inferring owner/repo.
3. Confirm destructive actions: close issues, delete branches, edit releases,
   merge PRs, or change labels.
4. Prefer read-only commands first; show the target repo and object id before
   mutating anything.
5. Do not print tokens or login config.

## Common Read Commands

```bash
tea repos ls
tea issues ls
tea issues view <id>
tea pulls ls
tea pulls view <id>
tea releases ls
tea labels ls
```

Use `tea --help` and subcommand help for the installed version; flags vary.

## Operating Rules

- Always identify the target remote, owner, repo, branch, issue, or PR.
- When multiple remotes exist, ask or use the one documented by the repo.
- Prefer `tea pulls view` plus local `git diff`/`git log` before reviewing a PR.
- For labels and milestones, preserve existing naming conventions.
- For releases, verify tag existence and changelog source before publishing.
- For automation, wrap `tea` in small scripts only when the command is repeated.

## Review And Triage Flow

1. List the relevant issues or PRs.
2. Open the target item with full metadata.
3. Cross-check local branch, CI status, and linked issues.
4. Perform the smallest needed action.
5. Report the command result and any follow-up state.

## Red Flags

- command would mutate a repo inferred only from the current directory
- ambiguous login/profile
- closing or merging without showing target id
- release creation without checking tag and artifacts
- automation that assumes one Gitea host across all projects
