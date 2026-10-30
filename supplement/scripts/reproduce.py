#!/usr/bin/env python3
"""Reproduce new RQ3 and multiplicity sensitivity from cluster aggregates alone.

Requires numpy. Uses a centred, bootstrap-standardised maximum statistic across
all 90 pairwise item contrasts. This approximate simultaneous-band sensitivity is
post hoc and does not make the analysis confirmatory or validate survey provenance.
"""
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def main():
 s=json.loads((ROOT/'aggregate/cluster_sufficient_statistics.json').read_text())
 rng=np.random.default_rng(s['seed']);k=s['repository_count'];b=s['replicates']
 weights=rng.multinomial(k,np.full(k,1/k),size=b)
 counts=np.array(s['cluster_student_counts']);totals=np.array(s['contrast_cluster_sums'])
 point=totals.sum(axis=0)/counts.sum();boot=weights@totals/(weights@counts)[:,None]
 se=boot.std(axis=0,ddof=1)
 if (se<=0).any():raise ValueError('Zero bootstrap SD in comparison family')
 maximum=np.max(np.abs((boot-point)/se),axis=1);cut=float(np.quantile(maximum,.95))
 contrasts=[]
 for j,label in enumerate(s['contrast_labels']):
  contrasts.append({**label,'difference':float(point[j]),'ci95_unadjusted':np.quantile(boot[:,j],[.025,.975]).tolist(),'ci95_simultaneous_90_comparisons':[float(point[j]-cut*se[j]),float(point[j]+cut*se[j])],'max_stat_adjusted_tail_fraction':float((1+np.sum(maximum>=abs(point[j]/se[j])))/(b+1))})
 xtx=np.array([m['xtx'] for m in s['context_cluster_moments']]);xty=np.array([m['xty'] for m in s['context_cluster_moments']])
 matrices=np.einsum('br,rij->bij',weights,xtx);responses=np.einsum('br,rij->bij',weights,xty)
 if not np.all(np.linalg.matrix_rank(matrices)==len(s['context_predictors'])):raise ValueError('Rank deficient bootstrap context model')
 coeff=np.linalg.solve(xtx.sum(axis=0),xty.sum(axis=0));draws=np.linalg.solve(matrices,responses)
 context={name:{'b_raw':float(coeff[0,j]),'ci95_repository':np.quantile(draws[:,0,j],[.025,.975]).tolist(),'valid_fits':b} for j,name in enumerate(s['context_outcomes'])}
 rating_counts=np.array(s['cluster_item_rating_counts']);rating_sums=rating_counts@np.arange(1,6);rating_n=rating_counts.sum(axis=2)
 item_boot=weights@rating_sums/(weights@rating_n)
 item_summary={item:{'mean':float(rating_sums[:,j].sum()/rating_n[:,j].sum()),'agree_percent':float(100*rating_counts[:,j,3:].sum()/rating_n[:,j].sum()),'ci95_repository_new_seed':np.quantile(item_boot[:,j],[.025,.975]).tolist()} for j,item in enumerate(s['item_labels'])}
 result={'item_summary':item_summary,'replicates':b,'seed':s['seed'],'multiplicity_family':'15 items x 6 configuration pairs = 90 two-sided contrasts, including raw Rejection','simultaneous_method':'95% centred bootstrap-standardised maximum band; fixed bootstrap SD per contrast, not nested studentisation; exploratory approximate sensitivity','max_stat_critical_value':cut,'context':context,'contrasts':contrasts}
 (ROOT/'aggregate/additional_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 chosen=next(c for c in contrasts if c['item']=='ACTIONABILITY' and c['a']=='Sandwich' and c['b']=='Explainable')
 print(json.dumps({'context':context,'actionability_Sandwich_Explainable':chosen},indent=2))
if __name__=='__main__':main()
