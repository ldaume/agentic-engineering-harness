# Status Report

A progressive status report is not proof of being busy. Transparency means
showing the actual system, not reporting upward.

After reading, it is clear: are we moving toward the outcome, what changed,
what did we learn, what is at risk, what decision or help is needed, what
happens next.

## Architecture

Overall signal, outcome movement, what changed, evidence and learning, risks
and uncertainty, decisions needed, next focus.

When a status reports delivery performance, use DORA's five metrics in two
groups - throughput (change lead time, deployment frequency, failed
deployment recovery time) and instability (change fail rate, deployment
rework rate) - and do not call them "four keys" (verified) [SRC-WRITE-010].
For AI claims, DORA 2025 frames AI as an amplifier of existing strengths and
weaknesses (supported) [SRC-WRITE-011] [SRC-WRITE-012]; do not quote 2024
percentages as current.

Not "completed 14 tickets", "velocity 42", or "sprint 83% complete", unless
such a number answers a real question the reader has.

## Template

```text
# Status - [Area] - [Date]

## Signal
[On track / attention / decision needed] + one-sentence meaning

## Outcome
[Movement or current evidence]

## Changed
[Meaningful product/system changes]

## Learned
[What evidence changed our understanding]

## Risks
[Risk + consequence + response]

## Decisions
[Decision, owner, date]

## Next
[Next learning/delivery focus]
```

## Golden example

<!-- golden: agile_status de -->
```text
# Status - Enterprise-Audit - 21. Oktober

**Signal:** Auf Kurs für die Pilotphase. Vor einer breiten Freigabe brauchen
wir noch Belege, wie Admins die Berechtigungen tatsächlich nutzen.

**Outcome:** Der Export ist technisch nutzbar. Ob er die Supportarbeit rund um
Audits wirklich senkt, zeigen erst die drei Pilotkunden.

**Gelernt:** Im internen Test lief der Export problemlos. Offen blieb, ob
Admins sofort verstehen, welche Rolle welche Audit-Daten sieht.

**Risiko:** Eine zu weit gefasste Berechtigung könnte sensible Daten sichtbar
machen. Deshalb bleibt der erste Rollout auf drei bekannte Enterprise-Accounts
begrenzt.

**Entscheidung:** Keine zusätzliche Management-Entscheidung nötig.

**Nächster Fokus:** Den ersten echten Audit-Ablauf begleiten und Fragen zu
Berechtigungen sammeln.
```

<!-- golden: agile_status en -->
```text
# Enterprise Audit status - October 21

**Signal:** On track for the pilot; we still need evidence of how admins use
permissions before a broad release.

**Outcome:** The export is technically usable. We won't know whether it
reduces audit-related support work until the three pilot customers use it in
real audits.

**Learned:** In internal testing the export itself worked. The open question
is whether admins immediately understand which roles can see which audit data.

**Risk:** An overly broad permission could expose sensitive information, so
the first rollout remains limited to three known enterprise accounts.

**Decision:** No additional management decision required.

**Next:** Observe the first real audit workflow and capture permission
questions.
```

Checks: outcome signal, learning, risk or an explicit "none", next focus. No
activity dump as status, no velocity as outcome. With metrics, also load
`plain-numbers` when installed.
