# QuickSight Highcharts Filter Buttons - Kiro Steering Guide

> **Usage:** Copy this file to `.kiro/steering/quicksight-filter-buttons.md` in your workspace. Kiro will automatically use it as context when you ask about QuickSight filter buttons.
>
> **Source:** [quicksight-highcharts-buttons](https://github.com/YOUR_USERNAME/quicksight-highcharts-buttons)

This steering document provides patterns for creating interactive filter buttons in Amazon QuickSight using Highcharts visuals.

## QuickSight Highcharts Fundamentals

Amazon QuickSight includes a Highcharts visual that renders charts from JSON configuration. Understanding these constraints is essential for generating correct configs.

### Version & Security

- QuickSight uses **Highcharts 11.4.6** — all features must be compatible with this version
- The editor accepts **JSON only** — no JavaScript functions, no CSS blocks, no raw HTML input
- All styling is done via inline styles in `useHTML: true` data labels
- For local testing, use: `<script src="https://code.highcharts.com/11.4.6/highcharts.js"></script>`

### QuickSight Expression Syntax

QuickSight replaces standard Highcharts JavaScript data binding with a JSON expression language:

```json
// Get column data (returns array of all values)
["getColumn", 0]           // First field in field wells
["getColumn", 0, 1, 2]     // Multiple columns (array of arrays)

// Get column name
["getColumnName", 0]

// Iterate over rows
["map", ["getColumn", 0, 1], {
  "name": ["get", ["item"], 0],    // Column 0 value for current row
  "value": ["get", ["item"], 1]    // Column 1 value for current row
}]

// Current row index (0-based)
["itemIndex"]

// Arithmetic
["+", value1, value2]
["*", value1, value2]
["/", value1, value2]
["-", value1, value2]

// Conditional logic
["case",
  ["==", value1, value2], "result_if_true",
  [">=", value1, value3], "result_if_second_true",
  "default_result"
]

// String concatenation
["+", "prefix-", ["get", ["item"], 0], "-suffix"]

// Filter rows
["filter", ["getColumn", 0, 1],
  ["==", ["get", ["item"], 0], "targetValue"]
]

// Unique values
["unique", ["getColumn", 0]]

// Extract single value from column (for filtered single-row data)
["get", ["getColumn", 0], 0]    // First element of column array

// Click events (for navigation actions)
["triggerClick", { "rowIndex": "point.index" }]
```

### Field Wells

- **GROUP BY**: Dimension fields — use for all filter button data
- **VALUE**: Measure fields — leave empty for button widgets
- Column indices in `["getColumn", X]` match the order fields appear in GROUP BY
- Maximum 20 dimension fields in GROUP BY

### Data Labels with HTML

QuickSight supports rich HTML in data labels when `useHTML: true`:
- Supported: `<div>`, `<span>`, `<b>`, `<i>`, `<br>`, `<p>`, `<ul>`, `<li>`, `<table>`
- Not supported: `<a>` (links), `<img>` (external images), `<script>`, `<style>`
- All styling must be inline: `style='color:red;font-size:14px;'`
- Use `{point.propertyName}` to reference data point properties in format strings

## Overview

Filter buttons allow users to click to filter dashboard data. This pattern uses:
- Single Highcharts widget containing all buttons
- Single navigation action that passes clicked value dynamically
- Parameter-based filtering with "ALL" option support
- Visual highlighting of selected button

## Architecture

| Component | Location | Purpose |
|-----------|----------|---------|
| Parameter | Analysis | Stores selected filter value (String, default: ALL) |
| Button Dataset | Small CSV | Defines button labels (includes ALL row) |
| `SelectedValue` calc field | Button dataset | Returns `${ParameterName}` for highlighting |
| `ShowByFilter` calc field | Target dataset | Handles ALL logic: `ifelse(${Param}='ALL', 1, ifelse(Field=${Param}, 1, 0))` |
| Filter | Target visuals | `ShowByFilter = 1` |

## Base JSON Pattern

All button styles follow this structure:

```json
{
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 50,
    "spacing": [5, 10, 5, 10],
    "animation": false
  },
  "title": { "text": null },
  "legend": { "enabled": false },
  "credits": { "enabled": false },
  "xAxis": { "min": 0, "max": 100, "visible": false },
  "yAxis": { "min": 0, "max": 100, "visible": false },
  "tooltip": { "enabled": false },
  "plotOptions": {
    "scatter": { "marker": { "enabled": false }, "animation": false },
    "series": { "enableMouseTracking": true, "cursor": "pointer", "animation": false }
  },
  "series": [{
    "name": "Buttons",
    "data": [
      "map",
      ["getColumn", 0, 1],
      {
        "x": ["+", START_X, ["*", ["itemIndex"], SPACING]],
        "y": 50,
        "label": ["get", ["item"], 0],
        "bgColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "SELECTED_BG", "UNSELECTED_BG"],
        "textColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "SELECTED_TEXT", "UNSELECTED_TEXT"],
        "borderColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "SELECTED_BORDER", "UNSELECTED_BORDER"]
      }
    ],
    "dataLabels": {
      "enabled": true,
      "useHTML": true,
      "format": "HTML_TEMPLATE_HERE",
      "align": "center",
      "verticalAlign": "middle",
      "style": { "textOutline": "none" }
    },
    "point": { "events": { "click": ["triggerClick", { "rowIndex": "point.index" }] } }
  }]
}
```

## Button Style Templates

### Style 1: Minimal Pill Buttons
- Border radius: 20px (full pill)
- Colors: Blue (#3b82f6) selected, slate (#f1f5f9) unselected
- Padding: 8px 16px
- Best for: Compact spaces, minimal dashboards

```json
"format": "<div style='background:{point.bgColor};color:{point.textColor};padding:8px 16px;border-radius:20px;cursor:pointer;font-weight:500;font-size:13px;border:1px solid {point.borderColor};'>{point.label}</div>"
```

### Style 2: Segmented Control
- No border radius (connected look)
- Colors: Dark slate (#1e293b) selected, white unselected
- Border: 2px solid on all buttons
- Best for: Binary choices, iOS-style controls

```json
"format": "<div style='background:{point.bgColor};color:{point.textColor};padding:10px 20px;cursor:pointer;font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:0.5px;border:2px solid #1e293b;margin:-1px;'>{point.label}</div>"
```

### Style 3: Icon Buttons
- Includes emoji/icon above label
- Border radius: 8px
- Colors: Green (#059669) selected, mint (#f0fdf4) unselected
- Requires 3rd column for icon in data
- Best for: Category filters, department selectors

```json
"format": "<div style='background:{point.bgColor};color:{point.textColor};padding:10px 14px;border-radius:8px;cursor:pointer;font-weight:600;font-size:11px;border:2px solid {point.borderColor};text-align:center;min-width:60px;'><div style='font-size:18px;margin-bottom:2px;'>{point.icon}</div>{point.label}</div>"
```

Data mapping addition:
```json
"icon": ["get", ["item"], 2]
```

### Style 4: Gradient Buttons
- Gradient backgrounds
- Box shadows for depth
- Border radius: 10px
- Best for: Hero dashboards, executive views

```json
"format": "<div style='background:{point.bgGradient};color:{point.textColor};padding:12px 20px;border-radius:10px;cursor:pointer;font-weight:600;font-size:13px;box-shadow:{point.shadow};min-width:70px;text-align:center;'>{point.label}</div>"
```

Data mapping:
```json
"bgGradient": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%)"],
"shadow": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "0 4px 15px rgba(102, 126, 234, 0.4)", "0 2px 8px rgba(0,0,0,0.08)"]
```

## Spacing Guidelines

| Buttons | X Start | X Multiplier | Chart Width |
|---------|---------|--------------|-------------|
| 3-4 | 12 | 25 | 100 (default) |
| 5-6 | 8 | 18 | 100 (default) |
| 8-10 | 5 | 10-12 | 100 (default) |
| 12+ | 3 | 7-8 | 100 (default) |

## Field Wells Configuration

GROUP BY (in order):
1. `ButtonLabel` (column 0) - The button text
2. `SelectedValue` (column 1) - Calc field returning parameter value
3. `Icon` (column 2) - Optional, for icon buttons only

VALUE: Empty (never use VALUE for this pattern)

## Navigation Action Setup

1. Actions → Add action
2. Name: "Set Filter" (or descriptive name)
3. Activation: Select
4. Type: Navigation action
5. Target: Current sheet
6. Parameters: Click + icon
   - Parameter: Your parameter name
   - Value: Select specific fields → ButtonLabel

CRITICAL: Must use "Select specific fields" to pass clicked value dynamically.

## Target Visual Filtering

On each target dataset, add calculated field:
```
ShowByFilter = ifelse(${FilterValue}='ALL', 1, ifelse(YourFieldName=${FilterValue}, 1, 0))
```

On each target visual, add filter:
- Field: ShowByFilter
- Condition: Equals 1

## Performance Requirements

Always include these settings:
- `"animation": false` on chart
- `"animation": false` in plotOptions.scatter
- `"animation": false` in plotOptions.series
- Use SPICE for button dataset
- Keep button data under 20 rows
- Calculate colors in data mapping (not pointRender)

## Sample Data Formats

### Basic (2 columns):
```csv
ButtonLabel
ALL
Option1
Option2
Option3
```

### With Icons (3 columns):
```csv
ButtonLabel,Icon
ALL,📊
Sales,💰
Marketing,📢
Engineering,⚙️
```

Note: SelectedValue is a calculated field, not in CSV.

## Color Palettes

### Blue Theme (Pill Buttons)
- Selected: bg=#3b82f6, text=#ffffff, border=#3b82f6
- Unselected: bg=#f1f5f9, text=#475569, border=#e2e8f0

### Dark Theme (Segmented)
- Selected: bg=#1e293b, text=#ffffff
- Unselected: bg=#ffffff, text=#1e293b

### Green Theme (Icon Buttons)
- Selected: bg=#059669, text=#ffffff, border=#059669
- Unselected: bg=#f0fdf4, text=#166534, border=#bbf7d0

### Purple Gradient Theme
- Selected: gradient=#667eea→#764ba2, text=#ffffff
- Unselected: gradient=#f5f7fa→#e4e8ec, text=#4a5568

## Troubleshooting

### Buttons not highlighting
- Verify SelectedValue calc field exists on button dataset
- Check both columns in GROUP BY field wells
- Ensure calc field formula is `${ParameterName}` (exact match)

### ALL shows no data
- Verify ShowByFilter calc field on TARGET dataset (not button dataset)
- Check filter ShowByFilter = 1 on target visual
- Verify calc field handles ALL case first

### Navigation action not working
- Must use "Select specific fields" for parameter value
- Parameter name must match exactly (case-sensitive)
- Verify action activation is "Select"

### Buttons overlapping
- Increase X multiplier in data mapping
- Reduce number of buttons
- Decrease font size or padding
