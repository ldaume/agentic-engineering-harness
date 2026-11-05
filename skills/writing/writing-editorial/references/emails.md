# Email

An email moves a relationship or a decision forward efficiently. It is neither
a mini memo nor a chat message.

Modes: inform, request, decide, coordinate, follow up, decline, resolve,
thank, introduce, escalate.

## Audience

Settle: relationship (close, colleague, manager, customer, unknown), power
distance (peer, upward, downward), shared context (high, medium, low),
sensitivity, and whether action is required.

## Architecture

Default: subject, opening or human context, point, necessary context, action
or decision or question, timing if relevant, close.

High shared context: point, context, ask.

## Workflow

1. Name the single job of the email.
2. Determine what the recipient already knows.
3. Write the ask or message in one sentence.
4. Add only the context needed to understand or act.
5. Move the important point up.
6. Remove defensive explanation.
7. Check names, dates, attachments, action owner.
8. Native-language edit.

Length: quick coordination 30 to 90 words, business request 60 to 180,
sensitive or context-heavy 120 to 300.

## Templates

```text
Betreff: [Ergebnis oder Thema]

Hi [Name],

[kurzer Kontext, falls nötig]

[Hauptaussage.]

[Relevanter Kontext / Konsequenz.]

[Konkrete Frage oder nächster Schritt] bis [Zeitpunkt]?

Danke
[Name]
```

```text
Subject: [Outcome or topic]

Hi [Name],

[Context if needed.]

[Main point.]

[Relevant implication.]

[Clear request or next step] by [time]?

Thanks,
[Name]
```

## Quality gate

- One clear purpose; main point visible in the first third.
- Ask or decision unambiguous; recipient knows who does what next.
- No invented facts, no unnecessary autobiography.
- Tone fits the relationship; subject predicts the content.

## Golden example

Input: Anna must decide whether audit export ships Friday. Security review is
done. One open UX issue affects labels only, not functionality. Answer needed
tomorrow noon.

<!-- golden: business_email de -->
```text
Betreff: Entscheidung zum Audit-Export am Freitag

Hi Anna,

der Security Review ist abgeschlossen. Offen ist nur noch ein UX-Thema bei den
Labels; die Funktion selbst ist davon nicht betroffen.

Mein Vorschlag ist, am Freitag wie geplant zu releasen und die Labels separat
nachzuziehen.

Kannst du uns bis morgen 12 Uhr kurz bestätigen, ob wir so vorgehen?

Danke
Alex
```

<!-- golden: business_email en -->
```text
Subject: Decision on Friday's audit export release

Hi Anna,

The security review is complete. The only open issue is a UX detail in the
labels; functionality is unaffected.

My recommendation is to release on Friday as planned and address the labels
separately.

Could you confirm by noon tomorrow whether we should proceed?

Thanks,
Alex
```
