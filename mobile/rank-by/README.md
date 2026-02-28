# Rank By — Mobile (1024px)

Mobile version of the Rank By button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 13 (Overall Score, Production Score, Athleticism Score, 10-yd Split, 40 Time, 40 Top Speed, Vertical Jump, Broad Jump, Short Shuttle, Three Cone, Height, Weight, Arm Length) |
| Default | Overall Score |
| Rows | 3 (5+5+3) |
| Chart height | 220px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `RankBy` (String, default: `Overall Score`) |
| Dataset | rank-by-data.csv |
| Calc field | `SelectedRankBy = ${RankBy}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `RankBy` = ButtonLabel |

## Files

- `quicksight-rank-by-mobile.json` — QuickSight config
- `test-rank-by-mobile.html` — Local test file
