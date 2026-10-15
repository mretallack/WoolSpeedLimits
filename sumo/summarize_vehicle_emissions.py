#!/usr/bin/env python3
"""
summarize_vehicle_emissions.py — Emit a compact per-vehicle emissions CSV from a
SUMO `--emission-output` file, so the vehicle-level results can be checked
without the multi-hundred-MB raw file.

For every vehicle it writes one row with the trip totals plus its route length
(from the matching tripinfo file, if supplied), so the outputs of
`analyze_emissions.py` (vehicle_total and vehicle_perkm) can be re-derived.

Usage:
  python3 summarize_vehicle_emissions.py \
      --emissions wool.dft_now.emissions.xml \
      --tripinfo  wool.dft_now.tripinfo.xml \
      --out       wool.dft_now.vehicle_emissions.csv
"""
import argparse
import csv
import xml.etree.ElementTree as ET
from collections import defaultdict

KEYS = ["CO2", "NOx", "PMx", "CO", "HC", "fuel"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--emissions", required=True)
    ap.add_argument("--tripinfo")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    # Sum per-timestep records over each vehicle's whole trip.
    per_veh = defaultdict(lambda: defaultdict(float))
    noise = defaultdict(list)
    vtype = {}
    for v in ET.parse(args.emissions).getroot().iter("vehicle"):
        vid = v.get("id")
        vtype[vid] = v.get("type", "")
        for k in KEYS:
            per_veh[vid][k] += float(v.get(k, 0.0))
        if v.get("noise") is not None:
            noise[vid].append(float(v.get("noise")))

    # Route length per vehicle (metres) from tripinfo.
    lengths = {}
    if args.tripinfo:
        for t in ET.parse(args.tripinfo).getroot().iter("tripinfo"):
            lengths[t.get("id")] = float(t.get("routeLength", 0.0))

    cols = ["vehicle_id", "type", "route_length_m", "route_length_km",
            "noise_mean_dBA"] + [f"{k}_abs" for k in KEYS]
    with open(args.out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for vid, vals in per_veh.items():
            rl = lengths.get(vid, 0.0)
            nm = sum(noise[vid]) / len(noise[vid]) if noise.get(vid) else ""
            w.writerow([vid, vtype.get(vid, ""), f"{rl:.2f}", f"{rl/1000:.6f}",
                        f"{nm:.4f}" if nm != "" else ""] +
                       [f"{vals[k]:.6f}" for k in KEYS])
    print(f"wrote {args.out}: {len(per_veh)} vehicles")


if __name__ == "__main__":
    main()
