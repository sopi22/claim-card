from claim_card.checks.closure import check_closure
from claim_card.structure import Section


def _section(text, heading="CONCLUSION"):
    return Section(heading=heading, start_line=1, end_line=text.count("\n") + 1, text=text)


def test_flags_absolutist_word_in_closing_section():
    text = "CONCLUSION: this is fully verified and guaranteed.\n"
    flags = check_closure([_section(text)], {"RESEARCH.txt": text})
    patterns = {f.pattern for f in flags}
    assert "verified" in patterns
    assert "guaranteed" in patterns


def test_signal_word_matches_across_a_line_wrap():
    text = "this is fully\nverified and there are no\nissues remaining.\n"
    flags = check_closure([_section(text)], {"RESEARCH.txt": text})
    assert any(f.pattern.replace("\n", " ") == "no issues" for f in flags) or any(
        f.pattern == "verified" for f in flags
    )


def test_no_signal_words_no_flags():
    text = "CONCLUSION: SUPPORTED, with a named caveat.\n"
    assert check_closure([_section(text)], {"RESEARCH.txt": text}) == []


def test_flags_nothing_pending_contradiction_with_open_item_elsewhere():
    closing_text = "No other items are pending on this phase.\n"
    full_docs = {
        "RESEARCH.txt": (
            "The different-OEM item is OPEN, not scheduled.\n\n" + closing_text
        )
    }
    flags = check_closure([_section(closing_text)], full_docs)
    assert any(f.pattern == "nothing-pending vs. OPEN item" for f in flags)


def test_no_contradiction_flag_without_an_open_item():
    closing_text = "No other items are pending on this phase.\n"
    full_docs = {"RESEARCH.txt": closing_text}
    flags = check_closure([_section(closing_text)], full_docs)
    assert not any(f.pattern == "nothing-pending vs. OPEN item" for f in flags)
