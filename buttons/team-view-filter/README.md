# Team View Filter Buttons

3-button filter for team page view selection.

## Buttons
TEAM SNAPSHOT | TEAM NEEDS | DIVISION RANKS

## QuickSight Setup

### Parameter
- Name: `TeamViewFilter`, Type: String, Default: `TEAM SNAPSHOT`

### Dataset
Upload `team-view-filter-data.csv` to SPICE. Add calculated field:
```
Name: SelectedTeamView
Expression: ${TeamViewFilter}
```

### Field Wells (GROUP BY)
1. `SortOrder` (col 0) — sort ascending
2. `ButtonLabel` (col 1)
3. `SelectedTeamView` (col 2)

### Navigation Action
- Activation: Select
- Action: Set parameter `TeamViewFilter` = field `ButtonLabel`

### Target Visuals
Use conditional visibility on widgets:
- Team Snapshot widgets: Show when `${TeamViewFilter} = 'TEAM SNAPSHOT'`
- Team Needs widgets: Show when `${TeamViewFilter} = 'TEAM NEEDS'`
- Division Ranks widgets: Show when `${TeamViewFilter} = 'DIVISION RANKS'`

## Files
- `quicksight-team-view-filter.json` — Highcharts config
- `team-view-filter-data.csv` — Button data (3 rows)
- `test-team-view-filter.html` — Local test file

## Widget Size
- Chart width: ~500px
- Chart height: 30px
- Button div: 130px wide, 17px tall, 11px font
