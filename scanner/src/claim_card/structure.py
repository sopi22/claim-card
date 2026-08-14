"""Plain-text section splitting shared by rules.py and the checks.

Recognizes three heading styles seen in practice: a line followed by a
line of repeated '=' or '-' characters (underline style), numbered
ALL-CAPS-ish headings like "8. FALSIFICATION REPORT", and standard
Markdown ATX headers ("#", "##", ... "######"). Added 2026-08-14
(RESEARCH.txt Section 13) -- every real Markdown repo in Section 12's
test set used ATX headers exclusively, which this module previously
had no recognition for at all.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_UNDERLINE_RE = re.compile(r"^[=-]{3,}\s*$")
_NUMBERED_HEADING_RE = re.compile(r"^\d+\.\s+[A-Z][A-Z0-9 /()'\-]{3,}$")
# Requires whitespace before the heading text (rules out "#!/bin/bash",
# "#SBATCH ..." -- real lines seen in this project's own test set), no
# preceding-blank-line requirement (unlike underline style): the '#'
# prefix is unambiguous on its own, so the same-line-could-be-a-rule
# heuristic underline style needs doesn't apply here.
_ATX_HEADING_RE = re.compile(r"^#{1,6}\s+\S.*$")
# Fenced code blocks (```...``` or ~~~...~~~) are common in real Markdown
# and can contain lines starting with '#' that are not headings at all
# (shell comments, shebangs) -- confirmed in this project's own test set
# (whisper/README.md, gpt-neox/README.md both have this). Toggled per
# line; heading detection for all three styles above is suppressed while
# inside a fence, not just the new ATX style, since a fenced code example
# could equally coincidentally resemble the other two styles.
_FENCE_RE = re.compile(r"^(`{3,}|~{3,})")

# Shared across vocab.py (non-goal confounder notes) and repro.py (caveat
# section extraction): a bounded, explicit list of heading synonyms for a
# self-declared limitations/non-goals/caveats section. Widened 2026-08-14
# beyond this project's own template vocabulary (NON-GOAL/OUT OF SCOPE) to
# also match real external repos' own phrasing (LIMITATIONS, KNOWN ISSUES,
# CAVEATS) -- see RESEARCH.txt Section 12. No fuzzy/semantic matching, no
# open-ended synonym expansion beyond this fixed list.
LIMITATION_HEADING_RE = re.compile(
    r"NON-GOALS?|REJECTED|OUT[\s-]OF[\s-]SCOPE|NOT BUILDING|EXPLICITLY NOT|"
    r"LIMITATIONS?|KNOWN ISSUES?|CAVEATS?",
    re.I,
)


@dataclass
class Section:
    heading: str
    start_line: int  # 1-indexed, heading line itself
    end_line: int  # 1-indexed, exclusive-ish: last line belonging to section
    text: str


def split_sections(text: str) -> list[Section]:
    lines = text.splitlines()
    heading_lines: list[tuple[int, str]] = []

    in_fence = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if _FENCE_RE.match(stripped):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent <= 3 and _ATX_HEADING_RE.match(stripped):
            heading_lines.append((i, stripped))
            continue
        preceding_ok = (
            i == 0
            or not lines[i - 1].strip()
            or _UNDERLINE_RE.match(lines[i - 1].strip())
        )
        if not preceding_ok:
            continue
        if _NUMBERED_HEADING_RE.match(stripped):
            heading_lines.append((i, stripped))
            continue
        if i + 1 < len(lines) and _UNDERLINE_RE.match(lines[i + 1].strip()):
            heading_lines.append((i, stripped))

    if not heading_lines:
        return [Section(heading="", start_line=1, end_line=len(lines), text=text)]

    sections: list[Section] = []
    for idx, (line_no, heading) in enumerate(heading_lines):
        next_start = heading_lines[idx + 1][0] if idx + 1 < len(heading_lines) else len(lines)
        body = "\n".join(lines[line_no:next_start])
        sections.append(
            Section(heading=heading, start_line=line_no + 1, end_line=next_start, text=body)
        )
    return sections


def line_at(text: str, offset: int) -> int:
    """1-indexed line number for a character offset into text."""
    return text.count("\n", 0, offset) + 1
