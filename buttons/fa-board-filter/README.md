# FA Board Filter Buttons

4-button filter for free agent board view selection.

## Buttons
STREET FA | STAFF CONNECTIONS | OUTGOING | CTR LIST

## QuickSight Setup

### Dataset
Uses the shared **Sheet1** dataset (Static Driver). No separate dataset needed.

**Data Type filter:** `Free Agent Board Filter` — scoped to this visual only, using `CONTAINS` match operator with `NON_NULLS_ONLY`.

### Parameter
- Name: `FABoardFilter`, Type: String, Default: `STREET FA`

### Calculated Field (on Sheet1)
```
Name: selected fa filter
Expression: ${FABoardFilter}
```

### Field Wells (GROUP BY)
1. `FA Board Filter ID` (col 0) — **NumericalDimensionField** (INTEGER type)
2. `FA Board Filter` (col 1) — CategoricalDimensionField
3. `selected fa filter` (col 2) — CategoricalDimensionField (calc field)

### Navigation Action
- Activation: Select (data point click)
- Action: Set parameter `FABoardFilter` = source field matching `FA Board Filter` FieldId

### Target Visuals
Use conditional visibility on widgets:
- Street FA widgets: Show when `${FABoardFilter} = 'STREET FA'`
- Staff Connections widgets: Show when `${FABoardFilter} = 'STAFF CONNECTIONS'`
- Outgoing widgets: Show when `${FABoardFilter} = 'OUTGOING'`
- CTR List widgets: Show when `${FABoardFilter} = 'CTR LIST'`

### Key Technical Notes
- ID columns are INTEGER in the dataset — must use `NumericalDimensionField`, not `CategoricalDimensionField`
- The calc field name is lowercase with spaces: `selected fa filter`
- Filter uses `CONTAINS` operator on `Data Type` column, scoped to this visual's ID only
- Visual dimensions: 928px × 80px in free-form layout

## Files
- `quicksight-fa-board-filter.json` — Highcharts config (matches deployed version)
- `fa-board-filter-data.csv` — Standalone button data (legacy, not used in shared dataset approach)
- `test-fa-board-filter.html` — Local test file
