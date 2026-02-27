# NFL Draft Picks Widget

This widget displays a team's draft picks for the current year (2026) and next year (2027).

## Dataset

**Dataset ID:** `769b5fe5-d563-4a0e-8a1e-0e602789d328`

**Key Columns:**
- `Team Abbr` (STRING) - Team abbreviation for filtering
- `Current Year Draft Picks` (STRING) - 2026 draft picks list
- `Next Year Draft Picks` (STRING) - 2027 draft picks by round

## Visual Design

The widget displays:
1. **2026 Draft Picks** - Full list of specific picks (e.g., "1.15, 2.47, 3.78")
2. **2027 Draft Picks** - Picks by round (e.g., "Rd 1, Rd 2, Rd 3, Rd 5")

## Files

- `quicksight-draft-picks.json` - Highcharts configuration
- `deploy-draft-picks.py` - Deployment script
- `test-draft-picks.html` - Local testing file

## Usage

1. Filter by team using `Team Abbr` parameter
2. Widget extracts single-row data using `["get", ["getColumn", X], 0]` pattern
3. Displays picks in formatted card layout

## Deployment

```bash
python draft-picks/deploy-draft-picks.py
```
