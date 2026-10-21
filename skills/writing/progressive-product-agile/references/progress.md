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

The important progress is not the completed export UI. We have removed the
feasibility uncertainty around generating the file from production-shaped
data.

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
# Fortschritt - Minimaler Audit Export

## Ziel

Enterprise-Admins rufen die Nachweise für Routine-Audits selbst ab, ohne
individuelle Hilfe aus dem Engineering.

## Aktueller Stand

Der Weg funktioniert durchgängig in der Pilot-Umgebung: Berechtigung prüfen,
Export anfordern, Datei erzeugen, Audit-Daten sichten.

## Fortschritt seit dem letzten Update

Der wichtige Fortschritt ist nicht die fertige Export-Oberfläche. Wir wissen
jetzt, dass sich die Datei aus produktionsnahen Daten erzeugen lässt; diese
Machbarkeitsfrage ist vom Tisch.

## Geklärte Unsicherheit

- der Export läuft innerhalb der bestehenden Service-Grenze
- das Datenmodell enthält alle Felder für den ersten Pilot

## Offene Unsicherheit

- ob Admins die Berechtigungsgrenze verstehen
- ob die exportierten Felder zu den echten Audit-Fragen passen

## Nächster Durchbruch

Den Workflow mit dem ersten Kunden-Admin und einer echten Audit-Anfrage
durchspielen.
```

Checks: goal, current state, change in uncertainty, next breakthrough. Reject
percent complete without a model behind it.
