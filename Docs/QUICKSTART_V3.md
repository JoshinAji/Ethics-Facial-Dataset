# V3 Ethical Labeling - Quick Start Guide

## 🚀 Quick Commands

### 1. Generate Ethical Labels
```bash
# Basic auto-fill (fills only empty columns)
python Script/autofill_v3_heuristics.py

# Regenerate all labels (overwrites existing)
python Script/autofill_v3_heuristics.py --overwrite

# Preview without saving
python Script/autofill_v3_heuristics.py --dry-run
```

### 2. Visualize Results
```bash
python Script/visualize_v3_results.py
```
Output: `Data/v3_ethical_analysis.png`

### 3. Quick Data Check
```bash
# View first few rows
head -5 Data/labels_v3.csv

# Count total images
wc -l Data/labels_v3.csv

# Check for uncertain cases
grep ",1.0," Data/labels_v3.csv | wc -l
```

---

## 📊 Current Dataset Stats

**Total Images:** 900  
**Ambiguous/Mixed:** 14.56% (131 images)  
**Uncertain Cases:** 20.44% (184 images)  
**Ethical Opt-Out:** 0.56% (5 images)

**Confidence Medians:**
- Race: 0.862
- Gender: 0.906  
- Skin: 0.651

---

## 🎛️ Common Parameter Adjustments

```bash
# More ambiguity (20% instead of 15%)
python Script/autofill_v3_heuristics.py --ambiguous-rate 0.2

# More uncertainty (15% instead of 10%)
python Script/autofill_v3_heuristics.py --uncertain-rate 0.15

# More ethical opt-outs (5% instead of 1%)
python Script/autofill_v3_heuristics.py --prefer-not-rate 0.05

# Different random seed
python Script/autofill_v3_heuristics.py --seed 123

# Brightness-based skin tone (requires images)
python Script/autofill_v3_heuristics.py --skin-tone-method brightness
```

---

## 📁 File Locations

| File | Purpose |
|------|---------|
| `Data/labels_v3.csv` | **Main dataset** with ethical metadata |
| `Script/autofill_v3_heuristics.py` | **Generator script** (Python) |
| `Script/autofill_v3_heuristics.ipynb` | Original notebook (has issues) |
| `Script/visualize_v3_results.py` | **Visualization script** |
| `Data/v3_ethical_analysis.png` | Generated visualization |
| `Docs/V3_ETHICAL_LABELING_RESULTS.md` | Full documentation |

---

## 🔍 Python Quick Analysis

```python
import pandas as pd

# Load dataset
v3 = pd.read_csv("Data/labels_v3.csv")

# Basic stats
print(f"Total images: {len(v3)}")
print(f"Uncertain: {(v3['unknown_uncertain']==1).sum()}")
print(f"Mixed identity: {(v3['ambiguous_mixed']==1).sum()}")

# Filter uncertain cases
uncertain = v3[v3['unknown_uncertain'] == 1]
print(uncertain[['image_id', 'race_ml', 'conf_race', 'annotation_notes']])

# Filter multi-label cases
mixed = v3[v3['race_ml'].str.contains('|', na=False)]
print(mixed[['image_id', 'race_ml', 'conf_race']])

# Confidence distribution
print(v3[['conf_race', 'conf_gender', 'conf_skin']].describe())
```

---

## 🛠️ Troubleshooting

### Issue: Script shows "0 rows filled"
**Solution:** Columns already populated. Use `--overwrite` to regenerate.

### Issue: FutureWarning about dtype
**Solution:** Warnings are informational only. Script still works correctly.

### Issue: Can't find input file
**Solution:** Check you're in the project root directory. Default input is `./Data/labels_v3.csv`

### Issue: Visualization doesn't display
**Solution:** 
- Check `Data/v3_ethical_analysis.png` was created
- If running remotely, image saved but won't display in terminal
- Open the PNG file manually

---

## 📈 What Each Column Means

| Column | Values | Meaning |
|--------|--------|---------|
| `race_ml` | `White`, `Black\|Latino`, etc. | Race (can be multi-label) |
| `ambiguous_mixed` | 0 or 1 | 1 = multiple races assigned |
| `unknown_uncertain` | 0 or 1 | 1 = low confidence or unclear |
| `prefer_not_to_label` | 0 or 1 | 1 = ethically sensitive case |
| `conf_race` | 0.0-1.0 | Confidence in race label |
| `conf_gender` | 0.0-1.0 | Confidence in gender label |
| `conf_skin` | 0.0-1.0 | Confidence in skin tone |
| `skin_tone_bin` | 1-7 | Skin tone (1=dark, 7=light) |
| `cultural_markers` | `none`, `beard`, etc. | Observable cultural cues |
| `annotation_notes` | text | Why flags were set |

---

## ✅ Next Steps

1. **Review Results:** Run visualization script to see distributions
2. **Validate Subset:** Manually check some uncertain cases
3. **Adjust Parameters:** Re-run with different rates if needed
4. **Use for Fairness:** Analyze model performance across groups
5. **Document Changes:** Keep notes on any manual corrections

---

## 🔗 Related Files

- Full documentation: `Docs/V3_ETHICAL_LABELING_RESULTS.md`
- Original prompt: See user conversation history
- Script source: `Script/autofill_v3_heuristics.py`

---

**Generated:** November 8, 2025  
**Last Run:** `--overwrite` with seed=42
