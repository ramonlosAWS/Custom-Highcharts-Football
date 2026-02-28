# Mobile Layouts (1024px)

1024px mobile/tablet versions of all button sets and data visuals. Each in its own subfolder with a `quicksight-*-mobile.json` config. Use conditional visibility in QuickSight to show desktop vs mobile.

## Sizing Constants

| Property | Value |
|----------|-------|
| Widget width | 1024px |
| Button div | 186px × 62px |
| Font size | 28px Barlow Condensed, weight 700 |
| Row Y-spacing | 28 units (rows at y=78, 50, 22) |
| Chart height (1 row) | 80px |
| Chart height (2-3 rows) | 220px |
| Chart spacing | [0, 0, 0, 0] |
| Bottom borders | None |
| Right borders | 1px solid #c0c8d1 (except last col per row) |
| X btn units | 18.16 (186px / 10.24px per unit) |

## Y-Position Formula

```
rowY = 78 - (rowIndex × 28)
```

Single-row: y=50. Multi-row: Row 0=78, Row 1=50, Row 2=22.

## X-Position Formula (Centered per row)

```
btnUnits = 186 / (1024 / 100) = 18.16
span = (maxPerRow - 1) × 18.16
startX = (100 - span) / 2
x = startX + (itemIndex % maxPerRow) × 18.16
```

## All 17 Button Sets

| Subfolder | Buttons | Max/Row | Rows | Height |
|-----------|---------|---------|------|--------|
| logo-sort | 2 | 2 | 1 | 80px |
| source-filter | 2 | 2 | 1 | 80px |
| page-selector | 3 | 3 | 1 | 80px |
| unit-filter | 3 | 3 | 1 | 80px |
| team-draft-targets | 3 | 3 | 1 | 80px |
| roster-filter | 3 | 3 | 1 | 80px |
| draft-class | 4 | 4 | 1 | 80px |
| team-strip-selector | 2 | 2 | 1 | 80px |
| team-draft-view-selector | 2 | 2 | 1 | 80px |
| team-view-filter | 3 | 3 | 1 | 80px |
| team-fit-filter | 4 | 4 | 1 | 80px |
| combine-days | 5 | 5 | 1 | 80px |
| fa-board-filter | 4 | 4 | 1 | 80px |
| team-content-body | 3 | 3 | 1 | 80px |
| draft-round | 7 | 4 | 2 | 220px |
| position-filter | 15 | 5 | 3 | 220px |
| rank-by | 13 | 5 | 3 | 220px |

## Files

- `{subfolder}/quicksight-{name}-mobile.json` — QuickSight config for each button set
- `test-all-buttons-mobile.html` — All button sets rendered at 1024px
- `test-position-filter-v4-mobile.html` — Position filter v4 standalone test
- `quicksight-position-filter-mobile.json` — Legacy position filter config (root level)
- `quicksight-position-filter-v4-mobile.json` — Legacy position filter v4 config (root level)

## Data Visuals (1024px)

Scaled-up mobile versions of data visuals. Fonts use Barlow Condensed, sizes increased ~1.5-1.7x from desktop.

| Subfolder | Desktop Source | Height | Key Font Sizes |
|-----------|---------------|--------|----------------|
| team-needs | team-needs/ | 340px | 44px needs, 22px header |
| draft-picks | draft-picks/ | 200px | 22px picks, 14px label |
| cap-space | CapSpace/ (v2) | 280px | 22px value, 18px badge, 14px label |
| jj-draft-capital | jj-draft-capital/ | 90px | 24px rank, 14px label |
| combine-athleticism | combine-athleticism/ | 680px | 36px title, 22px name, 28px rank |
