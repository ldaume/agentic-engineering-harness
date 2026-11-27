---
name: gitea-actions
description: Designs, debugs, secures, and reviews Gitea Actions workflows, act_runner or gitea-runner setups, runner labels, tokens, secrets, variables, cache, artifacts, and GitHub Actions compatibility. Use when working with .gitea/workflows, Gitea CI, act_runner or gitea-runner, GITEA_TOKEN permissions, self-hosted Gitea runners, workflow migration, sparse-checkout CI helpers, docker/build-push-action on Gitea, step summaries, or Gitea-specific CI failures. Not for self-hosted GitHub Actions runner fleets.
license: MIT
metadata:
  vocabulary: vendor
---

# Gitea Actions

Use this for Gitea-hosted CI/CD, especially when GitHub Actions examples need
to be adapted to Gitea's runner, token, and network model.

## Project Fit Check

Before changing workflows:

1. Read `AGENTS.md`, existing `.gitea/workflows/*.yml`, runner docs, deployment
   docs, and repo variables/secrets conventions.
2. Detect the Gitea version, runner version (act_runner was renamed
   gitea-runner in v1.0.0, with a new binary, repository, and config
   placeholders), runner labels, container mode,
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
- Know which labels run on the host: a label is `name[:schema[:args]]`, and
  `host` is the default schema, so a bare label runs the job directly on the
  runner machine as the runner's user. Use `docker://<image>` for isolation;
  keep host labels for trusted repositories.
- With an empty `container.docker_host` the runner mounts the Docker socket
  into job containers, which is root on the host. Set it to `"-"` or use the
  dind image unless jobs truly need the host daemon.

When one host runs several jobs at once (`runner.capacity` above its default
of 1, or several runners on one machine):

- Jobs in containers share the host's Docker daemon. Prune with an age
  filter (`docker system prune --filter until=2h`), because a plain prune
  removes a parallel job's freshly created container. Each concurrent job
  takes a subnet from the daemon's pool; raise `default-address-pools` or set
  `container.network` before raising capacity.
- Host-label jobs, and jobs sharing a mounted volume, share `HOME` and tool
  installs. Give each runner its own `HOME` and tool homes, use
  `tool_cache_mode: shared` (one volume per capacity slot), or install tools
  pinned on the host. On-demand installers such as rustup have no lock
  between processes and break when two jobs install into one home.
- All jobs leave through one public address. Expect rate limits from Docker
  Hub and GitHub when many jobs pull images or actions at once: use a registry
  mirror, and set `cache.offline_mode: true` so cached actions are reused
  instead of fetched per job (a moved tag then stays at the cached commit).

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
- registry retention that deletes the `sha256:` child manifests behind a
  multi-arch (OCI index) job-image tag, or trims tags by count or age without
  checking every consumer repository's pins (the tag still lists in the
  package UI, but pulls fail with `manifest unknown`; runners with a cached
  image keep working until their cache is pruned)
