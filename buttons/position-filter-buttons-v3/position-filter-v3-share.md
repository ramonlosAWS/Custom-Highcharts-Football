# Position Filter Buttons v3 — With OFF/DEF Groups

Adds OFF and DEF group buttons between All and the individual positions.

## Buttons (15)
All | OFF | DEF | QB | RB | WR | TE | T | G | C | DT | ED | LB | CB | S

## Changes from v2
- 2 new buttons — OFF and DEF inserted after All
- 3-tier filter logic — All (everything), OFF/DEF (group via `offdef` column), individual position
- Updated position labels — T, G, C, S (instead of OT, OG, OC, DS)
- Button div shrunk to 42px — fits 15 buttons in ~800px widget
- Spacing recalculated — startX 16.15, step 4.55 units

---

## Button Dataset CSV

```csv
SortOrder,ButtonLabel
1,All
2,OFF
3,DEF
4,QB
5,RB
6,WR
7,TE
8,T
9,G
10,C
11,DT
12,ED
13,LB
14,CB
15,S
```

---

## Highcharts Config (QuickSight)

```json
{
  "_comment": "Position Filter v3 - 15 buttons: All, OFF, DEF, QB, RB, WR, TE, T, G, C, DT, ED, LB, CB, S. Chart ~800px widget. Button div 42px, spacing 4.55 units, startX 16.15. Parameter: PositionFilter (String, default All). Dataset: position-filter-data-v3.csv + calc field SelectedPosition = ${PositionFilter}. Field Wells GROUP BY: SortOrder (col 0, sort asc), ButtonLabel (col 1), SelectedPosition (col 2). Nav Action: on select, set PositionFilter = ButtonLabel. Target calc field: ShowByPosition = ifelse(${PositionFilter}='All', 1, ifelse(${PositionFilter}='OFF' AND {offdef}='OFF', 1, ifelse(${PositionFilter}='DEF' AND {offdef}='DEF', 1, ifelse({Position}=${PositionFilter}, 1, 0))))",
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 30,
    "spacing": [5, 0, 5, 0],
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
    "name": "PositionFilter",
    "data": [
      "map",
      ["getColumn", 1, 2],
      {
        "x": ["+", 16.15, ["*", ["itemIndex"], 4.55]],
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
          ["==", ["itemIndex"], 14], "none",
          "1px solid #c0c8d1"
        ]
      }
    ],
    "dataLabels": {
      "enabled": true,
      "useHTML": true,
      "format": "<div style='width:42px;height:20px;line-height:20px;text-align:center;font-size:11px;font-weight:{point.fw};color:{point.tc};background:{point.bg};border-right:{point.div};cursor:pointer;box-sizing:border-box;'>{point.label}</div>",
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

## QuickSight Setup

### Parameter
- Name: `PositionFilter`, Type: String, Default: `All`

### Button Dataset
Upload CSV above to SPICE, add calculated field:
```
Name: SelectedPosition
Expression: ${PositionFilter}
```

### Field Wells (GROUP BY)
1. `SortOrder` (col 0) — sort ascending
2. `ButtonLabel` (col 1)
3. `SelectedPosition` (col 2)

### Navigation Action
- Activation: Select
- Action: Set parameter `PositionFilter` = field `ButtonLabel`

---

## Target Dataset — Calc Field (CRITICAL)

The target dataset must have an `offdef` column with values `OFF` or `DEF` for each row.

```
Name: ShowByPosition
Expression: ifelse(
  ${PositionFilter}='All', 1,
  ifelse(${PositionFilter}='OFF' AND {offdef}='OFF', 1,
    ifelse(${PositionFilter}='DEF' AND {offdef}='DEF', 1,
      ifelse({Position}=${PositionFilter}, 1, 0)
    )
  )
)
```

Filter target visuals: `ShowByPosition = 1`

### How the filter logic works

| Button clicked | Parameter value | Rows shown |
|----------------|-----------------|------------|
| All | `All` | All rows (first condition) |
| OFF | `OFF` | Rows where `offdef = 'OFF'` |
| DEF | `DEF` | Rows where `offdef = 'DEF'` |
| QB | `QB` | Rows where `Position = 'QB'` |
| T | `T` | Rows where `Position = 'T'` |
| ... | ... | ... |

---

## Spacing Math

```
Chart width:        800px
Chart spacing:      [5, 0, 5, 0] → plot area = 800px
1 xAxis unit:       800 / 100 = 8px
Button CSS width:   42px = 5.25 xAxis units
Center spacing:     4.55 units
Start X:            16.15
Last X:             16.15 + 14 × 4.55 = 79.85
Total button span:  15 × 42px = 630px
```

## Visual Size
- Widget width: ~800px
- Chart height: 30px
- Button width: 42px each (630px total for 15 buttons)
