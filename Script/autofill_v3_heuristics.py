#!/usr/bin/env python3
"""
V3 Ethical Metadata Auto-Fill Script

Generates ethical metadata for facial recognition datasets including:
- Multi-label race assignments
- Uncertainty quantification
- Confidence scores
- Skin tone bins
- Cultural markers

Author: Ethical Representation and Labeling Project
Date: November 2025
"""

import argparse
import random
import math
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False

FF_CLASSES = ["White","Black","EastAsian","SouthAsian","SoutheastAsian","MiddleEastern","Latino"]

ADJACENT_PAIRS = [
    ("MiddleEastern","SouthAsian"),
    ("EastAsian","SoutheastAsian"),
    ("Latino","White"),
    ("Latino","MiddleEastern"),
    ("SouthAsian","SoutheastAsian"),
]

def parse_args():
    ap = argparse.ArgumentParser(description="Heuristically auto-fill V3 ethical columns.")
    ap.add_argument("--in", dest="inp", default="./Data/labels_v3.csv", help="Input CSV (V3 scaffold or partial)")
    ap.add_argument("--out", dest="outp", default="./Data/labels_v3.csv", help="Output CSV (can be same as input)")
    ap.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    # rates
    ap.add_argument("--ambiguous-rate", type=float, default=0.15, help="Chance to make a 2-label race_ml for eligible classes")
    ap.add_argument("--uncertain-rate", type=float, default=0.10, help="Base chance to flag unknown_uncertain")
    ap.add_argument("--prefer-not-rate", type=float, default=0.01, help="Chance to set prefer_not_to_label=1")
    # confidence bands
    ap.add_argument("--hi-conf-range", type=str, default="0.80,1.00", help="Uniform range for confident cases")
    ap.add_argument("--mid-conf-range", type=str, default="0.55,0.80", help="Uniform range for mid/ambiguous cases")
    ap.add_argument("--lo-conf-range",  type=str, default="0.30,0.55", help="Uniform range for uncertain cases")
    ap.add_argument("--lowconf-threshold", type=float, default=0.60, help="Threshold used to set unknown_uncertain from conf_race")
    # skin tone
    ap.add_argument("--skin-tone-method", choices=["random","brightness"], default="random",
                    help="Random bins or rough brightness-based estimate (requires PIL, uses rel_path)")
    ap.add_argument("--skin-bins", type=int, default=7, help="Number of skin tone bins (bins labelled 1..N)")
    # cultural markers
    ap.add_argument("--marker-rate", type=float, default=0.12, help="Base chance to assign a non-'none' cultural marker")
    # behavior
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing values (otherwise only fill blanks)")
    ap.add_argument("--dry-run", action="store_true", help="Print summary only; do not write file")
    return ap.parse_args()

def urange(s):
    a,b = s.split(",")
    return float(a), float(b)

def safe_col(df, col, default=""):
    if col not in df.columns:
        df[col] = default
    return df

def choose_multilabel(rng, base_label, ambiguous_rate):
    # with some probability, turn into a 2-label if there's an adjacent pair match
    if base_label not in FF_CLASSES:
        return base_label
    # which pair(s) include this label?
    candidates = [tuple(sorted(p)) for p in ADJACENT_PAIRS if base_label in p]
    if candidates and rng.random() < ambiguous_rate:
        pair = rng.choice(candidates)
        a,b = pair
        # ensure base label present + one neighbor
        other = b if a == base_label else a
        return f"{base_label}|{other}"
    return base_label

def brightness_to_bin(img_path, bins=7):
    """Very rough: average brightness of a central crop -> bin 1..bins (1=dark, bins=light)."""
    if not PIL_OK:
        return None
    try:
        im = Image.open(img_path).convert("L")  # grayscale
        w,h = im.size
        if w<10 or h<10: return None
        # central crop
        cw, ch = max(8, int(w*0.6)), max(8, int(h*0.6))
        x0, y0 = (w-cw)//2, (h-ch)//2
        crop = im.crop((x0, y0, x0+cw, y0+ch))
        arr = np.asarray(crop, dtype=np.float32)
        bright = float(arr.mean()) / 255.0  # 0..1
        # map to bins 1..bins
        b = int(np.clip(math.floor(bright * bins) + 1, 1, bins))
        return b
    except Exception:
        return None

def main():
    args = parse_args()
    rng = random.Random(args.seed)
    np.random.seed(args.seed)

    loL, loH   = urange(args.lo_conf_range)
    midL, midH = urange(args.mid_conf_range)
    hiL, hiH   = urange(args.hi_conf_range)

    df = pd.read_csv(args.inp)
    
    # Ensure required columns exist
    for c in ["image_id","rel_path","race_cat","gender_cat","age_cat","split"]:
        df = safe_col(df, c, "")
    for c, default in [
        ("race_ml",""),
        ("skin_tone_bin",""),
        ("cultural_markers",""),
        ("ambiguous_mixed",""),
        ("prefer_not_to_label",""),
        ("unknown_uncertain",""),
        ("conf_race",""),
        ("conf_gender",""),
        ("conf_skin",""),
        ("annotation_notes",""),
    ]:
        df = safe_col(df, c, default)

    filled_counts = {k:0 for k in ["race_ml","ambiguous_mixed","unknown_uncertain","prefer_not_to_label","conf_race","skin_tone_bin","conf_skin","cultural_markers","conf_gender","annotation_notes"]}

    for i, row in df.iterrows():
        base_race = str(row.get("race_cat",""))
        # --- race_ml ---
        if args.overwrite or not str(row["race_ml"]).strip():
            ml = choose_multilabel(rng, base_race, args.ambiguous_rate)
            df.at[i,"race_ml"] = ml
            filled_counts["race_ml"] += 1
        else:
            ml = str(row["race_ml"])

        # --- ambiguous_mixed ---
        if args.overwrite or str(row["ambiguous_mixed"]).strip()=="":
            df.at[i,"ambiguous_mixed"] = 1 if "|" in ml else 0
            filled_counts["ambiguous_mixed"] += 1

        # --- prefer_not_to_label ---
        if args.overwrite or str(row["prefer_not_to_label"]).strip()=="":
            df.at[i,"prefer_not_to_label"] = 1 if rng.random() < args.prefer_not_rate else 0
            filled_counts["prefer_not_to_label"] += 1

        # --- conf_race & unknown_uncertain ---
        set_conf = False
        if args.overwrite or str(row["conf_race"]).strip()=="":
            if df.at[i,"prefer_not_to_label"] == 1:
                conf = rng.uniform(loL, loH)
            elif "|" in ml:
                conf = rng.uniform(midL, midH)
            else:
                # sometimes still uncertain
                conf = rng.uniform(hiL, hiH) if rng.random() > args.uncertain_rate else rng.uniform(loL, loH)
            df.at[i,"conf_race"] = round(conf, 3)
            filled_counts["conf_race"] += 1
            set_conf = True
        conf_val = float(df.at[i,"conf_race"]) if str(df.at[i,"conf_race"]).strip()!="" else 0.5

        if args.overwrite or str(row["unknown_uncertain"]).strip()=="":
            unk = 1 if (conf_val < args.lowconf_threshold or rng.random() < args.uncertain_rate) else 0
            df.at[i,"unknown_uncertain"] = unk
            filled_counts["unknown_uncertain"] += 1

        # --- cultural_markers (low-rate heuristics) ---
        if args.overwrite or not str(row["cultural_markers"]).strip():
            markers = []
            # modest priors by race/gender (purely heuristic; keep rates low)
            if base_race in ["MiddleEastern","SouthAsian"] and rng.random() < args.marker_rate:
                markers.append("religious_headwear")
            if str(row.get("gender_cat","")).lower() in ["male","m"] and rng.random() < args.marker_rate:
                markers.append("beard")
            if rng.random() < args.marker_rate/2:
                markers.append("piercing_visible")
            if not markers:
                markers = ["none"]
            df.at[i,"cultural_markers"] = "|".join(sorted(set(markers)))
            filled_counts["cultural_markers"] += 1

        # --- skin_tone_bin ---
        if args.overwrite or not str(row["skin_tone_bin"]).strip():
            bin_val = None
            if args.skin_tone_method == "brightness" and PIL_OK and str(row["rel_path"]).strip():
                img_path = Path(row["rel_path"])
                if not img_path.is_absolute():
                    # try common roots
                    for root in [Path("."), Path("data/images"), Path("data")]:
                        candidate = root / img_path
                        if candidate.exists():
                            img_path = candidate
                            break
                bin_val = brightness_to_bin(img_path, bins=args.skin_bins)
            if bin_val is None:
                # random but slightly skewed by race to avoid uniformity (very weak prior)
                # (NOTE: purely heuristic; adjust as needed)
                weights = {
                    "Black":[0.25,0.22,0.18,0.14,0.10,0.07,0.04],
                    "White":[0.04,0.07,0.10,0.14,0.18,0.22,0.25],
                }.get(base_race, [1/args.skin_bins]*args.skin_bins)
                choices = list(range(1, args.skin_bins+1))
                bin_val = int(np.random.choice(choices, p=np.array(weights)/np.sum(weights)))
            df.at[i,"skin_tone_bin"] = str(bin_val)
            filled_counts["skin_tone_bin"] += 1

        # --- conf_skin ---
        if args.overwrite or not str(row["conf_skin"]).strip():
            # higher confidence if brightness-based succeeded; else moderate
            if args.skin_tone_method == "brightness" and PIL_OK and df.at[i,"skin_tone_bin"] not in ["", "Unknown"]:
                df.at[i,"conf_skin"] = round(rng.uniform(0.6, 0.9), 3)
            else:
                df.at[i,"conf_skin"] = round(rng.uniform(0.5, 0.8), 3)
            filled_counts["conf_skin"] += 1

        # --- conf_gender ---
        if args.overwrite or not str(row["conf_gender"]).strip():
            g = str(row.get("gender_cat","")).strip().lower()
            if g in ["male","m","female","f"]:
                df.at[i,"conf_gender"] = round(rng.uniform(0.8, 1.0), 3)
            else:
                df.at[i,"conf_gender"] = round(rng.uniform(0.4, 0.7), 3)
            filled_counts["conf_gender"] += 1

        # --- annotation_notes (only for flagged cases) ---
        if args.overwrite or not str(row["annotation_notes"]).strip():
            notes = []
            if "|" in ml:
                notes.append("auto: multi-heritage heuristic")
            if df.at[i,"unknown_uncertain"] == 1:
                notes.append("auto: low confidence / uncertain")
            if df.at[i,"prefer_not_to_label"] == 1:
                notes.append("auto: prefer-not-to-label set")
            df.at[i,"annotation_notes"] = "; ".join(notes)
            if notes:
                filled_counts["annotation_notes"] += 1

    # Summary
    n = len(df)
    print("\n" + "="*80)
    print("AUTO-FILL SUMMARY")
    print("="*80)
    print(f"\nProcessed: {n} images")
    print("\nColumns filled:")
    for k,v in filled_counts.items():
        print(f"  {k:25s}: {v:4d} rows ({v/n:6.1%})")
    
    print("\n" + "="*80)
    print("ETHICAL METADATA STATISTICS")
    print("="*80)
    print("\nFlag rates:")
    print(f"  ambiguous_mixed=1     : {pd.to_numeric(df['ambiguous_mixed'], errors='coerce').fillna(0).astype(int).eq(1).mean():.2%} ({pd.to_numeric(df['ambiguous_mixed'], errors='coerce').fillna(0).astype(int).eq(1).sum():.0f} images)")
    print(f"  unknown_uncertain=1   : {pd.to_numeric(df['unknown_uncertain'], errors='coerce').fillna(0).astype(int).eq(1).mean():.2%} ({pd.to_numeric(df['unknown_uncertain'], errors='coerce').fillna(0).astype(int).eq(1).sum():.0f} images)")
    print(f"  prefer_not_to_label=1 : {pd.to_numeric(df['prefer_not_to_label'], errors='coerce').fillna(0).astype(int).eq(1).mean():.2%} ({pd.to_numeric(df['prefer_not_to_label'], errors='coerce').fillna(0).astype(int).eq(1).sum():.0f} images)")
    
    print("\nConfidence medians:")
    print(f"  conf_race             : {pd.to_numeric(df['conf_race'], errors='coerce').median():.3f}")
    print(f"  conf_gender           : {pd.to_numeric(df['conf_gender'], errors='coerce').median():.3f}")
    print(f"  conf_skin             : {pd.to_numeric(df['conf_skin'], errors='coerce').median():.3f}")

    if args.dry_run:
        print("\n" + "="*80)
        print("DRY RUN MODE - NO FILES WRITTEN")
        print("="*80)
        print("Use --overwrite to actually save the results.")
        return

    # Save output
    outp = Path(args.outp)
    outp.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        df.to_csv(outp, index=False)
        print("\n" + "="*80)
        print("SUCCESS!")
        print("="*80)
        print(f"✅ Saved: {outp}")
        print(f"📊 Dataset: {len(df)} images with {len(df.columns)} features")
        print("\n🚀 Next steps:")
        print("  • Run: python Script/visualize_v3_results.py")
        print("  • Run: python Script/compare_v1_v2_v3.py")
    except Exception as e:
        print(f"\n❌ Error saving file: {e}")
        sys.exit(1)

def main():
    """Main entry point"""
    try:
        args = parse_args()
        generate_v3_metadata(args)
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

def generate_v3_metadata(args):
    """Generate V3 ethical metadata with given arguments"""
    print("="*80)
    print("V3 ETHICAL METADATA GENERATOR")
    print("="*80)
    print(f"Input:  {args.inp}")
    print(f"Output: {args.outp}")
    print(f"Seed:   {args.seed}")
    print(f"Mode:   {'OVERWRITE' if args.overwrite else 'FILL_BLANKS'}")
    
    # Load and validate input
    if not Path(args.inp).exists():
        raise FileNotFoundError(f"Input file not found: {args.inp}")
    
    main_logic(args)  # Your existing main() logic

if __name__ == "__main__":
    main()
