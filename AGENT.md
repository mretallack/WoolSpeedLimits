# Agent Instructions (AGENT.md)

This repository (`TrafficSim` / `WoolSimulation`) models traffic simulation scenarios for the village of Wool, Dorset, using SUMO (Simulation of Urban MObility). It evaluates the impact of the proposed 20mph scheme.

**Scope of the scheme (important):** the proposal is **not** "all roads become 20mph except X". It is a **positive list**: a road becomes 20mph **only if it appears in the Dorset Council consultation**. The authoritative definition is `Sources/Wool20MphRoads.json` (consultation geoJSON: 41 segments, 35 streets, including Colliers Lane and Lulworth Road; Dorchester Road is not listed and stays at its existing limit). Any road not in that file is unchanged. `wool.20mph.net.xml` is generated from this list by `sumo/build_20mph_net.py` (see `sumo/NETWORK_BUILD.md` for the method, the 20 speed-tag anomalies and the 9 streets absent from the network).

## Key Components
- **`WoolSimulation/sumo/`**: Contains SUMO network files (`wool.net.xml`, `wool.20mph.net.xml`), additional files (traffic lights, level crossings, emissions), and runner configurations.
- **`WoolSimulation/Sources/`**: Contains official Department for Transport (DfT) vehicle speed compliance statistics (SPE01 series: SPE0101, SPE0102, SPE0103, SPE0104, SPE0105) used to parameterize realistic speed distributions by vehicle type and road type.
- **`WoolSimulation/EXPERIMENT_REPORT.md`**: Detailed findings, emission tracking, and non-vehicle/pedestrian/railway interaction models.

## Working with the Simulation
When running or modifying simulations:
1. There are **two comparison sets**; keep them separate and always report which one a number comes from:
   - **Main set (`dft`)**: fixed car mix (10%/70%/20%). Peak `wool.dft_now.sumo.cfg`
     vs `wool.dft_20mph.sumo.cfg` (routes `wool.rou.dft_controlled.v2.xml`);
     off-peak `wool.dft_offpeak_{now,20mph}.sumo.cfg` (routes `wool.rou.dft_offpeak.v2.xml`).
     Results doc: `EXPERIMENT_REPORT.md`.
   - **DfT-calibrated set (`cal`)**: driver compliance from DfT SPE0101 (2024),
     different mix per limit. `wool.cal_now.sumo.cfg` vs `wool.cal_20mph.sumo.cfg`
     (routes `wool.rou.dft_cal_30.xml` / `wool.rou.dft_cal_20.xml`).
     Results doc: `SENSITIVITY_BEHAVIOUR.md`; data: `sumo/DFT_BEHAVIOUR.md`.
   - Always use controlled random seeds / identical demand between baseline and
     scheme. The `.v2` and `.dft_cal_*` route files are survey-calibrated; **do
     not revert** to the old over-loaded `wool.rou.dft_controlled.xml` /
     `wool.rou.dft_offpeak.xml` (see `FLOW_CALIBRATION.md`).
   - **The emissions result depends on the behaviour assumption**: the `dft` set
     shows a reduction, the `cal` set an increase. State the assumption with any
     emissions claim.
2. Run SUMO using `sumo -c <config>.sumo.cfg`.
3. Respect submodules (`WoolSimulation`) when committing and pushing changes.

## Emissions: always report the LEVEL and the VIEW
A speed-limit change can move emissions in *opposite* directions depending on how
they are aggregated, so **never report a single figure**. Report:
- **Level**: road (`*.road_emissions.xml`, edgeData) vs vehicle (`*.emissions.xml`).
- **View**: absolute **total** vs **per km** (`vehicle_perkm`). These differ
  materially: absolute totals also depend on **how many vehicle-km are driven**
  (a scenario that completes more trips drives more km and raises every total).
  In the DfT-calibrated set the totals are *mixed* while **per km five of six
  pollutants fall**.

Analyse with `sumo/analyze_emissions.py` (prints road_total, vehicle_total and
vehicle_perkm side by side). Also **state the behaviour assumption**: the fixed
`dft` set and the DfT-calibrated `cal` set give different answers. See
`EXPERIMENT_REPORT.md` §2.1 and `SENSITIVITY_BEHAVIOUR.md`.

## Saturation guard (run this after every demand change)
Before trusting any emissions result, confirm the run did not saturate:
- `<vehicles ... waiting="0">` and `loaded == inserted` in `*.statistic.xml`
- `<teleports total="0">`
If either fails, the demand is over capacity and the emissions conclusion is
unreliable (an over-loaded peak run has been shown to invert the result).
See `FLOW_CALIBRATION.md` for the survey calibration.
