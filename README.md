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

EE% showed a **left-skewed distribution** with a median of **70.6%**, an IQR of **52.4–83.2%**, and a skewness of **−1.00**. Thirty-two formulations had EE below 20%. No individual descriptor showed a strong linear association with EE. The largest observed Pearson correlations were for surfactant_concentration (r = +0.31), surfactant_HLB (r = +0.30), and mol_logP (r = +0.23), supporting the use of multivariable modeling rather than reliance on any single descriptor.

These analyses are descriptive. Correlation does not imply causation, and the reported p-values assume independent observations. Because formulations are clustered within drugs and source studies, inferential statistics from the exploratory analysis should be interpreted cautiously. Drug-grouped validation was therefore used in Phase 4 to evaluate predictive generalization to unseen drugs.

## Phase 4 Deliverables — Model Training and Unseen-Drug Validation

**Notebook:** [`notebooks/04_model_training.ipynb`](notebooks/04_model_training.ipynb)

Model development used **`PLGA_clean_unscaled.csv`**, rather than the globally scaled processed file. Scaling and categorical encoding were therefore re-fitted within each training fold to prevent preprocessing leakage.

### Validation Setup

Three sparsely represented `LA/GA` categories (1.86, 2.33, and 5.67; 5 formulations across 4 drug groups) were combined into an `other` category. The final encoded feature matrix contained **430 formulations × 20 predictors**, with `EE` as the sole target.

Unseen-drug performance was evaluated using:

- `GroupKFold(n_splits=5)`
- grouping variable: `drug_group`
- no overlap of `drug_group` between training and test folds
- no overlap of raw `small_molecule_name` between training and test folds
- preprocessing fitted independently within each training fold

### Initial Grouped-CV Results

The following results correspond to the fixed five-fold grouped partition and are ranked by mean MAE:

| # | Model | MAE (mean ± SD) | RMSE (mean ± SD) | R² (mean ± SD) |
|---|---|---:|---:|---:|
| 1 | Random Forest | **16.70 ± 2.72** | 21.26 ± 2.69 | −0.076 ± 0.502 |
| 2 | SVR (RBF) | 18.33 ± 1.96 | 22.65 ± 2.31 | −0.196 ± 0.497 |
| — | *DummyRegressor (reference)* | *19.26 ± 4.37* | *23.59 ± 5.16* | *−0.194 ± 0.296* |
| 3 | XGBoost | 20.09 ± 4.23 | 24.66 ± 4.14 | −0.492 ± 0.884 |
| 4 | Linear Regression | 24.72 ± 6.09 | 30.04 ± 7.95 | −1.091 ± 0.987 |

These fixed-partition results suggested lower MAE for Random Forest. However, the negative mean R² values and large fold-to-fold variability indicated that this ranking required additional robustness testing before any conclusion about unseen-drug generalization could be made.

### Model Configuration

All candidate models used library-default hyperparameters; **no hyperparameter optimization was performed**. Only parameters required for reproducibility or computational control, such as `random_state` and `n_jobs`, were specified.

For SVR, the target was standardized within each training fold using `TransformedTargetRegressor(transformer=StandardScaler())`, because the default `C` and `epsilon` parameters operate on the scale of the target variable. The target transformer was fitted only on the training-fold `EE` values.

`DummyRegressor(strategy="mean")` was included solely as a **reference predictor** and was not treated as a candidate model or included in model ranking.

The Random Forest achieved the lowest mean MAE in the initial fixed grouped partition and was subsequently refitted on all 430 formulations for model inspection. The fitted artifact is stored in [`src/models/`](src/models) together with a metadata sidecar documenting its validation limitations.

### Robustness Across Grouped Partitions

The apparent Random Forest advantage in the initial `GroupKFold` partition was **not stable across repeated grouped partitions**. Mean per-fold R² was negative for every candidate model in the initial analysis, indicating substantial variation in performance across held-out drug groups.

To assess the stability of the ranking, grouped cross-validation was repeated across **five shuffled drug-group partitions**. Out-of-fold predictions were pooled across all held-out formulations within each partition before calculating performance metrics. This avoids giving small test folds the same weight as larger folds when summarizing performance.

| Model | Pooled OOF MAE | Pooled OOF R² |
|---|---:|---:|
| **DummyRegressor (mean-prediction reference)** | **19.14 ± 0.28** | −0.032 |
| Random Forest | 20.71 ± 3.18 | −0.299 |
| SVR (RBF) | 20.92 ± 1.72 | −0.210 |
| XGBoost | 21.86 ± 4.22 | −0.438 |
| Linear Regression | 25.72 ± 1.42 | −0.785 |

Across the repeated grouped partitions, **no candidate model consistently outperformed the mean-prediction reference for unseen drugs**. The lower MAE observed for Random Forest in the initial fixed partition was therefore partition-dependent rather than evidence of stable unseen-drug generalization.
### Overall Phase 4 Finding

**No candidate model consistently outperformed the mean-prediction reference across repeated grouped partitions.** Random Forest outperformed the reference in 2 of 5 partitions, XGBoost in 1 of 5, while SVR and Linear Regression did not outperform it in any partition.

The apparent Random Forest advantage observed in the initial fixed `GroupKFold` partition was therefore not stable across alternative drug-group partitions. The saved Random Forest artifact represents the best-performing candidate under that specified partition and is retained for model inspection and explainability analysis. It should **not be interpreted as a validated predictor of EE for unseen drugs**. This limitation is documented in the model metadata under `generalisation_caveat`.

### Interpretation

The limited generalization observed across the 63 drug groups is consistent with sparse and highly imbalanced drug representation, limited descriptor coverage, and substantial study-level heterogeneity. Approximately 51% of drug groups contain only a single formulation, which restricts the amount of transferable information available for learning relationships that extend to unseen compounds.

These findings indicate that performance obtained from formulation-level splits does not, by itself, demonstrate generalization to drugs excluded from model training. Drug-grouped evaluation is therefore necessary when the intended application involves prediction for previously unseen small-molecule drugs.

### Supporting Tables

- `laga_regrouping.csv`
- `ML_cv_fold_composition.csv`
- `ML_grouped_per_fold_metrics.csv`
- `ML_grouped_performance_repeated.csv`
- `ML_grouped_performance_pooled_oof_repeated.csv`
- `ML_grouped_pooled_oof_per_seed.csv`

`ML_cv_fold_composition.csv` documents the composition of the five grouped folds, including training/test sample sizes and variation in mean EE across held-out folds.

## Phase 5 Deliverables — Explainability and Error Analysis

**Notebook:** [`notebooks/05_explainability_and_errors.ipynb`](notebooks/05_explainability_and_errors.ipynb)

The analysis loads the saved Random Forest pipeline together with `PLGA_clean_unscaled.csv`. Feature order is verified against both the fitted pipeline and its `.meta.json` sidecar before model-attribution analysis is performed.

### SHAP Analysis

SHAP values were calculated using `shap.TreeExplainer` for all **430 formulations × 20 model features**. The model base value was **64.735 EE%**, and SHAP additivity was numerically verified against the pipeline predictions.

| # | Feature | Mean \|SHAP\| (EE points) | Share of attribution |
|---|---|---:|---:|
| 1 | `surfactant_concentration` | 6.67 | 26.0% |
| 2 | `mol_logP` | 4.14 | 16.1% |
| 3 | `polymer_MW` | 2.51 | 9.7% |
| 4 | `drug/polymer` | 2.38 | 9.3% |
| 5 | `mol_melting_point` | 1.68 | 6.5% |

> ⚠️ **Interpretation caution.** These SHAP values describe model attribution within the fitted Random Forest and should not be interpreted as biological causation or validated determinants of encapsulation efficiency. Phase 4 showed that the model did not generalize reliably to unseen drugs. In addition, 62 of 65 drugs occur in only one source publication, so drug identity, study conditions, and descriptor values are strongly confounded. Feature-attribution results should therefore be interpreted as model-specific patterns rather than biological ground truth.

### Prediction-Error Pattern

Repeated grouped out-of-fold predictions showed substantial compression toward the dataset mean. The analysis used five shuffled drug-group partitions, with no overlap in either `drug_group` or `small_molecule_name` between training and test sets.

The deterministic grouped partition produced an MAE of **16.695** and R² of **+0.170**, whereas the mean MAE across repeated grouped partitions was **20.710**.

| Prediction-compression measure | Model | Reference |
|---|---:|---:|
| Regression slope of predicted versus measured EE | **0.156** | 1.0 |
| SD of predictions | 13.94 | 23.51 measured |
| Prediction range | 8.7–83.5 | 0.0–98.9 measured |

The slope substantially below 1.0, together with the narrower prediction variance and range, indicates that the model tended to pull extreme EE values toward the center of the observed distribution.

### Error Distribution Across EE Quartiles

Drug groups were divided into quartiles according to their mean measured EE using `pd.qcut`.

**Δ vs mean predictor = model MAE − mean-predictor MAE.** Negative values indicate lower error than the reference, while positive values indicate higher error.

| Quartile | Drug-group mean EE% | n groups | Median MAE | Mean signed error | Δ vs mean predictor | Groups worse than reference |
|---|---:|---:|---:|---:|---:|---:|
| Q1 — lowest | 0.3–33.0 | 16 | 16.07 | **+20.95** | **−28.71** | 2/16 |
| Q2 | 33.5–65.1 | 16 | 15.91 | +11.05 | +0.15 | 8/16 |
| Q3 | 65.3–79.9 | 15 | 17.59 | −11.42 | +6.43 | 11/15 |
| Q4 — highest | 80.5–98.8 | 16 | **27.10** | **−32.06** | **+9.44** | 11/16 |

The error pattern was asymmetric. Predictions tended to **overestimate low-EE drugs** and **underestimate high-EE drugs**. Relative to the mean-prediction reference, Random Forest showed lower error in the lowest-EE quartile but poorer performance in the two highest quartiles. Overall, **32 of 63 drug groups** were predicted less accurately than the mean-prediction reference.

Distance from the dataset mean did not show a statistically significant association with per-drug prediction error (Pearson r = +0.201, p = 0.114; Spearman ρ = +0.225, p = 0.076; n = 63). These results suggest that the main limitation was not simply distance from the overall mean, but an asymmetric compression of predictions across the EE range.

### Drug-Level Error Analysis

The five drug groups with the highest repeated-CV MAE are shown below. All performed worse than the mean-prediction reference, and three were represented by a single formulation.

| Drug | n | Measured EE% | Predicted EE% | MAE | Δ vs mean predictor | Error direction |
|---|---:|---:|---:|---:|---:|---|
| ketoprofen | 2 | 10.6 | 83.3 | **72.78** | +17.99 | overprediction |
| paeonol | 1 | 86.3 | 31.7 | 54.61 | +32.17 | underprediction |
| tretinoin | 1 | 98.8 | 44.4 | 54.39 | +21.06 | underprediction |
| levofloxacin | 1 | 15.0 | 66.9 | 51.86 | +2.42 | overprediction |
| dexibuprofen | 3 | 88.7 | 38.0 | 50.64 | +25.39 | underprediction |

The five lowest-error drug groups were rapamycin (MAE 3.77), isoniazid (5.28), rhodamine-123 (5.92), kartogenin (6.44), and propyl-4-hydroxybenzoate (6.46). All five were singletons, so their apparently low errors are based on only one formulation each and should not be interpreted as evidence of consistently reliable prediction for those drugs.

Formulation count alone did not ensure stable prediction. For example, flurbiprofen was represented by 36 formulations but had a repeated-CV MAE of **41.42**, compared with **20.65** under the initial fixed grouped partition. This difference illustrates the sensitivity of drug-level performance to the particular grouped partition and further supports the use of repeated grouped evaluation rather than reliance on a single split.

### Phase 5 Figures and Tables

Figures are available at **300 DPI** in `results/figures/`:

- `Fig4_SHAP_summary.png` — SHAP beeswarm and mean absolute SHAP attribution.
- `Fig5_Actual_vs_Predicted_OOF.png` — measured versus out-of-fold predicted EE for the fixed and seed-averaged grouped analyses, with the `y = x` reference line and singleton drug groups identified.
- `Fig6_Worst_Predicted_Drugs.png` — absolute-error distributions for the five highest-error drug groups.

Supporting tables include:

- `Error_analysis_by_drug.csv` — 63 drug groups with drug-level error metrics.
- `Error_analysis_by_EE_quartile.csv`
- `SHAP_feature_importance.csv`
- `OOF_predictions_random_forest.csv` — 430 formulations with per-seed out-of-fold predictions.

> **Note on Fig. 5(b).** The seed-averaged out-of-fold prediction has an MAE of **20.02** and R² of **−0.129**. The Phase 4 value of **20.71** represents the mean of the five partition-specific pooled MAEs. Averaging predictions across partitions reduces partition-specific variation, so these values summarize different quantities and are not expected to be identical.

## Reproducing the Analysis

The analysis was developed using **Python 3.12**. Required dependencies are listed in [`requirements.txt`](requirements.txt).

The following commands reproduce the workflow on Windows:

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m jupyter nbconvert --to notebook --execute --inplace notebooks/01_data_audit.ipynb notebooks/02_preprocessing.ipynb notebooks/03_exploratory_analysis.ipynb notebooks/04_model_training.ipynb notebooks/05_explainability_and_errors.ipynb
```

## Research Integrity
No values or formulations were fabricated or synthetically generated. No oversampling was applied, and data modifications are documented throughout the workflow. Original source files were retained unchanged and verified using SHA256 checksums. Correlations are interpreted as associations rather than evidence of causation, and conclusions about generalization are restricted to the chemical and formulation space represented in the available dataset.

## License
The source dataset is distributed under CC BY 4.0 and should be attributed to Goren et al. (2025) using the citation provided above.
No separate software license is currently granted for the project code; all rights to the code are reserved unless otherwise stated.

I prefer **“Research Integrity”** over “Integrity commitments” because it sounds more natural in an academic repository.

The overall ending order is also correct:

**Reproducibility → Research Integrity → License**

If you later decide to make the code reusable, we can replace the last paragraph with a proper MIT or BSD license statement.
