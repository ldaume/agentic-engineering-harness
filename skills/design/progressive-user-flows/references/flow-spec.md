# Golden Path: Flow Specification

## Template

Copy this structure; `scripts/flow_lint.py` checks the sections and the
state diagram. German headings work as well (Hauptweg, Alternative Wege,
Fehler und Wiederherstellung, Unterbrechung und Wiederaufnahme, Zustände).

```markdown
# Flow: <goal in the person's words>

Person and context: <role, device, where they come from, what they know>
Done means: <the outcome for the person, not the screen>

## Happy path
1. <step> - system response - what the person sees and hears

## Alternative paths
- <another method, skip, do later> - where it rejoins

## Error and recovery
| Failure | Detected by | What the person sees | Recovery | Input kept |
|---|---|---|---|---|

## Interruptions and resume
| Interruption | State kept | Resume entry | Retention |
|---|---|---|---|

## Roles and permissions
| Role | Can | Cannot | What they see instead |
|---|---|---|---|

## States
<mermaid stateDiagram-v2>

## Acceptance criteria and test scenarios
- Given <state>, when <event>, then <observable result>

## Analytics events
| Event | When | Question it answers |
|---|---|---|

## Assumptions to test
- <assumption> - test: <smallest study that settles it>
```

## Edge-case checklist

Check each; write "not applicable because ..." rather than skipping silently.

| Case | Typical failure | Expected design |
|---|---|---|
| Slow or no connection | Spinner forever | Timeout with retry, input kept, offline notice |
| Timeout | Lost work | Turn off, adjust, or extend (2.2.1, verified) [SRC-FLOW-007]; keep data (2.2.6, AAA) [SRC-FLOW-009] |
| Session expiry | Silent redirect to login | Re-authenticate and return with data (2.2.5, AAA) [SRC-FLOW-008] |
| Double action | Two orders | Idempotent request, second activation ignored |
| Reload or back | Form reset, duplicate POST | Restored state, POST-redirect-GET |
| Missing permission | Dead button | Explain who can, offer to request access |
| Partially saved data | Unclear state | Show what is saved, what is not, how to finish |
| Invalid input | Generic error | Field-level fix, see progressive-forms-interactions |
| Lost focus | Keyboard users stranded | Focus to the new content's heading or the error |
| Screen reader | Silent updates | Status region or focus move per change |
| Mobile keyboard | Wrong input type | `type`, `inputmode`, `autocomplete` per field |
| Resume after a break | Start over | Task list with statuses, resume link [SRC-FLOW-019] |
| Concurrent edit | Last write wins silently | Detect, show both versions, let the person choose |
| Unclear AI result | Applied blindly | Proposal with accept, edit, reject, retry, undo [SRC-FLOW-014] |

## Multi-session work

Use a task list when a service has independent sections that people finish
over several visits: each task has a status, statuses are text, never color
alone, and "problem" is not styled as an error unless it is one
(supported) [SRC-FLOW-019].

## Save and resume

Offer "Save and come back later" next to the primary action, confirm what was
saved, and warn before sign-out loses anything (supported) [SRC-FLOW-018];
state the retention period in the spec, because the source leaves it open
(hypothesis). AAA timeouts keep
data for at least 20 hours or warn at the start (verified) [SRC-FLOW-009].

## Assisted digital

Name the route for people who cannot use the digital service, and include
them and their helpers in research (supported) [SRC-FLOW-005].

## Hand-over to engineering

Per path: acceptance criteria in Given/When/Then, the states and transitions
it covers, the analytics events, and the accessibility expectation (focus
target, announcement). Engineering should be able to write the tests from the
spec without asking.

## Anti-patterns

Happy-path-only specs; time limits without extension; error styling for
non-error statuses; personas or journeys built from analytics alone
[SRC-FLOW-004]; "5 users" quoted as proof a flow works [SRC-FLOW-001]
[SRC-FLOW-002].

## Agent prompt

"Write the flow spec for <goal> using `references/flow-spec.md`. Fill every
edge-case row or state why it does not apply. Draw the states as Mermaid
`stateDiagram-v2`, then run `scripts/flow_lint.py` and fix every error."
