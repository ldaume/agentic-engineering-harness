# Guiding Screens

Load this when a screen tells someone what to do next: task or status views,
approval and review flows, workflow dashboards, or any surface where a person
waits on, or acts for, a process. Each rule gives the principle and its reason.

## 1. The first viewport answers three questions

For whoever is looking at it now: what is happening, why, and what to do next.

- Show at most one primary act. Two equal calls to action make the viewer
  decide which matters; the screen should have decided already.
- When there is nothing for this viewer to do, say so, then say when they will
  be needed again and how they will be brought back: a time estimate, a
  notification, or "this updates by itself". Silence reads as "broken" or
  "I should poll".

Example: "Your export is being prepared. Nothing to do. About 10 minutes; we
will email you when it is ready."

## 2. The server computes the acts a viewer can take

Return a typed list, one entry per act: `kind`, `available`, `primary`, a label
per audience, and a `reason` when unavailable. The client renders it and
derives nothing. Permission and state logic duplicated in the client drifts
from the server, and the button then promises what the server refuses.

- Show an act only when it would succeed now.
- Show it disabled, with its reason, only when a person would otherwise look
  for it (for example "Approve" for a reviewer while a check still runs).
- Say "your turn" only to the person whose turn it is. Everyone else reads who
  the process waits on.

```json
{ "kind": "approve", "available": false, "primary": false,
  "label": { "plain": "Approve", "technical": "Approve change" },
  "reason": "Waiting for the automated checks to finish." }
```

## 3. A CTA at the top whose detail lives below

If the detail needed to act is further down the page, the button scrolls to it
and opens it. It does not copy the detail into the header, which would leave
two places to keep in sync.

- Only acts that need nothing more to read act in place (for example
  "Resume").
- The button uses the same verb as the status sentence ("Review the draft" /
  "Review"), so the sentence and the button read as one instruction.

## 4. Link to where the person can check

Wherever a person must verify or judge something, link straight to the place
where they can see it: the changed page, or the preview at the same path.
Making them navigate there themselves is where reviews get skipped.

- Compose links server-side from relative paths plus a configured base.
- Validate the host against an allowlist.
- Never accept a full URL from untrusted input and render it as a link. That is
  an open redirect and a phishing vector.

## 5. Two registers for audiences with different vocabularies

Audiences such as a non-technical owner and an engineer need the same facts in
their own words. One register serves neither.

- Plain register: no identifiers, branch names, hashes, status codes, or
  snake_case or camelCase tokens.
- Enforce it with a deterministic check, not a reviewer's eye: reject
  identifier-shaped tokens (long hex runs, `a_b` / `aB` tokens, path-like
  strings, numeric codes) in plain text.
- Machine-written text (model output, generated summaries) must be produced in
  both registers, and the plain one passes the same check before it is shown.

## 6. A suggestion names the same act as the button

When an assistant or agent suggests something, its wording names the act that
the button carrying it performs, so accepting the suggestion is one click on
the thing it named. Put the reason next to the suggestion. A reason hidden
behind a tab, tooltip, or "details" view gets skipped, and an unexplained
suggestion is one people learn to ignore.

## Checks

- Cover each rule with a test on the contract: the act list for each viewer
  state, the link composer rejecting foreign hosts, and the plain-register
  check failing on an identifier.
- Test the "nothing to do" state and the "not your turn" state as first-class
  views, not as empty cases.
