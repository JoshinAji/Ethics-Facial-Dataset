# Project Structure

## 📁 Clean, Production-Ready Organization

```
.
├── Data/                           # Datasets and visualizations
│   ├── codebook_v3.json           # V3 schema definition
│   ├── labels_v1.csv              # V1: Baseline (900 images)
│   ├── labels_v2_balanced.csv     # V2: Balanced (844 images)
│   ├── labels_v3.csv              # V3: Ethical metadata (900 images) ⭐
│   ├── v3_manual_subset.csv       # Validation subset (136 images)
│   ├── v1_v2_v3_comparison.png    # Comparative visualization
│   ├── v3_ethical_analysis.png    # V3 analysis dashboard
│   ├── v3_bias_detection_demo.png # Bias detection demonstration
│   ├── FairFace/                  # Source images (592 images)
│   └── UTKFace/                   # Source images (308 images)
│
├── Script/                         # Analysis and generation scripts
│   ├── autofill_v3_heuristics.py         # ⭐ Generate V3 ethical labels
│   ├── compare_v1_v2_v3.py               # ⭐ Compare all versions
│   ├── visualize_v3_results.py           # ⭐ Visualize V3 analysis
│   ├── demonstrate_v3_bias_detection.py  # ⭐ Show V3 bias detection
│   ├── complete_manual_validation.py     # Manual annotation helper
│   └── compare_manual_vs_heuristic.py    # Validation analysis
│
├── Docs/                           # Documentation
│   ├── V3_EXECUTIVE_SUMMARY.md    # Quick overview
│   ├── WHY_V3_IS_BETTER.md        # Detailed fairness analysis
│   ├── V3_ETHICAL_LABELING_RESULTS.md  # V3 results
│   └── QUICKSTART_V3.md           # Usage guide
│
├── Notebook/                       # (Empty - reserved for analysis)
│
└── README.md                       # ⭐ Main project documentation

⭐ = Essential files for final project
```

## 🎯 Key Files for Your Paper

### 1. Main Dataset
- **`Data/labels_v3.csv`** - Your primary contribution (900 images, 17 features)

### 2. Core Scripts (Show Your Work)
- **`Script/autofill_v3_heuristics.py`** - How V3 was generated
- **`Script/compare_v1_v2_v3.py`** - Comparison analysis
- **`Script/demonstrate_v3_bias_detection.py`** - NEW: Shows V3 reveals hidden bias

### 3. Visualizations (For Paper Figures)
- **`Data/v1_v2_v3_comparison.png`** - Shows evolution V1→V2→V3
- **`Data/v3_ethical_analysis.png`** - V3 metadata breakdown
- **`Data/v3_bias_detection_demo.png`** - NEW: V3 bias detection capabilities

### 4. Documentation (Reference Material)
- **`README.md`** - Complete project overview
- **`Docs/WHY_V3_IS_BETTER.md`** - Detailed fairness arguments
- **`Docs/V3_EXECUTIVE_SUMMARY.md`** - Quick reference

## 🧹 What Was Removed

**Cleaned up:**
- ❌ Jupyter checkpoint files (`.ipynb_checkpoints/`)
- ❌ Development notebooks (9 `.ipynb` files)
- ❌ Intermediate data (`pool.csv`, `reports/`, `splits/`, `views/`)
- ❌ macOS metadata (`.DS_Store` files)
- ❌ Empty placeholders (`.gitkeep`)

**Result:** 
- Before: ~25 files in Script/
- After: 6 essential Python scripts
- Data reduced from 121K+ rows to focused datasets

## 🚀 Quick Start

### Generate V3 Labels
```bash
python Script/autofill_v3_heuristics.py --overwrite
```

### Run Comparison Analysis
```bash
python Script/compare_v1_v2_v3.py
```

### Demonstrate Bias Detection
```bash
python Script/demonstrate_v3_bias_detection.py
```

### Visualize V3
```bash
python Script/visualize_v3_results.py
```

## 📊 For Your Final Project Submission

**Include:**
1. **Code:** All 6 scripts in `Script/` directory
2. **Data:** All CSV files and visualizations in `Data/`
3. **Documentation:** All markdown files in `Docs/` + README
4. **Images:** Source images (FairFace + UTKFace) if allowed by assignment

**Paper figures to use:**
- Figure 1: `v1_v2_v3_comparison.png` - Dataset evolution
- Figure 2: `v3_ethical_analysis.png` - V3 metadata breakdown
- Figure 3: `v3_bias_detection_demo.png` - Bias detection demonstration

## 📝 Total File Count

- **Scripts:** 6 Python files (~48 KB total)
- **Data:** 4 CSV files + 3 visualizations (~1.7 MB)
- **Docs:** 4 markdown files (~30 KB)
- **Images:** ~900 source images (~50-100 MB)

**Total project size:** ~100-150 MB (clean and focused)

---

**Last Updated:** November 8, 2025  
**Status:** Production-ready ✅
