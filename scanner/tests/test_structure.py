from claim_card.structure import split_sections

WRAPPED = """\
================================================================================
6. ENVIRONMENT GAPS (FACT log, relevant to Phase 1 only -- not blocking
   this Phase 0 deliverable)
================================================================================
body text here.
"""

FOOTER = """\
================================================================================
PHASE 1 CLOSED.

Conclusion stands. The item remains open, unchanged. No other items
are pending on this phase.
================================================================================
END OF DELIVERABLE.
================================================================================
"""


def test_does_not_misparse_a_wrapped_two_line_heading():
    sections = split_sections(WRAPPED)
    headings = [s.heading for s in sections]
    assert "this Phase 0 deliverable)" not in headings


def test_does_not_misparse_a_paragraph_line_before_a_footer_rule():
    sections = split_sections(FOOTER)
    headings = [s.heading for s in sections]
    assert not any("pending on this phase" in h for h in headings)
    assert "END OF DELIVERABLE." in headings
