# Team Needs — Mobile (1024px)

Mobile version of the Team Needs widget for 1024px tablet dashboard.

## Layout

| Property | Value |
|----------|-------|
| Chart height | 340px |
| Needs font | 44px Barlow Condensed, weight 700 |
| Header font | 22px |
| Border left | 6px solid team color |
| Content width | 920px |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Field Wells | GROUP BY: UniqueID (col 0), TeamAbbr (col 1), TeamColor (col 2), TeamNeeds (col 3) |
| Filter | TeamAbbr (single team) |

## Files

- `quicksight-team-needs-mobile.json` — QuickSight config
- `test-team-needs-mobile.html` — Local test file
