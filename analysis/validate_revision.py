#!/usr/bin/env python3
"""Independent numerical checks for the revised paper against the private export.

Uses an explicit student-dummy OLS design, rather than the demeaning algorithm in
check_export.py. Never writes identifiers or individual responses.
"""
import argparse
import json
from pathlib import Path
import re
import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xlsx', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    a = json.loads((root/'analysis/source_audit.json').read_text())
    d = pd.read_excel(args.xlsx, sheet_name='Chi tiết khảo sát sinh viên')
    d = d.rename(columns={c: m[1] for c in d.columns if (m:=re.search(r'\(([A-Z ]+)\)$',str(c)))})
    d = d.rename(columns={'Mã SV':'sid','Loại feedback':'format','Nguồn sinh câu hỏi':'context'})
    quality = d[['ACCURACY','SPECIFICITY','CLARITY','TRANSPARENCY']].mean(axis=1)
    utility = d[['USEFULNESS','ACTIONABILITY']].mean(axis=1)
    trust = d[['COMPETENCE TRUST','RELIABILITY','FAIRNESS']].mean(axis=1)
    predictors = pd.DataFrame({'PQ':quality,'PU':utility,'TR':trust,
        'AFFECT':d.AFFECT, 'PSYCHOLOGICAL SAFETY':d['PSYCHOLOGICAL SAFETY']})
    z = (predictors-predictors.mean())/predictors.std(ddof=1)
    student = pd.get_dummies(d.sid, dtype=float).to_numpy()
    config = pd.get_dummies(d['format'],dtype=float)[['Rubric','Explainable','Researching']].to_numpy()
    full = np.column_stack([z.to_numpy(),config,student])
    max_error = 0.
    for outcome in ['ACCEPTANCE','WILLINGNESS','BEHAVIORAL INTENTION']:
        coeff = np.linalg.lstsq(full,d[outcome].to_numpy(),rcond=None)[0]
        expected = np.array([a['within_student_models_configuration_adjusted'][outcome][k]['b'] for k in z.columns])
        error = float(np.max(np.abs(coeff[:5]-expected)))
        max_error = max(max_error,error)
        assert error < 1e-10, (outcome,error)
    context = (d.context=='Codebase').astype(float).to_numpy()
    aai_items = ['ACCURACY','SPECIFICITY','CLARITY','TRANSPARENCY','USEFULNESS','ACTIONABILITY',
        'COMPETENCE TRUST','RELIABILITY','FAIRNESS','AFFECT','PSYCHOLOGICAL SAFETY',
        'ACCEPTANCE','WILLINGNESS','BEHAVIORAL INTENTION']
    d['AAI'] = d[aai_items].mean(axis=1)
    cb = np.linalg.lstsq(np.column_stack([context,config,student]),d.AAI.to_numpy(),rcond=None)[0][0]
    context_error = abs(float(cb)-a['context_within_student']['b_raw'])
    assert context_error < 1e-10, context_error
    wide = d.pivot(index='sid',columns='format',values='AAI')[['Sandwich','Rubric','Explainable','Researching']]
    chi = friedmanchisquare(*wide.to_numpy().T).statistic
    assert abs(chi-a['original_result_checks']['AAI_friedman_recomputed']) < 1e-10
    assert all(p['within_exploratory_margin_025'] for p in a['AAI_pairs'])
    assert all(p['ci90_repository'][0]>-.25 and p['ci90_repository'][1]<.25 for p in a['additional_contrasts']['AAI15'])
    assert all(p['ci95_repository'][0]<0<p['ci95_repository'][1] for p in a['additional_contrasts']['ACCEPTANCE'])
    # Ensure generated manuscript blocks match the actual generated table files.
    source = (root/'main.tex').read_text()
    for name in ['rq1_items','within_student_models']:
        body = source.split('% BEGIN GENERATED '+name+'\n')[1].split('% END GENERATED '+name)[0]
        assert body == (root/'analysis/tables'/f'{name}.tex').read_text(),name
    # Public artifacts must remain aggregate-only and strict JSON.
    for name in ['results.json','source_audit.json','reference_metadata_audit.json']:
        json.loads((root/'analysis'/name).read_text(),parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    archived = json.loads((root/'analysis/results.json').read_text())
    assert isinstance(archived['replies'],dict) and archived['replies']['count']==160
    print(json.dumps({'status':'passed', 'explicit_dummy_OLS_max_coefficient_error':max_error,
        'context_coefficient_error':context_error, 'Friedman_chi2':float(chi),
        'generated_tables_match':True,'public_JSON_strict_and_aggregate':True},indent=2))


if __name__ == '__main__':
    main()
