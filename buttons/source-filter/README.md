# Source Filter Buttons

2-button filter for draft source selection.

## Buttons
GRINDING THE MOCKS | DJ'S TOP 50

## QuickSight Setup

### Parameter
- Name: `SourceFilter`, Type: String, Default: `GRINDING THE MOCKS`

### Dataset
Upload `source-filter-data.csv` to SPICE. Add calculated field:
```
Name: SelectedSource
Expression: ${SourceFilter}
```

### Field Wells (GROUP BY)
1. `SortOrder` (col 0) — sort ascending
2. `ButtonLabel` (col 1)
3. `SelectedSource` (col 2)

### Navigation Action
- Activation: Select
- Action: Set parameter `SourceFilter` = field `ButtonLabel`

### Target Visuals
On each target dataset, add calc field:
```
Name: ShowBySource
Expression: ifelse(Source=${SourceFilter}, 1, 0)
```
Filter target visuals: `ShowBySource = 1`

## Files
- `quicksight-source-filter.json` — Highcharts config
- `source-filter-data.csv` — Button data (2 rows)
- `test-source-filter.html` — Local test file

## Widget Size
- Chart width: ~400px
- Chart height: 30px
- Button div: 148px wide, 17px tall, 11px font
