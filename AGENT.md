# Agent Instructions (AGENT.md)

This repository (`TrafficSim` / `WoolSimulation`) models traffic simulation scenarios for the village of Wool, Dorset, using SUMO (Simulation of Urban MObility). It evaluates the impact of the proposed 20mph scheme.

**Scope of the scheme (important):** the proposal is **not** "all roads become 20mph except X". It is a **positive list**: a road becomes 20mph **only if it appears in the Dorset Council consultation**. The authoritative definition is `Sources/Wool20MphRoads.json` (consultation geoJSON: 41 segments, 35 streets, including Colliers Lane and Lulworth Road; Dorchester Road is not listed and stays at its existing limit). Any road not in that file is unchanged.

## Key Components
- **`WoolSimulation/sumo/`**: Contains SUMO network files (`wool.net.xml`, `wool.20mph.net.xml`), additional files (traffic lights, level crossings, emissions), and runner configurations.
- **`WoolSimulation/Sources/`**: Contains official Department for Transport (DfT) vehicle speed compliance statistics (SPE01 series: SPE0101, SPE0102, SPE0103, SPE0104, SPE0105) used to parameterize realistic speed distributions by vehicle type and road type.
- **`WoolSimulation/EXPERIMENT_REPORT.md`**: Detailed findings, emission tracking, and non-vehicle/pedestrian/railway interaction models.

## Working with the Simulation
When running or modifying simulations:
1. Always use controlled random seeds or identical route files between the 30mph baseline and 20mph proposed scheme to ensure valid before-and-after comparisons. Primary comparison pairs:
   - **Peak (controlled):** `wool.dft_now.sumo.cfg` vs `wool.dft_20mph.sumo.cfg` (routes `wool.rou.dft_controlled.v2.xml`).
   - **Off-peak:** `wool.dft_offpeak_now.sumo.cfg` vs `wool.dft_offpeak_20mph.sumo.cfg` (routes `wool.rou.dft_offpeak.v2.xml`).
   - The `.v2` route files are survey-calibrated. **Do not revert to the old**
     `wool.rou.dft_controlled.xml` / `wool.rou.dft_offpeak.xml`: those over-loaded
     the peak network (~39% above measured flow) and inverted the emissions
     result. See `FLOW_CALIBRATION.md`.
2. Run SUMO using `sumo -c <config>.sumo.cfg`.
3. Respect submodules (`WoolSimulation`) when committing and pushing changes.

## Emissions: always report TWO levels
A speed-limit change can move emissions in *opposite* directions at road level vs
vehicle level, so **never report a single figure**. Each config emits both:
- **Road-level** → `wool.dft_<scenario>.road_emissions.xml` (edgeData, via `wool.stats.<scenario>.additional.xml`).
- **Vehicle-level** → `wool.dft_<scenario>.emissions.xml` (`<emission-output>`).

Analyse with `sumo/analyze_emissions.py`, which prints **road_total**, **vehicle_total**
and **vehicle_perkm** (per-km) side by side. See `EXPERIMENT_REPORT.md` §2.1 for the
headline numbers.

## Saturation guard (run this after every demand change)
Before trusting any emissions result, confirm the run did not saturate:
- `<vehicles ... waiting="0">` and `loaded == inserted` in `*.statistic.xml`
- `<teleports total="0">`
If either fails, the demand is over capacity and the emissions conclusion is
unreliable (an over-loaded peak run has been shown to invert the result).
See `FLOW_CALIBRATION.md` for the survey calibration.
