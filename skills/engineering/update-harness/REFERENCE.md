# Managed Skill Updates

Load this reference only when a target needs a managed Skill manifest,
Renovate integration, or release-tag interpretation.

## Release Contract

Use one immutable tag per independently released Skill:

```text
<skill-name>-v<major>.<minor>.<patch>
```

Example:

```text
update-harness-v1.1.0
```

The tag points to a commit containing the declared Skill version. Never move or
reuse a release tag.

## Target Manifest

Prefer the target's existing dependency convention. When none exists and the
target manages copied Skills, use a concise `harness-skills.yaml`:

```yaml
version: 1
skills:
  - name: update-harness
    source: https://github.com/owner/skills.git
    path: skills/engineering/update-harness
    target: .agents/skills/update-harness
    # renovate: datasource=github-tags depName=update-harness packageName=owner/skills versioning=regex:^update-harness-v(?<major>\d+)\.(?<minor>\d+)\.(?<patch>\d+)$
    ref: update-harness-v1.0.0
    commit: 0123456789abcdef0123456789abcdef01234567
```

Keep target-specific wrappers outside the managed `target` directory. The
resolved commit protects against a moved or compromised tag; update it in the
same change as `ref`.

Verify manifest identity before copying content:

- `ref` matches `<name>-v<semver>` and resolves through the exact
  `refs/tags/<ref>` entry, not as an arbitrary Git revision
- the tag resolves to the recorded `commit`
- the tagged `SKILL.md` frontmatter name matches both `name` and the Skill path
  basename; when the source has a catalog, its recorded path and version match
  too
- the installed file tree matches the Skill tree at that tag

This manifest is target-owned. Do not confuse it with a source catalog's
`skills-lock.json` or a client-generated Skills CLI lockfile.

## Renovate Extraction

The annotation above can be extracted with a regex custom manager:

```json
{
  "customManagers": [
    {
      "customType": "regex",
      "managerFilePatterns": ["/(^|/)harness-skills\\.ya?ml$/"],
      "matchStrings": [
        "# renovate: datasource=(?<datasource>\\S+) depName=(?<depName>\\S+) packageName=(?<packageName>\\S+) versioning=(?<versioning>\\S+)(?: registryUrl=(?<registryUrl>\\S+))?\\s+ref:\\s+(?<currentValue>\\S+)"
      ]
    }
  ]
}
```

Choose the datasource from the source host:

| Source host | Datasource | Registry URL |
|---|---|---|
| GitHub.com | `github-tags` | omit; use the default GitHub registry |
| Gitea | `gitea-tags` | set the instance base URL |
| Forgejo | `forgejo-tags` | set the instance base URL |

Do not assume Gitea, Forgejo, and GitHub are interchangeable. Verify the
configuration against the deployed Renovate version:

- [Renovate regex manager](https://docs.renovatebot.com/modules/manager/regex/)
- [Renovate GitHub tags datasource](https://docs.renovatebot.com/modules/datasource/github-tags/)
- [Renovate Gitea tags datasource](https://docs.renovatebot.com/modules/datasource/gitea-tags/)
- [Renovate Forgejo tags datasource](https://docs.renovatebot.com/modules/datasource/forgejo-tags/)

Renovate updates the declared ref. An agent or repository-owned update command
must still synchronize the managed files, resolve the commit, and run checks in
the same pull request.

## Update Policy

Default to:

- patch and minor: propose a pull request and apply when target policy permits
- major: require explicit review of behavior and migration implications
- digest-only change for an existing immutable tag: stop and investigate

Do not auto-merge solely because a release is semantically classified as
patch or minor. Target checks and authority still govern the update.
