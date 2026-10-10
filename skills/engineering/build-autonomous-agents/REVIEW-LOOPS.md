# Review Loops and Asking People

Load this when agents review each other's work or when an agent may ask a
person a question.

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
