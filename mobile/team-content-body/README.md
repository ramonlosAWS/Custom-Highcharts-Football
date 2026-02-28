# Team Content Body — Mobile (1024px)

Mobile version of the Team Content Body button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 3 (DRAFT CLASS, FRONT OFFICE TENDENCIES, MOCK DRAFT TRACKER) |
| Default | DRAFT CLASS |
| Rows | 1 |
| Chart height | 80px |
| Button size | 320px x 62px |
| Font | 28px Barlow Condensed, weight 700 |
| X units | 31.25 (320px / 10.24px per unit) |
| startX | 18.75 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `TeamContentBody` (String, default: `DRAFT CLASS`) |
| Dataset | team-content-body-data.csv |
| Calc field | `SelectedContentBody = ${TeamContentBody}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `TeamContentBody` = ButtonLabel |

## Files

- `quicksight-team-content-body-mobile.json` — QuickSight config
- `test-team-content-body-mobile.html` — Local test file
