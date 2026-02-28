# Position Filter — Mobile (1024px)

Mobile version of the Position Filter button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 15 (All, OFF, DEF, QB, RB, WR, TE, T, G, C, DT, ED, LB, CB, S) |
| Default | All |
| Rows | 3 (5+5+5) |
| Chart height | 220px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `PositionFilter` (String, default: `All`) |
| Dataset | position-filter-data-v3.csv |
| Calc field | `SelectedPosition = ${PositionFilter}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `PositionFilter` = ButtonLabel |

## Files

- `quicksight-position-filter-mobile.json` — QuickSight config
- `test-position-filter-mobile.html` — Local test file
