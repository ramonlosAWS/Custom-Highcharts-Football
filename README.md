# NFL Buttons

Reusable QuickSight Highcharts button widgets for NFL dashboards. Each subfolder is a self-contained button set.

## Button Template Pattern

All buttons follow the same architecture:
- Single Highcharts scatter widget with `map` over data
- Thin segmented style: vertical dividers, square selected fill
- Data-driven highlighting via calc field comparing to parameter
- CSV with `SortOrder` column to guarantee button order

### QuickSight Setup (same for all buttons)

1. Create parameter (String, set default)
2. Upload CSV dataset to SPICE
3. Add calc field: `SelectedValue = ${ParameterName}`
4. Field Wells GROUP BY: SortOrder (col 0, sort asc), ButtonLabel (col 1), SelectedValue (col 2)
5. Add navigation action: on select, set parameter = ButtonLabel field
6. On target datasets, add calc field: `ShowByFilter = ifelse(${Param}='ALL', 1, ifelse(Field=${Param}, 1, 0))`
7. Filter target visuals: `ShowByFilter = 1`

### Customizing for New Button Sets

To create a new button set from this template:
1. Copy any subfolder
2. Update CSV with your labels and sort order
3. In the JSON config, adjust:
   - `startX` and spacing based on button count (see math below)
   - Last button index in `div` case expression
   - Parameter name in `_comment`
4. Update test HTML with your labels

### Spacing Math

```
Chart width: 800px, spacing [5,0,5,0] → plot area 800px
1 xAxis unit = 800 / 100 = 8px
Button center spacing = buttonWidthPx / 8
startX = (100 - numButtons * spacing) / 2 + spacing / 2
Last button index = numButtons - 1 (for div border-right: none)
```

## Button Sets

### From Static Driver CSV
- `position-filter/` — Position groups (13 buttons: All, QB, RB, WR, TE, T, G, C, DT, ED, LB, CB, S)
- `combine-days/` — Combine days (5 buttons: All, Day 1, Day 2, Day 3, Day 4)
- `rank-by/` — Rank metric (13 buttons: Overall Score, Production Score, Athleticism Score, 10-yd Split, 40 Time, 40 Top Speed, Vertical Jump, Broad Jump, Short Shuttle, Three Cone, Height, Weight, Arm Length)
- `draft-class/` — Draft class year (4 buttons: All, 2023, 2024, 2025)
- `logo-sort/` — Logo sort order (2 buttons: Alpha, Draft Order)
- `team-content-body/` — Team content section (3 buttons: DRAFT CLASS, FRONT OFFICE TENDENCIES, MOCK DRAFT TRACKER)
- `team-draft-targets/` — Team draft targets (3 buttons: ROUND 1, DAY 2, DAY 3)
- `draft-round/` — Draft round (7 buttons: ROUND 1 through ROUND 7)
- `roster-filter/` — Roster view (3 buttons: STARTERS, TOP 51, 90-MAN)

### From Design
- `unit-filter/` — Offense/Defense unit (3 buttons: ALL, OFFENSE, DEFENSE)
- `team-fit-filter/` — Team fit analysis (4 buttons: TEAM FIT, TOP 101, OUTGOING, CUT CANDIDATES)
- `source-filter/` — Draft source (2 buttons: GRINDING THE MOCKS, DJ'S TOP 50)
- `page-selector/` — Pagination (3 buttons: 1, 2, 3)
- `team-view-filter/` — Team page views (3 buttons: TEAM SNAPSHOT, TEAM NEEDS, DIVISION RANKS)
