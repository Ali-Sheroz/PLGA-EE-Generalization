# Raw data — provenance & integrity

**Directory policy:** `data/raw/` is **immutable**. These files are the authentic originals downloaded from the official source and must never be edited, cleaned, renamed, or re-saved. All processing happens downstream and writes elsewhere (`data/processed/`, `results/`).

## Source
| Field | Value |
|---|---|
| Dataset title | A formulation dataset of poly(lactide-co-glycolide) nanoparticles for small molecule delivery |
| Authors | Goren A, Bao Z, Martinez Lozano JP, Allen C |
| Publication | *Scientific Data* (2025) **12**:1182 |
| Article DOI | `10.1038/s41597-025-05520-9` |
| Dataset DOI | `10.17632/sbjf5csrdm.1` |
| Repository | Mendeley Data (official record), version 1 |
| License | **Creative Commons Attribution 4.0 (CC BY 4.0)** |
| Downloaded from | `https://data.mendeley.com/datasets/sbjf5csrdm/1` (official public files API) |
| Download date | **2026-08-27** |
| Downloaded by | Project author, for academic research (Phase 1 feasibility audit) |

Files were retrieved **only** from the official Mendeley Data record above — not from GitHub, Kaggle, ResearchGate, blogs, or any mirror.

## Files & integrity (SHA256)
Each SHA256 below was recomputed locally after download and matches the hash reported by the Mendeley Data public API for record `sbjf5csrdm`, version 1. Integrity: **all 5 files PASS**.

| File | Size (bytes) | Rows × Cols | SHA256 |
|---|---:|---|---|
| `NP_dataset.csv` | 31,170 | 433 × 18 | `51cca74b0ed5f24d02dc5ba9f416fc2e1769f56193fe4bd84f1d4f48a818d3b8` |
| `NP_dataset_formulations.csv` | 40,261 | 433 × 13 | `1cf666cc5dbc249503a632236691884a7d599606faa6d32d938db45163484357` |
| `NP_dataset_small_molecules.csv` | 4,696 | 65 × 3 | `c49898e48de033b47d21fceb4110aca2325f241a602402c2bc6ad0001f3be3fa` |
| `NP_dataset_solvents.csv` | 93 | 4 × 2 | `39fd8ddb553912ed6a69b0ae1e1ed46ea7d0d9463489eb4f6bc00fe0f307e279` |
| `NP_dataset_surfactants.csv` | 168 | 9 × 2 | `9027eb013e3922f96e64ef7b1478f02b831dbec3ab30d3f2c3651555f96e7a27` |

To re-verify at any time (Git Bash):

```bash
sha256sum data/raw/*.csv
```

## What each file contains
- **`NP_dataset.csv`** — the final analytical table: 433 formulations × 18 **numeric** features (polymer + RDKit molecular descriptors + formulation/process parameters + `surfactant_HLB` + `solvent_polarity_index` + `particle_size`, `EE`, `LC`). Contains **no** drug names or references.
- **`NP_dataset_formulations.csv`** — the initial literature-curated formulations (433 rows), holding **identity/provenance**: `reference` (source DOI), `small_molecule_name`, `surfactant_name`, `solvent`, plus raw formulation parameters and outcomes. Row-aligned 1:1 with `NP_dataset.csv` (verified: 0 cell mismatches across the 9 shared columns).
- **`NP_dataset_small_molecules.csv`** — lookup: `small_molecule_name`, `canonical_SMILES`, `mol_melting_point` (65 molecules).
- **`NP_dataset_surfactants.csv`** — lookup: `surfactant_name`, `surfactant_HLB` (9 surfactants incl. `none` = 0).
- **`NP_dataset_solvents.csv`** — lookup: `solvent`, `solvent_polarity_index` (4 solvents).

## Attribution (CC BY 4.0)
If any part of this dataset is used or shown, cite:

> Goren A, Bao Z, Martinez Lozano JP, Allen C. A formulation dataset of poly(lactide-co-glycolide) nanoparticles for small molecule delivery. *Scientific Data* 2025;12:1182. https://doi.org/10.1038/s41597-025-05520-9. Dataset: https://doi.org/10.17632/sbjf5csrdm.1 (CC BY 4.0).
