CLAIM CARD
============

RESEARCH QUESTION
------------------
Can a meaningful subset of epistemic-integrity violations in AI-agent-
authored project artifacts -- a locked vocabulary term reappearing, an
entropy budget being exceeded, a reproducibility grade overclaiming its
own logged evidence, a caveat present in a log but dropped from a
closing summary -- be detected through deterministic, pattern-based
text and structure analysis, at a false-positive rate low enough to be
useful to a human reviewer?

HYPOTHESIS
----------
H1 (research hypothesis): yes -- a meaningful subset can be detected
  this way.
H0 (null hypothesis): no -- these violations either don't occur in a
  consistent, detectable textual form, or deterministic analysis can't
  tell a real violation apart from a false positive.

See RESEARCH.txt for the full falsification report, the manual-read
baseline recorded before the tool was run, and what would change my
mind (stated in advance).

NON-GOALS
---------
This is explicitly NOT: an LLM-judged review pass, a general AI-text
detector, a GUI, a multi-repo dashboard, a CI/CD integration, a scope-
compliance or task-boundary checker (that space is already populated --
see RESEARCH.txt Section 2), or a tool that itself asserts a claim is
"verified," "proven," "guaranteed," or "confirmed." A pattern match is
a flag for human review, not a finding of fact.

CURRENT PHASE
--------------
Phase 1 complete for v0.1 scope: the four deterministic checks (Section
10 of the project brief) are implemented and have been run against one
real repo (sopi22/foss-escape-architecture) and one synthetic fixture
with known, planted violations. See RESEARCH.txt Section 10 for the
falsification report; conclusion is WEAKLY SUPPORTED, with named
limitations -- the real-repo run has no ground truth for real
violations (that repo appears to contain none), so it only measures
false-positive noise on clean text, not discriminative power. The
synthetic fixture supplies that missing ground truth and showed clean
recall, but a fixture written to be caught is not the same evidence as
a real repo with a real, naturally-occurring violation. Reproducibility
achieved: R1 (same environment, repeated runs, this session). R2/R3 not
yet performed.

SCOPE (validated vs. tested-and-not-found vs. open)
-----------------------------------------------------
Validated: within this project's own template family only -- repos
that declare a vocabulary lock, an entropy budget, and an R0-R3
reproducibility ladder in their own README/RESEARCH docs, using this
project's own phrasing ("Locked:", "Forbidden:", "R0"-"R3",
"CONCLUSION:"). This is the only setting the four checks have been
run against with any extractable rules to check.

Tested against 3 real external repos with genuinely different
self-declared-constraint phrasing, none from this project's template
family, and found zero extractable rules in any of them (see
RESEARCH.txt Section 11 for the full result):
  - stan-dev/httpstan -- Non-Goals section, in doc/contributing.rst.
  - openai/whisper -- Limitations section, in model-card.md.
  - microsoft/vscode -- explicit contribution rules, in CONTRIBUTING.md.
In each case the repo's real constraint document was not at a
root-level README/RESEARCH path, and separately, none of the three
repos' actual root-level README used this project's specific
vocabulary either.

This is a named, current limitation, not a bug fixed in this pass.
Extraction generalizing beyond this project's own vocabulary and
file-naming convention is an open question, not something planned,
in progress, or on a roadmap -- it has not been scoped as an
experiment yet, and won't be treated as one until it deliberately is.

SETUP / RUN
------------
See scanner/README.txt for exact, copy-pasteable setup and run
commands.

AUTHOR
------
Jhoana Sophia Munar (jhosophie@proton.me)
