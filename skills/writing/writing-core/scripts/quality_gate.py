"""Deterministic quality gate for writing artifacts.

Checks only what a script can decide: required parts, length, forbidden or
unsourced claims, artifact-specific anti-patterns. Meaning, tone, and native
phrasing stay with the agent's semantic review.

Usage:
    quality_gate.py --artifact commit --lang en [--facts facts.json] [--html] [--lang-class l-de] [FILE|-]

HTML input (a .html file or --html) is reduced to prose in p, li, dd first.

facts.json: {"facts": [...], "forbidden_claims": [...],
             "terms": {"Preferred Term": ["avoided variant", ...]},
             "known_terms": ["RLS", ...]}
Every artifact also gets the AI-tell warnings (references/ai-tells.md).
Exit code 1 when any error is found; warnings never fail.

--jev adds an advisory tier after the deterministic checks: one typed TypeSafe
Jev call per section (questions, thresholds, rules and examples live in
jev_questions.json), warnings tagged "jev:". Keys: VERCEL_AI_GATEWAY_API_KEY or
AI_GATEWAY_API_KEY (gateway, zero retention), else TYPESAFE_API_KEY. Without a
key or an answer the tier is skipped and says why; it never fails the gate.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from readability import WORD_RE, bilingual_report, diagnostics, html_text, is_german, limits, resolve_lang, sentences  # noqa: E402

# Each required part is a regex that may match DE or EN wording.
WHY = r"(?im)^#+\s*(why|warum|context|kontext|hintergrund|motivation|problem)\b"
VALIDATION = r"(?im)^#+\s*(validation|validierung|tests?|testing|test plan|how tested|verification|verifikation|prüfung|getestet|qa)\b"
SUBJECT = r"(?im)^(subject|betreff)\s*:"
PREVIEW = r"(?im)^(preview|vorschau(text)?)\s*:"


def label(keywords: str) -> str:
    """A section label: a Markdown heading containing the keyword, or a line
    whose first few words contain it and end in a colon ("- Risks:", "**Signal:**",
    "Was wir gelernt haben:"). A keyword in running prose ("the next release")
    does not count, because the gate checks structure, not vocabulary."""
    return (
        rf"(?im)^[\s>*+\-\d.)]*(?:#+[^\n]*?\b(?:{keywords})"
        rf"|[^\n:#]{{0,30}}?\b(?:{keywords})[^\n:]{{0,20}}:)"
    )

ARTIFACTS: dict[str, dict] = {
    "business_email": {"recommended": {"subject line (fine to omit in a reply that stays in its thread)": SUBJECT}, "warn_words": 180, "sentences": True},
    "marketing_email": {"required": {"subject line": SUBJECT, "preview line": PREVIEW}, "warn_words": 400},
    "slack": {
        "warn_words": 200,
        "sentences": True,
        "warn": {"email-style salutation line; Slack usually starts with the point": r"(?i)\A\s*(hi|hey|hello|dear|hallo|moin|servus|guten (morgen|tag)|liebe[rs]?|sehr geehrte[rs]?)\b[^\n]*,\s*\n"},
    },
    "hero": {"headline_max_words": 12},
    "landing_page": {"sentences": True},
    "website_content": {"sentences": True},
    "confluence": {
        "required": {
            "purpose": r"(?i)\b(purpose|zweck)\b",
            "owner or status": r"(?i)\b(owner|verantwortlich|status)\b",
        },
        "sentences": True,
    },
    "agile_status": {
        "required": {
            "signal": label("signal"),
            "outcome": label("outcome|ergebnis"),
            "learning": label("learned|learnings?|gelernt|erkenntnis\\w*|lernen"),
            "risk": label("risks?|risiken|risiko"),
            "next focus": label("next|nächste\\w*"),
        },
        # Warn, not error: a status may say it deliberately does not report velocity.
        "warn": {"velocity or story points; check they are not presented as the outcome": r"(?i)\b(velocity|story points?)\b"},
    },
    "fast_roadmap": {
        "required": {
            "strategic intent": r"(?i)(strategic intent|strategische[rs]? (intent|ziel|absicht))",
            "outcome": r"(?i)\b(outcomes?|ergebnis)",
            "now": r"(?im)^#+\s*(now|jetzt)\b",
            "confidence or uncertainty": r"(?i)(confidence|uncertain|zuversicht|unsicher|konfidenz)",
            "investment boundary": r"(?i)(investment boundary|appetite|investitionsgrenze|budgetgrenze)",
        },
    },
    "agile_progress": {
        "required": {
            "goal": r"(?im)^#+\s*(goal|ziel)\b",
            "current state": r"(?i)(current state|aktueller stand|ist-stand)",
            "next breakthrough": label("next|nächste\\w*"),
        },
        "reject": {"percent complete without a model": r"(?i)\d+\s?(%|prozent|percent)\s*(complete|done|finished|fertig|erledigt|abgeschlossen)"},
    },
    "product_document": {
        "required": {
            "problem": r"(?i)\bproblem\b",
            "evidence": r"(?i)\b(evidence|evidenz|belege)\b",
            "unknowns": r"(?i)\b(unknowns?|unbekannt|offene fragen|annahmen|assumptions)\b",
        },
    },
    "po_summary": {"warn_words": 300, "sentences": True},
    "executive_summary": {"warn_words": 300, "bottom_line_within_words": 40, "sentences": True},
    "pull_request": {"required": {"why or context": WHY, "validation": VALIDATION}},
    "commit": {},
    "slides": {},
    "prose": {"sentences": True},
}

# A sentence start, or after a comma or colon: where an imperative begins.
_START = r"(?:^|(?<=[.!?:;,]\s)|(?<=\())"
UI_INSTRUCTION = (
    # A quoted "click here" is a mention, as in a style guide, not an instruction.
    r"(?im)(?<![\"'\u201e])\b(?:click|tap) here\b|(?<![\"'\u201e])\bhier (?:klicken|tippen)\b|\bklicken sie hier\b"
    r"|\b(?:see|siehe) (?:below|above|unten|oben)\b"
    rf"|(?:{_START}|\byou can )(?:swipe|scroll)(?: the \w+)? (?:sideways|horizontally|left and right|down|up)\b"
    rf"|{_START}(?:click|tap|hover|swipe|scroll|pinch|zoom)(?: (?:on|over) (?:the|this|a|an|any) (?:image|picture|photo|chart|diagram|graphic|figure|table|map|bar|point|node))?"
    r" to (?:see|view|enlarge|zoom|expand|read|show|reveal|explore)\b"
    r"|\blässt sich\b[^.!?\n]{0,40}?\b(?:wischen|scrollen|zoomen)\b"
    r"|\b(?:kann man|können sie|kannst du)\b[^.!?\n]{0,40}?\b(?:wischen|scrollen|zoomen)\b"
    r"|\b(?:zum|für) (?:vergrößern|zoomen|anzeigen|weiterlesen)\b[^.!?\n]{0,30}?\b(?:tippen|klicken|wischen|scrollen)\b"
    r"|\b(?:scrollen|wischen) sie (?:nach|seitlich|weiter|horizontal|waagerecht)\b"
    r"|\b(?:nach (?:unten|oben|rechts|links)|seitlich|waagerecht|horizontal) (?:scrollen|wischen)\b"
    r"|\bfahren sie mit der maus\b"
    r"|\b(?:tippen|klicken) sie auf (?:das|die|den|ein|eine) (?:bild|diagramm|grafik|abbildung|tabelle|karte|foto)\b"
)

# Warnings, not errors: a contrast that corrects a belief the reader holds is
# fine. Each name says what to do, references/ai-tells.md says why.
AI_TELLS: dict[str, str] = {
    "not X but Y; state Y, keep X only if the reader believes it":
        r"(?i)\bnicht (?:nur |bloß |einfach |mehr )?[^.;:\n]{1,60}?,? sondern\b"
        r"|\bnot (?:just |only |merely |simply )?[^.;:\n]{1,60}?,? but\b"
        r"|\b(?:it|this|that)(?:'s| is) not [^.;:\n]{1,40}[,;] (?:it|this|that)(?:'s| is)\b"
        # Reversed form, a sentence that ends on the rejected half. Only a
        # parallel preposition or article counts, so a scope ("nicht bis zum
        # Merge") or a list of negations stays quiet.
        r"|, nicht (?:im|in|an|am|auf|als|der|die|das|den|dem)\b[^,.;:\n]{1,30}[.!]"
        r"|, not (?:in|on|at|as|the|a|an)\b[^,.;:\n]{1,30}[.!]",
    "'bewusst schlank/einfach' justifies instead of stating the state":
        r"(?i)\bbewusst (?:schlank|einfach|klein|knapp|minimal)\w*",
    "'ins Spiel kommen' is filler; name the mechanism":
        r"(?i)\bins Spiel\b",
    "'spielt eine zentrale Rolle' inflates; say what it does":
        r"(?i)\bspiel\w* eine (?:zentrale|entscheidende|wichtige|tragende) Rolle",
    "'plays a pivotal role' inflates; say what it does":
        r"(?i)\bplays? an? (?:key|crucial|pivotal|vital|central) role",
    "stock AI word (delve, tapestry, testament, landscape, seamless, game changer, unlock, at its core)":
        r"(?i)\b(?:delv(?:e|es|ed|ing)|tapestry|testament to|(?:evolving|ever-changing) landscape|seamless(?:ly)?"
        r"|game[- ]chang(?:er|ing)|unlock(?:s|ed|ing)? (?:the )?(?:full )?(?:power|potential)|at its core)\b",
    "staged opener (Let's dive in, Here's the thing, Die Wahrheit ist)":
        r"(?i)\blet'?s dive in\b|\bhere'?s the thing\b|\bdie wahrheit ist\b|\bund genau das\b",
    "'echter Mehrwert' / 'real value' claims value without naming it":
        r"(?i)\becht\w* Mehrwert\b|\breal value\b",
    # Chat residue: a reply to the user left inside the artifact.
    "chat residue (I hope this helps, Let me know if, Natürlich!, Ich hoffe, das hilft); cut it":
        r"(?i)\bi hope this helps\b|\blet me know if\b|\bich hoffe,? (?:das|dies|es) hilft\b"
        r"|^\s*natürlich[!,]|^\s*certainly[!,]",
    # Copula avoidance: a stock verb where "is" or "has" says it.
    "copula avoidance (serves as, stands as, boasts, stellt ... dar, fungiert als); use is or has":
        r"(?i)\b(?:serves|stands|functions) as\b|\bboasts\b|\bfungiert als\b|\bstellt\b[^.;:\n]{1,60}?\bdar\b",
    "vague attribution (experts argue, Experten sind sich einig); name the source or drop the claim":
        r"(?i)\b(?:experts|observers|critics|industry reports) (?:argue|say|agree|believe|have (?:cited|noted))\b"
        r"|\bexperten (?:sind sich einig|sagen|meinen|argumentieren)\b|\bbranchenberichte\b|\beinige kritiker\b",
    # Operating the page itself. A how-to step inside a product ("Click Approve to
    # publish", "Klicken Sie auf Speichern") stays quiet: the verbs need the page as
    # object, a direction, or a reveal goal. design-review's design-loop.mjs carries
    # the same patterns as UI_INSTRUCTION; change both together.
    "UI operating instruction (swipe sideways, scroll down, click here, siehe unten); fix the design, put screen reader hints in aria-label":
        UI_INSTRUCTION,
}

# Three or more short comma items before "and/or": a list in running prose. Items
# must start with a letter and be followed by ", " so German decimals ("1,5") and
# number lists never match.
_ITEM = r"[^\W\d_][\w'-]*(?:\s[\w'-]+){0,2}"
ENUMERATION = re.compile(rf"(?i)\b(?:{_ITEM},\s+){{2,}}{_ITEM},?\s+(?:and|und|or|oder)\s")

GENERIC_COMMIT = re.compile(
    r"(?i)^(\w+(\(.+\))?:\s*)?"
    r"(update[sd]?|fix(es|ed)?|bugfix|changes?|wip|misc|stuff|tweaks?|cleanup|änderungen|anpassungen|korrekturen)"
    r"(\s+(bugs?|typos?|stuff|things|code|it|readme))?\.?$"
    r"|^(\w+(\(.+\))?:\s*)?(typo|bug)s?\.?$"
)
BOTTOM_LINE = re.compile(r"(?i)(bottom line|kurzfassung|fazit|tl;dr|kernaussage)")
PERCENT = re.compile(r"(?i)(?<![\d.,])(\d+(?:[.,]\d+)?)\s?(?:%|prozent|percent)")


STOP = {
    "en": "the a an and or but of to in on at for with by from as is are was were be been it its this that these those "
          "not no we you they he she i our your their his her has have had do does did will would can could should may "
          "might must than then so if when while before after into over under about also more most very just".split(),
    "de": "der die das den dem des ein eine einen einem einer eines und oder aber von zu in im auf an am für mit bei aus "
          "als ist sind war waren wird werden wurde wurden nicht kein keine wir sie er es ich du ihr unser euer sich "
          "auch noch nur wenn dann vor nach über unter um zum zur zur dass daß so wie hat haben hatte kann können soll "
          "sollen muss müssen mehr sehr schon".split(),
}
DUP_JACCARD, DUP_MIN_WORDS = 0.6, 6
# Acronyms a technical reader knows; keep short, extend per audience with known_terms.
KNOWN_ACRONYMS = {"OK", "EU", "US", "UK", "PDF", "URL", "API", "HTML", "CSS", "HTTP", "HTTPS", "JSON", "ID", "UI", "AI",
                  "USD", "EUR", "PR", "CI", "GB", "MB", "FAQ"}
ACRONYM = re.compile(r"(?<![\w-])[A-Z]{2,6}\d*(?![\w-])")
# A label of 1 to 3 content words directly before a number with a unit.
FIGURE = re.compile(r"((?:[^\W\d_]+\s+){0,2}[^\W\d_]+)\s+(\d[\d.,]*)\s?(%|percent|prozent|usd|eur|\$|€|ms|gb|mb|days?|tage[n]?|hours?|stunden)(?![\w])", re.I)


def content_words(sentence: str, language: str) -> set[str]:
    stop = set(STOP["de" if is_german(language) else "en"])
    return {w for w in (m.lower() for m in WORD_RE.findall(sentence)) if w not in stop and len(w) > 2 and not w.isdigit()}


def check_repetition(text: str, language: str, warnings: list[str]) -> None:
    """Restated sentences: token overlap of content words, both sides long enough
    to carry a point. A warning shows both sentences shortened."""
    sents = [(s, content_words(s, language)) for s in sentences(text)]
    sents = [(s, w) for s, w in sents if len(w) >= DUP_MIN_WORDS]
    for i, (a, wa) in enumerate(sents):
        for b, wb in sents[i + 1:]:
            if len(wa & wb) / len(wa | wb) >= DUP_JACCARD:
                warnings.append(f"repetition: near-duplicate sentences, one home per statement: {a[:50]!r} / {b[:50]!r}")


def check_figures(text: str, language: str, warnings: list[str]) -> None:
    """The same label followed by different numbers with a unit. Low-recall on
    purpose: a label of stopwords only never matches."""
    stop = set(STOP["de" if is_german(language) else "en"])
    seen: dict[tuple[str, str], tuple[str, str]] = {}
    for m in FIGURE.finditer(text):
        label_words = [w.lower() for w in m.group(1).split()]
        while label_words and label_words[0] in stop:
            label_words.pop(0)
        # The label must be the content words right before the number.
        tail = []
        for w in reversed(label_words):
            if w in stop:
                break
            tail.insert(0, w)
        if not tail:
            continue
        key = (" ".join(tail), m.group(3).lower())
        value = m.group(2).rstrip(".,").replace(",", ".")
        if key in seen and seen[key][0] != value:
            warnings.append(f"figures: {key[0]!r} is {seen[key][1]} and {m.group(2)} {m.group(3)}; one of them is wrong?")
        seen.setdefault(key, (value, f"{m.group(2)} {m.group(3)}"))


def check_acronyms(text: str, facts: dict | None, warnings: list[str]) -> None:
    """Once per acronym: the reader cannot look it up in the writer's head. Explained
    when its first use sits next to a parenthesis, is listed in known_terms or is a
    preferred term, or is in the short built-in allowlist."""
    known = KNOWN_ACRONYMS | set((facts or {}).get("known_terms", [])) | set(((facts or {}).get("terms") or {}))
    done: set[str] = set()
    for m in ACRONYM.finditer(text):
        a = m.group()
        if a in known or a in done:
            continue
        done.add(a)
        before, after = text[: m.start()].rstrip(), text[m.end():].lstrip()
        if not (after.startswith("(") or before.endswith("(")):
            warnings.append(f"acronym: {a} is used without an expansion at first use; explain it or list it in known_terms")


def words(text: str) -> int:
    return len(WORD_RE.findall(text))


def check_commit(text: str, errors: list[str], warnings: list[str]) -> None:
    lines = text.strip("\n").splitlines()
    subject = lines[0].strip() if lines else ""
    if not subject:
        errors.append("commit: empty subject")
        return
    if GENERIC_COMMIT.match(subject):
        errors.append(f"commit: generic subject {subject!r} does not name the change")
    if len(subject) > 72:
        errors.append(f"commit: subject is {len(subject)} chars, tools truncate past 72")
    elif len(subject) > 50:
        warnings.append(f"commit: subject is {len(subject)} chars, aim for 50")
    if len(lines) > 1 and lines[1].strip():
        errors.append("commit: second line must be blank before the body")


def check_claims(text: str, facts: dict | None, errors: list[str], warnings: list[str]) -> None:
    if not facts:
        return
    lowered = text.lower()
    for claim in facts.get("forbidden_claims", []):
        if claim.lower() in lowered:
            errors.append(f"claim: forbidden or unknown claim stated as fact: {claim!r}")
    # Compare numbers, not strings: "3,5 %", "3.5%" and "3.5 Prozent" are one claim.
    sourced = {n.replace(",", ".") for n in PERCENT.findall(" ".join(facts.get("facts", [])))}
    for pct in sorted({n.replace(",", ".") for n in PERCENT.findall(text)}):
        if pct not in sourced:
            warnings.append(f"claim: {pct}% has no matching source fact; verify or remove")


def check_terms(text: str, facts: dict | None, errors: list[str]) -> None:
    """One term per thing, and the reader's term: an avoided variant is an error.
    Substring match, so German inflections and compounds are caught too."""
    for preferred, avoided in ((facts or {}).get("terms") or {}).items():
        for variant in avoided:
            if re.search(re.escape(variant), text, re.IGNORECASE):
                errors.append(f"term: {variant!r} found; this audience says {preferred!r}")


def check(text: str, artifact: str, language: str, facts: dict | None = None) -> dict:
    if artifact not in ARTIFACTS:
        raise ValueError(f"unknown artifact {artifact!r}; known: {', '.join(sorted(ARTIFACTS))}")
    rules = ARTIFACTS[artifact]
    errors: list[str] = []
    warnings: list[str] = []

    for name, pattern in rules.get("required", {}).items():
        if not re.search(pattern, text):
            errors.append(f"{artifact}: missing {name}")
    for name, pattern in rules.get("recommended", {}).items():
        if not re.search(pattern, text):
            warnings.append(f"{artifact}: no {name}")
    for name, pattern in rules.get("reject", {}).items():
        if re.search(pattern, text):
            errors.append(f"{artifact}: {name}")
    for name, pattern in rules.get("warn", {}).items():
        if re.search(pattern, text):
            warnings.append(f"{artifact}: {name}")

    for name, pattern in AI_TELLS.items():
        if re.search(pattern, text):
            warnings.append(f"ai-tell: {name}")

    if artifact == "commit":
        check_commit(text, errors, warnings)

    if artifact == "marketing_email":
        subj = re.search(r"(?im)^(?:subject|betreff)\s*:\s*(.+)$", text)
        prev = re.search(r"(?im)^(?:preview|vorschau(?:text)?)\s*:\s*(.+)$", text)
        if subj and prev and subj.group(1).strip().lower() == prev.group(1).strip().lower():
            errors.append("marketing_email: preview repeats the subject instead of adding to it")

    if "headline_max_words" in rules:
        h1 = re.search(r"(?m)^#\s+(.+)$", text)
        if not h1:
            errors.append(f"{artifact}: missing '# ' headline")
        elif words(h1.group(1)) > rules["headline_max_words"]:
            errors.append(f"{artifact}: headline has {words(h1.group(1))} words, max {rules['headline_max_words']}")

    if "bottom_line_within_words" in rules:
        m = BOTTOM_LINE.search(text)
        if not m or words(text[: m.start()]) > rules["bottom_line_within_words"]:
            warnings.append(f"{artifact}: no bottom line label in the first {rules['bottom_line_within_words']} words")

    total = words(text)
    if "warn_words" in rules and total > rules["warn_words"]:
        warnings.append(f"{artifact}: {total} words, default ceiling {rules['warn_words']}")

    check_claims(text, facts, errors, warnings)
    if artifact != "commit":
        check_repetition(text, language, warnings)
        check_figures(text, language, warnings)
        check_acronyms(text, facts, warnings)
    check_terms(text, facts, errors)

    diag = diagnostics(text, language) if rules.get("sentences") else {}
    if diag.get("long_sentences"):
        warnings.append(f"readability: {diag['long_sentences']} sentence(s) over {limits(language)[1]} words")
    if diag and diag["avg_sentence_words"] > limits(language)[0]:
        warnings.append(f"readability: mean sentence length {diag['avg_sentence_words']} words, target at most {limits(language)[0]}")

    if rules.get("sentences"):
        for sentence in sentences(text):
            if ENUMERATION.search(sentence):
                warnings.append(f"list: enumeration chain in running prose, consider a list: {sentence[:60]!r}")
            if sentence.count(";") >= 2:
                warnings.append(f"list: {sentence.count(';')} semicolons in one sentence, consider a list: {sentence[:60]!r}")

    return {"artifact": artifact, "language": language, "errors": errors, "warnings": warnings, "diagnostics": diag}


JEV_DATA = json.loads((Path(__file__).resolve().parent / "jev_questions.json").read_text(encoding="utf-8"))
JEV_GATEWAY = "https://ai-gateway.vercel.sh/v4/ai/decision-model"
JEV_DIRECT = "https://api.typesafe.ai/v1/systemone"
JEV_DIRECT_USD_PER_TOKEN = 0.042e-6
DEFAULT_AUDIENCE = "General readers who did not take part in the work."


def text_sections(text: str) -> list[tuple[str, str]]:
    """(heading, body) per Markdown heading; text before the first heading has heading ''."""
    out: list[tuple[str, list[str]]] = [("", [])]
    for line in text.splitlines():
        m = re.match(r"#{1,6}\s+(.+)", line)
        if m:
            out.append((m.group(1).strip(), []))
        else:
            out[-1][1].append(line)
    return [(h, "\n".join(b).strip()) for h, b in out if "\n".join(b).strip()]


class _JevSections(HTMLParser):
    """Whole sections as the pilot saw them: every visible text of one language,
    table cells joined by ' | ', a section starting at <section> or <h2> and named by its h2."""

    BLOCK = {"p", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "div", "dt", "dd", "caption", "figcaption", "br"}
    VOID = {"br", "img", "hr", "meta", "link", "input", "source", "wbr"}

    def __init__(self, lang_class: str | None):
        super().__init__(convert_charrefs=True)
        prefix = lang_class.rsplit("-", 1)[0] + "-" if lang_class else None
        self.foreign = lambda c: bool(prefix and c.startswith(prefix) and c != lang_class)
        self.stack: list[tuple[str, bool]] = []
        self.skip = 0
        self.sections: list[list] = []
        self.h2: list[str] | None = None

    def start(self) -> None:
        if not self.sections or self.sections[-1][1] or self.sections[-1][0]:
            self.sections.append(["", []])

    def handle_starttag(self, tag, attrs):
        if tag == "section" or (tag == "h2" and not self.skip and (not self.sections or self.sections[-1][0])):
            self.start()
        if tag in self.BLOCK and self.sections:
            self.sections[-1][1].append("\n")
        if tag in self.VOID:
            return
        drop = tag in {"script", "style", "svg"} or any(self.foreign(c) for c in (dict(attrs).get("class") or "").split())
        self.stack.append((tag, drop))
        self.skip += drop
        if tag == "h2" and not self.skip:
            self.h2 = []

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if tag == "h2" and self.h2 is not None:
            self.sections[-1][0] = " ".join("".join(self.h2).split())
            self.h2 = None
        if tag in {"td", "th"} and self.sections:
            self.sections[-1][1].append(" | ")
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.skip -= sum(d for _, d in self.stack[i:])
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.skip:
            return
        if not self.sections:
            self.sections.append(["", []])
        if self.h2 is not None:
            self.h2.append(data)
        self.sections[-1][1].append(data)


def html_page_sections(html: str, lang_class: str | None) -> list[tuple[str, str]]:
    parser = _JevSections(lang_class)
    parser.feed(html)
    parser.close()
    out = []
    for heading, parts in parser.sections:
        lines = (" ".join(l.split()) for l in "".join(parts).split("\n"))
        body = "\n".join(l for l in lines if l)
        if body:
            out.append((heading, body))
    return out


def jev_keys(env) -> tuple[str, str] | None:
    gateway = env.get("VERCEL_AI_GATEWAY_API_KEY") or env.get("AI_GATEWAY_API_KEY")
    if gateway:
        return ("gateway", gateway)
    return ("typesafe", env["TYPESAFE_API_KEY"]) if env.get("TYPESAFE_API_KEY") else None


def jev_request(section, sections, audience: str, key: tuple[str, str]):
    """The pilot's arm C: examples and rules first, then audience, heading, text, the rest of the page."""
    qs = JEV_DATA["questions"]
    heading, body = section
    state = {
        "labeled_examples": "labeled_examples (synthetic):\n" + "\n".join(f"{q}\n {v['examples'][0]}\n {v['examples'][1]}" for q, v in qs.items()),
        "skill_rules": "skill_rules (house style, condensed):\n" + "\n".join(v["rule"] for v in qs.values()),
        "audience": audience,
        "section_heading": heading,
        "section_text": json.dumps(body, ensure_ascii=False),
        "other_sections": json.dumps("\n\n".join(f"## {h}\n{b}" for h, b in sections if (h, b) != section), ensure_ascii=False),
    }
    kind, secret = key
    if kind == "gateway":
        parts = [{"type": "text", "text": v if k in ("labeled_examples", "skill_rules") else f"{k}: {v}"} for k, v in state.items()]
        headers = {"Authorization": "Bearer " + secret, "Content-Type": "application/json", "ai-gateway-protocol-version": "0.0.1",
                   "ai-decision-model-specification-version": "4", "ai-model-id": "typesafe-ai/jev"}
        body = {"stateParts": parts, "questions": {q: {"type": "boolean", "instructions": v["question"]} for q, v in qs.items()},
                "providerOptions": {"gateway": {"zeroDataRetention": True, "disallowPromptTraining": True, "only": ["typesafe-ai"]}}}
        return JEV_GATEWAY, headers, body
    # A text-only call: TypeSafe rejects the image opt-in header and an empty assets map here.
    headers = {"Authorization": "Bearer " + secret, "Content-Type": "application/json"}
    body = {"model": "jev-latest", "state": state, "questions": {q: {"type": "noul", "instructions": v["question"]} for q, v in qs.items()}}
    return JEV_DIRECT, headers, body


def jev_post(url: str, headers: dict, body: dict) -> dict:
    request = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.loads(response.read())


def jev_tier(sections, audience: str, env, post=None) -> dict:
    """Advisory: a warning per question whose probability reaches its threshold; fails open."""
    post = post or jev_post
    key = jev_keys(env)
    if not key:
        return {"warnings": [], "calls": 0, "cost_usd": 0.0,
                "note": "Jev tier skipped: no key (set VERCEL_AI_GATEWAY_API_KEY, AI_GATEWAY_API_KEY or TYPESAFE_API_KEY)"}
    if not sections:
        return {"warnings": [], "calls": 0, "cost_usd": 0.0, "note": "Jev tier skipped: no text"}

    def ask(section):
        try:
            return section, post(*jev_request(section, sections, audience, key)), None
        except Exception as exc:  # fail open: a network, HTTP or parse error never blocks the gate
            return section, None, f"{type(exc).__name__}: {str(exc)[:160]}"

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(ask, sections))
    warnings, failures, cost, calls = [], [], 0.0, 0
    for (heading, _), payload, error in results:
        if error:
            failures.append(f"section {heading!r}: {error}")
            continue
        calls += 1
        gateway_cost = (payload.get("providerMetadata") or {}).get("gateway", {}).get("cost")
        usage = payload.get("usage") or {}
        cost += float(gateway_cost) if gateway_cost is not None else (usage.get("inputTokens") or usage.get("input_tokens") or 0) * JEV_DIRECT_USD_PER_TOKEN
        for q, spec in JEV_DATA["questions"].items():
            answer = (payload.get("answers") or {}).get(q) or {}
            p = answer.get("probability", answer.get("noul"))
            if p is not None and spec["threshold"] is not None and float(p) >= spec["threshold"]:
                warnings.append(f"jev: {q} p={float(p):.2f} in section {heading!r} (advisory: reread it)")
    note = "Jev tier skipped: " + "; ".join(failures) if failures else None
    return {"warnings": warnings, "calls": calls, "cost_usd": round(cost, 6), "note": note}


def add_jev(result: dict, sections, audience: str) -> None:
    tier = jev_tier(sections, audience, os.environ, post=jev_post)
    result["warnings"] = result["warnings"] + tier.pop("warnings")
    result["jev"] = tier
    if tier["note"]:
        print(tier["note"], file=sys.stderr)


def main(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--artifact", required=True, choices=sorted(ARTIFACTS))
    parser.add_argument("--lang", help="de or en (default: suffix of --lang-class, else en)")
    parser.add_argument("--facts", help="JSON file with facts, forbidden_claims and terms")
    parser.add_argument("--html", action="store_true", help="parse HTML (automatic for .html files)")
    parser.add_argument("--lang-class", help="keep one language of a bilingual page, e.g. l-de; \"auto\" gates every language class")
    parser.add_argument("--jev", action="store_true", help="advisory Jev tier per section after the deterministic checks (sends the text to TypeSafe)")
    parser.add_argument("--audience", default=DEFAULT_AUDIENCE, help="who reads the text, for the Jev tier")
    parser.add_argument("file", nargs="?", default="-")
    args = parser.parse_args(argv)
    facts = json.loads(Path(args.facts).read_text(encoding="utf-8")) if args.facts else None
    if args.lang_class == "auto":
        raw = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
        report = bilingual_report(raw)
        langs = {l: check(html_text(raw, report["prefix"] + l), args.artifact, l, facts) for l in report["languages"]}
        merged = {
            "artifact": args.artifact, "languages": langs, "diagnostics": report["languages"],
            "errors": [f"{l}: {e}" for l, r in langs.items() for e in r["errors"]],
            "warnings": [f"{l}: {w}" for l, r in langs.items() for w in r["warnings"]] + report["parity"],
        }
        if args.jev:
            for l in langs:
                add_jev(langs[l], html_page_sections(raw, report["prefix"] + l), args.audience)
                merged["warnings"] += [f"{l}: {w}" for w in langs[l]["warnings"] if w.startswith("jev:")]
        print(json.dumps(merged, indent=2, ensure_ascii=False))
        return 1 if merged["errors"] else 0
    args.lang = resolve_lang(args.lang, args.lang_class)
    raw = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    is_html = args.html or args.file.lower().endswith((".html", ".htm"))
    text = html_text(raw, args.lang_class) if is_html else raw
    result = check(text, args.artifact, args.lang, facts)
    if args.jev:
        add_jev(result, html_page_sections(raw, args.lang_class) if is_html else text_sections(text), args.audience)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
