# Position Filter Buttons - Parameter Approach

This approach uses a parameter + calculated field to handle filtering, including an "ALL" option that shows all data.

## Files

- `quicksight-position-buttons-FILTER-v3.json` - Position buttons (data-driven from dataset)
- `quicksight-ALL-button.json` - Separate ALL button widget

## Setup Steps

### 1. Create Parameter

In QuickSight Analysis:
1. Go to Parameters → Create parameter
2. Name: `PositionFilter`
3. Data type: String
4. Default value: `ALL`

### 2. Create Calculated Field for Button Highlighting

On the dataset used by the button widget:
1. Add calculated field: `SelectedPosition`
2. Expression: `${PositionFilter}`

This returns the current parameter value for each row.

### 3. Create Calculated Field for Target Visuals

On the dataset(s) you want to filter (e.g., NFL Raw Roster):
1. Add calculated field: `ShowByPosition`
2. Expression:
```
ifelse(${PositionFilter} = 'ALL', 1, ifelse(position = ${PositionFilter}, 1, 0))
```

### 4. Add Filter to Target Visuals

On each visual you want filtered:
1. Add filter on `ShowByPosition`
2. Filter type: Equal to
3. Value: `1`

### 5. Configure Position Buttons Widget

1. Create Highcharts visual with `quicksight-position-buttons-FILTER-v3.json`
2. Field Wells: Add `position` field to GROUP BY
3. Add Navigation Action:
   - Name: `Set Position`
   - Activation: On select
   - Target: Same analysis
   - Set parameter: `PositionFilter` = `{{position}}`

### 6. Configure ALL Button Widget

1. Create Highcharts visual with `quicksight-ALL-button.json`
2. Field Wells: None needed (hardcoded)
3. Add Navigation Action:
   - Name: `Show All`
   - Activation: On select
   - Target: Same analysis
   - Set parameter: `PositionFilter` = `ALL` (literal string)

## How It Works

| User Action | Parameter Value | Result |
|-------------|-----------------|--------|
| Click "QB" | `PositionFilter = "QB"` | Only QB rows shown |
| Click "RB" | `PositionFilter = "RB"` | Only RB rows shown |
| Click "ALL" | `PositionFilter = "ALL"` | All rows shown |

The calculated field `ShowByPosition` evaluates to:
- `1` when parameter is "ALL" (show everything)
- `1` when position matches parameter (show matching)
- `0` otherwise (hide)

Filter `ShowByPosition = 1` shows only the rows that should be visible.

## Button Selection Highlighting (Optional)

To show which button is currently selected, update the position buttons config to use `SelectedPosition` calc field and add `pointRender` styling. See `quicksight-position-buttons-PARAMETER.json` for an example with selection highlighting.

## Embedding

When embedding with the SDK, you can set the initial parameter:

```javascript
const embeddedDashboard = await embedDashboard({
  url: dashboardUrl,
  parameters: [
    { Name: "PositionFilter", Values: ["ALL"] }
  ]
});
```

Button clicks update the parameter automatically within QuickSight - no additional SDK code needed.
