# Position Filter Buttons - Setup Instructions

## Step 1: Create Parameter

1. In QuickSight, go to Parameters
2. Create a new parameter:
   - **Name:** `PositionFilter`
   - **Data type:** String
   - **Default value:** `ALL`
   - **Static default value:** `ALL`

## Step 2: Create Calculated Field

In your dataset (NFL Raw Roster Data), create a calculated field:

**Field Name:** `IsSelectedPosition`

**Formula:**
```
ifelse(
  {PositionFilter} = 'ALL', 'ALL',
  ifelse({Position} = {PositionFilter}, {Position}, null)
)
```

This field will return the position value only when it matches the parameter, or 'ALL' when showing all positions.

## Step 3: Add Highcharts Visual

1. Add a Highcharts visual to your sheet
2. Configure field wells:
   - **GROUP BY:** 
     - Position (from dataset)
     - IsSelectedPosition (calculated field)
3. Go to Format visual → Chart code
4. Paste the contents of `quicksight-position-filter-buttons-final.json`
5. Click APPLY CODE

## Step 4: Create Navigation Action

1. Go to Actions → Add action → Navigation action
2. Configure:
   - **Name:** "Select Position Filter"
   - **Activation:** On select
   - **Target sheet:** Same sheet
   - **Parameters:** 
     - Parameter: `PositionFilter`
     - Set to: Field value from `Position`

## How It Works

1. User clicks a position button (e.g., "QB")
2. Navigation action sets `PositionFilter` parameter to "QB"
3. The `IsSelectedPosition` calculated field updates
4. `dataMarkMatch` highlights the button where `IsSelectedPosition` matches `Position`
5. The selected button shows darker blue with darker border
6. Other visuals can filter using: `{Position} = {PositionFilter} OR {PositionFilter} = 'ALL'`

## Visual Styling

- **Selected button:** Dark blue (#005a94) with dark border (#003d66)
- **Unselected buttons:** Standard blue (#0073bb)
- **Default:** "ALL" is selected on page load
