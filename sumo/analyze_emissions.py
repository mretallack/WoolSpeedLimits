#!/usr/bin/env python3
"""
analyze_emissions.py — Compare vehicle-level and road-level emissions between
two SUMO scenario runs (e.g. 30mph baseline "now" vs 20mph scheme).

Why this exists
---------------
SUMO can report emissions at two fundamentally different levels, and they can
move in DIFFERENT directions when a speed limit changes:

  * ROAD-level  (`edgeData type="emissions"`)  -> total mass deposited on each
    road edge over the run. This answers: "does this street/network get cleaner?"

  * VEHICLE-level (`--emission-output`)        -> per-vehicle mass, summed over
    each vehicle's whole trip. From this we derive:
      - total      : "does the whole fleet pollute less?"
      - per-vehicle: "does an average driver pollute less?"
      - per-km     : "is the average km travelled cleaner?"

A car travelling slower often emits less per second, but spends longer on the
road, so road-level totals can RISE while per-km vehicle emissions FALL.
Reporting only one level is misleading; this script reports all four views.

Usage
-----
  python3 analyze_emissions.py \
      --now-edge  emis_now.xml      --now-veh  veh_now.xml      --now-trip trip_now.xml \
      --scheme-edge emis_20.xml     --scheme-veh veh_20.xml     --scheme-trip trip_20.xml \
      [--label-now "30mph" --label-scheme "20mph"] [--csv results.csv]

Both --*-edge (edgeData emissions) and --*-veh (--emission-output) are optional
per side, but at least one pair must be supplied for a comparison row.

The vehicles are matched to their trip route length via the tripinfo id so that
per-km figures are accurate.
"""

import argparse
import csv
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

# Pollutants + fuel we track. Kept explicit so the output ordering is stable.
KEYS = ["CO2", "NOx", "PMx", "CO", "HC", "fuel"]


def _fmt_pct(a, b):
    """Percent change from a to b, guarded against divide-by-zero."""
    if a == 0:
        return float("nan")
    return (b - a) / a * 100.0


# --------------------------------------------------------------------------
# Road-level: parse an edgeData emissions file (values with _abs suffix).
# --------------------------------------------------------------------------
def road_totals(path):
    root = ET.parse(path).getroot()
    tot = defaultdict(float)
    for interval in root.findall("interval"):
        for edge in interval.findall("edge"):
            for k, v in edge.attrib.items():
                if k.endswith("_abs"):
                    try:
                        tot[k[:-4]] += float(v)
                    except ValueError:
                        pass
    return tot


# --------------------------------------------------------------------------
# Vehicle-level: sum --emission-output per-timestep records over whole trips.
# --------------------------------------------------------------------------
def vehicle_totals(path):
    root = ET.parse(path).getroot()
    per_veh = defaultdict(lambda: defaultdict(float))
    for v in root.iter("vehicle"):
        vid = v.get("id")
        for k in KEYS:
            per_veh[vid][k] += float(v.get(k, 0.0))
    return per_veh


def trip_route_lengths(path):
    """id -> routeLength (metres) from a tripinfo file."""
    root = ET.parse(path).getroot()
    return {t.get("id"): float(t.get("routeLength", 0.0)) for t in root.iter("tripinfo")}


def vehicle_summary(veh_path, trip_path):
    per_veh = vehicle_totals(veh_path)
    lengths = trip_route_lengths(trip_path) if trip_path else {}
    n = len(per_veh)
    tot = defaultdict(float)
    km_total = 0.0
    for vid, vals in per_veh.items():
        for k in KEYS:
            tot[k] += vals[k]
        km_total += lengths.get(vid, 0.0) / 1000.0
    if km_total == 0.0:
        km_total = float("nan")
    return {
        "n": n,
        "km": km_total,
        "total": tot,
        "per_veh": {k: tot[k] / n if n else float("nan") for k in KEYS},
        "per_km": {k: tot[k] / km_total for k in KEYS},
    }


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------
def print_comparison(rows, label_now, label_scheme):
    """rows: list of (view_name, now_value, scheme_value)."""
    print(f"\n=== EMISSIONS: {label_now}  ->  {label_scheme}  (% change) ===")
    print(f"{'view':22s}{'metric':8s}{label_now:>18s}{label_scheme:>18s}{'change':>12s}")
    for view, a, b in rows:
        if a == b is None:
            continue
        pct = _fmt_pct(a, b)
        print(f"{view:22s}{'':8s}{a:18.1f}{b:18.1f}{pct:11.2f}%")


def build_rows(now_road, scheme_road, now_veh, scheme_veh):
    rows = []
    if now_road and scheme_road:
        for k in KEYS:
            rows.append(("road_total/" + k, now_road[k], scheme_road[k]))
    if now_veh and scheme_veh:
        for k in KEYS:
            rows.append(("vehicle_total/" + k, now_veh["total"][k], scheme_veh["total"][k]))
        for k in KEYS:
            rows.append(("vehicle_perkm/" + k, now_veh["per_km"][k], scheme_veh["per_km"][k]))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--now-edge")
    ap.add_argument("--now-veh")
    ap.add_argument("--now-trip")
    ap.add_argument("--scheme-edge")
    ap.add_argument("--scheme-veh")
    ap.add_argument("--scheme-trip")
    ap.add_argument("--label-now", default="now(30mph)")
    ap.add_argument("--label-scheme", default="scheme(20mph)")
    ap.add_argument("--csv")
    args = ap.parse_args()

    now_road = road_totals(args.now_edge) if args.now_edge else None
    scheme_road = road_totals(args.scheme_edge) if args.scheme_edge else None
    now_veh = vehicle_summary(args.now_veh, args.now_trip) if args.now_veh else None
    scheme_veh = vehicle_summary(args.scheme_veh, args.scheme_trip) if args.scheme_veh else None

    if now_veh:
        print(f"[{args.label_now}] vehicles={now_veh['n']}  total_km={now_veh['km']:,.1f}")
    if scheme_veh:
        print(f"[{args.label_scheme}] vehicles={scheme_veh['n']}  total_km={scheme_veh['km']:,.1f}")

    rows = build_rows(now_road, scheme_road, now_veh, scheme_veh)
    if not rows:
        sys.exit("No data supplied: provide at least --now-veh/--scheme-veh or --now-edge/--scheme-edge.")

    print_comparison(rows, args.label_now, args.label_scheme)

    if args.csv:
        with open(args.csv, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["view_metric", f"{args.label_now}", f"{args.label_scheme}", "pct_change"])
            for view, a, b in rows:
                w.writerow([view, a, b, _fmt_pct(a, b)])
        print(f"\nWrote {args.csv}")


if __name__ == "__main__":
    main()
