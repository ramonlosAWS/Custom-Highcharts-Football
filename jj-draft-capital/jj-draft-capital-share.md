# JJ Draft Capital Rank Widget

A compact mini-widget that displays a team's JJ Draft Capital ranking as a centered badge. Designed to sit alongside other KPI widgets on a team profile page.

## Preview

```
    JJ DRAFT CAPITAL
        #12
```

- Gray pill badge with rank number
- 55px height, transparent background
- Single-row extraction — requires a team filter

## Data Requirements

| Column | Type | Example | Field Well |
|--------|------|---------|------------|
| JJ Draft Capital Rank | INTEGER | `12` | GROUP BY col 0 |

A `Team Abbr` filter must be applied so the visual shows one team at a time.

## QuickSight Setup

1. Add a Highcharts visual to your sheet
2. Paste the contents of `quicksight-jj-draft-capital.json` into the Chart code editor
3. Field Wells → GROUP BY:
   - Column 0: `JJ Draft Capital Rank` (NumericalDimensionField)
4. Add a filter control on `Team Abbr` linked to this visual
5. Click APPLY CODE

## Configuration

The full Highcharts JSON is in [`quicksight-jj-draft-capital.json`](quicksight-jj-draft-capital.json).

<details>
<summary>Expand JSON</summary>

```json
{
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 55,
    "spacing": [0, 0, 0, 0],
    "style": {
      "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    }
  },
  "title": { "text": null },
  "legend": { "enabled": false },
  "credits": { "enabled": false },
  "xAxis": { "min": 0, "max": 100, "visible": false },
  "yAxis": { "min": 0, "max": 100, "visible": false },
  "tooltip": { "enabled": false },
  "plotOptions": {
    "scatter": {
      "marker": { "enabled": false },
      "enableMouseTracking": false
    }
  },
  "series": [{
    "type": "scatter",
    "name": "JJCapitalRank",
    "data": [{
      "x": 50,
      "y": 50,
      "rank": ["get", ["getColumn", 0], 0]
    }],
    "dataLabels": {
      "enabled": true,
      "useHTML": true,
      "format": "<div style='display:flex;flex-direction:column;align-items:center;gap:3px;'><div style='font-size:9px;color:#888;font-weight:600;letter-spacing:0.5px;'>JJ DRAFT CAPITAL</div><div style='background:#e8e8e8;color:#555;border-radius:6px;padding:4px 0;width:48px;text-align:center;font-size:16px;font-weight:700;'>#{point.rank}</div></div>",
      "align": "center",
      "verticalAlign": "middle",
      "style": { "textOutline": "none" },
      "overflow": "allow",
      "crop": false
    }
  }]
}
```

</details>

## Local Testing

Open `test-jj-draft-capital.html` in a browser. Requires `highcharts.js` in the project root (not committed — download Highcharts 11.4.6 locally).

## Files

| File | Purpose |
|------|---------|
| `quicksight-jj-draft-capital.json` | Highcharts config (paste into QuickSight) |
| `test-jj-draft-capital.html` | Local browser test |
