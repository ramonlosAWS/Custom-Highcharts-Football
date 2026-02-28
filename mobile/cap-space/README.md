# Cap Space — Mobile (1024px)

Mobile version of the Cap Metrics v2 widget for 1024px tablet dashboard.

## Layout

| Property | Value |
|----------|-------|
| Chart height | 280px |
| Value font | 22px Barlow Condensed, weight 700 |
| Label font | 14px |
| Accent bar | 6px wide |
| Rank badge | 56px wide, 18px font |
| Progress bar | 180px wide, 16px tall |

## QuickSight Setup

| Property | Value |
|----------|-------|
| GROUP BY | CapSpaceRank (col 0), ActiveCapRank (col 1), DeadMoneyRank (col 2) |
| VALUE | CapSpace (col 0), ActiveCap (col 1), DeadMoney (col 2) |
| Filter | Team Abbr (single team) |

## Files

- `quicksight-cap-space-mobile.json` — QuickSight config
- `test-cap-space-mobile.html` — Local test file
