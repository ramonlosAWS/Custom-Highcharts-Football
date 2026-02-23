# Page Selector Buttons

3-button pagination control for multi-page views.

## Buttons
1 | 2 | 3

## QuickSight Setup

### Parameter
- Name: `PageSelector`, Type: String, Default: `1`

### Dataset
Upload `page-selector-data.csv` to SPICE. Add calculated field:
```
Name: SelectedPage
Expression: ${PageSelector}
```

### Field Wells (GROUP BY)
1. `SortOrder` (col 0) — sort ascending
2. `ButtonLabel` (col 1)
3. `SelectedPage` (col 2)

### Navigation Action
- Activation: Select
- Action: Set parameter `PageSelector` = field `ButtonLabel`

### Target Visuals
Use conditional visibility on widgets:
- Page 1 widgets: Show when `${PageSelector} = '1'`
- Page 2 widgets: Show when `${PageSelector} = '2'`
- Page 3 widgets: Show when `${PageSelector} = '3'`

## Files
- `quicksight-page-selector.json` — Highcharts config
- `page-selector-data.csv` — Button data (3 rows)
- `test-page-selector.html` — Local test file

## Widget Size
- Chart width: ~150px
- Chart height: 30px
- Button div: 36px wide, 17px tall, 11px font
