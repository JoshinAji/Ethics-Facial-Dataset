# Script Directory

This directory contains all analysis and generation scripts for the V3 Ethical Labeling project.

## Core Scripts

### 1. `autofill_v3_heuristics.py` ⭐
**Purpose:** Generate V3 ethical metadata from base demographic labels

**Usage:**
```bash
# Basic generation (fill empty columns only)
python autofill_v3_heuristics.py

# Regenerate all labels (overwrite existing)
python autofill_v3_heuristics.py --overwrite

# Preview without saving
python autofill_v3_heuristics.py --dry-run

# Custom parameters
python autofill_v3_heuristics.py --ambiguous-rate 0.20 --uncertain-rate 0.15 --seed 123
```

**Key Parameters:**
- `--seed`: Random seed for reproducibility (default: 42)
- `--ambiguous-rate`: % of images with multi-label race (default: 0.15)
- `--uncertain-rate`: % of images flagged uncertain (default: 0.10)
- `--overwrite`: Replace existing values instead of filling blanks

---

### 2. `compare_v1_v2_v3.py` ⭐
**Purpose:** Comprehensive comparison of all three dataset versions

**Usage:**
```bash
python compare_v1_v2_v3.py
```

**Output:**
- Console: Detailed comparison statistics
- File: `Data/v1_v2_v3_comparison.png` (9-panel visualization)

**What it shows:**
- Race/gender distribution across versions
- Balance scores and representation gaps
- V3-specific features (multi-label, uncertainty, etc.)
- Feature count comparison

---

### 3. `visualize_v3_results.py` ⭐
**Purpose:** Visualize V3 ethical metadata statistics

**Usage:**
```bash
python visualize_v3_results.py
```

**Output:**
- Console: V3 statistics summary
- File: `Data/v3_ethical_analysis.png` (8-panel dashboard)

**What it shows:**
- Skin tone distribution
- Confidence score distributions
- Flag rates (ambiguous, uncertain, prefer-not-to-label)
- Cultural marker breakdown

---

### 4. `demonstrate_v3_bias_detection.py` ⭐ NEW
**Purpose:** Show how V3 reveals bias that V1 cannot detect

**Usage:**
```bash
python demonstrate_v3_bias_detection.py
```

**Output:**
- Console: Multi-dimensional bias analysis
- File: `Data/v3_bias_detection_demo.png` (5-panel comparison)

**What it demonstrates:**
- V1 view: Race-level accuracy only
- V3 view: Within-race bias by skin tone
- Confidence-accuracy correlation
- Cultural marker impact
- Uncertainty as error predictor

**Note:** Uses simulated model performance. Replace with real model predictions in production.

---

### 5. `complete_manual_validation.py` NEW
**Purpose:** Helper tool for manual annotation workflow

**Usage:**
```bash
python complete_manual_validation.py
```

**What it does:**
- Checks `Data/v3_manual_subset.csv` annotation status
- Provides instructions for manual labeling
- Shows examples of what to annotate

**Workflow:**
1. Run this script to see what needs annotation
2. Open images in `Data/FairFace/` and `Data/UTKFace/`
3. Fill in ethical metadata columns manually
4. Save as `Data/v3_manual_annotated.csv`
5. Run `compare_manual_vs_heuristic.py` to validate

---

### 6. `compare_manual_vs_heuristic.py` NEW
**Purpose:** Validate heuristic approach against human annotations

**Usage:**
```bash
python compare_manual_vs_heuristic.py
```

**Prerequisites:**
- Must have `Data/v3_manual_annotated.csv` (from manual annotation)

**Output:**
- Agreement rates for each metadata field
- Confidence score correlation
- Disagreement pattern analysis
- Validation summary

**Expected results:**
- 70-85% agreement: Good validation
- 85%+ agreement: Excellent validation
- <70% agreement: Heuristics need refinement

---

## Workflow for Final Project

### Step 1: Generate V3 Dataset
```bash
python autofill_v3_heuristics.py --overwrite
```

### Step 2: Run Comparison Analysis
```bash
python compare_v1_v2_v3.py
python visualize_v3_results.py
```

### Step 3: Demonstrate Bias Detection
```bash
python demonstrate_v3_bias_detection.py
```

### Step 4 (Optional): Manual Validation
```bash
# 1. Check validation status
python complete_manual_validation.py

# 2. Manually annotate 50-100 images
#    (Open v3_manual_subset.csv and fill in columns)

# 3. Compare annotations
python compare_manual_vs_heuristic.py
```

---

## Output Files Generated

| Script | Output File | Use in Paper |
|--------|-------------|--------------|
| `compare_v1_v2_v3.py` | `v1_v2_v3_comparison.png` | **Figure 1:** Dataset Evolution |
| `visualize_v3_results.py` | `v3_ethical_analysis.png` | **Figure 2:** V3 Metadata |
| `demonstrate_v3_bias_detection.py` | `v3_bias_detection_demo.png` | **Figure 3:** Bias Detection |

---

## Dependencies

All scripts require:
- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn

Optional:
- PIL/Pillow (for brightness-based skin tone estimation)

Install dependencies:
```bash
pip install pandas numpy matplotlib seaborn pillow
```

---

## Troubleshooting

### "File not found" errors
- Make sure you're running scripts from project root directory
- Check that `Data/labels_v1.csv`, `labels_v2_balanced.csv`, `labels_v3.csv` exist

### "0 rows filled" warning
- Columns already populated
- Use `--overwrite` flag to regenerate

### FutureWarning messages
- These are informational only
- Scripts will still run correctly
- To suppress: `python -W ignore script.py`

### Visualization doesn't display
- Images are saved to `Data/` directory
- Open PNG files manually if running remotely
- Use `plt.savefig()` output files for your paper

---

## For Your Paper

**Methods Section - Include:**
1. `autofill_v3_heuristics.py` methodology
2. Reproducibility details (seed=42, rates used)
3. Validation approach (if you completed manual annotation)

**Results Section - Include:**
1. Output from `compare_v1_v2_v3.py` (tables and figures)
2. Output from `demonstrate_v3_bias_detection.py` (bias detection results)
3. Validation results from `compare_manual_vs_heuristic.py` (if available)

**Figures for Paper:**
- All three PNG files generated by the scripts
- Tables from console output (copy to LaTeX/Word)

---

**Last Updated:** November 8, 2025  
**Status:** Production-ready ✅
