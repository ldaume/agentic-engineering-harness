# Confluence Documentation

Confluence is learning memory, not storage. Atlassian's own content
foundations ask for clear, concise, consistent language (supported)
[SRC-WRITE-030]. Use a clear page hierarchy,
labels, and templates; keep pages findable and current.

Each page is mainly one of: reference, decision, procedure, working document,
product context, status, learning.

## Universal header

Title, purpose, audience, owner, status, last reviewed, decision or outcome if
applicable.

## Architectures

- Reference: purpose, context, model, details, examples, related decisions,
  owner and review trigger.
- Decision: decision, context, drivers, options, trade-offs, consequences,
  review trigger.
- Procedure: goal, prerequisites, steps, verification, failure and recovery.

## Workflow

1. Decide the document type.
2. Give the page one durable purpose.
3. Put current state or decision first.
4. Separate current truth from history.
5. Link source decisions instead of duplicating them.
6. Add owner and review trigger when staleness matters.
7. Archive superseded pages.

Length: as long as needed; split independent concerns into linked pages when
readers have different tasks or owners. Produce durable documentation, not
meeting minutes.

## Golden example

<!-- golden: confluence en -->
```text
# Audit export rollout decision

**Purpose:** Record how the first enterprise rollout will work.
**Owner:** Enterprise product group
**Status:** Accepted
**Review trigger:** First three pilot outcomes

## Decision

Release Audit Export to three pilot accounts behind the existing enterprise
entitlement before broad availability.

## Why

The export path is technically ready, but we still need production evidence
about audit workflow fit and permission expectations.

## Trade-offs

A limited pilot gives us slower initial reach, but it lets us validate
operational and permission assumptions before making the workflow broadly
available.

## Success signals

- pilot admins can retrieve required evidence without a support data pull
- no permission-related incident
- support can explain the workflow without bespoke engineering help

## Next review

Review after the third pilot has completed one real audit workflow.
```

<!-- golden: confluence de -->

```text
# Entscheidung zum Rollout des Audit-Exports

**Zweck:** Festhalten, wie der erste Enterprise-Rollout abläuft.
**Verantwortlich:** Produktgruppe Enterprise
**Status:** Beschlossen
**Review-Auslöser:** Ergebnisse der ersten drei Pilotkunden

## Entscheidung

Der Audit-Export geht zuerst an drei Pilotkunden, hinter der bestehenden
Enterprise-Berechtigung, bevor er allgemein verfügbar wird.

## Warum

Der Export ist technisch bereit. Was fehlt, sind Belege aus der Produktion:
Passt der Ablauf zu echten Audits, und stimmen die Erwartungen an die
Berechtigungen?

## Trade-offs

Eine begrenzte Pilotphase erreicht anfangs weniger Kunden. Dafür prüfen wir
Annahmen zu Betrieb und Berechtigungen, bevor der Ablauf breit verfügbar ist.

## Erfolgssignale

- Admins der Pilotkunden finden die nötigen Nachweise ohne Datenabzug durch
  den Support
- kein Vorfall im Zusammenhang mit Berechtigungen
- der Support erklärt den Ablauf ohne Spezialhilfe aus dem Engineering

## Nächstes Review

Sobald der dritte Pilotkunde einen echten Audit-Ablauf abgeschlossen hat.
```

Checks: purpose, current state or decision, durable context. Reject
transcripts without synthesis and unexplained stale status.
