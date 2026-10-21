# Adaptive Roadmap

A roadmap connects strategic intent, outcomes, opportunity areas, candidate
bets, confidence, investment boundary, and learning milestones. Now, Next,
Later focuses on goals and strategy rather than exact dates.

## Architecture

Strategic intent, desired outcomes, opportunity areas, current focus or bets,
evidence and confidence, investment boundary, learning milestones, next
candidate space.

## Template

```text
# Adaptive Roadmap - [Product]

## Strategic intent

## Desired outcomes

## Now
Outcome:
Opportunity:
Current bet:
Evidence:
Confidence:
Investment boundary:
Learning milestone:

## Next
Opportunity space:
Why it may matter:
What must be learned first:

## Later
Strategic possibilities, not commitments:

## Changed since last review

## Decisions / constraints
```

## Golden example

<!-- golden: fast_roadmap en -->
```text
# Adaptive Roadmap - Enterprise Trust

## Strategic intent

Make enterprise administration trustworthy enough that audit and permission
workflows no longer require bespoke support.

## Desired outcome

Enterprise admins can answer routine audit questions from the product with
appropriate access controls.

## Now

**Opportunity:** Audit evidence retrieval
**Bet:** Minimal Audit Export
**Confidence:** Medium
**Investment boundary:** First three customer pilots
**Learning milestone:** Three admins complete a real audit evidence request
without an engineering data pull.

## Next

**Opportunity:** Permission transparency

We need to understand whether the current role model is sufficient before
committing to a new permission workflow.

## Later

Potential opportunity spaces:
- admin activity review
- broader reporting
- permission review workflow

These are possibilities, not delivery commitments.
```

<!-- golden: fast_roadmap de -->

```text
# Adaptive Roadmap - Enterprise Trust

## Strategische Absicht

Die Enterprise-Administration so vertrauenswürdig machen, dass Audit- und
Berechtigungsfragen keinen individuellen Support mehr brauchen.

## Gewünschtes Outcome

Enterprise-Admins beantworten wiederkehrende Audit-Fragen direkt im Produkt,
mit passenden Zugriffsrechten.

## Jetzt

**Opportunity:** Audit-Nachweise abrufen
**Bet:** Minimaler Audit Export
**Zuversicht:** Mittel
**Investitionsgrenze:** Die ersten drei Kundenpiloten
**Lern-Meilenstein:** Drei Admins erledigen eine echte Audit-Anfrage ohne
Datenabzug durch das Engineering.

## Als Nächstes

**Opportunity:** Transparenz bei Berechtigungen

Bevor wir einen neuen Berechtigungs-Workflow zusagen, müssen wir verstehen, ob
das heutige Rollenmodell reicht.

## Später

Mögliche Opportunity-Felder:
- Admin-Aktivitäten prüfen
- breiteres Reporting
- Workflow für Berechtigungs-Reviews

Das sind Möglichkeiten, keine Lieferzusagen.
```

Checks: strategic intent, outcome, current learning, confidence or
uncertainty, investment boundary. Reject static team assignment presented as
FaST and feature calendars disguised as outcome roadmaps.
