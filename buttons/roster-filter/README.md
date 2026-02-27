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
Expression: ifelse(${RosterFilter}='90-MAN', 1, ${RosterFilter}='TOP 51' AND {Team Top 51 Contracts}<52, 1, ${RosterFilter}='STARTERS' AND {starter_flag}=1, 1, 0)
```
Filter target visuals: `ShowByRoster = 1`

**Logic:** Classification is derived from player data, not a pre-assigned column:
- **90-MAN** → shows all players (no condition)
- **TOP 51** → shows players where `Team Top 51 Contracts < 52`
- **STARTERS** → shows players where `starter_flag = 1`

## Files
- `quicksight-roster-filter.json` — Highcharts config
- `roster-filter-data.csv` — Button data (3 rows)
- `test-roster-filter.html` — Local test file

## Widget Size
- Chart width: ~350px
- Chart height: 30px
- Button div: 90px wide, 17px tall, 11px font
