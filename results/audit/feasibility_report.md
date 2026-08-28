# Feasibility of Unseen-Drug Encapsulation-Efficiency Prediction
**Phase 1 data feasibility audit — PLGA-EE-Generalization**

Dataset: Goren et al., *Scientific Data* (2025) 12:1182 · Mendeley DOI `10.17632/sbjf5csrdm.1` · License CC BY 4.0.
All five files verified against official Mendeley SHA256 hashes (see `source_manifest.csv`). No values were modified, imputed, or synthesised.

## Plain-language summary (for a non-specialist reviewer)
We want to predict how much drug gets trapped inside a PLGA nanoparticle (**encapsulation efficiency, EE%**), and — crucially — to test whether a model can do this for **drugs it has never seen before**. The dataset has **433 formulations** covering **65 different small-molecule drugs** from **59 published studies**. The good news: EE is recorded for **every** formulation, the molecular and formulation inputs are complete, and each drug has the chemical descriptors a model needs. The catch: the drugs are **very unevenly represented** — half of them (33 of 65) appear in only a **single** formulation, while a handful of drugs dominate. That imbalance shapes *how* we must test the model (grouped cross-validation, not naive random splits), but it does **not** block the project. Verdict: **feasible with modifications.**

## A. Is EE sufficiently available to serve as the primary regression target?
**Yes.** EE is present for 433/433 formulations (100%); 0 missing. Range 0.0–98.9% (mean 64.7, median 70.62), all within the plausible 0–100% bound. Caveat: per the Methods, some EE values were back-calculated from LC when EE was unreported — a reason to (a) exclude LC as a feature and (b) later flag which EE values were derived.

## B. How many unique drugs have usable EE observations?
All **65** unique drugs have at least one formulation with EE. But "usable for testing generalisation" depends on count: **32** drugs have ≥2 formulations, **28** have ≥3, **20** have ≥5, and **14** have ≥10.

## C. How uneven is the number of formulations per drug?
**Severely uneven.** Median = 1 formulation per drug, max = 36. Singletons: **33 drugs (51% of drugs)**. The 10 most common drugs account for **64%** of all formulations.

## D. Is drug-grouped validation possible?
**Yes.** Drug identity is recoverable for every row (via the row-aligned `NP_dataset_formulations.csv`), giving a clean group label. GroupKFold / GroupShuffleSplit by drug are directly applicable.

## E. Would literal Leave-One-Drug-Out be scientifically sensible?
**Only as a secondary, aggregate view.** With 33 singleton drugs, most LODO folds would test a single formulation, so per-drug metrics would be very noisy and easily misread. Report LODO only in aggregate, never as reliable individual-drug scores.

## F. Would GroupKFold be more defensible?
**Yes — recommended primary scheme.** Repeated GroupKFold-by-drug (≈5 folds, several seeds, averaged) tests every formulation once as an unseen drug while remaining stable despite the singletons.

## G. Which variables are suitable candidate predictors?
Molecular descriptors (mol_MW, mol_logP, mol_TPSA, mol_melting_point, mol_Hacceptors, mol_Hdonors, mol_heteroatoms), polymer descriptors (polymer_MW, LA/GA), process variables (drug/polymer, surfactant_concentration, aqueous/organic, pH*), and excipient/solvent descriptors (surfactant_HLB, solvent_polarity_index). *pH is an ordinal code, not raw pH.

## H. Which variables must be excluded because of leakage?
**LC (definite leakage** — inter-convertible with EE via formulation quantities; r(EE,LC)=0.49 here, but the leakage is structural, not just correlational). **particle_size** (measured outcome, not a pre-formulation design variable; r(EE,particle_size)=0.31). **Drug identity / reference** may be used only for grouping, never as features.

## I. Are molecular descriptors adequate for an unseen-drug study?
**Adequate, but the chemical space is concentrated.** Every drug has SMILES + RDKit descriptors + melting point (0% missing), so any new small molecule can be featurised. Consistent with the authors' note on constrained chemical diversity, the drugs cluster in a narrow lipophilicity band: per-drug logP IQR ≈ 1.9–3.86 and 85% of the 65 drugs fall within logP 0–5, with only a few outliers stretching the full range to -1.05–8.91. Generalisation claims must therefore be scoped to this well-populated region; drugs far outside it (very hydrophilic or very lipophilic) are extrapolation and should be flagged as such.

## J. Are there major missing-data problems?
**No.** The 18 analytical variables are 100% complete across all 433 formulations; identity columns are complete too.

## K. Are there publication/study-level clustering concerns?
**Yes.** 59 studies; **62/65** drugs appear in only one publication, so drug identity and study identity are partly confounded (a model may learn study "fingerprints"). Add a study-level (GroupKFold-by-reference) robustness check alongside the drug-level evaluation. Also note 3 exact duplicate rows flagged for review.

## L. Does the dataset support my current research title?
**Yes, with modifications.** The data supports "predicting EE for unseen small-molecule drugs in PLGA nanoparticles" provided the evaluation uses drug-grouped CV (not random splits), LC and particle_size are excluded as predictors, pH is handled as an ordinal code, and generalisation claims are scoped to the dataset's limited chemical space and the singleton-heavy drug distribution.

---
# OVERALL CLASSIFICATION: **FEASIBLE WITH MODIFICATIONS**

**Why:** EE is fully available, clean, and drug identity is cleanly recoverable, so the core experiment is possible. The required modifications are: (1) drug-grouped, repeated cross-validation (GroupKFold-by-drug primary; LODO aggregate-only) because 51% of drugs are singletons; (2) exclude LC (definite leakage) and particle_size (measured outcome) from predictors; (3) treat pH as an ordinal encoded variable and clarify the undocumented "-2" code; (4) add a study-level robustness check given 62/65 drugs are confined to one publication; (5) scope generalisation claims to the constrained chemical space; (6) review the 3 flagged duplicate rows. None of these block the project — they define an honest, leakage-free evaluation protocol.
