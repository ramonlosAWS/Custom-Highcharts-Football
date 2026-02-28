# Page Selector — Mobile (1024px)

Mobile version of the Page Selector button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 3 (1, 2, 3) |
| Default | 1 |
| Rows | 1 (3) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `PageSelector` (String, default: `1`) |
| Dataset | page-selector-data.csv |
| Calc field | `SelectedPage = ${PageSelector}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `PageSelector` = ButtonLabel |

## Files

- `quicksight-page-selector-mobile.json` — QuickSight config
- `test-page-selector-mobile.html` — Local test file
