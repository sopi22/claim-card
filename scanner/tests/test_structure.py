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


ATX = """\
# Model Card: CLIP

## Model Use

### Out-of-Scope Use Cases

Text describing out-of-scope uses.

## Limitations

Some limitations text.
"""


def test_atx_headers_are_recognized_at_all_levels():
    sections = split_sections(ATX)
    headings = [s.heading for s in sections]
    assert "# Model Card: CLIP" in headings
    assert "## Model Use" in headings
    assert "### Out-of-Scope Use Cases" in headings
    assert "## Limitations" in headings


ATX_NO_BLANK_LINE = """\
## Model Use
### Intended Use
text right after, no blank line separating the two headers.
"""


def test_atx_headers_do_not_need_a_preceding_blank_line():
    sections = split_sections(ATX_NO_BLANK_LINE)
    headings = [s.heading for s in sections]
    assert "## Model Use" in headings
    assert "### Intended Use" in headings


FENCED_SHELL_COMMENTS = """\
## Setup

```bash
# on Ubuntu or Debian
sudo apt install ffmpeg
```

```bash
#!/bin/bash
#SBATCH --job-name="neox"
echo hello
```

## Real Heading After The Fences
"""


def test_hash_comments_inside_fenced_code_are_not_headings():
    sections = split_sections(FENCED_SHELL_COMMENTS)
    headings = [s.heading for s in sections]
    assert "# on Ubuntu or Debian" not in headings
    assert "#!/bin/bash" not in headings
    assert '#SBATCH --job-name="neox"' not in headings
    assert "## Setup" in headings
    assert "## Real Heading After The Fences" in headings


def test_atx_heading_requires_whitespace_after_hashes():
    # not valid ATX syntax (no space) -- must not be treated as a heading
    sections = split_sections("#!/bin/bash\necho hi\n")
    headings = [s.heading for s in sections]
    assert "#!/bin/bash" not in headings


RST_INDENTED_LITERAL_BLOCK = """\
Install
--------

::

    # Build shared libraries
    make

    # Install the wheel
    python3 -m pip install dist/*.whl

Usage
------
"""


def test_atx_does_not_match_rst_indented_literal_block_comments():
    # RST's `::` + 4-space-indented literal block is not a fenced code
    # block (no ```/~~~ markers) -- found as a real false positive against
    # httpstan/README.rst when the ATX check stripped indentation instead
    # of capping it at 3 spaces per CommonMark's own ATX indentation rule.
    sections = split_sections(RST_INDENTED_LITERAL_BLOCK)
    headings = [s.heading for s in sections]
    assert "# Build shared libraries" not in headings
    assert "# Install the wheel" not in headings
    assert "Install" in headings
    assert "Usage" in headings


def test_fence_suppresses_underline_and_numbered_styles_too():
    text = (
        "```\n"
        "1. NOT A REAL NUMBERED HEADING\n"
        "Fake Heading\n"
        "------------\n"
        "```\n"
        "## Real Heading\n"
    )
    sections = split_sections(text)
    headings = [s.heading for s in sections]
    assert "1. NOT A REAL NUMBERED HEADING" not in headings
    assert "Fake Heading" not in headings
    assert "## Real Heading" in headings
