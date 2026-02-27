# Draft Picks Widget

Displays a team's draft picks for the current year (2026) and next year (2027) in a compact two-row layout with colored accent bars.

## Preview

```
 ▌ 2026 DRAFT PICKS
 ▌ 1.8, 2.40, 3.72, 4.104, 5.136, 6.168, 7.200

 ▌ 2027 DRAFT PICKS
 ▌ Rd 1, Rd 2, Rd 3, Rd 4, Rd 5, Rd 6, Rd 7
```

- Blue accent bar for current year, purple for next year
- 130px height, transparent background
- Single-row extraction — requires a team filter

## Data Requirements

| Column | Type | Example | Field Well |
|--------|------|---------|------------|
| Current Year Draft Picks | STRING | `1.8, 2.40, 3.72, 4.104, 5.136, 6.168, 7.200` | GROUP BY col 0 |
| Next Year Draft Picks | STRING | `Rd 1, Rd 2, Rd 3, Rd 4, Rd 5, Rd 6, Rd 7` | GROUP BY col 1 |

A `Team Abbr` filter must be applied so the visual shows one team at a time.

## QuickSight Setup

1. Add a Highcharts visual to your sheet
2. Paste the contents of `quicksight-draft-picks.json` into the Chart code editor
3. Field Wells → GROUP BY:
   - Column 0: `Current Year Draft Picks`
   - Column 1: `Next Year Draft Picks`
4. Add a filter control on `Team Abbr` linked to this visual
5. Click APPLY CODE

## Configuration

The full Highcharts JSON is in [`quicksight-draft-picks.json`](quicksight-draft-picks.json).

<details>
<summary>Expand JSON</summary>

```json
{
  "chart": {
    "type": "scatter",
    "backgroundColor": "transparent",
    "height": 130,
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
      "name": "2026Picks",
      "data": [{
        "x": 3,
        "y": 15,
        "picks": ["get", ["getColumn", 0], 0]
      }],
      "dataLabels": {
        "enabled": true,
        "useHTML": true,
        "format": "<div style='display:flex;align-items:center;gap:6px;padding:2px 0;'><div style='width:4px;height:34px;background:#3b82f6;border-radius:2px;flex-shrink:0;'></div><div><div style='font-size:9px;color:#888;font-weight:600;letter-spacing:0.5px;'>2026 DRAFT PICKS</div><div style='font-size:13px;font-weight:700;color:#333;line-height:1.5;white-space:nowrap;'>{point.picks}</div></div></div>",
        "align": "left",
        "verticalAlign": "middle",
        "style": { "textOutline": "none" },
        "overflow": "allow",
        "crop": false
      }
    },
    {
      "type": "scatter",
      "name": "2027Picks",
      "data": [{
        "x": 3,
        "y": 65,
        "picks": ["get", ["getColumn", 1], 0]
      }],
      "dataLabels": {
        "enabled": true,
        "useHTML": true,
        "format": "<div style='display:flex;align-items:center;gap:6px;padding:2px 0;'><div style='width:4px;height:34px;background:#8b5cf6;border-radius:2px;flex-shrink:0;'></div><div><div style='font-size:9px;color:#888;font-weight:600;letter-spacing:0.5px;'>2027 DRAFT PICKS</div><div style='font-size:13px;font-weight:700;color:#333;line-height:1.5;white-space:nowrap;'>{point.picks}</div></div></div>",
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

</details>

## Deployment Script

`deploy-draft-picks.py` handles backup + deploy via the QuickSight API.

```bash
# Dry run (preview only)
python draft-picks/deploy-draft-picks.py --dry-run

# Deploy
python draft-picks/deploy-draft-picks.py
```

Update these constants at the top of the script before running:

```python
AWS_REGION   = "us-east-1"
AWS_ACCOUNT  = "079495165177"
ANALYSIS_ID  = "afdeb116-3da4-42a7-a430-24bcba19b208"
SHEET_ID     = "c8901a01-414f-44e6-acf9-9a939f09f129"
VISUAL_ID    = "draft-picks-visual-001"
DATASET_ID   = "769b5fe5-d563-4a0e-8a1e-0e602789d328"
```

The script will:
1. Back up the current analysis definition to `backups/`
2. Load `quicksight-draft-picks.json`
3. Create or update the PluginVisual on the target sheet
4. Push the update via `update_analysis`

## Local Testing

Open `test-draft-picks.html` in a browser. Requires `highcharts.js` in the project root (not committed — download Highcharts 11.4.6 locally).

## Files

| File | Purpose |
|------|---------|
| `quicksight-draft-picks.json` | Highcharts config (paste into QuickSight) |
| `deploy-draft-picks.py` | API deployment script |
| `test-draft-picks.html` | Local browser test |
| `DEPLOYMENT-LOG.md` | Deployment history and troubleshooting |
