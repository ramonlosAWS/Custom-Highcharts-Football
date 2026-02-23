# Position Filter Buttons

13-button segmented control for filtering by NFL position group.

## Buttons
ALL | QB | RB | WR | TE | OT | OG | OC | DT | ED | LB | CB | DS

## QuickSight Setup

### Parameter
- Name: `PositionFilter`, Type: String, Default: `ALL`

### Dataset
Upload `position-filter-data.csv` to SPICE. Add calculated field:
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

### Target Visuals
On each target dataset, add calc field:
```
Name: ShowByPosition
Expression: ifelse(${PositionFilter}='ALL', 1, ifelse(PositionGroup=${PositionFilter}, 1, 0))
```
Filter target visuals: `ShowByPosition = 1`

## Files
- `quicksight-position-filter.json` — Highcharts config
- `position-filter-data.csv` — Button data (13 rows with sort order)
- `test-position-filter.html` — Local test file

## Widget Size
- Chart width: ~800px
- Chart height: 30px
- Button div: 48px wide, 20px tall, 11px font
