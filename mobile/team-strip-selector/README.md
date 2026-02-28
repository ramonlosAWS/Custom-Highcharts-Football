# Team Strip Selector — Mobile (1024px)

Mobile version of the Team Strip Selector button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 2 (OFFSEASON PREVIEW, TEAM NEEDS) |
| Default | OFFSEASON PREVIEW |
| Rows | 1 (2) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `TeamStripSelector` (String, default: `OFFSEASON PREVIEW`) |
| Dataset | Shared Sheet1 (Data Type = 'Team Strip Selector') |
| Calc field | `team strip selector selected = ${TeamStripSelector}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `TeamStripSelector` = ButtonLabel |

## Files

- `quicksight-team-strip-selector-mobile.json` — QuickSight config
- `test-team-strip-selector-mobile.html` — Local test file
