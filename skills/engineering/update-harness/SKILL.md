---
name: update-harness
description: Checks, installs, updates, and cleans a repository's managed Agent Skills against its skills-lock.json. Use for Skill installation, version checks and updates, duplicate or conflicting project Skill cleanup, a Renovate or bot Skill update, or a missing Skill a task needs.
---

# Update Harness

Update managed Skills without replacing repository-local truth or silently
changing what agents are allowed to do.

## 1. Select the Mode

Infer the narrowest mode from the request, because a wider mode touches files
the user did not ask about:

- `check` - report available updates and options without changing files
- `install` - add a missing Skill project-locally
- `update` - move managed Skills to newer pinned versions
- `clean` - remove duplicate, conflicting, or stale project Skill copies

With no explicit mode, check first, then apply only reversible updates the
request and repository policy clearly authorize.

## 2. Ground the Repository

Read the instruction hierarchy, harness contract, `skills-lock.json` (or the
repository's equivalent manifest), checks, and any local wrappers that must not
be overwritten. Inventory the Skill roots each active host actually loads, and
duplicate names or versions across them: hosts differ in precedence, so a
second copy can silently win.

## 3. Resolve Versions

Prefer immutable per-Skill release tags (`<name>-v<semver>`) and their commit,
because a moving default branch is not a reproducible dependency. Read the
release notes and diff between the pinned and the candidate version.

For a missing Skill, derive the technology and major version from the
repository's manifests and lockfiles, then search with an installed
`find-skills` or `npx skills find "<technology> <version> <task>"` and inspect
the candidate itself rather than trusting its ranking. If nothing passes
source, version, license, permission, and overlap checks, finish a one-off task
directly; use `write-a-skill` only when repeated work supplies real examples.

## 4. Apply

1. Replace only the managed Skill directory; keep local wrappers outside it.
2. Update the `skills-lock.json` entry and its ref together, so the manifest
   never describes content that is not there.
3. Run the source's Skill audit when it has one, an install check, and the
   repository's smallest relevant checks.
4. If a check fails, restore the previous content and manifest entry. Do not
   leave a half-synchronized dependency.

A `scaffold-harness` update is also a harness update: its templates are the
source of the repository's `AGENTS.md`, `HARNESS.md`, and bridges. Carry each
changed rule into the repository's own words instead of pasting a template
over a file it has adapted.

## 5. Classify the Update

Use the source's declared version policy. When none exists, classify the
observed diff conservatively:

- patch - correction with no intended behavior change
- minor - backward-compatible capability or workflow expansion
- major - changed invocation, ownership, completion, authority, output, or
  other behavior that may invalidate a consumer assumption

Separate source changes from local adaptations. Never infer that a newer Skill
is automatically appropriate for the repository's operating level.

## 6. Decide the Gate

Apply a patch or minor update autonomously only when it is reversible, within
documented repository policy, and covered by relevant checks.

Before a major update, new permissions, a destructive cleanup, or uncertain
compatibility, because those can change what agents do without anyone
noticing:

1. present two or three options, including keeping the current version
2. show the material behavior diff, evidence, blast radius, and rollback
3. recommend one option
4. wait for human acceptance before applying the dependent branch

## 7. Complete

Report updated, unchanged, and deferred Skills with old and new versions, the
behavior implications, checks run, and any decision still open. The update is
complete when the tag, manifest entry, installed content, and checks agree and
no local wrapper was overwritten.
