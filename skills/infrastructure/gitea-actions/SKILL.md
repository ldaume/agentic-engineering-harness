---
name: gitea-actions
description: Designs, debugs, secures, and reviews Gitea Actions workflows, act_runner setups, runner labels, tokens, secrets, variables, cache, artifacts, and GitHub Actions compatibility. Use when working with .gitea/workflows, Gitea CI, act_runner, GITEA_TOKEN permissions, self-hosted runners, workflow migration, sparse-checkout CI helpers, docker/build-push-action on Gitea, step summaries, or Gitea-specific CI failures.
---

# Gitea Actions

Use this for Gitea-hosted CI/CD, especially when GitHub Actions examples need
to be adapted to Gitea's runner, token, and network model.

## Project Fit Check

Before changing workflows:

1. Read `AGENTS.md`, existing `.gitea/workflows/*.yml`, runner docs, deployment
   docs, and repo variables/secrets conventions.
2. Detect the Gitea version, act_runner version, runner labels, container mode,
   and whether jobs run on Docker, host shell, or custom images.
3. Verify which GitHub Actions syntax is actually supported by the installed
   Gitea version before copying examples.
4. Keep secrets, registry credentials, and deploy tokens scoped to the smallest
   workflow that needs them.
5. If current behavior depends on self-hosted network topology, document the
   assumption in the workflow or agent docs.

## Workflow Rules

- Put workflows under `.gitea/workflows/`.
- Prefer explicit `on:` triggers and path filters for expensive jobs.
- Pin third-party actions when possible; avoid floating major tags for sensitive
  deploy paths.
- Keep preflight, verify, build, image, and deploy jobs separate enough that
  failures point to a real layer.
- Use concurrency/cancel-in-progress when repeated pushes to the same ref should
  not burn runner capacity.
- Keep cache keys tied to lockfiles and relevant runtime versions.
- Upload artifacts only when they help debugging or deployment.
- After any automated workflow mutation (fan-out, codegen, bulk step inject),
  parse every touched YAML file before push. Insert steps under an existing
  `steps:` list with the same indent as siblings.
- If a job uses sparse-checkout, include every path that job invokes. Prefer a
  helper directory pattern (for example `scripts/ci/`) over one-file lists.
- Soft-skip writing a job summary when `GITHUB_STEP_SUMMARY` is unset (local
  runs). Do not soft-fail summary or other `always()` helper steps in CI to hide
  a missing sparse path; fix the checkout list instead.
- On self-hosted Gitea, prefer raw `docker` / `docker buildx` for image builds.
  If you keep `docker/build-push-action`, set job env
  `DOCKER_BUILD_RECORD_UPLOAD=false` and `DOCKER_BUILD_SUMMARY=false` so the
  Complete job does not upload `.dockerbuild` records via the GitHub Artifact
  API.

## Runner Rules

- Match `runs-on` labels to registered runner labels exactly.
- Know whether job containers can reach the Gitea host, package registry,
  Docker socket, private networks, and deployment targets.
- Avoid privileged runners by default.
- Treat runner filesystem state as disposable unless explicitly managed.
- Document any required host mounts or Docker-in-Docker assumptions.

## Token And Secret Rules

- Use `GITEA_TOKEN` only for the permissions the workflow needs.
- Prefer repo or org variables for non-secret configuration.
- Never echo tokens, Docker auth JSON, private keys, or provider credentials.
- For private package/container registries, use one clear auth path and test it
  in the job image that actually pulls or pushes.
- Rotate or invalidate deploy tokens when workflow scope changes.

## Migration From GitHub Actions

When porting:

1. Check unsupported syntax first: permissions, reusable workflows, services,
   cache/action versions, OIDC, environments, and marketplace actions.
2. Replace GitHub-specific APIs, URLs, and token assumptions.
3. Validate action sources and whether the runner can fetch them.
4. Test on a small branch before wiring deploy jobs.
5. Keep the workflow readable; do not recreate GitHub-specific complexity if
   Gitea offers a simpler local path.

## Verification

- `yamllint` or parser check when available
- dry-run or test branch workflow for new CI paths
- one failing-path check for secrets/registry/network assumptions when feasible
- `git diff` review for accidental secret insertion

## Red Flags

- copied GitHub workflow with no Gitea compatibility review
- broad token permissions for read-only jobs
- deploy job triggered on every branch
- runner label that exists only on one machine but is undocumented
- cache key that ignores lockfiles
- private registry auth configured in one container but used in another
- `docker/build-push-action` on self-hosted Gitea without
  `DOCKER_BUILD_RECORD_UPLOAD=false` (Complete-job `CreateArtifact` timeouts
  after a successful registry push)
- sparse-checkout file lists that omit scripts or helpers the job still runs
  (exit 127 after an otherwise successful deploy or verify)
- workflow YAML left unparsed after automated step injection (de-indented
  steps at column 0 that break Actions parse only after merge)
