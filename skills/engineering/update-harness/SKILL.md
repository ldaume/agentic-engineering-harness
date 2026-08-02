---
name: update-harness
description: Checks, installs, updates, and cleans repository or cross-repository harness Skills across project, private organization or team, public, user, and global scopes. Use for Skill installation, updates, synchronization, duplicate or conflicting Skill cleanup, missing public complements, Renovate Skill changes, source federation, or stale harness dependencies and platform assumptions.
---

# Update Harness

Update managed capabilities without replacing target-local truth or silently
changing autonomy.

## 1. Select the Mode

Infer the narrowest mode from the request:

- `check` - inspect available updates and report options without changing files
- `skills` - check or update only managed Skill dependencies
- `hygiene` - reconcile effective Skill scopes, ownership, duplicates, and stale
  installations
- `apply` - apply approved or policy-allowed harness and Skill updates
- no explicit mode - check first, then apply only reversible updates clearly
  authorized by the request and target policy

Treat `/update-harness`, `update-harness skills`, and equivalent natural
language as invocation hints, not as platform-specific implementation.

## 2. Ground the Target

Read the applicable instruction hierarchy, harness contract, context map,
current dependency manifest, checks, and ownership boundaries. For several
repositories, work from their coordinating repository and preserve each
target's local authority.

Inventory:

- effective project, workspace, user, and global Skill scopes and host
  precedence
- private organization or team catalogs, public upstreams, coordinator policy,
  and the exact source authority for each managed Skill
- duplicate names, conflicting versions, invalid packages, and unnecessary
  copies across the roots each active host actually loads
- managed Skills, source repositories, exact refs, content digests, and targets
- public complements referenced by the selected loop and whether they are
  required now
- local wrappers or target-specific deltas that must not be overwritten
- harness artifacts and currentness claims affected by the update
- runtime lines, CI actions, container images, package managers, and dependency
  ecosystems that can emit support or deprecation warnings
- automated update coverage, routine release cooldowns, security-update
  exceptions, and evidence-gated merge behavior
- Fast Check, Full Gates, install checks, and rollback path

Do not create a dependency manifest merely because one is preferred. Add one
only when the target actually manages external Skills or harness components.

## 3. Reconcile Skill Scope

Keep one intentional owner for each effective Skill:

1. Keep repository-specific procedures and adaptations project-locally.
2. Keep genuinely shared non-public procedures, approved pins, and internal
   adapters in a private organization or team catalog.
3. Keep portable generic procedures in their public upstream and consume them
   through immutable refs instead of copying their lifecycle into private
   policy repositories.
4. Let a private coordinator own placement, compatibility, and shared policy;
   it does not become the source owner for public or project-local Skill text.
5. Keep only a small reusable bootstrap globally when it is useful across
   repositories.
6. Treat a host-required client copy as intentional only when that host cannot
   load the shared source without it.
7. Preserve system, bundled, plugin-managed, and unrelated installations.
8. Compare content and precedence before moving a duplicate; do not infer
   ownership from the Skill name alone.
9. Quarantine obsolete, conflicting, or mis-scoped user installations with an
   inventory and rollback path. Global cleanup requires explicit user intent.
10. Install a missing selected complement project-locally and invoke it in the
   current loop.

Do not confuse semantic ownership with host load precedence. Inspect what the
active host actually loads, then ensure the project-local owner or wrapper
supplies target semantics and exactly one managed private or public dependency
supplies the reusable procedure.

Complete hygiene when every active host resolves the intended version without
collisions, global context contains only justified reusable Skills, local
dependencies match the target, and removed entries are recoverable or were
explicitly approved for deletion.

## 4. Resolve Current Versions

Prefer immutable per-Skill release tags and exact commit digests. Fetch or
refresh a local source clone before comparing versions. Do not treat a moving
default branch as a reproducible release.

For runtimes and tools, prefer the latest supported stable LTS line when the
ecosystem publishes one and the current stable line otherwise. Keep a declared
older line only for an explicit compatibility owner and re-check trigger. Pin
exact action commits and container digests where integrity or reproducibility
requires it; update the human-readable release comment with the pin.

Use the repository's dependency bot or native platform updater for every
ecosystem it can actually manage. Apply a short routine-release cooldown;
security updates must not wait behind it. Treat a deprecation, end-of-support,
or forced-runtime annotation as a failed currentness check and update the
owning runtime, action, image, or adapter rather than hiding the annotation.

For a missing public Skill, derive the target technology and version from
manifests, lockfiles, runtime output, and official documentation. Prefer an
explicit upstream complement named by the selected local Skill. Otherwise use
an installed upstream `find-skills` or
`npx skills find "<technology> <major-version> <task>"`, then inspect the exact
candidate rather than trusting its ranking.

Use upstream release notes, source diffs, and current primary documentation
when behavior, platform support, pricing, model routing, security, or community
practice may have changed. Mark missing or ambiguous compatibility evidence.

Read [REFERENCE.md](./REFERENCE.md) only when creating or migrating a managed
Skill manifest, configuring Renovate, or resolving release-tag semantics.

## 5. Classify the Update

Use the source's declared version policy. When none exists, classify the
observed diff conservatively:

- patch - correction with no intended behavior change
- minor - backward-compatible capability or workflow expansion
- major - changed invocation, ownership, completion, authority, output, or
  other behavior that may invalidate a consumer assumption

Separate source changes from target-local adaptations. Never infer that a
newer Skill is automatically appropriate for the target's maturity.

## 6. Decide the Gate

Apply a patch or minor update autonomously only when it is reversible, within
documented target policy, and covered by relevant checks.

Before a major update, changed autonomy, new permissions, wider repository
scope, destructive migration, or uncertain compatibility:

1. present two or three options, including keeping the current version
2. show the material behavior diff, evidence, blast radius, and rollback
3. recommend one option
4. wait for human acceptance before applying the dependent branch

## 7. Apply Atomically

For every selected dependency:

1. retrieve the exact release ref into a temporary or existing trusted clone
2. verify the expected Skill path and declared version
3. replace only the managed target directory, or install a new public Skill
   project-locally; global installation requires explicit user intent
4. preserve target-local wrappers outside that directory
5. update the manifest ref and resolved commit digest together
6. update affected harness references without copying source-owned prose
7. run the source Skill audit or validator, an install check, and the target's
   smallest relevant checks
8. for CI or runtime changes, run the real workflow when possible and verify
   that support and deprecation annotations are empty

For hygiene changes, record exact source and quarantine paths, update any
owning lock or manifest, and verify the host's effective Skill list after the
move.

If a required check fails, restore the previous managed content and manifest
state. Do not leave a partially synchronized dependency.

## 8. Complete

Report:

- updated, unchanged, and deferred dependencies
- old and new versions
- behavior or harness implications
- checks run and rollback availability
- effective global and local Skill owners after reconciliation
- any decision still requiring a human

Persist only evidence that changes future work. A routine successful update
does not require a learning entry.

The update is complete when refs, resolved content, effective host scope,
manifest state, and checks agree, and no target-local authority or wrapper was
overwritten.

## Platform Wrappers

If a host supports slash commands, keep `/update-harness` as a thin wrapper
that invokes this Skill and forwards the requested mode. Do not duplicate this
workflow in Cursor, Claude Code, Codex, or other host-specific command files.
