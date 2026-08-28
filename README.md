# PLGA-EE-Generalization


**Evaluating Encapsulation-Efficiency Prediction for *Unseen* Small-Molecule Drugs in PLGA Nanoparticle Drug-Delivery Systems Using Machine Learning**

This undergraduate biotechnology research project evaluates whether encapsulation efficiency in PLGA nanoparticle formulations can be predicted reliably for small-molecule drugs excluded from model training.

> **Research question:** How accurately can machine-learning models predict encapsulation efficiency (EE%) in PLGA nanoparticle formulations for small-molecule drugs excluded from model training?

The scientific focus is **unseen-drug generalization**rather than simply determining whether machine-learning models can predict encapsulation efficiency. The sole prediction target is **EE%**. Particle size, loading capacity, drug release, toxicity, efficacy, biodistribution, and clinical response are outside the scope of this study as prediction targets.

## Technical Stack

- **Programming language:** Python
- **Analysis environment:** Jupyter Notebook
- **Data processing:** pandas, NumPy
- **Machine learning:** scikit-learn, XGBoost
- **Model interpretation:** SHAP
- **Visualization:** Matplotlib
- **Validation strategy:** drug-grouped cross-validation

## Dataset

Goren A, Bao Z, Martinez Lozano JP, Allen C. *A formulation dataset of poly(lactide-co-glycolide) nanoparticles for small molecule delivery.* *Scientific Data*. 2025;12:1182. Article DOI: `10.1038/s41597-025-05520-9` · Dataset DOI: `10.17632/sbjf5csrdm.1` · License: **CC BY 4.0**.

Full dataset provenance and SHA256 integrity records are provided in [`data/README.md`](https://github.com/Ali-Sheroz/PLGA-EE-Generalization/blob/main/data/README.md). The original raw files were retained unchanged throughout the analysis.

## Project status

- **Phase 1 — Data feasibility audit: complete.** No modeling was performed. Final assessment: **FEASIBLE WITH MODIFICATIONS**.
- **Phase 2 — Data preprocessing: complete.** All five issues identified during the feasibility audit were resolved, producing `data/processed/ML_ready_PLGA.csv` (430 × 31).
- **Phase 3 — Exploratory data analysis: complete.** Descriptive analysis produced three 300-DPI figures and supporting tables. No predictive model was trained at this stage.
- **Phase 4 — Model training and unseen-drug validation: complete.** Four regression pipelines and a mean-prediction reference were evaluated using `GroupKFold(5)` with `drug_group` as the grouping variable. **Primary finding:** no candidate model consistently outperformed the mean-prediction reference for unseen drugs.
- **Phase 5 — Explainability and error analysis: complete.** SHAP analysis of the fitted Random Forest and per-drug out-of-fold error analysis were used to examine model behavior and patterns of generalization failure. Predictions showed substantial shrinkage toward the dataset mean, with a regression slope of predicted versus measured EE of **0.156**.

- ## Repository layout

```text
data/
  raw/              # 5 official CSV files retained unchanged
                    # see data/README.md for provenance and integrity records

  processed/        # derived and documented working datasets
                    # ML_ready_PLGA.csv
                    # PLGA_clean_unscaled.csv
                    # scaler_params.csv
                    # preprocessing_pipeline.joblib
                    # feature_manifest.csv
                    # preprocessing_meta.json
                    # master_audit_view.csv

notebooks/
  01_data_audit.ipynb
                    # Phase 1: data feasibility audit

  02_preprocessing.ipynb
                    # Phase 2: preprocessing and flag resolution

  03_exploratory_analysis.ipynb
                    # Phase 3: exploratory data analysis

  04_model_training.ipynb
                    # Phase 4: grouped validation and robustness analysis

  05_explainability_and_errors.ipynb
                    # Phase 5: SHAP and per-drug error analysis

results/
  figures/          # analysis and modelling figures (300 DPI)

  tables/           # machine-readable audit, preprocessing,
                    # EDA, modelling, and error-analysis tables

  audit/            # source manifest and feasibility report

src/
  preprocessing.py   # reusable preprocessing utilities
  validation.py      # drug-grouped validation and leakage checks
  model_training.py  # regression model definitions
  explainability.py  # SHAP/model-attribution utilities

  models/            # saved model artifact and metadata
```

## Phase 1 deliverables

- **Feasibility report:** [`results/audit/feasibility_report.md`](https://github.com/Ali-Sheroz/PLGA-EE-Generalization/blob/main/results/audit/feasibility_report.md) — summarizes the feasibility assessment and overall classification.
- **Integrity manifest:** [`results/audit/source_manifest.csv`](https://github.com/Ali-Sheroz/PLGA-EE-Generalization/blob/main/results/audit/source_manifest.csv) — records source provenance and file-integrity information.
- **Audit tables:** available in `results/tables/`, including the dataset file map, variable dictionary, missingness summary, formulations-per-drug table, EE summary, leakage audit, duplicate audit, and outlier flags.
- **Figures:** available in `results/figures/`, including EE distribution and boxplots, formulations-per-drug, missingness, molecular and formulation-variable distributions, the correlation matrix, EE-versus-variable plots, and EE-by-drug distributions.

## Key Findings — Phase 1

- The source files contained **433 formulations, 65 small molecules, and 59 source publications**, consistent with the reported dataset characteristics.
- **Encapsulation efficiency was complete for all formulations** and ranged from 0–100%, supporting its use as the regression target.
- **Drug representation was highly imbalanced:** the median was one formulation per drug, **33 of 65 drugs (~51%) were represented by a single formulation**, and the 10 most represented drugs accounted for approximately 66% of all formulations. This distribution supported the use of **drug-grouped validation** rather than random formulation-level splitting for the unseen-drug analysis.
- **`LC` was excluded from EE prediction because of target-leakage risk**, while **`particle_size` was excluded because it is a measured formulation outcome rather than a pre-formulation predictor**.
- **`pH` was represented as an ordinal code rather than raw pH values.** An undocumented `-2` category was identified during the audit and addressed during preprocessing.

## Phase 2 deliverables (preprocessing)

**Notebook:** [`notebooks/02_preprocessing.ipynb`](notebooks/02_preprocessing.ipynb)  
**Processed dataset:** `data/processed/ML_ready_PLGA.csv` (**430 formulations × 31 columns**)

| Phase 1 flag | Resolution | Affected |
|---|---|---:|
| Exact duplicates | Removed while retaining the first occurrence | 433 → 430 rows |
| Salt/hydrate variants | A `drug_group` key was created for grouped validation while distinct molecular descriptors were retained | 65 drugs → 63 groups |
| `EE = 0` | Retained as a valid zero-encapsulation outcome and flagged as `EE_is_zero` | 1 row |
| Undocumented `pH = -2` | Converted to missing and represented as an explicit `pH_missing` category; no imputation was applied | 26 rows |
| Leakage-prone variables | `LC` and `particle_size` were excluded from the predictor set; `EE` remained the sole target | 2 columns |

The processed dataset contains **13 continuous predictors** and **9 one-hot encoded categorical features**, giving **22 model features**. Continuous variables were standardized, while the target `EE` was left unscaled. No missing values remained in the processed modeling view.

> **Preprocessing note:** `ML_ready_PLGA.csv` was created as a finalized processed dataset using scaling fitted on the full dataset and is intended for inspection and reuse. It was **not used as the input for unseen-drug cross-validation**. Phase 4 instead used `PLGA_clean_unscaled.csv`, with scaling and encoding re-fitted inside each training fold to prevent preprocessing leakage.

## Phase 3 Deliverables — Exploratory Data Analysis

**Notebook:** [`notebooks/03_exploratory_analysis.ipynb`](notebooks/03_exploratory_analysis.ipynb)

Figures are available at **300 DPI** in `results/figures/`:

- `Fig1_correlation_heatmap_EE.png` — Pearson correlation matrix across 13 continuous descriptors, `LA/GA`, and `EE`, accompanied by a ranked descriptor–EE panel with Spearman ρ.
- `Fig2_logP_vs_EE_by_LAGA.png` — relationship between `mol_logP` and EE%, stratified by PLGA LA/GA ratio.
- `Fig3_EE_distribution.png` — distribution of EE% shown using histogram, KDE, ECDF, and box/strip representations.

Supporting tables include `eda_EE_summary.csv`, `eda_correlations_with_EE.csv`, `eda_correlation_matrix_pearson.csv`, and `eda_observations.csv`.

### EDA Observations

EE% showed a **left-skewed distribution** with a median of **70.6%**, an IQR of **52.4–83.2%**, and a skewness of **−1.00**. Thirty-two formulations had EE below 20%. No individual descriptor showed a strong association with EE. The largest observed Pearson correlations were for `surfactant_concentration` (r = +0.31), `surfactant_HLB` (r = +0.30), and `mol_logP` (r = +0.23), supporting evaluation of multivariable predictive models rather than reliance on a single formulation descriptor.

These analyses are descriptive. Correlation does not imply causation, and the reported p-values assume independent observations. Because formulations are clustered within drugs and source studies, inferential statistics from the exploratory analysis should be interpreted cautiously. Drug-grouped validation was therefore used in Phase 4 to evaluate predictive generalization to unseen drugs.

## Phase 4 deliverables (model training & unseen-drug validation)
Notebook: [`notebooks/04_model_training.ipynb`](notebooks/04_model_training.ipynb). Input is **`PLGA_clean_unscaled.csv`** (not the globally-scaled file), so `StandardScaler` sits as step 1 of every `sklearn.pipeline.Pipeline` and is re-fit inside each training fold.

**Setup.** The three near-empty copolymer grades (`LA/GA` = 1.86, 2.33, 5.67 — 5 rows across 4 drug groups) are merged into `other`; one-hot encoding then yields fixed categories `pH ∈ {-1, 0, 1, missing}` and `LA/GA ∈ {1, 3, other}`. Design matrix **430 × 20**; target `EE`; CV = `GroupKFold(n_splits=5)` on `drug_group`. Every fold asserts that neither `drug_group` **nor** the raw `small_molecule_name` appears on both sides of the split.

**Leaderboard** (`results/tables/ML_grouped_performance_metrics.csv`, ranked by mean MAE):

| # | Model | MAE (mean ± SD) | RMSE (mean ± SD) | R² (mean ± SD) |
|---|---|---|---|---|
| 1 | Random Forest | **16.70 ± 2.72** | 21.26 ± 2.69 | −0.076 ± 0.502 |
| 2 | SVR (RBF) | 18.33 ± 1.96 | 22.65 ± 2.31 | −0.196 ± 0.497 |
| — | *DummyRegressor (reference)* | *19.26 ± 4.37* | *23.59 ± 5.16* | *−0.194 ± 0.296* |
| 3 | XGBoost | 20.09 ± 4.23 | 24.66 ± 4.14 | −0.492 ± 0.884 |
| 4 | Linear Regression (baseline) | 24.72 ± 6.09 | 30.04 ± 7.95 | −1.091 ± 0.987 |

Library defaults throughout — **no hyperparameter search was performed**; only `random_state`/`n_jobs` are pinned. SVR is wrapped in `TransformedTargetRegressor(transformer=StandardScaler())` because its `C`/`epsilon` defaults are expressed in target units (EE spans 0–98.9, SD ≈ 23.5); the y-transformer is fit on training-fold `y` only. `DummyRegressor(strategy="mean")` is a **reference, not a candidate** (`is_reference_not_a_candidate=True`) and is excluded from ranking.

Best model by mean MAE (Random Forest) refit on all 430 rows → [`src/models/best_model_random_forest.joblib`](src/models) with a `.meta.json` sidecar.

> ### ⚠️ The ranking above does not replicate — read this before citing it
> Mean per-fold R² is **negative for every model**, and un-shuffled `GroupKFold` produces exactly one partition. Repeating the grouped CV over **5 shuffled partitions** and pooling **out-of-fold** predictions (a size-independent metric — unweighted per-fold means over-weight the small folds that `shuffle=True` creates) gives:
>
> | Model | pooled OOF MAE | pooled OOF R² |
> |---|---|---|
> | **DummyRegressor (mean-predictor)** | **19.14 ± 0.28** | −0.032 |
> | Random Forest | 20.71 ± 3.18 | −0.299 |
> | SVR (RBF) | 20.92 ± 1.72 | −0.210 |
> | XGBoost | 21.86 ± 4.22 | −0.438 |
> | Linear Regression | 25.72 ± 1.42 | −0.785 |
>
> **No model beats the mean-predictor on average.** Wins vs the mean-predictor across the 5 partitions: RF 2/5, XGBoost 1/5, SVR 0/5, Linear 0/5. The Random Forest "win" in the main table is specific to the single un-shuffled partition. The saved artefact is therefore *the best of four candidates on one specified split*, **not a validated unseen-drug EE predictor** — this caveat is recorded inside the joblib sidecar as `generalisation_caveat`.
>
> **Interpretation.** With 63 drug groups, ~51 % of them singletons, and 13 descriptors, the models appear to learn drug- and study-specific idiosyncrasies rather than transferable structure–encapsulation relationships. This is the substantive finding of the project: published random-split R² values are **not** evidence of unseen-drug generalisation.

Supporting tables: `laga_regrouping.csv`, `ML_cv_fold_composition.csv` (all 5 folds n_train=344 / n_test=86, test-fold mean EE 58.1–76.8 — folds are *not* exchangeable), `ML_grouped_per_fold_metrics.csv`, `ML_grouped_performance_repeated.csv`, `ML_grouped_performance_pooled_oof_repeated.csv`, `ML_grouped_pooled_oof_per_seed.csv`.

## Phase 5 deliverables (explainability & error analysis)
Notebook: [`notebooks/05_explainability_and_errors.ipynb`](notebooks/05_explainability_and_errors.ipynb). Loads the saved Random Forest pipeline and `PLGA_clean_unscaled.csv`; the feature order is asserted identical to both the `.meta.json` sidecar and the fitted pipeline's `feature_names_in_` before anything is computed.

**SHAP (`shap.TreeExplainer`, 430 × 20, base value 64.735 EE %).** Additivity verified: `base_value + Σ SHAP` reproduces `pipeline.predict(X)` to 2.2e-13. Values are computed on the *scaled* matrix and coloured by *unscaled* feature values — `StandardScaler` is strictly monotone per feature, so ordering and attribution are unchanged.

| # | Feature | mean \|SHAP\| (EE points) | share of attribution |
|---|---|---|---|
| 1 | `surfactant_concentration` | 6.67 | 26.0 % |
| 2 | `mol_logP` | 4.14 | 16.1 % |
| 3 | `polymer_MW` | 2.51 | 9.7 % |
| 4 | `drug/polymer` | 2.38 | 9.3 % |
| 5 | `mol_melting_point` | 1.68 | 6.5 % |

> ⚠️ **These are not biological ground truth.** Phase 4 established that the model does **not** generalise to unseen drugs, so this ranking describes what the Random Forest memorised to minimise *training* error. It is in-sample model introspection. 62 of 65 drugs appear in a single publication, so drug identity, study protocol, and descriptor values are confounded — an "important" descriptor may be standing in for "which paper this row came from." Every row of `SHAP_feature_importance.csv` carries `in_sample_only__not_ground_truth = True`.

**Why Phase 4 came out negative — the mechanism is shrinkage toward the mean.** Pooled out-of-fold predictions (5 shuffled grouped partitions, 60 fits, every fold asserting no `drug_group` *and* no `small_molecule_name` overlap) reproduce Phase 4 exactly: deterministic partition MAE **16.695** / R² **+0.170**; repeated-partition mean MAE **20.710**.

| Calibration of the OOF predictions | Model | Ideal |
|---|---|---|
| Regression slope of predicted on measured | **0.156** | 1.0 |
| SD of predictions | 13.94 | 23.51 (measured) |
| Range of predictions | 8.7 – 83.5 | 0.0 – 98.9 (measured) |

The failure is **asymmetric**, not a symmetric loss of precision — quartiles of drug-group mean EE % (defined by `pd.qcut`, not chosen after inspecting errors):

| Quartile | drug-mean EE % | n groups | median MAE | mean signed error | Δ vs mean-predictor | worse than mean-predictor |
|---|---|---|---|---|---|---|
| Q1 lowest | 0.3 – 33.0 | 16 | 16.07 | **+20.95** (over) | **−28.71** | 2/16 |
| Q2 | 33.5 – 65.1 | 16 | 15.91 | +11.05 | +0.15 | 8/16 |
| Q3 | 65.3 – 79.9 | 15 | 17.59 | −11.42 | +6.43 | 11/15 |
| Q4 highest | 80.5 – 98.8 | 16 | **27.10** | **−32.06** (under) | **+9.44** | 11/16 |

So the model genuinely **helps** on the lowest-EE quartile (a flat guess of 64.8 % is hopeless for a 10 %-EE drug) and **hurts** on the top two. The two effects nearly cancel, leaving it **+1.57 EE points worse** than a mean guess overall — that cancellation *is* Phase 4's headline. **32 of 63 drug groups are predicted worse than a mean guess.**

Distance from the dataset mean does **not** significantly explain per-drug error (Pearson r = +0.201, p = 0.114; Spearman ρ = +0.225, p = 0.076; n = 63) — reported here because it was tested, and it is the asymmetry above, not distance, that carries the signal.

**Worst 5 drugs** (repeated-CV MAE, EE points) — all five worse than a mean guess, three of them singletons:

| Drug | n | measured EE % | predicted | MAE | Δ vs mean-pred. | direction |
|---|---|---|---|---|---|---|
| ketoprofen | 2 | 10.6 | 83.3 | **72.78** | +17.99 | over |
| paeonol | 1 | 86.3 | 31.7 | 54.61 | +32.17 | under |
| tretinoin | 1 | 98.8 | 44.4 | 54.39 | +21.06 | under |
| levofloxacin | 1 | 15.0 | 66.9 | 51.86 | +2.42 | over |
| dexibuprofen | 3 | 88.7 | 38.0 | 50.64 | +25.39 | under |

**Best 5** (rapamycin 3.77, isoniazid 5.28, rhodamine-123 5.92, kartogenin 6.44, propyl-4-hydroxybenzoate 6.46) are **all singletons** — one measurement each. They are recorded as *not yet contradicted*, not as solved.

Sample size does not buy safety: flurbiprofen has 36 formulations yet MAE 41.42 under repeated CV vs 20.65 on the single deterministic partition. Withholding a whole large drug block removes much of the training signal, so the `MAE_repeated` − `MAE_single_partition` gap is itself a diagnostic column.

Figures (300 DPI): `Fig4_SHAP_summary.png` (beeswarm + mean-|SHAP| bars), `Fig5_Actual_vs_Predicted_OOF.png` (deterministic vs seed-averaged OOF, `y = x` diagonal, singletons marked), `Fig6_Worst_Predicted_Drugs.png` (absolute-error distributions for the worst 5).
Tables: `Error_analysis_by_drug.csv` (63 rows, 23 columns), `Error_analysis_by_EE_quartile.csv`, `SHAP_feature_importance.csv`, `OOF_predictions_random_forest.csv` (430 rows, per-seed predictions retained).

> **Note on Fig 5(b).** Its MAE 20.02 / R² −0.129 are the metrics of the *seed-averaged* prediction; Phase 4's pooled 20.71 is the *mean of the five per-partition MAEs*. Averaging across partitions cancels partition-to-partition variance, so the averaged prediction scores better. Both are correct measures of different quantities.

## Reproducing the audit
Python 3.12, dependencies in [`requirements.txt`](requirements.txt).

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m jupyter nbconvert --to notebook --execute --inplace notebooks/01_data_audit.ipynb notebooks/02_preprocessing.ipynb notebooks/03_exploratory_analysis.ipynb notebooks/04_model_training.ipynb notebooks/05_explainability_and_errors.ipynb
```

## Integrity commitments
No fabricated values, no synthetic formulations, no minority-class oversampling, no silent data edits. Raw data is verified by SHA256 and never modified. Correlations are reported as associations, not causation. Generalisation claims are scoped to the dataset's constrained chemical space.

## License
Code: for academic evaluation. Dataset: CC BY 4.0 (attribute Goren et al. 2025 as above).
