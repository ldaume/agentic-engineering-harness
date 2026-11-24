# Product Engineering Vocabulary

The terms product and delivery practitioners use to judge a bet, a roadmap, a
plan, or a delivery system, so a review names the gap the way the field does
and points at something a reader can see in the brief, the board, the roadmap,
or the deployment data. Shared by `product-craft` and
`run-product-engineering`. Authors and check scripts use it; reviews do not
load it by default. A term is admitted only with a registered source and an
observable marker; evidence and access dates are in `sources.json`. Check:
`exact` (a count from version control, deployment, or board data a script can
compute; none ships here yet, so no rule ids), `jev` (a typed question),
`judge` (a person or model decides).

## Discovery and bets

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Outcome over output | Judge work by the change in customer or business behavior it causes, not by what shipped. | [SRC-PM-003] [SRC-PM-008] | A roadmap or status that lists features and dates with no outcome measure. | judge |
| Desired outcome | The business result at the root of discovery that the team can influence. | [SRC-PM-001] | A tree or brief whose root is a feature, or a goal no team behavior can move. | judge |
| Opportunity solution tree | Outcome, then customer needs, pains, and desires, then candidate solutions, then the assumption tests under each. | [SRC-PM-001] [SRC-FLOW-032] | A solution in delivery with no opportunity or outcome above it. | judge |
| Solution in disguise | An "opportunity" that can be addressed only one way, so it is already a solution. | [SRC-PM-001] | An opportunity worded as a feature ("add export") rather than a need. | judge |
| Compare and contrast | Weigh several candidate solutions for one target opportunity instead of a yes-or-no on one. | [SRC-PM-001] | A risky or differentiating bet with exactly one candidate considered. | judge |
| Assumption test | A small, fast test of the belief a solution depends on, run before building it. | [SRC-PM-001] [SRC-FLOW-032] | A bet entering delivery with no recorded assumption or test result. | judge |
| Continuous discovery | The team that builds talks to customers at least weekly. | [SRC-FLOW-032] | No dated customer interview or test in the last few weeks for an active bet. | judge |
| Four big risks | Value, usability, feasibility, and business viability, each burned down before build. | [SRC-PM-002] | A bet brief that addresses only one or two of the four. | judge |
| Viability risk | Whether the solution works for the business: sales channel, contracts, compliance, acquisition cost, revenue. | [SRC-PM-002] | A bet with no line on how it is sold, priced, or allowed. | judge |
| Feature team | A team handed prioritized features with dates, so value belongs to the requester, not the team. | [SRC-PM-003] | Work items arrive as features with deadlines and no problem or outcome. | judge |
| Build trap | Shipping to show activity and measuring success by what was released. | [SRC-PM-008] | A review that reports features shipped and no adoption or outcome. | judge |
| Appetite | The time a problem is worth, set before design; an estimate goes the other way. | [SRC-PM-004] | A bet with an estimate but no stated time budget. | judge |
| Fixed time, variable scope | When the time box is hit, cut scope; do not move the date. | [SRC-PM-004] | A deadline moved while the original scope stayed whole. | judge |
| Rabbit hole | An unknown in the concept that could eat the time budget, patched or fenced out before the bet. | [SRC-PM-005] | A pitch with no named unknowns, patches, or out-of-bounds list. | judge |
| Circuit breaker | Work that misses its appetite stops by default and is reshaped, not extended. | [SRC-PM-006] | A bet extended past its appetite with no new shaping or decision. | judge |
| Hill chart | Status as uphill (still figuring out) or downhill (making it happen) per scope. | [SRC-WRITE-031] | Status given as percent done while open unknowns remain. | judge |
| Story map | User activities as a backbone with detailed stories hung below and sliced into releases. | [SRC-PM-007] | A flat backlog with no user journey the stories belong to. | judge |
| Walking skeleton | The smallest end-to-end working system, built first. | [SRC-PM-007] | A first release that delivers one layer but no complete user path. | judge |

## Delivery and flow

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Change lead time | Time from commit to running in production. | [SRC-WRITE-010] | Commit-to-deploy times computed from version control and deploy logs. | exact |
| Deployment frequency | How often a service deploys to production. | [SRC-WRITE-010] | Deploys per period from the deploy log. | exact |
| Change fail rate | Share of deployments that need immediate intervention (rollback or hotfix). | [SRC-WRITE-010] | Rollback or hotfix deploys divided by all deploys. | exact |
| Failed deployment recovery time | Time to recover from a deployment that needed immediate intervention. | [SRC-WRITE-010] | Time from failed deploy to restored service in incident records. | exact |
| Deployment rework rate | Share of deployments that are unplanned and caused by a production incident. | [SRC-WRITE-010] | Incident-driven deploys divided by all deploys. | exact |
| DORA capability | A practice DORA's research links to delivery performance, improved instead of the metric itself. | [SRC-PM-009] | An improvement plan that targets a metric and names no capability. | judge |
| Small batch | Work sliced so it is built, checked, and released within days; over a week is too big. | [SRC-PM-010] | Branches or pull requests open longer than a week; finished slices held back to release together. | exact |
| WIP limit | An explicit cap on started but unfinished items, per column or system. | [SRC-PM-011] [SRC-PM-014] | A board with no limits, or people split across several items at once. | exact |
| Pull system | New work starts only when WIP falls below its limit. | [SRC-PM-014] | Items started while the column is at its limit. | exact |
| Invisible work | Work in the value stream that the board does not show. | [SRC-PM-011] | A board covering only development while review, release, or support waits elsewhere. | judge |
| Throughput | The exact count of items finished per unit of time. | [SRC-PM-014] | Items finished per week from the board, not points. | exact |
| Cycle time | Elapsed time from an item's start to its finish. | [SRC-PM-014] | Start and finish timestamps per item. | exact |
| Work item age | Elapsed time since an unfinished item started. | [SRC-PM-014] | An in-progress item older than the SLE with no action recorded. | exact |
| Service level expectation | A forecast of how long an item takes, with a probability, from historical cycle time. | [SRC-PM-014] | A promise made with no stated percentile or no cycle-time history behind it. | judge |
| Team types | Stream-aligned, platform, enabling, and complicated subsystem, each with a distinct purpose. | [SRC-PM-013] | A team with no stated type, or a platform team whose consumers cannot self-serve. | judge |
| Interaction mode | Collaboration for a set period, X-as-a-Service, or facilitation between two teams. | [SRC-PM-013] | A dependency between teams with no agreed mode or end date for collaboration. | judge |
| Generative culture | High-trust culture where bad news travels fast and failure leads to inquiry. | [SRC-PM-012] | A postmortem that names a person to blame, or a messenger punished. | judge |
| SPACE | Productivity read across several dimensions, never one activity number. | [SRC-PM-015] | Productivity judged by a single count such as commits, lines, or tickets closed. | judge |

## Not admitted

- Velocity or story points as a productivity or value metric: one activity
  number cannot measure productivity [SRC-PM-015]; flow counts finished items,
  not points [SRC-PM-014].
- A feature-and-date roadmap as the plan ("feature factory"): it moves value to
  the requester and measures output [SRC-PM-003] [SRC-PM-008].
- Any delivery metric as a target ("every service deploys daily by Q4"):
  invites gaming; compare a service with itself over time [SRC-WRITE-010].
- Comparing teams or ranking people by DORA metrics: they apply per service
  [SRC-WRITE-010].
- Estimates as commitments, extending a bet by default: set an appetite and
  cut scope [SRC-PM-004] [SRC-PM-006].
- Discovery as a phase that ends before delivery: it runs weekly
  [SRC-FLOW-032].
- Relaxing WIP limits when people are idle: they help elsewhere in the stream
  [SRC-PM-011].
