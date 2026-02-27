# Team Draft View Selector Buttons

2-button selector for team draft view.

## Buttons
MOCK DRAFT TRACKER | DJ'S TOP 50

## QuickSight Setup

### Dataset
Uses the shared **Sheet1** dataset (Static Driver). No separate dataset needed.

**Data Type filter:** `Team Draft View Selector` — scoped to this visual only, using `CONTAINS` match operator with `NON_NULLS_ONLY`.

### Parameter
- Name: `TeamDraftView`, Type: String, Default: `MOCK DRAFT TRACKER`

### Calculated Field (on Sheet1)
```
Name: team draft view selector selected
Expression: ${TeamDraftView}
```

### Field Wells (GROUP BY)
1. `Team Draft View Selector ID` (col 0) — **NumericalDimensionField** (INTEGER type)
2. `Team Draft View Selector` (col 1) — CategoricalDimensionField
3. `team draft view selector selected` (col 2) — CategoricalDimensionField (calc field)

### Navigation Action
- Activation: Select (data point click)
- Action: Set parameter `TeamDraftView` = source field matching `Team Draft View Selector` FieldId

### Target Visuals
Use conditional visibility on widgets:
- Mock Draft Tracker widgets: Show when `${TeamDraftView} = 'MOCK DRAFT TRACKER'`
- DJ's Top 50 widgets: Show when `${TeamDraftView} = 'DJ''S TOP 50'`

### Key Technical Notes
- ID columns are INTEGER in the dataset — must use `NumericalDimensionField`, not `CategoricalDimensionField`
- The calc field name is lowercase with spaces: `team draft view selector selected`
- Filter uses `CONTAINS` operator on `Data Type` column, scoped to this visual's ID only
- Visual dimensions: 800px × 64px in free-form layout

## Files
- `quicksight-team-draft-view-selector.json` — Highcharts config (matches deployed version)
- `team-draft-view-selector-data.csv` — Standalone button data (legacy, not used in shared dataset approach)
- `test-team-draft-view-selector.html` — Local test file
