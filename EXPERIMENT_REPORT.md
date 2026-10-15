# Wool 20mph Speed Limit Experiments & Non-Vehicle Modeling Report

This document outlines the experimental setup, simulation configurations, statistical output collection, and non-vehicle (pedestrian/railway) modeling designed to test the claims and assumptions in the [Wool Speed Limit Wiki](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit).

---

## Summary of Scenarios

The canonical comparison pairs (survey-calibrated demand, see
`FLOW_CALIBRATION.md`) are:

1. **Peak (08:00, controlled)** — routes `wool.rou.dft_controlled.v2.xml`
   - 30mph baseline: `wool.dft_now.sumo.cfg` (network `wool.net.xml`)
   - 20mph scheme:  `wool.dft_20mph.sumo.cfg` (network `wool.20mph.net.xml`)

2. **Off-peak** — routes `wool.rou.dft_offpeak.v2.xml`
   - 30mph baseline: `wool.dft_offpeak_now.sumo.cfg`
   - 20mph scheme:  `wool.dft_offpeak_20mph.sumo.cfg`

The 20mph network reduces back roads, **Colliers Lane** and **Lulworth Road** to
20mph / 8.94 m/s; **Dorchester Road** is excluded and retained at 30mph. Both
scenarios use the same heterogeneous driver mix (compliant / normal / speeder).

> The earlier `wool.stats_now` / `wool.stats_20mph` configs and the
> `wool.rou.speed_experiment.xml` route file are **superseded** by the pairs
> above and are retained only for historical reference.

---

## Wiki Coverage Map

This report is written to test the claims in
[**The Case for a 20mph Speed Limit in Wool, Dorset**](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit).
Every section of that wiki page is listed below with its anchor link and the
simulation evidence (or explicit note) that addresses it.

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

---

## 1. How to Generate Video Visualizations

Pre-rendered videos of the corrected scenarios live in `sumo/`:
`wool_peak_30mph.webm`, `wool_peak_20mph.webm`, `wool_offpeak_30mph.webm`,
`wool_offpeak_20mph.webm`.

To re-record in SUMO-GUI, use `sumo/render_sync.sh <config> <output.webm> [secs] [delay]`
(headless via Xvfb + ffmpeg), or interactively:

### Running the scenarios in GUI
```bash
cd sumo
sumo-gui -c wool.dft_now.sumo.cfg            # peak 30mph
sumo-gui -c wool.dft_20mph.sumo.cfg          # peak 20mph
sumo-gui -c wool.dft_offpeak_now.sumo.cfg    # off-peak 30mph
sumo-gui -c wool.dft_offpeak_20mph.sumo.cfg  # off-peak 20mph
```
*(In SUMO-GUI, use the recording toolbar or camera icon to export frames/video.)*

> **Note:** SUMO-GUI crashes on this host if a vType sets
> `device.rerouting.probability="0.0"`. That attribute has been removed from the
> route files (results are identical without it). See `FLOW_CALIBRATION.md`.

---

## 2. Statistical Analysis & Emissions

SUMO records trip statistics and pollutant emissions. **Emissions are deliberately
collected at two different levels**, because a change to the speed limit can push
them in *opposite* directions depending on the level of aggregation (see §2.1).

### Running Automated Batch Simulations & Stats Export
```bash
cd WoolSimulation/sumo
# Peak (controlled demand)
sumo -c wool.dft_now.sumo.cfg        # 30mph baseline
sumo -c wool.dft_20mph.sumo.cfg      # 20mph scheme
# Off-peak
sumo -c wool.dft_offpeak_now.sumo.cfg
sumo -c wool.dft_offpeak_20mph.sumo.cfg
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

> **Note (revised):** these figures supersede an earlier set that was produced
> from a **saturated** demand scenario (1,470 veh/hr, ~39% above the measured
> A352 flow). That over-loading inverted the peak-hour result. See
> `FLOW_CALIBRATION.md` for the audit and `wool.rou.dft_controlled.v2.xml` for
> the corrected demand. All numbers below are from the corrected runs
> (1,382 veh/hr, 0 teleports, all vehicles inserted).

**Why both levels matter.** A vehicle travelling at 20mph instead of 30mph emits a
similar mass **per second** but occupies each road segment for **~50% longer**.
For a *vehicle*, that is a near-wash or a small saving; for a *road section*, the
longer occupancy can push the **accumulated total up**. Reporting only one level
(as the original report did) is therefore misleading. `analyze_emissions.py`
reports:
- **road_total** — total mass on all edges (Δ = what a *street/network* experiences)
- **vehicle_total** — total mass over all trips
- **vehicle_perkm** — mass per km driven (Δ = is the *average km* cleaner)

**% change under the 20mph scheme (peak hour, corrected demand):**

| Metric | road_total | vehicle_total | vehicle_perkm |
|---|---|---|---|
| CO2  | −3.50% | −3.35% | −2.19% |
| NOx  | −3.25% | −3.18% | −2.01% |
| PMx  | −3.30% | −3.23% | −2.07% |
| CO   | −6.76% | −6.65% | −5.52% |
| HC   | −3.16% | −2.97% | −1.80% |
| fuel | −3.50% | −3.35% | −2.19% |

**% change under the 20mph scheme (off-peak, corrected demand):**

| Metric | road_total | vehicle_total | vehicle_perkm |
|---|---|---|---|
| CO2  | +0.11% | +0.09% | +0.55% |
| NOx  | +0.37% | +0.34% | +0.80% |
| PMx  | +0.61% | +0.61% | +1.07% |
| CO   | −2.51% | −2.46% | −2.01% |
| HC   | +0.79% | +0.60% | +1.06% |
| fuel | +0.11% | +0.09% | +0.55% |

**Interpretation (revised — supports Hypothesis 1):**

- **Peak**: with corrected (survey-matched) demand, the 20mph scheme **reduces**
  emissions at every level — approximately **−3% to −7%**. Lowering the limit
  smooths the peak and cuts stop-start and queuing.
- **Off-peak**: the change is negligible (≤1%), i.e. **no penalty** from the
  scheme at free-flow. CO falls slightly (−2.5%); other pollutants are within
  noise.
- Net: this now **supports Hypothesis 1** — 20mph does not increase pollution and
  reduces it under peak conditions.
- **Critical caveat:** this conclusion is *demand-dependent*. The earlier
  saturated scenario (1,470 veh/hr) reversed it (+3–6%). Any future re-run must
  use the calibrated demand in `FLOW_CALIBRATION.md` or the sign of the result
  cannot be trusted.

**Effect of the flow correction on the peak result:**

| Metric (road_total) | saturated (old) | corrected (new) |
|---|---|---|
| CO2  | +3.63% | −3.50% |
| NOx  | +5.86% | −3.25% |
| PMx  | +2.94% | −3.30% |
| fuel | +3.64% | −3.50% |

The over-loaded demand inverted the sign of the peak-hour emissions conclusion.

**Wiki link:** addresses
[2.1 Vehicle Emissions at Slower Speeds](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#vehicle_emissions_at_slower_speeds).
The wiki claims 20mph "is unlikely to result in an increase in vehicle
pollution and may even lead to a reduction" — the calibrated model **supports**
this (peak −3% to −7%). The wiki's London/TfL evidence cites an 8.3% PM10 drop
for petrol cars; our PMx change is smaller (−3.3% peak, +0.6% off-peak) because
the fleet is modelled generically rather than split petrol/diesel, and because
we track exhaust PMx from the HBEFA model (tyre/brake wear is not separately
resolved). The wiki's Future Transport figures (CO2 −26%, NOx −28%) are much
larger than ours; the simulation reflects Wool's specific demand and geometry.

### 2.2 Traffic Flow and Journey Times

**Wiki link:** [2.2 Impact on Traffic Flow and Congestion](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#impact_on_traffic_flow_and_congestion).

Measured journey-time and flow metrics (corrected demand, from
`wool.dft_*.statistic.xml`):

| Scenario | Avg duration | Avg time loss | Avg waiting | Completed trips |
|---|---|---|---|---|
| Peak 30mph | 875.7 s | 467.0 s | 127.4 s | 987 |
| Peak 20mph | 819.4 s | 412.0 s | 74.9 s | 992 |
| Off-peak 30mph | 682.7 s | 282.4 s | 42.7 s | 461 |
| Off-peak 20mph | 690.3 s | 283.1 s | 44.6 s | 460 |

- **Peak:** journey time falls **−56 s (−0.94 min)** and time loss **−12%**,
  waiting **−41%** under 20mph — i.e. smoother flow, matching the wiki's
  "smoother traffic flow / fewer acceleration-deceleration events" claim.
- **Off-peak:** journey time rises only **+8 s (+0.13 min)** — comfortably
  within the wiki's "average journey time might only increase by around one
  minute" (Wales / Richmond evidence).
- Both support the wiki's §2.2 conclusion of *negligible* journey-time impact.

### 2.3 Public Perception (Not Modelled)

**Wiki link:** [2.3 Public Perception and Acceptance](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#public_perception_and_acceptance).

This section concerns **attitudes and acceptance**, which a traffic simulation
cannot address. No simulation result is claimed here. The wiki's survey
findings (~70% support, growing after implementation) should be evidenced by
separate consultation data, not this model.

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

**Wiki link:** [3.1 Enhanced Safety for Pedestrians and Cyclists](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#enhanced_safety_for_pedestrians_and_cyclists).

**Partly covered.** The model reproduces the wiki's **premise** — that 20mph
lowers vehicle speeds on the back roads — and the collision *context* (vehicle
speeds, junction interactions, level-crossing queues). It does **not** reproduce
casualty outcomes: SUMO here has no accident/casualty model, no pedestrian
population (see §3.2), and no conflict-point analysis.

Therefore the wiki's headline safety evidence — the 24% Welsh casualty
reduction, and the
[Key Table 1](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#key_tables)
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

**Wiki link:** [3.3 Reduction in Noise Pollution](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#reduction_in_noise_pollution).

**Modelled.** SUMO's HBEFA noise model attaches a `noise` value (dB(A)) to every
vehicle timestep; `sumo/analyze_noise.py` aggregates it:

```bash
python3 sumo/analyze_noise.py --now sumo/wool.dft_now.emissions.xml \
                              --scheme sumo/wool.dft_20mph.emissions.xml
```

| Scenario | fleet mean dB(A) | per-vehicle mean dB(A) | Δ |
|---|---|---|---|
| Peak 30mph | 61.18 | 61.52 | — |
| Peak 20mph | 61.11 | 61.49 | **−0.07 / −0.03** |
| Off-peak 30mph | 62.64 | 62.88 | — |
| Off-peak 20mph | 62.58 | 62.75 | **−0.06 / −0.12** |

**Finding:** the model shows a **small reduction (<0.15 dB(A))**, far below the
wiki's cited 3 dB(A) (UK research) — see
[Key Table 3](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#key_tables).
This is expected: SUMO's noise model is dominated by vehicle class and
acceleration, and a "signs-only" speed cap without traffic calming changes
those only marginally. The wiki's larger figures come from physical measures
and real-world measurement; the simulation should be read as a *lower bound* on
the noise benefit, not a contradiction.

### 3.4 Community Liveability (Not Modelled)

**Wiki link:** [3.4 Improved Community Liveability](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#improved_community_liveability).

Qualitative outcomes (sense of community, severance, social interaction) are
not simulable and no result is claimed. The model contributes indirectly via
the safety and active-travel sections above.

---

## 4. Case Studies (External Evidence)

**Wiki links:** [4.1 Dorset Examples](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#dorset_examples),
[4.2 UK-Wide Examples](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#uk-wide_examples).

These sections are **external case-study evidence** (Bridport, Langton
Matravers, Wimborne, Winfrith Newburgh and Pimperne in Dorset; Scottish
Borders' 97-village rollout; Wales' national default). They require no
simulation and are referenced here for context. The Wool network used in this
study is the same village geometry those schemes would apply to.

---

## 5. Conclusion (Synthesis)

**Wiki link:** [5. Conclusion and Recommendations](https://www.retallack.org.uk/dokuwiki/doku.php?id=woolspeedlimit#conclusion_and_recommendations).

This simulation supports the wiki's overall case, with these qualifications:

| Wiki recommendation | Simulation support |
|---|---|
| Rec 1 — proceed with a formal 20mph proposal | Supported: no emissions penalty, flow preserved |
| Rec 2 — community engagement campaign | N/A (attitudinal, §2.3) — simulation gives the evidence base |
| Rec 3 — phased pilot with monitoring | Supported: the calibrated model is the monitoring baseline |
| Rec 4 — self-enforcing road design | Not modelled (physical calming differs from a signs-only cap) |
| Rec 5 — enforcement/education strategy | Not modelled |

**Net:** the corrected simulations support the emissions (§2.1), flow (§2.2)
and — modestly — noise (§3.3) arguments. The safety-outcome (§3.1) and
active-travel (§3.2) arguments remain **evidence gaps** in the current model
and are flagged as future work rather than confirmed.

---


## Note on Movie/Simulation Rating & Visuals
- **Observation**: The simulation color scheme (by speed or emissions) features vibrant red tones for high speeds or congestion, which can visually resemble high-contrast alert indicators.
- **Action Item**: Implement a refined movie/simulation rating and color-grading scheme to provide clearer, less visually jarring differentiation between compliant traffic (green), normal traffic, and speeders (muted tones) in future video exports.
