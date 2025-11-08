#!/usr/bin/env python3
"""
Manual Annotation Tool for V3 Validation Subset

This script helps you manually annotate the 136 images in v3_manual_subset.csv
to validate the heuristic approach used in the full V3 dataset.

Usage:
    python Script/complete_manual_validation.py
"""

import pandas as pd
import os
from pathlib import Path

# Configuration
MANUAL_SUBSET = "Data/v3_manual_subset.csv"
OUTPUT_FILE = "Data/v3_manual_annotated.csv"

def main():
    # Load the subset
    df = pd.read_csv(MANUAL_SUBSET)
    
    print("="*80)
    print("V3 MANUAL VALIDATION TOOL")
    print("="*80)
    print(f"\nTotal images to annotate: {len(df)}")
    print(f"Images per race category:")
    print(df['race_cat'].value_counts())
    
    # Check which images already have annotations
    annotated = df['race_ml'].notna().sum()
    remaining = len(df) - annotated
    
    print(f"\nAlready annotated: {annotated}")
    print(f"Remaining: {remaining}")
    
    if remaining > 0:
        print("\n" + "="*80)
        print("NEXT STEPS FOR MANUAL ANNOTATION:")
        print("="*80)
        print("""
1. Open the images in Data/FairFace/ and Data/UTKFace/ directories
2. For each image in v3_manual_subset.csv, manually annotate:
   
   a) race_ml: 
      - Single label: "Black", "White", "EastAsian", etc.
      - Multi-label: "Latino|White", "EastAsian|SoutheastAsian", etc.
   
   b) ambiguous_mixed: 1 if multi-label, 0 otherwise
   
   c) unknown_uncertain: 1 if you're uncertain about race/gender, 0 otherwise
   
   d) conf_race: Your confidence (0.0-1.0) in the race assignment
   
   e) conf_gender: Your confidence (0.0-1.0) in the gender assignment
   
   f) skin_tone_bin: 1 (darkest) to 7 (lightest)
   
   g) conf_skin: Your confidence (0.0-1.0) in the skin tone
   
   h) cultural_markers: "none" or "beard", "piercing_visible", 
      "religious_headwear", etc. (use | for multiple)
   
   i) annotation_notes: Any notes about difficult cases

3. Once complete, run comparison analysis:
   python Script/compare_manual_vs_heuristic.py

TIP: Annotate in batches of 20-30 images at a time to avoid fatigue
TIP: Focus on uncertain/ambiguous cases first - these are most valuable
        """)
    
    # Create annotation template if needed
    if remaining == len(df):
        print("\nCreating annotation template with example values...")
        # Show first few rows as examples
        print("\nFirst 3 images to annotate:")
        for idx in range(min(3, len(df))):
            row = df.iloc[idx]
            print(f"\n{idx+1}. Image: {row['image_id']}")
            print(f"   Path: {row['rel_path']}")
            print(f"   Current race_cat: {row['race_cat']}")
            print(f"   Current gender_cat: {row['gender_cat']}")
            print("   → You need to fill: race_ml, ambiguous_mixed, unknown_uncertain, etc.")

if __name__ == "__main__":
    main()
