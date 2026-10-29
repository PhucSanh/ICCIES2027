#!/usr/bin/env python3
"""Statistical analysis for the PACE feedback-agreement study.

Usage:
    python3 analysis/run_analysis.py data/PACE_KetQuaKhaoSat_2026-10-29.xlsx [question_context.csv]

The optional CSV (columns: question_id, context_type with values Raw|Graph) enables RQ3.
Outputs: analysis/results.json, analysis/tables/*.tex, figures/*.pdf
"""
import json, sys, os, re
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
XLSX = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data/PACE_KetQuaKhaoSat_2026-10-29.xlsx"
CTX = Path(sys.argv[2]) if len(sys.argv) > 2 else None
OUT = ROOT / "analysis"; TAB = OUT / "tables"; FIG = ROOT / "figures"
TAB.mkdir(parents=True, exist_ok=True); FIG.mkdir(exist_ok=True)
RNG = np.random.default_rng(20261029)
B = 5000

ITEMS = ["ACCURACY", "SPECIFICITY", "CLARITY", "TRANSPARENCY", "USEFULNESS", "ACTIONABILITY",
         "COMPETENCE TRUST", "RELIABILITY", "FAIRNESS", "AFFECT", "PSYCHOLOGICAL SAFETY",
         "ACCEPTANCE", "REJECTION", "WILLINGNESS", "BEHAVIORAL INTENTION"]
SHORT = {"ACCURACY": "ACC", "SPECIFICITY": "SPE", "CLARITY": "CLA", "TRANSPARENCY": "TRA",
         "USEFULNESS": "USE", "ACTIONABILITY": "ACT", "COMPETENCE TRUST": "COM", "RELIABILITY": "REL",
         "FAIRNESS": "FAI", "AFFECT": "AFF", "PSYCHOLOGICAL SAFETY": "PSY", "ACCEPTANCE": "ACE",
         "REJECTION": "REJ", "WILLINGNESS": "WIL", "BEHAVIORAL INTENTION": "BI"}
CONSTRUCTS = {
    "Perceived quality": ["ACCURACY", "SPECIFICITY", "CLARITY", "TRANSPARENCY"],
    "Perceived utility": ["USEFULNESS", "ACTIONABILITY"],
    "Trust": ["COMPETENCE TRUST", "RELIABILITY", "FAIRNESS"],
    "Affect": ["AFFECT", "PSYCHOLOGICAL SAFETY"],
    "Acceptance \\& intention": ["ACCEPTANCE", "WILLINGNESS", "BEHAVIORAL INTENTION"],
}
FORMATS = ["Sandwich", "Rubric", "Explainable", "Researching"]
R = {}


def holm(p):
    p = np.asarray(p, float); m = len(p); o = np.argsort(p); adj = np.empty(m); run = 0
    for k, i in enumerate(o):
        run = max(run, (m - k) * p[i]); adj[i] = min(1, run)
    return adj


def cronbach(df):
    df = df.dropna(); k = df.shape[1]
    return k / (k - 1) * (1 - df.var(ddof=1).sum() / df.sum(axis=1).var(ddof=1))


def omega_total(df):
    """McDonald's omega from a one-factor solution (principal axis, 50 iterations)."""
    X = df.dropna().values; C = np.corrcoef(X, rowvar=False)
    h = 1 - 1 / np.diag(np.linalg.inv(C))
    for _ in range(50):
        Cr = C.copy(); np.fill_diagonal(Cr, h)
        w, v = np.linalg.eigh(Cr); lam = v[:, -1] * np.sqrt(max(w[-1], 0))
        h = np.clip(lam ** 2, 0.005, 0.995)
    lam = np.abs(lam); return lam.sum() ** 2 / (lam.sum() ** 2 + (1 - lam ** 2).sum())


def cluster_boot_mean(df, col, cluster="sid"):
    g = df.groupby(cluster)[col].agg(["sum", "count"]).values; n = len(g)
    idx = RNG.integers(0, n, (B, n)); s = g[idx, 0].sum(1) / g[idx, 1].sum(1)
    return np.percentile(s, [2.5, 97.5])


def wilcoxon_vs(x, mu=3.0):
    d = np.asarray(x) - mu; d = d[d != 0]
    res = stats.wilcoxon(d)
    r = stats.rankdata(np.abs(d)); wp = r[d > 0].sum(); wm = r[d < 0].sum()
    return res.pvalue, (wp - wm) / (wp + wm), len(d)


# ---------------------------------------------------------------- load & screen
raw = pd.read_excel(XLSX, sheet_name=1)
ren = {}
for c in raw.columns:
    m = re.search(r"\(([A-Z ]+)\)$", str(c))
    if m and m.group(1) in ITEMS: ren[c] = m.group(1)
raw = raw.rename(columns=ren).rename(columns={
    "Mã SV": "sid", "Loại feedback": "format", "Nhận xét của AI": "fb", "Câu trả lời SV": "answer",
    "Ý kiến phản hồi SV (Student Reply)": "reply", "Question ID": "qid", "Submission ID": "sub",
    "Thời gian nộp bài (UTC)": "ts", "Repository ID": "repo", "Business ID": "biz"})


def origin(s):
    try:
        j = json.loads(s)
    except Exception:
        return "missing_feedback"
    if j.get("data_origin") == "synthetic_fixture" or j.get("provider_invoked") is False:
        return "synthetic"
    return "llm"


raw["origin"] = raw["fb"].map(origin)
if "Nguồn sinh câu hỏi" in raw.columns:  # context type is exported directly since the 2026-10-29 (5) export
    raw["context_type"] = raw["Nguồn sinh câu hỏi"].map({"Codebase": "Raw", "Raw": "Raw", "Graph": "Graph"})
for c in ITEMS: raw[c] = pd.to_numeric(raw[c], errors="coerce")
raw["rated"] = raw[ITEMS].notna().all(axis=1)
screen = {
    "rows_total": int(len(raw)), "submissions_total": int(raw["sub"].nunique()),
    "rows_synthetic": int((raw.origin == "synthetic").sum()),
    "subs_synthetic": int(raw.loc[raw.origin == "synthetic", "sub"].nunique()),
    "rows_missing_feedback": int((raw.origin == "missing_feedback").sum()),
    "rows_llm": int((raw.origin == "llm").sum()),
    "rows_llm_unrated": int(((raw.origin == "llm") & ~raw.rated).sum()),
}
d = raw[(raw.origin == "llm") & raw.rated].copy()
d["REJECTION_R"] = 6 - d["REJECTION"]
ALL15 = [c if c != "REJECTION" else "REJECTION_R" for c in ITEMS]
AAI14 = [c for c in ITEMS if c != "REJECTION"]
d["AAI"] = d[AAI14].mean(axis=1)  # REJECTION analysed separately (see reliability)
for k, v in CONSTRUCTS.items(): d[k] = d[v].mean(axis=1)
d["sd_row"] = d[ITEMS].std(axis=1, ddof=0)
d["straight"] = d["sd_row"] == 0
screen.update(rows_analysed=int(len(d)), students=int(d.sid.nunique()), repos=int(d.repo.nunique()),
              businesses=int(d.biz.nunique()), questions=int(d.qid.nunique()),
              complete_blocks=int((d.groupby("sid")["format"].nunique() == 4).sum()),
              straight_rows=int(d.straight.sum()),
              straight_students_all=int(d.groupby("sid")["straight"].all().sum()),
              dates=sorted(d.ts.str[:10].unique().tolist()),
              format_counts=d.format.value_counts().to_dict())
d["ans_len"] = d["answer"].astype(str).str.split().str.len()


def fb_text(s):
    j = json.loads(s); out = []
    def walk(x):
        if isinstance(x, str): out.append(x)
        elif isinstance(x, dict): [walk(v) for k, v in x.items() if k not in ("student_answer_id", "feedback_type", "models_involved")]
        elif isinstance(x, list): [walk(v) for v in x]
    walk(j); return " ".join(out)


def fb_score(s):
    j = json.loads(s); sc = [c.get("score") for c in (j.get("criteria") or []) if isinstance(c.get("score"), (int, float))]
    return np.mean(sc) if sc else np.nan


d["fb_len"] = d["fb"].map(lambda s: len(fb_text(s).split()))
d["ai_score"] = d["fb"].map(fb_score)
screen["ans_len_mean"] = float(d.ans_len.mean())
def _models(s_):
    try:
        j = json.loads(s_)
        return ",".join((j.get("researching") or {}).get("models_involved") or j.get("models_involved") or [])
    except Exception: return ""
screen["researching_models"] = d.loc[d.format == "Researching", "fb"].map(_models).value_counts().to_dict()
R["screening"] = screen

# ---------------------------------------------------------------- reliability
rel = {"alpha_15": cronbach(d[ALL15]), "omega_15": omega_total(d[ALL15]),
       "alpha_14_noREJ": cronbach(d[[c for c in ALL15 if c != "REJECTION_R"]]),
       "omega_14_noREJ": omega_total(d[[c for c in ALL15 if c != "REJECTION_R"]])}
for k, v in CONSTRUCTS.items():
    rel["alpha_" + k] = cronbach(d[v]) if len(v) > 1 else np.nan
tot = d[ALL15].sum(axis=1)
rel["item_rest"] = {SHORT[i]: float(np.corrcoef(d[c], tot - d[c])[0, 1]) for i, c in zip(ITEMS, ALL15)}
rel["rho_ACE_REJ"] = float(stats.spearmanr(d.ACCEPTANCE, d.REJECTION)[0])
rel["p_ACE_REJ"] = float(stats.spearmanr(d.ACCEPTANCE, d.REJECTION)[1])
ns = d[~d.straight]
rel["rho_ACE_REJ_nostraight"] = float(stats.spearmanr(ns.ACCEPTANCE, ns.REJECTION)[0])
rel["p_ACE_REJ_nostraight"] = float(stats.spearmanr(ns.ACCEPTANCE, ns.REJECTION)[1])
rel["rho_AAI_REJ"] = float(stats.spearmanr(d.AAI, d.REJECTION)[0])
rel["rho_AAI_REJ_nostraight"] = float(stats.spearmanr(ns.AAI, ns.REJECTION)[0])
rel["p_AAI_REJ_nostraight"] = float(stats.spearmanr(ns.AAI, ns.REJECTION)[1])
rel["alpha_14_nostraight"] = cronbach(ns[AAI14])
for k, v in CONSTRUCTS.items():
    rel["alpha_" + k] = cronbach(d[v]) if len(v) > 1 else np.nan
R["reliability"] = rel

# ---------------------------------------------------------------- RQ1 descriptives
stu = d.groupby("sid")[ITEMS + ["REJECTION_R", "AAI"] + list(CONSTRUCTS)].mean()
rows = []
for i in ITEMS:
    x = d[i]; ci = cluster_boot_mean(d, i)
    p, rrb, n = wilcoxon_vs(stu[i])
    rows.append(dict(item=i, short=SHORT[i], mean=x.mean(), sd=x.std(), median=x.median(), lo=ci[0], hi=ci[1],
                     agree=(x >= 4).mean() * 100, neutral=(x == 3).mean() * 100, disagree=(x <= 2).mean() * 100,
                     p=p, rrb=rrb, n=n, **{f"p{k}": (x == k).mean() * 100 for k in range(1, 6)}))
rq1 = pd.DataFrame(rows); rq1["p_holm"] = holm(rq1.p)
R["rq1_items"] = rq1.to_dict("records")
cons = []
for k in ["AAI"] + list(CONSTRUCTS):
    ci = cluster_boot_mean(d, k); p, rrb, n = wilcoxon_vs(stu[k])
    cons.append(dict(construct=k, mean=d[k].mean(), sd=d[k].std(), lo=ci[0], hi=ci[1], p=p, rrb=rrb,
                     agree=(d[k] >= 4).mean() * 100))
cons = pd.DataFrame(cons); cons["p_holm"] = holm(cons.p); R["rq1_constructs"] = cons.to_dict("records")

# acceptance drivers: mixed model with standardized predictors, random intercept per student
dz = d.copy()
pred = {"Perceived quality": "PQ", "Perceived utility": "PU", "Trust": "TR", "Affect": "AF"}
for k, s in pred.items(): dz[s] = (dz[k] - dz[k].mean()) / dz[k].std()
dz["ACE"] = dz["ACCEPTANCE"]; dz["WIL"] = dz["WILLINGNESS"]; dz["BI"] = dz["BEHAVIORAL INTENTION"]
drivers = {}
for y in ["ACE", "WIL", "BI"]:
    m = smf.mixedlm(f"{y} ~ PQ + PU + TR + AF", dz, groups=dz["sid"]).fit(reml=True)
    drivers[y] = {s: dict(b=m.params[s], se=m.bse[s], p=m.pvalues[s]) for s in pred.values()}
    resid = dz[y] - m.fittedvalues; fe = m.model.exog @ m.fe_params
    var_f = np.var(fe); var_u = float(m.cov_re.iloc[0, 0]); var_e = m.scale
    drivers[y]["R2m"] = var_f / (var_f + var_u + var_e); drivers[y]["R2c"] = (var_f + var_u) / (var_f + var_u + var_e)
Xv = dz[list(pred.values())].values
drivers["VIF"] = {s_: float(1 / (1 - np.corrcoef(Xv[:, i], Xv[:, [j for j in range(4) if j != i]] @ np.linalg.lstsq(Xv[:, [j for j in range(4) if j != i]], Xv[:, i], rcond=None)[0])[0, 1] ** 2)) for i, s_ in enumerate(pred.values())}
R["rq1_drivers"] = drivers
# intra-class correlation of AAI
m0 = smf.mixedlm("AAI ~ 1", d, groups=d["sid"]).fit(reml=True)
R["icc_AAI"] = float(m0.cov_re.iloc[0, 0] / (m0.cov_re.iloc[0, 0] + m0.scale))

# AI-assigned rubric score vs student response (self-serving bias check)
sb = d.dropna(subset=["ai_score"])
R["ai_score"] = dict(n=int(len(sb)), formats=sb.format.value_counts().to_dict(),
                     rho_ACE=stats.spearmanr(sb.ai_score, sb.ACCEPTANCE)[0], p_ACE=stats.spearmanr(sb.ai_score, sb.ACCEPTANCE)[1],
                     rho_FAI=stats.spearmanr(sb.ai_score, sb.FAIRNESS)[0], p_FAI=stats.spearmanr(sb.ai_score, sb.FAIRNESS)[1],
                     rho_REJ=stats.spearmanr(sb.ai_score, sb.REJECTION)[0], p_REJ=stats.spearmanr(sb.ai_score, sb.REJECTION)[1],
                     rho_AAI=stats.spearmanr(sb.ai_score, sb.AAI)[0], p_AAI=stats.spearmanr(sb.ai_score, sb.AAI)[1])

# ---------------------------------------------------------------- RQ2 format comparison
def friedman_block(df, col, by="format", levels=FORMATS):
    w = df.pivot_table(index="sid", columns=by, values=col, aggfunc="mean")[levels].dropna()
    chi, p = stats.friedmanchisquare(*[w[l] for l in levels]); n, k = w.shape
    return dict(chi2=chi, p=p, n=n, W=chi / (n * (k - 1))), w


_bf = d.groupby("format")[["AAI"] + list(CONSTRUCTS) + ITEMS + ["fb_len", "ans_len"]].agg(["mean", "std"])
rq2 = {"by_format": {f"{a}|{b}": v for (a, b), v in _bf.to_dict().items()}}
fr_rows = []
for k in ["AAI"] + list(CONSTRUCTS) + ITEMS:
    f, _ = friedman_block(d, k); f["var"] = k; fr_rows.append(f)
fr = pd.DataFrame(fr_rows)
fr["p_holm"] = np.nan
fr.loc[fr["var"].isin(CONSTRUCTS), "p_holm"] = holm(fr.loc[fr["var"].isin(CONSTRUCTS), "p"])
fr.loc[fr["var"].isin(ITEMS), "p_holm"] = holm(fr.loc[fr["var"].isin(ITEMS), "p"])
rq2["friedman"] = fr.to_dict("records")
_, wide = friedman_block(d, "AAI")
pairs = []
for i in range(4):
    for j in range(i + 1, 4):
        a, b = FORMATS[i], FORMATS[j]; diff = wide[a] - wide[b]
        p, rrb, n = wilcoxon_vs(diff + 3, 3)
        pairs.append(dict(a=a, b=b, md=diff.mean(), p=p, rrb=rrb))
        t = stats.t.ppf(0.95, len(diff) - 1); se = diff.std(ddof=1) / np.sqrt(len(diff))
        pairs[-1].update(ci90_lo=diff.mean() - t * se, ci90_hi=diff.mean() + t * se,
                         equivalent=bool(abs(diff.mean()) + t * se < 0.25))
pairs = pd.DataFrame(pairs); pairs["p_holm"] = holm(pairs.p); rq2["pairwise_AAI"] = pairs.to_dict("records")
# LMM with likelihood-ratio test
dd = d.copy(); dd["format"] = pd.Categorical(dd["format"], FORMATS)
full = smf.mixedlm("AAI ~ C(format, Treatment('Sandwich'))", dd, groups=dd["sid"]).fit(reml=False)
null = smf.mixedlm("AAI ~ 1", dd, groups=dd["sid"]).fit(reml=False)
lr = 2 * (full.llf - null.llf)
rq2["lmm"] = dict(lr=lr, df=3, p=stats.chi2.sf(lr, 3),
                  coefs={k: dict(b=full.params[k], se=full.bse[k], p=full.pvalues[k]) for k in full.params.index if "format" in k})
# covariate model: feedback length and answer length
dd["fb_len_z"] = (dd.fb_len - dd.fb_len.mean()) / dd.fb_len.std()
dd["ans_len_z"] = (np.log1p(dd.ans_len) - np.log1p(dd.ans_len).mean()) / np.log1p(dd.ans_len).std()
cov = smf.mixedlm("AAI ~ C(format, Treatment('Sandwich')) + fb_len_z + ans_len_z", dd, groups=dd["sid"]).fit(reml=False)
rq2["lmm_cov"] = {k: dict(b=cov.params[k], se=cov.bse[k], p=cov.pvalues[k]) for k in cov.params.index if k != "Group Var"}
rq2["fb_len_friedman"] = friedman_block(d, "fb_len")[0]
# sensitivity: drop straight-lined responses
ds = d[~d.straight]
f_s, _ = friedman_block(ds, "AAI"); rq2["sensitivity_no_straight"] = f_s
rq2["sensitivity_n_rows"] = int(len(ds)); rq2["sensitivity_means"] = ds.groupby("format")["AAI"].mean().to_dict()
sub_icc = smf.mixedlm("AAI ~ 1", ds, groups=ds["sid"]).fit(reml=True)
rq2["icc_nostraight"] = float(sub_icc.cov_re.iloc[0, 0] / (sub_icc.cov_re.iloc[0, 0] + sub_icc.scale))
rej = friedman_block(d, "REJECTION")[0]; rq2["friedman_REJ"] = rej
R["rq2"] = rq2

# ---------------------------------------------------------------- RQ3 (needs context labels)
if "context_type" in d.columns or (CTX and CTX.exists()):
    if "context_type" not in d.columns:
        c = pd.read_csv(CTX); c.columns = [x.strip().lower() for x in c.columns]
        d = d.merge(c.rename(columns={"question_id": "qid"}), on="qid", how="left")
    d3 = d.dropna(subset=["context_type"])
    rq3 = {"counts": d3.context_type.value_counts().to_dict()}
    m3 = smf.mixedlm("AAI ~ C(context_type) + C(format)", d3, groups=d3["sid"]).fit(reml=False)
    rq3["lmm"] = {k: dict(b=m3.params[k], se=m3.bse[k], p=m3.pvalues[k]) for k in m3.params.index if "context" in k}
    rq3["means"] = d3.groupby("context_type")[["AAI"] + list(CONSTRUCTS)].mean().to_dict()
    rq3["mwu_rows"] = {}
    for k in ["AAI"] + list(CONSTRUCTS):
        g = [d3.loc[d3.context_type == t, k] for t in ("Raw", "Graph")]
        u, p = stats.mannwhitneyu(*g); rq3["mwu_rows"][k] = dict(U=u, p=p)
    ci3 = m3.conf_int().loc[[k for k in m3.params.index if "context" in k]]
    rq3["lmm_ci"] = ci3.values.tolist()
    both = d3.groupby("sid")["context_type"].nunique(); bs = both[both == 2].index
    rq3["students_both"] = int(len(bs)); rq3["students_raw_any"] = int(d3.loc[d3.context_type == "Raw", "sid"].nunique())
    rq3["questions"] = d3.groupby("context_type")["qid"].nunique().to_dict()
    rq3["repos"] = d3.groupby("context_type")["repo"].nunique().to_dict()
    rq3["both_students_mean_AAI"] = float(d3[d3.sid.isin(bs)].AAI.mean())
    rq3["other_students_mean_AAI"] = float(d3[~d3.sid.isin(bs)].AAI.mean())
    rq3["within_both_means"] = d3[d3.sid.isin(bs)].groupby("context_type")["AAI"].mean().to_dict()
    rq3["mwu_items"] = {}
    for k in ITEMS:
        g = [d3.loc[d3.context_type == t, k] for t in ("Raw", "Graph")]
        u, p = stats.mannwhitneyu(*g); rq3["mwu_items"][k] = dict(U=u, p=p, raw=g[0].mean(), graph=g[1].mean())
    R["rq3"] = rq3
else:
    R["rq3"] = "not available: question context labels (Raw/Graph) are not in the export"

# ---------------------------------------------------------------- free-text replies
rep = d[d.reply.astype(str).str.strip().ne("—") & d.reply.notna()][["format", "reply", "ACCEPTANCE", "REJECTION"]]
R["replies"] = rep.to_dict("records")

with open(OUT / "results.json", "w") as f:
    json.dump(R, f, indent=1, ensure_ascii=False, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))

# ---------------------------------------------------------------- LaTeX tables
def fp(p):
    return "$<$.001" if p < .001 else f"{p:.3f}".lstrip("0") if p < .995 else "1.000"


with open(TAB / "rq1_items.tex", "w") as f:
    for _, r in rq1.iterrows():
        name = r["item"].title().replace("Behavioral Intention", "Behav.\\ intention").replace("Psychological Safety", "Psych.\\ safety").replace("Competence Trust", "Competence trust")
        if r["item"] == "REJECTION": name += "$^\\dagger$"
        f.write(f"{name} & {r['mean']:.2f} ({r['sd']:.2f}) & [{r['lo']:.2f}, {r['hi']:.2f}] & {r['agree']:.1f} & {r['disagree']:.1f} & {r['rrb']:.2f} & {fp(r['p_holm'])} \\\\\n")
with open(TAB / "rq2_formats.tex", "w") as f:
    for k in ["AAI"] + list(CONSTRUCTS):
        g = d.groupby("format")[k]; mu, sd = g.mean(), g.std()
        fr_k = fr[fr["var"] == k].iloc[0]
        lab = "Agreement index (AAI)" if k == "AAI" else k
        cells = " & ".join(f"{mu[x]:.2f} ({sd[x]:.2f})" for x in FORMATS)
        ph = fp(fr_k.p) if k == "AAI" else fp(fr_k.p_holm)
        f.write(f"{lab} & {cells} & {fr_k.chi2:.2f} & {ph} & {fr_k.W:.3f} \\\\\n")
        if k == "AAI": f.write("\\midrule\n")

# ---------------------------------------------------------------- figures
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
                     "font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6,
                     "xtick.major.width": 0.6, "ytick.major.width": 0.6, "pdf.fonttype": 42})
INK, MUTED = "#2b2b29", "#6b6a64"
LIK = ["#b2342c", "#e8a093", "#d9d8d3", "#86b6ef", "#1c5cab"]  # diverging red-gray-blue
# Fig: diverging stacked bars
order = rq1.sort_values("agree").reset_index(drop=True)
fig, ax = plt.subplots(figsize=(4.8, 3.4))
y = np.arange(len(order))
for i, r in order.iterrows():
    left = -(r.p1 + r.p2 + r.p3 / 2)
    for k, w in enumerate([r.p1, r.p2, r.p3, r.p4, r.p5]):
        ax.barh(i, w, left=left, color=LIK[k], height=0.62, edgecolor="white", linewidth=0.8)
        left += w
    ax.text(102, i, f"{r.agree:.0f}%", va="center", ha="right", fontsize=7, color=INK)
lab = [s.title() + ("$^\\dagger$" if s == "REJECTION" else "") for s in order["item"]]
ax.set_yticks(y, lab, fontsize=7)
ax.axvline(0, color=MUTED, lw=0.6)
ax.set_xlim(-60, 104); ax.set_xticks([-50, -25, 0, 25, 50, 75], ["50", "25", "0", "25", "50", "75"])
ax.set_xlabel("Share of ratings (%)  —  left: disagree, right: agree", color=INK)
ax.tick_params(axis="y", length=0)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(LIK, ["1 Strongly disagree", "2", "3 Neutral", "4", "5 Strongly agree"])],
          ncol=5, fontsize=6, frameon=False, loc="lower center", bbox_to_anchor=(0.42, 1.0), handlelength=1.2, columnspacing=0.8)
ax.text(103, len(order) - 0.2, "agree", ha="right", fontsize=6, color=MUTED)
fig.tight_layout(); fig.savefig(FIG / "likert_items.pdf", bbox_inches="tight"); plt.close(fig)

# Fig: per-format construct means with cluster-bootstrap CI (dot plot, marker shape + label encode format)
CAT = ["#2a78d6", "#eb6834", "#1e9e73", "#7a4fd1"]; MK = ["o", "s", "D", "^"]
keys = ["AAI"] + list(CONSTRUCTS)
fig, ax = plt.subplots(figsize=(4.8, 2.8))
for fi, fm in enumerate(FORMATS):
    sub = d[d.format == fm]
    for ki, k in enumerate(keys):
        lo, hi = cluster_boot_mean(sub, k); m_ = sub[k].mean(); yy = ki + (fi - 1.5) * 0.17
        ax.plot([lo, hi], [yy, yy], color=CAT[fi], lw=1.4, solid_capstyle="butt")
        ax.plot(m_, yy, MK[fi], color=CAT[fi], ms=6, mec="white", mew=0.7, label=fm if ki == 0 else None)
ax.set_yticks(range(len(keys)), ["Agreement index"] + [k.replace("\\&", "&") for k in CONSTRUCTS])
ax.invert_yaxis(); ax.axvline(3, color=MUTED, lw=0.6, ls=":")
ax.set_xlabel("Mean rating (1–5) with 95% cluster-bootstrap CI", color=INK); ax.set_xlim(2.95, 4.6)
ax.tick_params(axis="y", length=0)
ax.legend(ncol=4, fontsize=6.5, frameon=False, loc="lower center", bbox_to_anchor=(0.4, 1.0), handletextpad=0.3)
fig.tight_layout(); fig.savefig(FIG / "format_constructs.pdf", bbox_inches="tight"); plt.close(fig)

# Fig: Spearman correlation heatmap (sequential single hue on |rho|, values printed)
cm = d[ITEMS].corr(method="spearman")
fig, ax = plt.subplots(figsize=(4.2, 3.7))
im = ax.imshow(cm.values, cmap="Blues", vmin=0, vmax=1)
ax.set_xticks(range(15), [SHORT[i] for i in ITEMS], rotation=90, fontsize=6.5)
ax.set_yticks(range(15), [SHORT[i] for i in ITEMS], fontsize=6.5)
for i in range(15):
    for j in range(15):
        v = cm.values[i, j]
        ax.text(j, i, f"{v:.2f}".replace("0.", ".").replace("1.00", "1"), ha="center", va="center", fontsize=4.6,
                color="white" if abs(v) > 0.65 else INK)
cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02); cb.ax.tick_params(labelsize=6); cb.set_label("Spearman ρ", fontsize=7)
for s in ax.spines.values(): s.set_visible(False)
fig.tight_layout(); fig.savefig(FIG / "item_correlations.pdf", bbox_inches="tight"); plt.close(fig)
print(json.dumps(R["screening"], indent=1, ensure_ascii=False))
