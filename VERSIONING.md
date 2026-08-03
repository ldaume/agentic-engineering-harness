# Skill Versioning

## Purpose

Version Skills independently so consumers can pin, review, and update only the
capabilities they use. `skills-lock.json` is the canonical catalog index and
declares the current version of every local Skill.

## Versions and Tags

Use Semantic Versioning per Skill:

- major - incompatible invocation, ownership, authority, completion, output,
  or other behavior change
- minor - backward-compatible capability or workflow expansion
- patch - correction with no intended behavior change

Release tags use:

```text
<skill-name>-v<major>.<minor>.<patch>
```

Tags are immutable and point to the commit containing the matching
`skills-lock.json` version and Skill content. A change to one Skill does not
require version bumps for unrelated Skills.

## Release Sequence

1. Review the changed Skill's behavior contract and provenance.
2. Update only its version in `skills-lock.json`.
3. Run `python3 scripts/audit-skills.py` plus the required provenance, install,
   and representative activation checks for the change.
4. Commit and push the coherent release state.
5. Wait for the validation workflow to pass on that exact commit for every
   supported client.
6. Create and push the matching per-Skill tag on that commit.
7. Verify the remote tag resolves to the validated commit.
8. Create the matching GitHub Release from that tag with concise notes covering
   behavior changes, upgrade impact, and the exact install or pin reference.

Do not create or move a tag for an uncommitted tree. Add catalog-wide releases
only if evidence shows real bulk consumers; independent Skill tags are the
default.

The tag and `skills-lock.json` are the technical release sources. The GitHub
Release is their human-readable projection. Do not backfill historical tags
only to populate the Releases page; maintain this projection for new per-Skill
releases from `scaffold-harness-v1.27.0` onward.

If tag publication succeeds but GitHub Release creation fails, keep the tag
immutable and retry the missing projection. Before completion, verify an
existing Release targets the same tag; never move or recreate the tag as
recovery.

## Consumers

Pin managed Skills to exact per-Skill tags and record the resolved commit when
the target copies dependency content. Keep target-specific wrappers outside
managed directories.

Use
[`update-harness`](./skills/engineering/update-harness/SKILL.md) to check,
classify, synchronize, and verify updates. Its
[managed update reference](./skills/engineering/update-harness/REFERENCE.md)
contains a target manifest and Renovate custom-manager example.

The Skills CLI's own lockfiles and update behavior may evolve independently.
Do not treat them as a reproducible target manifest unless the installed CLI
version demonstrably supports restore and exact source refs.
