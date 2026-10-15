# Sensitivity Analysis: Driver Speed Behaviour (`dft_cal` set)

This document reports a **sensitivity test** on the main result. It asks: does
the "20mph has no negative effect" conclusion hold when driver behaviour is
calibrated to real DfT speed-compliance data?

**Answer: no — the emissions result reverses.** Journey times still improve
slightly, but emissions *increase* under 20mph once realistic non-compliance is
modelled.

## What was changed

Only the **driver behaviour mix** changed between the two scenarios, following
DfT SPE0101 (2024). Total demand is identical (1,382 veh/hr). See
`sumo/DFT_BEHAVIOUR.md`.

| | 30mph scenario | 20mph scenario |
|---|---|---|
| At/below limit | 57% | 24% |
| 1–10 mph over | 39% | 66% |
| 10+ mph over | 4% | 10% |
| (non-compliant total) | **43%** | **76%** |

## Emissions (peak, 20mph vs 30mph)

| Metric | road_total | vehicle_total | vehicle_perkm |
|---|---|---|---|
| CO2  | **+1.41%** | +1.39% | +6.03% |
| NOx  | **+3.07%** | +3.06% | +7.77% |
| PMx  | **+2.55%** | +2.50% | +7.18% |
| CO   | **+14.74%** | +14.55% | +19.78% |
| HC   | −1.19% | −0.95% | +3.58% |
| fuel | **+1.41%** | +1.39% | +6.03% |

## Journey time / flow (peak)

| Scenario | Avg duration | Time loss | Waiting | Completed |
|---|---|---|---|---|
| cal 30mph | 620.1 s | 262.5 s | 126.3 s | 1089 |
| cal 20mph | 594.5 s | 269.6 s | 111.5 s | 1037 |

- Journey time **−25.7 s**, waiting **−11.7%** (flow is fine).
- Time loss **+2.7%**; 52 fewer trips complete in the hour.

## Noise (peak)

Fleet mean 63.05 → 63.53 dB(A): **+0.48 dB(A)** (a small *increase*).

## Why the reversal?

Under the DfT-calibrated mix, a 20mph limit makes most drivers non-compliant by
a *larger* margin than a 30mph limit does (on 20mph roads the mid band sits at
~24mph — 20% over — and the high band at ~32mph — 60% over). The extra
acceleration/braking and higher-than-limit speeds on the constrained side roads
raise emissions. This effect is absent from the earlier `dft` set because that
set assumed only 20% non-compliance and the *same* mix at both limits.

## Comparison of the two simulation sets

| Peak, road_total | `dft` set (fixed 20% speeders) | `dft_cal` set (DfT-calibrated) |
|---|---|---|
| CO2  | −1.85% | **+1.41%** |
| NOx  | −2.99% | **+3.07%** |
| PMx  | −1.88% | **+2.55%** |
| CO   | −0.70% | **+14.74%** |
| HC   | −7.10% | **−1.19%** |
| fuel | −1.86% | **+1.41%** |
| journey time | +0.2 s | −25.7 s |
| noise | +0.13 dB(A) | +0.48 dB(A) |

## Interpretation (factual)

- The **direction of the emissions result depends on the assumed driver
  behaviour.** With low assumed non-compliance (the `dft` set) 20mph reduces
  emissions; with DfT-calibrated non-compliance (the `dft_cal` set) 20mph
  increases them.
- The `dft_cal` behaviour is the evidence-based one (DfT SPE0101, 2024), so its
  result should be given more weight — **but see the caveats**.
- Journey-time and flow results are **robust**: both sets show a small
  improvement under 20mph.
- Noise shows **no benefit** in either set.

## Caveats

1. Both sets use the same **simplified network and estimated flows**; see
   `FLOW_CALIBRATION.md` and `sumo/NETWORK_BUILD.md`.
2. The behaviour bands are a **three-band approximation** of a continuous
   distribution; the exact band boundaries affect the magnitude (not the sign).
3. DfT compliance is measured on **free-flowing** roads; congested conditions
   will differ.
4. HC remains the least stable metric (see `EXPERIMENT_REPORT.md` §2.1.1).

## Reproducing

```bash
cd sumo
sumo -c wool.cal_now.sumo.cfg
sumo -c wool.cal_20mph.sumo.cfg
python3 analyze_emissions.py \
  --now-edge wool.cal_now.road_emissions.xml --now-veh wool.cal_now.emissions.xml --now-trip wool.cal_now.tripinfo.xml \
  --scheme-edge wool.cal_20mph.road_emissions.xml --scheme-veh wool.cal_20mph.emissions.xml --scheme-trip wool.cal_20mph.tripinfo.xml
```
