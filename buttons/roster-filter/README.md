# Roster Filter Buttons

3-button filter for roster view selection.

## Buttons
STARTERS | TOP 51 | 90-MAN

## QuickSight Setup

### Parameter
- Name: `RosterFilter`, Type: String, Default: `STARTERS`

### Dataset
Upload `roster-filter-data.csv` to SPICE. Add calculated field:
```
Name: SelectedRoster
Expression: ${RosterFilter}
```

### Field Wells (GROUP BY)
1. `SortOrder` (col 0) — sort ascending
2. `ButtonLabel` (col 1)
3. `SelectedRoster` (col 2)

### Navigation Action
- Activation: Select
- Action: Set parameter `RosterFilter` = field `ButtonLabel`

### Target Visuals
On each target dataset, add calc field:
```
Name: ShowByRoster
Expression: ifelse(${RosterFilter}='STARTERS', 1, ifelse(RosterType=${RosterFilter}, 1, 0))
```
Filter target visuals: `ShowByRoster = 1`

## Files
- `quicksight-roster-filter.json` — Highcharts config
- `roster-filter-data.csv` — Button data (3 rows)
- `test-roster-filter.html` — Local test file

## Widget Size
- Chart width: ~350px
- Chart height: 30px
- Button div: 90px wide, 17px tall, 11px font
