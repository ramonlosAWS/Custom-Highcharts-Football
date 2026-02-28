# Team View Filter — Mobile (1024px)

Mobile version of the Team View Filter button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 3 (TEAM SNAPSHOT, TEAM NEEDS, DIVISION RANKS) |
| Default | TEAM SNAPSHOT |
| Rows | 1 (3) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `TeamViewFilter` (String, default: `TEAM SNAPSHOT`) |
| Dataset | team-view-filter-data.csv |
| Calc field | `SelectedTeamView = ${TeamViewFilter}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `TeamViewFilter` = ButtonLabel |

## Files

- `quicksight-team-view-filter-mobile.json` — QuickSight config
- `test-team-view-filter-mobile.html` — Local test file
