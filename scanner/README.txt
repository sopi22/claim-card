claim-card scanner
====================

What this is: a deterministic, stdlib-only scanner that reads a git
repo's own README/RESEARCH docs to extract that repo's own stated
vocabulary lock, entropy budget, and reproducibility ladder, then
checks that same repo's other artifacts against those self-declared
rules. Every result is a pattern flag for human review, not a finding
of fact -- see the confounder notes attached to each flag, and
RESEARCH.txt for what those flags meant on the two repos tested so far.

SETUP
------
    cd scanner
    python3 -m venv .venv && source .venv/bin/activate
    pip install -e ".[dev]"

RUN
----
    pytest                                   # run the test suite
    claim-card <path-to-target-repo>          # scan a repo
    claim-card <path-to-target-repo> -o out.json

The report is a single JSON file: the rules extracted from the target
repo's own docs, and the list of flags, each with the file, line,
matched pattern, and any confounder notes attached.

EXAMPLE
--------
    claim-card examples/synthetic_violations

examples/synthetic_violations/ is a small fixture with known,
deliberately-planted violations, used to get an actual recall reading
(see RESEARCH.txt Section 6, RUN 2) -- it is not a real project.

SCOPE (v0.1)
-------------
Four checks only: vocabulary scan, entropy check, reproducibility
cross-check, closure audit. No LLM-judged pass, no GUI, no multi-repo
support. Local static analysis only -- no network calls, no background
processes.
