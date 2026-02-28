# Team Draft View Selector — Mobile (1024px)

Mobile version of the Team Draft View Selector button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 2 (MOCK DRAFT TRACKER, DJ'S TOP 50) |
| Default | MOCK DRAFT TRACKER |
| Rows | 1 (2) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `TeamDraftView` (String, default: `MOCK DRAFT TRACKER`) |
| Dataset | Shared Sheet1 (Data Type = 'Team Draft View Selector') |
| Calc field | `team draft view selector selected = ${TeamDraftView}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `TeamDraftView` = ButtonLabel |

## Files

- `quicksight-team-draft-view-selector-mobile.json` — QuickSight config
- `test-team-draft-view-selector-mobile.html` — Local test file
