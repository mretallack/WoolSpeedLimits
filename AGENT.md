# Agent Instructions (AGENT.md)

This repository (`TrafficSim` / `WoolSimulation`) models traffic simulation scenarios for the village of Wool, Dorset, using SUMO (Simulation of Urban MObility). It specifically evaluates the impact of changing residential and back-road speed limits from 30mph to 20mph (excluding Dorchester Road, while updating Colliers Lane and Lulworth Road).

## Key Components
- **`WoolSimulation/sumo/`**: Contains SUMO network files (`wool.net.xml`, `wool.20mph.net.xml`), additional files (traffic lights, level crossings, emissions), and runner configurations.
- **`WoolSimulation/Sources/`**: Contains official Department for Transport (DfT) vehicle speed compliance statistics (SPE01 series: SPE0101, SPE0102, SPE0103, SPE0104, SPE0105) used to parameterize realistic speed distributions by vehicle type and road type.
- **`WoolSimulation/EXPERIMENT_REPORT.md`**: Detailed findings, emission tracking, and non-vehicle/pedestrian/railway interaction models.

## Working with the Simulation
When running or modifying simulations:
1. Always use controlled random seeds or identical route files between the 30mph baseline and 20mph proposed scheme to ensure valid before-and-after comparisons. Primary comparison pairs:
   - **Peak (controlled):** `wool.dft_now.sumo.cfg` vs `wool.dft_20mph.sumo.cfg` (routes `wool.rou.dft_controlled.xml`).
   - **Off-peak:** `wool.dft_offpeak_now.sumo.cfg` vs `wool.dft_offpeak_20mph.sumo.cfg` (routes `wool.rou.dft_offpeak.xml`).
2. Run SUMO using `sumo -c <config>.sumo.cfg`.
3. Respect submodules (`WoolSimulation`) when committing and pushing changes.

## Emissions: always report TWO levels
A speed-limit change can move emissions in *opposite* directions at road level vs
vehicle level, so **never report a single figure**. Each config emits both:
- **Road-level** → `wool.dft_<scenario>.road_emissions.xml` (edgeData, via `wool.stats.<scenario>.additional.xml`).
- **Vehicle-level** → `wool.dft_<scenario>.emissions.xml` (`<emission-output>`).

Analyse with `sumo/analyze_emissions.py`, which prints **road_total**, **vehicle_total**
and **vehicle_perkm** (per-km) side by side. See `EXPERIMENT_REPORT.md` §2.1 for the
headline numbers and the caveat that "slower ⇒ cleaner" only holds per-km off-peak.
