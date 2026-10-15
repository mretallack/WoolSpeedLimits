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

## Emissions (peak, 20mph vs 30mph)

| Metric | road_total | vehicle_total | vehicle_perkm |
|---|---|---|---|
| CO2  | **−4.81%** | −4.79% | −11.51% |
| NOx  | +0.83% | +0.77% | −6.35% |
| PMx  | **+3.09%** | +2.83% | −4.43% |
| CO   | **+30.72%** | +30.36% | +21.15% |
| HC   | +1.72% | +1.51% | −5.66% |
| fuel | **−4.80%** | −4.78% | −11.50% |

Mixed at the totals: CO2 and fuel fall, PMx and CO rise sharply. The **per-km**
view (which normalises out the extra distance travelled) shows CO2/fuel/NOx/PMx/
HC all **fall**, with CO still rising.

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

| Peak, road_total | `dft` set (fixed 20% speeders) | `dft_cal` set (DfT-calibrated, continuous) |
|---|---|---|
| CO2  | −1.85% | **−4.81%** |
| NOx  | −2.99% | +0.83% |
| PMx  | −1.88% | **+3.09%** |
| CO   | −0.70% | **+30.72%** |
| HC   | −7.10% | +1.72% |
| fuel | −1.86% | **−4.80%** |
| journey time | +0.2 s | −114.0 s |
| noise | +0.13 dB(A) | +0.93 dB(A) |

## Interpretation (factual)

- The **emissions result depends strongly on the assumed driver behaviour**, and
  becomes **mixed rather than a clean sign** once behaviour is DfT-calibrated:
  CO2 and fuel **fall**, while PMx and CO **rise sharply**; NOx and HC are
  roughly flat.
- The **per-km** view (which removes the effect of the 20mph scenario covering
  more distance) shows CO2, fuel, NOx, PMx and HC **all fall**, with only CO
  rising. So "pollution per km driven" improves even though some absolute
  totals rise.
- **Journey time and flow improve** under 20mph in the calibrated set
  (−114 s, −16% time loss); the earlier `dft` set showed it roughly unchanged.
  Both are non-negative, so the flow conclusion is robust.
- Noise shows **no benefit** in either set (+0.48 to +0.93 dB(A)).

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
4. The emissions result is **not a clean sign**: CO2/fuel fall but PMx/CO rise at
   the road total. Report the metric, not a single verdict.
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
