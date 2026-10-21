# Product Documents

Not every product question fits a user story. The original story idea is
card, conversation, confirmation, with detail growing as the horizon nears.
Choose the smallest artifact that supports the decision at hand, and do not
turn it into a feature specification unless a solution commitment is actually
required.

## Routing

| Need | Artifact |
|---|---|
| understand a problem | Problem Brief |
| choose an investment | Bet Brief |
| test an uncertainty | Experiment Card |
| record a durable decision | Decision Record |
| assess impact | Outcome Review |

Keep evidence and assumptions in separate sections, because a reader must be
able to tell what was observed from what is hoped.

## Problem Brief

```text
# Problem Brief
## Problem
## Segment
## Observed behavior
## Evidence
## Impact
## Desired outcome
## Unknowns
## Risks
## Non-goals
## Decision needed
## Next learning step
```

## Bet Brief

```text
# Bet Brief
## Outcome
## Problem / opportunity
## Why now
## Evidence
## Assumptions
## Risks
## Appetite / investment boundary
## Solution direction
## Non-goals
## Quality / security / operability
## Learning plan
## Kill / pivot criteria
```

## Experiment Card

```text
# Experiment
## Hypothesis (We believe ... for ... will ...)
## Riskiest assumption
## Method
## Signal and threshold
## Time box / cost
## Decision on result (persevere / pivot / stop)
```

## Decision Record

```text
# Decision: [title]
## Status
## Context
## Decision
## Options considered
## Trade-offs
## Consequences
## Review trigger
```

## Outcome Review

```text
# Outcome Review - [Bet]
## Intended outcome
## What happened (evidence)
## What we learned
## What surprised us
## Decision (scale / iterate / stop)
## Follow-up bets or questions
```

## Golden example

<!-- golden: product_document en -->
```text
# Problem Brief - Enterprise audit evidence

## Problem

Enterprise admins cannot answer recurring audit evidence requests without
manual support or engineering help.

## Segment

Enterprise accounts subject to recurring security or compliance reviews.

## Evidence

- recurring support requests for audit data
- renewal conversations in which auditability is discussed
- current workflow requires manual data preparation

## Desired outcome

Admins can retrieve the evidence needed for routine audits through an
appropriately permissioned product workflow.

## Unknowns

- which evidence is common across audits
- whether export is enough
- which roles should have access

## Non-goals

- full BI capability
- bespoke reporting for every customer

## Decision needed

Is this problem valuable enough for a bounded pilot bet?
```

<!-- golden: product_document de -->

```text
# Problem Brief - Audit-Nachweise im Enterprise-Segment

## Problem

Enterprise-Admins können wiederkehrende Audit-Anfragen nicht ohne manuelle
Hilfe von Support oder Engineering beantworten.

## Segment

Enterprise-Accounts mit regelmäßigen Security- oder Compliance-Prüfungen.

## Evidenz

- wiederkehrende Support-Anfragen nach Audit-Daten
- Verlängerungsgespräche, in denen Auditierbarkeit Thema ist
- der heutige Ablauf verlangt manuelle Datenaufbereitung

## Gewünschtes Outcome

Admins rufen die Nachweise für Routine-Audits über einen passend
berechtigten Produkt-Workflow selbst ab.

## Unbekannt

- welche Nachweise über alle Audits hinweg gleich sind
- ob ein Export reicht
- welche Rollen Zugriff bekommen sollen

## Nicht-Ziele

- vollständige BI-Funktionalität
- individuelles Reporting pro Kunde

## Offene Entscheidung

Ist das Problem wertvoll genug für einen begrenzten Pilot-Bet?
```

Checks: problem before solution, evidence, unknowns, decision or learning
step. Reject fabricated customer evidence and story format by default.
