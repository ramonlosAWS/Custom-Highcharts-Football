# Cap Metrics Visual (v2 — Tier Badge)

3-row cap space metric cards. Cap Space and Active Spending use rank bars. Dead Money uses a tier badge instead of a bar to avoid visual confusion (lower rank = less dead money = good, but a full bar would imply "lots of dead money").

Designed for 185px height.

## What Changed from v1

- Dead Money row: progress bar replaced with a color-coded tier pill (MINIMAL / LOW / MODERATE / BURDENED)
- Dead Money rank badge is now color-coded (green for low ranks, red for high)
- Cap Space and Active Spending rows unchanged

## Dead Money Ranking

Rank 1 = least dead money (best), Rank 32 = most dead money (worst).

| Rank Range | Tier | Badge Color | Pill Color |
|------------|------|-------------|------------|
| 1–8 | MINIMAL | Green `#dcfce7` | Green `#16a34a` |
| 9–16 | LOW | Green `#dcfce7` | Green `#059669` |
| 17–24 | MODERATE | Amber `#fef9c3` | Amber `#a16207` |
| 25–32 | BURDENED | Red `#fef2f2` | Red `#dc2626` |

## Config

`quicksight-cap-metrics-v2.json`

## Field Wells

Same as v1 — 3 columns in GROUP BY + 3 columns in VALUE:

**GROUP BY:**

| Index | Column | Type | Used For |
|-------|--------|------|----------|
| 0 | Cap Space Rank | INTEGER | Row 1 rank badge + bar |
| 1 | Active Cap Spending Rank | INTEGER | Row 2 rank badge + bar |
| 2 | Dead Money Rank | INTEGER | Row 3 rank badge + tier pill |

**VALUE (formatted as Currency):**

| Index | Column | Type | Used For |
|-------|--------|------|----------|
| 0 | Cap Space | INTEGER | Row 1 value (handles negative) |
| 1 | Active Cap Spending | INTEGER | Row 2 value |
| 2 | Dead Money | INTEGER | Row 3 value |

## Filter

Add a filter control on Team Abbr (or any unique identifier) to display one team at a time.

## Rows

| Row | Metric | Visual | Color |
|-----|--------|--------|-------|
| 1 | Cap Space | Rank bar | Green/Red (conditional on positive/negative) |
| 2 | Active Cap Spending | Rank bar | Green `#10b981` |
| 3 | Dead Money | Tier pill | Gray accent `#9ca3af`, pill color varies by tier |

## Progress Bars (Rows 1 & 2)

Bars represent rank position out of 32 NFL teams.

**Formula:** `((33 - rank) / 32) * 100%`

| Rank | Bar Fill |
|------|----------|
| 1 (best) | ~100% |
| 16 (mid) | ~53% |
| 32 (worst) | ~3% |

## Working Files

- `working/test-cap-metrics-v2.html` — Local test page with all design alternatives
- `working/highcharts.js` — Local Highcharts 11.4.6

## Highcharts JSON (paste into QuickSight Chart Code editor)

```json
{
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 185,
    "spacing": [5, 0, 5, 0],
    "style": {
      "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    }
  },
  "title": { "text": null },
  "legend": { "enabled": false },
  "credits": { "enabled": false },
  "xAxis": { "min": 0, "max": 100, "visible": false },
  "yAxis": { "min": 0, "max": 100, "visible": false, "reversed": true },
  "tooltip": { "enabled": false },
  "plotOptions": {
    "scatter": {
      "marker": { "enabled": false },
      "enableMouseTracking": false
    }
  },
  "series": [
    {
      "type": "scatter",
      "name": "CapSpace",
      "data": [{
        "x": 3,
        "y": 10,
        "metricLabel": "CAP SPACE",
        "millions": ["/", ["get", ["getColumnFromValue", 0], 0], 1000000],
        "rank": ["get", ["getColumnFromGroupBy", 0], 0],
        "barPct": ["+", ["/", ["*", ["-", 33, ["get", ["getColumnFromGroupBy", 0], 0]], 100], 32], "%"],
        "barColor": ["case", [">=", ["get", ["getColumnFromValue", 0], 0], 0], "#10b981", "#dc3545"],
        "textColor": ["case", [">=", ["get", ["getColumnFromValue", 0], 0], 0], "#333", "#dc3545"],
        "badgeColor": ["case", [">=", ["get", ["getColumnFromValue", 0], 0], 0], "#10b981", "#dc3545"]
      }],
      "dataLabels": {
        "enabled": true,
        "useHTML": true,
        "format": "<div style='display:flex;align-items:center;gap:6px;padding:2px 0;'><div style='width:4px;height:34px;background:{point.barColor};border-radius:2px;flex-shrink:0;'></div><div><div style='font-size:9px;color:#888;font-weight:600;letter-spacing:0.5px;'>{point.metricLabel}</div><div style='display:flex;align-items:center;gap:6px;'><div style='font-size:13px;font-weight:700;color:{point.textColor};white-space:nowrap;width:140px;flex-shrink:0;'>${point.millions:.1f}M</div><div style='background:#e8e8e8;color:#555;border-radius:6px;padding:2px 0;width:40px;text-align:center;font-size:12px;font-weight:700;flex-shrink:0;'>#{point.rank}</div><div style='width:120px;background:#e5e7eb;border-radius:3px;height:12px;flex-shrink:0;'><div style='width:{point.barPct};max-width:100%;background:{point.barColor};height:12px;border-radius:3px;'></div></div></div></div></div>",
        "align": "left",
        "verticalAlign": "middle",
        "style": { "textOutline": "none" },
        "overflow": "allow",
        "crop": false
      }
    },
    {
      "type": "scatter",
      "name": "ActiveCap",
      "data": [{
        "x": 3,
        "y": 40,
        "metricLabel": "ACTIVE CAP SPENDING",
        "millions": ["/", ["get", ["getColumnFromValue", 1], 0], 1000000],
        "rank": ["get", ["getColumnFromGroupBy", 1], 0],
        "barPct": ["+", ["/", ["*", ["-", 33, ["get", ["getColumnFromGroupBy", 1], 0]], 100], 32], "%"],
        "barColor": "#10b981",
        "textColor": "#333"
      }],
      "dataLabels": {
        "enabled": true,
        "useHTML": true,
        "format": "<div style='display:flex;align-items:center;gap:6px;padding:2px 0;'><div style='width:4px;height:34px;background:#10b981;border-radius:2px;flex-shrink:0;'></div><div><div style='font-size:9px;color:#888;font-weight:600;letter-spacing:0.5px;'>{point.metricLabel}</div><div style='display:flex;align-items:center;gap:6px;'><div style='font-size:13px;font-weight:700;color:{point.textColor};white-space:nowrap;width:140px;flex-shrink:0;'>${point.millions:.1f}M</div><div style='background:#e8e8e8;color:#555;border-radius:6px;padding:2px 0;width:40px;text-align:center;font-size:12px;font-weight:700;flex-shrink:0;'>#{point.rank}</div><div style='width:120px;background:#e5e7eb;border-radius:3px;height:12px;flex-shrink:0;'><div style='width:{point.barPct};max-width:100%;background:#10b981;height:12px;border-radius:3px;'></div></div></div></div></div>",
        "align": "left",
        "verticalAlign": "middle",
        "style": { "textOutline": "none" },
        "overflow": "allow",
        "crop": false
      }
    },
    {
      "type": "scatter",
      "name": "DeadMoney",
      "data": [{
        "x": 3,
        "y": 70,
        "metricLabel": "DEAD MONEY",
        "millions": ["/", ["get", ["getColumnFromValue", 2], 0], 1000000],
        "rank": ["get", ["getColumnFromGroupBy", 2], 0],
        "tierText": ["case",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 8], "MINIMAL",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 16], "LOW",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 24], "MODERATE",
          "BURDENED"
        ],
        "tierBg": ["case",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 8], "#dcfce7",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 16], "#ecfdf5",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 24], "#fef9c3",
          "#fef2f2"
        ],
        "tierColor": ["case",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 8], "#16a34a",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 16], "#059669",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 24], "#a16207",
          "#dc2626"
        ],
        "badgeBg": ["case",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 16], "#dcfce7",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 24], "#fef9c3",
          "#fef2f2"
        ],
        "badgeColor": ["case",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 16], "#16a34a",
          ["<=", ["get", ["getColumnFromGroupBy", 2], 0], 24], "#a16207",
          "#dc2626"
        ]
      }],
      "dataLabels": {
        "enabled": true,
        "useHTML": true,
        "format": "<div style='display:flex;align-items:center;gap:6px;padding:2px 0;'><div style='width:4px;height:34px;background:#9ca3af;border-radius:2px;flex-shrink:0;'></div><div><div style='font-size:9px;color:#888;font-weight:600;letter-spacing:0.5px;'>{point.metricLabel}</div><div style='display:flex;align-items:center;gap:6px;'><div style='font-size:13px;font-weight:700;color:#6b7280;white-space:nowrap;width:140px;flex-shrink:0;'>${point.millions:.1f}M</div><div style='background:{point.badgeBg};color:{point.badgeColor};border-radius:6px;padding:2px 0;width:40px;text-align:center;font-size:12px;font-weight:700;flex-shrink:0;'>#{point.rank}</div><div style='background:{point.tierBg};color:{point.tierColor};font-size:9px;font-weight:700;padding:3px 10px;border-radius:10px;letter-spacing:0.3px;'>{point.tierText}</div></div></div></div>",
        "align": "left",
        "verticalAlign": "middle",
        "style": { "textOutline": "none" },
        "overflow": "allow",
        "crop": false
      }
    }
  ]
}
```
