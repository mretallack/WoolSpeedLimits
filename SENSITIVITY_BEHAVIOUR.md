# Sensitivity Analysis: Driver Speed Behaviour (`dft_cal` set)

This document reports a **sensitivity test** on the main result. It asks: does
the "20mph has no negative effect" conclusion hold when driver behaviour is
calibrated to real DfT speed-compliance data?

**Answer: no — the emissions result reverses.** Journey times still improve
slightly, but emissions *increase* under 20mph once realistic non-compliance is
modelled.

## What was changed

Only the **driver speed distribution** changed between the two scenarios,
fitted to DfT SPE0101 (2024). Total demand is identical (1,382 veh/hr). Cars use
a continuous `normc` speed-factor distribution; see `sumo/DFT_BEHAVIOUR.md`.

| | 30mph scenario | 20mph scenario |
|---|---|---|
| Distribution | `normc(0.968,0.180,…)` | `normc(1.141,0.200,…)` |
| DfT target % exceeding | 43% | 76% |
| Achieved % exceeding | 42.7% | 74.7% |
| Mean speed | 29.1 mph | 22.9 mph |

## Vehicle distance drove more under 20mph

In this calibrated run the 20mph scenario **completes more trips** (journey
times are lower), so **more vehicle-km are driven in the hour**:

| | 30mph | 20mph | change |
|---|---|---|---|
| total vehicle-km | 6,007 | 6,464 | **+7.60%** |
| completed trips | 1,012 | 1,059 | +47 |

This matters: an absolute emissions total = (distance driven) × (emission per km).
A **+7.6% rise in distance alone raises every absolute total by ~7.6%**, even
where the per-km rate improves.

## Emissions (peak, 20mph vs 30mph)

`total` is road_total; `per km` is vehicle_perkm. The right-hand columns show
whether the change is a **rate** effect (per km) or a **volume** effect
(distance).

| Metric | total | per km | driven by |
|---|---|---|---|
| CO2  | **−4.81%** | −11.51% | rate (per-km fall overcomes +7.6% volume) |
| NOx  | +0.83% | −6.35% | mostly volume; rate improves |
| PMx  | **+3.09%** | −4.43% | **volume** — total rises only because more km driven |
| CO   | **+30.72%** | +21.15% | **rate** — genuine per-km increase |
| HC   | +1.72% | −5.66% | **volume** — total rises only because more km driven |
| fuel | **−4.80%** | −11.50% | rate (per-km fall overcomes +7.6% volume) |

**Reading it correctly:**
- **CO2 and fuel fall** in absolute terms — the per-km improvement is larger
  than the extra distance.
- **PMx and HC rise in the totals *only* because more vehicle-km are driven;
  per km they fall.** They are **not** per-vehicle increases. (HC is also the
  least stable metric — see §2.1.1 — so treat its small change as within noise.)
- **NOx** is roughly flat at the total, falling per km.
- **CO** is the one pollutant that genuinely **rises per km** (+21%) as well as
  in total.

## Journey time / flow (peak)

| Scenario | Avg duration | Time loss | Waiting | Completed |
|---|---|---|---|---|
| cal 30mph | 814.4 s | 433.9 s | 139.7 s | 1012 |
| cal 20mph | 700.5 s | 362.6 s | 138.9 s | 1059 |

- Journey time **−114.0 s**, time loss **−16.4%**, 47 more trips complete.
- Waiting essentially unchanged (−0.6%).

## Noise (peak)

Fleet mean 61.56 → 62.49 dB(A): **+0.93 dB(A)** (a small *increase*).

## Why the reversal?

Under the DfT-calibrated mix, a 20mph limit makes most drivers non-compliant by
a *larger* margin than a 30mph limit does (on 20mph roads the mid band sits at
~24mph — 20% over — and the high band at ~32mph — 60% over). The extra
acceleration/braking and higher-than-limit speeds on the constrained side roads
raise emissions. This effect is absent from the earlier `dft` set because that
set assumed only 20% non-compliance and the *same* mix at both limits.

## Comparison of the two simulation sets

| Peak | `dft` set (fixed 20% speeders) | `dft_cal` set (DfT-calibrated) |
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

## Interpretation (factual)

- The **emissions result depends strongly on the assumed driver behaviour**, and
  becomes **mixed rather than a clean sign** once behaviour is DfT-calibrated.
- **Most apparent "increases" are a distance-driven volume effect, not a
  per-vehicle effect.** The 20mph scenario drives **+7.6% more vehicle-km**
  (more trips complete). PMx and HC rise in the totals purely because of that;
  **per km they fall**.
- **Per km driven, five of six pollutants fall** (CO2, fuel, NOx, PMx, HC). Only
  **CO rises per km** (+21%). So from a "cleanliness of each kilometre" view,
  20mph is better or neutral except for CO.
- **Journey time and flow improve** under 20mph in the calibrated set
  (−114 s, −16% time loss, +47 trips); the `dft` set showed it roughly
  unchanged. The flow conclusion is robust (never worse).
- Noise shows **no benefit** in either set (+0.13 to +0.93 dB(A)).

### Why the calibrated set differs so much from the first attempt

The first `cal` attempt used **three discrete bands**; this version uses a
**continuous distribution fitted to the DfT % exceeding**. The continuous form
puts more traffic at moderate over-limit speeds (on 20mph roads, a mean factor
of ~1.14), which raises CO and PMx while lowering CO2/fuel — hence the change in
sign for several pollutants. The discrete-band result (CO2 +1.41%, NOx +3.07%)
is superseded by the fitted continuous result above.

## Caveats

1. Both sets use the same **simplified network and estimated flows**; see
   `FLOW_CALIBRATION.md` and `sumo/NETWORK_BUILD.md`.
2. The speed distribution is a **truncated normal fitted to the % exceeding**,
   not a full empirical histogram (DfT does not publish one). Real distributions
   are right-skewed, so the fitted mean speed sits ~1–1.5 mph below DfT's
   rounded average — see `sumo/DFT_BEHAVIOUR.md`.
3. DfT compliance is measured on **free-flowing** roads; congested conditions
   will differ, and this is a single-hour peak model.
4. The emissions result is **not a clean sign**, and **absolute totals conflate
   two effects**: (i) distance driven and (ii) emissions per km. The 20mph
   scenario drives +7.6% more vehicle-km, which raises all absolute totals.
   Always report the **per-km** figure alongside the total, and state which is
   meant. Per km, five of six pollutants fall; only CO rises.
5. HC remains the least stable metric (see `EXPERIMENT_REPORT.md` §2.1.1).

## Reproducing

```bash
cd sumo
sumo -c wool.cal_now.sumo.cfg
sumo -c wool.cal_20mph.sumo.cfg
python3 analyze_emissions.py \
  --now-edge wool.cal_now.road_emissions.xml --now-veh wool.cal_now.emissions.xml --now-trip wool.cal_now.tripinfo.xml \
  --scheme-edge wool.cal_20mph.road_emissions.xml --scheme-veh wool.cal_20mph.emissions.xml --scheme-trip wool.cal_20mph.tripinfo.xml
```
