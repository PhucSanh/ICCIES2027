#!/usr/bin/env python3
"""Read-only source audit and repository-cluster sensitivity analyses.

Usage: python analysis/check_export.py '/path/to/export.xlsx'
Requires numpy, pandas and openpyxl. Writes aggregate results only; never exports
student identifiers, source answers or individual free-text replies.
Bootstrap CIs are percentile intervals (5,000 replicates, seed 20261029).
These analyses supplement, rather than silently replace, the original mixed models.
"""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import platform
import itertools
import json
from pathlib import Path
import re

import numpy as np
import pandas as pd

ITEMS = ['ACCURACY', 'SPECIFICITY', 'CLARITY', 'TRANSPARENCY', 'USEFULNESS',
         'ACTIONABILITY', 'COMPETENCE TRUST', 'RELIABILITY', 'FAIRNESS', 'AFFECT',
         'PSYCHOLOGICAL SAFETY', 'ACCEPTANCE', 'REJECTION', 'WILLINGNESS',
         'BEHAVIORAL INTENTION']
FORMATS = ['Sandwich', 'Rubric', 'Explainable', 'Researching']
B = 5000
SEED = 20261029


def model_names(feedback):
    nested = feedback.get('researching') or {}
    return nested.get('models_involved') or feedback.get('models_involved') or []


def friedman_stat(wide):
    """Friedman statistic with tie correction, complete student blocks only."""
    ranks = pd.DataFrame(wide).rank(axis=1).to_numpy()
    n, k = ranks.shape
    statistic = 12 / (n * k * (k + 1)) * np.square(ranks.sum(axis=0)).sum() - 3 * n * (k + 1)
    ties = sum(sum(t ** 3 - t for t in Counter(row).values()) for row in wide)
    correction = 1 - ties / (n * (k ** 3 - k))
    return float(statistic / correction) if correction else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xlsx', type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('source_audit.json'))
    args = parser.parse_args()
    raw = pd.read_excel(args.xlsx, sheet_name='Chi tiết khảo sát sinh viên')
    ren = {}
    for column in raw.columns:
        match = re.search(r'\(([A-Z ]+)\)$', str(column))
        if match and match[1] in ITEMS:
            ren[column] = match[1]
    d = raw.rename(columns=ren).rename(columns={'Mã SV': 'sid', 'Repository ID': 'repo',
        'Question ID': 'qid', 'Submission ID': 'sub', 'Loại feedback': 'format',
        'Nhận xét của AI': 'fb', 'Nguồn sinh câu hỏi': 'context'})
    for item in ITEMS:
        d[item] = pd.to_numeric(d[item], errors='raise')
    if not d[ITEMS].isin([1, 2, 3, 4, 5]).all().all():
        raise ValueError('Incomplete or out-of-range survey ratings; define exclusions before proceeding.')
    for key in ['sid', 'repo', 'qid', 'sub', 'format', 'context']:
        if d[key].isna().any():
            raise ValueError(f'Missing grouping variable: {key}')
    feedback = d.fb.map(json.loads)
    if not feedback.map(lambda j: isinstance(j, dict)).all():
        raise ValueError('Non-object feedback JSON')
    fixtures = feedback.map(lambda j: j.get('data_origin') == 'synthetic_fixture' or j.get('provider_invoked') is False)
    if fixtures.any():
        raise ValueError('Development fixtures present; apply explicit screening first.')
    if d.groupby(['sid', 'format']).size().ne(1).any() or not d.groupby('sid')['format'].apply(lambda x: set(x) == set(FORMATS)).all():
        raise ValueError('Expected exactly one instance per student and configuration.')
    nested_students = bool(d.groupby('sid').repo.nunique().eq(1).all())
    nested_questions = bool(d.groupby('qid').repo.nunique().eq(1).all())
    if not (nested_students and nested_questions):
        raise ValueError('Repository clusters do not contain students and questions; use crossed-cluster inference.')
    required_fields = {'Sandwich': ['positives', 'constructive_criticism', 'next_steps'],
        'Rubric': ['criteria'], 'Explainable': ['code_evidence', 'logic_explanation'],
        'Researching': ['researching', 'criteria', 'next_steps', 'code_evidence']}
    schema_ok = pd.Series([all(key in j for key in required_fields[fmt])
        for j, fmt in zip(feedback, d['format'])], index=d.index)
    if any(j.get('feedback_type') != fmt for j, fmt in zip(feedback, d['format'])):
        raise ValueError('Feedback JSON and assigned configuration labels disagree')
    bad_students = set(d.loc[~schema_ok, 'sid'])
    schema_counts = {fmt: {'instances': int(d['format'].eq(fmt).sum()),
        'missing_required_fields': int((d['format'].eq(fmt) & ~schema_ok).sum())}
        for fmt in FORMATS}
    if not d.context.isin(['Codebase', 'Raw', 'Graph']).all():
        raise ValueError('Unknown context label')
    d['AAI15'] = (d[[x for x in ITEMS if x != 'REJECTION']].sum(axis=1) + 6 - d.REJECTION) / 15
    d['AF'] = d[['AFFECT', 'PSYCHOLOGICAL SAFETY']].mean(axis=1)
    d['AI'] = d[['ACCEPTANCE', 'WILLINGNESS', 'BEHAVIORAL INTENTION']].mean(axis=1)
    d['AAI'] = d[[x for x in ITEMS if x != 'REJECTION']].mean(axis=1)
    d['PQ'] = d[['ACCURACY', 'SPECIFICITY', 'CLARITY', 'TRANSPARENCY']].mean(axis=1)
    d['PU'] = d[['USEFULNESS', 'ACTIONABILITY']].mean(axis=1)
    d['TR'] = d[['COMPETENCE TRUST', 'RELIABILITY', 'FAIRNESS']].mean(axis=1)
    d['straight'] = d[ITEMS].nunique(axis=1).eq(1)
    rng = np.random.default_rng(SEED)
    repos = list(d.repo.unique())
    cluster_indices = [np.flatnonzero(d.repo.eq(repo)) for repo in repos]
    sampled = rng.integers(0, len(repos), (B, len(repos)))
    # Sample repositories with replacement and retain every student/answer in each.
    selected_rows = [np.concatenate([cluster_indices[i] for i in sample]) for sample in sampled]
    means = {}
    for item in ['AAI'] + ITEMS:
        values = d[item].to_numpy(float)
        boots = np.array([values[idx].mean() for idx in selected_rows])
        means[item] = {'mean': float(values.mean()), 'ci95_repository': np.percentile(boots, [2.5, 97.5]).tolist()}
    wide = d.pivot(index='sid', columns='format', values='AAI')[FORMATS]
    sid_repo = d.groupby('sid').repo.first().reindex(wide.index)
    wi = [np.flatnonzero(sid_repo.eq(repo)) for repo in repos]
    pairs = []
    for a, b in itertools.combinations(FORMATS, 2):
        diff = (wide[a] - wide[b]).to_numpy()
        totals = np.array([diff[idx].sum() for idx in wi])
        sizes = np.array([len(idx) for idx in wi])
        boots = totals[sampled].sum(axis=1) / sizes[sampled].sum(axis=1)
        lo, hi = np.percentile(boots, [5, 95])
        pairs.append({'a': a, 'b': b, 'mean_difference': float(diff.mean()),
                      'ci90_repository': [float(lo), float(hi)],
                      'within_exploratory_margin_025': bool(lo > -.25 and hi < .25)})
    # Additional contrasts use the same repository draws and student weights.
    contrasts = {}
    for outcome in ['ACTIONABILITY', 'ACCEPTANCE', 'AAI15']:
        ow = d.pivot(index='sid', columns='format', values=outcome).reindex(wide.index)[FORMATS]
        rows = []
        for a, b in itertools.combinations(FORMATS, 2):
            delta = (ow[a] - ow[b]).to_numpy()
            totals = np.array([delta[idx].sum() for idx in wi])
            sizes = np.array([len(idx) for idx in wi])
            boots = totals[sampled].sum(axis=1) / sizes[sampled].sum(axis=1)
            rows.append({'a': a, 'b': b, 'mean_difference': float(delta.mean()),
                'ci95_repository': np.percentile(boots, [2.5, 97.5]).tolist(),
                'ci90_repository': np.percentile(boots, [5, 95]).tolist()})
        contrasts[outcome] = rows
    configuration_means = {}
    for fmt in FORMATS:
        configuration_means[fmt] = {}
        for outcome in ['AAI', 'PQ', 'PU', 'TR', 'AF', 'AI']:
            totals = np.array([d.loc[d.repo.eq(repo) & d['format'].eq(fmt), outcome].sum() for repo in repos])
            sizes = np.array([int((d.repo.eq(repo) & d['format'].eq(fmt)).sum()) for repo in repos])
            boots = totals[sampled].sum(axis=1) / sizes[sampled].sum(axis=1)
            configuration_means[fmt][outcome] = {'mean': float(d.loc[d['format'].eq(fmt), outcome].mean()),
                'ci95_repository': np.percentile(boots, [2.5, 97.5]).tolist()}
    # Student fixed effects: demean predictors/outcomes within student, then OLS.
    # Repository bootstrap preserves repeated students and all shared questions.
    predictors = ['PQ', 'PU', 'TR', 'AFFECT', 'PSYCHOLOGICAL SAFETY']
    z = (d[predictors] - d[predictors].mean()) / d[predictors].std(ddof=1)
    x = (z - z.groupby(d.sid).transform('mean')).to_numpy()
    within_models = {}
    for outcome in ['ACCEPTANCE', 'WILLINGNESS', 'BEHAVIORAL INTENTION']:
        y = (d[outcome] - d.groupby('sid')[outcome].transform('mean')).to_numpy()
        if np.linalg.matrix_rank(x) != x.shape[1]:
            raise ValueError('Rank-deficient within-student predictor design')
        coefficient = np.linalg.lstsq(x, y, rcond=None)[0]
        boot = []
        for idx in selected_rows:
            if np.linalg.matrix_rank(x[idx]) == x.shape[1]:
                boot.append(np.linalg.lstsq(x[idx], y[idx], rcond=None)[0])
        if len(boot) != B:
            raise ValueError('Rank-deficient predictor bootstrap; inspect before reporting')
        intervals = np.percentile(np.array(boot), [2.5, 97.5], axis=0)
        within_models[outcome] = {'bootstrap_valid': len(boot), 'predictors': {
            name: {'b': float(coefficient[i]), 'ci95_repository': intervals[:, i].tolist()}
            for i, name in enumerate(predictors)}}
    # Sensitivity: control configuration in the association models. The three
    # dummy columns are demeaned within student, just like the other predictors.
    config = pd.get_dummies(d['format'], dtype=float).reindex(columns=FORMATS[1:])
    xc = (config - config.groupby(d.sid).transform('mean')).to_numpy()
    adjusted_models = {}
    def fit_boot(design, response):
        coef = np.linalg.lstsq(design, response, rcond=None)[0]
        boot = [np.linalg.lstsq(design[idx], response[idx], rcond=None)[0]
                for idx in selected_rows if np.linalg.matrix_rank(design[idx]) == design.shape[1]]
        if len(boot) != B:
            raise ValueError('Rank-deficient bootstrap design; inspect before reporting')
        return coef, np.percentile(boot, [2.5, 97.5], axis=0)
    for outcome in ['ACCEPTANCE', 'WILLINGNESS', 'BEHAVIORAL INTENTION']:
        y = (d[outcome] - d.groupby('sid')[outcome].transform('mean')).to_numpy()
        coef, ci = fit_boot(np.column_stack([x, xc]), y)
        adjusted_models[outcome] = {name: {'b': float(coef[i]), 'ci95_repository': ci[:, i].tolist()}
            for i, name in enumerate(predictors)}
    raw_context = d.context.isin(['Codebase', 'Raw']).astype(float)
    context_within = (raw_context - raw_context.groupby(d.sid).transform('mean')).to_numpy()
    y = (d.AAI - d.groupby('sid').AAI.transform('mean')).to_numpy()
    coef, ci = fit_boot(np.column_stack([context_within, xc]), y)
    context_model = {'b_raw': float(coef[0]), 'ci95_repository': ci[:, 0].tolist(),
        'specification': 'student fixed effects and configuration indicators; repository bootstrap'}
    nonstraight_sids = d.groupby('sid').straight.any()
    complete_ns = wide.loc[~nonstraight_sids.reindex(wide.index)]
    scoring = {'AAI15_mean': float(d.AAI15.mean()),
        'AAI15_friedman': friedman_stat(d.pivot(index='sid', columns='format', values='AAI15')[FORMATS].to_numpy()),
        'nonstraight_complete_students': len(complete_ns),
        'nonstraight_complete_means': complete_ns.mean().to_dict()}
    provenance = Counter(','.join(model_names(j)) for j, fmt in zip(feedback, d['format']) if fmt == 'Researching')
    baseline = json.loads(Path(__file__).with_name('results.json').read_text())
    differences = {item: float(d[item].mean() - next(r['mean'] for r in baseline['rq1_items'] if r['item'] == item)) for item in ITEMS}
    chi = friedman_stat(wide.to_numpy())
    fidelity_wide = wide.loc[~wide.index.isin(bad_students)]
    expected_chi = next(r['chi2'] for r in baseline['rq2']['friedman'] if r['var'] == 'AAI')
    result = {'source': {'filename': args.xlsx.name, 'sha256': hashlib.sha256(args.xlsx.read_bytes()).hexdigest()},
        'environment': {'python': platform.python_version(), **{name: importlib.metadata.version(name) for name in ['numpy', 'pandas', 'openpyxl']}},
        'method': {'bootstrap_clusters': 'repository', 'replicates': B, 'seed': SEED,
            'interval': 'percentile', 'within_model': 'student fixed effects, repository bootstrap, separate motivation and safety'},
        'counts': {'rows': len(d), 'students': int(d.sid.nunique()), 'repos': len(repos),
            'questions': int(d.qid.nunique()), 'formats': d['format'].value_counts().to_dict(),
            'contexts': d.context.value_counts().to_dict(), 'straight_rows': int(d.straight.sum())},
        'nesting': {'students_within_repository': nested_students, 'questions_within_repository': nested_questions},
        'exported_researching_models': dict(provenance),
        'configuration_fidelity': {'schema_counts': schema_counts,
            'complete_blocks_excluding_schema_deviation_students': len(fidelity_wide),
            'AAI_friedman_excluding_schema_deviation_students': friedman_stat(fidelity_wide.to_numpy())},
        'original_result_checks': {'item_mean_max_absolute_difference': max(abs(v) for v in differences.values()),
            'AAI_friedman_recomputed': chi, 'AAI_friedman_archived': expected_chi,
            'AAI_friedman_absolute_difference': abs(chi - expected_chi)},
        'means': means, 'configuration_means': configuration_means, 'AAI_pairs': pairs,
        'additional_contrasts': contrasts, 'scoring_sensitivity': scoring,
        'within_student_models': within_models, 'within_student_models_configuration_adjusted': adjusted_models,
        'context_within_student': context_model,
        'limitations': ['Exported model names are metadata, not independent provider logs.',
            'No causal comparison of individual configuration features.',
            'Context is selected by method count; no isolated raw-code/graph effect.',
            'Original mixed models and signed-rank tests are not rerun by this script.']}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    print(json.dumps({'counts': result['counts'], 'checks': result['original_result_checks'],
        'provenance': dict(provenance), 'pairwise_repository_intervals': pairs,
        'within_student_models': within_models}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
