"""Dependency-free readability diagnostics for German and English.

Scores are sensors, not objectives: use them to find passages worth a second
look, never as a target. The syllable counters are vowel-group heuristics;
swap in a tested library (Pyphen, textstat) when exact scores matter.
"""

from __future__ import annotations

import math
import re
import sys
from html.parser import HTMLParser
from dataclasses import dataclass

WORD_RE = re.compile(r"[^\W\d_]+(?:['\u2019-][^\W\d_]+)*")
SENTENCE_RE = re.compile(r"[.!?]+(?=\s|$)")
EN_VOWELS = re.compile(r"[aeiouy]+")
DE_VOWELS = re.compile(r"(?:au|ei|eu|äu|ie|[aeiouyäöü])+")
# Reference-page limits per language: (mean sentence words, longest sentence).
# German follows plain-language practice; the English maximum is a local working value.
LIMITS = {"de": (15, 25), "en": (20, 30)}


def limits(language: str) -> tuple[int, int]:
    return LIMITS["de" if is_german(language) else "en"]


def resolve_lang(lang: str | None, lang_class: str | None) -> str:
    """Explicit --lang wins; else the de/en suffix of --lang-class; else en."""
    if lang:
        return lang
    suffix = (lang_class or "").rsplit("-", 1)[-1].lower()
    return suffix if suffix in LIMITS else "en"


@dataclass(frozen=True)
class Counts:
    words: int
    sentences: int
    syllables: int
    long_words: int
    polysyllables: int
    long_sentences: int


# Periods that do not end a sentence: common DE/EN abbreviations and German
# ordinals ("am 3. Oktober"). Without this guard "z. B." alone adds two sentences.
ABBREVIATION_RE = re.compile(
    r"(?i)\b(?:u\.s|z\.\s?b|u\.\s?a|d\.\s?h|e\.\s?g|i\.\s?e|bzw|ca|dr|nr|vgl|etc|usw|ggf|inkl|evtl|mr|mrs|ms|vs)\."
)
ORDINAL_RE = re.compile(r"\b(\d{1,2})\.(?=\s+[^\W\d_])")
# A blank line, heading, or list item ends a sentence even without a period.
BLOCK_RE = re.compile(r"\n\s*\n|\n(?=\s*(?:[-*+]|\d+[.)]|#+)\s)")


def sentences(text: str) -> list[str]:
    # ponytail: rule-based split, use a language-aware segmenter if counts still skew
    guarded = ABBREVIATION_RE.sub(lambda m: m.group().replace(".", "\x00"), text)
    guarded = ORDINAL_RE.sub("\\1\x00", guarded)
    parts = [p.strip() for block in BLOCK_RE.split(guarded) for p in SENTENCE_RE.split(block)]
    return [p.replace("\x00", ".") for p in parts if p.strip()] or [text]


def syllables_en(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    count = len(EN_VOWELS.findall(w))
    if w.endswith("e") and not w.endswith(("le", "ye")) and count > 1:
        count -= 1
    return max(1, count)


def syllables_de(word: str) -> int:
    w = re.sub(r"[^a-zäöüß]", "", word.lower())
    return max(1, len(DE_VOWELS.findall(w))) if w else 0


def is_german(language: str) -> bool:
    return language.lower().startswith("de")


def counts(text: str, language: str) -> Counts:
    words = WORD_RE.findall(text)
    syllable_fn = syllables_de if is_german(language) else syllables_en
    per_word = [syllable_fn(w) for w in words]
    parts = sentences(text)
    return Counts(
        words=max(1, len(words)),
        sentences=max(1, len(parts)),
        syllables=max(1, sum(per_word)),
        long_words=sum(1 for w in words if len(w) > 6),
        polysyllables=sum(1 for n in per_word if n >= 3),
        long_sentences=sum(1 for s in parts if len(WORD_RE.findall(s)) > limits(language)[1]),
    )


def diagnostics(text: str, language: str) -> dict[str, float | int]:
    c = counts(text, language)
    wps = c.words / c.sentences
    spw = c.syllables / c.words
    result: dict[str, float | int] = {
        "words": c.words,
        "sentences": c.sentences,
        "avg_sentence_words": round(wps, 2),
        "long_sentences": c.long_sentences,
        "max_sentence_words": limits(language)[1],
        "lix": round(wps + 100.0 * c.long_words / c.words, 2),
    }
    if is_german(language):
        result["flesch_de"] = round(180.0 - wps - 58.5 * spw, 2)
    else:
        result["flesch_en"] = round(206.835 - 1.015 * wps - 84.6 * spw, 2)
        result["flesch_kincaid_grade"] = round(0.39 * wps + 11.8 * spw - 15.59, 2)
        result["smog"] = (
            round(1.043 * math.sqrt(c.polysyllables * 30.0 / c.sentences) + 3.1291, 2)
            if c.polysyllables
            else 0.0
        )
    return result


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
PROSE = {"p", "li", "dd", "figcaption"}
# Everything else that starts or ends a block, so text never runs across it.
BREAKS = {"ul", "ol", "dl", "dt", "div", "section", "article", "header", "footer", "blockquote",
          "h1", "h2", "h3", "h4", "h5", "h6", "tr", "pre", "figure", "br"}


class _Extractor(HTMLParser):
    """Collects prose blocks (p, li, dd, figcaption) with their section. Skips script,
    style, tables, diagram source (class "mermaid"; a "mermaid-legend" caption is
    prose the reader sees) and, with lang_class, any
    element carrying a sibling language class (same prefix, other suffix)."""

    def __init__(self, lang_class: str | None) -> None:
        super().__init__()
        self.prefix = lang_class.rsplit("-", 1)[0] + "-" if lang_class and "-" in lang_class else None
        self.lang_class = lang_class
        self.stack: list[tuple[str, bool]] = []
        self.skip = 0
        self.prose: list[str] = []
        self.buf: list[str] = []
        self.out: list[tuple[str, str]] = []
        self.section = ""
        self.by_id = False
        self.h2: list[str] | None = None

    def flush(self) -> None:
        text = " ".join("".join(self.buf).split())
        self.buf = []
        if text and self.prose:
            self.out.append((self.section, text))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if tag in BREAKS or tag in PROSE:
            self.flush()
        if tag in VOID:
            return
        drop = (
            tag in {"script", "style", "table"}
            or "mermaid" in classes
            or bool(self.prefix and any(c.startswith(self.prefix) and c != self.lang_class for c in classes))
        )
        self.stack.append((tag, drop))
        self.skip += drop
        if tag == "section" and a.get("id"):
            self.section, self.by_id = a["id"], True
        if tag == "h2" and not self.skip:
            self.h2 = []
        if tag in PROSE and not self.skip:
            self.prose.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag in BREAKS or tag in PROSE:
            self.flush()
        if tag == "h2" and self.h2 is not None:
            if not self.by_id:
                self.section = " ".join("".join(self.h2).split())
            self.h2 = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for t, dropped in self.stack[i:]:
                    self.skip -= dropped
                    if t in PROSE and self.prose:
                        self.prose.pop()
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.skip:
            return
        if self.h2 is not None:
            self.h2.append(data)
        self.buf.append(data)


def html_blocks(html: str, lang_class: str | None = None) -> list[tuple[str, str]]:
    """(section, prose block) pairs; a block always ends a sentence."""
    parser = _Extractor(lang_class)
    parser.feed(html)
    parser.close()
    parser.flush()
    return parser.out


def html_text(html: str, lang_class: str | None = None) -> str:
    return "\n\n".join(b for _, b in html_blocks(html, lang_class))


def html_sections(html: str, language: str, lang_class: str | None = None) -> list[dict]:
    """Diagnostics per section (section[id], else the preceding h2)."""
    grouped: dict[str, list[str]] = {}
    for section, block in html_blocks(html, lang_class):
        grouped.setdefault(section, []).append(block)
    return [{"section": k, **diagnostics("\n\n".join(v), language)} for k, v in grouped.items()]


LANG_CLASS_RE = re.compile(r"^(.*-)(de|en)$")


class _Node:
    def __init__(self, tag, classes, parent):
        self.tag, self.classes, self.parent, self.kids, self.text = tag, classes, parent, [], []

    def words(self) -> int:
        return len(WORD_RE.findall(" ".join(self.text))) + sum(k.words() for k in self.kids)

    def preview(self) -> str:
        return " ".join(" ".join(self.text).split())[:40] or self.tag


def _tree(html: str) -> _Node:
    root = cur = _Node("root", [], None)

    class P(HTMLParser):
        def handle_starttag(self, tag, attrs):
            nonlocal cur
            if tag in VOID:
                return
            n = _Node(tag, (dict(attrs).get("class") or "").split(), cur)
            cur.kids.append(n)
            cur = n

        def handle_endtag(self, tag):
            nonlocal cur
            n = cur
            while n.parent and n.tag != tag:
                n = n.parent
            if n.parent:
                cur = n.parent

        def handle_data(self, data):
            if cur.tag not in {"script", "style"}:
                cur.text.append(data)

    P().feed(html)
    return root


def _walk(n):
    yield n
    for k in n.kids:
        yield from _walk(k)


def bilingual_report(html: str) -> dict:
    """Measure every language class (prefix-de, prefix-en) found, each with its own
    formulas and limits, plus twin parity: an element needs an adjacent sibling
    in the other language, and twins should not differ in length by more than 2x."""
    found = [m for c in re.findall(r'class="([^"]*)"', html) for t in c.split() if (m := LANG_CLASS_RE.match(t))]
    if not found:
        return {"prefix": "", "languages": {}, "parity": []}
    prefix = found[0].group(1)
    langs = sorted({m.group(2) for m in found if m.group(1) == prefix})
    report: dict = {"prefix": prefix, "languages": {l: diagnostics(html_text(html, prefix + l), l) for l in langs}, "parity": []}
    tag = lambda n: next((t[len(prefix):] for t in n.classes if t.startswith(prefix) and t[len(prefix):] in LIMITS), None)
    for parent in _walk(_tree(html)):
        kids = parent.kids
        paired: set[int] = set()
        for i, n in enumerate(kids):
            lang = tag(n)
            if not lang or tag(parent) or i in paired:
                continue
            nxt = kids[i + 1] if i + 1 < len(kids) else None
            if nxt and tag(nxt) and tag(nxt) != lang and i + 1 not in paired:
                paired.add(i + 1)
                a, b = sorted((n.words(), nxt.words()))
                if a * 2 < b:
                    report["parity"].append(f"parity: twin word counts differ more than 2x ({n.words()} vs {nxt.words()}): {n.preview()!r}")
            else:
                report["parity"].append(f"parity: {lang} element has no twin next to it: {n.preview()!r}")
    return report


def read_input(file: str, html: bool = False, lang_class: str | None = None) -> str:
    text = sys.stdin.read() if file == "-" else open(file, encoding="utf-8").read()
    if html or file.lower().endswith((".html", ".htm")):
        return html_text(text, lang_class)
    return text


def main(argv: list[str]) -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Readability diagnostics (warn-only).")
    parser.add_argument("--lang", help="de or en (default: suffix of --lang-class, else en)")
    parser.add_argument("--html", action="store_true", help="parse HTML (automatic for .html files)")
    parser.add_argument("--lang-class", help="keep one language of a bilingual page, e.g. l-de; \"auto\" measures every language class")
    parser.add_argument("--sections", action="store_true", help="HTML only: report per section")
    parser.add_argument("file", nargs="?", default="-")
    args = parser.parse_args(argv)
    if args.lang_class == "auto":
        raw = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
        print(json.dumps(bilingual_report(raw), indent=2, ensure_ascii=False))
        return 0
    args.lang = resolve_lang(args.lang, args.lang_class)
    if args.sections:
        raw = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
        print(json.dumps(html_sections(raw, args.lang, args.lang_class), indent=2))
        return 0
    text = read_input(args.file, args.html, args.lang_class)
    print(json.dumps(diagnostics(text, args.lang), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
