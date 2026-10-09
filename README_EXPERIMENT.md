# Wool Simulation & Speed Limit Experiments in SUMO

This repository now contains the **WoolSimulation** submodule integrated into the main `TrafficSim` repository, set up to test various speed limit adherence scenarios (such as strict adherence vs speeders) in the village of Wool, Dorset, using SUMO (Simulation of Urban MObility).

## Background & Objectives
As detailed in the [Wool Speed Limit Wiki](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit), the village of Wool considers speed limit adjustments (e.g. 20mph vs 30mph zones) to improve safety, reduce emissions, and encourage active travel. 

This repository allows experimenting with behavioral conditions:
- **Strict adherence** (e.g. 10% of drivers rigidly adhering to speed limits/20mph).
- **Speeders** (drivers traveling above standard speeds).
- **Normal traffic flow**.

## File Structure (`WoolSimulation/sumo/`)
- `wool.net.xml`: The road network of Wool, Dorset.
- `wool.rou.xml`: Standard route file based on surveyed traffic flows.
- `wool.rou.speed_experiment.xml`: Experimental route file featuring heterogeneous driver behaviors (`CAR_STRICT`, `CAR`, `CAR_SPEEDER`).
- `wool.sumo.cfg`: Standard SUMO configuration.
- `wool.speed_experiment.sumo.cfg`: Experimental SUMO configuration utilizing the speed experiment routes.
- `wool.additional-6-9-2016.xml`: Traffic light and level-crossing timings (e.g. railway crossing closures).

## Running the Simulation

Make sure you have SUMO installed. You can run simulations via terminal or GUI:

### 1. Run Standard Simulation
```bash
cd WoolSimulation/sumo
sumo -c wool.sumo.cfg --end 3600
```

### 2. Run Speed Experiment Simulation (with Compliant / Speeder mix)
```bash
cd WoolSimulation/sumo
sumo -c wool.speed_experiment.sumo.cfg --end 3600
```

### 3. Run with GUI (requires X11 / desktop environment)
```bash
cd WoolSimulation/sumo
sumo-gui -c wool.speed_experiment.sumo.cfg
```
