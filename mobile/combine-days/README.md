# Combine Days — Mobile (1024px)

Mobile version of the Combine Days button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 5 (All, Day 1, Day 2, Day 3, Day 4) |
| Default | All |
| Rows | 1 (5) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `CombineDays` (String, default: `All`) |
| Dataset | combine-days-data.csv |
| Calc field | `SelectedDay = ${CombineDays}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `CombineDays` = ButtonLabel |

## Files

- `quicksight-combine-days-mobile.json` — QuickSight config
- `test-combine-days-mobile.html` — Local test file
