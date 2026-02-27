# Team Strip Selector Buttons

2-button selector for team strip view.

## Buttons
OFFSEASON PREVIEW | TEAM NEEDS

## QuickSight Setup

### Dataset
Uses the shared **Sheet1** dataset (Static Driver). No separate dataset needed.

**Data Type filter:** `Team Strip Selector` — scoped to this visual only, using `CONTAINS` match operator with `NON_NULLS_ONLY`.

### Parameter
- Name: `TeamStripSelector`, Type: String, Default: `OFFSEASON PREVIEW`

### Calculated Field (on Sheet1)
```
Name: team strip selector selected
Expression: ${TeamStripSelector}
```

### Field Wells (GROUP BY)
1. `Team Strip Selector ID` (col 0) — **NumericalDimensionField** (INTEGER type)
2. `Team Strip Selector` (col 1) — CategoricalDimensionField
3. `team strip selector selected` (col 2) — CategoricalDimensionField (calc field)

### Navigation Action
- Activation: Select (data point click)
- Action: Set parameter `TeamStripSelector` = source field matching `Team Strip Selector` FieldId

### Target Visuals
Use conditional visibility on widgets:
- Offseason Preview widgets: Show when `${TeamStripSelector} = 'OFFSEASON PREVIEW'`
- Team Needs widgets: Show when `${TeamStripSelector} = 'TEAM NEEDS'`

### Key Technical Notes
- ID columns are INTEGER in the dataset — must use `NumericalDimensionField`, not `CategoricalDimensionField`
- The calc field name is lowercase with spaces: `team strip selector selected`
- Filter uses `CONTAINS` operator on `Data Type` column, scoped to this visual's ID only
- Visual dimensions: 800px × 64px in free-form layout

## Files
- `quicksight-team-strip-selector.json` — Highcharts config (matches deployed version)
- `team-strip-selector-data.csv` — Standalone button data (legacy, not used in shared dataset approach)
- `test-team-strip-selector.html` — Local test file
