"""Dependency-free readability diagnostics for German and English.

Scores are sensors, not objectives: use them to find passages worth a second
look, never as a target. The syllable counters are vowel-group heuristics;
swap in a tested library (Pyphen, textstat) when exact scores matter.
"""

from __future__ import annotations

import math
import re
import sys
from dataclasses import dataclass

WORD_RE = re.compile(r"[^\W\d_]+(?:['\u2019-][^\W\d_]+)*")
SENTENCE_RE = re.compile(r"[.!?]+(?=\s|$)")
EN_VOWELS = re.compile(r"[aeiouy]+")
DE_VOWELS = re.compile(r"(?:au|ei|eu|äu|ie|[aeiouyäöü])+")
LONG_SENTENCE_WORDS = 25


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
    r"(?i)\b(?:z\.\s?b|u\.\s?a|d\.\s?h|e\.\s?g|i\.\s?e|bzw|ca|dr|nr|vgl|etc|usw|ggf|inkl|evtl|mr|mrs|ms|vs)\."
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
        long_sentences=sum(1 for s in parts if len(WORD_RE.findall(s)) > LONG_SENTENCE_WORDS),
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


def main(argv: list[str]) -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Readability diagnostics (warn-only).")
    parser.add_argument("--lang", default="en", help="de or en (default en)")
    parser.add_argument("file", nargs="?", default="-")
    args = parser.parse_args(argv)
    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    print(json.dumps(diagnostics(text, args.lang), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
