# Updated Filter Button Configs (Feb 2026)

Fixed spacing, reduced padding, adjusted X positions and div widths for all 3 filter button bars.

---

## 1. FA Board Filter (4 buttons)

**Buttons:** STREET FA | STAFF CONNECTIONS | OUTGOING | CTR LIST
**Parameter:** `FABoardFilter` (String, default `STREET FA`)
**Widget width:** ~780px → div width 195px
**X positions:** 12.5, 37.5, 62.5, 87.5

```json
{
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 32,
    "spacing": [0, 0, 0, 0],
    "animation": false,
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
    "scatter": { "marker": { "enabled": false, "radius": 0 }, "animation": false, "states": { "hover": { "enabled": false }, "select": { "enabled": false }, "inactive": { "enabled": false } } },
    "series": { "enableMouseTracking": true, "cursor": "pointer", "animation": false, "marker": { "enabled": false, "radius": 0, "states": { "hover": { "enabled": false, "radius": 0 }, "select": { "enabled": false, "radius": 0 } } } }
  },
  "series": [{
    "name": "FABoardFilter",
    "data": [
      "map",
      ["getColumn", 1, 2],
      {
        "x": ["+", 12.5, ["*", ["itemIndex"], 25]],
        "y": 50,
        "label": ["get", ["item"], 0],
        "bg": [
          "case",
          ["==", ["get", ["item"], 0], ["get", ["item"], 1]],
          "#1a2b4c",
          "transparent"
        ],
        "tc": [
          "case",
          ["==", ["get", ["item"], 0], ["get", ["item"], 1]],
          "#ffffff",
          "#1a2b4c"
        ],
        "fw": "600",
        "div": [
          "case",
          ["==", ["itemIndex"], 3], "none",
          "1px solid #c0c8d1"
        ]
      }
    ],
    "dataLabels": {
      "enabled": true,
      "useHTML": true,
      "format": "<div style='width:195px;height:31px;line-height:31px;text-align:center;font-size:14px;font-weight:{point.fw};color:{point.tc};background:{point.bg};border-right:{point.div};cursor:pointer;box-sizing:border-box;white-space:nowrap;'>{point.label}</div>",
      "align": "center",
      "verticalAlign": "middle",
      "overflow": "allow",
      "crop": false,
      "style": { "textOutline": "none" }
    },
    "point": { "events": { "click": ["triggerClick", { "rowIndex": "point.index" }] } }
  }]
}
```

---

## 2. Team Draft View Selector (2 buttons)

**Buttons:** MOCK DRAFT TRACKER | DJ'S TOP 50
**Parameter:** `TeamDraftView` (String, default `MOCK DRAFT TRACKER`)
**Div width:** 180px
**X positions:** 38, 62

```json
{
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 32,
    "spacing": [0, 0, 0, 0],
    "animation": false,
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
    "scatter": { "marker": { "enabled": false, "radius": 0 }, "animation": false, "states": { "hover": { "enabled": false }, "select": { "enabled": false }, "inactive": { "enabled": false } } },
    "series": { "enableMouseTracking": true, "cursor": "pointer", "animation": false, "marker": { "enabled": false, "radius": 0, "states": { "hover": { "enabled": false, "radius": 0 }, "select": { "enabled": false, "radius": 0 } } } }
  },
  "series": [{
    "name": "TeamDraftView",
    "data": [
      "map",
      ["getColumn", 1, 2],
      {
        "x": ["+", 38, ["*", ["itemIndex"], 24]],
        "y": 50,
        "label": ["get", ["item"], 0],
        "bg": [
          "case",
          ["==", ["get", ["item"], 0], ["get", ["item"], 1]],
          "#1a2b4c",
          "transparent"
        ],
        "tc": [
          "case",
          ["==", ["get", ["item"], 0], ["get", ["item"], 1]],
          "#ffffff",
          "#1a2b4c"
        ],
        "fw": "600",
        "div": [
          "case",
          ["==", ["itemIndex"], 1], "none",
          "1px solid #c0c8d1"
        ]
      }
    ],
    "dataLabels": {
      "enabled": true,
      "useHTML": true,
      "format": "<div style='width:180px;height:31px;line-height:31px;text-align:center;font-size:14px;font-weight:{point.fw};color:{point.tc};background:{point.bg};border-right:{point.div};cursor:pointer;box-sizing:border-box;white-space:nowrap;'>{point.label}</div>",
      "align": "center",
      "verticalAlign": "middle",
      "overflow": "allow",
      "crop": false,
      "style": { "textOutline": "none" }
    },
    "point": { "events": { "click": ["triggerClick", { "rowIndex": "point.index" }] } }
  }]
}
```

---

## 3. Team Strip Selector (2 buttons)

**Buttons:** OFFSEASON PREVIEW | TEAM NEEDS
**Parameter:** `TeamStripSelector` (String, default `OFFSEASON PREVIEW`)
**Div width:** 180px
**X positions:** 38, 62

```json
{
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 32,
    "spacing": [0, 0, 0, 0],
    "animation": false,
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
    "scatter": { "marker": { "enabled": false, "radius": 0 }, "animation": false, "states": { "hover": { "enabled": false }, "select": { "enabled": false }, "inactive": { "enabled": false } } },
    "series": { "enableMouseTracking": true, "cursor": "pointer", "animation": false, "marker": { "enabled": false, "radius": 0, "states": { "hover": { "enabled": false, "radius": 0 }, "select": { "enabled": false, "radius": 0 } } } }
  },
  "series": [{
    "name": "TeamStripSelector",
    "data": [
      "map",
      ["getColumn", 1, 2],
      {
        "x": ["+", 38, ["*", ["itemIndex"], 24]],
        "y": 50,
        "label": ["get", ["item"], 0],
        "bg": [
          "case",
          ["==", ["get", ["item"], 0], ["get", ["item"], 1]],
          "#1a2b4c",
          "transparent"
        ],
        "tc": [
          "case",
          ["==", ["get", ["item"], 0], ["get", ["item"], 1]],
          "#ffffff",
          "#1a2b4c"
        ],
        "fw": "600",
        "div": [
          "case",
          ["==", ["itemIndex"], 1], "none",
          "1px solid #c0c8d1"
        ]
      }
    ],
    "dataLabels": {
      "enabled": true,
      "useHTML": true,
      "format": "<div style='width:180px;height:31px;line-height:31px;text-align:center;font-size:14px;font-weight:{point.fw};color:{point.tc};background:{point.bg};border-right:{point.div};cursor:pointer;box-sizing:border-box;white-space:nowrap;'>{point.label}</div>",
      "align": "center",
      "verticalAlign": "middle",
      "overflow": "allow",
      "crop": false,
      "style": { "textOutline": "none" }
    },
    "point": { "events": { "click": ["triggerClick", { "rowIndex": "point.index" }] } }
  }]
}
```

---

## Tuning Guide

If buttons don't align perfectly, adjust the div `width` value:
- **Formula:** `divWidth = widgetPixelWidth / numberOfButtons`
- FA Board Filter (4 buttons): `widgetWidth / 4`
- Team Draft View & Team Strip (2 buttons): `widgetWidth / 2`

If buttons are too spread out or too bunched, adjust X positions:
- 4 buttons: startX = 12.5, step = 25
- 2 buttons centered: startX = 38, step = 24
- 2 buttons full-width: startX = 25, step = 50
