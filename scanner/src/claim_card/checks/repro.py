"""Reproducibility cross-check: flag a claimed reproducibility grade that
exceeds the R-level entries actually logged, or a caveat named at the
highest logged R-level whose distinctive wording doesn't reappear
anywhere in the closing text.
"""

from __future__ import annotations

import re

from claim_card.flag import Flag
from claim_card.structure import (
    LIMITATION_HEADING_RE,
    Section,
    distinctive_words,
    split_sections,
)

_CAVEAT_LINE_RE = re.compile(r"^.*\b(CAVEAT|residual limitation)\b.*$", re.I | re.M)
_GENERALITY_RE = re.compile(
    r"\b(in\s+general|on\s+all\s+devices|on\s+any\s+device|universally|"
    r"works\s+everywhere)\b",
    re.I,
)


def check_repro(
    repro_entries: list[int],
    repro_achieved: int | None,
    conclusion_grade: str | None,
    doc_texts: dict[str, str],
    closing_sections: list[Section],
) -> list[Flag]:
    flags: list[Flag] = []

    max_logged = max(repro_entries) if repro_entries else None

    if repro_achieved is not None and max_logged is not None and repro_achieved > max_logged:
        flags.append(
            Flag(
                check="reproducibility_cross_check",
                file="(rule source doc)",
                line=0,
                pattern=f"achieved: R{repro_achieved}",
                snippet=f"claims R{repro_achieved} but only R0-R{max_logged} entries are logged",
                notes=[
                    "the stated achieved level is higher than the highest "
                    "R-level entry actually found in the text"
                ],
            )
        )

    closing_text = "\n".join(s.text for s in closing_sections)
    for path, text in doc_texts.items():
        for m in _GENERALITY_RE.finditer(text):
            if max_logged is None or max_logged < 3:
                line_no = text.count("\n", 0, m.start()) + 1
                line_text = text.splitlines()[line_no - 1].strip()
                flags.append(
                    Flag(
                        check="reproducibility_cross_check",
                        file=path,
                        line=line_no,
                        pattern=m.group(0),
                        snippet=line_text,
                        notes=[
                            "generality language found without an R3 "
                            "(separate environments/repos) entry logged -- "
                            "check the claim is scoped to what was actually "
                            "tested"
                        ],
                    )
                )

    for path, text in doc_texts.items():
        for caveat_line_match in _CAVEAT_LINE_RE.finditer(text):
            caveat_line = caveat_line_match.group(0)
            distinctive = distinctive_words(caveat_line)
            if not distinctive:
                continue
            hits = sum(1 for w in distinctive if w in closing_text.lower())
            if closing_text and hits == 0:
                line_no = text.count("\n", 0, caveat_line_match.start()) + 1
                flags.append(
                    Flag(
                        check="reproducibility_cross_check",
                        file=path,
                        line=line_no,
                        pattern="caveat wording overlap",
                        snippet=caveat_line.strip(),
                        notes=[
                            "none of this caveat's distinctive words "
                            "('%s') were found in the detected closing "
                            "section(s) -- check the closing summary "
                            "still reflects this limitation" % ", ".join(distinctive)
                        ],
                    )
                )

    # Heading-based generalization (2026-08-14, RESEARCH.txt Section 12):
    # the CAVEAT-line check above only fires on this project's own literal
    # wording. A real repo's own Limitations/Non-Goals/Known-Issues section
    # is a caveat too, just declared as a whole section rather than a line
    # carrying the word "CAVEAT". Same word-overlap-survival mechanism,
    # applied to the section body instead of a single matched line.
    for path, text in doc_texts.items():
        for section in split_sections(text):
            if not section.heading or not LIMITATION_HEADING_RE.search(section.heading):
                continue
            distinctive = distinctive_words(section.text)
            if not distinctive:
                continue
            hits = sum(1 for w in distinctive if w in closing_text.lower())
            if closing_text and hits == 0:
                flags.append(
                    Flag(
                        check="reproducibility_cross_check",
                        file=path,
                        line=section.start_line,
                        pattern="limitation section wording overlap",
                        snippet=section.heading.strip(),
                        notes=[
                            "none of this section's distinctive words "
                            "('%s') were found in the detected closing "
                            "section(s) -- check whether this stated "
                            "limitation survived into the closing summary, "
                            "or whether no closing section exists at all "
                            "in this repo's docs" % ", ".join(distinctive)
                        ],
                    )
                )

    return flags
