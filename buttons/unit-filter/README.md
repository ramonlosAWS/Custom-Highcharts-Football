# Unit Filter Buttons

3-button filter for Offense/Defense unit selection.

## Buttons
ALL | OFFENSE | DEFENSE

## QuickSight Setup

### Parameter
- Name: `UnitFilter`, Type: String, Default: `ALL`

### Dataset
Upload `unit-filter-data.csv` to SPICE. Add calculated field:
```
Name: SelectedUnit
Expression: ${UnitFilter}
```

### Field Wells (GROUP BY)
1. `SortOrder` (col 0) — sort ascending
2. `ButtonLabel` (col 1)
3. `SelectedUnit` (col 2)

### Navigation Action
- Activation: Select
- Action: Set parameter `UnitFilter` = field `ButtonLabel`

### Target Visuals
On each target dataset, add calc field:
```
Name: ShowByUnit
Expression: ifelse(${UnitFilter}='ALL', 1, ifelse(Unit=${UnitFilter}, 1, 0))
```
Filter target visuals: `ShowByUnit = 1`

## Files
- `quicksight-unit-filter.json` — Highcharts config
- `unit-filter-data.csv` — Button data (3 rows)
- `test-unit-filter.html` — Local test file

## Widget Size
- Chart width: ~800px (buttons centered, ~240px total)
- Chart height: 30px
- Button div: 84px wide, 17px tall, 11px font
