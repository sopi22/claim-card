# CLAIM CARD — RESEARCH LOG

## 1. CLARIFICATION GATE (Section 17)

Q: Does FOSS Pulse make a good first test fixture, or should a synthetic
   repo with injected violations be built instead?
A: DECISION — both, not either/or. FOSS Pulse alone (a repo with, as far
   as could be determined, zero real violations) can only test the
   tool's behavior on clean text -- it produces no ground truth for
   whether the checks can actually tell a real violation apart from
   noise, because it has no real violations to find. A synthetic fixture
   with known, deliberately-planted violations closes that gap and gives
   an actual recall/precision reading. Both are used below: FOSS Pulse
   as the real-world baseline, examples/synthetic_violations/ as the
   ground-truth recall test. This decision was made without checking
   back in, per this session's autonomy instruction -- flagged here so
   it can be revisited.

## 2. NOVELTY FIREWALL (Section 4)

Searched (2026-08-13): AI-agent compliance/audit tooling, AI-text
detectors, reproducibility-documentation scorers.

Existing systems found:
  - AudAgent and similar AI-agent compliance auditors: check agent
    behavior against an external privacy/compliance policy document, not
    against a project's own self-declared epistemic rules about its own
    claims.
  - Stylometric AI-text detectors (isgen.ai, GPTZero, etc.): classify
    whether text was AI-written at all -- a different question from
    whether a specific claim in the text matches the evidence logged for
    it.
  - SciScore and similar reproducibility-reporting scorers: score how
    completely a paper documents its methodology, not whether its
    closing claims are proportionate to what was actually logged.
  - General AI-agent scope-compliance/governance platforms: check
    whether an agent stayed within a file/task boundary, not whether its
    own stated claims (a locked term reappearing, a caveat dropped from
    a summary, a reproducibility grade exceeding its logged evidence)
    match what it actually logged.

CONCLUSION: no found system checks a project's own claims against that
same project's own stated epistemic rules. Residual gap holds. Building
is justified. DECISION logged; no fork candidate was found or expected.

### 2A. SUPPLEMENTARY NOVELTY CHECK (2026-08-13, later same day, follow-up)

This entry is additive -- Section 2 above stands as originally logged
and covered a different, real search. The operator surfaced four
additional named candidates via their own web search; each was fetched
and read past its one-line description (README/docs content, not just
a search snippet) before being logged here.

1. github.com/theonaai/Heron -- CONFIRMED, fetched and read.
   Interviews an agent via MCP, then deterministically diffs declared
   capabilities (runtime configs, OAuth scopes, MCP tool inventory)
   against actual access. Does NOT support custom, project-supplied
   rules -- it maps findings to fixed, built-in compliance frameworks
   (EU AI Act, GDPR, ISO/IEC 42001, AIUC-1, NIST AI RMF) via a
   `src/compliance/` framework-control catalogue. `heron.example.yaml`
   configures credentials and which LLM does the analysis, not custom
   audit rules. No plugin or custom-rule-loading mechanism found in the
   documentation.

2. github.com/scadastrangelove/agent-audit -- CONFIRMED, fetched and
   read. Forensic auditor for local AI coding agents; reads session
   logs/configs/instruction files against a fixed, bundled rule set
   (~573 rules total: 104 ATR + 180 Aguara-derived + 26 Cisco
   PromptGuard-derived + 217 Gitleaks-derived + 46 NOVA-derived, plus
   native detectors). No custom-rule config file, plugin architecture,
   or external rule-pack loader is documented as currently available.
   `docs/architecture.md` is referenced as covering "how to add
   detectors/surfaces/rules," which reads as a maintainer-extensibility
   note, not a documented project-facing custom-rules feature -- worth
   a second look if this project is revisited, but not counted as
   custom-rule support here since it isn't demonstrated as such.

3. github.com/yaniv-golan/proof-engine -- CONFIRMED, fetched and read.
   Verifies claims via code-computed or cited evidence rather than LLM
   self-assessment; enforces a fixed set of "9 Hardening Rules" against
   fabricated citations/hallucinated values. `--registry-check` and the
   `proof-citations` package are runtime options, not a custom-rule
   definition mechanism. No custom verification-rule loading found.

4. "Bifrost" (deterministic fact-checker for AI coding agents,
   verifies claims against code/git diff/logs, per search-result
   snippets) -- NOT CONFIRMED. Multiple unrelated projects share this
   name: maximhq/bifrost is an LLM API gateway (unrelated function);
   BrokkAi/bifrost is a multi-language static-analysis/code-query
   engine -- fetched and read directly, and its actual README describes
   "code intelligence for AI, with structural queries," not claim
   verification against git diff/logs, so it does not match the
   description despite the name match. No repository matching the
   fact-checker description as actually described could be confirmed.
   Per instruction, no URL is guessed here. If the operator has the
   exact repo, it still needs to be checked directly.

FINDING: of the three tools that could be confirmed, none support
loading custom, project-declared rules -- all three ship fixed,
built-in rule/framework sets (Heron's compliance-framework catalogue,
agent-audit's bundled signature packs, proof-engine's 9 hardening
rules). The fourth (Bifrost) is unconfirmed and this finding makes no
claim about it either way.

DECISION: Claim Card's stated residual gap -- auditing a project
against rules that project declared for itself, not a fixed external
rule set -- still holds against all three confirmed tools. This
supplementary check does not change the Section 2 conclusion; it adds
three more checked candidates without narrowing the gap. The one
open item is Bifrost's identity, which remains genuinely unresolved,
not resolved in Claim Card's favor by default.

## 3. RESEARCH HYPOTHESIS FRAMING (Section 7)

H1: A meaningful subset of epistemic-integrity violations in AI-agent-
authored project artifacts -- locked-vocabulary leakage, entropy-budget
overruns, reproducibility-grade overclaiming, and completeness-theater
or manufactured-closure patterns in closing reports -- can be detected
via deterministic, pattern-based text/structure analysis at a
false-positive rate low enough to be practically useful.

H0: these violations either don't occur in a detectable, consistent
form, or deterministic analysis can't distinguish real violations from
false positives.

FALSIFICATION CRITERIA (as stated in the brief): if, run against FOSS
Pulse's own real history, the checks produce mostly false positives or
catch nothing a quick manual read wouldn't already catch effortlessly,
that supports H0. If false positives exceed roughly half of flagged
items on the first real test run, that's grounds to reconsider the
deterministic-only approach.

## 4. VOCABULARY LOCK AND ENTROPY BUDGET FOR THIS PROJECT (Sections 9-10)

Locked: claim, check, flag, pattern, evidentiary grade, closure
  language, vocabulary term, entropy count, scan.
Forbidden: capability, provider, broker, cost, negotiation. claim-card's
  own output MUST NOT use "verified," "proven," "guaranteed," or
  "confirmed" about what it detects -- a pattern match is a flag for
  human review. Checked by hand across cli.py/report.py output strings
  before this log was written; none of the forbidden words or
  overclaiming words appear in the tool's own output.

Entropy budget used: 4 check types (vocabulary scan, entropy check,
  reproducibility cross-check, closure audit). 1 persistent format
  (JSON). Transport: none. External services: 0. Network calls: 0.
  Background processes: 0. Dependencies: stdlib only at runtime; pytest
  is a dev-only dependency, same justification pattern as FOSS Pulse's.
  Git history text comes from the `git` binary via subprocess, not a
  parsing library -- closes the one named exception case without adding
  a dependency. Docker: not used, not needed for local static analysis
  of one repo at a time.

## 5. BASELINE -- MANUAL READ (recorded before comparing to tool output)

Before writing any check code, README.md and RESEARCH.md in
foss-escape-architecture were read directly, and a manual grep for the
repo's own forbidden-vocabulary terms and a small set of overclaiming
words (verified, proven, guarantee(d), confirmed, always, never, 100%,
fully) was run across all non-.venv text files.

What this baseline caught:
  - README.md's NON-GOALS list uses "capability", "provider", and
    "cost" as explicitly disclaimed concepts ("this is explicitly NOT
    ... a capability/provider abstraction, a cost model").
  - RESEARCH.md uses "provider" six more times, all as part of
    "Settings provider" / "settings-provider", the literal Android API
    name -- not the locked abstraction sense.
  - "capability" appears once more, inside a quoted phrase describing
    what the project's own epistemic rules reject ("advertised
    capability treated as evidence").
  - "confirmed" appears five times, none of them a claim about the
    tool's own detection accuracy -- each is either "the operator
    confirmed X" or "the probe confirmed the specific path's live
    state," in a sentence that immediately contrasts it with
    "assuming."
  - "verified" appears once, in the CONCLUSION, immediately followed by
    an explicit caveat in the same paragraph.
  - The closing section states "No other items are pending on this
    phase" while a different-OEM-device item is separately marked OPEN,
    NOT-SCHEDULED elsewhere in the same document -- read in full, the
    two statements are consistent (the OPEN item is explicitly scoped
    as non-blocking), not a contradiction.

A quick, unaided skim (not already knowing to search for this specific
term list) would likely have caught the NON-GOALS disclaimer and the
CONCLUSION's "verified" sentence on a careful read, but would plausibly
have missed at least some of the six scattered "Settings provider"
occurrences and the OPEN-item cross-reference, both several hundred
lines apart from the text that would need to be held against them.

## 6. TOOL RESULTS

RUN 1 -- foss-escape-architecture (real repo, first test case):
  17 flags: 11 vocabulary_scan, 6 closure_audit, 0 entropy_check,
  0 reproducibility_cross_check.
  Manual review of all 17: every flag corresponds to one of the
  confounder categories recorded in the baseline above (disclaimed
  non-goal, quoted description, domain-compound API name, hypothetical/
  counterfactual framing, or a caveat legitimately carried into the
  closing section). Zero flags were left unexplained after review.
  Zero entropy or reproducibility flags -- both cross-checked cleanly:
  the repo's probe count, dependency count, and R4-vs-logged-entries
  claim all matched what was declared.

RUN 2 -- examples/synthetic_violations (fixture, known ground truth):
  A small fixture was written with four planted vocabulary violations
  (a real, undisclaimed claim using "capability provider... broker...
  cost"), one planted entropy overrun (3 probe functions against a
  stated "2 maximum"), one planted reproducibility-grade overclaim
  (claims R3, only R1 logged), one planted generality claim without an
  R3 entry, and four planted closure-language violations plus one
  planted nothing-pending/OPEN-item contradiction.
  Result: 12 flags, matching all 12 planted violations exactly. Zero
  false positives, zero false negatives on this fixture.

Bug found and fixed via this fixture: the vocabulary-list and closing-
language regexes only matched phrases on a single line; hand-wrapped
plain text (both FOSS Pulse's and this fixture's own docs wrap at
roughly 78 characters) can split a phrase like "on all devices" across
a line break, silently defeating a literal-space match. Fixed by
matching internal whitespace as \s+ instead of a literal space.
A second bug: the "Forbidden:" list-terminator regex only recognized a
Unicode em-dash, not the ASCII "--" this fixture happened to use, and
silently dropped the last listed term when hit. Fixed to accept both.
Both bugs were caught by disagreement between the tool's output and the
known ground truth in the synthetic fixture -- neither would have been
visible from the FOSS Pulse run alone, since that run had no ground
truth to compare against.

A third, structural bug was found and fixed before either run above:
the heading detector mis-split FOSS Pulse's own RESEARCH.md on a
two-line wrapped heading and a footer paragraph, both purely from
plain-text formatting, not from any content issue. Fixed by requiring a
heading candidate line to be preceded by a blank line, an underline, or
start-of-file.

## 7. FALSE POSITIVES / FALSE NEGATIVES

FALSE POSITIVES: on RUN 1 (real repo), 17/17 flags were confounders
relative to "a real forbidden-vocabulary or overclaiming violation" --
by the strict letter of the brief's "false positives exceed roughly
half of flagged items" criterion, this is over the stated pivot
threshold. See Section 9 for why this reading needs a caveat rather
than a flat pass/fail. On RUN 2 (synthetic), 0/12 flags were false
positives.

FALSE NEGATIVES: none detected on RUN 2 -- all 12 planted violations
were caught. RUN 1 cannot supply a false-negative reading on its own,
since (as far as could be determined by the same manual baseline read)
it contains no real violations to miss.

## 8. CONFOUNDERS CONSIDERED (Section 11)

  - A forbidden term appearing in a disclaimed NON-GOALS/rejected-
    candidates list, not as a real claim -- the majority cause of
    RUN 1's vocabulary_scan flags.
  - A forbidden term used in its ordinary domain sense as part of a
    compound API name ("Settings provider") rather than the locked
    architecture-abstraction sense -- the vocab check now annotates
    this specifically when a capitalized or hyphen-joined prefix word
    matches a small known list, but this is a fixed allowlist, not
    general word-sense disambiguation, and will miss compounds it
    doesn't already know about.
  - An overclaiming-shaped word used in a hypothetical/counterfactual
    sentence ("if observations always tracked X, that would weaken
    H1") rather than as an assertion about actual results -- closure_
    audit does not currently distinguish this case; it was only caught
    by manual review in RUN 1, not flagged with a specific note.
  - A "nothing pending" closing statement that is legitimately
    reconciled with a separately-logged OPEN item elsewhere in the same
    document -- closure_audit flags the co-occurrence but cannot itself
    tell whether the reconciling language is actually present nearby.

## 9. REPRODUCIBILITY LEVEL (Section 12)

R1 -- same environment, repeated runs during this session, both
against foss-escape-architecture and against examples/synthetic_
violations, before and after each bug fix in Section 6.
R2 (separate session) and R3 (separate environment/repo) have not yet
been performed. The conclusion below is graded no higher than R1;
claiming a general false-positive rate for the tool across other real
repos, sight unseen, would be a reproducibility-grade overclaim of
exactly the kind this tool exists to catch, and is not made here.

## 10. FALSIFICATION REPORT (Section 15 deliverable)

QUESTION: can deterministic, pattern-based text/structure analysis
detect the four named classes of epistemic-integrity violation at a
false-positive rate low enough to be practically useful?

PATTERNS TESTED: vocabulary-lock leakage, entropy-budget overrun,
reproducibility-grade overclaiming (achieved-level and generality-
language forms), and closure-language/manufactured-closure patterns
(absolutist words and a nothing-pending-vs-OPEN-item contradiction).

BASELINE (manual read, recorded before running the tool): Section 5.

TOOL RESULT: Section 6, both runs.

FALSE POSITIVES / FALSE NEGATIVES: Section 7.

CONFOUNDERS CONSIDERED: Section 8.

REPRODUCIBILITY LEVEL: R1 (Section 9).

WHAT WOULD CHANGE OUR MIND (as stated in advance): false positives
exceeding roughly half of flagged items on the first real test run.
By a strict, literal count this happened (17/17 on FOSS Pulse). By a
substantive reading it is less clear-cut: FOSS Pulse has no known real
violations, so a 100% confounder rate there is close to the only
possible outcome regardless of how good the checks are -- it measures
noise-on-clean-text, not discriminative power. The synthetic fixture,
which does have a real denominator, showed 0 false positives against
12 known violations. Both readings are recorded rather than picking the
more flattering one.

CONCLUSION: WEAKLY SUPPORTED.
The checks reliably found every planted violation in a fixture with
known ground truth, and did not silently miss anything in the real
repo either (nothing was found there that manual review called a real
violation and the tool missed, though the sample of real violations in
that repo is zero, so this is a weak claim). Against real, honestly-
written text, every flag required a human to spend a few seconds
resolving it against a confounder, and the two structural bugs in
Section 6 show the checks are not yet robust to ordinary plain-text
formatting variation (line wrapping, dash style) without deliberate
testing to catch it. This is short of "false-positive rate low enough
to be practically useful, demonstrated" -- that demonstration needs a
real repo with real, naturally-occurring violations, which neither
fixture here provides -- but it is well short of NOT SUPPORTED, since
the tool is demonstrably not just noise: it distinguishes real
violations from confounders correctly wherever ground truth exists to
check it against.

RECOMMENDED NEXT EXPERIMENT (open item, not scheduled):
  1. Find or wait for a second real repo -- ideally one with at least
     one naturally-occurring violation of its own stated rules -- to
     get an actual joint precision/recall reading on real text, not
     just a clean-text noise reading. Not urgent, not required for this
     phase to be considered complete.
  2. Give closure_audit the same context-aware confounder notes
     vocab_scan already has (hypothetical/counterfactual framing in
     particular), since RUN 1 showed this is currently the check's
     weakest spot.
  3. Repeat RUN 1 in a separate session (R2) before relying on the
     17-flags/17-confounders reading for anything beyond this report.

## END OF PHASE 1 DELIVERABLE.

11. POST-CLOSURE: EXTRACTION GENERALITY CHECK (does not reopen the
    Section 10 conclusion, which was scoped to this project's own
#     template family)

FACT (2026-08-14) -- before pursuing RECOMMENDED NEXT EXPERIMENT item 1
  above (a wider real-repo hunt), checked a prior question: can the
  scanner's extraction stage (rules.py) find anything at all in a real
  repo that does not use this project's own vocabulary ("vocabulary
  lock," "entropy budget," "R0"-"R3," "CONCLUSION:")? Ran the
  unmodified scanner, unmodified extraction regexes, against 3 real
  public repos chosen specifically because each has a genuine
  self-declared-constraint document, in a different form, none from
  this project's template family:
    - stan-dev/httpstan -- an explicit Non-Goals section, but located
      in doc/contributing.rst, not a root-level README/RESEARCH file.
    - openai/whisper -- an explicit Limitations section, but located in
      model-card.md, not a root-level README/RESEARCH file.
    - microsoft/vscode -- an explicit, detailed CONTRIBUTING.md with
      stated rules, but not a root-level README/RESEARCH file (and not
      named "readme"/"research").

  RESULT: extract_rules() returned a completely empty RuleSet on all
  three (no locked terms, no forbidden terms, no entropy-budget lines,
  no repro entries, no conclusion grade) and the scan produced 0 flags
  on all three. Two independent, compounding reasons, both confirmed
  directly rather than assumed:
    1. scan.py's `_doc_texts()` only considers top-level files whose
       stem starts with "readme" or "research" -- each repo's actual
       constraint document lives elsewhere, so none were even read as
       rule sources. (Each repo's actual top-level README *was*
       correctly identified and read -- `rule_source_files` shows
       README.rst / README.md in all three -- so this is not a
       file-walk bug; it is that the genuine constraint text isn't in
       that file for any of these three repos.)
    2. Even where a real top-level README was read (all three), its
       phrasing did not match rules.py's vocabulary-specific regexes
       (`Locked...:`, `Forbidden:`, `^R\d+`, `Reproducibility achieved:
       R\d+`, `CONCLUSION:`, entropy-budget-style `Label: N` lines) --
       none of these three projects happen to phrase their own
       constraints that way, which is unsurprising since that phrasing
       is this project's own convention, not a general one.

DECISION (2026-08-14) -- scope narrowed in README.md (CURRENT PHASE
  section), not in the scanner. No change to rules.py's regexes, no
  change to scan.py's file-selection stage, no CONTRIBUTING.md/
  model-card.md fallback added, even though the finding above suggests
  it would help -- that is exactly the kind of reactive, un-scoped
  patch this check exists to head off. Extraction generalizing beyond
  this project's own vocabulary is left as an open question, not a
  planned or in-progress item: it would need its own falsification-
  first brief (a stated hypothesis about what generalizes and why, a
  baseline, a defined pass/fail bar) before any code changes, not a
  quiet fix prompted by this result. RECOMMENDED NEXT EXPERIMENT item 1
  (Section 10) is updated by this finding but not superseded: a wider
  real-repo hunt for naturally-occurring violations remains open and
  unscheduled, and this result means such a hunt would currently need
  to be restricted to repos already using this project's own
  vocabulary convention to produce any extractable rules at all.

FACT (2026-08-14) -- follow-up hunt, restricted to the narrower
  population named above: public repos that plausibly use this
  project's own template family or closely similar phrasing, found via
  GitHub code/repo search (`gh api search/code`, `search/repositories`)
  rather than a broad real-repo hunt. Searched, in order of
  specificity:
    1. Direct fork/citation: repo search for "foss-escape-architecture"
       and "claim-card"; code search for either name as a string
       reference (fork, "inspired by," citation). Result: zero -- the
       only matches for "foss-escape-architecture" as a repo are
       sopi22's own; no code anywhere references either project by
       name.
    2. Tight combinations of this project's distinctive phrasing:
       "vocabulary lock" + "entropy budget" (3 hits, 2 repos);
       "Locked:" + "Forbidden:" + "entropy budget" (0); "closure audit"
       + "vocabulary lock" (1 hit); "novelty firewall" + "vocabulary
       lock" (0); "Reproducibility achieved: R" (0, this project's own
       regex-matching phrase verbatim); "CONCLUSION: WEAKLY SUPPORTED"
       (0); literal function name "probe_settings_persist" (1 hit);
       "epistemic integrity" + "entropy budget" (26 hits, one repo
       cluster).
    3. Every hit from (2) was fetched and read, not assumed. All were
       confirmed false positives, coincidental term overlap in
       unrelated projects, not this project's template family:
         - UniversalModel/core, UniversalModel/System_Stability_Score:
           a speculative/fringe physics "string theory" manifesto.
           "Vocabulary lock" there means locking physics notation
           terminology; "entropy budget" is literal thermodynamic
           entropy in a Landauer's-principle argument. Unrelated
           subject matter, unrelated meaning of both phrases.
         - ACB-CORE-Labs/builder-2: an unrelated "CodeVault" governance/
           proof framework (Proof classes R/D/U, Axiom Zero, gate-
           ordered roadmap). "Vocabulary lock" labels one glossary doc
           in its own numbering scheme; "B1 Closure Audit" is an
           unrelated document title. No shared structure with this
           project's four named checks.
         - TezcatAI/Tezcat: a Django test file
           (test_probe_limits.py) -- "probe_settings_persist" was a
           token-level false match (probe/settings/persist matched
           separately), not the literal function name.
         - NeuralBlitz/* (LRS-NeuralBlitz, Linkglys, ComputationalAxioms,
           ncx, and related repos): a large, independent, pre-existing
           AI-cognitive-architecture framework ("NBOS") with its own
           extensive invented vocabulary. "Entropy Budget" there is a
           drift/plasticity policy cap; "Epistemic Integrity Chain" is
           their own proof-lineage concept. Neither matches this
           project's usage, and the framework shows no structural
           resemblance (no R0-R3 ladder, no vocabulary-lock-as-scanned-
           rule convention, no falsification-report format).
    4. Looser single-term hits not chased further, per this hunt's own
       scope limit (narrow population, not a broad search): "CONCLUSION:
       SUPPORTED" (141 hits) and "falsification-first" (1704 hits) are
       common enough phrases on their own, in unrelated contexts (ADR
       templates, an apparently distinct AI-agent-skill-registry
       ecosystem), that they don't indicate template-family membership
       without co-occurring with the distinctive markers above -- none
       of which they did in the combination searches run.

  RESULT: zero real candidates found. Every hit specific enough to be
  worth checking was checked, and every one was a confirmed false
  positive -- coincidental vocabulary overlap in unrelated, independent
  projects, several of which (UniversalModel, NeuralBlitz, ACB-CORE-
  Labs) have their own large, unrelated, internally-consistent
  terminology systems of their own that happen to share a phrase or
  two with this project's, not evidence of derivation from it.

DECISION (2026-08-14) -- this is a valid, informative null result, not
  a search failure: per this hunt's own stop condition, no scanner run
  was performed against any candidate (there were none to run it
  against), and the vocabulary-matching regexes were not loosened to
  manufacture candidates. The WEAKLY SUPPORTED conclusion (Section 10)
  is unchanged -- this hunt did not produce a real repo with a
  naturally-occurring violation, so RECOMMENDED NEXT EXPERIMENT item 1
  (Section 10) remains open, unscheduled, and now additionally informed
  by this finding: even restricted to repos plausibly using this
  project's own convention, none currently exist in public GitHub
  search results. A future repo derived from this project's template
  (e.g. a genuine fork, or a project explicitly modeled on it) would be
  the way this population stops being empty -- not something to search
  harder for today.

12. GENERALIZE EXTRACTION EXPERIMENT (2026-08-14, operator-directed,
#     falsification-first)

H1: widening vocab.py's heading-synonym detection and repro.py's
  word-overlap survival check -- more file-discovery patterns, more
  heading synonyms -- lets Claim Card extract and check self-declared
  limitations/non-goals/caveats sections in real, heterogeneous public
  repos, without requiring this project's own bespoke phrasing, while
  keeping false positives low enough to be useful.

H0: widening these mechanisms either still fails to extract anything
  usable, or extracts content but produces mostly false-positive flags
  on manual review.

BASELINE: 0 of 3 previously-tested real repos (httpstan, whisper,
  vscode) produced any extractable content (Section 11).

SCOPE IMPLEMENTED (entropy budget: bounded, no fuzzy/semantic
  matching, no new check type, no new dependencies):
  - scan.py: file discovery widened to an explicit list -- root-level
    CONTRIBUTING.md, model-card.md, LIMITATIONS.md (exact names, not
    prefixes), plus top-level docs/*.rst only (not any nested
    docs/**/*.rst, and not the singular "doc/" some projects use --
    deliberately not chased, see RESULT below).
  - vocab.py: its non-goal heading regex now imports a shared,
    widened LIMITATION_HEADING_RE (structure.py) covering NON-GOALS,
    OUT-OF-SCOPE (hyphen-flexible), LIMITATIONS, KNOWN ISSUES, CAVEATS
    in addition to the original terms.
  - repro.py: new heading-based caveat extraction, reusing the same
    LIMITATION_HEADING_RE and split_sections() -- treats the body of
    any matching section as caveat text and runs the existing
    word-overlap-survival check against it, alongside the original
    literal "CAVEAT:"-line mechanism (kept, unchanged).
  - rules.py: closing-section heading regex widened to also accept
    SUMMARY.
  All four changes are unit-tested (7 new tests, tests/test_scan.py
  added); full suite is 40/40 passing.

BUG FOUND AND FIXED DURING THIS WORK (not part of the falsification
  result, a correctness fix): the new heading-based caveat extraction
  initially fed each matched section's full text -- including its
  underline decoration ("----------") -- through the same
  distinctive-word extraction the literal-CAVEAT-line path uses. A
  token of pure dashes strips down to an empty string, and "" is a
  substring of every Python string, which silently defeated the
  overlap check (a false "found" on every comparison). Fixed by
  dropping empty tokens in _distinctive_words(). Caught by the
  project's own synthetic-fixture regression test failing, not by
  manual inspection -- exactly the kind of thing that test exists to
  catch.

NEW CONFOUNDER FOUND ON THE SYNTHETIC FIXTURE (ground truth: 12
  planted violations, unchanged): the widened repro.py mechanism now
  also flags examples/synthetic_violations/README.md's own
  "NON-GOALS / None stated for this fixture." section, because that
  placeholder wording (also) doesn't survive into the closing text.
  Not a planted violation, and not patched away -- kept, and the two
  integration-test assertions that counted exact flag totals were
  updated (2->3 repro flags, 12->13 total) with an inline comment
  explaining why, per this project's own rule against reactively
  patching a result you don't like. This is a real, if minor, false-
  positive cost of the widening on the one dataset with actual ground
  truth.

TEST SET: the 3 baseline repos (httpstan, whisper, vscode) plus 2 new,
  previously-unseen real repos, chosen for genuinely different
  self-declared-limitations document forms: openai/CLIP (model-card.md,
  headed "Out-of-Scope Use Cases" / "Limitations" / "Bias and
  Fairness" -- richer heading vocabulary than whisper's own model
  card) and EleutherAI/gpt-neox (CONTRIBUTING.md). Several other real
  CONTRIBUTING.md files were read looking for a second positive
  candidate (golang/go, facebook/react, stanfordnlp/dspy,
  allenai/allennlp) -- none contained real limitations/scope content,
  only contribution-process instructions; this is itself a genuine,
  if informal, finding: CONTRIBUTING.md in practice is reliably
  process-only, in every real example checked, none had epistemic
  content this project's checks are meant to catch. gpt-neox was kept
  as the second test repo specifically because it is real and
  representative of that pattern, not because it was expected to
  produce a positive result.

  For all 5, a minimal local directory was built from the exact real
  file content (fetched from raw.githubusercontent.com) at the real
  relative path, rather than a full git clone -- sufficient to
  exercise the real file-discovery and text-parsing logic honestly,
  without the size/time cost of cloning full repos (vscode's tree
  alone would be large) for files whose content is what's actually
  under test.

RESULT, per repo:
  - httpstan: rule_source_files = [README.rst] only. doc/contributing.rst
    still NOT discovered -- its real path uses singular "doc/", which
    the bounded file-discovery pattern ("docs/*.rst") deliberately does
    not match (widening to also catch "doc/" was not in scope and was
    not added). 0 flags. Unchanged from Section 11.
  - whisper: rule_source_files now includes model-card.md (previously
    never read at all -- confirmed improvement). 0 flags.
  - vscode: rule_source_files now includes CONTRIBUTING.md (previously
    never read -- confirmed improvement). 0 flags.
  - clip: rule_source_files now includes model-card.md. 0 flags,
    despite this file having real, on-topic "Out-of-Scope Use Cases"
    and "Limitations" headings.
  - gpt-neox: rule_source_files now includes CONTRIBUTING.md. 2 flags,
    both from check_repro's pre-existing (not part of this widening)
    generality-language regex matching literal "In general" in
    ordinary hostfile-configuration instructions -- ordinary technical
    writing, unrelated to any claim about test/reproducibility
    generality. Both are false positives / confounders on manual
    review.

ROOT CAUSE, CONFIRMED DIRECTLY (not assumed): ran split_sections()
  against every .md/.rst file in the 5-repo test set and counted
  recognized headings. Every one of the 8 real Markdown files (clip
  x2, gpt-neox x2, vscode x2, whisper x2) returned ZERO recognized
  headings. Only httpstan's two genuine RST files, which use real
  underline-style headers, returned any (7 and 2). structure.py's
  split_sections() recognizes exactly two heading styles -- RST-style
  underline (text line + a line of repeated =/- characters) and this
  project's own numbered-ALLCAPS convention ("8. FALSIFICATION
  REPORT") -- and does not recognize standard Markdown ATX headers
  (#, ##, ###) at all. Every real repo in this test set, including
  CLIP's model-card.md with its on-topic "### Limitations" heading,
  uses ATX headers. This is why the widened LIMITATION_HEADING_RE
  never got a chance to match anything on real content: the section
  splitter never hands it a heading string to test in the first
  place. This is a different, deeper gap than "heading vocabulary was
  too narrow" -- it's that section boundaries themselves are never
  detected in the most common real-world heading style.

FALSIFICATION CRITERIA (stated in advance): if most flags across all 5
  are false positives on manual review, that supports H0. RESULT: 2
  flags total were produced across all 5 repos, and both are
  confounders on manual review (2/2 = 100%). The file-discovery
  widening independently worked (3 previously-unread real files are
  now read), but the heading-synonym widening -- the mechanism this
  experiment was actually testing -- produced zero true engagements
  with real content, for a reason (ATX header support) outside this
  experiment's bounded scope.

CONCLUSION: NOT SUPPORTED, for the mechanism as scoped. File-discovery
  widening is a real, tested, non-regressive improvement and is kept.
  Heading-synonym widening is also real, tested, and correct on this
  project's own convention (see the new passing unit tests) -- but it
  does not yet achieve H1's goal on real repos, because a prerequisite
  it implicitly depended on (ATX Markdown header recognition in
  split_sections()) was never in place and was not part of this
  experiment's authorized scope to add. Per this project's own rule
  against reactive, un-scoped patching (Section 11's DECISION), that
  gap is named here, not silently fixed in the same pass.

DECISION: per the operator's own stated gate for this two-phase task,
  Phase A's result is NOT SUPPORTED -- stopping here. Phase B (GitHub
  Action packaging) is not built this round.

RECOMMENDED NEXT EXPERIMENT (open item, not scheduled, needs its own
  falsification-first brief before any code changes, exactly like
  Section 11's DECISION): add ATX Markdown header recognition
  (#, ##, ###) to structure.py's split_sections(), which is shared
  across all four checks and rules.py -- meaning that one change, if
  it holds up, would very likely be what actually unlocks real-repo
  checking generally, not just for the two mechanisms touched in this
  experiment. Given how directly this experiment's own root-cause
  finding points at it, this is a strong candidate for the next
  falsification-first brief -- but it is a structural parser change
  with broader blast radius (every check, not just two), so it earns
  its own scoped experiment rather than being folded into this one
  after the fact.

13. ATX MARKDOWN HEADER SUPPORT (2026-08-14, operator-directed,
#     falsification-first; the structural fix Section 12 identified)

H1: adding standard Markdown ATX-header recognition (#, ##, ###) to
  structure.py's split_sections() -- alongside the existing RST-underline
  and numbered-caps recognition, not replacing them -- lets real repos'
  genuine Limitations/Non-Goals/Caveats sections be detected at all, the
  precondition Section 12 found completely missing.

H0: ATX support still produces mostly false positives on real repos, or
  regresses existing behavior (this project's own repos, httpstan's RST).

BASELINE: Section 12's own result -- 0 of 8 real Markdown files in the
  5-repo test set produced any recognized heading; CLIP's real
  "### Limitations" heading was the clearest concrete miss.

ENTROPY BUDGET: one function (split_sections(), structure.py) gets one
  new heading-pattern branch, plus a fence-state tracker the new branch
  needs to be safe (reasoning below). No new dependency (no markdown/
  commonmark library -- stayed regex/stdlib). No changes to vocab.py or
  repro.py this round -- Section 12 already widened those; this phase
  only unblocks them.

PROPOSED PATTERN (reasoned through before implementing, not after):
  _ATX_HEADING_RE = re.compile(r"^#{1,6}\s+\S.*$")
    Requires whitespace after the '#'s and at least one non-space
    character following -- this alone already rejects "#!/bin/bash" and
    "#SBATCH --job-name=..." (real lines in this test set: gpt-neox's
    README.md), which have no space after '#'. No preceding-blank-line
    requirement, unlike underline style: the '#' prefix is unambiguous
    on its own, so underline style's "could this line just be a rule"
    heuristic doesn't apply to ATX.
  _FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
    Toggled per line; heading detection is suppressed for ALL THREE
    styles while inside a fence, not just ATX -- confirmed necessary,
    not hypothetical: whisper/README.md and gpt-neox/README.md (already
    read as doc sources) both contain fenced shell blocks with lines
    like "# on Ubuntu or Debian" that are comments, not headings.
    Extending suppression to the pre-existing two styles was verified
    to be a no-op for their current passing behavior (this project's
    own .txt docs and httpstan's RST have no triple-backtick fences).

BUG FOUND DURING THIS WORK, BEFORE DECLARING DONE (not part of the
  falsification result, a correctness fix caught by re-running the
  actual 5-repo test set, not assumed clean after the unit tests
  passed): the first implementation stripped a line's indentation
  entirely before testing the ATX pattern. httpstan/README.rst uses
  RST's "::" + 4-space-indented literal-block convention for its
  install commands -- not a fenced code block (no ```/~~~ markers), so
  the fence guard didn't catch it -- and its indented "# Build shared
  libraries" / "# Install the wheel" comment lines were misparsed as
  headings, regressing httpstan's recognized-heading count from 7 (the
  correct Section 12 baseline) to 10. Root cause: CommonMark's own ATX
  spec caps heading indentation at 3 spaces (4+ spaces is an indented
  code block by spec, not a heading) -- the fix applies that same cap
  (`indent <= 3`) rather than stripping indentation away unconditionally.
  Regression test added (test_atx_does_not_match_rst_indented_literal_
  block_comments) alongside 6 other new structure.py tests (fence
  suppression, no-blank-line-needed, all six ATX levels, non-ATX "#!"
  rejection). Full suite: 46/46 passing (40 pre-existing + 6 new).

TEST SET: same 5 real repos as Section 12 (httpstan, whisper, vscode,
  CLIP, gpt-neox), same local minimal-file snapshots, re-run unchanged.

RESULT -- heading recognition (Section 12's own root-cause measurement,
  re-run):
  - clip/README.md: 0 -> 14 recognized headings.
  - clip/model-card.md: 0 -> 18 recognized headings, including the exact
    concrete miss named in Section 12: confirmed directly (not inferred
    from a flag count) that split_sections() now returns "### Out-of-
    Scope Use Cases", "## Performance and Limitations", and
    "## Limitations" as real sections with real body text (1093, 31, and
    550 characters respectively) -- the detection precondition H1 names
    is met.
  - gpt-neox/README.md: 0 -> 60. gpt-neox/CONTRIBUTING.md: 0 -> 10.
  - vscode/README.md: 0 -> 10. vscode/CONTRIBUTING.md: 0 -> 13.
  - whisper/README.md: 0 -> 8. whisper/model-card.md: 0 -> 10.
  - httpstan/README.rst: 7 -> 7 (unchanged, correctly -- RST files don't
    use ATX headers; this is the regression check, not a new gain).
  - httpstan/doc/contributing.rst: 2 -> 2 (unchanged).
  8 of 8 real Markdown files went from zero recognized headings to their
  real heading count; both RST files are unaffected.

RESULT -- scanner flags, full run against all 5 repos: httpstan,
  whisper, vscode, and clip all produced 0 flags (unchanged from Section
  12). gpt-neox produced the same 2 flags as Section 12, same file,
  same lines, same pattern ("In general") -- these come from
  check_repro's pre-existing generality-language regex, a mechanism this
  round did not touch, and are unrelated to heading detection. This
  round produced literally zero NEW flags on any of the 5 repos, so the
  stated falsification criterion ("false positives exceed roughly half
  of flags") does not apply in a meaningful 0-flags-produced sense --
  there is nothing new to be a false positive.

WHY CLIP STILL PRODUCES 0 FLAGS DESPITE ITS LIMITATIONS SECTION NOW
  BEING DETECTED (checked directly, not left as an unexplained gap):
  check_repro's heading-based caveat check only flags when
  `closing_text and hits == 0` -- it requires a non-empty
  `closing_sections` list (a CONCLUSION/CLOSED/FALSIFICATION REPORT/
  DELIVERABLE/CLOSING/SUMMARY heading) to compare the caveat's wording
  against. CLIP's model-card.md has zero closing_sections (confirmed by
  calling extract_rules() on it directly) -- an ordinary model card
  states limitations without a separate "closing summary" in this
  project's specific sense, so the check correctly has nothing to
  compare against and correctly declines to flag, rather than guessing.
  Separately, check_vocab's forbidden-term matching short-circuits
  entirely (`if not forbidden_terms: return flags`) because none of
  these 5 repos declare their own vocabulary lock (already established,
  Section 11/12) -- unrelated to headings, unaffected by this round.
  Both are real, already-understood mechanisms, not new mysteries, and
  both are named as the actual reason 0 flags persist on real repos even
  with the root-cause gap fixed.

FALSIFICATION CRITERIA (stated in advance): if CLIP's real Limitations
  section still isn't detected, that supports H0. RESULT: it is now
  detected, confirmed directly against the actual section objects
  produced (not inferred from a downstream flag count) -- does not
  support H0 on this criterion. If false positives on the 5-repo set
  exceed roughly half of flags, that supports H0. RESULT: zero new
  flags were produced by this change; the 2 flags present are carried
  over unchanged and were already known, pre-existing confounders --
  does not support H0 on this criterion either.

CONCLUSION: SUPPORTED, precisely for what H1 claims -- the detection
  precondition. ATX header recognition is implemented, tested (46/46,
  including a caught-and-fixed regression), and directly confirmed to
  make real repos' genuine Limitations/Non-Goals/Caveats sections
  visible to the downstream checks for the first time, with no
  regression to this project's own convention or to RST files. It does
  NOT yet cause any of the 5 real repos to produce a new, real flag --
  that is a distinct, already-identified, structural fact about
  check_repro's own comparison requirement (needs a closing/summary
  section to compare against, which ordinary real-world docs like model
  cards typically don't have) and check_vocab's requirement (the target
  repo must declare its own vocabulary lock), neither of which this
  round was scoped to change. Per this project's own rule against
  reactive, un-scoped patching (Section 11's DECISION, reaffirmed in
  Section 12's), that gap is named here, not silently patched in the
  same pass.

DECISION: stopping here, as instructed. Phase B (GitHub Action
  packaging) is a separate decision for the operator to greenlight next,
  not automatic from this result.

RECOMMENDED NEXT EXPERIMENT (open item, not scheduled, needs its own
  falsification-first brief before any code changes): whether
  check_repro's closing-section requirement should also recognize a
  real repo's own "conclusion"-shaped ending (a final paragraph, a
  model card's summary line) even without one of the specific headings
  _CLOSING_HEADING_RE already matches -- this is exactly the kind of
  mechanism-widening decision Section 11's DECISION says needs its own
  scoped brief, not a quiet addition here.

14. CLOSING-TEXT FALLBACK FOR CAVEAT-SURVIVAL COMPARISON (2026-08-22,
#     operator-directed, falsification-first; the comparison-text gap
#     Section 13 named)

H1: in check_repro's two wording-survival checks (the CAVEAT-line check
  and the LIMITATION_HEADING_RE-based section check), dropping
  _CLOSING_HEADING_RE as the sole gate on what text a caveat's wording
  is compared against -- and falling back to the rest of the repo's own
  document text when no doc has an explicitly-headed closing section --
  lets these checks actually engage with real repos that state a
  caveat/limitation but have no CONCLUSION/CLOSED/FALSIFICATION REPORT/
  DELIVERABLE/CLOSING/SUMMARY-headed section, the exact structural gap
  Section 13 named as the reason it produced zero new flags on any of
  its 5 real repos even after ATX headers made their Limitations
  sections visible.

H0: falling back to the rest of the document text produces mostly false
  positives on manual review -- e.g. it flags a Limitations section as
  "wording didn't survive" essentially every time a repo simply has no
  closing summary at all (a structurally guaranteed non-overlap, since
  there was never anywhere for the wording to be echoed), rather than
  distinguishing that case from a caveat that was genuinely stated once
  and then dropped.

BASELINE: Section 13's own result -- closing_text is built solely from
  rules.closing_sections (gated by _CLOSING_HEADING_RE in rules.py); 0
  of 5 real repos tested there (httpstan, whisper, vscode, CLIP,
  gpt-neox) produced any closing_sections outside this project's own
  numbered-caps convention, so closing_text was "" for all of them and
  `if closing_text and hits == 0` short-circuited on the empty string --
  both survival checks silently declined to compare at all, rather than
  comparing and finding zero overlap.

ENTROPY BUDGET: both existing loops in checks/repro.py get one local
  fallback expression each; no new function, no new regex, no new file.
  No change to rules.py's extraction, no change to structure.py, no new
  heading vocabulary (LIMITATION_HEADING_RE and _CLOSING_HEADING_RE are
  unchanged), no fuzzy/semantic matching -- still exact substring
  membership on distinctive_words(), same as every prior round.
  closure.py's check_closure and check_caveat_survival are explicitly
  untouched and out of this brief's scope: check_closure scans inside
  closing_sections for its own absolutist-language signal words, a
  different mechanism that doesn't compare against caveat wording at
  all, and check_caveat_survival's closing_text is filename-convention-
  gated (README*-prefixed docs), not _CLOSING_HEADING_RE-gated, so it
  isn't the mechanism this brief is scoped to.

PROPOSED PATTERN (reasoned through before implementing): keep
  `closing_text = "\n".join(s.text for s in closing_sections)` exactly
  as today when closing_sections is non-empty. When it's empty, each of
  the two loops (both already keyed by `path` as they iterate
  doc_texts.items()) compares against
  `"\n".join(t for p, t in doc_texts.items() if p != path)` instead --
  every other doc's text, excluding the current document. The exclusion
  is deliberate, not incidental: without it, a caveat's own line or
  section would always trivially "survive" inside a comparison text that
  still contains that exact line, defeating the check in the opposite
  direction (silently never flagging instead of silently never
  comparing). A repo with only one doc file therefore still correctly
  produces no flag on this path -- there is no "rest of the document
  text" to fall back to -- matching today's behavior for that case
  rather than changing it.

TEST SET: httpstan (README.rst, doc/contributing.rst), whisper
  (README.md, model-card.md), vscode (README.md, CONTRIBUTING.md) --
  fresh live snapshots of the same files Sections 12-13 used -- plus
  examples/synthetic_violations/ (this project's own ground-truth
  fixture) and this repo's own README.md/RESEARCH.md, per the
  operator's own choice of set for this round (replacing Section 13's
  CLIP/gpt-neox pair with the synthetic fixture and a self-scan).

FALSIFICATION CRITERIA (stated in advance): if this change produces a
  new flag on any of the 5 that is a false positive on manual review --
  including the systematic "no closing section exists at all" shape H0
  names, not just an isolated bad match -- that supports H0, and per the
  operator's own stated gate for this round, the change is reverted (not
  patched further) and logged NOT SUPPORTED with the specific case. If
  it produces zero new false positives (whether or not it produces new
  true-eligible flags), that does not support H0 on this criterion.

IMPLEMENTATION: checks/repro.py's `check_repro()` keeps
  `closing_text = "\n".join(s.text for s in closing_sections)` and a new
  `has_closing = bool(closing_sections)`, plus a local
  `_compare_text(path)` helper returning `closing_text` when
  `has_closing`, else `"\n".join(t for p, t in doc_texts.items() if p !=
  path)`. Both existing loops (the CAVEAT-line check, the
  LIMITATION_HEADING_RE section check) call `_compare_text(path)` in
  place of the bare `closing_text` reference for both the `hits = sum(...)`
  line and the `if closing_text and hits == 0` gate. No other file
  touched. Full test suite: 52/52 passing, no regressions.

RESULT: ran against all 5 targets (fresh live snapshots for the 3 real
  repos, fetched the same files Sections 12-13 used):
  - httpstan: 0 flags. Directly confirmed why, not assumed: `_doc_texts()`
    only reads README.rst for this repo -- doc/contributing.rst (singular
    "doc/") is still not discovered, the separate, already-named,
    out-of-scope gap from this memory's open-items list. With only one
    doc read, `_compare_text()`'s fallback has no "rest of the document"
    to fall back to (same as a single-doc repo always has), so this
    round's mechanism was never exercised here at all -- unchanged from
    Section 13.
  - vscode: 0 flags. Both docs (README.md, CONTRIBUTING.md) are read and
    closing_sections is empty, so the fallback path is live, but neither
    doc has a LIMITATION_HEADING_RE-matching section or a literal
    CAVEAT/"residual limitation" line to begin with -- confirmed directly
    by re-running split_sections() over both files. The new mechanism had
    nothing to compare, not a missed comparison.
  - whisper: 0 flags, but this is the one repo where the new mechanism
    actually ran, confirmed directly (not inferred from the flag count):
    model-card.md's real "## Performance and Limitations" section
    produces distinctive words `['performance', 'limitations', 'studies',
    'existing', 'systems', 'models']`; with closing_sections empty, the
    fallback compared this against README.md's text (the only other doc)
    and found real overlap (`performance`, `models` both appear in
    README.md), so `hits == 0` was false and no flag was raised -- a
    correct decline on real evidence, not a silent no-op the way this
    case would have resolved under Section 13's behavior (closing_text
    empty, check never even compares).
  - synthetic_violations fixture: 13 flags, identical to the pre-change
    baseline (5 closure_audit, 1 entropy_check, 3 reproducibility_
    cross_check, 4 vocabulary_scan). Confirmed why unchanged: this
    project's own docs have 2 closing_sections (its own numbered-caps
    CONCLUSION/FALSIFICATION-REPORT convention), so `has_closing` is
    True and `_compare_text()` returns the exact same `closing_text` as
    before -- the new code path is provably not exercised on this
    target, which is the correct non-regression result, not a
    coincidence.
  - claim-card's own README.md/RESEARCH.md (self-scan): 13 flags (2
    closure_audit, 10 reproducibility_cross_check, 1 vocabulary_scan),
    CSR 0.89 -- identical counts to the pre-change baseline for the same
    reason as the synthetic fixture (closing_sections non-empty here
    too, fallback not exercised).

  Zero new flags were produced anywhere in this run, and the one case
  where the new code path actually executed (whisper) was verified by
  direct introspection of `_compare_text()`'s inputs and output, not
  just the final report -- it performed a real comparison and reached a
  correct, evidence-based decision not to flag.

FALSIFICATION CRITERIA RE-CHECKED: no new flag was produced on any of
  the 5, so there is no new false positive to find on manual review --
  does not support H0. The systematic "no closing section exists at
  all" shape H0 warned about (every Limitations section flagging just
  because nothing exists to compare against) did not materialize on
  this set: the one eligible case (whisper) had a second real doc to
  compare against and genuinely found overlap, rather than reaching an
  empty `compare_text` and skipping, or reaching a non-empty
  `compare_text` with no real relationship to the caveat and flagging
  spuriously. Does not support H0.

CONCLUSION: SUPPORTED, precisely for the narrow claim H1 makes -- the
  comparison-text fallback replaces "silently never compare" with
  "actually compare, using real document text," confirmed directly by
  execution trace on the one real repo in this set with the structural
  precondition to exercise it (whisper), with zero new false positives
  and zero regressions (52/52 tests, identical flag counts on both
  targets whose docs already had closing_sections). It does NOT yet
  produce a new true-positive-eligible flag on this 5-repo set --
  httpstan and vscode each fail a different, already-named,
  out-of-scope precondition (single doc discovered; no Limitations
  section present at all) rather than this round's mechanism, and
  whisper's one eligible case resolved as a correct decline on genuine
  evidence rather than a flag. This mirrors Section 13's own precedent
  for how this project grades a mechanism that is directly confirmed
  working as scoped but hasn't yet produced a new real-world catch on a
  small sample -- graded the same way here for consistency, not rounded
  up further.

DECISION: keeping the change -- the stated revert-on-false-positive gate
  for this round was not triggered. Whether check_repro's survival
  checks should also widen beyond LIMITATION_HEADING_RE / the literal
  CAVEAT line, or whether httpstan's doc/-discovery gap should finally be
  closed, remain separate, already-named open items needing their own
  scoped briefs -- not folded into this round.

