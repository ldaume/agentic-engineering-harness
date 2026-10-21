# Pull Request Description

A PR description minimizes the time from "what am I looking at?" to "I
understand the change, the reason, the risk, and how to review it". Use the
repository's PR template when one exists; fill it with the content below.

## Architecture

- Small PR: Why, What changed, Validation.
- Larger or riskier PR: Context, Approach, Key changes, Review focus,
  Validation, Risk and rollout, Follow-up.

## Workflow

1. Read the diff and the linked issue.
2. Reconstruct the behavioral change.
3. Explain why before listing changes.
4. Identify reviewer-sensitive decisions.
5. State exactly what was tested, with the command when known.
6. Keep "not tested" visibly separate from "passed".
7. Surface migration, rollback, and compatibility implications.
8. Remove diff narration the reviewer can see directly.

Never claim a test run without evidence (command output in the session, CI
result, or the user's statement).

## Golden example

<!-- golden: pull_request en -->
```text
## Why

Enterprise admins need to request audit evidence without a support-side data
pull.

## What changed

This adds the first end-to-end export path:

- validates the caller's existing audit permission
- creates an export from the current audit dataset
- exposes the generated file through the admin workflow

No new permission type is introduced.

## Review focus

Please focus on the authorization boundary in `AuditExportService` and the
behavior when export generation fails after the request has been accepted.

## Validation

- unit tests for permission and export-state transitions
- integration test for successful export generation
- manual pilot-workflow check in the development environment

## Rollout

The endpoint remains behind the existing enterprise entitlement. Broader
customer rollout is handled separately.
```

Checks: why, behavioral change, validation; claimed tests exist. Reject a
file-by-file diff summary as primary content and fabricated test execution.
