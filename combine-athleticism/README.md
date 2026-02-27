# Combine Athleticism Scores

Horizontal bar chart showing top athleticism scores by position from the NFL Combine.

## Design
- Dark background (#1a1a2e)
- Horizontal bars with gradient fill and color-coded score circles
- College logos via base64 bubble markers (the only way to show images in QuickSight)
- NFL Draft badge (top right)
- Next Gen Stats logo (bottom left)
- Gradient legend bar at bottom

## Score Tiers
| Range | Color | Label |
|-------|-------|-------|
| 90-100 | #0077c8 (Blue) | ELITE |
| 75-89 | #00b050 (Green) | GOOD |
| 60-74 | #ffc000 (Yellow) | AVERAGE |
| 50-59 | #c00000 (Red) | < AVG |

## Data Structure (CSV)
```
Rank,PlayerName,College,CollegeLogo,Score,BarColor
1,First Last,Florida,url(data:image/png;base64,...),92,#0077c8
```

CollegeLogo must be in `url(data:image/png;base64,...)` format for bubble marker.symbol.

## Field Wells (GROUP BY)
- Rank (column 0) - INTEGER
- PlayerName (column 1) - STRING
- College (column 2) - STRING
- CollegeLogo (column 3) - STRING (base64 with url() wrapper)
- Score (column 4) - INTEGER
- BarColor (column 5) - STRING (hex color)

## Files
- `quicksight-combine-athleticism.json` - QuickSight Highcharts config
- `test-combine-athleticism.html` - Local test file
- `combine-athleticism-data.csv` - Sample data
- `college-logos-base64.csv` - All 131 FBS college logos as base64
- `generate-test.py` - Generates test HTML with downloaded logos
- `download-college-logos.py` - Downloads all FBS logos to CSV
- `highcharts-more.js` - Local copy for bubble chart support in test files

## Local Testing
Load from local files (CDN blocked on file:// protocol):
- `../CapSpace/working/highcharts.js` for Highcharts core
- `highcharts-more.js` (local copy) for bubble chart support
