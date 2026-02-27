# Cap Metrics Visual

3-row cap space metric cards with rank badges and progress bars. Designed for 185px height.

## Config

- `quicksight-cap-metrics.json` — v1 (all rows with rank bars)
- `quicksight-cap-metrics-v2.json` — v2 (dead money uses tier badge instead of bar)

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

## Share Docs

- `cap-metrics-share.md` — v1 documentation + JSON
- `cap-metrics-v2-share.md` — v2 documentation + JSON (tier badge for dead money)

## Working Files

Development assets are in `working/`:
- `test-cap-designs.html` — Local test page (all design variants)
- `highcharts.js` — Local Highcharts 11.4.6
- `NFL IQ Live Data - TeamCap (1).csv` — Source data
- `quicksight-draft-capital-*.json` — Earlier draft configs
- `deploy-cap-metrics.py` / `update-all-visuals.py` — Deployment scripts
