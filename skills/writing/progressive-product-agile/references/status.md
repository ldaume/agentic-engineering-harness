# Status Report

A progressive status report is not proof of being busy. Transparency means
showing the actual system, not reporting upward.

After reading, it is clear: are we moving toward the outcome, what changed,
what did we learn, what is at risk, what decision or help is needed, what
happens next.

## Architecture

Overall signal, outcome movement, what changed, evidence and learning, risks
and uncertainty, decisions needed, next focus.

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
# Status - Enterprise Audit - 21. Oktober

**Signal:** Auf Kurs für den Pilot; vor breiter Freigabe brauchen wir noch
reale Evidenz zur Permission-Nutzung.

**Outcome:** Der Export ist technisch nutzbar. Ob er Audit-bedingte
Support-Arbeit tatsächlich reduziert, können wir erst mit den drei
Pilotkunden bewerten.

**Gelernt:** Im internen Test war nicht die Exportfunktion die offene Frage,
sondern ob Admins sofort verstehen, welche Rollen welche Audit-Daten sehen
dürfen.

**Risiko:** Eine zu breite Permission könnte sensible Daten sichtbar machen.
Deshalb bleibt der erste Rollout auf drei bekannte Enterprise-Accounts
begrenzt.

**Entscheidung:** Keine zusätzliche Management-Entscheidung nötig.

**Nächster Fokus:** Ersten echten Audit-Workflow beobachten und
Permission-Fragen erfassen.
```

<!-- golden: agile_status en -->
```text
# Enterprise Audit status - October 21

**Signal:** On track for the pilot; we still need real permission-usage
evidence before broad release.

**Outcome:** The export is technically usable. We won't know whether it
reduces audit-related support work until the three pilot customers use it in
real audits.

**Learned:** The open question in internal testing was not exporting data. It
was whether admins immediately understand which roles can see which audit
data.

**Risk:** An overly broad permission could expose sensitive information, so
the first rollout remains limited to three known enterprise accounts.

**Decision:** No additional management decision required.

**Next:** Observe the first real audit workflow and capture permission
questions.
```

Checks: outcome signal, learning, risk or an explicit "none", next focus. No
activity dump as status, no velocity as outcome. With metrics, also load
`plain-numbers` when installed.
