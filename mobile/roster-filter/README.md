# Roster Filter — Mobile (1024px)

Mobile version of the Roster Filter button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 3 (STARTERS, TOP 51, 90-MAN) |
| Default | STARTERS |
| Rows | 1 (3) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `RosterFilter` (String, default: `STARTERS`) |
| Dataset | roster-filter-data.csv |
| Calc field | `SelectedRoster = ${RosterFilter}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `RosterFilter` = ButtonLabel |

## Files

- `quicksight-roster-filter-mobile.json` — QuickSight config
- `test-roster-filter-mobile.html` — Local test file
