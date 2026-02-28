# Team Fit Filter — Mobile (1024px)

Mobile version of the Team Fit Filter button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 4 (TEAM FIT, TOP 101, OUTGOING, CUT CANDIDATES) |
| Default | TEAM FIT |
| Rows | 1 (4) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `TeamFitFilter` (String, default: `TEAM FIT`) |
| Dataset | team-fit-filter-data.csv |
| Calc field | `SelectedTeamFit = ${TeamFitFilter}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `TeamFitFilter` = ButtonLabel |

## Files

- `quicksight-team-fit-filter-mobile.json` — QuickSight config
- `test-team-fit-filter-mobile.html` — Local test file
