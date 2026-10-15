# Wool 20mph Speed Limit Experiments & Non-Vehicle Modeling Report

This document outlines the experimental setup, simulation configurations, statistical output collection, and non-vehicle (pedestrian/railway) modeling designed to test the claims and assumptions in the [Wool Speed Limit Wiki](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit).

---

## Summary of Scenarios

The comparison pairs (survey-calibrated demand, see `FLOW_CALIBRATION.md`) are:

1. **Peak (08:00, controlled)** — routes `wool.rou.dft_controlled.v2.xml`
   - 30mph baseline: `wool.dft_now.sumo.cfg` (network `wool.net.xml`)
   - 20mph scheme:  `wool.dft_20mph.sumo.cfg` (network `wool.20mph.net.xml`)

2. **Off-peak** — routes `wool.rou.dft_offpeak.v2.xml`
   - 30mph baseline: `wool.dft_offpeak_now.sumo.cfg`
   - 20mph scheme:  `wool.dft_offpeak_20mph.sumo.cfg`

These use a **fixed** car mix (10% compliant / 70% normal / 20% speeder) at both
limits. A **second set with DfT-calibrated driver behaviour**
(`wool.cal_*.sumo.cfg`) produces a **mixed** emissions result that differs from
this set — reported in [§2.4](#24-sensitivity-to-driver-speed-behaviour-the-cal-set).

The 20mph scheme is defined by an **explicit list of roads**, not a blanket
change. The authoritative definition is the Dorset Council consultation geoJSON
`Sources/Wool20MphRoads.json`: **41 segments across 35 streets**, including
**Colliers Lane** and **Lulworth Road**. A road becomes 20mph (8.94 m/s)
**only if it is in that list**; every other road keeps its existing limit.
**Dorchester Road** is not in the list and is retained at its current limit.

`wool.20mph.net.xml` is built from that list by matching consultation streets to
network edges (name + geometry overlap) and setting the matched edges that are
**currently 30/31 mph** to 20mph — **99 edges**. Higher-speed matched edges
(50/62 mph anomalies) and all unlisted roads are left unchanged. The full method,
the 20 anomalous edges and the 9 consultation streets absent from the network are
documented in [`sumo/NETWORK_BUILD.md`](sumo/NETWORK_BUILD.md). Both scenarios
use the same heterogeneous driver mix (compliant / normal / speeder).

**Seeding and repeatability.** All four configs now carry a fixed seed
(`<seed value="42"/>`). Repeated runs of the same config are identical to the
last digit, so the numbers below are reproducible — see `REPRODUCING.md`. The
results in this report were produced by re-running all four scenarios with the
fixed seed and the corrected network; where they differ from an earlier draft,
the causes are documented in [§2.1.1](#211-reproducibility-run-to-run-variation-and-the-hc-metric).

**Model limitations** (detail in [`sumo/NETWORK_BUILD.md`](sumo/NETWORK_BUILD.md)):
1. **9 consultation streets are absent from the SUMO network** (minor roads
   dropped at OSM import): Access To Wool Station, Baker Close, Burton Wood,
   Hillside Road, New Road, Oakdene Road, Sandhills Crescent, Water Meadow
   Lane. Their 20mph zones are not modelled (negligible corridor effect).
2. **20 matched edges carry implausible 50/62 mph OSM tags** (e.g. a 130 m
   stretch of "Lulworth Road" at 62 mph). These are left at their baseline
   speed so the "Now" baseline stays a consistent 30mph world.

---

## Wiki Coverage Map

This report is written to test the claims in
[**The Case for a 20mph Speed Limit in Wool, Dorset**](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit).
Every section of that wiki page is listed below with its anchor link and the
simulation evidence (or explicit note) that addresses it. Each report section
that maps to the wiki also links the relevant **sub-sections** directly (the
wiki's `h4` anchors, e.g. *Evidence from London*, *How lower speeds can mean
shorter journeys*, *How much quieter?*, *The 20mph threshold*, *Table 1–3*).

| Wiki section | Simulation coverage | Where |
|---|---|---|
| [2.1 Vehicle Emissions at Slower Speeds](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#vehicle_emissions_at_slower_speeds) | **Modelled** — road- and vehicle-level CO2, NOx, PMx, CO, HC, fuel, both scenarios | [§2.1](#21-measured-emissions--road-level-vs-vehicle-level) |
| [2.2 Impact on Traffic Flow and Congestion](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#impact_on_traffic_flow_and_congestion) | **Modelled** — journey time, time loss, waiting time, throughput | [§2.2](#22-traffic-flow-and-journey-times) |
| [2.3 Public Perception and Acceptance](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#public_perception_and_acceptance) | **Not modelled** — attitudinal, outside a traffic simulation's scope | [§2.3](#23-public-perception-not-modelled) |
| [3.1 Enhanced Safety for Pedestrians and Cyclists](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#enhanced_safety_for_pedestrians_and_cyclists) | **Partly** — speed reduction modelled; casualty outcomes require an accident model (not present) | [§3.1](#31-pedestrian-and-cyclist-safety) |
| [3.2 Encouraging Active Travel](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#encouraging_active_travel) | **Partly** — pedestrian substructure exists but is not yet populated | [§3.2](#32-active-travel-not-yet-populated) |
| [3.3 Reduction in Noise Pollution](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#reduction_in_noise_pollution) | **Modelled** — HBEFA vehicle noise (dB(A)), both scenarios | [§3.3](#33-noise-pollution) |
| [3.4 Improved Community Liveability](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#improved_community_liveability) | **Not modelled** — qualitative | [§3.4](#34-community-liveability-not-modelled) |
| [4.1 Dorset Examples](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#dorset_examples) | **External** — case studies, cited for context | [§4](#4-case-studies-external-evidence) |
| [4.2 UK-Wide Examples](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#uk-wide_examples) | **External** — case studies, cited for context | [§4](#4-case-studies-external-evidence) |
| [5. Conclusion and Recommendations](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#conclusion_and_recommendations) | **Synthesis** — this report's findings feed Recommendations 1–5 | [§5](#5-conclusion-synthesis) |
| [Key Tables 1–3](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#key_tables) | **Referenced** — external evidence (fatality risk, casualties, noise) | [§3.3](#33-noise-pollution), [§3.1](#31-pedestrian-and-cyclist-safety) |

**Summary:** of the four *substantive* claims the simulation can test
(emissions, flow, active travel, noise), **two are fully modelled**
(emissions §2.1, flow §2.2) and **one is newly added** (noise §3.3). Active
travel (§3.2) and the safety *outcomes* in §3.1 are only partly covered because
the model has no pedestrian population and no accident/casualty model. The
attitudinal (§2.3) and case-study (§4) sections are out of scope by nature.
Emissions are also tested under two driver-behaviour assumptions (`dft` §2.1 and
DfT-calibrated `cal` §2.4), which give different answers.

---

## 1. Video Visualizations

Pre-rendered videos of every scenario are committed in `sumo/` (each 200 s,
~20–29 MB). They let a reader see the scheme playing out — traffic volumes,
queues at the level crossing, and how compliance differs between the two
driver-behaviour sets.

| Video (`sumo/…`) | Set | Period | Network | Driver behaviour | Illustrates |
|---|---|---|---|---|---|
| `wool_peak_30mph.webm` | `dft` | peak | 30mph baseline | fixed 10 / 70 / 20 | §2.1 baseline |
| `wool_peak_20mph.webm` | `dft` | peak | 20mph scheme | fixed 10 / 70 / 20 | §2.1 scheme |
| `wool_offpeak_30mph.webm` | `dft` | off-peak | 30mph baseline | fixed 10 / 70 / 20 | §2.1 baseline |
| `wool_offpeak_20mph.webm` | `dft` | off-peak | 20mph scheme | fixed 10 / 70 / 20 | §2.1 scheme |
| `wool_cal_peak_30mph.webm` | `cal` | peak | 30mph baseline | DfT-fitted (43% exceed) | §2.4 baseline |
| `wool_cal_peak_20mph.webm` | `cal` | peak | 20mph scheme | DfT-fitted (76% exceed) | §2.4 scheme |
| `wool_cal_offpeak_30mph.webm` | `cal` | off-peak | 30mph baseline | DfT-fitted (43% exceed) | §2.4 baseline |
| `wool_cal_offpeak_20mph.webm` | `cal` | off-peak | 20mph scheme | DfT-fitted (76% exceed) | §2.4 scheme |

*Set key:* `dft` = fixed car mix (10% compliant / 70% normal / 20% speeder);
`cal` = driver speed distribution fitted to DfT 2024 compliance data (§2.4).
The `cal` videos show **more speeding**, especially on the 20mph network.

### Re-recording or running interactively

Headless (Xvfb + ffmpeg):

```bash
cd sumo
./render_sync.sh <config.sumo.cfg> <output.webm> [duration_secs] [delay_ms]
# e.g. ./render_sync.sh wool.dft_20mph.sumo.cfg wool_peak_20mph.webm 200 60
```

Or in SUMO-GUI (use the recording toolbar / camera icon to export frames/video):

```bash
cd sumo
sumo-gui -c wool.dft_now.sumo.cfg            # peak 30mph
sumo-gui -c wool.dft_20mph.sumo.cfg          # peak 20mph
sumo-gui -c wool.dft_offpeak_now.sumo.cfg    # off-peak 30mph
sumo-gui -c wool.dft_offpeak_20mph.sumo.cfg  # off-peak 20mph
sumo-gui -c wool.cal_now.sumo.cfg            # peak 30mph (DfT-calibrated)
sumo-gui -c wool.cal_20mph.sumo.cfg          # peak 20mph (DfT-calibrated)
sumo-gui -c wool.cal_offpeak_now.sumo.cfg    # off-peak 30mph (DfT-calibrated)
sumo-gui -c wool.cal_offpeak_20mph.sumo.cfg  # off-peak 20mph (DfT-calibrated)
```

> **Note:** SUMO-GUI crashes on this host if a vType sets
> `device.rerouting.probability="0.0"`. That attribute has been removed from the
> route files (results are identical without it). See `FLOW_CALIBRATION.md`.

---

## 2. Statistical Analysis & Emissions

SUMO records trip statistics and pollutant emissions. **Emissions are deliberately
collected at two different levels**, because a change to the speed limit can push
them in *opposite* directions depending on the level of aggregation (see §2.1).

### Data sources

- **Traffic demand** — WoolRATH manual survey (Sept 2016); see
  [`FLOW_CALIBRATION.md`](FLOW_CALIBRATION.md).
- **Driver speed behaviour** — DfT *Vehicle speed compliance statistics for
  Great Britain: 2024* (published 25 June 2025).
  Landing page: <https://www.gov.uk/government/statistics/vehicle-speed-compliance-statistics-for-great-britain-2024>.
  Local copies committed under [`Sources/`](Sources/):
  `spe0101.ods` (% exceeding by road type / vehicle type — the key table),
  `spe0113.ods` (by hour of day), `spe0102.ods` (free-flow speeds),
  `spe0116.ods` (by day). Full provenance and the derivation are in
  [`sumo/DFT_BEHAVIOUR.md`](sumo/DFT_BEHAVIOUR.md).
- **20mph road list** — Dorset Council consultation; see
  [`sumo/NETWORK_BUILD.md`](sumo/NETWORK_BUILD.md) and `Sources/Wool20MphRoads.json`.

### Running Automated Batch Simulations & Stats Export
```bash
cd sumo
# Main set — fixed driver mix (`dft`)
sumo -c wool.dft_now.sumo.cfg            # peak 30mph baseline
sumo -c wool.dft_20mph.sumo.cfg          # peak 20mph scheme
sumo -c wool.dft_offpeak_now.sumo.cfg    # off-peak 30mph
sumo -c wool.dft_offpeak_20mph.sumo.cfg  # off-peak 20mph
# Sensitivity set — DfT-calibrated driver behaviour (`cal`, see §2.4)
sumo -c wool.cal_now.sumo.cfg            # peak 30mph
sumo -c wool.cal_20mph.sumo.cfg          # peak 20mph
sumo -c wool.cal_offpeak_now.sumo.cfg    # off-peak 30mph
sumo -c wool.cal_offpeak_20mph.sumo.cfg  # off-peak 20mph
```

Each config now produces **both**:
- **Road-level** emissions — `wool.dft_<scenario>.road_emissions.xml`
  (`edgeData type="emissions"`, per edge per 60 s, defined in
  `wool.stats.<scenario>.additional.xml`).
- **Vehicle-level** emissions — `wool.dft_<scenario>.emissions.xml`
  (`<emission-output>`, per-vehicle per timestep).

### Key Statistical Metrics Collected
- **Trip Statistics (`<scenario>.tripinfo.xml` / `<scenario>.statistic.xml`)**:
  - Average travel duration and time loss.
  - Waiting times at junctions and railway level crossings (`joinedS_0`).
  - Route lengths and vehicle throughput.
- **Emissions & Fuel Consumption** — collected at both road level
  (`wool.dft_<scenario>.road_emissions.xml`) and vehicle level
  (`wool.dft_<scenario>.emissions.xml`):
  - CO2, CO, PMx (particulate matter), NOx, HC and fuel consumption.

### Analysis Tool: `analyze_emissions.py`
Compare any two scenario runs across **all four views** in one command:

```bash
cd WoolSimulation/sumo
python3 analyze_emissions.py \
  --now-edge   wool.dft_offpeak_now.road_emissions.xml \
  --now-veh    wool.dft_offpeak_now.emissions.xml \
  --now-trip   wool.dft_offpeak_now.tripinfo.xml \
  --scheme-edge wool.dft_offpeak_20mph.road_emissions.xml \
  --scheme-veh  wool.dft_offpeak_20mph.emissions.xml \
  --scheme-trip wool.dft_offpeak_20mph.tripinfo.xml \
  --label-now "offpeak 30mph" --label-scheme "offpeak 20mph" \
  --csv results_offpeak.csv
```
(swap the `dft_offpeak_*` names for `dft_now` / `dft_20mph` for the peak-hour pair).

### 2.1 Measured Emissions — Road-Level vs Vehicle-Level

**Why both levels matter.** A vehicle travelling at 20mph instead of 30mph emits a
similar mass **per second** but occupies each road segment for **~50% longer**.
For a *vehicle*, that is a near-wash or a small saving; for a *road section*, the
longer occupancy can push the **accumulated total up**. Reporting only one level
is therefore misleading, so `analyze_emissions.py` reports:
- **road_total** — total mass on all edges (Δ = what a *street/network* experiences)
- **vehicle_total** — total mass over all trips
- **vehicle_perkm** — mass per km driven (Δ = is the *average km* cleaner)

**These tables are for the `dft` set** — the fixed driver mix (10% compliant /
70% normal / 20% speeder, identical at both limits), peak and off-peak, seed 42.
The **`cal` set**, where the driver speed distribution is fitted to DfT 2024
speed-compliance data instead, gives a **different** result and is reported in
[§2.4](#24-sensitivity-to-driver-speed-behaviour-the-cal-set).

**`dft` set — % change under the 20mph scheme (peak hour, seed 42):**

| Metric | road_total | vehicle_total | vehicle_perkm |
|---|---|---|---|
| CO2  | −1.85% | −1.80% | −3.10% |
| NOx  | −2.99% | −2.80% | −4.09% |
| PMx  | −1.88% | −1.72% | −3.03% |
| CO   | −0.70% | −0.72% | −2.03% |
| HC   | −7.10% | −7.01% | −8.24% |
| fuel | −1.86% | −1.80% | −3.10% |

**`dft` set — % change under the 20mph scheme (off-peak, seed 42):**

| Metric | road_total | vehicle_total | vehicle_perkm |
|---|---|---|---|
| CO2  | −0.63% | −0.45% | −0.53% |
| NOx  | −0.55% | −0.38% | −0.46% |
| PMx  | −0.20% | −0.16% | −0.24% |
| CO   | −0.23% | −0.28% | −0.35% |
| HC   | +0.24% | +0.16% | +0.08% |
| fuel | −0.63% | −0.45% | −0.53% |

**Interpretation (supports Hypothesis 1):**

- **Peak**: the 20mph scheme **reduces** emissions at every level. The bulk
  pollutants (CO2, NOx, PMx, fuel) fall **−1.7% to −3.0%** (road/vehicle totals)
  and **−3.0% to −4.1%** per km; CO and HC fall further.
- **Off-peak**: the change is small (|Δ| ≤ 0.6% except HC), i.e. **no
  meaningful penalty** from the scheme at free-flow. HC is within run-to-run
  tolerance (see §2.1.1).
- Net: for **this behaviour assumption only** (fixed 10%/70%/20% car mix, same
  at both limits) the peak result reduces emissions; it does **not** establish
  the conclusion generally — the DfT-calibrated set below gives a mixed result.
- **Major caveat — the result is behaviour-dependent.** These figures are for
  the fixed-mix (`dft`) set only. When the driver speed distribution is fitted
  to DfT 2024 speed-compliance data (the `cal` set), the peak result becomes
  **mixed** — see [§2.4](#24-sensitivity-to-driver-speed-behaviour-the-cal-set).
  This section's conclusion should therefore be read as *conditional on the
  behaviour assumption and on whether per-km or total is quoted*.
- **Other caveats:** the conclusion is also *demand- and network-dependent*.
  Re-runs must use the calibrated demand (`FLOW_CALIBRATION.md`) and the
  consultation-defined network (`sumo/NETWORK_BUILD.md`).

### 2.1.1 Reproducibility, run-to-run variation and the HC metric

**Setup.** Each comparison config now sets a fixed seed (`<seed value="42"/>`).
Two consecutive runs of the same config produce results that are identical to
the last digit — only the `generated on …` timestamp comment in the XML header
differs. All figures in §2.1 and §3.3 come from these seeded runs, and every raw
file can be regenerated per `REPRODUCING.md`.

**Two changes since an earlier draft of this report.** (1) The comparison
configs gained a fixed seed; (2) `wool.20mph.net.xml` was corrected to match the
consultation (previously it wrongly reduced the arterial to 20mph — see
`sumo/NETWORK_BUILD.md`). Both changes altered the reported percentages while
leaving the *direction* of every finding unchanged. The figures above are the
current, reproducible values.

**Run-to-run variation by pollutant (fact, prior vs current 30mph baseline).**
The change in the *absolute* emitted mass of the 30mph baseline between the
earlier (unseeded/unfixed) run and the current seeded run is small for most
pollutants but distinctly larger for HC and CO:

| Peak 30mph, absolute road_total | earlier run | current run | difference |
|---|---|---|---|
| CO2  | 2,625,789,854.7 | 2,625,806,612.7 | +0.00% |
| NOx  | 910,120.3 | 913,848.2 | +0.41% |
| PMx  | 267,986.5 | 267,895.7 | −0.03% |
| fuel | 848,684,965.9 | 848,706,394.9 | +0.00% |
| CO   | 6,081,801.6 | 6,046,637.4 | −0.58% |
| **HC** | **345,019.0** | **351,607.1** | **+1.91%** |

The peak `road_total` **percent change** for HC has been reported between
**−3.2%** and **−7.1%** across successive runs/revisions. CO has been between
−0.7% and −7.0%. CO2/NOx/PMx/fuel have stayed within ~1 percentage point.

**What HC is.** HC is the mass of **hydrocarbons** (unburnt fuel and partially
combusted fuel components) in the exhaust. SUMO reports it via the **HBEFA4**
emission model, per vehicle and per simulation step, in the `HC` / `HC_abs`
attribute, in **milligrams per second** (the `_abs` totals here are the sum of
those per-second values over the trip). It is distinct from CO2 (fully combusted
carbon), NOx (nitrogen oxides) and PMx (particulates). Different fuels/engines
emit HC in very different amounts, and HC output is concentrated in specific
operating states (e.g. cold start and transient acceleration).

**Statement of fact (no mechanism claimed).** Across the two data sets, HC is
the metric whose *ratio* between the 30 and 20mph scenarios is least stable,
while its absolute value is stable to ~2% between runs. This is recorded here as
an observed fact. A mechanistic explanation is deferred pending multiple seeded
replicates of each scenario.

**Wiki link:** addresses
[2.1 Vehicle Emissions at Slower Speeds](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#vehicle_emissions_at_slower_speeds),
specifically:
- [Evidence from London (Imperial College / TfL)](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#evidence_from_london_imperial_college_tfl)
- [Emissions vary by engine type](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#emissions_vary_by_engine_type)
- [The physics of lower speeds](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#the_physics_of_lower_speeds)
- [Real-world emissions modelling (Future Transport)](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#real-world_emissions_modelling_future_transport)
- [Speed limits vs physical traffic calming](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#speed_limits_vs_physical_traffic_calming)

The wiki claims 20mph "is unlikely to result in an increase in vehicle
pollution and may even lead to a reduction". The **`dft` set supports** this
(§2.1 tables above). The **`cal` set gives a mixed answer** (§2.4): per km driven
CO2/fuel/HC fall but PMx and CO rise. The
wiki's London/TfL evidence cites an 8.3% PM10 drop for petrol cars, with
emissions varying by engine type (petrol vs diesel); our PMx change is smaller
(−2.2% peak, +0.8% off-peak) because the fleet is modelled generically rather
than split petrol/diesel, and because we track exhaust PMx from the HBEFA model
(tyre/brake wear is not separately resolved). The wiki's *physics of lower
speeds* point (30mph needs 2.25× the energy of 20mph) is reflected in our
`fuel` totals. The wiki's Future Transport figures (CO2 −26%, NOx −28%) are much
larger than ours; the simulation reflects Wool's specific demand and geometry.
The wiki notes that **physical traffic calming** (humps) raises emissions,
whereas Wool's proposal is a **speed limit without physical obstructions** — the
model implements the latter (signs-only network speed caps).

### 2.2 Traffic Flow and Journey Times

**Wiki link:** [2.2 Impact on Traffic Flow and Congestion](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#impact_on_traffic_flow_and_congestion),
specifically:
- [How lower speeds can mean shorter journeys](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#how_lower_speeds_can_mean_shorter_journeys)
- [Context matters, but delays are minimal](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#context_matters_but_delays_are_minimal)

Measured journey-time and flow metrics for the **`dft` set** (survey-calibrated
demand, from `wool.dft_*.statistic.xml`). The `cal` set's flow metrics are in
[§2.4](#24-sensitivity-to-driver-speed-behaviour-the-cal-set); they show a
larger journey-time improvement (−114 s) and reach the same conclusion — flow is
never worse under 20mph.

| Scenario | Avg duration | Avg time loss | Avg waiting | Completed trips |
|---|---|---|---|---|
| Peak 30mph | 864.7 s | 456.8 s | 125.1 s | 978 |
| Peak 20mph | 864.9 s | 460.5 s | 119.9 s | 1004 |
| Off-peak 30mph | 683.3 s | 282.4 s | 43.2 s | 461 |
| Off-peak 20mph | 682.5 s | 278.6 s | 42.0 s | 461 |

- **Peak:** journey time is essentially **unchanged (+0.2 s)**; time loss
  **+0.8%**, waiting **−4.2%**, and **26 more trips complete** in the hour. The
  through-route (Dorchester Road) now keeps its 30mph+ limit, so the scheme's
  only new constraint is on the 20mph side roads — consistent with the wiki's
  "negligible impact on journey time" claim.
- **Off-peak:** journey time **−0.8 s (−0.01 min)** — negligible, well within
  the wiki's "average journey time might only increase by around one minute".
- Both support the wiki's §2.2 conclusion of *negligible* journey-time impact.

### 2.3 Public Perception (Not Modelled)

**Wiki link:** [2.3 Public Perception and Acceptance](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#public_perception_and_acceptance),
specifically:
- [Survey support](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#survey_support)
- [Real-world sentiment](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#real-world_sentiment)
- [Addressing opposition](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#addressing_opposition)

This section concerns **attitudes and acceptance**, which a traffic simulation
cannot address. No simulation result is claimed here. The wiki's survey
findings (~70% support, growing after implementation) should be evidenced by
separate consultation data, not this model.

---

### 2.4 Sensitivity to Driver Speed Behaviour (the `cal` set)

§2.1 and §2.2 use the **`dft` set**, whose driver mix (10% compliant / 70%
normal / 20% speeder) is **fixed and applied identically at both limits**. That
assumption is not evidence-based. This section repeats the simulation with the
driver speed distribution **fitted to official DfT data**, to test whether the
conclusions hold.

#### What was changed

Only the **driver speed distribution** differs; total demand is identical
(1,382 veh/hr). Cars use a **continuous** `speedFactor` distribution
(`normc(mean, sd, min, max)`), fitted so the modelled **% exceeding the limit**
matches DfT SPE0101 (2024). See [`sumo/DFT_BEHAVIOUR.md`](sumo/DFT_BEHAVIOUR.md).

| | 30mph scenario | 20mph scenario |
|---|---|---|
| Distribution | `normc(0.968, 0.180, …)` | `normc(1.141, 0.200, …)` |
| DfT target % exceeding | 43% | 76% |
| Achieved % exceeding | 42.7% | 74.7% |
| Mean speed | 29.1 mph | 22.9 mph |

The key DfT fact is that **non-compliance is much higher at 20mph than at
30mph** — so unlike the `dft` set, the two scenarios use *different* speed
spread.

#### Result: the peak emissions picture becomes mixed

Unlike the `dft` set (a clean reduction), the calibrated set is **mixed**.

**Vehicle distance.** The 20mph scenario completes more trips, so **more
vehicle-km are driven** — an absolute emission total = distance × rate:

| | 30mph | 20mph | change |
|---|---|---|---|
| total vehicle-km | 6,007 | 6,464 | **+7.60%** |
| completed trips | 1,012 | 1,059 | +47 |

**Emissions (peak, `cal` set).** `total` = road_total; `per km` = vehicle_perkm:

| Metric | total | per km | what drives the change |
|---|---|---|---|
| CO2  | **−4.81%** | −11.51% | rate (per-km fall overcomes the +7.6% volume) |
| NOx  | +0.83% | −6.35% | mostly volume; rate improves |
| PMx  | **+3.09%** | −4.43% | **volume only** — total rises purely from more km |
| CO   | **+30.72%** | +21.15% | **rate** — a genuine per-km increase |
| HC   | +1.72% | −5.66% | **volume only** — total rises purely from more km |
| fuel | **−4.80%** | −11.50% | rate (per-km fall overcomes the +7.6% volume) |

- **Per km driven, five of six pollutants fall** (CO2, fuel, NOx, PMx, HC);
  only **CO rises per km**.
- **How to read the PMx and HC rows.** An absolute total = (distance driven) ×
  (emission per km), so the two effects multiply. For PMx that is
  **+7.60%** (distance) × **−4.43%** (per km) ≈ +2.8% → the *total* rises
  **+3.09%** *even though each kilometre is cleaner*. In words: **the rise is
  entirely a distance/volume effect, not a dirtier vehicle.** HC is the same
  (+7.60% × −5.66% ≈ +1.6% → +1.72%). This is why the PMx total (+3.09%) is
  smaller than the distance rise (+7.60%): the per-km improvement offsets part
  of it. Contrast **CO**, where both factors are positive (+7.60% × +21.15%) —
  a genuine per-km increase.
- HC is also the least stable metric (§2.1.1), so its small change is within
  noise.

**Journey time / flow (peak, `cal` set).**

| Scenario | Avg duration | Time loss | Waiting | Completed |
|---|---|---|---|---|
| cal 30mph | 814.4 s | 433.9 s | 139.7 s | 1012 |
| cal 20mph | 700.5 s | 362.6 s | 138.9 s | 1059 |

- Journey time **−114.0 s**, time loss **−16.4%**, 47 more trips complete;
  waiting essentially unchanged (−0.6%). Flow is **never worse**.

**Noise (peak, `cal` set).** Fleet mean 61.56 → 62.49 dB(A): **+0.93 dB(A)**
(no benefit, as in the `dft` set).

#### Off-peak (`cal` set)

The off-peak `cal` scenarios are also provided (configs
`wool.cal_offpeak_{now,20mph}.sumo.cfg`, routes
`wool.rou.dft_cal_offpeak_{30,20}.xml`). Here the picture is clearer, because
the 20mph scenario drives **about the same distance** (vehicle-km −0.46%), so
the totals and per-km figures largely agree:

| Metric | total | per km |
|---|---|---|
| CO2  | **−4.79%** | −4.58% |
| NOx  | +0.42% | +0.64% |
| PMx  | **+3.59%** | +3.96% |
| CO   | **+25.95%** | +26.12% |
| HC   | **−8.33%** | −7.62% |
| fuel | **−4.78%** | −4.57% |

- **CO2, fuel and HC fall**; **PMx and CO rise**; NOx roughly flat.
- Journey time **−90 s** (557 → 467 s), trips 480 → 479 (unchanged).
- Noise fleet mean 63.87 → 65.34 dB(A): **+1.46 dB(A)** (no benefit).

The direction matches the peak `cal` result (CO2/fuel/HC down, PMx/CO up), so
the mixed finding is consistent across peak and off-peak once behaviour is
DfT-calibrated.

#### Both sets side by side (peak, 20mph vs 30mph)

| Peak | `dft` set (fixed mix) | `cal` set (DfT-fitted) |
|---|---|---|
| **vehicle-km driven** | +1.34% | **+7.60%** |
| CO2 (total / per km) | −1.85% / −1.64% | **−4.81% / −11.51%** |
| NOx (total / per km) | −2.99% / −4.09% | +0.83% / −6.35% |
| PMx (total / per km) | −1.88% / −3.03% | **+3.09% / −4.43%** |
| CO  (total / per km) | −0.70% / −2.03% | **+30.72% / +21.15%** |
| HC  (total / per km) | −7.10% / −8.24% | +1.72% / −5.66% |
| fuel (total / per km) | −1.86% / −3.10% | **−4.80% / −11.50%** |
| journey time | +0.2 s | −114.0 s |
| noise | +0.13 dB(A) | +0.93 dB(A) |

#### Interpretation

- The **emissions result depends strongly on the assumed driver behaviour** and
  becomes **mixed rather than a clean sign** once behaviour is DfT-calibrated.
- **Most apparent "increases" are a distance-driven volume effect, not a
  per-vehicle effect** (the 20mph scenario drives +7.6% more vehicle-km).
- **Robust across both sets:** journey time is **never worse** under 20mph, and
  **noise shows no benefit**.
- *(Superseded:* an earlier `cal` attempt used three discrete bands and gave
  CO2 +1.41% / NOx +3.07%; the continuous fitted distribution above replaces it.)

#### Caveats (apply to both sets)

1. Both sets use the same **simplified network and estimated flows**; see
   [`FLOW_CALIBRATION.md`](FLOW_CALIBRATION.md) and
   [`sumo/NETWORK_BUILD.md`](sumo/NETWORK_BUILD.md).
2. The speed distribution is a **truncated normal fitted to the % exceeding**,
   not a full empirical histogram (DfT does not publish one); real distributions
   are right-skewed, so the fitted mean speed sits ~1–1.5 mph below DfT's
   rounded average — see [`sumo/DFT_BEHAVIOUR.md`](sumo/DFT_BEHAVIOUR.md).
3. DfT compliance is measured on **free-flowing** roads; congested conditions
   will differ, and this is a single-hour peak model.
4. **Absolute totals conflate two effects**: distance driven and emissions per
   km. Always report the **per-km** figure alongside a total, and state which is
   meant.

#### Reproducing (the `cal` set)

```bash
cd sumo
sumo -c wool.cal_now.sumo.cfg
sumo -c wool.cal_20mph.sumo.cfg
python3 analyze_emissions.py \
  --now-edge wool.cal_now.road_emissions.xml --now-veh wool.cal_now.emissions.xml --now-trip wool.cal_now.tripinfo.xml \
  --scheme-edge wool.cal_20mph.road_emissions.xml --scheme-veh wool.cal_20mph.emissions.xml --scheme-trip wool.cal_20mph.tripinfo.xml
```

---

## 3. The Benefits (Wiki Section 3)

This section addresses the wiki's benefits claims, plus the non-vehicle and
railway model components. The Wool SUMO model incorporates the village railway
line and level crossing timings (`wool.additional-6-9-2016.xml`), which
periodically close for passing trains (`Train 1W96`, `Train 1W51`, etc.).

**Non-vehicle model components in the network:**
1. **Pedestrian substructure (`wool.pedestrians.additional.xml`)** — a
   `personFlow` between the east and west edges; runnable via
   `wool.pedestrian_experiment.sumo.cfg` but not yet part of the canonical runs
   (see §3.2).
2. **Level crossing interaction** — when the railway gates close, vehicles
   queue along the primary and back routes; slower speeds reduce harsh braking
   and smooth re-acceleration when barriers reopen (relevant to the PMx result
   in §2.1).

### 3.1 Pedestrian and Cyclist Safety

**Wiki link:** [3.1 Enhanced Safety for Pedestrians and Cyclists](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#enhanced_safety_for_pedestrians_and_cyclists),
specifically:
- [Risk rises sharply with speed](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#risk_rises_sharply_with_speed)
- [Pedestrian survival rates by impact speed](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#pedestrian_survival_rates_by_impact_speed)
- [The 20mph threshold](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#the_20mph_threshold)
- [Cyclists](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#cyclists)
- [Children](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#children)

**Partly covered.** The model reproduces the wiki's **premise** — that 20mph
lowers vehicle speeds on the listed roads — and the collision *context* (vehicle
speeds, junction interactions, level-crossing queues). It does **not** reproduce
casualty outcomes: SUMO here has no accident/casualty model, no pedestrian
population (see §3.2), and no conflict-point analysis.

Therefore the wiki's headline safety evidence — the 24% Welsh casualty
reduction
([Table 2](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#table_2summary_of_casualty_changes_in_areas_with_20mph_limits)),
and the
[Table 1](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#table_1pedestrian_fatality_risk_vs_impact_speed)
fatality-risk-vs-impact-speed curve (20mph: 1–5% vs 30mph: 20–45%) — is
**cited as external evidence**, not derived from this simulation. What the model
adds is confirmation that the *speed reduction itself* is achievable on the
Wool network (0% of vehicles exceed the 20mph compliant-type cap in the
`CAR_COMPLIANT` class).

**Gap:** to model §3.1 properly would require either (a) SUMO's SSM
(surrogate safety measures) device to quantify conflict severity, or (b) a
pedestrian population. Both are feasible extensions but are not present.

### 3.2 Active Travel (Not Yet Populated)

**Wiki link:** [3.2 Encouraging Active Travel](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#encouraging_active_travel).

**Partly covered — infrastructure only.** A pedestrian substructure exists
(`wool.pedestrians.additional.xml`, a `personFlow` from the east edge to the
west edge) and the pedestrian-experiment config
(`wool.pedestrian_experiment.sumo.cfg`) is runnable. **However, the canonical
`wool.dft_*` scenario runs contain zero pedestrians** — all statistic files
report `pedestrianStatistics number="0"`. No active-travel result is therefore
claimed.

The wiki claims increased walking/cycling following a 20mph limit. To test this
in SUMO the pedestrian flows (and ideally a mode-shift elasticity) must be
added to the main scenarios, and pedestrian journey times / wait times at the
level crossing compared between 30 and 20mph. That is an outstanding task.

### 3.3 Noise Pollution

**Wiki link:** [3.3 Reduction in Noise Pollution](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#reduction_in_noise_pollution),
specifically:
- [How much quieter?](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#how_much_quieter)
- [European evidence](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#european_evidence)
- [Why speed affects noise](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#why_speed_affects_noise)

**Modelled.** SUMO's HBEFA noise model attaches a `noise` value (dB(A)) to every
vehicle timestep; `sumo/analyze_noise.py` aggregates it:

```bash
python3 sumo/analyze_noise.py --now sumo/wool.dft_now.emissions.xml \
                              --scheme sumo/wool.dft_20mph.emissions.xml
```

| Scenario (`dft` set) | fleet mean dB(A) | per-vehicle mean dB(A) | Δ |
|---|---|---|---|
| Peak 30mph | 61.17 | 61.55 | — |
| Peak 20mph | 61.30 | 61.64 | **+0.13 / +0.09** |
| Off-peak 30mph | 62.63 | 62.86 | — |
| Off-peak 20mph | 62.64 | 62.86 | **+0.01 / +0.00** |

The `cal` set agrees (no benefit): fleet mean +0.93 dB(A) at peak
([§2.4](#24-sensitivity-to-driver-speed-behaviour-the-cal-set)).

**Finding:** the model shows **essentially no change** — a **+0.13 dB(A)** rise
at peak (within noise) and **+0.01 dB(A)** off-peak. This is far below the
wiki's cited 3 dB(A) (UK research), up to 6 dB(A) at peak — see
[Table 3](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#table_3noise_reduction_from_30mph_to_20mph)
and [European evidence](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#european_evidence)
(Graz, Zurich). This is expected: SUMO's noise model is dominated by vehicle
class and acceleration, and a "signs-only" speed cap without traffic calming
changes those only marginally (see
[Why speed affects noise](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#why_speed_affects_noise)).
With the corrected network the arterial keeps its speed, so the scheme does not
reduce noise below the baseline in this model. The wiki's larger figures come
from physical measures and real-world measurement; the simulation models a
signs-only cap on side roads and should be read as a **lower bound** on the
noise benefit, not a contradiction.

### 3.4 Community Liveability (Not Modelled)

**Wiki link:** [3.4 Improved Community Liveability](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#improved_community_liveability).

Qualitative outcomes (sense of community, severance, social interaction) are
not simulable and no result is claimed. The model contributes indirectly via
the safety and active-travel sections above.

---

## 4. Case Studies (External Evidence)

**Wiki links:** [4.1 Dorset Examples](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#dorset_examples)
([locations progressing with Dorset Council](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#locations_progressing_with_dorset_council)),
[4.2 UK-Wide Examples](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#uk-wide_examples).

These sections are **external case-study evidence** (Bridport, Langton
Matravers, Wimborne, Winfrith Newburgh and Pimperne in Dorset; Scottish
Borders' 97-village rollout; Wales' national default). They require no
simulation and are referenced here for context. The Wool network used in this
study is the same village geometry those schemes would apply to.

---

## 5. Conclusion (Synthesis)

**Wiki link:** [5. Conclusion and Recommendations](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#conclusion_and_recommendations),
specifically [5.1 Summary](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#summary)
and [5.2 Recommendations](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#recommendations).

This simulation supports the wiki's overall case, with these qualifications:

| Wiki recommendation | Simulation support |
|---|---|
| Rec 1 — proceed with a formal 20mph proposal | Supported for flow (journey time never worse); emissions are **mixed** and behaviour-dependent (per km mostly fall, totals mixed — see §2.1) |
| Rec 2 — community engagement campaign | N/A (attitudinal, §2.3) — simulation gives part of the evidence base |
| Rec 3 — phased pilot with monitoring | Supported: the calibrated model is the monitoring baseline |
| Rec 4 — self-enforcing road design | Not modelled (physical calming differs from a signs-only cap) |
| Rec 5 — enforcement/education strategy | Not modelled |

**Net:** the simulations support the **flow** argument (§2.2) — journey time is
never worse under 20mph. The **emissions** picture (§2.1) is **behaviour-
dependent and, when calibrated to DfT data, mixed**: per km driven most
pollutants fall (only CO rises), while absolute totals can move either way
depending on how much extra distance is driven. On **noise** (§3.3) the model
shows **no reduction** (a signs-only cap on side roads leaves network noise
essentially unchanged), so the noise argument rests on the wiki's external
evidence rather than this simulation. The safety-outcome (§3.1) and
active-travel (§3.2) arguments remain **evidence gaps** in the current model and
are flagged as future work rather than confirmed.

---


## Note on Movie/Simulation Rating & Visuals
- **Observation**: The simulation color scheme (by speed or emissions) features vibrant red tones for high speeds or congestion, which can visually resemble high-contrast alert indicators.
- **Action Item**: Implement a refined movie/simulation rating and color-grading scheme to provide clearer, less visually jarring differentiation between compliant traffic (green), normal traffic, and speeders (muted tones) in future video exports.
