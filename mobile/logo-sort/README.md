# Logo Sort — Mobile (1024px)

Mobile version of the Logo Sort button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 2 (Alpha, Draft Order) |
| Default | Alpha |
| Rows | 1 (2) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `LogoSort` (String, default: `Alpha`) |
| Dataset | logo-sort-data.csv |
| Calc field | `SelectedLogoSort = ${LogoSort}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `LogoSort` = ButtonLabel |

## Files

- `quicksight-logo-sort-mobile.json` — QuickSight config
- `test-logo-sort-mobile.html` — Local test file
