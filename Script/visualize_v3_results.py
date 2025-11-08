import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the V3 dataset
v3 = pd.read_csv("Data/labels_v3.csv")

print("="*60)
print("V3 ETHICAL LABELING DATASET SUMMARY")
print("="*60)
print(f"\nTotal images: {len(v3)}")
print(f"\nSource datasets:")
print(v3['source_dataset'].value_counts())

print("\n" + "="*60)
print("ETHICAL METADATA STATISTICS")
print("="*60)

# Flag statistics
print(f"\n📊 Flag Rates:")
print(f"  Ambiguous/Mixed Identity: {v3['ambiguous_mixed'].astype(float).eq(1).mean():.2%} ({v3['ambiguous_mixed'].astype(float).eq(1).sum():.0f} images)")
print(f"  Unknown/Uncertain:        {v3['unknown_uncertain'].astype(float).eq(1).mean():.2%} ({v3['unknown_uncertain'].astype(float).eq(1).sum():.0f} images)")
print(f"  Prefer Not to Label:      {v3['prefer_not_to_label'].astype(float).eq(1).mean():.2%} ({v3['prefer_not_to_label'].astype(float).eq(1).sum():.0f} images)")

# Confidence statistics
print(f"\n🎯 Confidence Medians:")
print(f"  Race:   {pd.to_numeric(v3['conf_race'], errors='coerce').median():.3f}")
print(f"  Gender: {pd.to_numeric(v3['conf_gender'], errors='coerce').median():.3f}")
print(f"  Skin:   {pd.to_numeric(v3['conf_skin'], errors='coerce').median():.3f}")

# Multi-label analysis
multi_labels = v3['race_ml'].str.contains('\\|', na=False).sum()
print(f"\n🏷️  Multi-label Race Assignments: {multi_labels} ({multi_labels/len(v3):.2%})")

# Cultural markers
markers = v3['cultural_markers'].value_counts().head(10)
print(f"\n🎭 Cultural Markers (Top 10):")
for marker, count in markers.items():
    print(f"  {marker}: {count} ({count/len(v3):.2%})")

# Skin tone distribution
print(f"\n🌈 Skin Tone Distribution:")
skin_counts = v3['skin_tone_bin'].value_counts().sort_index()
for tone, count in skin_counts.items():
    print(f"  Bin {tone}: {count} ({count/len(v3):.2%})")

# Visualization
print("\n" + "="*60)
print("GENERATING VISUALIZATIONS...")
print("="*60)

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1. Skin Tone Distribution
ax1 = fig.add_subplot(gs[0, 0])
v3['skin_tone_bin'].astype(float).plot(kind='hist', bins=7, ax=ax1, color='skyblue', edgecolor='black')
ax1.set_title('Skin Tone Distribution', fontsize=12, fontweight='bold')
ax1.set_xlabel('Skin Tone Bin (1=dark, 7=light)')
ax1.set_ylabel('Frequency')
ax1.grid(axis='y', alpha=0.3)

# 2. Race Confidence Distribution
ax2 = fig.add_subplot(gs[0, 1])
pd.to_numeric(v3['conf_race'], errors='coerce').plot(kind='hist', bins=20, ax=ax2, color='coral', edgecolor='black')
ax2.set_title('Race Confidence Distribution', fontsize=12, fontweight='bold')
ax2.set_xlabel('Confidence Score')
ax2.set_ylabel('Frequency')
ax2.axvline(0.6, color='red', linestyle='--', alpha=0.5, label='Uncertainty Threshold')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# 3. Ambiguous/Mixed Flag
ax3 = fig.add_subplot(gs[0, 2])
v3['ambiguous_mixed'].astype(float).value_counts().plot(kind='bar', ax=ax3, color=['lightgreen', 'orange'])
ax3.set_title('Ambiguous/Mixed Identity', fontsize=12, fontweight='bold')
ax3.set_xlabel('Flag Value')
ax3.set_ylabel('Count')
ax3.set_xticklabels(['Clear (0)', 'Mixed (1)'], rotation=0)
ax3.grid(axis='y', alpha=0.3)

# 4. Gender Confidence Distribution
ax4 = fig.add_subplot(gs[1, 0])
pd.to_numeric(v3['conf_gender'], errors='coerce').plot(kind='hist', bins=20, ax=ax4, color='plum', edgecolor='black')
ax4.set_title('Gender Confidence Distribution', fontsize=12, fontweight='bold')
ax4.set_xlabel('Confidence Score')
ax4.set_ylabel('Frequency')
ax4.grid(axis='y', alpha=0.3)

# 5. Skin Confidence Distribution
ax5 = fig.add_subplot(gs[1, 1])
pd.to_numeric(v3['conf_skin'], errors='coerce').plot(kind='hist', bins=20, ax=ax5, color='khaki', edgecolor='black')
ax5.set_title('Skin Tone Confidence Distribution', fontsize=12, fontweight='bold')
ax5.set_xlabel('Confidence Score')
ax5.set_ylabel('Frequency')
ax5.grid(axis='y', alpha=0.3)

# 6. Unknown/Uncertain Flag
ax6 = fig.add_subplot(gs[1, 2])
v3['unknown_uncertain'].astype(float).value_counts().plot(kind='bar', ax=ax6, color=['lightblue', 'salmon'])
ax6.set_title('Unknown/Uncertain Flag', fontsize=12, fontweight='bold')
ax6.set_xlabel('Flag Value')
ax6.set_ylabel('Count')
ax6.set_xticklabels(['Certain (0)', 'Uncertain (1)'], rotation=0)
ax6.grid(axis='y', alpha=0.3)

# 7. Cultural Markers Distribution
ax7 = fig.add_subplot(gs[2, :2])
top_markers = v3['cultural_markers'].value_counts().head(8)
top_markers.plot(kind='barh', ax=ax7, color='teal')
ax7.set_title('Top Cultural Markers', fontsize=12, fontweight='bold')
ax7.set_xlabel('Count')
ax7.set_ylabel('Marker Type')
ax7.grid(axis='x', alpha=0.3)

# 8. Confidence Comparison by Category
ax8 = fig.add_subplot(gs[2, 2])
conf_data = {
    'Race': pd.to_numeric(v3['conf_race'], errors='coerce').median(),
    'Gender': pd.to_numeric(v3['conf_gender'], errors='coerce').median(),
    'Skin': pd.to_numeric(v3['conf_skin'], errors='coerce').median()
}
plt.bar(conf_data.keys(), conf_data.values(), color=['coral', 'plum', 'khaki'], edgecolor='black')
ax8.set_title('Median Confidence by Category', fontsize=12, fontweight='bold')
ax8.set_ylabel('Median Confidence')
ax8.set_ylim(0, 1)
ax8.grid(axis='y', alpha=0.3)
for i, (k, v) in enumerate(conf_data.items()):
    ax8.text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')

plt.suptitle('V3 Ethical Labeling Dataset Analysis', fontsize=16, fontweight='bold', y=0.995)

# Save figure
plt.savefig('Data/v3_ethical_analysis.png', dpi=300, bbox_inches='tight')
print("\n✅ Visualization saved to: Data/v3_ethical_analysis.png")
plt.show()

print("\n" + "="*60)
print("ANALYSIS COMPLETE!")
print("="*60)
