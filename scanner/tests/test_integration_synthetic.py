"""Runs the full scanner against examples/synthetic_violations, a fixture
with known, deliberately-planted violations of its own stated rules.
Every flag here has a known ground truth, unlike a real repo.
"""

from pathlib import Path

from claim_card.scan import scan_repo

FIXTURE = Path(__file__).parent.parent / "examples" / "synthetic_violations"


def test_catches_all_planted_vocabulary_violations():
    result = scan_repo(FIXTURE)
    vocab_terms = {f.pattern for f in result.flags if f.check == "vocabulary_scan"}
    assert vocab_terms == {"capability", "provider", "broker", "cost"}


def test_catches_planted_entropy_overrun():
    result = scan_repo(FIXTURE)
    entropy_flags = [f for f in result.flags if f.check == "entropy_check"]
    assert len(entropy_flags) == 1
    assert "probe types" in entropy_flags[0].pattern


def test_catches_planted_reproducibility_overclaim():
    result = scan_repo(FIXTURE)
    repro_flags = [f for f in result.flags if f.check == "reproducibility_cross_check"]
    assert len(repro_flags) == 2  # achieved-level overclaim + generality language


def test_catches_planted_closure_violations():
    result = scan_repo(FIXTURE)
    closure_patterns = {f.pattern for f in result.flags if f.check == "closure_audit"}
    assert {"verified", "guaranteed", "proven", "no issues"} <= closure_patterns
    assert "nothing-pending vs. OPEN item" in closure_patterns


def test_total_flag_count_matches_known_ground_truth():
    result = scan_repo(FIXTURE)
    assert len(result.flags) == 12
