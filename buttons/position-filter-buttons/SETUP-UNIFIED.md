# Position Filter Buttons - Complete Setup

Single widget, ONE navigation action, data-driven buttons with ALL option.

## Quick Overview

| Component | Where | Purpose |
|-----------|-------|---------|
| `PositionFilter` parameter | Analysis | Stores selected position |
| `SelectedPosition` calc field | Button dataset | For button highlighting |
| `ShowByPosition` calc field | **Target dataset (roster, etc.)** | For filtering data |
| Filter `ShowByPosition = 1` | **Target visuals** | Actually filters the data |

---

## Step 1: Create Parameter

In your QuickSight Analysis:
1. Parameters → Create parameter
2. Settings:
   - Name: `PositionFilter`
   - Type: String
   - Default: `ALL`

---

## Step 2: Setup Button Dataset

Upload `position-buttons-data.csv`:
```csv
Position
ALL
QB
RB
WR
TE
OT
IOL
DT
EDGE
LB
S
CB
```

Add calculated field on this dataset:
```
Name: SelectedPosition
Expression: ${PositionFilter}
```

---

## Step 3: Create Button Widget

1. Add Highcharts visual
2. Field Wells (GROUP BY): 
   - `Position`
   - `SelectedPosition`
3. Paste `quicksight-position-buttons-SINGLE-ACTION.json`
4. Click APPLY CODE

---

## Step 4: Add Navigation Action

1. Actions menu → Add action
2. Name: `Set Position Filter`
3. Activation: `Select`
4. Action type: `Navigation action`
5. Target sheet: (current sheet)
6. Parameters: Click **+** icon
   - Parameter: `PositionFilter`
   - Value: **Select specific fields** → `Position`

---

## Step 5: Setup Target Visuals (CRITICAL!)

**On each dataset you want to filter** (e.g., NFL Roster dataset):

Add calculated field:
```
Name: ShowByPosition
Expression: ifelse(${PositionFilter}='ALL', 1, ifelse(Position=${PositionFilter}, 1, 0))
```

**On each visual** (roster table, depth chart, etc.):

Add filter:
- Field: `ShowByPosition`
- Condition: Equals `1`

---

## How the ALL Option Works

The `ShowByPosition` calc field logic:
- If parameter = 'ALL' → return 1 (show row)
- Else if Position matches parameter → return 1 (show row)  
- Else → return 0 (hide row)

Filter `ShowByPosition = 1` shows only rows where the calc returns 1.

| Click | Parameter Value | ShowByPosition Result |
|-------|-----------------|----------------------|
| ALL | `'ALL'` | 1 for ALL rows |
| QB | `'QB'` | 1 only for QB rows |
| WR | `'WR'` | 1 only for WR rows |

---

## Troubleshooting

**ALL shows no data:**
- Did you add `ShowByPosition` calc field to the TARGET dataset?
- Did you add filter `ShowByPosition = 1` to the target visual?
- Check calc field: `ifelse(${PositionFilter}='ALL', 1, ...)`

**Specific position shows no data:**
- Check that Position values in your data match button values exactly (QB, RB, WR, etc.)
- Case sensitive!

**Buttons not highlighting:**
- Verify `SelectedPosition` calc field on button dataset
- Check both `Position` and `SelectedPosition` in GROUP BY

---

## Files

- `quicksight-position-buttons-SINGLE-ACTION.json` - Highcharts config
- `position-buttons-data.csv` - Button data (12 rows)
