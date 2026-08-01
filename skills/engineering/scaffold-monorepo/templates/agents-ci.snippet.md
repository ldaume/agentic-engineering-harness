## CI

__CI_HOST_NAME__ Actions (`__CI_DIR__/ci.yml`): `pnpm verify`, `pnpm build`, `pnpm test:e2e` on Node __NODE_MAJOR__ LTS with pinned job images.

Pre-commit: format staged files, then `pnpm verify` (`format:check`, `typecheck`, `deadcode`, `test`). Skips `build` and `test:e2e` (CI only). Bypass once: `SKIP_SIMPLE_GIT_HOOKS=1 git commit`.

## Renovate

Renovate (`__CI_DIR__/renovate.yml`, `renovate.json`): nightly + manual. Required secrets: `RENOVATE_TOKEN`. Recommended: `RENOVATE_GITHUB_COM_TOKEN`, `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`. Gitea: create labels `dependencies`, `major`, `security`; `RENOVATE_ALLOWED_COMMANDS` lives in the workflow env (not `renovate.json`). Agents: evidence-gated merge or comment-on-defer per harness **Dependency bot PRs** (never silent-merge / silent-ignore).
