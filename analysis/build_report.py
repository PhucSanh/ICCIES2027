#!/usr/bin/env python3
"""Build the revised tables and repository-bootstrap plot from aggregate JSON.
Run after run_analysis.py and check_export.py. Does not read individual records.
"""
import json
import re
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
audit = json.loads((ROOT/'analysis/source_audit.json').read_text())
original = json.loads((ROOT/'analysis/results.json').read_text())
rows = []
for x in original['rq1_items']:
    name = x['item'].title().replace('Behavioral Intention','Behav.\\ intention').replace('Psychological Safety','Psych.\\ safety').replace('Competence Trust','Competence trust')
    if x['item'] == 'REJECTION': name += '$^\\dagger$'
    lo, hi = audit['means'][x['item']]['ci95_repository']
    rows.append(f"{name} & {x['mean']:.2f} ({x['sd']:.2f}) & [{lo:.2f}, {hi:.2f}] & {x['agree']:.1f} & {x['disagree']:.1f} \\\\")
(ROOT/'analysis/tables/rq1_items.tex').write_text('\n'.join(rows)+'\n')
rows = []
for name, key in [('Perceived quality','PQ'),('Perceived utility','PU'),('Trust','TR'),('Motivation','AFFECT'),('Psych.\\ safety','PSYCHOLOGICAL SAFETY')]:
    cells = []
    for outcome in ['ACCEPTANCE', 'WILLINGNESS', 'BEHAVIORAL INTENTION']:
        x = audit['within_student_models_configuration_adjusted'][outcome][key]
        lo, hi = x['ci95_repository']
        cells.append(f"${x['b']:.2f}$ [$ {lo:.2f}, {hi:.2f} $]")
    rows.append(name+' & '+' & '.join(cells)+' \\\\')
(ROOT/'analysis/tables/within_student_models.tex').write_text('\n'.join(rows)+'\n')
plt.rcParams.update({'font.family':'serif', 'font.serif':['Nimbus Roman','DejaVu Serif'],
    'font.size':8, 'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
fig, ax = plt.subplots(figsize=(4.8, 2.8))
formats = ['Sandwich','Rubric','Explainable','Researching']
colors = ['#2a78d6','#eb6834','#1e9e73','#7a4fd1']
keys = ['AAI','PQ','PU','TR','AF','AI']
for fi, fmt in enumerate(formats):
    for ki, key in enumerate(keys):
        x = audit['configuration_means'][fmt][key]
        lo, hi = x['ci95_repository']; y = ki + (fi-1.5)*.17
        ax.plot([lo,hi],[y,y],color=colors[fi],lw=1.4)
        ax.plot(x['mean'],y,['o','s','D','^'][fi],color=colors[fi],ms=6,mec='white',mew=.7,label=fmt if ki==0 else None)
ax.set_yticks(range(6), ['Agreement index','Perceived quality','Perceived utility','Trust','Affect','Acceptance & intention'])
ax.invert_yaxis(); ax.axvline(3,color='#6b6a64',lw=.6,ls=':')
ax.set_xlabel('Mean rating (1–5) with 95% repository-bootstrap CI'); ax.set_xlim(2.95,4.75)
ax.tick_params(axis='y',length=0)
ax.legend(ncol=4,fontsize=6.5,frameon=False,loc='lower center',bbox_to_anchor=(.4,1),handletextpad=.3)
fig.tight_layout();fig.savefig(ROOT/'figures/format_constructs.pdf',bbox_inches='tight');plt.close(fig)
print('Built two revised tables and repository-bootstrap configuration figure.')

# Synchronise the manuscript's generated blocks as well as standalone tables.
paper = ROOT/'main.tex'
source = paper.read_text()
for name in ['rq1_items', 'within_student_models']:
    pattern = r'% BEGIN GENERATED ' + name + r'\n.*?% END GENERATED ' + name
    replacement = '% BEGIN GENERATED ' + name + '\n' + (ROOT/'analysis/tables'/f'{name}.tex').read_text() + '% END GENERATED ' + name
    if len(re.findall(pattern, source, flags=re.S)) != 1:
        raise ValueError(f'Missing/duplicate generated block: {name}')
    source = re.sub(pattern, lambda _: replacement, source, flags=re.S)
paper.write_text(source)
