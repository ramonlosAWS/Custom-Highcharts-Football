# Draft Round — Mobile (1024px)

Mobile version of the Draft Round button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 7 (ROUND 1, ROUND 2, ROUND 3, ROUND 4, ROUND 5, ROUND 6, ROUND 7) |
| Default | ROUND 1 |
| Rows | 2 (4+3) |
| Chart height | 220px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `DraftRound` (String, default: `ROUND 1`) |
| Dataset | draft-round-data.csv |
| Calc field | `SelectedDraftRound = ${DraftRound}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `DraftRound` = ButtonLabel |

## Files

- `quicksight-draft-round-mobile.json` — QuickSight config
- `test-draft-round-mobile.html` — Local test file
