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
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from readability import WORD_RE, bilingual_report, diagnostics, html_text, is_german, limits, read_input, resolve_lang, sentences  # noqa: E402

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


def main(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--artifact", required=True, choices=sorted(ARTIFACTS))
    parser.add_argument("--lang", help="de or en (default: suffix of --lang-class, else en)")
    parser.add_argument("--facts", help="JSON file with facts, forbidden_claims and terms")
    parser.add_argument("--html", action="store_true", help="parse HTML (automatic for .html files)")
    parser.add_argument("--lang-class", help="keep one language of a bilingual page, e.g. l-de; \"auto\" gates every language class")
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
        print(json.dumps(merged, indent=2, ensure_ascii=False))
        return 1 if merged["errors"] else 0
    args.lang = resolve_lang(args.lang, args.lang_class)
    text = read_input(args.file, args.html, args.lang_class)
    result = check(text, args.artifact, args.lang, facts)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
