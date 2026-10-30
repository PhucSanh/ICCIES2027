# Numerical validation

The aggregate-only reproduction script was run successfully with Python 3.12 and NumPy 2.3.5. Independent checks against the restricted workbook used explicit student dummy variables (rather than cluster moment estimation) for both context outcomes and four weighted bootstrap samples. All 90 item contrasts and 15 item means/endorsement percentages were also checked.

```json
{
  "status": "passed",
  "maximum_independent_discrepancy": 1.4210854715202004e-14,
  "item_contrasts_verified": 90,
  "direct_dummy_context_outcomes_verified": 2,
  "weighted_dummy_bootstrap_fits_verified": 4,
  "item_means_and_agree_percentages_verified": 15
}
```

These checks validate arithmetic and aggregation, not consent, identity, deployment history, or exact bootstrap coverage. The full bootstrap is reproducible from supplied sufficient statistics; only four selected draws were independently cross-checked against raw-data weighted dummy OLS.
