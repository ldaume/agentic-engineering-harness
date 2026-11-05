# Slack

Async messages need enough context to act on without a follow-up question,
scannable phrasing, and threads for detail. A reaction beats an
acknowledgement message. Sensitive topics or big direction changes may
deserve a call instead; say so rather than typing a wall.

Slack is more direct than email, not semantically sloppier.

Intents: signal, inform, coordinate, ask, decide, unblock, summarize, hand
off.

## Architecture

- Normal: context or headline, state, meaning, ask or next step.
- Update: signal, meaning, next.
- Decision request: decision, why now, options and trade-off, recommendation,
  what you need from whom by when.

Length: simple 1 to 4 lines, update 50 to 150 words, decision context 100 to
250. More than that: link a durable document plus a short summary.

No email salutation ("Hi Anna," on its own line), no sign-off.

## Template

```text
Heads-up: [what changed].

[What it means.]

Next: [owner/action/time].
```

## Golden example

<!-- golden: slack de -->
```text
Kurzes Update zum Audit-Export: Der Security Review ist durch. Offen ist nur
noch die Benennung von zwei Labels; das blockiert die Funktion nicht.

Mein Vorschlag: Freitag releasen, Labels separat nachziehen.

@Anna - Einwand dagegen bis morgen 12 Uhr? Sonst gehen wir damit weiter.
```

<!-- golden: slack en -->
```text
Audit Export update: security review is complete. The only open item is the
wording of two labels; it doesn't block the feature.

Recommendation: release Friday and follow up on the labels separately.

@Anna - any objection by noon tomorrow? Otherwise we'll proceed.
```

## Checks

Under 200 words; when actionable, a next step and an owner or audience; not
formatted like an email; no memo length without a link.
