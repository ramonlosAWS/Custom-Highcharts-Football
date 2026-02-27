# Team Page Header - Mobile

Mobile version of the team page header widget for the NFL site.

## Design Approach

- Dashboard designed at **1024px width**, zoomed to fit mobile screens
- This is the standard approach for all mobile widgets on the NFL site
- Layout uses a **2-column flex grid** (50%/50%) instead of the desktop 5-column scatter layout
- Single series with one combined HTML format string (avoids multi-series large-HTML rendering issues)

## Layout

- Team name (full width, top)
- 2-column grid below:
  - Row 1: Record | GM
  - Row 2: HC | OC
  - Row 3: DC | (empty)

## Field Wells (GROUP BY)

Same as desktop v5 — all 11 columns in order:

| Index | Column | Type |
|-------|--------|------|
| 0 | TeamName | STRING |
| 1 | TeamColor | STRING |
| 2 | Record | STRING |
| 3 | GM | STRING |
| 4 | GMSince | STRING |
| 5 | HC | STRING |
| 6 | HCSince | STRING |
| 7 | OC | STRING |
| 8 | OCSince | STRING |
| 9 | DC | STRING |
| 10 | DCSince | STRING |

## Files

- `quicksight-team-header-mobile.json` — QuickSight Highcharts config
- `test-team-header-mobile.html` — Local test file (1024px container)
