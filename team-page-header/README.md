# Team Page Header

Scatter-based team header displaying team name, record, and coaching staff in a 5-column layout. Uses Barlow Condensed font loaded via Google Fonts.

## Config

- `quicksight-team-header-v5.json`

## Field Wells (GROUP BY)

| Column | Index | Field | Type |
|--------|-------|-------|------|
| 0 | TeamName | STRING |
| 1 | TeamColor | STRING (hex, e.g. `#A71930`) |
| 2 | Record | STRING (e.g. `10-7 / NFC South Champs`) |
| 3 | GM | STRING |
| 4 | GMSince | STRING (year) |
| 5 | HeadCoach | STRING |
| 6 | HCSince | STRING (year) |
| 7 | OffCoordinator | STRING |
| 8 | OCSince | STRING (year) |
| 9 | DefCoordinator | STRING |
| 10 | DCSince | STRING (year) |

VALUE: (empty)

## Filter Requirement

Add a filter control (e.g. Team dropdown) to limit data to one row. This visual uses single-row extraction (`["get", ["getColumn", X], 0]`).

## Layout

- Row 1 (y=76.3): Team name — 34px, weight 900, uppercase, team color
- Row 2 (y=55): Column labels — 12px, gray, uppercase, includes "SINCE" year
- Row 3 (y=38): Values — 15px (14px for record), bold italic, fixed height 34px for vertical alignment

Columns: Record (x=0, 230px), GM (x=23, 180px), HC (x=41, 180px), OC (x=59, 180px), DC (x=77, 180px)

## Responsive

Stacks vertically at ≤768px with label/value pairs.
