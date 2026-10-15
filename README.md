# Wool Traffic Simulation & Speed Limit Analysis

This repository contains SUMO (Simulation of Urban MObility) models evaluating
the proposed 20mph speed limit in the village of Wool, Dorset, as detailed in
the [Wool Speed Limit Wiki](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit).

**Headline finding (caveated):** whether 20mph *reduces* or *increases* modelled
emissions depends on the assumed driver behaviour. With DfT-calibrated
non-compliance (the evidence-based set) it **increases** peak emissions; journey
times improve slightly in all sets. See the two result documents below.

## Tests we have run

| # | Test set | Behaviour assumption | Configs | Results doc |
|---|---|---|---|---|
| 1 | **Main scenarios** | fixed car mix (10% compliant / 70% normal / 20% speeder), same for both limits | `sumo/wool.dft_{now,20mph}.sumo.cfg` (peak), `wool.dft_offpeak_{now,20mph}.sumo.cfg` | [`EXPERIMENT_REPORT.md`](EXPERIMENT_REPORT.md) |
| 2 | **DfT-calibrated behaviour (sensitivity)** | driver compliance from DfT SPE0101 (2024): 43% exceed on 30mph, 76% on 20mph | `sumo/wool.cal_{now,20mph}.sumo.cfg` | [`SENSITIVITY_BEHAVIOUR.md`](SENSITIVITY_BEHAVIOUR.md) |

Both sets use the same survey-calibrated demand and the same two networks
(`wool.net.xml` vs `wool.20mph.net.xml`), so they isolate the behaviour
assumption.

## Result documents
- **[`EXPERIMENT_REPORT.md`](EXPERIMENT_REPORT.md)** — main analysis (emissions,
  flow/journey times, noise), mapped section-by-section to the Wool Speed Limit wiki.
- **[`SENSITIVITY_BEHAVIOUR.md`](SENSITIVITY_BEHAVIOUR.md)** — sensitivity of the
  result to driver speed behaviour (DfT-calibrated).
- **[`FLOW_CALIBRATION.md`](FLOW_CALIBRATION.md)** — how traffic demand was
  calibrated to the WoolRATH survey.
- **[`sumo/NETWORK_BUILD.md`](sumo/NETWORK_BUILD.md)** — how the 20mph network is
  derived from the Dorset Council consultation.
- **[`sumo/DFT_BEHAVIOUR.md`](sumo/DFT_BEHAVIOUR.md)** — the DfT compliance data
  and the behaviour bands used.
- **[`REPRODUCING.md`](REPRODUCING.md)** — exact commands to regenerate results.

## Methodology & DfT Speed Compliance Data (`Sources/`)
Driver behaviour is parameterised from official Department for Transport (DfT)
**vehicle speed compliance** statistics (SPE01 series), see
[`sumo/DFT_BEHAVIOUR.md`](sumo/DFT_BEHAVIOUR.md). Source files in `Sources/`:
`spe0101.ods` (% exceeding the limit by road type/vehicle type), `spe0113.ods`
(by hour of day), `spe0102.ods` (free-flow speeds), `spe0116.ods`;
`spe0201_offences.ods` is speeding **offences** (not compliance).

- Two comparison sets are provided (fixed-mix and DfT-calibrated) to show the
  sensitivity of the result to this assumption.
- Identical trip demands and fixed seed (42) between the **"Now" (30mph
  baseline)** and **"With 20mph" (proposed scheme)** scenarios.
- The 20mph scheme is defined by an **explicit list of roads** — not a blanket
  change. Roads become 20mph **only if listed** in the Dorset Council
  consultation; every other road keeps its existing limit. The authoritative
  list is `Sources/Wool20MphRoads.json` (41 segments across 35 streets,
  including **Colliers Lane** and **Lulworth Road**). **Dorchester Road** is not
  listed, so it stays at its current (higher) limit. `wool.20mph.net.xml` is
  built from this list — see [`sumo/NETWORK_BUILD.md`](sumo/NETWORK_BUILD.md).

## Repository Structure
- `Sources/` — DfT speed-compliance data and the consultation geoJSON (see above).
- `sumo/` — SUMO networks (`wool.net.xml`, `wool.20mph.net.xml`), route files,
  `*.sumo.cfg` configs, analysis scripts (`analyze_emissions.py`,
  `analyze_noise.py`) and build tooling (`build_20mph_net.py`).
- `AGENT.md` — operational instructions for AI agents.

## Running Simulations
See [`REPRODUCING.md`](REPRODUCING.md) for full instructions to run any test set
in `sumo` or `sumo-gui`.


## Traffic Data & Statistics Origin (WoolRATH Survey)
The traffic flow rates and demand patterns used in this repository are derived directly from the **WoolRATH Traffic Data survey** conducted by local volunteers on September 6th and 9th, 2016 (documented in detail at [Wool Crossing Traffic Simulation Part 5](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolcrossingtrafficsimulationpart5)).

### Baseline Flows (Station Garage at 8:00 AM):
- **Westbound (W):** 500 Cars, 17 HGVs
- **Eastbound (E):** 518 Cars, 25 HGVs

### Development Impact (800 Homes):
- Based on TRICS / PTI trip rate modeling (scaling 1,000 homes down to 800 homes = **277 vehicles/hour** generated).
- Applying the measured 50.88% Eastbound split yields **141 additional cars heading East** (towards Wareham, passing the level crossing) between 8:00 AM and 9:00 AM.
- Railway barrier closure timings (from the 6th–9th September 2016 level-crossing logs, e.g. Train 1W96 closing the crossing at 08:14:58) are integrated to study queue buildup (reaching ~228m near Bailey's Drove during barrier closures).

> **Flow calibration:** the operational peak/off-peak demand has been audited and
> corrected against the survey above — see **`FLOW_CALIBRATION.md`**. The route
> files now in use are `wool.rou.dft_controlled.v2.xml` (peak) and
> `wool.rou.dft_offpeak.v2.xml` (off-peak). An earlier demand file over-loaded
> the peak network (~39% above the measured A352 flow) and inverted the
> emissions result; the corrected demand removes that saturation.


## Comprehensive Simulation Plan: Sticky Routing & Hourly/Weekly Temporal Profiling
To further enhance the realism and accuracy of the Wool speed limit study, the simulation methodology incorporates two key advancements:

1. **Sticky Through-Traffic Routing (No Back-Street Detours):**
   - Vehicles traveling West-to-East or East-through-West are assigned fixed, explicit route edges along the primary corridor (Dorchester Road / High Street).
   - Automatic dynamic re-routing is disabled, ensuring that when railway level crossing barrier closures occur, vehicles queue realistically along the main route rather than making artificial detours through residential back roads (such as Colliers Lane or Lulworth Road).

2. **24/7 Hourly & Day-of-Week Temporal Profiling:**
   - Utilizing Department for Transport temporal distributions (**SPE0103** for hour-of-day and **SPE0104** for day-of-week) combined with WoolRATH survey data, a full 24-hour × 7-day batch runner scales the baseline traffic flow rates (e.g. the 8:00 AM peak of 518 cars, 49 LGVs and 25 HGVs west-to-east).
   - This captures distinct traffic behaviors across weekday commuter peaks, school runs, weekend leisure travel, and late-night quiet periods, generating complete multi-day statistical matrices for emissions, queue lengths (e.g., up to 228m near Bailey's Drove), and journey times.
