from claim_card.checks.entropy import check_entropy

PYPROJECT = """
[project]
dependencies = ["one", "two"]
"""


def test_flags_probe_count_overrun():
    budget = {"probe types": 2}
    source = {"probes.py": "def probe_a():\n    pass\ndef probe_b():\n    pass\ndef probe_c():\n    pass\n"}
    flags = check_entropy(budget, source, None)
    assert len(flags) == 1
    assert "counted 3" in flags[0].snippet


def test_no_flag_when_within_budget():
    budget = {"probe types": 3}
    source = {"probes.py": "def probe_a():\n    pass\n"}
    assert check_entropy(budget, source, None) == []


def test_flags_dependency_overrun():
    budget = {"dependencies": 1}
    flags = check_entropy(budget, {}, PYPROJECT)
    assert len(flags) == 1
    assert "counted 2" in flags[0].snippet


def test_skips_not_computable_labels():
    budget = {"persistent formats": 1, "transport": 1, "docker": 0}
    assert check_entropy(budget, {}, None) == []


def test_flags_network_import_when_budget_is_zero():
    budget = {"network calls from pulse itself": 0}
    source = {"net.py": "import requests\n"}
    flags = check_entropy(budget, source, None)
    assert len(flags) == 1
