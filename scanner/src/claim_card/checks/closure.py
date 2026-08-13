"""Closure audit: flag absolutist/closing-language patterns inside a
repo's own closing sections, and flag a possible contradiction where a
closing section claims nothing is pending while an OPEN/not-scheduled
item is named elsewhere in the same docs.

The signal-word list below deliberately overlaps with the words
claim-card's own vocabulary lock forbids in its own output (see
scanner/README.txt) -- the same overclaiming pattern is what this check
looks for in a target repo's text.
"""

from __future__ import annotations

import re

from claim_card.flag import Flag
from claim_card.structure import Section

_SIGNAL_WORDS = (
    "verified", "proven", "guarantee", "guaranteed", "confirmed",
    "always", "never", "100%", "flawless", "bulletproof", "no issues",
    "no bugs", "perfect", "definitely", "certainly", "completely",
    "totally", "fully complete",
)
# words may wrap across a line break in hand-wrapped plain text, so an
# internal space in a phrase is matched as \s+, not a literal space
_SIGNAL_RE = re.compile(
    r"\b("
    + "|".join(re.escape(w).replace(r"\ ", r"\s+") for w in _SIGNAL_WORDS)
    + r")\b",
    re.I,
)

_NOTHING_PENDING_RE = re.compile(
    r"\b(no\s+other\s+items?\s+(are\s+|is\s+)?pending|"
    r"nothing\s+(else\s+)?(is\s+)?pending|"
    r"no\s+items?\s+remain(?:ing)?)\b", re.I
)
_OPEN_ITEM_RE = re.compile(r"\bOPEN\b[,.]? (NOT-SCHEDULED|not scheduled)?", re.I)


def check_closure(closing_sections: list[Section], full_doc_texts: dict[str, str]) -> list[Flag]:
    flags: list[Flag] = []

    for section in closing_sections:
        text = section.text
        for m in _SIGNAL_RE.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            lines = text.splitlines()
            line_text = lines[line_no - 1].strip() if line_no - 1 < len(lines) else ""
            flags.append(
                Flag(
                    check="closure_audit",
                    file=f"section '{section.heading or '(untitled)'}'",
                    line=section.start_line + line_no - 1,
                    pattern=m.group(0),
                    snippet=line_text,
                    notes=[
                        "closure/absolutist-language pattern inside a "
                        "closing section -- cross-check against the "
                        "evidentiary grade actually logged before treating "
                        "this as an overclaim"
                    ],
                )
            )

        for m in _NOTHING_PENDING_RE.finditer(text):
            has_open_elsewhere = any(
                _OPEN_ITEM_RE.search(t) for t in full_doc_texts.values()
            )
            if has_open_elsewhere:
                line_no = text.count("\n", 0, m.start()) + 1
                lines = text.splitlines()
                line_text = lines[line_no - 1].strip() if line_no - 1 < len(lines) else ""
                flags.append(
                    Flag(
                        check="closure_audit",
                        file=f"section '{section.heading or '(untitled)'}'",
                        line=section.start_line + line_no - 1,
                        pattern="nothing-pending vs. OPEN item",
                        snippet=line_text,
                        notes=[
                            "this closing section says nothing is pending, "
                            "but an item marked OPEN was found elsewhere in "
                            "the docs -- check whether it's legitimately "
                            "scoped as non-blocking rather than silently "
                            "dropped from this summary"
                        ],
                    )
                )

    return flags
