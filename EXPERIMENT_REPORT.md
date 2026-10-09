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

SUMO records trip statistics and pollutant emissions via additional output definitions (`wool.stats.additional.xml`).

### Running Automated Batch Simulations & Stats Export
```bash
cd WoolSimulation/sumo
sumo -c wool.stats_now.sumo.cfg
sumo -c wool.stats_20mph.sumo.cfg
```

### Key Statistical Metrics Collected
- **Trip Statistics (`wool.tripinfo.xml` / `wool.statistic.xml`)**:
  - Average travel duration and time loss.
  - Waiting times at junctions and railway level crossings (`joinedS_0`).
  - Route lengths and vehicle throughput.
- **Emissions & Fuel Consumption (`wool.emissions.xml`)**:
  - Total CO2, CO, PMx (particulate matter from exhaust and tire/brake wear), NOx, and fuel consumption (`fuel_abs`).

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
