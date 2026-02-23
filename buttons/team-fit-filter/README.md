# Team Fit Filter Buttons

4-button filter for team fit analysis views.

## Buttons
TEAM FIT | TOP 101 | OUTGOING | CUT CANDIDATES

## QuickSight Setup

### Parameter
- Name: `TeamFitFilter`, Type: String, Default: `TEAM FIT`

### Dataset
Upload `team-fit-filter-data.csv` to SPICE. Add calculated field:
```
Name: SelectedTeamFit
Expression: ${TeamFitFilter}
```

### Field Wells (GROUP BY)
1. `SortOrder` (col 0) — sort ascending
2. `ButtonLabel` (col 1)
3. `SelectedTeamFit` (col 2)

### Navigation Action
- Activation: Select
- Action: Set parameter `TeamFitFilter` = field `ButtonLabel`

### Target Visuals
On each target dataset, add calc field:
```
Name: ShowByTeamFit
Expression: ifelse(${TeamFitFilter}='TEAM FIT', 1, ifelse(FitCategory=${TeamFitFilter}, 1, 0))
```
Filter target visuals: `ShowByTeamFit = 1`

## Files
- `quicksight-team-fit-filter.json` — Highcharts config
- `team-fit-filter-data.csv` — Button data (4 rows)
- `test-team-fit-filter.html` — Local test file

## Widget Size
- Chart width: ~500px
- Chart height: 30px
- Button div: 110px wide, 17px tall, 11px font
