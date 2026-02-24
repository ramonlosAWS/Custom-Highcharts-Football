# Mobile Button Layouts

Fixed-width (340px) mobile versions of all 14 button sets. No responsive switching — each is a dedicated mobile visual. In QuickSight, use conditional visibility to show desktop vs mobile.

## Layout Strategy

| Tier | Buttons | Mobile Approach | Examples |
|------|---------|-----------------|----------|
| T1 | 2-4 | Single row, shrunk | Logo Sort, Page Selector, Unit Filter |
| T2 | 5-7 or wide labels | Two rows | Combine Days (3+2), Draft Round (4+3) |
| T3 | 8-13 | Three+ rows | Position Filter (5+4+4), Rank By (3×3+2×2) |

## All 14 Sets

| Name | Count | Div Width | Rows | Chart Height |
|------|-------|-----------|------|-------------|
| Logo Sort | 2 | 140px | 2 | 38px |
| Source Filter | 2 | 145px | 2 | 38px |
| Page Selector | 3 | 40px | 3 | 38px |
| Unit Filter | 3 | 90px | 3 | 38px |
| Team Draft Targets | 3 | 80px | 3 | 38px |
| Roster Filter | 3 | 85px | 3 | 38px |
| Draft Class | 4 | 70px | 4 | 38px |
| Team View Filter | 3 wide | 110px | 2+1 | 80px |
| Team Fit Filter | 4 | 100px | 2+2 | 80px |
| Combine Days | 5 | 80px | 3+2 | 80px |
| Draft Round | 7 | 72px | 4+3 | 80px |
| Team Content Body | 3 very wide | 280px | 1+1+1 | 110px |
| Position Filter | 13 | 56px | 5+4+4 | 110px |
| Rank By | 13 wide | 100px | 3+3+3+2+2 | 170px |

## Files

- `test-all-buttons-mobile.html` — All 14 sets at 340px fixed width
- `test-position-filter-mobile.html` — Position filter standalone
- `quicksight-position-filter-mobile.json` — QuickSight config (position filter)
- `position-filter-mobile-data.csv` — Data with RowNum/RowIndex columns

## Centering Math

Each row is independently centered:
```
span = (buttonsInRow - 1) × btnUnits
startX = (100 - span) / 2
```
Where `btnUnits = divPx / (chartWidth / 100)`.

Rows with fewer buttons naturally center narrower, creating a clean pyramid effect.
