#!/usr/bin/env python3
"""Independent private-workbook verification of aggregate supplement; read-only."""
import argparse, json, re
from pathlib import Path
import numpy as np
import pandas as pd


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('xlsx',type=Path);a=p.parse_args();root=Path(__file__).resolve().parents[1]
 r=json.loads((root/'supplement/aggregate/additional_results.json').read_text());s=json.loads((root/'supplement/aggregate/cluster_sufficient_statistics.json').read_text())
 d=pd.read_excel(a.xlsx,sheet_name='Chi tiết khảo sát sinh viên');d=d.rename(columns={c:m[1] for c in d.columns if (m:=re.search(r'\(([A-Z ]+)\)$',str(c)))})
 d['AAI']=d[[x for x in s['item_labels'] if x!='REJECTION']].mean(axis=1)
 config=pd.get_dummies(d['Loại feedback'],dtype=float)[['Rubric','Explainable','Researching']]
 student=pd.get_dummies(d['Mã SV'],dtype=float)
 raw=d['Nguồn sinh câu hỏi'].eq('Codebase').astype(float)
 design=np.column_stack([raw,config,student]);outcome=d[['ACCEPTANCE','AAI']].to_numpy()
 explicit=np.linalg.lstsq(design,outcome,rcond=None)[0][0]
 errors=[abs(float(explicit[j])-r['context'][k]['b_raw']) for j,k in enumerate(['ACCEPTANCE','AAI'])]
 for q in r['contrasts']:
  wide=d.pivot(index='Mã SV',columns='Loại feedback',values=q['item'])
  errors.append(abs(float((wide[q['a']]-wide[q['b']]).mean())-q['difference']))
 for item,v in r['item_summary'].items():
  errors.extend([abs(float(d[item].mean())-v['mean']),abs(float(100*d[item].ge(4).mean())-v['agree_percent'])])
 # Independently fit four resamples using explicit student indicators, rather
 # than demeaned cluster cross-products. Duplicate draws give row weights.
 rng=np.random.default_rng(s['seed']);weights=rng.multinomial(28,np.full(28,1/28),size=s['replicates']);repos=list(d['Repository ID'].unique())
 xtx=np.array([m['xtx'] for m in s['context_cluster_moments']]);xty=np.array([m['xty'] for m in s['context_cluster_moments']])
 for w in weights[:4]:
  roww=d['Repository ID'].map(dict(zip(repos,w))).to_numpy();sqrt=np.sqrt(roww)
  direct=np.linalg.lstsq(design*sqrt[:,None],outcome*sqrt[:,None],rcond=None)[0][0]
  aggregate=np.linalg.solve(np.einsum('r,rij->ij',w,xtx),np.einsum('r,rij->ij',w,xty))[0]
  errors.append(float(abs(direct-aggregate).max()))
 assert max(errors)<1e-10,max(errors)
 assert len(r['contrasts'])==90 and len({(q['item'],q['a'],q['b']) for q in r['contrasts']})==90
 for q in r['contrasts']:
  lo,hi=q['ci95_simultaneous_90_comparisons'];assert lo<q['difference']<hi
 print(json.dumps({'status':'passed','maximum_independent_discrepancy':max(errors),'item_contrasts_verified':90,'direct_dummy_context_outcomes_verified':2,'weighted_dummy_bootstrap_fits_verified':4,'item_means_and_agree_percentages_verified':15},indent=2))
if __name__=='__main__':main()
