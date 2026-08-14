"""Extract a repo's own stated rules from its own README/RESEARCH text.

This is the core design choice: claim-card does not ship a fixed rulebook.
It reads whatever vocabulary lock, entropy budget, and reproducibility
ladder a project already wrote down for itself, then checks that project's
other artifacts against those self-declared rules.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from claim_card.structure import Section, split_sections

_LOCKED_RE = re.compile(r"Locked[^:]*:\s*(?P<list>.+?)(?:\n\n|\.\s*\n|\.$)", re.S)
_FORBIDDEN_RE = re.compile(r"Forbidden:\s*(?P<list>.+?)(?:—|--|\n\n|\.\s*\n)", re.S)
_BUDGET_LINE_RE = re.compile(
    r"^\s*([A-Za-z][A-Za-z /'\-]*?):\s*(?:≤\s*)?(\d+)\b(.*)$", re.M
)
_REPRO_ENTRY_RE = re.compile(r"^R(\d+)\b", re.M)
_REPRO_ACHIEVED_RE = re.compile(
    r"[Rr]eproducibility (?:level )?achieved:\s*R(\d+)", re.S
)
_GRADE_RE = re.compile(r"\bCONCLUSION:\s*([A-Z][A-Z ]*?)(?:[,.\n]|$)")

_BUDGET_LABELS = (
    "probe types",
    "probe/check types",
    "persistent format",
    "persistent formats",
    "transport",
    "external services",
    "background processes",
    "network calls",
    "docker",
)


def _split_terms(raw: str) -> list[str]:
    raw = re.sub(r"\s+", " ", raw).strip()
    raw = raw.rstrip(".")
    terms = [t.strip().strip('"').strip("'") for t in raw.split(",")]
    return [t for t in terms if t and " " not in t]


@dataclass
class RuleSet:
    vocab_locked: list[str] = field(default_factory=list)
    vocab_forbidden: list[str] = field(default_factory=list)
    entropy_budget: dict[str, int] = field(default_factory=dict)
    repro_entries: list[int] = field(default_factory=list)
    repro_achieved: int | None = None
    conclusion_grade: str | None = None
    closing_sections: list[Section] = field(default_factory=list)
    source_files: list[str] = field(default_factory=list)


_CLOSING_HEADING_RE = re.compile(
    r"CONCLUSION|CLOSED|FALSIFICATION REPORT|DELIVERABLE|CLOSING|SUMMARY", re.I
)


def extract_rules(doc_texts: dict[str, str]) -> RuleSet:
    combined = "\n\n".join(doc_texts.values())
    rules = RuleSet(source_files=list(doc_texts.keys()))

    m = _LOCKED_RE.search(combined)
    if m:
        rules.vocab_locked = _split_terms(m.group("list"))

    m = _FORBIDDEN_RE.search(combined)
    if m:
        rules.vocab_forbidden = _split_terms(m.group("list"))

    for label, value, _rest in _BUDGET_LINE_RE.findall(combined):
        norm = re.sub(r"\s+", " ", label.strip().lower())
        if any(norm.startswith(known) or known in norm for known in _BUDGET_LABELS):
            rules.entropy_budget[norm] = int(value)

    rules.repro_entries = sorted({int(n) for n in _REPRO_ENTRY_RE.findall(combined)})

    m = _REPRO_ACHIEVED_RE.search(combined)
    if m:
        rules.repro_achieved = int(m.group(1))

    m = _GRADE_RE.search(combined)
    if m:
        rules.conclusion_grade = m.group(1).strip()

    for path, text in doc_texts.items():
        for section in split_sections(text):
            if _CLOSING_HEADING_RE.search(section.heading) or (
                not section.heading and _CLOSING_HEADING_RE.search(section.text[:200])
            ):
                rules.closing_sections.append(section)

    return rules
