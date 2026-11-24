# Review and Integration Vocabulary

The terms reviewers and integrators use to judge whether a change is ready to
merge, so a gate names the gap the way the field does and points at something a
reader can see in the pull request, its comments, or the branch history.
Authors and check scripts use it; reviews do not load it by default.
Change-shape and test terms (small change, why comment, red run) live in
`coding-discipline` and `testing-strategies`. A term is admitted only with a
registered source and an observable marker; evidence and access dates are in
`sources.json`. Check: `exact` (a pattern in the pull request, comments, or git
data a script can match; none ships here yet, so no rule ids), `jev` (a typed
question), `judge` (a person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Code health | Approve when the change clearly leaves the codebase better, even if imperfect; never approve one that leaves it worse. | [SRC-REV-001] | Approval held for polish that changes nothing, or given to a change that adds debt with no follow-up. | judge |
| Nit | Optional polish, labeled so the author may ignore it. | [SRC-REV-001] [SRC-REV-005] | A preference comment that blocks merge with no label. | judge |
| Design first | Review the overall design before naming, style, or details. | [SRC-REV-002] | Comments only on style for a change that adds a module or a dependency. | judge |
| Every line | Read every line asked of you, in its context. | [SRC-REV-002] | An approval of a large diff with files never opened or minutes after the request. | judge |
| Review latency | The time from review request to first response; at most one business day. | [SRC-REV-003] | A pull request with no reviewer response for over one business day. | exact |
| Reasoned comment | A review comment that says why, kindly, and leaves the fix to the author where it can. | [SRC-REV-004] | "Change this" or "wrong" with no reason. | judge |
| CL description | A pull request text that says what changes and why, readable later without links. | [SRC-WRITE-013] | A description that says only "fix bug" or repeats the title. | judge |
| Conventional comment | A comment shaped `label (decorations): subject`, so intent is explicit. | [SRC-REV-005] | Review comments whose intent (issue, suggestion, question) a reader has to guess. | exact |
| Blocking decoration | A marker that says whether a comment must be resolved before merge. | [SRC-REV-005] | An author unsure which comments block, or blocking comments marked as suggestions. | judge |
| Praise | A sincere note on something done well; never false praise. | [SRC-REV-002] [SRC-REV-005] | A review that lists only defects, or praise attached to code with open issues. | judge |
| Ship / Show / Ask | Merge without review, merge and invite review, or wait for review, chosen per change. | [SRC-REV-006] | A routine change waiting days for approval, or an uncertain approach merged unasked. | judge |
| Trunk-based development | Everyone integrates into one trunk; no long-lived development branches. | [SRC-REV-007] | A develop or integration branch that collects features for later release. | exact |
| Short-lived feature branch | One author, a couple of days at most, merged to trunk and deleted. | [SRC-REV-008] | A branch older than two days, or not deleted after merge. | exact |
| One branch in flight | A developer, pair, or agent holds one feature branch at a time. | [SRC-REV-008] | Several worktrees per author, each with an aging unmerged branch. | exact |
| Merge from trunk first | Update the branch from trunk, verify, then merge it on its own. | [SRC-REV-008] | One feature branch merged into another, or a merge to trunk not verified after trunk moved. | judge |
| Branch by abstraction | Replace a component in trunk behind an abstraction, never on a long branch. | [SRC-REV-009] | A multi-day replacement developed on a branch that cannot merge until done. | judge |
| Feature flag | Unfinished work merged to trunk and switched off. | [SRC-REV-010] | A finished slice held on a branch because the feature is not complete. | judge |
| Flag permutation | CI runs each meaningful on and off combination of flags. | [SRC-REV-010] | Flag-guarded code that no test runs in one of its states. | judge |
| Flag debt | A flag left in place after its decision is settled. | [SRC-REV-010] | A flag fixed in one state for over a month after release with no removal date. | exact |

## Not admitted

- "LGTM" approvals of a diff nobody read: review every line in context
  [SRC-REV-002].
- Withholding approval until the change is perfect: approve on improved code
  health [SRC-REV-001].
- Every change waiting for approval: choose Ship, Show, or Ask
  [SRC-REV-006].
- Long-lived feature or integration branches as the default flow
  [SRC-REV-007] [SRC-REV-008].
- Merging one feature branch into another [SRC-REV-008].
- Flags kept forever "in case" [SRC-REV-010].
- Unlabeled preference comments treated as blockers [SRC-REV-001]
  [SRC-REV-005].
