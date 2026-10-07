# Review Loops, Asking People, and Orchestration

Load this when agents review each other's work, when an agent may ask a person
a question, or when an orchestrator runs delegated workers.

## Review loops

- **Every send-back records what to fix.** A send-back from review to the
  builders carries a reason. When the sender gives none, use the review's own
  findings as the reason. Without a recorded reason the builders resolve
  against stale findings from an earlier round, change nothing, and the loop
  spins.
- **A reviewer's question to a person survives the reviewer's own send-back.**
  Do not let one verdict erase the other. Split mixed findings: send the
  fixable defects back at once, ask the person only what only they can answer,
  and route the answer to the builders or to the next review round.

## Asking people

- **The platform finds out, the person decides.** Before asking, check the
  item's own acceptance criteria and scope. What they already answer is a
  defect to fix, not a question. People are asked for decisions, never for
  facts the system can look up.
- **Repair before asking, within bounds.** The agents repair a stale or
  conflicting branch, red checks, and timed-out runs, up to one shared return
  bound that every stage counts against. Infrastructure failures (a runner
  that died, a flaky service, a timeout with no code cause) are re-run and
  never treated as code defects.
- **Never push an empty commit to retrigger CI.** Some preview and deploy
  systems skip commits that touch nothing they build, so the run never
  starts. Re-run the job through the CI system, or change something real.
- **Ask only past the bound, and say what was tried.** The question names the
  attempts, their outcomes, and the decision needed, so the person never
  repeats the investigation.

## Orchestration

- **Workers emit heartbeats; the orchestrator re-arms a short watchdog every
  turn.** A heartbeat is the worker's signal ("still alive, last step X"). The
  watchdog is the observer's own one-shot timer (for example 15 minutes). It
  fires even when nothing arrives, then checks whether any worker's heartbeat
  or progress went stale and stops or restarts it. A missing heartbeat is
  noticed, never waited on silently.
- **Delegate for speed and to keep the parent's context lean.** Ask children
  for conclusions and numbers, never for raw transcripts.
- **A child may not load the project's instructions.** A read-only search
  child often loads none of the project instruction files, and a child on
  another host loads only that host's files. The parent's prompt carries every
  rule, shared state link, and item id the child must act on instead of relying
  on the child to find them.
- **When a host's permission classifier blocks delegated work,** propose the
  narrowest allow rule that covers it to the owner. Never add permission rules
  to your own host configuration: that changes the autonomy level, and the
  autonomy level belongs to the owner.
