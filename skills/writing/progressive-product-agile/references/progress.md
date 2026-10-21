# Progress Document

Under uncertainty, progress is not percent complete. Shape Up's hill chart
is a useful model: uphill is figuring out the unknowns, downhill is executing
the known. "The central uncertainty is resolved" usually carries more
information than "70% done". The hill chart is a lens, not a required metric.

## Architecture

Goal, current state, what is now true that was not before, unknowns retired,
unknowns remaining, evidence, scope or decision change, next breakthrough.

## Template

```text
# Progress - [Bet]

## Goal

## Current state

## Progress since last update
- product
- technical
- user/business evidence
- quality/operations

## Uncertainty retired

## Remaining uncertainty

## Scope / decision changes

## Next breakthrough

## Signals to watch
```

## Golden example

<!-- golden: agile_progress en -->
```text
# Progress - Minimal Audit Export

## Goal

Let enterprise admins retrieve the evidence needed for routine audits without
bespoke engineering support.

## Current state

The end-to-end path works in the pilot environment: permission check, export
request, generated file, audit data review.

## Progress since last update

The feasibility question is settled: the file can be generated from
production-shaped data. That was the main risk; the remaining UI work is
known.

## Uncertainty retired

- export can run within the existing service boundary
- current data model contains the fields needed for the first pilot

## Remaining uncertainty

- whether admins understand the permission boundary
- whether exported fields match actual audit questions

## Next breakthrough

Run the workflow with the first customer admin using a real audit request.
```

<!-- golden: agile_progress de -->

```text
# Fortschritt - Minimaler Audit-Export

## Ziel

Enterprise-Admins rufen die Nachweise für Routine-Audits selbst ab, ohne
individuelle Hilfe aus dem Engineering.

## Aktueller Stand

Der Ablauf funktioniert durchgängig in der Pilotumgebung: Berechtigung prüfen,
Export anfordern, Datei erzeugen, Audit-Daten sichten.

## Fortschritt seit dem letzten Update

Die Machbarkeit ist geklärt: Die Datei lässt sich aus produktionsnahen Daten
erzeugen. Das war das größte Risiko; die restliche Arbeit an der Oberfläche ist
bekannt.

## Geklärte Unsicherheit

- der Export läuft innerhalb der bestehenden Service-Grenze
- das Datenmodell enthält alle Felder für die erste Pilotphase

## Offene Unsicherheit

- ob Admins verstehen, wer welche Daten sehen darf
- ob die exportierten Felder zu den echten Audit-Fragen passen

## Nächster Durchbruch

Den Ablauf mit dem ersten Kunden-Admin und einer echten Audit-Anfrage
durchspielen.
```

Checks: goal, current state, change in uncertainty, next breakthrough. Reject
percent complete without a model behind it.
