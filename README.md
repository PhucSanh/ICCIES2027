# ICCIES 2027 — PACE feedback-perception study

The `codex-review` branch contains the revised manuscript and its self-review.
Read `SELF_REVIEW.md` for evidence, limitations and author confirmations still
needed before submission. The branch is ready for critical review; it is not a
claim that ethics or conference-policy requirements have been resolved.

## Revision after the 30 October review

See `REVISION_RESPONSE_20261030.md` for the reviewer-response matrix and current
validation. Acceptance is now the direct agreement outcome; all six paired
Acceptance and secondary AAI contrasts are reported. Nearest-work positioning,
margin sensitivity and voluntary recruitment have been clarified. The authors
confirm human completion of all 344 ratings (86 students × four configurations).
Local demo snapshot matches do not constitute an authenticated production-DB
audit; the discrepancy and author clarification are preserved in the response
note. No database was accessed or modified during this revision.

## Build

```bash
latexmk -pdf main.tex
# Alternative: pdflatex main && bibtex main && pdflatex main && pdflatex main
# Tectonic alternative (create the output directory first):
mkdir -p /tmp/pace-paper-build
tectonic --keep-logs --keep-intermediates --outdir /tmp/pace-paper-build main.tex
```

Overleaf: upload this folder, select pdfLaTeX and `main.tex`. The checked-in
`main.pdf` and `main.bbl` are rebuilt from the final source. Local validation uses
Tectonic 0.17.0 with the supplied LNCS class and bibliography style. Other compilers
should be checked for pagination independently. ICCIES specifies 12–15 pages.

## Files

- `main.tex`, `main.pdf`, `main.bbl`: revised article and compiled artifacts.
- `refs.bib`: 37 references. Verification scope and evidence are in
  `analysis/REFERENCE_AUDIT.md`; raw registry metadata are in
  `analysis/reference_metadata_audit.json`.
- `analysis/run_analysis.py`, `analysis/results.json`: original statistical
  pipeline and aggregate results. Original student-based intervals and mixed
  models are preserved for comparison; their row-level p-values are not used
  as independent-observation inference in the revised article.
- `analysis/check_export.py`, `analysis/source_audit.json`: independent source
  audit, repository-bootstrap intervals, scoring sensitivity, and student fixed
  effects with configuration adjustment.
- `analysis/build_report.py`: regenerate revised tables, synchronise their marked
  manuscript blocks, and rebuild the configuration plot using repository CIs.
- `analysis/validate_revision.py`: independent OLS verification using explicit
  student dummy variables, contrast checks, table synchronisation and strict JSON.
- `figures/`: vector figures. The correlation heatmap is supplementary.
- `REVIEW_ICCIES2027.md`, `REVISION_NOTES.md`: earlier review and revision history.

## Reproduce locally with the private export

The workbook contains student identifiers, emails, answers and repository data.
It is not committed. Obtain it from the research team and use a local path.

```bash
python3 -m pip install numpy pandas openpyxl scipy statsmodels matplotlib
python3 analysis/run_analysis.py "/path/to/PACE-BaiDaNop-DaDanhGiaAI-2026-10-29 (5).xlsx"
python3 analysis/check_export.py "/path/to/PACE-BaiDaNop-DaDanhGiaAI-2026-10-29 (5).xlsx"
python3 analysis/build_report.py
python3 analysis/build_contrasts.py
python3 analysis/leave_one_repository_out.py "/path/to/PACE-BaiDaNop-DaDanhGiaAI-2026-10-29 (5).xlsx"
python3 analysis/validate_revision.py "/path/to/PACE-BaiDaNop-DaDanhGiaAI-2026-10-29 (5).xlsx"
```

Run `build_report.py` after both analyses: the original pipeline writes older
student-bootstrap table/figure versions; the report step replaces them with the
repository-bootstrap versions used in the revised manuscript. The original
item and composite rank tests remain exploratory. The report step reads only
aggregate JSON and exports no individual student text. Public results now
contain reply counts only; raw replies are not regenerated into public JSON.
Existing Git history has not been rewritten.

All 344 records (86 students × four configurations) pass structural export screening; this is not independent authentication of respondent origin. There
are 28 repositories and 190 questions. Both students and questions are nested
within repositories. One assigned Rubric output is a guardrail refusal; it stays
in the assigned-label analysis and has a block-exclusion sensitivity check.
The source SHA-256 and numerical environment are recorded in the source audit.
The numerical reproduction check and independent validation are documented in
`SELF_REVIEW.md`. Public replication from aggregate artifacts alone cannot replace
access to the private workbook; an approved anonymised data release is pending.

## Verify references

```bash
python3 analysis/verify_references.py
```

This requires network access. It resolves 33 exact DOIs; three non-DOI papers
have manual proceedings/original-article evidence in `analysis/REFERENCE_AUDIT.md`.
DOI resolution confirms bibliographic identity, not every empirical claim.

## Before submission

Authors must document research consent, voluntariness, grading relationships,
institutional review/exemption and data governance. They must also verify the
study deployment's immutable model versions, execution logs and randomisation
implementation, and disclose any earlier PACE publication/overlap. Classroom
use or two exported model names alone do not establish those facts.

The official submission page also prohibits AI-generated text and contains a
2026/2027 wording inconsistency. Authors must clarify its applicability before
submitting text revised with AI assistance. See the linked evidence in the
reference audit. No conference submission is performed by this branch.
