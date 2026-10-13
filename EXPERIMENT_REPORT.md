# Wool 20mph Speed Limit Experiments & Non-Vehicle Modeling Report

This document outlines the experimental setup, simulation configurations, statistical output collection, and non-vehicle (pedestrian/railway) modeling designed to test the claims and assumptions in the [Wool Speed Limit Wiki](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit).

---

## Summary of Scenarios

1. **"Now" (30mph Baseline)**
   - Config file: `wool.stats_now.sumo.cfg`
   - Network: `wool.net.xml` (standard speed limits, with residential/back roads at 30mph).
   - Traffic mix: Heterogeneous driver behavior (`wool.rou.speed_experiment.xml` containing compliant drivers, normal drivers, and speeders).

2. **"With 20mph" (Proposed Scheme)**
   - Config file: `wool.stats_20mph.sumo.cfg`
   - Network: `wool.20mph.net.xml` (back roads, **Colliers Lane**, and **Lulworth Road** reduced to 20mph / 8.94 m/s; **Dorchester Road** excluded and kept at standard 30mph).
   - Traffic mix: Same heterogeneous driver behavior.

---

## 1. How to Generate Video Visualizations

To record or view video simulations of the "Now" vs "With 20mph" scenarios in SUMO-GUI:

### Running "Now" in GUI
```bash
cd WoolSimulation/sumo
sumo-gui -c wool.stats_now.sumo.cfg
```
*(In SUMO-GUI, use the recording toolbar or camera icon to export frames/video during simulation run).*

### Running "With 20mph" in GUI
```bash
cd WoolSimulation/sumo
sumo-gui -c wool.stats_20mph.sumo.cfg
```

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

**Why both levels matter.** A vehicle travelling at 20mph instead of 30mph emits a
similar mass **per second** but occupies each road segment for **~50% longer**.
For a *vehicle*, that is a near-wash or a small saving; for a *road section*, the
longer occupancy can push the **accumulated total up**. Reporting only one level
(as the original report did) is therefore misleading. `analyze_emissions.py`
reports:
- **road_total** — total mass on all edges (Δ = what a *street/network* experiences)
- **vehicle_total** — total mass over all trips
- **vehicle_perkm** — mass per km driven (Δ = is the *average km* cleaner)

**% change under the 20mph scheme (peak hour, controlled demand):**

| Metric | road_total | vehicle_total | vehicle_perkm |
|---|---|---|---|
| CO2  | +2.17% | +1.96% | +5.63% |
| NOx  | +3.74% | +3.51% | +7.24% |
| PMx  | +2.32% | +2.23% | +5.90% |
| CO   | −4.47% | −4.39% | −0.95% |
| HC   | +3.98% | +4.15% | +7.90% |
| fuel | +2.18% | +1.97% | +5.64% |

**% change under the 20mph scheme (off-peak):**

| Metric | road_total | vehicle_total | vehicle_perkm |
|---|---|---|---|
| CO2  | −0.31% | −0.32% | −0.51% |
| NOx  | +0.24% | +0.22% | +0.03% |
| PMx  | +0.38% | +0.31% | +0.12% |
| CO   | −2.70% | −2.78% | −2.96% |
| HC   | −0.27% | −0.64% | −0.83% |
| fuel | −0.31% | −0.33% | −0.51% |

**Interpretation (refines Hypothesis 1):**

- **Off-peak**, the two levels broadly agree and the change is negligible
  (≤0.5%). Slower cruising marginally *lowers* per-km CO2/fuel/PMx — the
  "smoother pacing" effect is real but tiny at free-flow.
- **Peak**, emissions rise under 20mph, and rise **more per km** (+5–8%) than in
  total (+2–4%). The 20mph cap extends time spent queued/accelerating at
  capacity, so per-km pollution increases. Some trips also fail to complete
  within the hour, so the *total* under-states the per-km penalty.
- **The naive claim "slower ⇒ less pollution" holds only per-km, and only
  off-peak.** Under congested conditions it is the opposite at every level.
- This is a **negative result for the scheme's emissions rationale** and should
  be reported as such, not as a confirmation.

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
