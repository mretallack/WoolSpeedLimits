# Driver Speed Behaviour Calibration (DfT SPE0101)

This note documents how the **`dft_cal`** simulation set derives realistic driver
speed behaviour from official Department for Transport statistics, and how it
differs from the earlier `dft` set.

## Source data

**Vehicle speed compliance statistics for Great Britain: 2024**
- Published **25 June 2025** by DfT (data tables updated September 2025).
- Landing page:
  <https://www.gov.uk/government/statistics/vehicle-speed-compliance-statistics-for-great-britain-2024>
- Data tables page:
  <https://www.gov.uk/government/statistical-data-sets/vehicle-speed-compliance-statistics-data-tables-spe>

Committed source files (`Sources/`):

| File | Table | Content |
|---|---|---|
| `spe0101.ods` | SPE0101 | **% of vehicles exceeding the speed limit by road type and vehicle type** (2018–2024) — the key table |
| `spe0113.ods` | SPE0113 | % exceeding by **hour of day** |
| `spe0102.ods` | SPE0102 | Free-flow speeds by road type / vehicle type |
| `spe0116.ods` | SPE0116 | % of cars exceeding by road type (longer series) |
| `spe0201_offences.ods` | SPE0201 | Speeding **offences** (FPNs / convictions) — *not* compliance; previously mislabelled `SPE0101.ods` |

> The old `Sources/SPE0101.ods` was actually **SPE0201** (offences), not the
> compliance table the docs referenced. It has been renamed `spe0201_offences.ods`
> and the genuine SPE0101 downloaded as `spe0101.ods`.

## The headline numbers (2024, cars)

| Road type | % exceeding the limit | % exceeding by ≥10 mph | Average free-flow speed |
|---|---|---|---|
| **30 mph roads** | **43%** | 4% | 30 mph |
| **20 mph roads** | **76%** | 10% | 24 mph |

At the **08:00 peak hour** (SPE0113, cars): **41%** exceed on 30 mph roads,
**77%** on 20 mph roads.

**Key fact:** non-compliance is far higher on 20 mph roads, and the two limits
have *different* compliance profiles. A model that uses the same behaviour mix
for both cannot represent this.

## Behaviour bands used in `dft_cal`

Three car types, each a band, calibrated so the mix matches the DfT split and
`speedFactor` ≈ achieved speed / limit:

| Band | 30 mph roads | 20 mph roads | speedFactor (30 / 20) | achieved speed |
|---|---|---|---|---|
| `CAR_LOW`  (at/below)      | 57% | 24% | 0.95 / 0.95 | 28.5 / 19 mph |
| `CAR_MID`  (1–10 over)     | 39% | 66% | 1.10 / 1.20 | 33 / 24 mph |
| `CAR_HIGH` (10+ over)      | 4%  | 10% | 1.40 / 1.60 | 42 / 32 mph |

Applied to the survey-calibrated car totals (518 W→E, 500 E→W):

| Scenario | `CAR_LOW` | `CAR_MID` | `CAR_HIGH` |
|---|---|---|---|
| `wool.rou.dft_cal_30.xml` (30 mph) | 295 / 285 | 202 / 195 | 21 / 20 |
| `wool.rou.dft_cal_20.xml` (20 mph) | 124 / 120 | 342 / 330 | 52 / 50 |

Only the **behaviour mix** differs between the two scenarios — the total demand
(1,382 veh/hr) is identical, so the comparison is controlled.

## How this differs from the earlier `dft` set

| | `dft` set (original) | `dft_cal` set (this) |
|---|---|---|
| Non-compliant share | **20% fixed** (arbitrary) | **41%** (30mph) / **77%** (20mph), from DfT |
| Same mix at 20 and 30? | Yes | **No** — matches DfT |
| Basis | leftover ratio, not evidence-based | DfT SPE0101 (2024) |

## Files

- Routes: `wool.rou.dft_cal_30.xml`, `wool.rou.dft_cal_20.xml`
- Configs: `wool.cal_now.sumo.cfg`, `wool.cal_20mph.sumo.cfg`
- Results doc: `../SENSITIVITY_BEHAVIOUR.md`
