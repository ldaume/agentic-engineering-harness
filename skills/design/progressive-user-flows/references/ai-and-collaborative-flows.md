# AI-Assisted and Collaborative Flows

## AI proposes, the person decides

- Show an AI change as a reviewable proposal before it applies, with accept,
  edit, reject or dismiss, retry, and undo next to the output (supported)
  [SRC-FLOW-014] [SRC-FLOW-015] [SRC-FLOW-010].
- Destructive, hard-to-reverse, or costly AI actions need an explicit
  confirmation that names the consequence (supported) [SRC-FLOW-014].
- A correction applies at once, persists, and can itself be corrected
  (supported) [SRC-FLOW-015].
- When the AI cannot help, say what it cannot do and offer a manual or human
  route (supported) [SRC-FLOW-012] [SRC-FLOW-020].
- Long AI operations say what they are doing, not "Processing..."
  [SRC-FLOW-014].

## Explanations are not a safety net

Lab studies found that explanations can raise acceptance of wrong AI output;
cognitive forcing (decide before seeing the AI answer) reduced over-reliance
but was rated worse by participants (context-dependent) [SRC-FLOW-028]
[SRC-FLOW-029]. So: validate any confidence or explanation display with test
users before relying on it [SRC-FLOW-013], and use a forcing step only for
high-stakes accept decisions.

## Agent supervision

Developers supervising coding agents plan and scope up front, monitor while
the agent runs, and review afterwards; a final diff alone is not enough
(hypothesis; small 2025-2026 preprint samples read at abstract level)
[SRC-FLOW-024] [SRC-FLOW-025] [SRC-FLOW-026].

## Collaborative and multi-role flows

- Each role's actions, blocked actions, and what they see instead go into the
  roles table of the spec.
- Concurrent edits are detected, never resolved by silent last-write-wins:
  show both versions and let the person choose (hypothesis).
- Hand-offs between roles name the next owner and notify them; the requester
  sees the current owner and status.
- An approval that waits longer than its deadline escalates or expires in a
  stated way; nothing waits forever.

## States to model

proposed, under review, changes requested, approved, applied, rejected,
reverted, expired, conflict - and from every one of them a way out.

## Evidence gaps

No NN/g article on AI trust, undo, or review-before-apply was found in the
2026-10 refresh; no controlled study of diff-review interfaces exists yet.
