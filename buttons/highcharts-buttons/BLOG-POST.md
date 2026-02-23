# Building Interactive Filter Buttons in Amazon QuickSight with Highcharts and Kiro

*Accelerate dashboard development with AI-assisted coding*

## Introduction

Amazon QuickSight's Highcharts visual opens up powerful customization possibilities beyond traditional charts. One compelling use case is creating interactive filter buttons that let users quickly filter dashboard data with a single click—including an "ALL" option to reset filters.

In this post, we'll walk through a proven pattern for building filter buttons and show how [Kiro](https://kiro.dev), an AI-powered IDE, can accelerate your development workflow. We'll provide four ready-to-use examples and a steering document you can use with Kiro to generate custom button styles.

## Why Use Kiro for QuickSight Development?

QuickSight's Highcharts visual requires JSON configuration with a specific expression syntax (`["getColumn", 0]`, `["map", ...]`, etc.) that differs from standard Highcharts JavaScript. This learning curve can slow down development.

Kiro helps by:
- **Understanding the pattern** – Feed Kiro a steering document with the button pattern, and it generates correct QuickSight-compatible JSON
- **Rapid iteration** – Describe the style you want ("make it purple with rounded corners"), and Kiro updates the configuration
- **Consistency** – Kiro follows the documented architecture, ensuring all buttons work the same way
- **Troubleshooting** – Describe issues ("buttons aren't highlighting"), and Kiro identifies missing calc fields or configuration errors

## The Solution Architecture

Our filter button pattern uses these components:

| Component | Purpose |
|-----------|---------|
| **Parameter** | Stores the selected filter value |
| **Button Dataset** | Small CSV defining button labels (includes "ALL") |
| **Calculated Field (buttons)** | Returns current parameter value for highlighting |
| **Calculated Field (target)** | Handles "ALL" logic for filtering |
| **Navigation Action** | Passes clicked button value to parameter |

### Why This Works

The key insight is using QuickSight's navigation action with "Select specific fields" to dynamically pass the clicked button's value to the parameter. Combined with a calculated field that handles the "ALL" case, we get a complete filter solution in a single widget.

## Setting Up Kiro for QuickSight Button Development

The key to getting great results from Kiro is giving it context about the pattern. We've published a ready-to-use steering document that teaches Kiro everything it needs to know about QuickSight filter buttons.

### Step 1: Grab the Steering Document

Clone or download the steering doc from the companion repo:

> **GitHub:** [quicksight-highcharts-buttons](https://github.com/YOUR_USERNAME/quicksight-highcharts-buttons)

The repo contains:
- `quicksight-filter-buttons.md` – The Kiro steering document
- Four example JSON configurations
- Sample CSV data files
- An HTML test page to preview all styles locally

### Step 2: Add It to Your Project

Copy the steering doc into your workspace:

```bash
# Create the steering directory if it doesn't exist
mkdir -p .kiro/steering

# Copy the steering doc
cp quicksight-filter-buttons.md .kiro/steering/
```

Once it's in `.kiro/steering/`, Kiro automatically picks it up for every conversation in that workspace. The steering doc teaches Kiro:
- The JSON structure for filter buttons
- Four style templates (pill, segmented, icon, gradient)
- Field wells configuration and column ordering
- Navigation action setup
- Spacing calculations for different button counts
- Performance requirements and troubleshooting

### Step 3: Ask Kiro to Generate Buttons

With the steering document in place, you can prompt Kiro naturally:

> "Create a filter button widget for department filtering with options: ALL, Sales, Marketing, Engineering, Support. Use the green icon style with emoji icons."

Kiro generates:
1. The complete JSON configuration
2. Sample CSV data with appropriate icons
3. Setup instructions for the parameter and calc fields

### Step 4: Iterate on Design

Need changes? Just ask:

> "Make the buttons more compact with smaller padding"

> "Change to a blue color scheme"

> "Add a 'Finance' option with a 💵 icon"

Kiro updates the configuration while maintaining the correct architecture because the steering doc defines the rules.

## Implementation Steps

### Step 1: Create the Parameter

In your QuickSight analysis:
- Name: `FilterValue`
- Type: String
- Default: `ALL`

### Step 2: Create Button Dataset

Upload a simple CSV:
```csv
ButtonLabel
ALL
Option1
Option2
Option3
Option4
```

Add calculated field on this dataset:
```
SelectedValue = ${FilterValue}
```

### Step 3: Configure Highcharts Visual

Add a Highcharts visual with:
- Field Wells: `ButtonLabel`, `SelectedValue` in GROUP BY
- Apply the JSON configuration (see examples below)

### Step 4: Add Navigation Action

1. Actions → Add action
2. Activation: Select
3. Type: Navigation action
4. Parameters: Click **+**, select `FilterValue`, choose "Select specific fields" → `ButtonLabel`

### Step 5: Setup Target Visual Filtering

On your target dataset, add:
```
ShowByFilter = ifelse(${FilterValue}='ALL', 1, ifelse(YourField=${FilterValue}, 1, 0))
```

Add filter on target visuals: `ShowByFilter = 1`

---

## Example 1: Minimal Pill Buttons

Clean, modern pill-shaped buttons with subtle styling.

**Best for:** Compact spaces, minimal dashboards

**Kiro prompt:** *"Create minimal pill-style filter buttons with blue selected state and light gray unselected"*

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
        "x": ["+", 8, ["*", ["itemIndex"], 18]],
        "y": 50,
        "label": ["get", ["item"], 0],
        "bgColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "#3b82f6", "#f1f5f9"],
        "textColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "#ffffff", "#475569"],
        "borderColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "#3b82f6", "#e2e8f0"]
      }
    ],
    "dataLabels": {
      "enabled": true,
      "useHTML": true,
      "format": "<div style='background:{point.bgColor};color:{point.textColor};padding:8px 16px;border-radius:20px;cursor:pointer;font-weight:500;font-size:13px;border:1px solid {point.borderColor};'>{point.label}</div>",
      "align": "center",
      "verticalAlign": "middle",
      "style": { "textOutline": "none" }
    },
    "point": { "events": { "click": ["triggerClick", { "rowIndex": "point.index" }] } }
  }]
}
```

**Sample Data:**
```csv
ButtonLabel
ALL
Active
Pending
Completed
Archived
```

---

## Example 2: Bold Segmented Control

iOS-style segmented control with connected buttons.

**Best for:** Binary or small option sets, prominent placement

**Kiro prompt:** *"Create iOS-style segmented control buttons with dark slate selected and white unselected, uppercase text"*

```json
{
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 55,
    "spacing": [8, 15, 8, 15],
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
    "name": "Segments",
    "data": [
      "map",
      ["getColumn", 0, 1],
      {
        "x": ["+", 12, ["*", ["itemIndex"], 25]],
        "y": 50,
        "label": ["get", ["item"], 0],
        "isFirst": ["==", ["itemIndex"], 0],
        "isLast": ["==", ["itemIndex"], 3],
        "bgColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "#1e293b", "#ffffff"],
        "textColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "#ffffff", "#1e293b"]
      }
    ],
    "dataLabels": {
      "enabled": true,
      "useHTML": true,
      "format": "<div style='background:{point.bgColor};color:{point.textColor};padding:10px 20px;cursor:pointer;font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:0.5px;border:2px solid #1e293b;margin:-1px;'>{point.label}</div>",
      "align": "center",
      "verticalAlign": "middle",
      "style": { "textOutline": "none" }
    },
    "point": { "events": { "click": ["triggerClick", { "rowIndex": "point.index" }] } }
  }]
}
```

**Sample Data:**
```csv
ButtonLabel
ALL
Q1
Q2
Q3
```

---

## Example 3: Icon-Style Category Buttons

Buttons with emoji/icon indicators for visual categorization.

**Best for:** Category filters, status indicators, department selectors

**Kiro prompt:** *"Create category filter buttons with emoji icons above the label, green theme, for department filtering"*

```json
{
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 65,
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
    "name": "Categories",
    "data": [
      "map",
      ["getColumn", 0, 1, 2],
      {
        "x": ["+", 10, ["*", ["itemIndex"], 18]],
        "y": 50,
        "label": ["get", ["item"], 0],
        "icon": ["get", ["item"], 2],
        "bgColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "#059669", "#f0fdf4"],
        "textColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "#ffffff", "#166534"],
        "borderColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "#059669", "#bbf7d0"]
      }
    ],
    "dataLabels": {
      "enabled": true,
      "useHTML": true,
      "format": "<div style='background:{point.bgColor};color:{point.textColor};padding:10px 14px;border-radius:8px;cursor:pointer;font-weight:600;font-size:11px;border:2px solid {point.borderColor};text-align:center;min-width:60px;'><div style='font-size:18px;margin-bottom:2px;'>{point.icon}</div>{point.label}</div>",
      "align": "center",
      "verticalAlign": "middle",
      "style": { "textOutline": "none" }
    },
    "point": { "events": { "click": ["triggerClick", { "rowIndex": "point.index" }] } }
  }]
}
```

**Sample Data:**
```csv
ButtonLabel,Icon
ALL,📊
Sales,💰
Marketing,📢
Engineering,⚙️
Support,🎧
```

Note: `SelectedValue` column uses the calc field `${FilterValue}`.

---

## Example 4: Gradient Accent Buttons

Modern buttons with gradient backgrounds and shadow effects.

**Best for:** Hero dashboards, executive views, high-visibility filters

**Kiro prompt:** *"Create premium gradient buttons with purple gradient when selected, subtle shadows, for year filtering"*

```json
{
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 60,
    "spacing": [8, 15, 8, 15],
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
    "name": "GradientButtons",
    "data": [
      "map",
      ["getColumn", 0, 1],
      {
        "x": ["+", 10, ["*", ["itemIndex"], 22]],
        "y": 50,
        "label": ["get", ["item"], 0],
        "bgGradient": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%)"],
        "textColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "#ffffff", "#4a5568"],
        "shadow": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "0 4px 15px rgba(102, 126, 234, 0.4)", "0 2px 8px rgba(0,0,0,0.08)"]
      }
    ],
    "dataLabels": {
      "enabled": true,
      "useHTML": true,
      "format": "<div style='background:{point.bgGradient};color:{point.textColor};padding:12px 20px;border-radius:10px;cursor:pointer;font-weight:600;font-size:13px;box-shadow:{point.shadow};min-width:70px;text-align:center;'>{point.label}</div>",
      "align": "center",
      "verticalAlign": "middle",
      "style": { "textOutline": "none" }
    },
    "point": { "events": { "click": ["triggerClick", { "rowIndex": "point.index" }] } }
  }]
}
```

**Sample Data:**
```csv
ButtonLabel
ALL
2024
2025
2026
```

---

## Using Kiro Effectively

### The Steering Document

The [companion GitHub repo](https://github.com/YOUR_USERNAME/quicksight-highcharts-buttons) includes `quicksight-filter-buttons.md`, a steering document purpose-built for this pattern. It covers:

1. **Architecture overview** – Components and their relationships
2. **Base JSON pattern** – The template structure with placeholder tokens
3. **Style templates** – Four pre-defined looks with CSS
4. **Spacing guidelines** – How to calculate X positions for different button counts
5. **Field wells configuration** – Column order and types
6. **Troubleshooting** – Common issues and fixes

Drop it into `.kiro/steering/` and Kiro picks it up automatically—no configuration needed.

### Example Kiro Conversations

**Creating new buttons:**
> "Create filter buttons for status filtering with options: ALL, Draft, Review, Approved, Published. Use the pill style with orange as the selected color."

**Modifying existing buttons:**
> "Update the button spacing to fit 8 buttons instead of 5"

**Troubleshooting:**
> "My buttons aren't highlighting when clicked. The parameter updates but the colors don't change."

Kiro will identify that the `SelectedValue` calc field might be missing or the column order in field wells is incorrect.

**Custom styling:**
> "Create buttons that match our brand colors: selected=#1a365d, unselected=#edf2f7, with 4px border radius"

### Best Practices with Kiro

1. **Start with the steering doc** – Add it to `.kiro/steering/` before asking for buttons
2. **Be specific about options** – List all button labels you need
3. **Reference existing styles** – "Use the gradient style but with blue colors"
4. **Ask for the full setup** – "Include the CSV data and calc field formulas"
5. **Iterate incrementally** – Make one change at a time for best results

---

## Performance Best Practices

1. **Disable animations** – Set `animation: false` on chart and series
2. **Use SPICE** – Store button dataset in SPICE for fast queries
3. **Keep dataset small** – 10-20 rows maximum for button data
4. **Calculate colors in data mapping** – Avoid `pointRender` when possible
5. **Single series** – All buttons in one series, not separate series per button

## Common Customizations

### Adjusting Button Spacing

Modify the X-coordinate multiplier:
```json
"x": ["+", 8, ["*", ["itemIndex"], 18]]
```
- Increase `18` for wider spacing
- Decrease for tighter spacing
- Adjust starting offset `8` to shift all buttons left/right

### Changing Colors

Update the `bgColor`, `textColor`, and `borderColor` case statements:
```json
"bgColor": ["case", ["==", ["get", ["item"], 0], ["get", ["item"], 1]], "#YOUR_SELECTED_COLOR", "#YOUR_UNSELECTED_COLOR"]
```

### Adding More Buttons

Simply add rows to your CSV—the `map` function automatically creates buttons for each row.

## Conclusion

This pattern provides a robust, performant way to add interactive filter buttons to your QuickSight dashboards. Combined with Kiro's AI assistance, you can rapidly create and customize button widgets without memorizing the QuickSight expression syntax.

The steering document approach means Kiro understands your specific requirements—just describe what you want, and it generates correct, working configurations. This dramatically reduces the time from idea to implementation.

## Resources

- [Kiro IDE](https://kiro.dev) – AI-powered development environment
- [Companion GitHub Repo](https://github.com/YOUR_USERNAME/quicksight-highcharts-buttons) – Steering doc, example configs, sample data, and HTML test page
- [QuickSight Highcharts Documentation](https://docs.aws.amazon.com/quicksight/latest/user/highchart.html)
- [Highcharts 11.4.6 API Reference](https://api.highcharts.com/highcharts/)
- [Kiro Steering Docs](https://kiro.dev/docs/steering/) – Learn more about steering documents

---

*This post demonstrates how AI-assisted development with Kiro can accelerate QuickSight dashboard customization. The steering document pattern works for any complex configuration task—teach Kiro once, benefit repeatedly.*
