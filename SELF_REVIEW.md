> Cập nhật 30/10/2026: xem [REVISION_RESPONSE_20261030.md](REVISION_RESPONSE_20261030.md) cho vòng sửa sau phản biện và đính chính phạm vi audit nguồn phản hồi. Những mô tả phiên bản cũ bên dưới là lịch sử; không thay thế thông tin mới.

# Self-review of the codex-review revision

Review date: 29 October 2026. Base: local `quanghieu` checkout, clean before
creation of `codex-review`. Scope: mentor-style scientific revision, source
verification, reproducible analysis, independent numerical checks and PDF QA.

## Decision

Ready for Claude/author review in the scope of the available evidence. **Not
submission-ready** until the author-dependent matters below are resolved. There
is no defensible way to invent consent, ethics approval, deployment logs, an
expert correctness audit or new experimental controls from this export.

The strongest defensible contribution is a classroom study of perceptions of
four complete feedback configurations on repository-comprehension answers.
It does not establish correctness, improved learning, a causal next-steps effect,
or a raw-code/graph equivalence result. The paper now states this consistently.

## Findings corrected during self-review

| Issue | Resolution |
|---|---|
| Item table and configuration figure used student-only CIs despite shared repositories. | Both now use 5,000 repository-bootstrap draws; student/question nesting is checked. Rank-test and student-intercept p-values are explicitly exploratory. |
| Acceptance regressions omitted configuration even though perceived utility varies by configuration. | Added configuration indicators. Utility and trust retain positive acceptance associations; perceived-quality CI now includes zero. All 15 regression CIs are unadjusted for multiplicity. |
| Context mixed model combines within- and between-student information. | Replaced the reported estimate with a student fixed-effects/configuration model and repository-bootstrap CI: 0.0723 [−0.0242, 0.1954]. Only 26 students have both contexts. Routing remains confounded by complexity. |
| Equivalence wording could overstate a pragmatic margin. | Main evidence is six repository-bootstrap 90% intervals. The ±0.25 margin remains exploratory and uncalibrated. No item-level equivalence claim. |
| Excluding Rejection was data-informed. | Explicitly retained this disclosure and added all-15-item, reverse-scored sensitivity: mean 4.0089; all six composite intervals remain within the exploratory margin. |
| A Rubric output lacks criteria and includes next steps. | It is a guardrail refusal, retained under the assigned label. Excluding its student block gives n=85, Friedman χ²=23.2207. |
| Actionability gap rounded inconsistently. | Sandwich–Explainable is 0.3721, CI95% [0.1613, 0.5667], reported as 0.37 [0.16, 0.57]. |
| Affective construct and motivation item were conflated in prose. | Separated item-level motivation from the two-item affect score; low affect consistency remains disclosed. |
| References omitted metadata and overstated some transferred evidence. | Corrected Zhang's author order, added DOI/pages, added the automated-feedback review and clustering reference, distinguished debate from sequential synthesis, and kept ENL writing evidence in its own setting. |
| Model alias could be read as a pinned release. | Distinguished `deepseek-chat` from immutable model versions and exported display labels from provider execution evidence. |
| JSON results included individual free-text replies and non-standard NaN. | Public results and future pipeline outputs retain aggregate reply counts only and strict JSON. Existing history was not rewritten. |
| Tables could drift from analysis output. | Added an aggregate-only report builder that regenerates tables, synchronises marked manuscript blocks, and creates the revised configuration figure. |

## Checks and evidence

- Reran the original pipeline from the private source in an isolated temporary
  directory. Every numeric value in the archived results matched within absolute
  tolerance `1e-7`; no numerical discrepancy was found. New privacy changes do
  not change survey statistics.
- Independently reread the workbook: 344 rows, 86 students, 28 repositories,
  190 questions, four complete assigned configurations per student, valid 1–5
  ratings, matching JSON/configuration labels and no explicit fixture marker.
- Recomputed means and Friedman statistic independently: maximum item-mean
  difference 0; AAI Friedman difference 0.
- Repeated repository audit with 5,000 draws and fixed seed 20261029. Every
  within-student bootstrap model had full rank in all 5,000 fits.
- Verified the adjusted regression coefficients using **explicit student dummy
  OLS**, independently of the demeaning implementation: maximum coefficient
  discrepancy `4.39e-15`; context discrepancy `9.85e-16`.
- `validate_revision.py` passes scoring-sensitivity and Acceptance-contrast
  checks, generated-table synchronisation and strict aggregate JSON checks.
- All 33 exact DOI requests succeeded; three non-DOI items were checked against
  official proceedings/original-article evidence. `analysis/REFERENCE_AUDIT.md`
  distinguishes registry checks from claim-level reading and records limitations.
- Final PDF: 15 pages, rebuilt bibliography, no unresolved citations/references,
  missing characters, overfull boxes or BibTeX warnings. Rendered all 15 pages
  and inspected the layout; inspected the updated table and figure pages.
- `git diff --check` passes. Workbook, identifiers, provider credentials and
  extracted application code are not added to this branch.

Numerical environment used: Python 3.12, numpy 2.3.5, pandas 2.2.3,
openpyxl 3.1.5, scipy 1.18.1, statsmodels 0.15.0 and matplotlib 3.11.2.
Compilation: Tectonic 0.17.0; PDF rendering: Poppler. Some font-selection notices
and underfull line notices from TeX are cosmetic; they are not missing-font or
missing-character errors.

## Remaining author-dependent submission blockers

1. Confirm voluntariness, grading implications, research consent, institutional
   review/exemption and governance of student and repository data. The manuscript
   retains an explicit author-confirmation statement; no procedure is fabricated.
2. Verify the deployed revision, assignment mechanism, exact model IDs/versions,
   question-generation prompts and provider execution/fallback logs. A local
   application archive was inspected but cannot establish the exact study
   deployment. Exported role labels do not prove provider calls occurred.
3. Supply any earlier PACE publication and clarify overlap/new contribution.
4. Clarify the conference's AI-text policy. The current official 2027 submission
   page prohibits AI-generated text while its next paragraph refers to 2026.
   This revision is a review artifact, not a compliance certification.

## Material limitations retained

A single university, classroom recruitment with no established sampling frame,
unvalidated instrument, high ratings/possible ceiling effects, only 28 repository
clusters, confounded context routing, different answers for each configuration,
and unmeasured correctness/revision/learning outcomes limit the study. Percentile
bootstrap CIs are approximate with this number of clusters. Shared course-wide
influences are not estimated as an independent replication level. Predictor
associations are contemporaneous and do not establish causal direction.

An expert correctness audit and a controlled same-input feature experiment would
strengthen a future study. Neither has been fabricated or presented as completed.
No external review outcome or acceptance probability is guaranteed.
