"""Vocabulary scan: flag a repo's own forbidden-vocabulary terms reappearing
in that same repo's text.

A raw word-boundary match cannot tell a real claim apart from a term
quoted as an example, a term used in a disclaimed non-goals list, or a
polysemous term used in its ordinary domain sense (e.g. "Settings
provider" as an Android API name vs. "provider" as the forbidden
architecture-abstraction concept). Each match carries the note(s) that
apply so a human reviewer isn't starting from zero -- the match itself
is still just a pattern flag, not a violation.
"""

from __future__ import annotations

import re

from claim_card.flag import Flag
from claim_card.structure import line_at, split_sections

_NON_GOAL_HEADING_RE = re.compile(
    r"NON-GOAL|REJECTED|OUT OF SCOPE|NOT BUILDING|EXPLICITLY NOT", re.I
)

# Capitalized words that, immediately before a forbidden term, suggest a
# domain-specific compound noun rather than the locked abstraction sense.
_DOMAIN_COMPOUND_PREFIXES = {
    "provider": {"settings", "content", "location", "identity", "service"},
}


def check_vocab(forbidden_terms: list[str], files: dict[str, str]) -> list[Flag]:
    flags: list[Flag] = []
    if not forbidden_terms:
        return flags

    for term in forbidden_terms:
        pattern = re.compile(rf"\b{re.escape(term)}s?\b", re.I)
        for path, text in files.items():
            sections = split_sections(text)
            for m in pattern.finditer(text):
                line_no = line_at(text, m.start())
                line_text = text.splitlines()[line_no - 1].strip()

                if re.search(r"\b(Forbidden|Locked)\s*:", line_text):
                    # the rule-declaration line itself will always match
                    # every term it lists -- that's the definition, not an
                    # occurrence, so it's excluded rather than flagged
                    continue

                notes = []

                section = _section_for_line(sections, line_no)
                if section and _NON_GOAL_HEADING_RE.search(section.heading):
                    notes.append(
                        "inside a section headed '%s' -- read as a disclaimed "
                        "concept (something explicitly not being built), not "
                        "a claim, unless the surrounding sentence says "
                        "otherwise" % section.heading
                    )

                prefix_word = _word_before(text, m.start())
                if prefix_word and prefix_word.lower() in _DOMAIN_COMPOUND_PREFIXES.get(
                    term.lower(), set()
                ):
                    notes.append(
                        "preceded by '%s' -- may be a domain-specific compound "
                        "term (e.g. an API name) rather than the locked "
                        "abstraction sense of '%s'" % (prefix_word, term)
                    )

                if _in_quotes(line_text, m.group()):
                    notes.append(
                        "appears inside a quoted phrase on this line -- check "
                        "whether it's being quoted/described rather than "
                        "asserted"
                    )

                flags.append(
                    Flag(
                        check="vocabulary_scan",
                        file=path,
                        line=line_no,
                        pattern=term,
                        snippet=line_text,
                        notes=notes,
                    )
                )
    return flags


def _section_for_line(sections, line_no: int):
    for section in sections:
        if section.start_line <= line_no <= section.end_line:
            return section
    return None


def _word_before(text: str, offset: int) -> str | None:
    before = text[:offset].rstrip()
    if before.endswith("-"):
        # hyphenated compounds ("settings-provider") join like a space
        # would ("Settings provider") for domain-compound purposes
        before = before[:-1]
    m = re.search(r"([A-Za-z]+)$", before)
    return m.group(1) if m else None


def _in_quotes(line: str, term: str) -> bool:
    return bool(re.search(r'["“][^"”]*' + re.escape(term) + r'[^"”]*["”]', line, re.I))
