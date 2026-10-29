#!/usr/bin/env python3
"""Verify DOI metadata without accepting fuzzy title-search matches as evidence.

Uses the standard library; writes bibliographic metadata only. Non-DOI records
require the explicit proceedings evidence in REFERENCE_AUDIT.md. Network failures
are recorded as failures, never silently treated as successful verification.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import time
import urllib.parse
import urllib.request


def entries(text):
    for match in re.finditer(r'@\w+\s*\{\s*([^,]+),', text):
        start = match.end()
        depth, end = 1, start
        while depth and end < len(text):
            char = text[end]
            if char == '{' and text[end-1] != '\\': depth += 1
            if char == '}' and text[end-1] != '\\': depth -= 1
            end += 1
        body = text[start:end-1]
        fields = {}
        for field in re.finditer(r'(\w+)\s*=\s*\{', body):
            i, depth = field.end(), 1
            j = i
            while depth and j < len(body):
                if body[j] == '{' and body[j-1] != '\\': depth += 1
                if body[j] == '}' and body[j-1] != '\\': depth -= 1
                j += 1
            fields[field[1].lower()] = body[i:j-1]
        yield match[1], fields


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('reference_metadata_audit.json'))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    rows = []
    for key, fields in entries((root/'refs.bib').read_text()):
        row = {'key': key, 'local': fields}
        if 'doi' not in fields:
            row.update(status='manual_proceedings_check', evidence='REFERENCE_AUDIT.md')
        else:
            url = 'https://api.crossref.org/works/' + urllib.parse.quote(fields['doi'], safe='')
            row['metadata_source'] = url
            for attempt in range(3):
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'PACE-bibliographic-audit/1.0'})
                    with urllib.request.urlopen(req, timeout=35) as response:
                        item = json.load(response)['message']
                    row.update(status='resolved_exact_doi', registered={k: item.get(k) for k in
                        ['DOI', 'title', 'author', 'container-title', 'published-print',
                         'published-online', 'volume', 'issue', 'page', 'article-number', 'URL']})
                    break
                except Exception as exc:
                    if attempt == 2: row.update(status='failed', error=str(exc))
                    else: time.sleep(2 + attempt)
            time.sleep(.3)
        rows.append(row)
    args.output.write_text(json.dumps({'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'DOI identity and bibliographic metadata; claim support assessed manually in REFERENCE_AUDIT.md',
        'entries': rows}, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'references': len(rows), 'failures': [r['key'] for r in rows if r['status']=='failed'],
        'manual': [r['key'] for r in rows if r['status']=='manual_proceedings_check']}))
    if any(r['status']=='failed' for r in rows): raise SystemExit(1)


if __name__ == '__main__':
    main()
