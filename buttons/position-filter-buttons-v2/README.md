# Position Filter Buttons v2 — Segmented Control

Redesigned position filter using a segmented control style with 13 buttons connected as a single bar.

## Positions
ALL | QB | RB | WR | TE | OT | OG | OC | DT | ED | LB | CB | DS

## Key Changes from v1
- **Single series with `map`** — no more 12 separate series definitions
- **Segmented control look** — buttons touch each other with thin dividers, rounded ends
- **Data-driven highlighting** — colors computed in data mapping, no pointRender needed
- **Fixed width required** — chart must be ~1100px wide to avoid button overlap

## Spacing Math (important)

This design uses fixed-width CSS buttons positioned via scatter x-coordinates.
The math must be precise or buttons overlap/get eaten:

```
Chart width:        1100px
Chart spacing:      [5, 10, 5, 10] → plot area = 1080px
1 xAxis unit:       1080 / 100 = 10.8px
Button CSS width:   76px = 7.037 xAxis units
Center spacing:     7.08 units (buttons nearly touch, shared borders)
Start X:            3.5
Last X:             3.5 + 12 × 7.08 = 88.46
```

If you change the visual width in QuickSight, recalculate:
1. Plot area = visual width - left spacing - right spacing
2. 1 unit = plot area / 100
3. Button units = button px width / (1 unit in px)
4. Spacing = button units + tiny gap (~0.04 units)

## QuickSight Setup

### Parameter
- Name: `PositionFilter`, Type: String, Default: `ALL`

### Dataset
Upload `position-filter-data-v2.csv`, add calculated field:
```
Name: SelectedPosition
Expression: ${PositionFilter}
```

### Field Wells (GROUP BY)
1. `ButtonLabel` (column 0)
2. `SelectedPosition` (column 1)

### Navigation Action
- Activation: Select
- Action: Set parameter `PositionFilter` = field `ButtonLabel`

### Target Visuals
On each target dataset, add calc field:
```
Name: ShowByPosition
Expression: ifelse(${PositionFilter}='ALL', 1, ifelse(Position=${PositionFilter}, 1, 0))
```
Filter target visuals: `ShowByPosition = 1`

## Files
- `quicksight-position-filter-v2.json` — QuickSight Highcharts config
- `position-filter-data-v2.csv` — Button dataset (13 rows)
- `test-position-filter-v2.html` — Local test file (open in browser)

## Visual Size
- **Required widget width: ~1100px** (fixed — do not let it float)
- Chart height: 50px
- Button width: 76px each (988px total for 13 buttons)
