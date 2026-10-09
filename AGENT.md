# Agent Instructions (AGENT.md)

This repository (`TrafficSim` / `WoolSimulation`) models traffic simulation scenarios for the village of Wool, Dorset, using SUMO (Simulation of Urban MObility). It specifically evaluates the impact of changing residential and back-road speed limits from 30mph to 20mph (excluding Dorchester Road, while updating Colliers Lane and Lulworth Road).

## Key Components
- **`WoolSimulation/sumo/`**: Contains SUMO network files (`wool.net.xml`, `wool.20mph.net.xml`), additional files (traffic lights, level crossings, emissions), and runner configurations.
- **`WoolSimulation/Sources/`**: Contains official Department for Transport (DfT) vehicle speed compliance statistics (SPE01 series: SPE0101, SPE0102, SPE0103, SPE0104, SPE0105) used to parameterize realistic speed distributions by vehicle type and road type.
- **`WoolSimulation/EXPERIMENT_REPORT.md`**: Detailed findings, emission tracking, and non-vehicle/pedestrian/railway interaction models.

## Working with the Simulation
When running or modifying simulations:
1. Always use controlled random seeds or identical route files (`wool.rou.dft_controlled.xml`) between the 30mph baseline (`wool.stats_now.sumo.cfg`) and 20mph proposed scheme (`wool.stats_20mph.sumo.cfg`) to ensure valid before-and-after comparisons.
2. Run SUMO using `sumo -c <config>.sumo.cfg`.
3. Respect submodules (`WoolSimulation`) when committing and pushing changes.
