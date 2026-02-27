# Team Needs Widget

Compact sidebar widget showing a team's top 5 positional needs with a team-color accent bar. Designed for single-team filtered views (e.g., team profile pages).

Transparent background — blends with any QuickSight theme or sheet color.

## Visual Design

- 350px wide, 240px tall
- 4px left border in team primary color
- "TOP 5 TEAM NEEDS" header (14px bold)
- "ENTERING FREE AGENCY" subheader (11px uppercase, muted)
- Needs list displayed large (32px bold) for quick scanning

## Data Structure

### CSV Format

```csv
UniqueID,TeamAbbr,TeamColor,TeamNeeds
1,KC,#E31837,"DL, OL, EDGE, S, WR"
2,ATL,#A71930,"EDGE, DL, CB, OL, S"
```

Full 32-team dataset included in `team-needs-data.csv`.

Columns 4–7 (GMName, HCName, OCName, DCName) are also in the CSV for future use but not referenced by this visual.

## Field Wells

**GROUP BY:**

| Index | Column | Type | Used For |
|-------|--------|------|----------|
| 0 | UniqueID | INTEGER | Unique row identifier |
| 1 | TeamAbbr | STRING | Team filter target |
| 2 | TeamColor | STRING | Left accent bar color |
| 3 | TeamNeeds | STRING | Displayed needs text |

**VALUE:** (empty)

## Filter

Add a filter control on `TeamAbbr` to display one team at a time. Without a filter, only the first row's data shows (single-row extraction pattern).

## QuickSight Setup

1. Upload `team-needs-data.csv` to S3 and create a QuickSight dataset
2. Add a Highcharts visual to your sheet
3. Set field wells: GROUP BY → UniqueID, TeamAbbr, TeamColor, TeamNeeds
4. Paste the JSON below into the Chart Code editor
5. Add a `TeamAbbr` filter control (or link to an existing one)

## Highcharts JSON (paste into QuickSight Chart Code editor)

```json
{
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 240,
    "spacing": [5, 5, 5, 5]
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
  "series": [
    {
      "name": "FourColumns",
      "data": [{
        "x": 50,
        "y": 50,
        "teamColor": ["get", ["getColumn", 2], 0],
        "teamNeeds": ["get", ["getColumn", 3], 0]
      }],
      "dataLabels": {
        "enabled": true,
        "useHTML": true,
        "format": "<div style='width:350px;padding:15px 10px 15px 15px;border-left:4px solid {point.teamColor};background:transparent;'><div style='font-size:14px;font-weight:700;color:#333;margin-bottom:5px;'>TOP 5 TEAM NEEDS</div><div style='font-size:11px;color:#999;text-transform:uppercase;margin-bottom:18px;'>ENTERING FREE AGENCY</div><div style='font-size:32px;font-weight:700;color:#333;line-height:1.3;'>{point.teamNeeds}</div></div>",
        "align": "center",
        "verticalAlign": "middle"
      }
    }
  ]
}
```

## Customization

**Width:** Change `width:350px` in the format string. Works well at 300–450px.

**Needs font size:** Currently `32px`. Use `24px` for longer need lists or `16px` for compact layouts.

**Add background:** Replace `background:transparent` with `background:#f8f8f8` for a light card look, or use `background:{point.teamColor}10` for a subtle team-tinted card (hex + `10` = ~6% opacity).

**Spacing:** Adjust `margin-bottom:18px` on the subheader to tighten or loosen the gap before the needs text.

## Integration

Designed as a sidebar element alongside team header, roster table, or depth chart visuals. The 350px width fits a sidebar layout with main content at 900–1000px.

## Working Files

- `quicksight-team-needs.json` — Config file (same JSON as above)
- `test-team-needs.html` — Local test page (Highcharts 11.4.6)
- `team-needs-data.csv` — Full 32-team dataset
- `prepare-team-needs-data.py` — Data preparation script