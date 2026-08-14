from claim_card.rules import extract_rules

SAMPLE = """\
1. CLARIFICATION GATE
================================================================================
Q: What vocabulary is locked?
A: Locked (as specified in the brief): assumption, probe, observation.
   Forbidden: capability, provider, broker, cost -- and by extension
   anything else.

Probe types:            3 maximum
External services:      0

R1 (first session): ran once.
R2 (second session): ran again.

Reproducibility achieved: R2

================================================================================
8. FALSIFICATION REPORT
================================================================================
CONCLUSION: SUPPORTED, with a caveat.
"""


def test_extracts_locked_and_forbidden_terms():
    rules = extract_rules({"RESEARCH.txt": SAMPLE})
    assert rules.vocab_locked == ["assumption", "probe", "observation"]
    assert rules.vocab_forbidden == ["capability", "provider", "broker", "cost"]


def test_extracts_entropy_budget_numbers():
    rules = extract_rules({"RESEARCH.txt": SAMPLE})
    assert rules.entropy_budget["probe types"] == 3
    assert rules.entropy_budget["external services"] == 0


def test_extracts_reproducibility_ladder():
    rules = extract_rules({"RESEARCH.txt": SAMPLE})
    assert rules.repro_entries == [1, 2]
    assert rules.repro_achieved == 2
    assert rules.conclusion_grade == "SUPPORTED"


def test_finds_closing_section():
    rules = extract_rules({"RESEARCH.txt": SAMPLE})
    headings = [s.heading for s in rules.closing_sections]
    assert any("FALSIFICATION REPORT" in h for h in headings)


def test_finds_summary_heading_as_closing_section():
    text = "Summary\n-------\nEverything works as intended.\n"
    rules = extract_rules({"README.md": text})
    headings = [s.heading for s in rules.closing_sections]
    assert any("Summary" in h for h in headings)
