# Backend Vocabulary

The terms backend and reliability engineers use to judge a service, a data
path, or a worker, so a review names the gap the way the field does and points
at something a reader can see in the code, the schema, the alert rules, or the
telemetry. Authors and check scripts use it; reviews do not load it by default.
A term is admitted only with a registered source and an observable marker;
evidence and access dates are in `sources.json`. Check: `exact` (a pattern in
code, config, or alert rules a script can match; none ships here yet, so no
rule ids), `jev` (a typed question), `judge` (a person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| SLI | A measured ratio of good events to all events for something users notice, such as request success or latency. | [SRC-BACK-001] | An objective defined on host CPU or process uptime instead of user-visible requests. | judge |
| SLO | A target for an SLI over a time window. | [SRC-BACK-001] [SRC-BACK-016] | A user-facing service with no written objective, or one nobody agreed is achievable. | judge |
| SLA | A contract with users whose missed objectives carry consequences. | [SRC-BACK-001] | "SLA" used for an internal target with no stated consequence. | judge |
| Error budget | The unreliability an SLO allows: one minus the target, spent by failures. | [SRC-BACK-002] | Releases decided with no reference to how much budget remains. | judge |
| Error budget policy | The agreed action when the budget is spent, such as pausing feature releases. | [SRC-BACK-003] [SRC-BACK-016] | An SLO with no written consequence for exhausting it. | judge |
| Burn-rate alert | A page on how fast the error budget is being spent, over more than one window. | [SRC-BACK-004] | Paging rules on raw thresholds (CPU, queue depth) tied to no objective. | exact |
| Symptom over cause | Page on what users experience; use causes to explain, not to wake people. | [SRC-BACK-005] | A page for a cause metric while user-facing requests are healthy. | judge |
| Tail latency | Latency read as a distribution, at high percentiles, not as a mean. | [SRC-BACK-001] | A latency dashboard or SLO that shows only the average. | exact |
| Golden signals | Latency, traffic, errors, and saturation of a user-facing service. | [SRC-BACK-005] | A service dashboard missing one of the four, or error latency hidden. | judge |
| Jittered backoff | Retries spaced by randomized, exponentially growing delays, with a cap on attempts. | [SRC-BACK-006] | A retry loop with a fixed delay, no jitter, or no attempt limit. | exact |
| Retry amplification | Retries at several layers that multiply the attempts on one failing dependency. | [SRC-BACK-006] | Client, gateway, and worker each retrying the same call with no shared budget. | judge |
| Load shedding | Rejecting part of the traffic early near overload so the rest is served. | [SRC-BACK-006] | No 429 or 503 path; overload shows up only as timeouts. | judge |
| Bounded queue | A queue with a length limit and a rejection path. | [SRC-BACK-006] | A queue or job backlog with no maximum length and no rejection or alert. | exact |
| Deadline propagation | Passing the remaining time budget and cancellation to every downstream call. | [SRC-BACK-006] | An outbound HTTP, database, or queue call with no timeout. | exact |
| Toil | Manual, repetitive, automatable operational work that grows with the service. | [SRC-BACK-007] | A runbook step a person repeats per release, tenant, or week. | judge |
| Blameless postmortem | An incident review that finds the system fix, not a person to blame. | [SRC-BACK-008] | A postmortem whose root cause is a named person or "human error". | judge |
| Idempotency key | A client-generated key under which the server records a request, so a retry resumes or returns the stored result. | [SRC-BACK-009] | An endpoint or job that charges, sends, or creates with no key or dedupe on retry. | judge |
| Atomic phase | Local changes grouped in one transaction between calls that change foreign state. | [SRC-BACK-009] | An external API call made inside an open database transaction. | judge |
| Recovery point | A recorded checkpoint after each phase so a retry continues where it failed. | [SRC-BACK-009] | A multi-step job that restarts from the top and repeats external side effects. | judge |
| Foreign state mutation | A call that changes state in another system; safe to retry only if that system is idempotent. | [SRC-BACK-009] | A blind retry after a timeout on a call with no idempotency guarantee. | judge |
| Transactionally staged job | A job written to a table in the same transaction as its data and enqueued after commit. | [SRC-BACK-010] | A job enqueued inside a transaction that can still roll back, or before commit. | judge |
| Structured event | One wide record per request per service with its context as typed fields. | [SRC-BACK-011] [SRC-BACK-012] | Free-text log lines with interpolated values and no request id. | exact |
| High cardinality | Fields with many distinct values (user, tenant, request, build) kept as group-by dimensions. | [SRC-BACK-012] | Telemetry that cannot be filtered by tenant, user, or version. | judge |
| Observability | Asking new questions of a running system without shipping new code. | [SRC-BACK-012] | An incident that needs a deploy to add logging before it can be diagnosed. | judge |
| Linearizability | Once a write completes, every later read sees it or something newer. | [SRC-BACK-013] | A read-after-write path served from a replica or cache with no stated guarantee. | judge |
| Lost update | Two read-modify-write cycles race and one silently overwrites the other. | [SRC-BACK-014] | A read then write of the same row with no lock, version check, or atomic update. | judge |
| Write skew | Two transactions read overlapping data, write different rows, and together break an invariant. | [SRC-BACK-014] | An invariant across rows (one on-call, no double booking) enforced only by a prior read. | judge |
| Fencing token | A number that rises with each lock grant and that storage checks to reject stale holders. | [SRC-BACK-015] | A distributed lock or lease guarding correctness with no token checked on write. | judge |

## Not admitted

- 100 percent uptime as the goal: it leaves no error budget and no basis for
  release decisions [SRC-BACK-016] [SRC-BACK-002].
- Labeling a store "CP" or "AP" as a design argument: name the guarantee
  instead [SRC-BACK-013].
- Average latency as the service level: it hides the tail [SRC-BACK-001].
- Log levels and grepping log lines as the observability strategy
  [SRC-BACK-011] [SRC-BACK-012].
- Retrying everything immediately, at every layer [SRC-BACK-006].
- A lease-based lock alone as a correctness guarantee [SRC-BACK-015].
- An isolation level name as proof of safety: check the anomaly
  [SRC-BACK-014].
- "Human error" as a root cause [SRC-BACK-008].
