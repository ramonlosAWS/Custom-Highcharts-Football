# Position Filter Buttons Widget

Interactive button widget for filtering NFL depth chart or roster data by position.

## Overview

This widget creates a horizontal row of clickable position filter buttons (ALL, QB, RB, WR, TE, OT, IOL, DT, EDGE, LB, S, CB, ST) that trigger QuickSight filter actions to show only players at the selected position.

## Features

- **13 Position Buttons**: All major NFL positions plus "ALL" to clear filters
- **Click-to-Filter**: Each button triggers a QuickSight filter action
- **Visual Feedback**: Hover states and cursor pointer for interactivity
- **Responsive Layout**: Buttons automatically space across available width
- **Professional Styling**: NFL-themed colors with modern design

## Data Structure

The widget requires a simple CSV with position codes:

```csv
Position,DisplayName
ALL,ALL
QB,QB
RB,RB
WR,WR
TE,TE
OT,OT
IOL,IOL
DT,DT
EDGE,EDGE
LB,LB
S,S
CB,CB
ST,ST
```

## QuickSight Setup

### 1. Upload Data
```bash
python scripts/quicksight-dataset-manager.py position-filter-buttons/position-filter-data.csv
```

### 2. Add Highcharts Visual
- Add visual → Highcharts visual
- Configure field wells:
  - GROUP BY: Position (column 0), DisplayName (column 1)
  - VALUE: (empty)

### 3. Apply Configuration
- Format visual → Chart code
- Paste contents of `quicksight-position-filter-buttons.json`
- Click APPLY CODE

### 4. Create Filter Action
- Actions → Add action → Filter action
- Name: "Filter by Position"
- Activation: On select
- Filter scope: Same sheet (or All sheets)
- Target visuals: Select visuals to filter (depth chart, roster table, etc.)
- The action will filter based on the Position field

### 5. Configure Target Visuals
Ensure your target visuals (depth chart, roster tables) have a "Position" field that matches the button values (QB, RB, WR, etc.)

## How It Works

1. **Default State**: "ALL" button appears selected (darker blue with darker border)
2. User clicks a position button (e.g., "QB")
3. Highcharts triggers click event with `["triggerClick", {"rowIndex": "point.index"}]`
4. QuickSight filter action activates
5. The clicked button becomes visually selected (darker blue)
6. All visuals on the sheet filter to show only that position
7. Clicking "ALL" clears the position filter and shows all positions

The visual selection state is managed by QuickSight's `dataMarkMatch` function, which highlights the button that matches the current filter selection.

## Customization

### Button Colors
Edit the colors in the `quicksight.pointRender` section:
```json
"color": [
  "case",
  ["dataMarkMatch", ["getColumnName", 0], "point.position"],
  "#005a94",  // Selected button color (darker blue)
  "#0073bb"   // Unselected button color (standard blue)
]
```

### Button Spacing
Adjust X-coordinate calculation:
```json
"x": ["+", 5, ["*", ["itemIndex"], 7.5]]  // Change 7.5 to adjust spacing
```

### Button Size
Modify padding and font size in the format string:
```css
padding:8px 16px;  /* vertical horizontal */
font-size:13px;
```

## Files

- `position-filter-data.csv` - Position button data
- `quicksight-position-filter-buttons.json` - Highcharts configuration
- `test-position-filter-buttons.html` - Local testing file
- `deploy-position-filter-buttons.py` - Deployment script
- `README.md` - This file

## Testing Locally

Open `test-position-filter-buttons.html` in a browser to preview the button layout and styling before deploying to QuickSight.

## Deployment

```bash
# Deploy to QuickSight analysis
python deploy-position-filter-buttons.py
```

## Notes

- The "ALL" button should clear all position filters (configure this in QuickSight filter action settings)
- Buttons work with any visual that has a Position field in its data
- For multi-position players, ensure your data structure handles this appropriately
- Consider adding a visual indicator for which button is currently active (requires calculated field)
