# Cap Metrics Visual (v2)

3-row cap space metric cards with rank badges and progress bars. Designed for 185px height.

## Field Wells

3 columns in GROUP BY + 3 columns in VALUE:

**GROUP BY:**

| Index | Column | Type | Used For |
|-------|--------|------|----------|
| 0 | Cap Space Rank | INTEGER | Row 1 rank badge |
| 1 | Active Cap Spending Rank | INTEGER | Row 2 rank badge |
| 2 | Dead Money Rank | INTEGER | Row 3 rank badge |

**VALUE (formatted as Currency):**

| Index | Column | Type | Used For |
|-------|--------|------|----------|
| 0 | Cap Space | INTEGER | Row 1 value (handles negative) |
| 1 | Active Cap Spending | INTEGER | Row 2 value |
| 2 | Dead Money | INTEGER | Row 3 value |

## Filter

Add a filter control on Team Abbr (or any unique identifier) to display one team at a time. This is a single-row extraction visual — without a filter, only the first row's data displays.

## Rows

| Row | Metric | Color | Notes |
|-----|--------|-------|-------|
| 1 | Cap Space | Green/Red (conditional) | Most important — listed first. Red `#dc3545` when negative. |
| 2 | Active Cap Spending | Green `#10b981` | |
| 3 | Dead Money | Gray `#9ca3af` | Gray text `#6b7280` to convey "dead" visually. |

## Progress Bars

Bars represent rank position out of 32 NFL teams, not dollar amounts.

**Formula:** `((33 - rank) / 32) * 100%`

| Rank | Bar Fill | Position |
|------|----------|----------|
| 1 (best) | ~100% | Full bar (right edge) |
| 16 (mid) | ~53% | Half bar |
| 32 (worst) | ~3% | Nearly empty (left edge) |

## Changelog

### v3
- Progress bars now rank-based instead of value-based — bar width shows position out of 32 teams (rank 1 = full, rank 32 = empty)
- Removed per-metric bar divisors (were 1,050,000 / 3,600,000 / 760,000) — all bars now use the same rank formula

### v2
- Reordered rows: Cap Space → Active Cap Spending → Dead Money (cap space is the headline metric)
- Tighter vertical spacing: Y positions 10/40/70 (was 10/42/74), chart height 185px (was 220px), row padding 2px (was 4px)
- Dead Money color changed from amber `#f59e0b` to gray `#9ca3af` — better semantic fit

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
        "barPct": ["+", ["/", ["*", ["-", 33, ["get", ["getColumnFromGroupBy", 2], 0]], 100], 32], "%"],
        "barColor": "#9ca3af",
        "textColor": "#6b7280"
      }],
      "dataLabels": {
        "enabled": true,
        "useHTML": true,
        "format": "<div style='display:flex;align-items:center;gap:6px;padding:2px 0;'><div style='width:4px;height:34px;background:#9ca3af;border-radius:2px;flex-shrink:0;'></div><div><div style='font-size:9px;color:#888;font-weight:600;letter-spacing:0.5px;'>{point.metricLabel}</div><div style='display:flex;align-items:center;gap:6px;'><div style='font-size:13px;font-weight:700;color:{point.textColor};white-space:nowrap;width:140px;flex-shrink:0;'>${point.millions:.1f}M</div><div style='background:#e8e8e8;color:#555;border-radius:6px;padding:2px 0;width:40px;text-align:center;font-size:12px;font-weight:700;flex-shrink:0;'>#{point.rank}</div><div style='width:120px;background:#e5e7eb;border-radius:3px;height:12px;flex-shrink:0;'><div style='width:{point.barPct};max-width:100%;background:#9ca3af;height:12px;border-radius:3px;'></div></div></div></div></div>",
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
