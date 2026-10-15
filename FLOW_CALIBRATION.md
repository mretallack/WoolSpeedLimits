# Wool Flow Calibration Note

This note records the calibration audit of the peak/off-peak traffic demand
against the WoolRATH manual survey, and the corrections applied.

## 1. What the survey actually measures

Source: `SurveyResults.ods` (also summarised in `README.md`). The survey has
**only two geographic count points**, both on the A352:

| Point | Date / time | W-bound | E-bound |
|---|---|---|---|
| Winfrith Roundabout | 06/09/16 08:00 | 439 cars + 17 HGV | 639 cars + 30 HGV |
| **Station Garage** (in Wool) | 06/09/16 08:00 | **500 cars + 17 HGV** | **518 cars + 25 HGV** |

**Nothing in the survey covers** Colliers Lane, Lulworth Road, the new-estate
spur, the south leg, or any residential back road. Every flow on those links is
*modelled*, not measured.

`ForecastFlows.ods` scales these by DfT Scenario 1 (+22.80% for 2030), giving
the "west to east" baseline car count of 471 cars used in the older flow files.

## 2. The over-loading problem (pre-v2)

The peak route file `wool.rou.dft_controlled.xml` declared:

| Corridor | Declared | Survey | Issue |
|---|---|---|---|
| A352 W→E | 471 cars + 27 HGV + 63 other | 543 | ok |
| A352 E→W | 296 cars + 15 HGV + 60 other | 517 | **28% low** |
| Estate feed `west_to_east_10` | **320** | *(none)* | **2.3× too high** |
| Lulworth legs (2×80) | **160** | *(none)* | duplicated estate feed |
| South→North leg | **58** | *(none)* | extra |

Total declared = **1,470 veh/hr** vs survey A352 through-flow = **1,060 veh/hr**,
i.e. **+39%** demand beyond anything measured, layered onto the busiest corridor.

Consequences in the pre-v2 runs:
- Only **1,418 of 1,470** vehicles inserted; **52 never entered**.
- Only **1,033 completed** their trip in the hour.
- **22 teleport events.**
- The network operated **above capacity**, which *inverted* the emissions
  conclusion (see `EXPERIMENT_REPORT.md` §2.1).

Root cause of the estate figure: `320` is the old **1,000-home** figure. The
README's own TRICS derivation for the **800-home** scheme is 277 veh/hr ×
50.88% Eastbound = **141**, which is what `wool.woolrathflows800.st8am.xml`
already used.

## 3. Corrections applied (`wool.rou.dft_controlled.v2.xml` / `.dft_offpeak.v2.xml`)

| Item | Old | Corrected | Basis |
|---|---|---|---|
| A352 W→E cars | 471 | **518** | Station Garage survey |
| A352 W→E HGV | 27 | **25** | Station Garage survey |
| A352 E→W cars | 296 | **500** | Station Garage survey |
| A352 E→W HGV | 15 | **17** | Station Garage survey |
| Estate feed | 320 | **141** | 800-home TRICS figure |
| Lulworth legs (2×80) | 160 | **removed** | duplicated the estate origin edge `4691379#0` |

Car behaviour split retained at the file's existing **10% compliant / 70%
normal / 20% speeder** ratio, applied to the corrected car totals.

Off-peak has no dedicated survey; it is a **0.40 scale** of the corrected peak
(the ratio used in the original files).

**Result:** peak demand 1,470 → **1,382** veh/hr. All vehicles now insert
(waiting = 0), **0 teleports**, and no capacity inversion.

## 4. Residual model assumptions (not survey-derived)

These remain modelled and are flagged for transparency:
- South→North leg (58 veh/hr peak) — no survey coverage.
- LGV/BUS/MCY proportions — carried from the original files.
- Off-peak = 0.40 × peak: an assumption, not a documented time-of-day profile.

## 5. Reproducing

```bash
cd sumo
sumo -c wool.dft_now.sumo.cfg          # peak, corrected v2 demand
sumo -c wool.dft_20mph.sumo.cfg
sumo -c wool.dft_offpeak_now.sumo.cfg
sumo -c wool.dft_offpeak_20mph.sumo.cfg
```
