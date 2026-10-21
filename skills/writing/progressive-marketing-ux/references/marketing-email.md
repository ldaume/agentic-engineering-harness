# Marketing Email

Moves a defined recipient toward one relevant next step. From name, subject,
and preview are the first things read; the preview complements the subject
and front-loads what matters.

## Architecture

From, subject, preview, hook or relevance, value, proof or mechanism, CTA,
optional objection handling, close.

## Workflow

1. Define segment and trigger.
2. Define one desired action.
3. Write the value proposition before the subject.
4. Identify the evidence.
5. Draft the body.
6. Draft subject and preview as a pair.
7. Make the CTA describe the next step.
8. Remove generic excitement.
9. Verify every claim.
10. Write a testable alternative subject or hook when the campaign warrants it.

German: concrete and credible, not translated advertising language. English:
conversational, benefit-led, specific.

Length: announcement 80 to 180 words, activation or nurture 120 to 250,
high-consideration B2B 180 to 400.

## Template

```text
Subject: [specific value / relevant change]
Preview: [adds context; does not repeat subject]

Hi [Name],

[Why this matters to this reader now.]

[What changed / what they get.]

[Evidence or concrete mechanism.]

[CTA]

[Optional low-pressure close]
```

Never invent urgency, social proof, customer numbers, or outcomes.

## Send readiness (Gmail)

Copy alone does not make a campaign deliverable. For marketing or
promotional mail from senders of more than 5,000 messages a day to Gmail,
one-click unsubscribe is required: `List-Unsubscribe` plus
`List-Unsubscribe-Post: List-Unsubscribe=One-Click`, an HTTPS POST target
without redirect; a visible link in the body does not satisfy it. In force
since 2024-02-01, with rejections ramping up since November 2025;
transactional mail is exempt; keep the spam rate below 0.10% and never reach
0.30% (verified) [SRC-WRITE-007] [SRC-WRITE-008] [SRC-WRITE-009]. Flag a
missing header to whoever owns the sending setup.

The CTA link text names the action ("Watch the 3-minute walkthrough"), never
"click here" (verified) [SRC-WRITE-026].

## Golden example

Input: feature automated audit evidence export; audience enterprise admins;
benefit: exports existing audit data without a support request; CTA: 3-minute
walkthrough; no performance metrics yet.

<!-- golden: marketing_email de -->
```text
Betreff: Audit-Nachweise ohne Support-Anfrage exportieren
Preview: Der neue Export nutzt die Audit-Daten, die bereits in deinem Workspace liegen.

Hallo [Name],

wenn du für einen Audit-Nachweis bisher erst Daten über den Support anfordern
musstest, geht das jetzt direkt.

Mit dem neuen Audit-Export lädst du die vorhandenen Audit-Daten selbst aus
deinem Workspace herunter, in dem Format, das du für den Nachweis brauchst.

Der Walkthrough zeigt in drei Minuten, wo du den Export findest und welche
Rolle du dafür brauchst.

[3-Minuten-Walkthrough ansehen]

Viele Grüße
[Name]
```

<!-- golden: marketing_email en -->
```text
Subject: Export audit evidence without a support request
Preview: The new export uses the audit data already available in your workspace.

Hi [Name],

If preparing an audit has meant asking support to pull data for you, you can
now do it yourself.

The new Audit Export lets you download the audit data already in your
workspace, in the format your evidence request needs.

The walkthrough shows in three minutes where to find the export and which role
it requires.

[Watch the 3-minute walkthrough]

Best,
[Name]
```

Checks: subject, preview, one primary CTA; preview adds to the subject; value
is specific; no unsupported percentage or fake urgency.
