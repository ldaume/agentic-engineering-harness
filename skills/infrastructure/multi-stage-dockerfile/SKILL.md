---
name: multi-stage-dockerfile
description: Creates and reviews secure, cache-friendly multi-stage Dockerfiles for Node, web, backend, and static-site projects. Use when writing Dockerfiles, optimizing image size, separating build/runtime stages, hardening containers, fixing slow Docker builds, or preparing production images.
---

# Multi-Stage Dockerfile

Use this for production-oriented Dockerfiles where build dependencies, runtime
dependencies, security, and cache behavior should be explicit.

## Project Fit Check

Before writing a Dockerfile:

1. Detect runtime, package manager, lockfile, build output, server command, and
   required native dependencies.
2. Read existing Dockerfiles, compose files, CI image build jobs, and deployment
   docs.
3. Preserve the project's base-image policy, registry, and runtime user model.
4. Do not introduce Alpine, distroless, rootless, or monorepo pruning patterns
   without checking framework/native dependency compatibility.
5. If the image is deployed by CI, align build args, secrets, labels, and tags
   with that pipeline.

## Structure

Default shape:

1. `base`: shared runtime image and environment
2. `deps`: install dependencies from lockfile
3. `build`: copy source and build artifacts
4. `runtime`: copy only runtime files and run as non-root when possible

Keep dependency install before source copy so source changes do not invalidate
the dependency cache.

## Rules

- Use the lockfile with the matching package manager.
- Copy only needed files between stages.
- Keep build secrets out of final layers.
- Use `.dockerignore` to exclude `node_modules`, build output, VCS metadata,
  local env files, and caches.
- Prefer explicit `CMD` and documented `EXPOSE`.
- Use health checks only when the deployment platform respects them.
- Add OCI labels if the registry/deploy process uses them.

## Security

- Avoid root in the final image when the runtime allows it.
- Never bake `.env`, tokens, SSH keys, or registry credentials into layers.
- Keep package manager caches out of the final image.
- Pin base image by digest when supply-chain policy requires reproducibility.
- Rebuild regularly for base image security patches.

## Verification

```bash
docker build -t local-test .
docker run --rm local-test <smoke command>
```

For web services, run the container and hit a health or homepage route.

## Red Flags

- one-stage image with compilers and dev dependencies in production
- `COPY . .` before dependency install
- missing `.dockerignore`
- final image runs as root without a reason
- secrets passed via `ARG` and kept in image history
- container command differs from documented deploy command
