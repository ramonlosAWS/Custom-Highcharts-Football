# Highcharts Filter Buttons for QuickSight

Interactive filter button examples using Amazon QuickSight's Highcharts visual, with Kiro AI-assisted development.

## Contents

| File | Description |
|------|-------------|
| `BLOG-POST.md` | Full blog post explaining the pattern + Kiro workflow |
| `quicksight-filter-buttons.md` | **Kiro steering doc** - copy to `.kiro/steering/` |
| `example-1-pill-buttons.json` | Minimal pill-shaped buttons (blue/slate) |
| `example-2-segmented-control.json` | iOS-style segmented control |
| `example-3-icon-buttons.json` | Buttons with emoji icons (green theme) |
| `example-4-gradient-buttons.json` | Gradient accent buttons (purple) |
| `data-example-*.csv` | Sample data files for each example |
| `test-all-buttons.html` | Local preview of all button styles |

## Quick Start

1. Open `test-all-buttons.html` in a browser to preview all styles
2. Choose an example that fits your dashboard
3. Follow the setup steps in `BLOG-POST.md`

## Using with Kiro

1. Copy `quicksight-filter-buttons.md` to `.kiro/steering/` in your project
2. Ask Kiro to create buttons: *"Create filter buttons for status with options ALL, Active, Pending, Complete using the pill style"*
3. Kiro generates the JSON config, CSV data, and setup instructions

See the [blog post](BLOG-POST.md) for detailed walkthrough and example prompts.

## Publishing

This folder is designed to be published as a standalone GitHub repo. Replace `YOUR_USERNAME` in `BLOG-POST.md` with your GitHub username before publishing. The steering doc is the key artifact readers will grab.

## Key Features

- **Single widget** – All buttons in one Highcharts visual
- **Single action** – One navigation action handles all clicks
- **ALL option** – Built-in support for "show all" filter reset
- **Fast performance** – Optimized with disabled animations

## Setup Summary

1. Create parameter: `FilterValue` (String, default: ALL)
2. Upload button CSV with `ButtonLabel` column
3. Add calc field: `SelectedValue = ${FilterValue}`
4. Apply JSON config to Highcharts visual
5. Add navigation action: Set `FilterValue` = `ButtonLabel` (Select specific fields)
6. On target dataset: `ShowByFilter = ifelse(${FilterValue}='ALL', 1, ifelse(YourField=${FilterValue}, 1, 0))`
7. Filter target visuals: `ShowByFilter = 1`

## Customization

### Button Spacing
Adjust the X multiplier in the data mapping:
```json
"x": ["+", 8, ["*", ["itemIndex"], 18]]
```
- Increase `18` for wider spacing
- Decrease for tighter spacing

### Colors
Update the case statements:
```json
"bgColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "#SELECTED", "#UNSELECTED"]
```

### Adding Buttons
Simply add rows to your CSV – the map function creates buttons automatically.

## Performance Tips

- Always set `animation: false` on chart and series
- Use SPICE for button dataset
- Keep button data small (10-20 rows max)
- Calculate colors in data mapping, not pointRender
