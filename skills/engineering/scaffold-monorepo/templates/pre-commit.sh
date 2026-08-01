#!/usr/bin/env sh
set -eu

pnpm lint-staged
pnpm verify
