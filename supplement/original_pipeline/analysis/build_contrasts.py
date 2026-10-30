#!/usr/bin/env python3
"""Synchronise all six paired Acceptance/AAI contrasts from aggregate evidence.

No private records, database connections or model calls are used. Numerical
reproduction does not independently authenticate respondent origin.
"""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    audit = json.loads((ROOT / 'analysis/source_audit.json').read_text())
    aai = audit['AAI_pairs']
    acceptance = audit['additional_contrasts']['ACCEPTANCE']
    if len(aai) != 6 or len(acceptance) != 6:
        raise ValueError('Expected six complete paired contrasts per outcome')
    rows = []
    for a, q in zip(acceptance, aai):
        if (a['a'], a['b']) != (q['a'], q['b']):
            raise ValueError('Contrast outcome order differs')
        al, ah = a['ci95_repository']
        ql, qh = q['ci90_repository']
        rows.append(f"{q['a']}--{q['b']} & {a['mean_difference']:.3f} [{al:.3f}, {ah:.3f}] & {q['mean_difference']:.3f} [{ql:.3f}, {qh:.3f}] " + r'\\')
    content = '\n'.join(rows) + '\n'
    paper = ROOT / 'main.tex'
    source = paper.read_text()
    pattern = r'% BEGIN GENERATED paired_contrasts\n.*?% END GENERATED paired_contrasts'
    if len(re.findall(pattern, source, flags=re.S)) != 1:
        raise ValueError('Missing or duplicated paired-contrast block')
    source = re.sub(pattern, lambda _: '% BEGIN GENERATED paired_contrasts\n' + content + '% END GENERATED paired_contrasts', source, flags=re.S)
    (ROOT / 'analysis/tables/paired_contrasts.tex').write_text(content)
    paper.write_text(source)
    for margin in [.25, .20, .10]:
        n = sum(-margin < q['ci90_repository'][0] and q['ci90_repository'][1] < margin for q in aai)
        print(f'Exploratory AAI margin +/-{margin:.2f}: {n}/6 intervals contained')


if __name__ == '__main__':
    main()
