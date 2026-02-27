# Position Filter Buttons v3 — With OFF/DEF Groups

Adds OFF and DEF group buttons between All and the individual positions.

## Buttons (15)
All | OFF | DEF | QB | RB | WR | TE | T | G | C | DT | ED | LB | CB | S

## Key Changes from v2
- **2 new buttons** — OFF and DEF inserted after All
- **3-tier filter logic** — All (everything), OFF/DEF (group via `offdef` column), individual position
- **Updated position labels** — T, G, C, S (instead of OT, OG, OC, DS)
- **Button div shrunk to 42px** — fits 15 buttons in ~800px widget
- **Spacing recalculated** — startX 16.15, step 4.55 units

## QuickSight Setup

### Parameter
- Name: `PositionFilter`, Type: String, Default: `All`

### Button Dataset
Upload `position-filter-data-v3.csv`, add calculated field:
```
Name: SelectedPosition
Expression: ${PositionFilter}
```

### Field Wells (GROUP BY)
1. `SortOrder` (col 0) — sort ascending
2. `ButtonLabel` (col 1)
3. `SelectedPosition` (col 2)

### Navigation Action
- Activation: Select
- Action: Set parameter `PositionFilter` = field `ButtonLabel`

### Target Dataset — Calc Field (CRITICAL)

The target dataset must have an `offdef` column with values `OFF` or `DEF` for each row.

```
Name: ShowByPosition
Expression: ifelse(
  ${PositionFilter}='All', 1,
  ifelse(${PositionFilter}='OFF' AND {offdef}='OFF', 1,
    ifelse(${PositionFilter}='DEF' AND {offdef}='DEF', 1,
      ifelse({Position}=${PositionFilter}, 1, 0)
    )
  )
)
```

Filter target visuals: `ShowByPosition = 1`

### How the filter logic works

| Button clicked | Parameter value | Rows shown |
|----------------|-----------------|------------|
| All | `All` | All rows (first condition) |
| OFF | `OFF` | Rows where `offdef = 'OFF'` |
| DEF | `DEF` | Rows where `offdef = 'DEF'` |
| QB | `QB` | Rows where `Position = 'QB'` |
| T | `T` | Rows where `Position = 'T'` |
| ... | ... | ... |

## Spacing Math

```
Chart width:        800px
Chart spacing:      [5, 0, 5, 0] → plot area = 800px
1 xAxis unit:       800 / 100 = 8px
Button CSS width:   42px = 5.25 xAxis units
Center spacing:     4.55 units
Start X:            16.15
Last X:             16.15 + 14 × 4.55 = 79.85
Total button span:  15 × 42px = 630px
```

## Files
- `quicksight-position-filter-v3.json` — QuickSight Highcharts config
- `position-filter-data-v3.csv` — Button dataset (15 rows)
- `test-position-filter-v3.html` — Local test file (open in browser)
- `position-filter-v3-share.md` — Combined doc with code + setup

## Visual Size
- Widget width: ~800px
- Chart height: 30px
- Button width: 42px each (630px total for 15 buttons)
