# Unit Filter — Mobile (1024px)

Mobile version of the Unit Filter button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 3 (ALL, OFFENSE, DEFENSE) |
| Default | ALL |
| Rows | 1 (3) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `UnitFilter` (String, default: `ALL`) |
| Dataset | unit-filter-data.csv |
| Calc field | `SelectedUnit = ${UnitFilter}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `UnitFilter` = ButtonLabel |

## Files

- `quicksight-unit-filter-mobile.json` — QuickSight config
- `test-unit-filter-mobile.html` — Local test file
