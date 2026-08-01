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
3. Run `python3 scripts/audit-skills.py`.
4. Let the repository validation workflow install-test the catalog for every
   supported client, and run representative activation checks when behavior
   changed.
5. Commit the coherent release state.
6. Create the matching per-Skill tag on that commit.
7. Push the commit before or with its tags.

Do not create or move a tag for an uncommitted tree. Add catalog-wide releases
only if evidence shows real bulk consumers; independent Skill tags are the
default.

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
