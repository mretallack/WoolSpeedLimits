# Wool Traffic Simulation & Speed Limit Analysis

This repository contains SUMO (Simulation of Urban MObility) models and experimental frameworks for evaluating the proposed 20mph speed limit in the village of Wool, Dorset, as detailed in the [Wool Speed Limit Wiki](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit).

## Methodology & DfT Speed Compliance Data (`Sources/`)
To model realistic driver behaviors across different vehicle classes (Cars, Vans/LGVs, HGVs, Buses, Motorcycles), we incorporate official Department for Transport (DfT) vehicle speed compliance statistics (SPE01 series, such as **SPE0101** stored in `Sources/SPE0101.ods`). 

By applying empirical speed distributions and compliance rates by road type and vehicle class:
- We capture realistic free-flow speeds, speeders, and compliant drivers.
- We ensure identical trip demands and random seed controls between the **"Now" (30mph baseline)** and **"With 20mph" (proposed scheme)** scenarios.
- The 20mph scheme specifically excludes **Dorchester Road** (maintaining primary through-route speeds) while updating all other residential and back roads, notably **Colliers Lane** and **Lulworth Road**.

## Repository Structure
- `WoolSimulation/sumo/`: SUMO network files (`wool.net.xml`, `wool.20mph.net.xml`), additional configuration files (traffic lights, level crossings, emissions), and runner configs.
- `WoolSimulation/Sources/`: DfT speed compliance data tables (SPE01).
- `WoolSimulation/EXPERIMENT_REPORT.md`: Detailed findings, emission metrics, and non-vehicle/pedestrian/railway interaction models.
- `WoolSimulation/AGENT.md`: Operational instructions for AI agents.

## Running Simulations
See `WoolSimulation/EXPERIMENT_REPORT.md` for full instructions on running simulations in `sumo` or `sumo-gui`.
