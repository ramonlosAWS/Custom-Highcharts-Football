# Fa Board Filter — Mobile (1024px)

Mobile version of the Fa Board Filter button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 4 (STREET FA, STAFF CONNECTIONS, OUTGOING, CTR LIST) |
| Default | STREET FA |
| Rows | 1 (4) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `FABoardFilter` (String, default: `STREET FA`) |
| Dataset | Shared Sheet1 (Data Type = 'Free Agent Board Filter') |
| Calc field | `selected fa filter = ${FABoardFilter}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `FABoardFilter` = ButtonLabel |

## Files

- `quicksight-fa-board-filter-mobile.json` — QuickSight config
- `test-fa-board-filter-mobile.html` — Local test file
