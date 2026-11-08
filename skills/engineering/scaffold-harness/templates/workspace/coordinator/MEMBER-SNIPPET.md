# Member Snippet

Paste the section below into every member's `AGENTS.md`, unchanged except for
the placeholders. When the snippet changes, refresh every member in the same
loop (`SYNC.md` **Fan-out**). Keep it thin: it points at the coordinator and
never copies its policy, because a copy drifts.

---

## Workspace

This repository is a member of a multi-repository workspace. Coordinator:
`../<coordinator>/` (remote: `https://<host>/<owner>/<coordinator>`).

- Before substantial work, read `HARNESS.md` and `SYNC.md` from the
  coordinator's current default branch (`git -C ../<coordinator> fetch`, then
  `git -C ../<coordinator> show origin/<default>:HARNESS.md`), or from the
  remote when the sibling checkout is missing. If neither is reachable,
  continue only with reversible work inside this repository.
- Before touching another repository, read the coordinator's `CONTEXT-MAP.md`
  and open a sibling only on a named relationship. No match: stay here.
- When several sessions share the workspace, claim your checkout in the
  coordinator's `STATUS.md` and never remove a checkout another session holds.
- This repository's own instructions win for its product, code, and checks.
  Route lessons that apply to more than this repository to the coordinator
  (`SYNC.md` **Write-back**).
