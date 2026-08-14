from claim_card.checks.repro import check_repro
from claim_card.structure import Section


def _closing(text, heading="CONCLUSION"):
    return [Section(heading=heading, start_line=1, end_line=text.count("\n") + 1, text=text)]


def test_flags_achieved_level_above_logged_entries():
    flags = check_repro(
        repro_entries=[1], repro_achieved=3, conclusion_grade="SUPPORTED",
        doc_texts={"RESEARCH.txt": "R1: ran once.\n"}, closing_sections=[],
    )
    assert any("achieved: R3" in f.pattern for f in flags)


def test_no_flag_when_achieved_matches_logged_entries():
    flags = check_repro(
        repro_entries=[1, 2, 3], repro_achieved=3, conclusion_grade="SUPPORTED",
        doc_texts={"RESEARCH.txt": "R1 R2 R3\n"}, closing_sections=[],
    )
    assert not any("achieved" in f.pattern for f in flags)


def test_flags_generality_language_without_r3():
    text = "CONCLUSION: this works on all devices.\n"
    flags = check_repro(
        repro_entries=[1], repro_achieved=1, conclusion_grade="SUPPORTED",
        doc_texts={"RESEARCH.txt": text}, closing_sections=_closing(text),
    )
    assert any("generality language" in n for f in flags for n in f.notes)


def test_generality_phrase_matches_across_a_line_wrap():
    text = "this is guaranteed to work on\nall devices, no issues.\n"
    flags = check_repro(
        repro_entries=[1], repro_achieved=1, conclusion_grade="SUPPORTED",
        doc_texts={"RESEARCH.txt": text}, closing_sections=_closing(text),
    )
    assert any("generality language" in n for f in flags for n in f.notes)


def test_flags_dropped_caveat():
    text = (
        "CAVEAT: no run yet used a second vendor's device.\n\n"
        "CONCLUSION: SUPPORTED, no other notes.\n"
    )
    flags = check_repro(
        repro_entries=[1], repro_achieved=1, conclusion_grade="SUPPORTED",
        doc_texts={"RESEARCH.txt": text}, closing_sections=_closing("CONCLUSION: SUPPORTED, no other notes.\n"),
    )
    assert any("caveat" in f.notes[0] for f in flags if f.pattern == "caveat wording overlap")


def test_no_flag_when_caveat_wording_carried_into_closing_text():
    caveat = "CAVEAT: no run yet used a second vendor device.\n"
    closing = "CONCLUSION: SUPPORTED. No run yet used a second vendor device, noted above.\n"
    text = caveat + "\n" + closing
    flags = check_repro(
        repro_entries=[1], repro_achieved=1, conclusion_grade="SUPPORTED",
        doc_texts={"RESEARCH.txt": text}, closing_sections=_closing(closing),
    )
    assert not any(f.pattern == "caveat wording overlap" for f in flags)


def test_flags_dropped_limitations_section():
    text = (
        "Limitations\n-----------\nDoes not support concurrent access safely.\n\n"
        "Summary\n-------\nEverything works as intended.\n"
    )
    flags = check_repro(
        repro_entries=[], repro_achieved=None, conclusion_grade=None,
        doc_texts={"README.md": text}, closing_sections=_closing("Everything works as intended.\n", heading="Summary"),
    )
    assert any(f.pattern == "limitation section wording overlap" for f in flags)


def test_no_flag_when_limitations_section_wording_carried_into_closing():
    text = (
        "Limitations\n-----------\nDoes not support concurrent access safely.\n\n"
        "Summary\n-------\nStill does not support concurrent access safely.\n"
    )
    closing = "Still does not support concurrent access safely.\n"
    flags = check_repro(
        repro_entries=[], repro_achieved=None, conclusion_grade=None,
        doc_texts={"README.md": text}, closing_sections=_closing(closing, heading="Summary"),
    )
    assert not any(f.pattern == "limitation section wording overlap" for f in flags)


def test_no_flag_for_limitations_section_when_no_closing_section_exists():
    text = "Limitations\n-----------\nDoes not support concurrent access safely.\n"
    flags = check_repro(
        repro_entries=[], repro_achieved=None, conclusion_grade=None,
        doc_texts={"README.md": text}, closing_sections=[],
    )
    assert not any(f.pattern == "limitation section wording overlap" for f in flags)
