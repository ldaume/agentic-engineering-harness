#!/usr/bin/env sh
# Print registry versions to copy into scaffold templates (run at scaffold time).
set -eu

echo "=== Local runtime ==="
command -v node >/dev/null && node -v || echo "node: not found"
command -v corepack >/dev/null && corepack pnpm -v 2>/dev/null | sed 's/^/pnpm (corepack): /' || true

echo ""
echo "=== npm registry (latest) ==="
for pkg in pnpm typescript prettier knip lint-staged simple-git-hooks vitest "@playwright/test" "@types/node"; do
  ver="$(npm view "$pkg" version 2>/dev/null || echo "?")"
  printf "  %-22s %s\n" "$pkg" "$ver"
done

echo ""
echo "=== Next steps (manual) ==="
echo "  1. Node Active LTS major: https://nodejs.org/en/about/releases"
echo "  2. Pin node:__NODE_MAJOR__-bookworm digest: docker pull + docker inspect RepoDigests"
echo "  3. Pin playwright image to match @playwright/test version"
echo "  4. Pin ghcr.io/renovatebot/renovate:<tag> digest"
echo "  5. Pin actions/checkout and actions/upload-artifact commit SHAs"
echo "  6. Set @types/node allowed major to match Node LTS in renovate.json"
