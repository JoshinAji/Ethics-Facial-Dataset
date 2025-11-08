"""
Comparative Analysis: V1 → V2 → V3 Evolution
Shows how each version improves fairness and ethical representation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load all three versions
print("="*80)
print("LOADING DATASETS...")
print("="*80)

v1 = pd.read_csv("Data/labels_v1.csv")
v2 = pd.read_csv("Data/labels_v2_balanced.csv")
v3 = pd.read_csv("Data/labels_v3.csv")

print(f"\nV1 (Original):     {len(v1)} images")
print(f"V2 (Balanced):     {len(v2)} images")
print(f"V3 (Ethical):      {len(v3)} images")

# ============================================================================
# SECTION 1: Dataset Composition & Balance
# ============================================================================

print("\n" + "="*80)
print("SECTION 1: DATASET COMPOSITION & BALANCE")
print("="*80)

def calculate_balance_score(df, col='race_cat'):
    """Calculate how balanced a dataset is (1.0 = perfect balance, 0.0 = worst)"""
    counts = df[col].value_counts()
    expected = len(df) / len(counts)
    # Chi-square-like deviation
    deviations = [(count - expected)**2 / expected for count in counts]
    max_deviation = len(df) * (len(counts) - 1)
    balance = 1 - (sum(deviations) / max_deviation)
    return balance

print("\n📊 RACE DISTRIBUTION:")
print("\nV1 (Original):")
v1_race = v1['race_cat'].value_counts()
for race, count in v1_race.items():
    print(f"  {race:20s}: {count:4d} ({count/len(v1)*100:5.1f}%)")
print(f"  Balance Score: {calculate_balance_score(v1, 'race_cat'):.3f}")

print("\nV2 (Balanced):")
v2_race = v2['race_cat'].value_counts()
for race, count in v2_race.items():
    print(f"  {race:20s}: {count:4d} ({count/len(v2)*100:5.1f}%)")
print(f"  Balance Score: {calculate_balance_score(v2, 'race_cat'):.3f}")

print("\nV3 (Ethical - base categories):")
v3_race = v3['race_cat'].value_counts()
for race, count in v3_race.items():
    print(f"  {race:20s}: {count:4d} ({count/len(v3)*100:5.1f}%)")
print(f"  Balance Score: {calculate_balance_score(v3, 'race_cat'):.3f}")

print("\n📊 GENDER DISTRIBUTION:")
print("\nV1:")
print(v1['gender_cat'].value_counts())
print(f"  Balance Score: {calculate_balance_score(v1, 'gender_cat'):.3f}")

print("\nV2:")
print(v2['gender_cat'].value_counts())
print(f"  Balance Score: {calculate_balance_score(v2, 'gender_cat'):.3f}")

print("\nV3:")
print(v3['gender_cat'].value_counts())
print(f"  Balance Score: {calculate_balance_score(v3, 'gender_cat'):.3f}")

# ============================================================================
# SECTION 2: Feature Comparison
# ============================================================================

print("\n" + "="*80)
print("SECTION 2: FEATURE EVOLUTION")
print("="*80)

print("\n📋 AVAILABLE FEATURES:")
print(f"\nV1 Columns ({len(v1.columns)}): {list(v1.columns)}")
print(f"\nV2 Columns ({len(v2.columns)}): {list(v2.columns)}")
print(f"\nV3 Columns ({len(v3.columns)}): {list(v3.columns)}")

print("\n✨ NEW FEATURES IN V3:")
v3_only = set(v3.columns) - set(v1.columns)
for feat in sorted(v3_only):
    print(f"  • {feat}")

# ============================================================================
# SECTION 3: Ethical Metadata Benefits
# ============================================================================

print("\n" + "="*80)
print("SECTION 3: V3 ETHICAL METADATA ADVANTAGES")
print("="*80)

print("\n🎯 MULTI-LABEL SUPPORT:")
multi_label_count = v3['race_ml'].str.contains('\\|', na=False).sum()
print(f"  Images with multiple racial identities: {multi_label_count} ({multi_label_count/len(v3)*100:.1f}%)")
print(f"  V1/V2 approach: Force into single category (information loss)")
print(f"  V3 approach: Preserve ambiguity (more accurate representation)")

print("\n❓ UNCERTAINTY QUANTIFICATION:")
uncertain_count = v3['unknown_uncertain'].astype(float).eq(1).sum()
print(f"  Images flagged as uncertain: {uncertain_count} ({uncertain_count/len(v3)*100:.1f}%)")
print(f"  V1/V2 approach: No uncertainty measure (false confidence)")
print(f"  V3 approach: Explicit confidence scores (transparency)")

print("\n📊 CONFIDENCE DISTRIBUTION:")
print(f"  Race confidence:   Mean={pd.to_numeric(v3['conf_race'], errors='coerce').mean():.3f}, "
      f"Median={pd.to_numeric(v3['conf_race'], errors='coerce').median():.3f}")
print(f"  Gender confidence: Mean={pd.to_numeric(v3['conf_gender'], errors='coerce').mean():.3f}, "
      f"Median={pd.to_numeric(v3['conf_gender'], errors='coerce').median():.3f}")
print(f"  Skin confidence:   Mean={pd.to_numeric(v3['conf_skin'], errors='coerce').mean():.3f}, "
      f"Median={pd.to_numeric(v3['conf_skin'], errors='coerce').median():.3f}")

print("\n🌈 SKIN TONE GRANULARITY:")
print(f"  V1/V2: No skin tone information")
print(f"  V3:    7-bin scale with confidence scores")
skin_dist = v3['skin_tone_bin'].value_counts().sort_index()
for bin_num, count in skin_dist.items():
    print(f"    Bin {bin_num}: {count} images ({count/len(v3)*100:.1f}%)")

print("\n🎭 CULTURAL CONTEXT:")
markers = v3['cultural_markers'].value_counts()
print(f"  V1/V2: No cultural markers")
print(f"  V3:    {len(markers)} distinct marker types")
print(f"    Most common: {markers.head(5).to_dict()}")

# ============================================================================
# SECTION 4: Fairness Metrics
# ============================================================================

print("\n" + "="*80)
print("SECTION 4: FAIRNESS IMPROVEMENTS")
print("="*80)

def calculate_representation_gaps(df, col='race_cat'):
    """Calculate max representation gap (fairness measure)"""
    counts = df[col].value_counts()
    max_gap = (counts.max() - counts.min()) / len(df)
    return max_gap

print("\n⚖️ REPRESENTATION GAPS:")
v1_gap = calculate_representation_gaps(v1)
v2_gap = calculate_representation_gaps(v2)
v3_gap = calculate_representation_gaps(v3)

print(f"  V1 max race gap: {v1_gap:.3f} ({v1_gap*100:.1f}% of dataset)")
print(f"  V2 max race gap: {v2_gap:.3f} ({v2_gap*100:.1f}% of dataset)")
print(f"  V3 max race gap: {v3_gap:.3f} ({v3_gap*100:.1f}% of dataset)")
print(f"\n  Improvement V1→V2: {(1-v2_gap/v1_gap)*100:.1f}% reduction in gap")
print(f"  Improvement V2→V3: {(1-v3_gap/v2_gap)*100:.1f}% change in gap")

print("\n🎯 EFFECTIVE REPRESENTATION (V3 advantage):")
# V3 allows multi-label, so effective representation is higher
all_races = []
for race_ml in v3['race_ml']:
    if pd.notna(race_ml):
        all_races.extend(str(race_ml).split('|'))
race_counter = Counter(all_races)
print(f"  With multi-label expansion:")
for race, count in race_counter.most_common():
    print(f"    {race:20s}: {count:4d} appearances")

print("\n🔍 SUBSET IDENTIFICATION CAPABILITY:")
print(f"  V1/V2: Can only filter by single demographic")
print(f"  V3:    Can filter by:")
print(f"    • Base demographics (like V1/V2)")
print(f"    • Confidence levels ({(v3['conf_race']<0.6).sum()} low-conf images)")
print(f"    • Uncertainty flags ({uncertain_count} uncertain images)")
print(f"    • Skin tone ranges (7 bins available)")
print(f"    • Cultural markers ({len(markers)-1} non-'none' types)")
print(f"    • Multi-identity cases ({multi_label_count} images)")

# ============================================================================
# SECTION 5: Use Case Scenarios
# ============================================================================

print("\n" + "="*80)
print("SECTION 5: PRACTICAL ADVANTAGES BY USE CASE")
print("="*80)

print("\n🤖 MODEL TRAINING:")
print("  V1/V2 Limitations:")
print("    • Models trained on single-label only")
print("    • No way to weight by confidence")
print("    • Ignores within-group diversity (skin tone)")
print("\n  V3 Advantages:")
print("    • Can train on multi-label (more realistic)")
print("    • Can weight samples by confidence scores")
print("    • Can stratify by skin tone for fairness")
print("    • Can exclude ethically sensitive cases")

print("\n📊 BIAS AUDITING:")
print("  V1/V2 Limitations:")
print("    • Can only measure error rates by broad category")
print("    • No understanding of confidence vs accuracy")
print("\n  V3 Advantages:")
print("    • Can correlate model errors with confidence")
print("    • Can identify bias across skin tone spectrum")
print("    • Can flag cases where humans are also uncertain")
print("    • Can analyze cultural marker impact")

print("\n⚠️ ETHICAL DEPLOYMENT:")
print("  V1/V2 Limitations:")
print("    • Forces classification even in ambiguous cases")
print("    • No mechanism to defer uncertain decisions")
print("\n  V3 Advantages:")
print("    • Can set confidence thresholds (e.g., require >0.7)")
print("    • Can route uncertain cases to human review")
print("    • Can respect prefer_not_to_label flags")
print("    • Transparent about limitations via annotation_notes")

# ============================================================================
# VISUALIZATION
# ============================================================================

print("\n" + "="*80)
print("GENERATING COMPARATIVE VISUALIZATIONS...")
print("="*80)

fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.3)

# 1. Race distribution comparison
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(v1_race))
width = 0.25
races = sorted(set(list(v1_race.index) + list(v2_race.index) + list(v3_race.index)))
v1_counts = [v1_race.get(r, 0) for r in races]
v2_counts = [v2_race.get(r, 0) for r in races]
v3_counts = [v3_race.get(r, 0) for r in races]

ax1.bar([i-width for i in range(len(races))], v1_counts, width, label='V1 (Original)', alpha=0.8, color='lightcoral')
ax1.bar([i for i in range(len(races))], v2_counts, width, label='V2 (Balanced)', alpha=0.8, color='skyblue')
ax1.bar([i+width for i in range(len(races))], v3_counts, width, label='V3 (Ethical)', alpha=0.8, color='lightgreen')
ax1.set_xlabel('Race Category')
ax1.set_ylabel('Count')
ax1.set_title('Race Distribution Comparison: V1 vs V2 vs V3', fontweight='bold', fontsize=13)
ax1.set_xticks(range(len(races)))
ax1.set_xticklabels(races, rotation=45, ha='right')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# 2. Balance Score Comparison
ax2 = fig.add_subplot(gs[1, 0])
balance_scores = [
    calculate_balance_score(v1),
    calculate_balance_score(v2),
    calculate_balance_score(v3)
]
colors_bal = ['lightcoral', 'skyblue', 'lightgreen']
bars = ax2.bar(['V1', 'V2', 'V3'], balance_scores, color=colors_bal, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Balance Score')
ax2.set_title('Dataset Balance Score\n(1.0 = Perfect Balance)', fontweight='bold')
ax2.set_ylim(0, 1)
ax2.grid(axis='y', alpha=0.3)
for bar, score in zip(bars, balance_scores):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
             f'{score:.3f}', ha='center', va='bottom', fontweight='bold')

# 3. Feature Count Comparison
ax3 = fig.add_subplot(gs[1, 1])
feature_counts = [len(v1.columns), len(v2.columns), len(v3.columns)]
colors_feat = ['lightcoral', 'skyblue', 'lightgreen']
bars = ax3.bar(['V1', 'V2', 'V3'], feature_counts, color=colors_feat, edgecolor='black', linewidth=1.5)
ax3.set_ylabel('Number of Features')
ax3.set_title('Feature Richness', fontweight='bold')
ax3.grid(axis='y', alpha=0.3)
for bar, count in zip(bars, feature_counts):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.3,
             f'{count}', ha='center', va='bottom', fontweight='bold', fontsize=12)

# 4. Representation Gap
ax4 = fig.add_subplot(gs[1, 2])
gaps = [v1_gap * 100, v2_gap * 100, v3_gap * 100]
colors_gap = ['lightcoral', 'skyblue', 'lightgreen']
bars = ax4.bar(['V1', 'V2', 'V3'], gaps, color=colors_gap, edgecolor='black', linewidth=1.5)
ax4.set_ylabel('Max Representation Gap (%)')
ax4.set_title('Fairness: Max Race Gap\n(Lower is Better)', fontweight='bold')
ax4.grid(axis='y', alpha=0.3)
for bar, gap in zip(bars, gaps):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{gap:.1f}%', ha='center', va='bottom', fontweight='bold')

# 5. V3 Multi-label breakdown
ax5 = fig.add_subplot(gs[2, 0])
multi_data = {
    'Single Label': len(v3) - multi_label_count,
    'Multi-Label': multi_label_count
}
colors_multi = ['lightblue', 'orange']
ax5.pie(multi_data.values(), labels=multi_data.keys(), autopct='%1.1f%%',
        colors=colors_multi, startangle=90, textprops={'fontweight': 'bold'})
ax5.set_title('V3: Multi-Label Support\n(Preserves Ambiguity)', fontweight='bold')

# 6. V3 Uncertainty breakdown
ax6 = fig.add_subplot(gs[2, 1])
uncertain_data = {
    'Certain': len(v3) - uncertain_count,
    'Uncertain': uncertain_count
}
colors_unc = ['lightgreen', 'salmon']
ax6.pie(uncertain_data.values(), labels=uncertain_data.keys(), autopct='%1.1f%%',
        colors=colors_unc, startangle=90, textprops={'fontweight': 'bold'})
ax6.set_title('V3: Uncertainty Quantification\n(Transparency)', fontweight='bold')

# 7. V3 Confidence distributions
ax7 = fig.add_subplot(gs[2, 2])
conf_race_clean = pd.to_numeric(v3['conf_race'], errors='coerce').dropna()
conf_gender_clean = pd.to_numeric(v3['conf_gender'], errors='coerce').dropna()
conf_skin_clean = pd.to_numeric(v3['conf_skin'], errors='coerce').dropna()
ax7.hist([conf_race_clean, conf_gender_clean, conf_skin_clean], bins=15, 
         label=['Race', 'Gender', 'Skin'], alpha=0.6, color=['coral', 'plum', 'khaki'])
ax7.set_xlabel('Confidence Score')
ax7.set_ylabel('Frequency')
ax7.set_title('V3: Confidence Distributions\n(Quality Measure)', fontweight='bold')
ax7.legend()
ax7.grid(axis='y', alpha=0.3)
ax7.axvline(0.6, color='red', linestyle='--', alpha=0.5, label='Uncertainty Threshold')

# 8. V3 Skin tone distribution
ax8 = fig.add_subplot(gs[3, 0])
skin_counts = v3['skin_tone_bin'].value_counts().sort_index()
ax8.bar(skin_counts.index, skin_counts.values, color='skyblue', edgecolor='black')
ax8.set_xlabel('Skin Tone Bin (1=dark, 7=light)')
ax8.set_ylabel('Count')
ax8.set_title('V3: Skin Tone Distribution\n(Within-Group Diversity)', fontweight='bold')
ax8.grid(axis='y', alpha=0.3)

# 9. V3 Cultural markers
ax9 = fig.add_subplot(gs[3, 1:])
top_markers = v3['cultural_markers'].value_counts().head(8)
ax9.barh(range(len(top_markers)), top_markers.values, color='teal', edgecolor='black')
ax9.set_yticks(range(len(top_markers)))
ax9.set_yticklabels(top_markers.index)
ax9.set_xlabel('Count')
ax9.set_title('V3: Cultural Markers\n(Contextual Information)', fontweight='bold')
ax9.grid(axis='x', alpha=0.3)

plt.suptitle('Dataset Evolution: V1 → V2 → V3\nFrom Basic Labeling to Ethical AI', 
             fontsize=16, fontweight='bold', y=0.995)

plt.savefig('Data/v1_v2_v3_comparison.png', dpi=300, bbox_inches='tight')
print("\n✅ Visualization saved to: Data/v1_v2_v3_comparison.png")

# ============================================================================
# SUMMARY TABLE
# ============================================================================

print("\n" + "="*80)
print("SUMMARY: WHY V3 IS BETTER FOR FAIRNESS")
print("="*80)

summary_data = {
    'Metric': [
        'Dataset Size',
        'Balance Score',
        'Feature Count',
        'Max Race Gap',
        'Multi-Label Support',
        'Uncertainty Tracking',
        'Confidence Scores',
        'Skin Tone Info',
        'Cultural Context',
        'Ethical Opt-Out'
    ],
    'V1': [
        len(v1),
        f"{calculate_balance_score(v1):.3f}",
        len(v1.columns),
        f"{v1_gap*100:.1f}%",
        '❌ No',
        '❌ No',
        '❌ No',
        '❌ No',
        '❌ No',
        '❌ No'
    ],
    'V2': [
        len(v2),
        f"{calculate_balance_score(v2):.3f}",
        len(v2.columns),
        f"{v2_gap*100:.1f}%",
        '❌ No',
        '❌ No',
        '❌ No',
        '❌ No',
        '❌ No',
        '❌ No'
    ],
    'V3': [
        len(v3),
        f"{calculate_balance_score(v3):.3f}",
        len(v3.columns),
        f"{v3_gap*100:.1f}%",
        f'✅ Yes ({multi_label_count})',
        f'✅ Yes ({uncertain_count})',
        '✅ Yes (3 types)',
        '✅ Yes (7 bins)',
        f'✅ Yes ({len(markers)} types)',
        f'✅ Yes ({v3["prefer_not_to_label"].astype(float).eq(1).sum()})'
    ]
}

summary_df = pd.DataFrame(summary_data)
print("\n" + summary_df.to_string(index=False))

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("""
V3 represents a significant advancement over V1 and V2:

1. BETTER REPRESENTATION: Multi-label support captures mixed identities
2. BETTER TRANSPARENCY: Confidence scores reveal uncertainty
3. BETTER FAIRNESS: Skin tone bins enable within-group analysis
4. BETTER CONTEXT: Cultural markers provide additional dimensions
5. BETTER ETHICS: Opt-out mechanism respects sensitive cases

These features enable:
• More accurate model training (weighted by confidence)
• More nuanced bias auditing (across multiple dimensions)
• More ethical deployment (defer low-confidence cases)
• More transparent research (document limitations)

V3 moves beyond demographic balancing to true ethical AI.
""")

print("="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
