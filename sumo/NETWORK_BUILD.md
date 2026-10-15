# 20mph Network Build (`wool.20mph.net.xml`)

This note records how the "with 20mph" network is derived, so the scheme is
auditable and reproducible.

## Source of truth

The set of roads that become 20mph is defined by the Dorset Council
consultation, exported as
[`Sources/Wool20MphRoads.json`](../Sources/Wool20MphRoads.json)
(`data.features`, 41 speed-limit line segments across 35 streets). A road is
20mph **only if it appears in this file**; everything else keeps its current
limit.

## Method

The SUMO network (`wool.net.xml`) carries **no street names**, so matching was
done in two steps:

1. **Name source** — regenerate a temporary named network from the OSM source
   with `netconvert --output.street-names true`. This yields edge→street-name
   tags (Dorchester Road, High Street, Colliers Lane, Lulworth Road, …) while
   preserving the same edge IDs as `wool.net.xml`.
2. **Match** — a consultation street is matched to network edges by
   **name**, then confirmed by **geometry overlap**: the consultation
   LineString coordinates are projected to the network CRS (UTM zone 30N, using
   the network's `netOffset`) and an edge is accepted only if ≥50% of its
   vertices lie within 15 m of the consultation segment. This prevents
   over-applying to nearby but unrelated edges.

Tooling: `build_20mph_net.py` (see below).

## Option A: invert genuine 30mph roads only

Some matched edges are tagged **50–62 mph** in the OSM baseline (see
Limitations). Forcing those to 20mph would corrupt the "Now" baseline, because
they are not 30mph "today". Following Option A, `wool.20mph.net.xml` sets to
20mph (8.94 m/s) **only the matched edges currently at 30 or 31 mph**:

- matched edges (by name + geometry): **119**
- of which ≤31 mph (set to 20mph): **99**
- of which 50/62 mph (left unchanged): **20**

The long arterial edge `116368205#1` (1,850 m, 62 mph) is **excluded** — only
~5% of its vertices fall in the consultation geometry. (The previous, incorrect
`wool.20mph.net.xml` had set it and other arterial edges to 20mph.)

Result: `wool.20mph.net.xml` has 99 edges at 20mph; 50/60/62 mph edges are
identical to the baseline.

## Reproducing

```bash
cd sumo
netconvert --lefthand --type-files osm-urban-de.typ.xml --ramps.guess \
  --remove-edges.by-vclass hov,taxi,bus,delivery,truck,tram,rail_urban,rail,rail_electric,motorcycle,bicycle,pedestrian \
  --geometry.remove --remove-edges.isolated --tls.join \
  --osm-files WoolStripedV5.osm --output-file /tmp/wool_named.net.xml \
  --output.street-names true
python3 build_20mph_net.py        # writes wool.20mph.net.xml (Option A)
```

## Limitations

1. **OSM speed-tag anomalies (20 matched edges).** The consultation lists some
   streets (Lulworth Road, Colliers Lane, Burton Road) whose network edges are
   tagged 50–62 mph — implausible for a village road and almost certainly OSM
   import errors. Under Option A these are **left unchanged** (kept at their
   baseline speed) so the before/after baseline stays honest. If they should in
   fact be village 30mph roads, the baseline itself needs correcting first.

2. **Streets in the proposal but absent from the network (9).** These minor
   roads were removed during OSM import (`--remove-edges.isolated` /
   geometry reduction) and cannot be represented:
   `Access To Wool Station, Baker Close, Burton Wood, Hillside Road, New Road,
   Oakdene Road, Sandhills Crescent, Water Meadow Road`.
   Their 20mph zones are not modelled; they are low-flow residential links with
   negligible effect on the corridor results.

3. **Name aliasing.** `Macville Avenue` (consultation) = `MacVille Ave`
   (network); `Breach Field` is matched to `Breach Field Road`.
