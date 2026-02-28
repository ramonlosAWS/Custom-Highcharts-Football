# Combine Athleticism — Mobile (1024px)

Mobile version of the Combine Athleticism Scores visual for 1024px tablet dashboard.

## Layout

| Property | Value |
|----------|-------|
| Chart height | 680px |
| Background | #1a1a2e (dark) |
| Title font | 36px Barlow Condensed, weight 900 |
| Player name | 22px, weight 800 |
| Rank font | 28px |
| Score bubble | 48px diameter, 20px font |
| Row width | 920px |
| Logo size | 54px (bubble minSize/maxSize) |
| Legend bar | 340px wide |

## QuickSight Setup

| Property | Value |
|----------|-------|
| Field Wells | GROUP BY: Rank(0), PlayerName(1), College(2), CollegeLogoBase64(3), Score(4), BarColor(5) |
| Filter | Position group |

## Files

- `quicksight-combine-athleticism-mobile.json` — QuickSight config
- `test-combine-athleticism-mobile.html` — Local test file
