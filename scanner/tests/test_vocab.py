from claim_card.checks.vocab import check_vocab

FORBIDDEN = ["provider", "capability", "cost"]


def test_flags_a_real_claim():
    files = {"RESEARCH.txt": "We built a capability provider for this.\n"}
    flags = check_vocab(FORBIDDEN, files)
    patterns = {f.pattern for f in flags}
    assert patterns == {"provider", "capability"}


def test_notes_non_goals_context():
    files = {
        "README.txt": (
            "NON-GOALS\n---------\nThis is explicitly NOT a capability "
            "abstraction.\n"
        )
    }
    flags = check_vocab(["capability"], files)
    assert len(flags) == 1
    assert any("disclaimed" in n for n in flags[0].notes)


def test_notes_limitations_heading_context():
    files = {
        "README.txt": (
            "LIMITATIONS\n-----------\nThe provider abstraction does not "
            "handle this case.\n"
        )
    }
    flags = check_vocab(["provider"], files)
    assert len(flags) == 1
    assert any("disclaimed" in n for n in flags[0].notes)


def test_notes_domain_compound():
    files = {"RESEARCH.txt": "the Settings provider write path\n"}
    flags = check_vocab(["provider"], files)
    assert len(flags) == 1
    assert any("domain-specific compound" in n for n in flags[0].notes)


def test_notes_quoted_context():
    files = {"RESEARCH.txt": 'described as "advertised capability" here.\n'}
    flags = check_vocab(["capability"], files)
    assert len(flags) == 1
    assert any("quoted phrase" in n for n in flags[0].notes)


def test_skips_the_rule_definition_line_itself():
    files = {"RESEARCH.txt": "Forbidden: capability, provider, cost.\n"}
    flags = check_vocab(FORBIDDEN, files)
    assert flags == []


def test_no_forbidden_terms_means_no_flags():
    assert check_vocab([], {"RESEARCH.txt": "capability provider cost"}) == []
