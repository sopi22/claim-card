"""Repo walking and orchestration. Reads a target repo's own docs to
extract its rules, then runs the four checks against that same repo.

Uses the `git` binary via subprocess for commit-message text rather than
a git-parsing library -- this is the "specific gap that can't be closed
without one" the entropy budget names, closed here by shelling out to a
tool already present rather than adding a dependency.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from claim_card.checks.closure import check_closure
from claim_card.checks.entropy import check_entropy
from claim_card.checks.repro import check_repro
from claim_card.checks.vocab import check_vocab
from claim_card.flag import Flag
from claim_card.rules import RuleSet, extract_rules

_EXCLUDE_DIR_NAMES = {
    ".git", ".venv", "venv", "__pycache__", "node_modules",
    ".pytest_cache", "build", "dist",
}
_TEXT_EXTENSIONS = {".txt", ".md", ".rst", ".py"}
_DOC_PREFIXES = ("readme", "research")


@dataclass
class ScanResult:
    rules: RuleSet
    flags: list[Flag] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "vocabulary_lock": {
                "locked": self.rules.vocab_locked,
                "forbidden": self.rules.vocab_forbidden,
            },
            "entropy_budget": self.rules.entropy_budget,
            "reproducibility": {
                "entries_found": self.rules.repro_entries,
                "achieved_claim": self.rules.repro_achieved,
                "conclusion_grade": self.rules.conclusion_grade,
            },
            "rule_source_files": self.rules.source_files,
            "flag_count": len(self.flags),
            "flags": [f.to_dict() for f in self.flags],
        }


def _walk_text_files(repo_root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in _EXCLUDE_DIR_NAMES for part in path.parts):
            continue
        if path.suffix.lower() not in _TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        files[str(path.relative_to(repo_root))] = text
    return files


def _doc_texts(all_files: dict[str, str], repo_root: Path) -> dict[str, str]:
    docs = {}
    for rel_path, text in all_files.items():
        p = Path(rel_path)
        if len(p.parts) == 1 and p.stem.lower().startswith(_DOC_PREFIXES):
            docs[rel_path] = text
    return docs


def _pyproject_text(repo_root: Path) -> str | None:
    for path in sorted(repo_root.rglob("pyproject.toml")):
        if any(part in _EXCLUDE_DIR_NAMES for part in path.parts):
            continue
        return path.read_text(encoding="utf-8", errors="ignore")
    return None


def _git_log_text(repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "log", "--format=%s%n%b"],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return result.stdout if result.returncode == 0 else ""


def scan_repo(repo_root: str | Path) -> ScanResult:
    repo_root = Path(repo_root).resolve()
    all_files = _walk_text_files(repo_root)
    doc_texts = _doc_texts(all_files, repo_root)

    rules = extract_rules(doc_texts)

    git_log = _git_log_text(repo_root)
    scan_files = dict(all_files)
    if git_log:
        scan_files["(git log)"] = git_log

    flags: list[Flag] = []
    flags += check_vocab(rules.vocab_forbidden, scan_files)

    source_files = {p: t for p, t in all_files.items() if p.endswith(".py")}
    flags += check_entropy(rules.entropy_budget, source_files, _pyproject_text(repo_root))

    flags += check_repro(
        rules.repro_entries, rules.repro_achieved, rules.conclusion_grade,
        doc_texts, rules.closing_sections,
    )

    flags += check_closure(rules.closing_sections, doc_texts)

    return ScanResult(rules=rules, flags=flags)
