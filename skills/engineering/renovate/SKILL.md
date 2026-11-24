---
name: renovate
license: MIT
description: Configures, self-hosts, and diagnoses the Renovate dependency bot - renovate.json, packageRules, groups, schedules, minimumReleaseAge cooldowns, automerge, the Dependency Dashboard, custom regex managers, and a self-hosted run on GitHub Actions with a GitHub App token. Use when setting up or changing Renovate, when Renovate opens no pull requests or too few, when runs are green but nothing arrives, when dashboard items sit in Pending Status Checks or Pending Approval, or when the Renovate workflow or app permissions change. Not for reviewing or delivering a single update pull request, or for managed Skill pins.
---

# Renovate

Keep Renovate delivering: every run ends with `result: done`, each update
appears once, and an update waits only where a rule says it should. A green
workflow proves nothing here, because Renovate exits 0 on most aborts.

Hand off a single update pull request (impact, adaptation, rollout) to
`deliver-dependency-upgrades`, and greenfield repository setup to
`scaffold-monorepo` when installed.

## Diagnose before changing config

Run this when Renovate seems quiet, before editing `renovate.json`, because
most "Renovate does nothing" reports are a permission, a cooldown, or a
schedule and not a missing rule.

1. **Read run results, not conclusions.** For the last runs that fell inside
   the schedule, grep the log for `"result":`. Anything other than `done`
   (`repository-changed`, `external-host-error`, ...) means the run stopped
   before it reached most branches. Done when every in-schedule run of the last
   week is accounted for.
2. **Run once at debug level.** A self-hosted workflow should expose
   `LOG_LEVEL` as a dispatch input; info level hides every reason below. Grep
   the debug log for the signatures in the table.
3. **Read the Dependency Dashboard sections.** Pending Approval waits for a
   tick; Awaiting Schedule waits for the window; Pending Status Checks waits for
   a status or for `minimumReleaseAge`. An item that stays in Pending Status
   Checks longer than the cooldown is stuck, not waiting.
4. **Reproduce out of schedule.** Tick the item's dashboard checkbox; with an
   `issues: edited` trigger this starts a run that processes that branch now.
   Prefer an item that does not automerge, so the probe changes nothing
   unreviewed. Done when the failing step shows in a log you triggered.

| Log signature | Cause | Fix |
| --- | --- | --- |
| `Repository has changed during renovation - aborting` right after a branch update; debug shows `integration-unauthorized` on `POST .../statuses` | The token cannot write commit statuses, and Renovate maps the 403 to `repository-changed`, aborting the whole run | Grant the app Commit statuses read and write (full table below) |
| `Marking N release(s) as pending, as they do not have a releaseTimestamp ... timestamp-required` | `minimumReleaseAgeBehaviour` defaults to `timestamp-required`; datasources without timestamps (Docker Hub tags, some registries) never become stable | `packageRules` entry with `matchDatasources` for that datasource and `minimumReleaseAgeBehaviour: "timestamp-optional"`; keep the default elsewhere |
| `creation is disabled because internalChecksFilter was not met` | Release younger than `minimumReleaseAge`, with `internalChecksFilter: "strict"` | Expected while young; stuck when combined with the row above |
| `Package not scheduled` / `Skipping PR creation out of schedule` | Run outside `schedule` | Make the window cover at least two runs, so one abort or busy runner does not cost a week |
| A whole group under Pending Approval | A `dependencyDashboardApproval` rule matches one member of a group set by an earlier rule; approval applies to the group | Give the approval rule its own `groupName` (or `null`) |
| Same dependency listed twice, in two branches | A custom regex manager reads a value a built-in manager already reads (the `github-actions` manager reads `renovatebot/github-action`'s `renovate-version` and `setup-terraform`'s `terraform_version`) | Delete the custom manager; two branches would edit one line |
| Automerge PR green but never merged | Merge queue on the base branch without the queue permission, or `platformAutomerge: false` with no Renovate run after checks pass | Grant Merge queues read and write; or let GitHub automerge (`platformAutomerge: true`) |

## Self-host on GitHub Actions

Use a GitHub App token, because a pull request opened with the built-in
`GITHUB_TOKEN` starts no workflows, so required checks never run and nothing
merges.

- Mint the token with `actions/create-github-app-token` and no `owner` or
  `repositories` input, so it covers only the repository the workflow runs in.
  Set workflow `permissions: {}`; the job needs nothing from `GITHUB_TOKEN`.
- Give the app the permissions Renovate's GitHub platform docs list, because a
  missing write permission fails as an abort, not as an error you will see:
  repository Administration read, Checks read and write, Commit statuses read
  and write, Contents read and write, Dependabot alerts read, Issues read and
  write, Merge queues read and write (when a merge queue exists), Metadata read,
  Pull requests read and write, Workflows read and write; organization Members
  read. After changing app permissions, the installation owner must accept
  them; verify with `gh api orgs/<org>/installations` that the installation
  shows them.
- Set `RENOVATE_REPOSITORIES` to the current repository, `RENOVATE_ONBOARDING:
  "false"`, `RENOVATE_REQUIRE_CONFIG: required`, and
  `RENOVATE_PLATFORM_COMMIT: enabled` so commits are signed by the app.
- Trigger on a schedule, on `workflow_dispatch` with a log-level input, on
  pushes that change the workflow or `renovate.json`, and on `issues: edited`
  guarded to the bot's own dashboard edited by someone else, so a tick acts
  now and the bot's own dashboard rewrite does not loop.
- Pin every action by commit SHA and the Renovate version as an input; the
  `github-actions` manager keeps both current.
- A pin that carries a checksum (a downloaded binary with its SHA-256) needs a
  `postUpgradeTasks` script that rewrites the checksum, allowed through
  `RENOVATE_ALLOWED_COMMANDS` in the workflow, plus a CI check that downloads
  and compares; otherwise automerge ships a stale checksum.

## Configuration defaults

- Extend `config:recommended` and `helpers:pinGitHubActionDigests`.
- Cooldown: `minimumReleaseAge` (three days is a common floor) with
  `internalChecksFilter: "strict"`, and the timestamp exception above per
  datasource. When the package manager has its own cooldown (pnpm
  `minimumReleaseAge`), keep Renovate's at least as long, or lock file updates
  fail on companion packages.
- Automerge only minor, patch, pin, and digest updates, and only behind
  required checks; majors, runtimes, and data stores wait for a person through
  `dependencyDashboardApproval` or `automerge: false`.
- Every rule gets a `description` that says why it exists, because the next
  reader has to decide whether a hold is still needed. Re-check holds when the
  pinned reason is gone (lock file already past it, override removed).
- Keep property tests next to the config for the rules that protect
  production (no major automerges, holds name their group, no duplicate
  readers), written as Given/When/Then.

## Verify and finish

1. Run `npx --package renovate@<deployed version> renovate-config-validator
   --strict renovate.json`, using the version the workflow runs, because
   options change between majors.
2. After the change reaches the default branch, read the next run (the push
   trigger starts one): `result: done`, no WARN you cannot explain, and the
   dashboard shows the expected section for every item you touched.
3. Done when an in-schedule run ends `done` and the update you expected exists
   as a pull request or sits in the dashboard section a rule puts it in.

## Sources

- [Configuration options](https://docs.renovatebot.com/configuration-options/)
- [Minimum release age](https://docs.renovatebot.com/key-concepts/minimum-release-age/)
- [GitHub platform and app permissions](https://docs.renovatebot.com/modules/platform/github/)
- [Dependency Dashboard](https://docs.renovatebot.com/key-concepts/dashboard/)
- [Noise reduction and schedules](https://docs.renovatebot.com/noise-reduction/)
