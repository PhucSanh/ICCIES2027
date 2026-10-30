# PACE review supplement — 30 October 2026

This is a **local review package**, not an externally published dataset or a claim
of submission compliance. Research/disclosure permissions must be checked before
public release. No credentials, student names, student/repository/question identifiers,
individual survey rows, free-text replies or student source code are included.
Even cluster aggregates can carry disclosure risk; no claim of guaranteed
anonymity is made. Respondent origin remains based on the author account, not an
independent production-database authentication.

## Contents and evidence scope

- S1 `INSTRUMENT_VI.md`: Vietnamese statements transcribed from a criteria snapshot;
  source hash and limits are given, with no source IDs. Display-order gaps are
  preserved rather than silently renumbered.
- S2 `PROCEDURE_UI.md`: author-confirmed collection sequence and actual current
  implementation inspection. The frontend commit postdates collection. This is
  not a study-time screenshot or verification of the deployed build.
- S3 `aggregate/cluster_sufficient_statistics.json`: 28 unidentified repository
  clusters, paired-difference sums, rating histograms and within-student context
  model cross-products. No student-level rows are needed for the new analysis.
- `scripts/reproduce.py`: independently executable NumPy reproduction of new RQ3
  coefficients/CIs, all 90 item contrasts, approximate simultaneous bands and item
  means/endorsement percentages. Outputs `aggregate/additional_results.json`.
- S4 `CONFIGURATION_PROFILES.md`: full archived construct profiles and link to the corresponding figure.
- `tables/`: complete actionability comparison family, both context outcomes, and
  readable summaries of all 90 comparisons.
- `original_pipeline/`: original analysis code, archived aggregate results,
  manuscript source, figures and table files. Run on an authorised private export
  to regenerate the earlier analyses. An archived result is not a new rerun.

## Run without private records

From this directory:

```bash
python3 -m pip install -r requirements-minimal.txt
python3 scripts/reproduce.py
```

Python 3.12 and NumPy 2.3.5 were used for local numerical verification. This command
reconstructs context student fixed-effects models from repository-level X'X/X'y
and draws 5,000 repository multinomial resamples with seed 20261030. All 5,000
context fits were full rank. The 26 students exposed to both context types belong
to 12 repositories; block aggregation keeps dependence within a repository.

The item comparison family is **15 items × six unordered configuration pairs =
90 two-sided contrasts**, with raw Rejection retained. For each contrast, the
bootstrap SD standardises centred resampled differences. The 95th percentile of
the maximum absolute standardised difference supplies an approximate simultaneous
band. This uses a fixed bootstrap SD, not replicate-specific nested studentisation.
It is an exploratory, post hoc sensitivity check, with approximate coverage under
independent-repository sampling, only 28 clusters and uncorrected analysis choices
outside this family. Tail fractions in JSON are approximate sensitivity summaries,
not an exact randomisation test or a confirmatory discovery claim.

## Which results are reproduced by which evidence?

| Result | Evidence/reproduction |
|---|---|
| RQ3 direct Acceptance and secondary AAI coefficients/CIs | Fully recomputed from supplied cluster moments; common draws, seed 20261030 |
| All 90 item contrast estimates and simultaneous sensitivity | Fully recomputed from supplied cluster sums; same common draws |
| Item means and endorsement percentages | Fully recomputed from supplied cluster histograms; match archived means/percentages |
| Earlier unadjusted percentile CIs and model diagnostics | Archived in `original_pipeline/analysis`; exact earlier runs require private export and original RNG sequence |
| Prior within-student regression coefficients | Code and archived aggregate output supplied; fresh run requires private export |
| Exact deployment, viewing order/dwell time, provider calls | Not reproduced by survey aggregates; requires historical deployment/event evidence |
| Ethics approval or individually recorded consent | Not established by this computational package |

Small differences between earlier unadjusted CIs and new unadjusted CIs arise
from a different fixed seed/common-draw protocol; they are explicitly separated.
The manuscript's original unadjusted Actionability interval is [0.16, 0.57]; the
new same-family resample gives [0.167, 0.570]. Do not label the original interval
multiplicity-adjusted.

## Restricted-data reproduction of earlier analysis

Only with an authorised workbook, install `requirements-full.txt`, then:

```bash
python3 original_pipeline/analysis/run_analysis.py /authorised/path/export.xlsx
python3 original_pipeline/analysis/check_export.py /authorised/path/export.xlsx
python3 original_pipeline/analysis/build_report.py
python3 original_pipeline/analysis/build_contrasts.py
python3 original_pipeline/analysis/validate_revision.py /authorised/path/export.xlsx
python3 original_pipeline/analysis/leave_one_repository_out.py /authorised/path/export.xlsx
```

These commands write within `original_pipeline/`. Do not run production application
scripts or database mutations. Private exports are intentionally excluded.
To rebuild and independently validate the new sufficient statistics from an authorised private workbook:

```bash
python3 scripts/prepare_private.py /authorised/path/export.xlsx
python3 scripts/reproduce.py
python3 scripts/validate_private.py /authorised/path/export.xlsx
```

The main workspace also retains `analysis/prepare_supplement.py` and
`analysis/validate_supplement.py`. These private-data commands are distinct from
the aggregate-only reproduction command.
