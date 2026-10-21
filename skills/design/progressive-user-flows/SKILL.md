---
name: progressive-user-flows
description: Use whenever designing, specifying, or reviewing a user flow or journey across screens - onboarding, sign-up, checkout, approvals, invites, account recovery, subscription changes, import and export, multi-role or collaborative workflows, AI-assisted workflows - including edge cases, error and recovery paths, interruptions, state models, and flow diagrams (User Flow, Nutzerfluss, Journey, Ablauf, Statechart, Onboarding). Not for a single form's validation, which progressive-forms-interactions owns.
license: MIT
---

# Progressive User Flows

Specify a journey so that a person can always reach their goal or a clear,
recoverable stop - and so that engineering can build every path, not only
the happy one. A flow drawn only as the happy path hides exactly the cases
engineering meets first: failures, interruptions, and missing permissions.

## Golden path

1. State the person's goal and what "done" means to them.
2. Name the trigger and entry context: where they come from, what they
   already know, which device, which role.
3. Define the start and end states, including the honest "could not
   finish" end.
4. Mark the decisions the person makes and the responses the system gives.
5. Add alternative paths (another method, skip, later) and error paths with
   their recovery; each failure keeps the person's work.
6. Model interruptions: reload, back, timeout and re-authentication, closing
   the tab, switching device, a second person editing. Time limits follow
   WCAG 2.2.1 (verified) [SRC-FLOW-007].
7. Write the state model as a Mermaid `stateDiagram-v2`, because interleaved
   async, retry, and approval states produce impossible combinations unless
   they are enumerated (supported; benefit asserted, not measured)
   [SRC-FLOW-016] [SRC-FLOW-017].
8. Check keyboard and screen reader use along the whole path, and
   assisted-digital routes for people who cannot use it (supported)
   [SRC-FLOW-005].
9. Run `scripts/flow_lint.py FLOW.md`: no unreachable state, no state
   without a way out, an error or recovery state present, all sections there.
10. Test the flow with concrete tasks (`progressive-ux-research`), then cut
    steps that add no value.
11. Hand over acceptance criteria and test scenarios per path.

## Load when

- `references/flow-spec.md` - always: the flow spec template, the edge-case
  checklist, multi-session task lists, save and resume, and the hand-over
  format.
- `references/ai-and-collaborative-flows.md` - when an AI proposes or applies
  changes, or several roles or people act on the same object.
- `references/example-approval-flow.md` - a complete worked example that
  passes `flow_lint.py`; copy its structure.

## Rules that change the result

- Every error state has a transition out that keeps the person's input.
- A flow spanning sessions starts with the fewest task statuses (completed,
  incomplete) and adds more - cannot start yet, in progress, problem - only
  when research shows people need them, and defines what "complete" means
  (supported) [SRC-FLOW-019].
- Save and resume states a retention period, because the source pattern
  leaves it open and engineering will otherwise pick one silently
  (hypothesis; the pattern itself is supported) [SRC-FLOW-018].
- A flow must stay understandable without the diagram: the written paths are
  the spec, the diagram is a check.
- Onboarding or time-to-value claims need a primary source; otherwise they
  are hypotheses (no credible primary evidence found in the 2026-10 refresh).

## Gates

Automated: `scripts/flow_lint.py` (tests in `tests/test_flow_lint.py`).
Manual: task-based walkthrough with keyboard only and with a screen reader;
review of each role's permissions; a walkthrough of every interruption.

## Done when

Every path has a start, an end, and recovery; the lint passes; acceptance
criteria and test scenarios exist per path; open assumptions are listed as
hypotheses with the test that would settle them.
