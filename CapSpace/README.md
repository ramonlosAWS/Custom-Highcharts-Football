# Cap Metrics Visual

3-row cap space metric cards with rank badges and progress bars. Designed for 192px height.

## Config

`quicksight-cap-metrics.json`

## Field Wells

3 columns in GROUP BY + 3 columns in VALUE:

**GROUP BY:**

| Index | Column | Type | Used For |
|-------|--------|------|----------|
| 0 | Cap Space Rank | INTEGER | Row 3 rank badge |
| 1 | Active Cap Spending Rank | INTEGER | Row 1 rank badge |
| 2 | Dead Money Rank | INTEGER | Row 2 rank badge |

**VALUE (formatted as Currency):**

| Index | Column | Type | Used For |
|-------|--------|------|----------|
| 0 | Cap Space | INTEGER | Row 3 value (handles negative) |
| 1 | Active Cap Spending | INTEGER | Row 1 value |
| 2 | Dead Money | INTEGER | Row 2 value |

VALUE: (empty)

## Filter

Add a filter control on Team Abbr (or any unique identifier) to display one team at a time. This is a single-row extraction visual — without a filter, only the first row's data displays.

## Rows

| Row | Metric | Color | Bar Divisor |
|-----|--------|-------|-------------|
| 1 | Active Cap Spending | Green `#10b981` | 3,600,000 |
| 2 | Dead Money | Amber `#f59e0b` | 760,000 |
| 3 | Cap Space | Green/Red (conditional) | 1,050,000 |

Cap Space turns red (`#dc3545`) when negative, with value shown in parentheses.

## Working Files

Development assets are in `working/`:
- `test-cap-designs.html` — Local test page (all design variants)
- `highcharts.js` — Local Highcharts 11.4.6
- `NFL IQ Live Data - TeamCap (1).csv` — Source data
- `quicksight-draft-capital-*.json` — Earlier draft configs
- `deploy-cap-metrics.py` / `update-all-visuals.py` — Deployment scripts
