"""Plain-text section splitting shared by rules.py and the checks.

Recognizes two heading styles seen in practice: a line followed by a line
of repeated '=' or '-' characters (underline style), and numbered
ALL-CAPS-ish headings like "8. FALSIFICATION REPORT".
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_UNDERLINE_RE = re.compile(r"^[=-]{3,}\s*$")
_NUMBERED_HEADING_RE = re.compile(r"^\d+\.\s+[A-Z][A-Z0-9 /()'\-]{3,}$")


@dataclass
class Section:
    heading: str
    start_line: int  # 1-indexed, heading line itself
    end_line: int  # 1-indexed, exclusive-ish: last line belonging to section
    text: str


def split_sections(text: str) -> list[Section]:
    lines = text.splitlines()
    heading_lines: list[tuple[int, str]] = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
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
