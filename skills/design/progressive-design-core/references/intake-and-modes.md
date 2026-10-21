# Intake and Working Modes

## Context to establish

Fill from the repository, tickets, analytics, screenshots, and conversation.
Ask only for what changes the design; record the rest as an explicit
assumption with the test that would check it.

| Context | Why it matters |
|---|---|
| Person and situation of use (role, device, frequency, environment) | Density, input method, and pacing differ for daily experts and first-time visitors |
| The problem and today's friction | Without it the design optimizes appearance |
| Desired outcome and how it is observed | Decides what "better" means and what to measure |
| Product and business goal | Settles trade-offs the person's view cannot |
| Platform and stack, existing product or greenfield | Constrains components, motion, and performance budgets |
| Brand and design-system constraints | What is fixed and what may vary |
| Accessibility target (default WCAG 2.2 AA) | Conformance, not WCAG 3 drafts [SRC-A11Y-001] [SRC-A11Y-002] |
| Existing research and data | Prevents re-asking what is known and inventing what is not |
| Critical journeys | Where a defect costs most |
| Time and technical constraints | Shapes the smallest useful slice |

## Modes

Pick one mode per request; it sets the output and stops the work at the right
place.

| Mode | When | Output |
|---|---|---|
| Explore | The problem or direction is unclear | Problem statement, assumptions, two or three options with risks, the smallest test |
| Design | The problem is clear, a solution is needed | Direction, information architecture, flow, states, components, visual spec, accessibility requirements |
| Build | A design exists or the task is implementation | Working code via `frontend-craft`, tests, screenshots where possible, decision notes |
| Review | Something exists and needs judging | Findings with evidence and severity, priorities, validation plan (`progressive-design-review`) |
| Improve | A known issue needs a targeted change | Small reversible changes, regression tests, before and after |
| Research refresh | The knowledge base may be stale | Updated registry entries, changed or deprecated rules, changelog (`research-refresh.md`) |

## Assumptions

Write them as "Assumption: ... Test: ... Risk if wrong: ...". An assumption
without a test is a guess presented as a plan.
