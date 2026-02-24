# Mobile-Responsive Button Designs

Mobile-friendly versions of all 14 Custom Highcharts Football button/filter/toggle widgets.

## Strategy

All buttons use the same responsive pattern: single-row on desktop, multi-row wrapping on mobile (≤500px). The `makeResponsiveChart()` function handles layout math automatically.

| Tier | Buttons | Mobile Approach | Row Split |
|------|---------|-----------------|-----------|
| T1 | 2-4 | Shrink width/font | Stay single row |
| T2 | 5-7 or wide labels | Two rows | 3+2, 4+3, or 1+1+1 |
| T3 | 8-13 | Three+ rows | 5+4+4 or 3+3+3+2+2 |

## All 14 Button Sets

| # | Name | Count | Desktop Div | Mobile Div | Mobile Rows | Tier |
|---|------|-------|-------------|------------|-------------|------|
| 1 | Logo Sort | 2 | 100px | 80px | 2 | T1 |
| 2 | Source Filter | 2 | 185px | 140px | 2 | T1 |
| 3 | Page Selector | 3 | 45px | 40px | 3 | T1 |
| 4 | Unit Filter | 3 | 105px | 80px | 3 | T1 |
| 5 | Team Draft Targets | 3 | 90px | 75px | 3 | T1 |
| 6 | Roster Filter | 3 | 113px | 85px | 3 | T1 |
| 7 | Team View Filter | 3 | 163px | 110px | 3 | T1 |
| 8 | Draft Class | 4 | 60px | 55px | 4 | T1 |
| 9 | Team Fit Filter | 4 | 138px | 80px | 2+2 | T1 |
| 10 | Combine Days | 5 | 70px | 65px | 3+2 | T2 |
| 11 | Draft Round | 7 | 85px | 72px | 4+3 | T2 |
| 12 | Team Content Body | 3 wide | 220px | 200px | 1+1+1 | T2 |
| 13 | Position Filter | 13 | 48px | 56px | 5+4+4 | T3 |
| 14 | Rank By | 13 wide | 110px | 100px | 3+3+3+2+2 | T3 |

## Files

- `test-all-buttons-mobile.html` — Master test file with all 14 sets (open in browser, resize to test)
- `test-position-filter-mobile.html` — Position filter standalone test (desktop + mobile + responsive)
- `quicksight-position-filter-mobile.json` — QuickSight config for position filter mobile layout
- `position-filter-mobile-data.csv` — Position filter data with RowNum/RowIndex columns

## Testing

Open `test-all-buttons-mobile.html` in a browser. A width indicator shows in the top-right corner. Resize below 500px to see all buttons switch to mobile layout. Click any button to verify selection state works.

## QuickSight Implementation

Since QuickSight `responsive` rules can change format strings and chart height but NOT data point positions, use one of:

1. **Separate mobile visual** — Dedicated config with pre-calculated multi-row positions. Use conditional visibility to show desktop vs mobile.
2. **Pre-calculated row data** — Add RowNum/RowIndex to CSV, use `case` expressions for x/y positioning. Single visual handles mobile natively.

See `quicksight-position-filter-mobile.json` for the Approach 2 pattern.
