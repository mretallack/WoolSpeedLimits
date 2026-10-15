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

## Behaviour model used in `dft_cal` (continuous distribution)

Instead of a few discrete bands, cars use a **single continuous speed-factor
distribution per limit**, fitted so the modelled **% exceeding the limit matches
DfT**. SUMO's `speedFactor="normc(mean, sd, min, max)"` gives each vehicle a
factor drawn from a truncated normal.

| Road type | target % exceeding | `normc(mean, sd, min, max)` | achieved % exceeding | mean speed |
|---|---|---|---|---|
| 30 mph | 43% | `normc(0.968, 0.180, 0.2, 2.0)` | **42.7%** | 29.1 mph |
| 20 mph | 76% | `normc(1.141, 0.200, 0.2, 2.0)` | **74.7%** | 22.9 mph |

*(Achieved figures measured from the run's `tripinfo` `speedFactor` values.)*

Applied to the survey-calibrated car totals (518 W→E, 500 E→W) — all cars use
the one fitted type:

| Scenario | car type | car flow |
|---|---|---|
| `wool.rou.dft_cal_30.xml` (30 mph) | `CAR` = `normc(0.968,0.180,…)` | 518 / 500 |
| `wool.rou.dft_cal_20.xml` (20 mph) | `CAR` = `normc(1.141,0.200,…)` | 518 / 500 |

Only the **distribution** differs between the two scenarios — the total demand
(1,382 veh/hr) is identical, so the comparison is controlled.

### On matching DfT's average speed as well

DfT publishes both a **% exceeding** and an **average free-flow speed**. For a
**symmetric** distribution these are very slightly inconsistent (DfT: 30 mph
roads average 30 mph yet 43% exceed — a symmetric distribution with mean exactly
on the limit would give 50%). Real speed distributions are **right-skewed** (a
long tail of high speeders), which the truncated normal approximates. We
therefore fit to the **% exceeding** (the measure that defines speeders) and
accept the mean lands ~1–1.5 mph below DfT's rounded average. This is a known
approximation.

## How this differs from the earlier `dft` set

| | `dft` set (original) | `dft_cal` set (this) |
|---|---|---|
| Speed representation | 3 fixed types | **continuous `normc` distribution** |
| Non-compliant share | **20% fixed** (arbitrary) | **~43%** (30mph) / **~75%** (20mph), fitted to DfT |
| Same spread at 20 and 30? | Yes | **No** — matches DfT |
| Basis | leftover ratio, not evidence-based | DfT SPE0101 (2024) |

## Files

- Routes: `wool.rou.dft_cal_30.xml`, `wool.rou.dft_cal_20.xml`
- Configs: `wool.cal_now.sumo.cfg`, `wool.cal_20mph.sumo.cfg`
- Results: `../EXPERIMENT_REPORT.md` §2.4
