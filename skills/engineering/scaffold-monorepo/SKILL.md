---
name: scaffold-monorepo
description: Scaffolds a pnpm TypeScript monorepo with verify gates, knip, pre-commit hooks, pinned CI, and Renovate using current toolchain versions at scaffold time. Use when creating a new monorepo, bootstrapping apps/packages layout, or aligning a greenfield repo with progressive-pragmatic craftsmanship golden paths for GitHub Actions or Gitea Actions.
---

# Scaffold Monorepo

Golden-path bootstrap for **pnpm workspaces** + **Node Active LTS** + **verify CI** + **Renovate**. Versions are resolved **at scaffold time**, not copied from memory.

Pair with **scaffold-harness** after the toolchain exists, or adapt to the
repo's existing agent docs.

## Project Fit Check

Before scaffolding:

1. Confirm this is greenfield, an explicit re-scaffold, or a repo where the user
   accepted structural changes.
2. Scan for existing package manager, workspace layout, CI host, Renovate config,
   hooks, formatter, linter, and agent docs.
3. Preserve existing choices unless the user asks to replace them or they block
   the requested scaffold.
4. If the repo already has agent docs, update them in place. If not, offer
   **scaffold-harness** or create only the minimal documented bridge.
5. Resolve routine choices from repository evidence and the defaults below.
   Ask only when a consequential choice or the authority for structural change
   remains unresolved.

## Before writing files

### 1. Resolve current versions (required)

Run [scripts/print-toolchain-hints.sh](./scripts/print-toolchain-hints.sh) and
follow the Version resolution section in [REFERENCE.md](./REFERENCE.md):

- Node **Active LTS** major -> `engines`, `.node-version`, `.nvmrc`, CI `node -e` guard
- Latest **pnpm** -> `packageManager`, `corepack prepare`, Renovate regex manager
- Latest **knip**, **prettier**, **typescript**, **lint-staged**, **simple-git-hooks**
- Pin **container digests** for `node:*`, Playwright image (if E2E), `renovatebot/renovate`, `actions/checkout`, `actions/upload-artifact`
- `@types/node` major must match Node LTS (not npm's latest major)

### 2. Resolve once

| Question                     | Default                                                                                                    |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------- |
| CI host                      | `gitea` -> `.gitea/workflows/`; `github` -> `.github/workflows/`                                           |
| Layout                       | `apps/*`, `packages/*`                                                                                     |
| E2E in CI                    | yes if Playwright app exists                                                                               |
| Framework groups in Renovate | add only stacks present (Astro, React, Tailwind, etc.); Astro -> defer vite major until framework adopts it |
| Root `package.json` `name`   | for `renovate.json` `ignoreDeps`                                                                           |

### 3. Plan output

Record the file list and resolved versions. Write without another confirmation
when the requested scaffold and repository evidence provide authority. Stop for
the human only when the plan would replace an owned choice, widen scope, or
cross another consequential boundary.

## Scaffold checklist

Copy templates from [templates/](./templates/), substitute placeholders (`__NODE_MAJOR__`, `__PNPM_VERSION__`, `__CI_DIR__`, `__RENOVATE_PLATFORM__`, digests, repo name).

**Root toolchain**

- [ ] `package.json` - scripts from [templates/package.root.json](./templates/package.root.json)
- [ ] `pnpm-workspace.yaml` - `allowBuilds.simple-git-hooks: true` (+ native deps as needed)
- [ ] `.node-version`, `.nvmrc` - Active LTS major only
- [ ] `.prettierrc.json`, `.prettierignore`
- [ ] `knip.jsonc` - start minimal; tune per workspace (see [templates/knip.jsonc](./templates/knip.jsonc))
- [ ] `scripts/pre-commit.sh` - lint-staged then `pnpm verify`
- [ ] `simple-git-hooks` + `lint-staged` in root `package.json`
- [ ] `pnpm install` at root

**CI** (`__CI_DIR__/ci.yml`)

- [ ] `preflight` - skip stale main pushes
- [ ] `verify` - `pnpm verify` + `pnpm build`
- [ ] `e2e` - optional; Playwright image pinned
- [ ] Path filters include `__CI_DIR__/`, lockfile, workspaces

**Renovate**

- [ ] `renovate.json` - supply-chain cooldowns, groups for your stack, pnpm regex for `package.json` + `__CI_DIR__/*.yml`
- [ ] `__CI_DIR__/renovate.yml` - platform env (`gitea` vs `github`), `RENOVATE_ALLOWED_COMMANDS` (Gitea self-hosted), token validation
- [ ] Gitea only: create repo labels `dependencies`, `major`, `security` (Renovate config references them)
- [ ] Document secrets in `AGENTS.md` (see [templates/agents-ci.snippet.md](./templates/agents-ci.snippet.md))

**Agent docs**

- [ ] Run **scaffold-harness** or update the existing agent docs - wire `pnpm verify`, `pnpm precommit`, CI/Renovate notes into the local source of truth

## Verify before done

```bash
pnpm verify
pnpm build
# if E2E: pnpm test:e2e
pnpm precommit   # dry-run hook path
```

Use **completion-gate** before first commit.

## Templates

| File                                                               | Purpose                      |
| ------------------------------------------------------------------ | ---------------------------- |
| [templates/package.root.json](./templates/package.root.json)       | Root scripts, engines, hooks |
| [templates/pre-commit.sh](./templates/pre-commit.sh)               | Hook entrypoint              |
| [templates/ci.yml](./templates/ci.yml)                             | Preflight + verify + e2e     |
| [templates/renovate.yml](./templates/renovate.yml)                 | Scheduled Renovate job       |
| [templates/renovate.json](./templates/renovate.json)               | Base Renovate policy         |
| [templates/knip.jsonc](./templates/knip.jsonc)                     | Minimal knip baseline        |
| [templates/pnpm-workspace.yaml](./templates/pnpm-workspace.yaml)   | Workspace + allowBuilds      |
| [templates/agents-ci.snippet.md](./templates/agents-ci.snippet.md) | Paste into AGENTS.md         |

Details: [REFERENCE.md](./REFERENCE.md) - GitHub vs Gitea matrix, secrets, digest pinning, framework-specific Renovate groups.
