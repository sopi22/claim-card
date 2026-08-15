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
from claim_card.structure import Section, distinctive_words

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


# CAVEAT SURVIVAL RATE (CSR): does a caveat logged in a source RESEARCH*
# doc survive into a downstream README* closing doc? A caveat tagged
# [CAVEAT:ID] survives if that exact ID reappears anywhere in the closing
# doc; an untagged caveat/limitation line survives by the same
# distinctive-word lexicon overlap check_repro already uses for its own
# wording-survival check -- reused from structure.py rather than
# reimplemented here.
_CAVEAT_TAG_RE = re.compile(r"\[CAVEAT:([A-Za-z0-9_.-]+)\]")
_CAVEAT_LINE_RE = re.compile(r"^.*\b(CAVEAT|residual limitation)\b.*$", re.I | re.M)


def _is_source_log(path: str) -> bool:
    return path.rsplit("/", 1)[-1].lower().startswith("research")


def _is_closing_doc(path: str) -> bool:
    return path.rsplit("/", 1)[-1].lower().startswith("readme")


def check_caveat_survival(doc_texts: dict[str, str]) -> tuple[float | None, list[Flag]]:
    """Returns (CSR, flags). CSR is survived/total across every CAVEAT-line
    entry found in this repo's RESEARCH* doc(s); None (not 0.0 or 1.0) when
    no caveats are logged at all, so an empty log can't misread as a
    perfect or a failed score.
    """
    source_texts = {p: t for p, t in doc_texts.items() if _is_source_log(p)}
    closing_text = "\n".join(t for p, t in doc_texts.items() if _is_closing_doc(p))
    closing_text_lower = closing_text.lower()

    entries: list[tuple[str, str | None, str, int]] = []
    for path, text in source_texts.items():
        for m in _CAVEAT_LINE_RE.finditer(text):
            line = m.group(0)
            tag = _CAVEAT_TAG_RE.search(line)
            line_no = text.count("\n", 0, m.start()) + 1
            entries.append((path, tag.group(1) if tag else None, line, line_no))

    if not entries:
        return None, []

    flags: list[Flag] = []
    survived = 0
    for path, caveat_id, line, line_no in entries:
        if caveat_id is not None:
            ok = caveat_id in closing_text
            match_desc = f"exact ID match on [CAVEAT:{caveat_id}]"
        else:
            words = distinctive_words(line)
            ok = bool(words) and any(w in closing_text_lower for w in words)
            match_desc = "lexicon fallback (no [CAVEAT:ID] tag on this line)"
        if ok:
            survived += 1
        else:
            flags.append(
                Flag(
                    check="closure_audit",
                    file=path,
                    line=line_no,
                    pattern="caveat_survival",
                    snippet=line.strip(),
                    notes=[
                        f"caveat did not survive into the closing doc by "
                        f"{match_desc} -- check whether it was dropped or "
                        f"just reworded past what this check can match"
                    ],
                )
            )

    return survived / len(entries), flags
