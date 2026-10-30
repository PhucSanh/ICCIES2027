#!/usr/bin/env python3
"""Aggregate-only leave-one-repository-out sensitivity of existing survey data.

Does not access a database or establish response provenance. Ranges are point
estimate sensitivity summaries, not confidence intervals or hypothesis tests.
"""
import argparse
import itertools
import json
from pathlib import Path
import re
import numpy as np
import pandas as pd

FORMATS = ['Sandwich', 'Rubric', 'Explainable', 'Researching']
ITEMS = ['ACCURACY','SPECIFICITY','CLARITY','TRANSPARENCY','USEFULNESS','ACTIONABILITY',
         'COMPETENCE TRUST','RELIABILITY','FAIRNESS','AFFECT','PSYCHOLOGICAL SAFETY',
         'ACCEPTANCE','WILLINGNESS','BEHAVIORAL INTENTION']


def context_coefficient(d):
    design = pd.DataFrame({'raw': d['context'].isin(['Codebase','Raw']).astype(float)})
    config = pd.get_dummies(d['format'], dtype=float).reindex(columns=FORMATS[1:])
    design = pd.concat([design, config], axis=1)
    within = design - design.groupby(d.sid).transform('mean')
    y = d.AAI - d.groupby('sid').AAI.transform('mean')
    if np.linalg.matrix_rank(within.to_numpy()) != within.shape[1]:
        raise ValueError('Rank-deficient context specification')
    return float(np.linalg.lstsq(within.to_numpy(), y.to_numpy(), rcond=None)[0][0])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('xlsx', type=Path)
    p.add_argument('--output', type=Path, default=Path(__file__).with_name('leave_one_repository_out.json'))
    args = p.parse_args()
    d = pd.read_excel(args.xlsx, sheet_name='Chi tiết khảo sát sinh viên')
    d = d.rename(columns={c:m[1] for c in d.columns if (m:=re.search(r'\(([A-Z ]+)\)$',str(c)))})
    d = d.rename(columns={'Mã SV':'sid','Loại feedback':'format','Repository ID':'repo','Nguồn sinh câu hỏi':'context'})
    if d[ITEMS].isna().any().any() or not d[ITEMS].isin([1,2,3,4,5]).all().all():
        raise ValueError('Incomplete or out-of-range ratings')
    if not (d.groupby('sid').repo.nunique()==1).all():
        raise ValueError('Students are not nested in repositories')
    d['AAI'] = d[ITEMS].mean(axis=1)
    wide = {key:d.pivot(index='sid',columns='format',values=key).reindex(columns=FORMATS) for key in ['AAI','ACCEPTANCE','ACTIONABILITY']}
    if any(w.isna().any().any() for w in wide.values()):
        raise ValueError('Incomplete configuration blocks')
    mixed = d.groupby('sid').context.nunique().gt(1)
    informative = d[d.sid.isin(mixed[mixed].index)]
    rows = []
    for a,b in itertools.combinations(FORMATS,2):
        entry = {'a':a,'b':b}
        for key,w in wide.items():
            original = float((w[a]-w[b]).mean())
            estimates = []
            for repo in d.repo.unique():
                remaining = d.loc[d.repo.ne(repo),'sid'].unique()
                estimates.append(float((w.loc[remaining,a]-w.loc[remaining,b]).mean()))
            entry[key] = {'full_mean_difference':original,'leave_one_repository_out_min':min(estimates),
                          'leave_one_repository_out_max':max(estimates),
                          'sign_reversals':sum(v*original<0 for v in estimates)}
        rows.append(entry)
    context = [context_coefficient(d.loc[d.repo.ne(repo)]) for repo in d.repo.unique()]
    sizes = d.groupby('repo').sid.nunique()
    result = {'method':'Delete one entire repository and refit; point estimate ranges, not CIs',
              'rows':len(d),'students':int(d.sid.nunique()),'repositories':int(d.repo.nunique()),
              'students_per_repository':{'min':int(sizes.min()),'median':float(sizes.median()),'max':int(sizes.max())},
              'contrasts':rows,
              'context':{'informative_students':int(mixed.sum()),'informative_repositories':int(informative.repo.nunique()),
                         'full_b_raw':context_coefficient(d),'leave_one_repository_out_min':min(context),
                         'leave_one_repository_out_max':max(context),'full_rank_fits':len(context)}}
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'repositories':result['repositories'],'context':result['context'],
                      'Sandwich_Explainable_actionability':rows[1]['ACTIONABILITY']},indent=2))


if __name__ == '__main__':
    main()
