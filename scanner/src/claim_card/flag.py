"""Shared flag type. A flag is a pattern match for human review, not a
finding of fact about what actually happened -- see the confounder rule
in RESEARCH.txt.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Flag:
    check: str
    file: str
    line: int
    pattern: str
    snippet: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "check": self.check,
            "file": self.file,
            "line": self.line,
            "pattern": self.pattern,
            "snippet": self.snippet,
            "notes": self.notes,
        }
