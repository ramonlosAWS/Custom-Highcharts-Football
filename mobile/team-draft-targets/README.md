# Team Draft Targets — Mobile (1024px)

Mobile version of the Team Draft Targets button set for 1024px tablet/mobile dashboard.

## Layout

| Property | Value |
|----------|-------|
| Buttons | 3 (ROUND 1, DAY 2, DAY 3) |
| Default | ROUND 1 |
| Rows | 1 (3) |
| Chart height | 80px |
| Button size | 186px x 62px |
| Font | 28px Barlow Condensed, weight 700 |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Parameter | `TeamDraftTargets` (String, default: `ROUND 1`) |
| Dataset | team-draft-targets-data.csv |
| Calc field | `SelectedDraftTarget = ${TeamDraftTargets}` |
| Field Wells | GROUP BY: SortOrder (col 0, asc), ButtonLabel (col 1), Selected (col 2) |
| Nav Action | On select, set `TeamDraftTargets` = ButtonLabel |

## Files

- `quicksight-team-draft-targets-mobile.json` — QuickSight config
- `test-team-draft-targets-mobile.html` — Local test file
