# Reference and claim audit

Checked 29 October 2026. This audit distinguishes bibliographic identity from
support for the manuscript's claims. Resolving a DOI is not a full-text review.

## Bibliographic evidence

`reference_metadata_audit.json` records exact-DOI responses from Crossref for 33
of the 36 references. All 33 resolved successfully. `verify_references.py` uses
exact DOI lookup only: title-search candidates are not accepted as matches.
Online-first dates and volume publication dates can differ; the bibliography
uses the cited volume's year. In particular, Winstone (2017), Parkes (2013),
Kim (2019), Er (2025), and Keuning (2019) predate their issue years online.
Keuning's DOI metadata records online publication in September 2018 and print
publication in March 2019. Cameron's registered page range is 317–372, even
though the author's publications page lists 317–373.

Corrections made:

- Zhang: Price precedes Matsuda, following the [AAAI publisher record](https://ojs.aaai.org/index.php/AAAI/article/view/30372).
  Added pages 23250–23258. The record is volume 38, issue 21; the LNCS BibTeX
  proceedings style does not support both volume and issue, so the citation
  retains volume and pages while the audit retains issue 21.
- Nazaretsky: added [chapter DOI](https://link.springer.com/chapter/10.1007/978-3-031-72315-5_20).
- CodeHelp: added pages 1–11 from the DOI record.
- Du: added pages 11733–11763 from the [official PMLR proceedings](https://proceedings.mlr.press/v235/du24e.html).
- Zheng: completed volume 36 and pages 46595–46623, cross-checked with the
  [official NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html).
- Added Keuning, Jeuring and Heeren, DOI 10.1145/3231711, for the pre-LLM
  automated-feedback baseline; and Cameron and Miller, DOI
  10.3368/jhr.50.2.317, for dependence and the limitations of few-cluster inference.

Three records are checked manually rather than by DOI:

| Reference | Evidence | Scope |
|---|---|---|
| Du et al. (2024) | [PMLR publisher record](https://proceedings.mlr.press/v235/du24e.html) | Author order, title, volume, year and pages; multi-round debate differs from PACE's sequential pipeline. |
| Zheng et al. (2023) | [NeurIPS publisher record](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html) | Author order, title and proceedings identity; judge agreement does not validate classroom correctness. |
| Holm (1979) | [Facsimile of the original article](https://www.ime.usp.br/~abe/lista/pdf4R8xPVzCnX.pdf) | Scandinavian Journal of Statistics 6(2), 65–70; sequentially rejective multiple-test procedure. |

An initial exploratory registry title search returned unrelated candidates for
Du and Holm. They were rejected; no candidate DOI was added. Two initially
rate-limited DOI requests succeeded on the final exact-DOI pass. The checked-in
JSON contains the final successful responses, not the failed discovery output.

## Claim-to-source checks

- Zhang's publisher abstract supports preference for prompts containing student
  code, attributed to specificity, clarity and corrective feedback. This is not
  evidence about the correctness of PACE's feedback.
- Nazaretsky's Springer abstract supports changes in perception after provenance
  disclosure; PACE has no corresponding human-feedback comparator.
- Er's [original article](https://edepot.wur.nl/684724) concerns a Java programming
  setting and instructor-versus-AI feedback. The manuscript confines the citation
  to that setting rather than claiming universal instructor superiority.
- Escalante's [publisher abstract](https://link.springer.com/article/10.1186/s41239-023-00425-2)
  concerns ENL writing, not programming. The introduction now states that its
  participants split preferences between tutor and AI feedback, without using it
  to support a programming-specific clarity claim.
- Keuning's [original article in the authors' repository](https://research.ou.nl/ws/files/41611996/A_Systematic_Literature_Review_of_Automated_Feedback_Generation_for_Programming_Exercises.pdf)
  reviews 101 tools and reports less emphasis on fixing problems or next steps.
- Du supports multi-round debate on benchmark tasks. The paper explicitly
  distinguishes this from the sequential inspector–synthesiser design.
- Zheng supports both human-preference agreement and known judge biases. Neither
  agreement nor a displayed consensus field establishes technical correctness.
- Cameron and Miller support accounting for within-cluster dependence and caution
  with few clusters. They do not certify that percentile-bootstrap coverage is
  exact with 28 repositories; this limitation remains explicit.
- Lakens motivates equivalence assessment, but supplies no substantive justification
  for PACE's ±0.25 margin. That margin remains exploratory and uncalibrated.
- Internal consistency, technology acceptance, trust and reverse-wording sources
  motivate measurement choices, not validation of this newly written instrument.

## Conference requirements (separate from scientific claims)

The [official ICCIES 2027 submission page](https://iccies.tdtu.edu.vn/2027/how-to-submit/)
requires English, LNCS/LNAI style, and 12–15 pages. It also explicitly prohibits
AI-generated text; the following explanatory paragraph still says ICCIES 2026.
The authors must clarify the applicable policy before submission. This branch
is a review artifact, not a certification of submission compliance or ethics.

## Addition in the 30 October revision

Added `lehtinen2024askai` (37 references in the revised bibliography). Checked the
[authors' arXiv record](https://arxiv.org/abs/2404.11734): title, author order,
2024 date, arXiv identifier and DataCite DOI 10.48550/arXiv.2404.11734. The abstract
supports the narrow comparison of LLM responses to QLCs on model-generated
programs and warns about tracing errors. This was an abstract-level check, not
a new full-text systematic literature review. The earlier 33-DOI Crossref audit
remains historical; it does not cover this DataCite DOI. The current
`verify_references.py` uses Crossref and should not be interpreted as a successful
DataCite resolver for this added record.
