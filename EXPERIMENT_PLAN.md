# Wool Speed Limit Simulation Experiment & Testing Plan

This document defines the complete experimental plan, testing procedures, data collection, and visualization methods to evaluate the impact of lowering back-road speed limits in the village of Wool, Dorset, from 30mph to 20mph (as outlined in the [Wool Speed Limit Wiki](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit)).

---

## 1. Experimental Hypotheses & Conditions

- **Hypothesis 1 (Emissions & Particulates):** Lowering speed limits on residential back roads and village routes from 30mph to 20mph does not increase overall exhaust pollution and can reduce stop-start particulate emissions (PMx) due to smoother vehicle pacing and reduced harsh acceleration/braking.
- **Hypothesis 2 (Traffic Flow & Journey Times):** Restricting the **listed** roads to 20mph while leaving non-listed arterial thoroughfares (**Dorchester Road** is not in the list) at their existing limits results in a negligible impact on overall journey duration (estimated under 1 minute difference).
- **Hypothesis 3 (Non-Vehicle & Active Travel):** Slower vehicle speeds improve pedestrian safety, reduce crossing wait times, and harmonize traffic flow around railway level crossing barrier closures (`joinedS_0`).

### Scheme definition
The set of roads that become 20mph is defined by the Dorset Council consultation
(`Sources/Wool20MphRoads.json`) — a **positive list** of 41 segments across 35
streets. A road reverts to 20mph **only if it is in that list**; all other roads
keep their current limit. This is not a blanket "everything except Dorchester
Road" change.

### Compared Scenarios:
1. **"Now" (Baseline):** Network `wool.net.xml` at existing limits (residential/back roads at 30mph ~13.4 m/s).
2. **"With 20mph" (Proposed Scheme):** Network `wool.20mph.net.xml` where the **listed** roads (including **Colliers Lane** and **Lulworth Road**) are capped at 20mph (~8.94 m/s). Non-listed roads, including **Dorchester Road**, retain their existing limits.

---

## 2. Test Procedure & Execution

Both scenarios use identical traffic demand flows and Department for Transport (DfT) speed compliance distributions (`Sources/SPE0101.ods`) parameterized in `wool.rou.dft_controlled.xml`. This ensures 100% controlled before-and-after comparability.

### Step 1: Run Batch Simulations (Statistical & Emission Data Collection)
Execute the headless SUMO runners to generate trip records, performance statistics, and emission XMLs:
```bash
cd WoolSimulation/sumo

# 1. Run 30mph Baseline
sumo -c wool.dft_now.sumo.cfg

# 2. Run 20mph Proposed Scheme
sumo -c wool.dft_dft_20mph.sumo.cfg
```

### Step 2: Analyze Output Statistics
Output files generated:
- **Trip Info (`wool.dft_now.tripinfo.xml` vs `wool.dft_20mph.tripinfo.xml`)**: Measures travel times, waiting times, and time loss per vehicle.
- **Aggregated Statistics (`wool.dft_now.statistic.xml` vs `wool.dft_20mph.statistic.xml`)**: Overall vehicle counts, throughput, and simulation performance.
- **Emissions (`wool.emissions.xml`)**: Tracks CO2, CO, PMx (particulate matter), NOx, and fuel consumption (`fuel_abs`).

---

## 3. Video Recording & Visualization Procedure

To generate side-by-side video comparisons of the **"Now"** vs **"With 20mph"** simulations:

1. **Interactive GUI Mode**:
   ```bash
   cd WoolSimulation/sumo
   sumo-gui -c wool.dft_now.sumo.cfg
   ```
   *(Use the built-in recording toolbar in `sumo-gui` to capture frames or record video).*

2. **Headless Xvfb Frame Capture**:
   For automated recording on headless environments, launch a virtual X server (`Xvfb :99`) and run `sumo-gui` with `--start --quit-on-end`.
