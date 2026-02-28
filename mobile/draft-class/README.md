# Draft Class — Mobile (1024px)

Mobile version of the Draft Class button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 4 (All, 2023, 2024, 2025) |
| Default | All |
| Rows | 1 (4) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `DraftClass` (String, default: `All`) |
| Dataset | draft-class-data.csv |
| Calc field | `SelectedDraftClass = ${DraftClass}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `DraftClass` = ButtonLabel |

## Files

- `quicksight-draft-class-mobile.json` — QuickSight config
- `test-draft-class-mobile.html` — Local test file
