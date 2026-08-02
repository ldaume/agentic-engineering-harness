# Scaffold monorepo - reference

## Principles (progressive pragmatic craftsmanship)

- **Problem-first**: scaffold only what the repo will use day one (no dummy apps).
- **Built-in quality**: `verify` on every commit; `build` + `e2e` in CI, not pre-commit (speed vs signal).
- Do not add Nx or Turborepo unless the user asks or the repository has an
  evidenced need; pnpm `-r` scripts are enough for small monorepos.
- **Pin what moves you**: container digests, action SHAs, `packageManager` field; let Renovate bump them.
- **Supply-chain patience**: Renovate `minimumReleaseAge` on npm/docker/actions (see template).
- **Evidence-gated bot merges**: agents must not silent-merge Renovate PRs;
  inspect the jump, run verify gates, merge only with safety evidence, or
  comment with deferral rationale (see `scaffold-harness` HARNESS **Dependency
  bot PRs**).

## Version resolution

At scaffold time, never hardcode versions from an old project.

| Artifact | How to resolve |
|----------|----------------|
| Node Active LTS | [nodejs.org/en/about/releases](https://nodejs.org/en/about/releases) - use **Active LTS** major |
| pnpm | `npm view pnpm version` - set `packageManager` and CI `corepack prepare` |
| TypeScript, knip, prettier, vitest, playwright | `npm view <pkg> version` |
| `@types/node` | major = Node LTS major (`^24.` when on Node 24) - use `npm view @types/node@<LTS-major> version`, **not** `npm view @types/node version` (latest major tracks next Node line) |
| `node:24-bookworm` digest | `docker pull node:24-bookworm` then `docker inspect --format='{{index .RepoDigests 0}}'` |
| Playwright CI image | Match `@playwright/test` version: `mcr.microsoft.com/playwright:v<ver>-noble` + digest |
| Renovate image | `ghcr.io/renovatebot/renovate:<tag>` - use latest stable tag + digest from GHCR |
| `actions/checkout`, `actions/upload-artifact` | Use current supported stable releases, pin commit SHAs, keep same-line release comments accurate, and let Renovate update them after the configured cooldown |

Run [scripts/print-toolchain-hints.sh](./scripts/print-toolchain-hints.sh) for a quick npm-registry snapshot.

## Placeholder substitution

| Placeholder | Example |
|-------------|---------|
| `__NODE_MAJOR__` | `24` |
| `__PNPM_VERSION__` | `11.5.2` |
| `__CI_DIR__` | `.gitea/workflows` or `.github/workflows` |
| `__RENOVATE_PLATFORM__` | `gitea` or `github` |
| `__ROOT_PACKAGE_NAME__` | root `package.json` `name` (Renovate `ignoreDeps`) |
| `__PLAYWRIGHT_VERSION__` | matches devDependency |
| `__E2E_REPORT_PATH__` | e.g. `apps/web/playwright-report/` (only if `upload-artifact` step enabled) |
| `__PRIMARY_APP_FILTER__` | pnpm filter for E2E build, e.g. `@scope/web` |
| `__RUNNER_LABEL__` | `ubuntu-latest` (GitHub) or org label e.g. `linux_amd64` (Gitea) |
| `__RENOVATE_BOT_LOGIN__` | `renovate[bot]` (GitHub) or org bot user (Gitea) |
| `__RENOVATE_BOT_EMAIL__` | bot email for git author |
| `__RENOVATE_ENDPOINT__` | Gitea: `${{ github.server_url }}/api/v1/` - GitHub: delete this env line |
| `__CI_DIR_ESCAPED__` | regex path: `\\.gitea/workflows` or `\\.github/workflows` |
| Digest placeholders | full `image@sha256:...` |

Replace every `__CI_DIR__` in `ci.yml` path filters and `renovate.yml` push paths. Set `__CI_DIR_ESCAPED__` in `renovate.json` `customManagers` only.

## GitHub vs Gitea

Workflow YAML is largely identical (Gitea Actions is approximately compatible
with the GitHub Actions API).

| Concern | GitHub | Gitea |
|---------|--------|-------|
| Workflow path | `.github/workflows/` | `.gitea/workflows/` |
| `runs-on` | `ubuntu-latest` or org label | org runner label (e.g. `linux_amd64`) |
| Renovate `RENOVATE_PLATFORM` | `github` | `gitea` |
| Renovate endpoint | default | `${{ github.server_url }}/api/v1/` |
| `upload-artifact` | v4+ OK | pinned SHA may fail on act_runner (`reference not found`) - omit upload step until runner resolves the action; use Playwright `github` reporter |
| Renovate bot user | `renovate[bot]` | org bot user (e.g. `renovate-bot`) - match `RENOVATE_GIT_AUTHOR` |
| Renovate PR labels | auto-created on GitHub | **create** `dependencies`, `major`, `security` labels in repo before first Renovate PR |
| `RENOVATE_ALLOWED_COMMANDS` | usually N/A | required on self-hosted Gitea for `postUpgradeTasks` (`pnpm install --lockfile-only`) - set in workflow env, not `renovate.json` |

### Renovate secrets

**Required**

- `RENOVATE_TOKEN` - PAT with repo write + issues (Dependency Dashboard)

**Recommended**

- `RENOVATE_GITHUB_COM_TOKEN` - read npm metadata / changelogs (rate limits)
- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` - Renovate docker digest lookups

Document in `AGENTS.md`; never commit tokens.

## Root `package.json` scripts (contract)

```json
{
  "format": "prettier --write .",
  "format:check": "prettier --check .",
  "typecheck": "pnpm -r typecheck",
  "deadcode": "knip",
  "verify": "pnpm format:check && pnpm typecheck && pnpm deadcode && pnpm test",
  "precommit": "sh scripts/pre-commit.sh",
  "prepare": "simple-git-hooks"
}
```

Each workspace package should expose `typecheck`, `test`, and `build` (where applicable) so `pnpm -r` works.

## knip tuning

Start with [templates/knip.jsonc](./templates/knip.jsonc). Common additions:

- `ignoreWorkspaces` - non-Node trees (PocketBase hooks, Go apps)
- `ignoreBinaries` - CLI invoked only from npm scripts
- `ignoreDependencies` - `lint-staged`, implicit framework deps
- per-workspace `entry` / `ignoreFiles` - framework-specific (Astro `live.config.ts`, `env.d.ts`)

Run `pnpm deadcode` after scaffold; fix false positives in config before deleting real code.

## Framework-specific Renovate groups

Add `packageRules` only for dependencies you ship:

- **Astro**: `astro`, `@astrojs/*`
- **React islands**: `react`, `react-dom`, `@astrojs/react` or Next equivalents
- **Tailwind v4**: `@tailwindcss/vite`, `tailwindcss`
- **Quality toolchain**: knip, prettier, typescript, hooks
- **Testing**: vitest, playwright, `@playwright/test`
- **Zod**: if shared across packages

Remove unused groups from the template to avoid noise.

## CI job design

1. **preflight** - on `push` to `main`, skip if SHA is no longer tip (saves runner time).
2. **verify** - `pnpm install --frozen-lockfile`, `pnpm verify`, `pnpm build`.
3. **e2e** - separate job, Playwright container; **build the app in this job** (fresh checkout - `verify`'s build does not carry over). Upload report on failure only when `upload-artifact` works on your runner.

Pre-commit runs `verify` only (not `build` / `e2e`). Document bypass: `SKIP_SIMPLE_GIT_HOOKS=1 git commit`.

### Astro + Playwright E2E

- CI: `astro preview` in `playwright.config.ts` webServer (not `astro dev`); set `reuseExistingServer: !isHostedCI` with `CI` / `GITEA_ACTIONS` / `GITHUB_ACTIONS` detection.
- `pnpm-workspace.yaml` overrides: pin transitive `vite` to the major Astro declares (e.g. `^7.0.0` while Astro 6 depends on vite 7.x).
- Renovate: defer **vite major** until Astro's `package.json` depends on vite 8+ - do not force via override alone:

```json
{
  "description": "Vite 8 major: wait until Astro ships vite 8.x",
  "matchManagers": ["npm"],
  "matchPackageNames": ["vite"],
  "matchUpdateTypes": ["major"],
  "enabled": false
}
```

Remove that rule when Astro bumps its vite dependency.

## After scaffold

1. **scaffold-harness** - audit and establish the repository harness
2. First `pnpm format` baseline commit
3. Enable Renovate workflow; confirm Dependency Dashboard issue
4. **agent-sync** - persist durable toolchain evidence in the owning artifacts
