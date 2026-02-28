# Source Filter — Mobile (1024px)

Mobile version of the Source Filter button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 2 (GRINDING THE MOCKS, DJ'S TOP 50) |
| Default | GRINDING THE MOCKS |
| Rows | 1 (2) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `SourceFilter` (String, default: `GRINDING THE MOCKS`) |
| Dataset | source-filter-data.csv |
| Calc field | `SelectedSource = ${SourceFilter}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `SourceFilter` = ButtonLabel |

## Files

- `quicksight-source-filter-mobile.json` — QuickSight config
- `test-source-filter-mobile.html` — Local test file
