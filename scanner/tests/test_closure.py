from claim_card.checks.closure import check_caveat_survival, check_closure
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


def test_csr_none_when_no_caveats_logged():
    csr, flags = check_caveat_survival({"RESEARCH.txt": "no caveats here.\n"})
    assert csr is None
    assert flags == []


def test_csr_tagged_caveat_survives_by_exact_id():
    docs = {
        "RESEARCH.txt": "[CAVEAT:C1] no run yet used a second vendor device.\n",
        "README.txt": "CONCLUSION: SUPPORTED. See [CAVEAT:C1] for the untested case.\n",
    }
    csr, flags = check_caveat_survival(docs)
    assert csr == 1.0
    assert flags == []


def test_csr_tagged_caveat_does_not_survive():
    docs = {
        "RESEARCH.txt": "[CAVEAT:C1] no run yet used a second vendor device.\n",
        "README.txt": "CONCLUSION: SUPPORTED, no other notes.\n",
    }
    csr, flags = check_caveat_survival(docs)
    assert csr == 0.0
    assert any(f.pattern == "caveat_survival" for f in flags)
    assert "exact ID match" in flags[0].notes[0]


def test_csr_untagged_caveat_survives_by_lexicon_fallback():
    docs = {
        "RESEARCH.txt": "CAVEAT: no run yet used a second vendor device.\n",
        "README.txt": "CONCLUSION: no run yet used a second vendor device, noted above.\n",
    }
    csr, flags = check_caveat_survival(docs)
    assert csr == 1.0
    assert flags == []


def test_csr_untagged_caveat_does_not_survive():
    docs = {
        "RESEARCH.txt": "CAVEAT: no run yet used a second vendor device.\n",
        "README.txt": "CONCLUSION: SUPPORTED, no other notes.\n",
    }
    csr, flags = check_caveat_survival(docs)
    assert csr == 0.0
    assert "lexicon fallback" in flags[0].notes[0]


def test_csr_mix_of_survived_and_dropped():
    docs = {
        "RESEARCH.txt": (
            "[CAVEAT:C1] tagged caveat that survives.\n"
            "[CAVEAT:C2] tagged caveat that is dropped.\n"
        ),
        "README.txt": "CONCLUSION: SUPPORTED. See [CAVEAT:C1] above.\n",
    }
    csr, flags = check_caveat_survival(docs)
    assert csr == 0.5
    assert len(flags) == 1
    assert "C2" in flags[0].snippet
