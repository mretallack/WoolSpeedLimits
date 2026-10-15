#!/usr/bin/env python3
"""
analyze_noise.py — Summarise vehicle noise from SUMO `--emission-output`.

SUMO's HBEFA noise model attaches a `noise` value (dB(A)) to every vehicle
timestep in the emission output. This script aggregates it two ways:

  * fleet_mean_dBA   — mean over all vehicle-timesteps (network-weighted)
  * per_veh_mean_dBA — mean of each vehicle's time-averaged noise (vehicle-weighted)

Use it to test the "20mph reduces noise" claim (wiki section 3.3).  Note that
SUMO's noise model is dominated by vehicle class and acceleration, so a modest
speed-cap change typically yields only a small effect.

Usage:
  python3 analyze_noise.py --now wool.dft_now.emissions.xml \
                           --scheme wool.dft_20mph.emissions.xml \
                           [--label-now "30mph" --label-scheme "20mph"]
"""
import argparse
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict


def noise_stats(path):
    root = ET.parse(path).getroot()
    per_veh = defaultdict(list)
    for v in root.iter("vehicle"):
        n = v.get("noise")
        if n is not None:
            per_veh[v.get("id")].append(float(n))
    all_ts = [x for ts in per_veh.values() for x in ts]
    veh_means = [sum(ts) / len(ts) for ts in per_veh.values() if ts]
    return {
        "n_veh": len(veh_means),
        "fleet_mean": sum(all_ts) / len(all_ts) if all_ts else float("nan"),
        "per_veh_mean": sum(veh_means) / len(veh_means) if veh_means else float("nan"),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--now", required=True, help="emission-output file for the 30mph baseline")
    ap.add_argument("--scheme", required=True, help="emission-output file for the 20mph scheme")
    ap.add_argument("--label-now", default="30mph")
    ap.add_argument("--label-scheme", default="20mph")
    args = ap.parse_args()

    a = noise_stats(args.now)
    b = noise_stats(args.scheme)

    print(f"\n=== VEHICLE NOISE (dB(A)): {args.label_now} -> {args.label_scheme} ===")
    print(f"{'metric':18s}{args.label_now:>16s}{args.label_scheme:>16s}{'delta dB(A)':>14s}")
    for key, label in [("fleet_mean", "fleet_mean_dBA"), ("per_veh_mean", "per_veh_mean_dBA")]:
        d = b[key] - a[key]
        print(f"{label:18s}{a[key]:16.2f}{b[key]:16.2f}{d:+14.2f}")
    print(f"\nvehicles: {a['n_veh']} vs {b['n_veh']}")
    print("Note: a ~3 dB(A) change is perceived as roughly halving loudness.")


if __name__ == "__main__":
    main()
