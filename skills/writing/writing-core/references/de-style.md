# House Style Deutsch

Basis: das Amtliche Regelwerk des Rats für deutsche Rechtschreibung in der
Fassung 2024. Es ist seit dem 1. Juli 2024 für Schule und Verwaltung
verbindlich, mit Übergangsfristen der staatlichen Stellen (verified)
[SRC-WRITE-041]; ein Stichtag Juli 2025 ist nicht belegt. Dazu die Regeln,
wie Duden sie erklärt [SRC-WRITE-035]. Für breit adressierte Produkt- und
Business-Texte gilt als Default: logische kurze Sätze, aktive Verben, direkte
Ansprache, notwendige Fachbegriffe erklären (supported) [SRC-WRITE-004]
[SRC-WRITE-020].

Anker für verständliche Sprache: DIN 8581-1:2024-05 "Einfache Sprache -
Anwendung für das Deutsche", sie baut auf DIN ISO 24495-1 auf und macht
deren Empfehlungen für das Deutsche konkret (verified) [SRC-WRITE-038]
[SRC-WRITE-037]. Einfache Sprache richtet sich an eine breite fachliche
Leserschaft. Leichte Sprache ist etwas anderes: Sie richtet sich an Menschen
mit kognitiven Einschränkungen und hat eigene Regeln, die DIN 8581-1
ausdrücklich nicht regelt [SRC-WRITE-038]. Der Text der Norm war nicht
einsehbar; die Zahlenwerte im Reference-Page-Profil (`quality-model.md`)
stammen nicht daraus.

## Regeln

- Idiomatisches Hochdeutsch, nicht übersetztes Englisch.
- Konkrete Verben statt Nominalstil: "Wir prüfen den Export" statt "Die
  Durchführung der Prüfung des Exports erfolgt".
- Fachsprache nur dort, wo die Zielgruppe sie wirklich nutzt.
- Komposita sind erlaubt; kognitiv schwere Ketten auflösen
  ("Berechtigungsprüfungsergebnisanzeige" wird "Anzeige, ob die Berechtigung
  passt").
- Hauptaussage früh, weil das Verb im Nebensatz ans Ende rutscht und lange
  Klammern den Leser warten lassen.
- "du", "Sie" oder neutral, aber konsequent im ganzen Text.
- Keine pseudo-englische Marketing-Syntax ("Next Level Collaboration für dein
  Team").
- Keine wörtlichen Übersetzungen englischer Idiome ("am Ende des Tages",
  "Sinn machen" nur wenn bewusst gewählt).
- Anglizismen, die im Team gelebt werden (Release, Pull Request, Rollout,
  in Produktteams auch Outcome, Bet, Opportunity), dürfen bleiben; einmal
  erklären, wenn die Leser sie nicht kennen.
- Es gilt der Begriff, den die Zielgruppe täglich benutzt, ob englisch oder
  deutsch. Ein etablierter Anglizismus bleibt: für IT-Leser "Row-Level
  Security", "Service Account", "Secrets", "Drift", "Quota", nicht
  "Zeilenrechte", "Dienstkonto", "Geheimnisse", "Abweichungen", "Kontingent".
  Ein etablierter deutscher Begriff bleibt, wo die Gruppe ihn nutzt:
  "Mandantentrennung" (nicht das erfundene "Kundentrennung", auch nicht
  "Tenant Isolation" für deutsche IT-Leser), "Aufbewahrungsfristen" für
  Datenschutz-Leser. Die Begriffe stehen in den eigenen Texten der Gruppe
  (Mails, Tickets, Wiki, Code, der Standard, nach dem sie arbeitet); dort
  nachsehen, nicht nach Gefühl wählen, und als `terms` in facts.json an das
  Gate geben. Einen Begriff einmal erklären, wenn die Gruppe ihn vielleicht
  nicht kennt. Wer "Knowledge Store" oder "Rate Limit" eindeutscht
  ("Wissensspeicher", "Abfragelimit"), zwingt den Leser zum Rückübersetzen;
  das ist so falsch wie Denglisch (`references/ai-tells.md`, Terms the
  audience uses).
- Erfundene Mischformen nicht:
  "Permission-Grenze" wird "wer welche Daten sehen darf", "Nutzungsevidenz"
  wird "Belege aus der echten Nutzung".
- Gendern in den eigenen Texten des Hauses: Gender-Doppelpunkt oder
  Gender-Stern ("Nutzer:innen", "Nutzer*innen") sind erlaubt und der Default,
  wo ein Personenwort es braucht. Neutrale Formen (Partizip, Sammelbegriff,
  direkte Ansprache) bevorzugen, wo sie flüssig lesen. Eine Form pro Text,
  konsequent. In Texten für Kunden gilt deren Konvention. Der Rat für
  deutsche Rechtschreibung hat die Zeichen im Wortinneren 2023 nicht in den
  Kernbestand der Orthografie aufgenommen, und manche Behörden und Länder
  untersagen sie (supported) [SRC-WRITE-040]; vorab die Regel des Empfängers
  prüfen. Das Gate warnt nicht vor diesen Formen.
- Ein Begriff pro Sache im ganzen Text, auch über Dokumente hinweg: nicht
  "Berechtigung" hier und "Permission" dort.
- Datum und Zahl im Zielformat: "21. Oktober", "bis morgen 12 Uhr", "1.500".
- E-Mail-Anrede: nach "Hi Anna," klein weiterschreiben.

## Ton

- Direkt, ruhig, respektvoll. "Mein Vorschlag ist ..." statt "Hiermit möchte
  ich höflichst anfragen ...".
- Kein "Bezugnehmend auf unsere vorangegangene Korrespondenz".
- Geschäftsbriefe und formelle E-Mails: DIN 5008:2020 als Orientierung für
  Form und Erfassbarkeit, nicht als Tonvorgabe; 2020 ist laut DIN Media die
  aktuelle Ausgabe (verified) [SRC-WRITE-005]. Vor "aktuell" im Text das
  DIN-Portal erneut prüfen.

## Gute Muster

- "Danke für ..."
- "Mein Vorschlag ist ..."
- "Für die Entscheidung fehlen uns noch ..."
- "Kannst du bis Donnerstag ...?"
