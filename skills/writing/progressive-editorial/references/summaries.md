# Summaries: PO, Management, C-Level, Customer

## PO summary

May carry more product mechanics than an executive summary.

Intent: shared product understanding, decision preparation, visible
trade-offs, next product or engineering learning.

Architecture: what changed, why it matters to the product, evidence,
trade-off or uncertainty, decision, next learning step. Default 100 to 300
words.

Golden:

<!-- golden: po_summary de -->
```text
Der Audit-Export ist technisch bereit für eine begrenzte Pilotphase. Offen ist
nicht mehr die Exportfunktion selbst. Offen ist, ob Enterprise-Admins verstehen,
wer welche Audit-Daten sehen darf, und ob die exportierten Daten ihre echten
Audit-Fragen beantworten.

Eine breite Freigabe würde ich deshalb noch nicht planen. Der nächste sinnvolle
Schritt sind drei echte Audit-Abläufe bei Kunden.

Reichen dort die vorhandenen Daten und Rollen, entscheiden wir über die breite
Verfügbarkeit. Reichen sie nicht, wissen wir früh, ob das eigentliche
Produktproblem bei der Transparenz der Berechtigungen oder beim Reporting liegt.
```

<!-- golden: po_summary en -->
```text
The Audit Export is technically ready for a limited pilot. The main open
question is no longer the export itself; it is whether enterprise admins
understand the permission boundary and whether the exported data answers real
audit questions.

I would therefore avoid planning broad availability yet. The next useful step
is three real customer workflows.

If those show that the existing data and roles are sufficient, we can decide
on broader availability. If not, we will learn early whether the actual
product problem is permission transparency or reporting.
```

Must answer: what changed, product meaning, uncertainty, next learning step.

## Executive summary (C-level, management, customer)

Executive writing is decision compression, not shortening.

Architecture: bottom line, business or customer meaning, evidence, exposure or
trade-off, recommendation or decision, next checkpoint.

Length: flash 50 to 120 words, normal brief 120 to 300, complex decision one
screen plus linked detail.

Voice: direct, calm, evidence-led, no false certainty, no management theater.
Remove implementation detail unless it changes cost, risk, timing, customer
impact, or reversibility.

Template:

```text
Bottom line:
Impact:
Evidence:
Risk:
Recommendation:
Next checkpoint:
```

Golden:

<!-- golden: executive_summary en -->
```text
**Bottom line:** The enterprise audit pilot can start without increasing the
planned technical scope.

The export path is ready, and the remaining uncertainty is now customer
behavior: whether admins can answer real audit questions with the existing
data and permissions.

**Recommendation:** Keep the release limited to three pilot customers before
broader availability. This gives us production evidence without committing to
a larger reporting or permission initiative prematurely.

**Next checkpoint:** Review after all three customers complete one real audit
workflow.
```

<!-- golden: executive_summary de -->
```text
**Kurzfassung:** Der Pilot für Enterprise-Audits kann starten, ohne den
geplanten technischen Umfang zu erweitern.

Der Export ist bereit. Unsicher ist jetzt nur noch der Ablauf beim Kunden:
Reichen die vorhandenen Daten und Berechtigungen, damit Admins ihre
Audit-Fragen selbst beantworten?

**Empfehlung:** Die Freigabe zunächst auf drei Pilotkunden begrenzen. So
sammeln wir Belege aus der echten Nutzung, bevor wir uns auf ein größeres
Vorhaben für Reporting oder Berechtigungen festlegen.

**Nächster Prüfpunkt:** Wenn jeder der drei Kunden einen echten Audit-Ablauf
abgeschlossen hat.
```

Checks: bottom line in the first 40 words; business or customer meaning;
recommendation or an explicit "no decision needed"; no ticket inventory; no
unexplained technical detail. If the numbers carry the message, also load
`plain-numbers` when installed.
