---
name: github-self-hosted-runners
description: Use whenever building, scaling, or debugging a fleet of self-hosted GitHub Actions runners - several runner slots per host, just-in-time or ephemeral registration, burst servers, offline or stuck runners, rate limits, shared caches, nightly rebuilds. Not for writing workflow YAML or for Gitea's act_runner; `gitea-actions` owns Gitea, `manage-infrastructure-as-code` the provisioning lifecycle.
license: MIT
metadata:
  vocabulary: vendor
---

# GitHub Self-Hosted Runners

Run self-hosted GitHub Actions runners that stay clean, isolated, and cheap
when several jobs share a host and servers come and go. Most failures in such
a fleet come from things the jobs share: a home directory, a tool install, a
Docker daemon, a public address, a runner name. The rules below exist because
each of those broke real jobs.

## Standing Rules

1. **No credential reaches a job.** Self-hosted runners run pull request code,
   and a `runs-on` label is no boundary: any pull request can name it. Keep
   workflows that hold secrets, cloud identities (`id-token: write`), or deploy
   keys on runners the fleet does not share, set `permissions:` to the minimum,
   restrict the runner group to selected private repositories, and never allow
   public repositories, because a fork's pull request would run on your host.
2. **One job per registration.** Register each runner just in time
   (`POST /orgs/{org}/actions/runners/generate-jitconfig`) or with
   `--ephemeral`, so no job inherits a previous job's state; GitHub
   recommends ephemeral runners and advises against autoscaling persistent
   ones. Give every registration a new name (`<host>-<slot>-<random>`): a
   runner that died mid-job stays registered offline under its name, and a
   name still registered cannot be reused. GitHub removes an offline
   ephemeral runner after a day and a persistent one after 14 days.
3. **Slots on one host share nothing a job writes into.** Give each slot its
   own `HOME` and its own tool homes. `runuser`/`su` reset `HOME` to the
   user's home, so set it again after the switch, or every slot shares one
   tool cache ("Text file busy"). rustup has no lock between processes: two
   slots installing one `rust-toolchain.toml` into a shared `RUSTUP_HOME`
   break each other ("component download failed ... could not rename"). The
   same holds for any installer or cache a job fills on demand. Either give it
   a per-slot home or install it pinned when the host is built.
4. **Clean up only what is yours.** After each job, wipe the slot's work
   folder and kill processes left under the slot's folder, since nothing tears
   the host down between jobs. All slots share one Docker daemon: prune with
   an age filter (`docker system prune --filter until=2h`), because a plain
   prune deletes another slot's freshly created container.
5. **One public address means shared rate limits.** Every slot downloading
   its actions from the same address draws HTTP 429 at peaks. Fill a
   root-owned action cache after each job and point the runner at it
   (`ACTIONS_RUNNER_ACTION_ARCHIVE_CACHE`, layout `{owner}_{repo}/{sha}.tar.gz`;
   read by actions/runner and used by GitHub's runner images, but not in the
   public docs, so re-check it on runner upgrades). Fetch the archives from
   GitHub by commit SHA, never from the job's folder, so a job cannot plant
   code for the next one. Call the API with an app installation token:
   anonymous calls get 60 an hour per address, shared by every slot.
6. **Rebuild, never repair.** Rebuild a host from its boot configuration
   instead of fixing it by hand, and pin every download by version and
   checksum. A rebuild kills running jobs: drain first (slots stop taking jobs
   before the rebuild, the rebuild waits for busy runners up to a limit), and
   never rebuild on merge or in working hours.
7. **Keep the runner version current.** With `--disableupdate` (usual for
   pinned images) a runner must move to a new release within 63 days, after
   which GitHub assigns it no jobs; let a dependency bot raise the pin.
8. **Jobs expect `ubuntu-latest`.** A job failing on a missing tool (corepack,
   cargo, sudo, gh) needs a pinned install on the host, not a workaround in
   the consumer's workflow.
9. **Block the metadata service** (169.254.169.254, fe80::a9fe:a9fe) for jobs
   when the host's user data carries a registration key.

## Autoscaling With Burst Servers

Add short-lived servers during queue peaks instead of a second permanent one,
when the provider bills by the hour.

- **The scaler runs outside the runners.** Its token can create and delete
  servers, and runner hosts run pull request code.
- **Prefer the maintained path.** Actions Runner Controller (Kubernetes) or
  GitHub's scale set client do the scaling for you; build a scaler only when
  neither fits, for example plain cloud servers billed by the hour.
- **Pick the signal you can read.** The `workflow_job` webhook (queued,
  in_progress, completed) or the queued runs show the real queue; prefer
  them, and tolerate delayed deliveries. If the scaler's identity cannot read
  Actions runs, "every online runner busy" stands in for the queue; measure how
  often it fires without a queue before trusting it. Do not gate on CPU: busy
  slots wait on the network and databases, so the CPU can stay low while jobs
  queue for an hour.
- **Removal never depends on scaling up.** Read the provider first and delete
  servers past their end plus the job time limit even when GitHub cannot be
  read. Delete a server that never registered a runner within the boot
  timeout. A nightly backstop deletes only servers past end plus grace, so it
  never kills a burst server that is still working.
- **Make creation idempotent.** Name a burst server after its time window, so
  a retried or overlapping scaler run cannot create a twin.
- **End by time, drain by runner.** A burst server knows its end from boot and
  takes no new job after it; the scaler removes its idle runners and deletes
  it once none is busy. Runners of an ending server do not count toward the
  scale-up signal.
- **Prune dead registrations safely.** Delete an offline, idle registration
  once its slot registered again (runner ids grow per registration) or its
  server is gone. Keep a slot's newest registration even when offline: it may
  still be connecting.

## Measure Before Sizing

Log one line per scaler run with runner count, busy runners (base and burst
apart), servers, actions, and busy vCPUs per server, and keep it long enough
for a sizing review (30 days). Size the permanent server for normal load and
let burst servers take the peaks. Full slots are not a full CPU: check both
before adding slots or cores.

## Diagnose a Job

- **Which host ran it:** the jobs API
  (`GET /repos/{owner}/{repo}/actions/runs/{run}/jobs?filter=all`) lists
  `runner_name` with start and end. Slot numbers repeat on every host, so
  "slot 05" means nothing without the host part of the name.
- **A registration that never took a job** does not appear in any job's
  `runner_name`; it exited before a job reached it.
- **Listing the fleet** (`GET /orgs/{org}/actions/runners`) needs a token with
  organization admin rights (`admin:org` for a classic token).

## Completion

A fleet change is done when: every slot is back online after the rollout, one
consumer run is green, the scaler's next log line shows the intended action,
and nothing in the change lets a job write into another slot's state.

## Red Flags

- a workflow with secrets or `id-token: write` on the shared runners
- a runner group that allows public repositories
- one `HOME`, tool home, or cache directory shared by all slots
- `docker system prune` without a filter on a shared daemon
- a rebuild triggered by merge, or one that does not drain
- a scaler running on a runner host, or removal that needs GitHub to answer
- a burst server name without a time window (retries create twins)
- deleting every offline runner instead of only dead registrations

## Sources

- Self-hosted runner reference (ephemeral, autoscaling, `--disableupdate`):
  https://docs.github.com/en/actions/reference/runners/self-hosted-runners
- Removing runners (offline removal times, JIT runners):
  https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/remove-runners
- Secure use (public repositories, runner groups):
  https://docs.github.com/en/actions/reference/security/secure-use
- REST rate limits: https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
- Action archive cache: actions/runner `src/Runner.Worker/ActionManager.cs`
