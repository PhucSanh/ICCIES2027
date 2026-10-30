#!/usr/bin/env python3
"""Create cluster sufficient statistics; no student identifiers or response text.

Reads the private export, never accesses an application or database. Outputs a
local review package; publication/third-party sharing still requires author review.
"""
import argparse, hashlib, json, itertools, re
from pathlib import Path
import numpy as np
import pandas as pd

ITEMS=['ACCURACY','SPECIFICITY','CLARITY','TRANSPARENCY','USEFULNESS','ACTIONABILITY','COMPETENCE TRUST','RELIABILITY','FAIRNESS','AFFECT','PSYCHOLOGICAL SAFETY','ACCEPTANCE','REJECTION','WILLINGNESS','BEHAVIORAL INTENTION']
FORMATS=['Sandwich','Rubric','Explainable','Researching']

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('xlsx',type=Path);args=p.parse_args()
 root=Path(__file__).resolve().parents[1];d=pd.read_excel(args.xlsx,sheet_name='Chi tiết khảo sát sinh viên')
 d=d.rename(columns={c:m[1] for c in d.columns if (m:=re.search(r'\(([A-Z ]+)\)$',str(c)))})
 d=d.rename(columns={'Mã SV':'sid','Repository ID':'repo','Loại feedback':'format','Nguồn sinh câu hỏi':'context'})
 assert d[ITEMS].isin([1,2,3,4,5]).all().all()
 assert (d.groupby('sid').repo.nunique()==1).all()
 assert set(d.context)=={'Codebase','Graph'}
 d['AAI']=d[[i for i in ITEMS if i!='REJECTION']].mean(axis=1)
 design=pd.concat([d.context.eq('Codebase').astype(float).rename('raw'),pd.get_dummies(d['format'],dtype=float).reindex(columns=FORMATS[1:])],axis=1)
 x=(design-design.groupby(d.sid).transform('mean')).to_numpy()
 y=d[['ACCEPTANCE','AAI']]-d.groupby('sid')[['ACCEPTANCE','AAI']].transform('mean')
 repos=list(d.repo.unique());moments=[];totals=[];sizes=[];labels=[]
 for item in ITEMS:
  for a,b in itertools.combinations(FORMATS,2):labels.append({'item':item,'a':a,'b':b})
 wides={k:d.pivot(index='sid',columns='format',values=k).reindex(columns=FORMATS) for k in ITEMS}
 assert all(not w.isna().any().any() for w in wides.values())
 for repo in repos:
  mask=d.repo.eq(repo);sub=d.loc[mask];sids=sub.sid.unique();xx=x[mask.to_numpy()]
  moments.append({'xtx':(xx.T@xx).tolist(),'xty':(xx.T@y.loc[mask].to_numpy()).tolist()})
  totals.append([float((wides[q['item']].loc[sids,q['a']]-wides[q['item']].loc[sids,q['b']]).sum()) for q in labels]);sizes.append(len(sids))
 info=d.groupby('sid').context.nunique().eq(2);info_sids=info[info].index
 item_counts=[[[int((sub[item]==v).sum()) for v in range(1,6)] for item in ITEMS] for repo in repos for sub in [d.loc[d.repo.eq(repo)]]]
 out={'item_labels':ITEMS,'cluster_item_rating_counts':item_counts,'source_sha256':hashlib.sha256(args.xlsx.read_bytes()).hexdigest(),'rows':len(d),'students':int(d.sid.nunique()),'repository_count':len(repos),'replicates':5000,'seed':20261030,'context_predictors':list(design.columns),'context_outcomes':['ACCEPTANCE','AAI'],'context_cluster_moments':moments,'contrast_labels':labels,'contrast_cluster_sums':totals,'cluster_student_counts':sizes,'context_informative_students':int(info.sum()),'context_informative_repositories':int(d.loc[d.sid.isin(info_sids),'repo'].nunique()),'context_means':{k:{'n':int((d.context==k).sum()),'Acceptance':float(d.loc[d.context==k,'ACCEPTANCE'].mean()),'AAI':float(d.loc[d.context==k,'AAI'].mean())} for k in ['Graph','Codebase']},'privacy':'No source identifiers, individual ratings, answers, code, emails or replies. Array order has no published repository identity map. Small cluster aggregates still require disclosure review before public release.'}
 (root/'aggregate/cluster_sufficient_statistics.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
 print('Wrote sufficient statistics for',len(repos),'clusters; 90 paired item comparisons and context models.')
if __name__=='__main__':main()
