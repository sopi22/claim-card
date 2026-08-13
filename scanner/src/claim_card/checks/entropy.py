"""Entropy check: cross-check a repo's stated numeric budget against a
handful of reliably-countable signals in its own source.

Only the sub-items that are cheaply and honestly countable via static
text patterns are checked. Everything else is reported as not
computable this way rather than forced into a shaky heuristic.
"""

from __future__ import annotations

import re

from claim_card.flag import Flag

_PROBE_DEF_RE = re.compile(r"^\s*def (probe_|check_)\w+", re.M)
_NETWORK_IMPORT_RE = re.compile(
    r"^\s*(?:import|from)\s+(socket|requests|urllib\w*|http\.client|aiohttp)\b", re.M
)
_BACKGROUND_RE = re.compile(
    r"\b(subprocess\.Popen|threading\.Thread|multiprocessing\.Process)\s*\("
)
_DEPS_ARRAY_RE = re.compile(r"(?<!optional-)dependencies\s*=\s*\[(?P<body>[^\]]*)\]")

_NOT_COMPUTABLE = {"persistent format", "persistent formats", "transport", "docker"}


def check_entropy(
    budget: dict[str, int], source_files: dict[str, str], pyproject_text: str | None
) -> list[Flag]:
    flags: list[Flag] = []

    for label, stated in budget.items():
        if any(label.startswith(k) or k in label for k in _NOT_COMPUTABLE):
            continue

        if "probe" in label or "check" in label:
            actual = sum(len(_PROBE_DEF_RE.findall(t)) for t in source_files.values())
            _compare(flags, label, stated, actual, "probe/check function count")

        elif "external service" in label or "network call" in label:
            actual = sum(len(_NETWORK_IMPORT_RE.findall(t)) for t in source_files.values())
            _compare(flags, label, stated, actual, "network-module import count")

        elif "background process" in label:
            actual = sum(len(_BACKGROUND_RE.findall(t)) for t in source_files.values())
            _compare(flags, label, stated, actual, "background-process construct count")

        elif "dependenc" in label and pyproject_text:
            m = _DEPS_ARRAY_RE.search(pyproject_text)
            actual = 0
            if m:
                actual = len([e for e in m.group("body").split(",") if e.strip()])
            _compare(flags, label, stated, actual, "pyproject.toml [project.dependencies] entry count")

    return flags


def _compare(flags: list[Flag], label: str, stated: int, actual: int, method: str) -> None:
    if actual > stated:
        flags.append(
            Flag(
                check="entropy_check",
                file="(repo-wide, source files)",
                line=0,
                pattern=label,
                snippet=f"stated budget {stated}, counted {actual} via {method}",
                notes=[
                    "counted total exceeds the stated budget -- confirm the "
                    "count method above actually matches what the budget "
                    "line meant before treating this as an overrun"
                ],
            )
        )
