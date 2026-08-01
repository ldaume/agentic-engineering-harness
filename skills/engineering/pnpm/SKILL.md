---
name: pnpm
description: Handles pnpm package management, workspaces, lockfiles, scripts, catalogs, overrides, patches, Corepack, and dependency troubleshooting. Use when running pnpm commands, configuring pnpm workspaces, fixing strict dependency resolution, managing packageManager versions, or updating dependencies in Node.js projects.
---

# pnpm

Use this for Node.js package management with pnpm's strict dependency model.

## Project Fit Check

Before running pnpm:

1. Read `package.json`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`, `.npmrc`,
   `engines`, `packageManager`, and toolchain files.
2. Use the repo's pinned pnpm version through Corepack, mise, Volta, or the
   documented path.
3. Run commands from the workspace root unless a package-level command is
   explicitly needed.
4. Do not replace npm/yarn/bun with pnpm unless the user asked.
5. Treat lockfile changes as intentional and review them.

## Commands

```bash
pnpm install
pnpm --filter <package> <script>
pnpm exec <tool>
pnpm why <package>
pnpm update <package>
pnpm patch <package>
```

## Workspace Rules

- Use `--filter` for targeted work.
- Keep root scripts as orchestration; package scripts do package-local work.
- Prefer `workspace:*` for internal package dependencies.
- Use catalogs only when the repo already uses or wants centralized versions.
- Use `overrides` sparingly and document why.

## Dependency Rules

- Add dependencies to the package that imports them.
- Keep dev tools in the narrowest sensible workspace.
- Do not bypass peer dependency warnings without understanding runtime impact.
- Use `pnpm why` before deleting or deduplicating dependencies.

## Red Flags

- running install from the wrong directory
- changing package manager version without aligning docs and CI
- lockfile churn unrelated to the task
- adding dependency at root because it is convenient
- using `--force` or `--shamefully-hoist` as a first move
