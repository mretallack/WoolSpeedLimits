# Wool 20mph Speed Limit Experiments & Non-Vehicle Modeling Report

This document outlines the experimental setup, simulation configurations, statistical output collection, and non-vehicle (pedestrian/railway) modeling designed to test the claims and assumptions in the [Wool Speed Limit Wiki](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit).

---

## Summary of Scenarios

The canonical comparison pairs (survey-calibrated demand, see
`FLOW_CALIBRATION.md`) are:

1. **Peak (08:00, controlled)** — routes `wool.rou.dft_controlled.v2.xml`
   - 30mph baseline: `wool.dft_now.sumo.cfg` (network `wool.net.xml`)
   - 20mph scheme:  `wool.dft_20mph.sumo.cfg` (network `wool.20mph.net.xml`)

2. **Off-peak** — routes `wool.rou.dft_offpeak.v2.xml`
   - 30mph baseline: `wool.dft_offpeak_now.sumo.cfg`
   - 20mph scheme:  `wool.dft_offpeak_20mph.sumo.cfg`

The 20mph network reduces back roads, **Colliers Lane** and **Lulworth Road** to
20mph / 8.94 m/s; **Dorchester Road** is excluded and retained at 30mph. Both
scenarios use the same heterogeneous driver mix (compliant / normal / speeder).

> The earlier `wool.stats_now` / `wool.stats_20mph` configs and the
> `wool.rou.speed_experiment.xml` route file are **superseded** by the pairs
> above and are retained only for historical reference.

---

## 1. How to Generate Video Visualizations

Pre-rendered videos of the corrected scenarios live in `sumo/`:
`wool_peak_30mph.webm`, `wool_peak_20mph.webm`, `wool_offpeak_30mph.webm`,
`wool_offpeak_20mph.webm`.

To re-record in SUMO-GUI, use `sumo/render_sync.sh <config> <output.webm> [secs] [delay]`
(headless via Xvfb + ffmpeg), or interactively:

### Running the scenarios in GUI
```bash
cd sumo
sumo-gui -c wool.dft_now.sumo.cfg            # peak 30mph
sumo-gui -c wool.dft_20mph.sumo.cfg          # peak 20mph
sumo-gui -c wool.dft_offpeak_now.sumo.cfg    # off-peak 30mph
sumo-gui -c wool.dft_offpeak_20mph.sumo.cfg  # off-peak 20mph
```
*(In SUMO-GUI, use the recording toolbar or camera icon to export frames/video.)*

> **Note:** SUMO-GUI crashes on this host if a vType sets
> `device.rerouting.probability="0.0"`. That attribute has been removed from the
> route files (results are identical without it). See `FLOW_CALIBRATION.md`.

---

## 2. Statistical Analysis & Emissions

SUMO records trip statistics and pollutant emissions. **Emissions are deliberately
collected at two different levels**, because a change to the speed limit can push
them in *opposite* directions depending on the level of aggregation (see §2.1).

### Running Automated Batch Simulations & Stats Export
```bash
cd WoolSimulation/sumo
# Peak (controlled demand)
sumo -c wool.dft_now.sumo.cfg        # 30mph baseline
sumo -c wool.dft_20mph.sumo.cfg      # 20mph scheme
# Off-peak
sumo -c wool.dft_offpeak_now.sumo.cfg
sumo -c wool.dft_offpeak_20mph.sumo.cfg
```

Each config now produces **both**:
- **Road-level** emissions — `wool.dft_<scenario>.road_emissions.xml`
  (`edgeData type="emissions"`, per edge per 60 s, defined in
  `wool.stats.<scenario>.additional.xml`).
- **Vehicle-level** emissions — `wool.dft_<scenario>.emissions.xml`
  (`<emission-output>`, per-vehicle per timestep).

### Key Statistical Metrics Collected
- **Trip Statistics (`<scenario>.tripinfo.xml` / `<scenario>.statistic.xml`)**:
  - Average travel duration and time loss.
  - Waiting times at junctions and railway level crossings (`joinedS_0`).
  - Route lengths and vehicle throughput.
- **Emissions & Fuel Consumption** — collected at both road level
  (`wool.dft_<scenario>.road_emissions.xml`) and vehicle level
  (`wool.dft_<scenario>.emissions.xml`):
  - CO2, CO, PMx (particulate matter), NOx, HC and fuel consumption.

### Analysis Tool: `analyze_emissions.py`
Compare any two scenario runs across **all four views** in one command:

```bash
cd WoolSimulation/sumo
python3 analyze_emissions.py \
  --now-edge   wool.dft_offpeak_now.road_emissions.xml \
  --now-veh    wool.dft_offpeak_now.emissions.xml \
  --now-trip   wool.dft_offpeak_now.tripinfo.xml \
  --scheme-edge wool.dft_offpeak_20mph.road_emissions.xml \
  --scheme-veh  wool.dft_offpeak_20mph.emissions.xml \
  --scheme-trip wool.dft_offpeak_20mph.tripinfo.xml \
  --label-now "offpeak 30mph" --label-scheme "offpeak 20mph" \
  --csv results_offpeak.csv
```
(swap the `dft_offpeak_*` names for `dft_now` / `dft_20mph` for the peak-hour pair).

### 2.1 Measured Emissions — Road-Level vs Vehicle-Level

> **Note (revised):** these figures supersede an earlier set that was produced
> from a **saturated** demand scenario (1,470 veh/hr, ~39% above the measured
> A352 flow). That over-loading inverted the peak-hour result. See
> `FLOW_CALIBRATION.md` for the audit and `wool.rou.dft_controlled.v2.xml` for
> the corrected demand. All numbers below are from the corrected runs
> (1,382 veh/hr, 0 teleports, all vehicles inserted).

**Why both levels matter.** A vehicle travelling at 20mph instead of 30mph emits a
similar mass **per second** but occupies each road segment for **~50% longer**.
For a *vehicle*, that is a near-wash or a small saving; for a *road section*, the
longer occupancy can push the **accumulated total up**. Reporting only one level
(as the original report did) is therefore misleading. `analyze_emissions.py`
reports:
- **road_total** — total mass on all edges (Δ = what a *street/network* experiences)
- **vehicle_total** — total mass over all trips
- **vehicle_perkm** — mass per km driven (Δ = is the *average km* cleaner)

**% change under the 20mph scheme (peak hour, corrected demand):**

| Metric | road_total | vehicle_total | vehicle_perkm |
|---|---|---|---|
| CO2  | −3.50% | −3.35% | −2.19% |
| NOx  | −3.25% | −3.18% | −2.01% |
| PMx  | −3.30% | −3.23% | −2.07% |
| CO   | −6.76% | −6.65% | −5.52% |
| HC   | −3.16% | −2.97% | −1.80% |
| fuel | −3.50% | −3.35% | −2.19% |

**% change under the 20mph scheme (off-peak, corrected demand):**

| Metric | road_total | vehicle_total | vehicle_perkm |
|---|---|---|---|
| CO2  | +0.11% | +0.09% | +0.55% |
| NOx  | +0.37% | +0.34% | +0.80% |
| PMx  | +0.61% | +0.61% | +1.07% |
| CO   | −2.51% | −2.46% | −2.01% |
| HC   | +0.79% | +0.60% | +1.06% |
| fuel | +0.11% | +0.09% | +0.55% |

**Interpretation (revised — supports Hypothesis 1):**

- **Peak**: with corrected (survey-matched) demand, the 20mph scheme **reduces**
  emissions at every level — approximately **−3% to −7%**. Lowering the limit
  smooths the peak and cuts stop-start and queuing.
- **Off-peak**: the change is negligible (≤1%), i.e. **no penalty** from the
  scheme at free-flow. CO falls slightly (−2.5%); other pollutants are within
  noise.
- Net: this now **supports Hypothesis 1** — 20mph does not increase pollution and
  reduces it under peak conditions.
- **Critical caveat:** this conclusion is *demand-dependent*. The earlier
  saturated scenario (1,470 veh/hr) reversed it (+3–6%). Any future re-run must
  use the calibrated demand in `FLOW_CALIBRATION.md` or the sign of the result
  cannot be trusted.

**Effect of the flow correction on the peak result:**

| Metric (road_total) | saturated (old) | corrected (new) |
|---|---|---|
| CO2  | +3.63% | −3.50% |
| NOx  | +5.86% | −3.25% |
| PMx  | +2.94% | −3.30% |
| fuel | +3.64% | −3.50% |

The over-loaded demand inverted the sign of the peak-hour emissions conclusion.

---

## 3. Non-Vehicle Modeling & Railway Level Crossing Integration

The Wool SUMO model incorporates the village railway line and level crossing timings (`wool.additional-6-9-2016.xml`), which periodically close for passing trains (`Train 1W96`, `Train 1W51`, etc.).

### Proposed Non-Vehicle & Active Travel Experiments in SUMO
1. **Pedestrian Crossing & Walkability Flows (`wool.pedestrians.additional.xml`)**:
   - Models pedestrian flow (`personFlow`) from residential areas toward the village center and railway station.
   - Evaluates how lower vehicle speeds (20mph on back roads) impact pedestrian safety, crossing wait times, and multimodal interaction.
2. **Level Crossing Queue Interaction**:
   - When the railway gates close, vehicles and pedestrians queue up along the primary and back routes.
   - Slower vehicle speeds (20mph) reduce harsh braking events and smoother acceleration queues when crossing barriers reopen, mitigating stop-start particulate emissions (PMx).


## Note on Movie/Simulation Rating & Visuals
- **Observation**: The simulation color scheme (by speed or emissions) features vibrant red tones for high speeds or congestion, which can visually resemble high-contrast alert indicators.
- **Action Item**: Implement a refined movie/simulation rating and color-grading scheme to provide clearer, less visually jarring differentiation between compliant traffic (green), normal traffic, and speeders (muted tones) in future video exports.
