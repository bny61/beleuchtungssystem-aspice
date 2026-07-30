# Operational situations (situation catalogue)

Basis of the hazard analysis in [`hara.md`](hara.md). The catalogue is formed as the cross product
**driving situation x operating mode x environment** and then reduced to the combinations relevant
to the lighting functions.

> Values are plausible example values of a teaching project, not validated usage data.
> The usage profile is based on assumption `A-07`.

## 1 Dimensions

| Dimension | Values |
|---|---|
| **Driving situation** | standstill · manoeuvring (< 10 km/h) · urban (50 km/h) · rural road (80 km/h) · motorway (85 km/h) |
| **Operating mode** | daytime running lights · low beam · high beam · cornering light · work lamps · limp-home |
| **Environment** | day / dusk / night · lit / unlit · dry / rain / fog · oncoming traffic yes / no |

The full cross product spans several hundred combinations. It was reduced by two criteria:
(1) the combination is technically possible, (2) it is relevant to at least one lighting function.
Combinations without hazard potential (e.g. standstill with daytime running lights in daylight) are
deliberately not carried.

## 2 Relevant operational situations

| ID | Driving situation | Operating mode | Environment | Used in |
|---|---|---|---|---|
| **BS-01** | Rural road, 80 km/h | Low beam active | Night, unlit, dry | H-01, H-03, H-05 |
| **BS-02** | Rural road, 80 km/h | High beam active | Night, oncoming traffic | H-02 |
| **BS-03** | Motorway, 85 km/h | Low beam active | Night, rain | H-04 |
| **BS-04** | Construction site / yard, < 10 km/h | Work lamps active | Night | — (intended use) |
| **BS-05** | Urban traffic, 50 km/h | Low beam + cornering light | Night, lit | H-07 |
| **BS-06** | Rural road, 80 km/h | Daytime running lights active | Day, good visibility | H-06 |
| **BS-07** | Standstill, ignition on | Work lamps active | Night, loading point | — (intended use) |

**BS-04** and **BS-07** lead to no hazard because work-lamp operation is intended there. They remain
in the catalogue because they justify the delimitation against H-03: only the combination of *work
lamps active* with *driving operation* is hazardous, not the operating mode as such. It is exactly
this distinction that `FSR-008` implements via the speed threshold.

## 3 Usage profile (basis of the E rating)

| Situation | Estimated share of operating time | Rating |
|---|---|---|
| Night driving overall | approx. 25 % | — |
| Of which night driving on unlit rural roads (BS-01) | a few percent | **E3** |
| Night driving with oncoming traffic and high beam active (BS-02) | low | **E2** |
| Daytime driving in good visibility (BS-06) | predominant | **E3** in the context of H-06 |

> Assigning *unlit rural road at night* to **E3** rather than E4 is the critical decision of the
> HARA and is tracked as `RISK-01`. Confirmation through real OEM usage data is outstanding
> (`A-07`).
