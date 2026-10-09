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


## Traffic Data & Statistics Origin (WoolRATH Survey)
The traffic flow rates and demand patterns used in this repository are derived directly from the **WoolRATH Traffic Data survey** conducted by local volunteers on September 6th and 9th, 2016 (documented in detail at [Wool Crossing Traffic Simulation Part 5](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolcrossingtrafficsimulationpart5)).

### Baseline Flows (Station Garage at 8:00 AM):
- **Westbound (W):** 500 Cars, 17 HGVs
- **Eastbound (E):** 518 Cars, 25 HGVs

### Development Impact (800 Homes):
- Based on TRICS / PTI trip rate modeling (scaling 1,000 homes down to 800 homes = **277 vehicles/hour** generated).
- Applying the measured 50.88% Eastbound split yields **141 additional cars heading East** (towards Wareham, passing the level crossing) between 8:00 AM and 9:00 AM.
- Railway barrier closure timings () are integrated to study queue buildup (reaching ~228m near Bailey's Drove during barrier closures).
