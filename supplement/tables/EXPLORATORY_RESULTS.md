# S3. Exploratory item contrasts and context models

Family: 15 items × six configuration pairs = 90 two-sided contrasts. Differences are first minus second. Unadjusted intervals use the new common draws (seed 20261030); simultaneous bands use the bootstrap-standardised maximum across all 90. Approximate sensitivity analysis, not preregistered confirmation.

## Direct agreement outcome for RQ3

| Outcome | Raw-code coefficient | Repository CI95% | Valid fits |
|---|---:|---|---:|
| ACCEPTANCE | 0.034372 | [-0.179854, 0.257205] | 5000 |
| AAI | 0.072349 | [-0.024834, 0.187393] | 5000 |

## All six Actionability contrasts

| Contrast | Difference | Unadjusted CI95% | Simultaneous 95% band, family of 90 |
|---|---:|---|---|
| Sandwich − Rubric | 0.360465 | [0.154739, 0.554378] | [0.007965, 0.712965] |
| Sandwich − Explainable | 0.372093 | [0.166667, 0.569771] | [0.019283, 0.724903] |
| Sandwich − Researching | 0.046512 | [-0.088636, 0.172855] | [-0.179852, 0.272875] |
| Rubric − Explainable | 0.011628 | [-0.130448, 0.160494] | [-0.244161, 0.267417] |
| Rubric − Researching | -0.313953 | [-0.516854, -0.109756] | [-0.670646, 0.042739] |
| Explainable − Researching | -0.325581 | [-0.521739, -0.122443] | [-0.673520, 0.022357] |

## Full comparison family

| Item | Contrast | Difference | Unadjusted CI95% | Simultaneous 95% band |
|---|---|---:|---|---|
| ACCURACY | Sandwich − Rubric | 0.127907 | [-0.091954, 0.358989] | [-0.262869, 0.518683] |
| ACCURACY | Sandwich − Explainable | 0.046512 | [-0.144777, 0.226190] | [-0.278211, 0.371235] |
| ACCURACY | Sandwich − Researching | 0.162791 | [-0.063161, 0.398010] | [-0.235573, 0.561155] |
| ACCURACY | Rubric − Explainable | -0.081395 | [-0.226667, 0.046525] | [-0.318554, 0.155764] |
| ACCURACY | Rubric − Researching | 0.034884 | [-0.207342, 0.271608] | [-0.384478, 0.454246] |
| ACCURACY | Explainable − Researching | 0.116279 | [-0.090962, 0.337504] | [-0.261505, 0.494063] |
| SPECIFICITY | Sandwich − Rubric | -0.069767 | [-0.239130, 0.093023] | [-0.356192, 0.216657] |
| SPECIFICITY | Sandwich − Explainable | -0.023256 | [-0.149425, 0.088889] | [-0.227525, 0.181013] |
| SPECIFICITY | Sandwich − Researching | 0.000000 | [-0.139241, 0.136364] | [-0.240540, 0.240540] |
| SPECIFICITY | Rubric − Explainable | 0.046512 | [-0.088608, 0.180875] | [-0.185146, 0.278169] |
| SPECIFICITY | Rubric − Researching | 0.069767 | [-0.044957, 0.193191] | [-0.136016, 0.275550] |
| SPECIFICITY | Explainable − Researching | 0.023256 | [-0.095745, 0.151181] | [-0.195820, 0.242332] |
| CLARITY | Sandwich − Rubric | 0.023256 | [-0.153846, 0.194805] | [-0.279599, 0.326110] |
| CLARITY | Sandwich − Explainable | -0.023256 | [-0.195409, 0.144448] | [-0.319791, 0.273280] |
| CLARITY | Sandwich − Researching | 0.197674 | [0.025301, 0.350515] | [-0.087335, 0.482684] |
| CLARITY | Rubric − Explainable | -0.046512 | [-0.194813, 0.096386] | [-0.298580, 0.205557] |
| CLARITY | Rubric − Researching | 0.174419 | [-0.012195, 0.361702] | [-0.150427, 0.499264] |
| CLARITY | Explainable − Researching | 0.220930 | [0.051282, 0.372340] | [-0.062916, 0.504776] |
| TRANSPARENCY | Sandwich − Rubric | 0.023256 | [-0.222252, 0.272727] | [-0.408930, 0.455441] |
| TRANSPARENCY | Sandwich − Explainable | -0.116279 | [-0.287360, 0.034483] | [-0.397894, 0.165336] |
| TRANSPARENCY | Sandwich − Researching | -0.034884 | [-0.209302, 0.139541] | [-0.335209, 0.265441] |
| TRANSPARENCY | Rubric − Explainable | -0.139535 | [-0.360490, 0.074084] | [-0.518172, 0.239102] |
| TRANSPARENCY | Rubric − Researching | -0.058140 | [-0.214286, 0.096386] | [-0.328345, 0.212066] |
| TRANSPARENCY | Explainable − Researching | 0.081395 | [-0.082496, 0.259768] | [-0.216754, 0.379544] |
| USEFULNESS | Sandwich − Rubric | 0.174419 | [-0.036145, 0.369061] | [-0.174803, 0.523640] |
| USEFULNESS | Sandwich − Explainable | 0.279070 | [0.092101, 0.441860] | [-0.027063, 0.585202] |
| USEFULNESS | Sandwich − Researching | 0.058140 | [-0.170461, 0.284091] | [-0.339808, 0.456087] |
| USEFULNESS | Rubric − Explainable | 0.104651 | [-0.044470, 0.250000] | [-0.149957, 0.359259] |
| USEFULNESS | Rubric − Researching | -0.116279 | [-0.321439, 0.080460] | [-0.465467, 0.232909] |
| USEFULNESS | Explainable − Researching | -0.220930 | [-0.369048, -0.060976] | [-0.490416, 0.048555] |
| ACTIONABILITY | Sandwich − Rubric | 0.360465 | [0.154739, 0.554378] | [0.007965, 0.712965] |
| ACTIONABILITY | Sandwich − Explainable | 0.372093 | [0.166667, 0.569771] | [0.019283, 0.724903] |
| ACTIONABILITY | Sandwich − Researching | 0.046512 | [-0.088636, 0.172855] | [-0.179852, 0.272875] |
| ACTIONABILITY | Rubric − Explainable | 0.011628 | [-0.130448, 0.160494] | [-0.244161, 0.267417] |
| ACTIONABILITY | Rubric − Researching | -0.313953 | [-0.516854, -0.109756] | [-0.670646, 0.042739] |
| ACTIONABILITY | Explainable − Researching | -0.325581 | [-0.521739, -0.122443] | [-0.673520, 0.022357] |
| COMPETENCE TRUST | Sandwich − Rubric | 0.325581 | [0.132530, 0.511117] | [-0.000466, 0.651629] |
| COMPETENCE TRUST | Sandwich − Explainable | 0.104651 | [-0.100032, 0.280488] | [-0.221383, 0.430685] |
| COMPETENCE TRUST | Sandwich − Researching | 0.034884 | [-0.187500, 0.221082] | [-0.325729, 0.395496] |
| COMPETENCE TRUST | Rubric − Explainable | -0.220930 | [-0.390244, -0.064506] | [-0.506160, 0.064299] |
| COMPETENCE TRUST | Rubric − Researching | -0.290698 | [-0.475624, -0.109756] | [-0.612036, 0.030641] |
| COMPETENCE TRUST | Explainable − Researching | -0.069767 | [-0.230789, 0.100000] | [-0.352930, 0.213395] |
| RELIABILITY | Sandwich − Rubric | 0.000000 | [-0.154762, 0.156259] | [-0.266469, 0.266469] |
| RELIABILITY | Sandwich − Explainable | -0.127907 | [-0.259740, -0.013154] | [-0.341796, 0.085982] |
| RELIABILITY | Sandwich − Researching | -0.081395 | [-0.256429, 0.082353] | [-0.376521, 0.213730] |
| RELIABILITY | Rubric − Explainable | -0.127907 | [-0.273814, 0.000000] | [-0.365647, 0.109833] |
| RELIABILITY | Rubric − Researching | -0.081395 | [-0.258824, 0.078974] | [-0.373405, 0.210614] |
| RELIABILITY | Explainable − Researching | 0.046512 | [-0.086420, 0.177229] | [-0.184273, 0.277296] |
| FAIRNESS | Sandwich − Rubric | 0.302326 | [0.114277, 0.467391] | [-0.002001, 0.606652] |
| FAIRNESS | Sandwich − Explainable | 0.058140 | [-0.149469, 0.244193] | [-0.287199, 0.403478] |
| FAIRNESS | Sandwich − Researching | 0.069767 | [-0.075974, 0.204545] | [-0.172746, 0.312281] |
| FAIRNESS | Rubric − Explainable | -0.244186 | [-0.397727, -0.087912] | [-0.514807, 0.026435] |
| FAIRNESS | Rubric − Researching | -0.232558 | [-0.355571, -0.105248] | [-0.450976, -0.014140] |
| FAIRNESS | Explainable − Researching | 0.011628 | [-0.159103, 0.179114] | [-0.283186, 0.306442] |
| AFFECT | Sandwich − Rubric | 0.220930 | [0.036574, 0.397594] | [-0.094590, 0.536451] |
| AFFECT | Sandwich − Explainable | 0.279070 | [0.053333, 0.493834] | [-0.101504, 0.659643] |
| AFFECT | Sandwich − Researching | 0.116279 | [-0.064527, 0.263158] | [-0.173107, 0.405665] |
| AFFECT | Rubric − Explainable | 0.058140 | [-0.119061, 0.236559] | [-0.251945, 0.368224] |
| AFFECT | Rubric − Researching | -0.104651 | [-0.222222, 0.000000] | [-0.294493, 0.085191] |
| AFFECT | Explainable − Researching | -0.162791 | [-0.329268, -0.022989] | [-0.430588, 0.105007] |
| PSYCHOLOGICAL SAFETY | Sandwich − Rubric | -0.034884 | [-0.206907, 0.150013] | [-0.349137, 0.279369] |
| PSYCHOLOGICAL SAFETY | Sandwich − Explainable | -0.058140 | [-0.202247, 0.081395] | [-0.304752, 0.188473] |
| PSYCHOLOGICAL SAFETY | Sandwich − Researching | -0.069767 | [-0.238109, 0.096386] | [-0.363971, 0.224436] |
| PSYCHOLOGICAL SAFETY | Rubric − Explainable | -0.023256 | [-0.180726, 0.120492] | [-0.283405, 0.236893] |
| PSYCHOLOGICAL SAFETY | Rubric − Researching | -0.034884 | [-0.160951, 0.106667] | [-0.267446, 0.197678] |
| PSYCHOLOGICAL SAFETY | Explainable − Researching | -0.011628 | [-0.132530, 0.119048] | [-0.233993, 0.210737] |
| ACCEPTANCE | Sandwich − Rubric | 0.046512 | [-0.116313, 0.184783] | [-0.216676, 0.309699] |
| ACCEPTANCE | Sandwich − Explainable | -0.011628 | [-0.162797, 0.120492] | [-0.259271, 0.236015] |
| ACCEPTANCE | Sandwich − Researching | -0.023256 | [-0.200000, 0.141176] | [-0.315766, 0.269254] |
| ACCEPTANCE | Rubric − Explainable | -0.058140 | [-0.200000, 0.088608] | [-0.309702, 0.193423] |
| ACCEPTANCE | Rubric − Researching | -0.069767 | [-0.276336, 0.142857] | [-0.426259, 0.286724] |
| ACCEPTANCE | Explainable − Researching | -0.011628 | [-0.182927, 0.161312] | [-0.309435, 0.286179] |
| REJECTION | Sandwich − Rubric | 0.081395 | [-0.132530, 0.308647] | [-0.303544, 0.466334] |
| REJECTION | Sandwich − Explainable | -0.023256 | [-0.211268, 0.168421] | [-0.350576, 0.304064] |
| REJECTION | Sandwich − Researching | -0.046512 | [-0.170455, 0.089744] | [-0.268803, 0.175780] |
| REJECTION | Rubric − Explainable | -0.104651 | [-0.317073, 0.086980] | [-0.456653, 0.247350] |
| REJECTION | Rubric − Researching | -0.127907 | [-0.317647, 0.037742] | [-0.441980, 0.186166] |
| REJECTION | Explainable − Researching | -0.023256 | [-0.178947, 0.134163] | [-0.294251, 0.247739] |
| WILLINGNESS | Sandwich − Rubric | -0.046512 | [-0.207317, 0.113636] | [-0.325528, 0.232504] |
| WILLINGNESS | Sandwich − Explainable | -0.081395 | [-0.194805, 0.011494] | [-0.265515, 0.102725] |
| WILLINGNESS | Sandwich − Researching | -0.011628 | [-0.207317, 0.168539] | [-0.336844, 0.313588] |
| WILLINGNESS | Rubric − Explainable | -0.034884 | [-0.186830, 0.107527] | [-0.291647, 0.221879] |
| WILLINGNESS | Rubric − Researching | 0.034884 | [-0.102273, 0.170461] | [-0.201608, 0.271376] |
| WILLINGNESS | Explainable − Researching | 0.069767 | [-0.108434, 0.241389] | [-0.231817, 0.371352] |
| BEHAVIORAL INTENTION | Sandwich − Rubric | 0.139535 | [-0.031587, 0.317660] | [-0.166456, 0.445525] |
| BEHAVIORAL INTENTION | Sandwich − Explainable | 0.081395 | [-0.057488, 0.238109] | [-0.176798, 0.339589] |
| BEHAVIORAL INTENTION | Sandwich − Researching | -0.058140 | [-0.181818, 0.068977] | [-0.279878, 0.163599] |
| BEHAVIORAL INTENTION | Rubric − Explainable | -0.058140 | [-0.216867, 0.105276] | [-0.339583, 0.223304] |
| BEHAVIORAL INTENTION | Rubric − Researching | -0.197674 | [-0.345238, -0.034884] | [-0.468866, 0.073517] |
| BEHAVIORAL INTENTION | Explainable − Researching | -0.139535 | [-0.285714, 0.012500] | [-0.400076, 0.121007] |
