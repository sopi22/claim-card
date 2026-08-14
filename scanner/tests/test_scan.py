from pathlib import Path

from claim_card.scan import _doc_texts


def test_matches_widened_root_level_doc_names():
    files = {
        "README.md": "x",
        "CONTRIBUTING.md": "x",
        "model-card.md": "x",
        "LIMITATIONS.md": "x",
        "unrelated.md": "x",
    }
    docs = _doc_texts(files, Path("."))
    assert set(docs) == {"README.md", "CONTRIBUTING.md", "model-card.md", "LIMITATIONS.md"}


def test_matches_top_level_docs_rst_only_not_nested():
    files = {
        "docs/contributing.rst": "x",
        "docs/sub/deep.rst": "x",
        "doc/contributing.rst": "x",  # singular "doc", deliberately not matched
    }
    docs = _doc_texts(files, Path("."))
    assert set(docs) == {"docs/contributing.rst"}
