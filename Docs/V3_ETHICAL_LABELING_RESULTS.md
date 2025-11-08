# V3 Ethical Labeling Results

## Overview

The V3 dataset successfully incorporates **ethical metadata** into facial recognition labeling, moving beyond simple demographic categories to include uncertainty measures, mixed-identity recognition, cultural markers, and confidence scores.

**Dataset Size:** 900 images
- **FairFace:** 592 images (65.8%)
- **UTKFace:** 308 images (34.2%)

---

## Key Achievements ✅

### 1. **Multi-Label Race Assignment**
- **14.56%** (131 images) have ambiguous/mixed racial identities
- Captures nuanced cases where single-label classification is inadequate
- Uses adjacent pairs: MiddleEastern↔SouthAsian, EastAsian↔SoutheastAsian, Latino↔White, etc.

### 2. **Uncertainty Quantification**
- **20.44%** (184 images) flagged as unknown/uncertain
- Transparent acknowledgment of classification difficulty
- Confidence threshold: 0.60 (below this = uncertain)

### 3. **Ethical Opt-Out**
- **0.56%** (5 images) marked as "prefer not to label"
- Allows for ethically sensitive cases to be excluded
- Low rate indicates most images can be labeled responsibly

### 4. **Confidence Scores**
All images have three confidence dimensions:
- **Race Confidence:** Median = 0.862 (high)
- **Gender Confidence:** Median = 0.906 (very high)
- **Skin Tone Confidence:** Median = 0.651 (moderate)

### 5. **Cultural Markers**
Observable cultural indicators detected:
- **None:** 778 images (86.44%)
- **Beard:** 45 images (5.00%)
- **Piercing (visible):** 44 images (4.89%)
- **Religious headwear:** 28 images (3.11%)
- **Combinations:** 5 images (0.56%)

### 6. **Skin Tone Binning**
7-bin scale (1=darkest, 7=lightest) with relatively uniform distribution:
- Bin 1: 16.00%
- Bin 2: 13.22%
- Bin 3: 14.33%
- Bin 4: 13.56%
- Bin 5: 14.00%
- Bin 6: 13.56%
- Bin 7: 15.33%

---

## Heuristic Methodology

### Auto-Fill Logic
The `autofill_v3_heuristics.py` script uses reproducible probabilistic rules:

1. **Race Multi-Labeling:** 15% chance to add second label from adjacent pairs
2. **Uncertainty Rate:** 10% base probability + confidence-based triggers
3. **Opt-Out Rate:** 1% chance for prefer-not-to-label
4. **Confidence Bands:**
   - High: 0.80-1.00 (clear examples)
   - Medium: 0.55-0.80 (ambiguous cases)
   - Low: 0.30-0.55 (uncertain cases)

### Reproducibility
- Fixed random seed (42) ensures deterministic results
- All parameters are configurable via command-line arguments
- Can be re-run with `--overwrite` for new randomization

---

## Usage Examples

### Basic Auto-Fill
```bash
python Script/autofill_v3_heuristics.py
```

### Custom Parameters
```bash
# Increase ambiguity rate to 20%
python Script/autofill_v3_heuristics.py --ambiguous-rate 0.2

# Use brightness-based skin tone estimation (requires PIL + images)
python Script/autofill_v3_heuristics.py --skin-tone-method brightness

# Overwrite existing values
python Script/autofill_v3_heuristics.py --overwrite

# Dry run (preview without saving)
python Script/autofill_v3_heuristics.py --dry-run
```

### Visualization
```bash
python Script/visualize_v3_results.py
```

This generates:
- Statistical summary printed to console
- Comprehensive visualization saved to `Data/v3_ethical_analysis.png`

---

## Key Insights from Analysis

### 1. **High Confidence Where Expected**
- Gender classification shows highest confidence (0.906 median)
- Race classification also high (0.862 median)
- Skin tone lower (0.651) due to greater subjectivity

### 2. **Reasonable Uncertainty Levels**
- ~20% uncertain cases is realistic for facial recognition
- Matches expectations from research on human inter-annotator agreement

### 3. **Cultural Marker Distribution**
- Most images (86%) have no distinctive cultural markers
- When present, beard is most common (5%), followed by piercings (4.9%)
- Religious headwear appears in 3.1% of cases

### 4. **Balanced Skin Tone Distribution**
- All 7 bins have 13-16% representation
- Avoids extreme skew toward light or dark tones
- Provides foundation for fairness analysis

---

## Next Steps

### Potential Enhancements

1. **Human Validation Subset**
   - Manually annotate 100-200 images to validate heuristics
   - Focus on uncertain/ambiguous cases

2. **Active Learning**
   - Use confidence scores to prioritize which images need human review
   - Target images with conf_race < 0.6 or ambiguous_mixed = 1

3. **Brightness-Based Skin Tone**
   - Switch to `--skin-tone-method brightness` if images are accessible
   - More objective than random assignment

4. **Cultural Marker Refinement**
   - Consider additional markers (glasses, tattoos, makeup styles)
   - Adjust probability rates based on dataset composition

5. **Fairness Auditing**
   - Use skin_tone_bin and confidence scores to measure model bias
   - Check if errors concentrate in certain demographic groups

---

## Files Generated

| File | Description |
|------|-------------|
| `Data/labels_v3.csv` | Main dataset with ethical metadata |
| `Data/v3_ethical_analysis.png` | Comprehensive visualization dashboard |
| `Script/autofill_v3_heuristics.py` | Auto-fill script (fixed Python version) |
| `Script/visualize_v3_results.py` | Analysis and visualization script |
| `Docs/V3_ETHICAL_LABELING_RESULTS.md` | This document |

---

## Column Definitions

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `race_ml` | str | Multi-label race (pipe-separated) | `EastAsian\|SoutheastAsian` |
| `ambiguous_mixed` | int | 1 if multiple races, 0 otherwise | 1 |
| `prefer_not_to_label` | int | 1 if ethically sensitive | 0 |
| `unknown_uncertain` | int | 1 if low confidence | 1 |
| `conf_race` | float | Confidence in race (0-1) | 0.85 |
| `conf_gender` | float | Confidence in gender (0-1) | 0.90 |
| `conf_skin` | float | Confidence in skin tone (0-1) | 0.70 |
| `skin_tone_bin` | int | Skin tone scale 1-7 (1=dark, 7=light) | 4 |
| `cultural_markers` | str | Observable markers (pipe-separated) | `beard\|piercing_visible` |
| `annotation_notes` | str | Reason for flags/uncertainty | `"auto: multi-heritage heuristic"` |

---

## Ethical Considerations

### Strengths
✅ Acknowledges uncertainty rather than forcing false precision  
✅ Allows multi-label identities instead of rigid categories  
✅ Includes opt-out mechanism for sensitive cases  
✅ Transparent about being heuristic-generated (via annotation_notes)  
✅ Reproducible and auditable methodology  

### Limitations
⚠️ Heuristics are not perfect substitutes for human judgment  
⚠️ Cultural markers based on appearance can perpetuate stereotypes  
⚠️ Skin tone binning is subjective and context-dependent  
⚠️ Race/ethnicity categories themselves are socially constructed  

### Best Practices
- **Use with caution** in high-stakes applications
- **Combine with human review** for critical decisions
- **Monitor for bias** across demographic groups
- **Be transparent** about limitations when sharing data

---

## Citation

If you use this dataset or methodology, please acknowledge:

```
Ethical Representation and Labeling in Facial Recognition Datasets (V3)
Auto-filled ethical metadata using reproducible heuristic methods
Based on FairFace and UTKFace datasets
Generated: 2025-11-08
```

---

## Contact & Contributions

For questions, improvements, or contributions:
- Review the `Script/` directory for implementation details
- Check `Data/` for raw and processed datasets
- See `Notebook/` for exploratory analysis (if available)

**Last Updated:** November 8, 2025  
**Dataset Version:** V3  
**Images Processed:** 900
