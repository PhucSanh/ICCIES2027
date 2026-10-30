#!/usr/bin/env python3
"""Read-only comparison of a private survey export and a known demo batch.

Writes aggregate evidence only: no answer IDs, student IDs, emails or replies.
The fixture folder must contain manifest.json, before.json and after.json.
No application service or database connection is invoked.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xlsx', type=Path)
    parser.add_argument('fixture_folder', type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('data_provenance_audit.json'))
    args = parser.parse_args()
    paths = {name: args.fixture_folder/name for name in ['manifest.json','before.json','after.json']}
    manifest, before, after = [json.loads(paths[name].read_text()) for name in paths]
    ids = set(manifest['answer_ids'])
    d = pd.read_excel(args.xlsx, sheet_name='Chi tiết khảo sát sinh viên')
    if d['Student Answer ID'].isna().any() or d['Student Answer ID'].duplicated().any():
        raise ValueError('Missing/duplicate answer IDs')
    selected = d['Student Answer ID'].astype(str).isin(ids)
    rows = {str(r['Student Answer ID']): r for _,r in d.iterrows()}
    criteria = {r['Id']:r['Code'] for r in before['criteria']}
    columns = {m[1]:c for c in d.columns if (m:=re.search(r'\(([A-Z ]+)\)$',str(c)))}
    compared = matches = 0
    for rating in after['ratings']:
        aid, code = rating['StudentAnswerId'], criteria[rating['CriterionId']]
        if aid in rows and code in columns:
            compared += 1
            matches += int(rows[aid][columns[code]] == rating['Score'])
    review_matches = reply_matches = review_files = 0
    origins, models = {}, {}
    for aid in ids:
        path = args.fixture_folder/(aid+'.review.json')
        if not path.exists() or aid not in rows:
            continue
        saved = json.loads(path.read_text())
        review_files += 1
        origin, model = saved.get('evaluation_origin'), saved.get('model')
        origins[origin] = origins.get(origin,0)+1
        models[model] = models.get(model,0)+1
        for rating in saved['review']['ratings']:
            code = rating['code']
            if code in columns:
                review_matches += int(rows[aid][columns[code]] == rating['score'])
        reply_matches += int(str(rows[aid]['Ý kiến phản hồi SV (Student Reply)']).strip() == saved['review']['reply'].strip())
    receipt_path = args.fixture_folder/'commit-result.json'
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
    result = {'status':'research_eligibility_hold',
        'source_sha256': hashlib.sha256(args.xlsx.read_bytes()).hexdigest(),
        'private_evidence_sha256': {name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in paths.items()},
        'export_rows':len(d), 'export_students':int(d['Mã SV'].nunique()),
        'known_demo_manifest_rows':len(ids), 'matching_demo_export_rows':int(selected.sum()),
        'matching_demo_students':int(d.loc[selected,'Mã SV'].nunique()),
        'ratings_compared_to_demo_after_snapshot':compared, 'ratings_exactly_matching_demo_snapshot':matches,
        'generation_review_files_compared':review_files,
        'generated_review_origins':origins, 'generated_review_models':models,
        'export_ratings_matching_generated_reviews':review_matches,
        'export_replies_matching_generated_reviews':reply_matches,
        'application_receipt':{k:receipt[k] for k in ['status','origin','rating_rows','scores_changed','replies_updated','post_commit_verified','committed_utc'] if k in receipt},
        'remaining_rows_not_in_this_manifest':int((~selected).sum()),
        'remaining_students_not_in_this_manifest':int(d.loc[~selected,'Mã SV'].nunique()),
        'interpretation':'Known simulated demo ratings contaminate the analysed export. Remaining rows require independent human-response provenance confirmation; absence from this manifest alone does not verify them.',
        'scope':'Read-only workbook and local JSON comparison; no database access, provider calls, identifiers or individual text exported.'}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['private_evidence_sha256','source_sha256']},indent=2))


if __name__ == '__main__':
    main()
