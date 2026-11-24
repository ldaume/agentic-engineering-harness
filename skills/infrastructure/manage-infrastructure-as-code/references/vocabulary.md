# Infrastructure as Code Vocabulary

The terms practitioners use to judge whether infrastructure is managed as
reviewable desired state, so a review names a gap the way the field does and
points at something visible in a repository, plan, state configuration, or
pipeline. Authors and check scripts use it; reviews do not load it by default.
Security terms live in `shift-left-security`; Ansible, Gitea CI, and host
hardening terms live in their vendor Skills. A term is admitted only with a
registered source and an observable marker; evidence and access dates are in
`sources.json`. Check: `exact` (a pattern in files, config, or plan output a
script can match; none ships here yet, so no rule ids), `jev` (a typed
question), `judge` (a person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Desired state | The configuration needed to rebuild a system so its instances behave the same, kept apart from runtime data. | [SRC-IAC-002] | Settings that exist only on a running system and in no repository file. | judge |
| Declarative description | A statement of the wanted condition, not the steps to reach it. | [SRC-IAC-001] [SRC-IAC-002] | A shell step in a workflow that creates a resource the declarations could express. | judge |
| Versioned and immutable | Desired state is stored so history is complete and cannot be rewritten. | [SRC-IAC-001] [SRC-IAC-003] | Infrastructure configuration outside version control, or a force-pushed history. | exact |
| Pulled automatically | An agent fetches desired state from its source instead of a person pushing it. | [SRC-IAC-001] | A laptop or ad hoc script that applies the change, with no agent in the loop. | judge |
| Continuous reconciliation | An agent keeps observing actual state and moves it toward desired state. | [SRC-IAC-001] [SRC-IAC-002] | A run that applies once and never compares again; no scheduled or event-driven check. | judge |
| Drift | Actual state has moved, or is moving, away from desired state. | [SRC-IAC-002] | A plan that shows changes nobody made in a commit. | judge |
| Snowflake server | A server made unique by accumulated manual tweaks, hard to rebuild or mirror. | [SRC-IAC-003] [SRC-IAC-004] | A rebuild runbook that lists manual steps after the automated ones. | judge |
| Configuration drift | Untracked ad hoc changes accumulating on a system. | [SRC-IAC-005] | A host whose settings differ from its source recipe. | judge |
| Phoenix server | A server regularly burned down and rebuilt from source, catching drift anywhere. | [SRC-IAC-005] | A host never rebuilt since its first install, with no scheduled rebuild. | judge |
| Immutable server | A server never modified after deploy, only replaced from a new tested image. | [SRC-IAC-006] | Configuration tools run against live instances, or in-place edits to a deployed one. | judge |
| Saved plan applied | The reviewed plan file is the thing applied, not a fresh plan. | [SRC-IAC-013] | An apply step that re-plans, or that ignores the plan the reviewer saw. | exact |
| Speculative plan | A plan made only to look, not meant to be applied. | [SRC-IAC-013] | A plan output without a saved file offered as approval for an apply. | exact |
| Refresh-only | A run that syncs state to out-of-band changes without changing infrastructure. | [SRC-IAC-013] | A deliberate emergency change absorbed into state with no commit explaining it. | judge |
| Routine targeting | Using resource targeting in normal operation, which hides drift. | [SRC-IAC-013] | -target in a pipeline or runbook for everyday changes. | exact |
| State backend | The store for state, giving shared access and the locking API. | [SRC-IAC-011] | State in a local file on one machine for a shared stack. | exact |
| State locking | Automatic exclusive lock during any operation that can write state. | [SRC-IAC-012] | A backend without locking, or -lock=false in a script. | exact |
| Forced unlock | Releasing a lock someone else may hold, risking two writers. | [SRC-IAC-012] | force-unlock in a runbook without checking the lock holder. | exact |
| Sensitive state | State holds every resource attribute, secrets included, and is protected as such. | [SRC-IAC-014] [SRC-IAC-013] | State or plan files committed, or in a world-readable artifact. | exact |
| Import block | Adoption of an existing resource declared in code and reviewed in the plan. | [SRC-IAC-015] | A resource created by hand and later imported by an unreviewed one-off command. | judge |
| Policy as code | Organizational rules written as executable, versioned policy run before release. | [SRC-IAC-007] [SRC-IAC-010] | A review checklist in a wiki with no policy file in the repository. | judge |
| Decision versus enforcement | The policy engine returns a decision; the caller decides to block. | [SRC-IAC-007] | A policy result printed in logs that no gate reads. | judge |
| Policy test | A test rule that proves a policy allows and denies what it should. | [SRC-IAC-008] | Policy files with no test_ rules, or a test run that executes none. | exact |
| Plan as policy input | The machine-readable plan feeds policy, which reads each change and its action. | [SRC-IAC-009] | A policy that scans source only and never the plan's resource changes. | judge |

## Not admitted

- On-the-fly manual changes to a running server as routine practice: they
  create snowflakes [SRC-IAC-003].
- Disabling state locking to get a run through: it risks corruption
  [SRC-IAC-012].
- Resource targeting as an everyday workflow: it leaves undetected drift
  [SRC-IAC-013].
- Treating a plain plan as approval to apply: it is speculative
  [SRC-IAC-013].
- Local state for secrets-bearing stacks: it is plain-text JSON
  [SRC-IAC-014].
