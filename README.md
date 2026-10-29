# ICCIES 2027 – PACE feedback-agreement paper

## Build
```
latexmk -pdf main.tex        # or: pdflatex main && bibtex main && pdflatex main && pdflatex main
```
Overleaf: upload the whole folder, set compiler = pdfLaTeX, main document = main.tex.
`llncs.cls`/`splncs04.bst` here are TeX Live v2.24; replace with the v2.25 files from the
conference template if you prefer (both work; `\Description` is provided for v2.24).

## Layout
- `main.tex` – paper (LNCS, ICCIES limit is 12–15 pages)
- `refs.bib` – 34 references, each checked against DOI / publisher / DBLP
- `figures/` – vector PDFs produced by the analysis script (Fig. 1 is TikZ inside main.tex;
  `item_correlations.pdf` is not used in the paper, kept as supplementary)
- `analysis/run_analysis.py` – full, reproducible analysis (seeded bootstrap)
- `analysis/results.json` – every number used in the paper
- `analysis/tables/*.tex` – generated table bodies (already pasted into main.tex)

## Re-run the analysis
```
pip install pandas openpyxl scipy statsmodels matplotlib
python3 analysis/run_analysis.py data/PACE-BaiDaNop-DaDanhGiaAI-2026-10-29_5.xlsx
```
The survey export is NOT in the repo (`data/` is git-ignored) because it contains student IDs and emails. Ask the team for the file and put it in `data/`.

## Data (export 2026-10-29 "(5)")
All 344 records (86 students x 4 formats) pass the screening rules
(no synthetic_fixture marker, feedback stored, all 15 ratings present) -> nothing excluded.
RQ3 context type is read directly from the column "Nguồn sinh câu hỏi" (Codebase = raw code, Graph).
Older versions and old exports are kept locally in `_archive/` (git-ignored).

## Still to fill before submission (search for `TODO` in main.tex)
- ORCIDs (optional)
- citation of the earlier PACE paper (if published)
- recruitment / voluntariness / grading / consent statement
