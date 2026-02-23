# Dashboard Navigation Buttons

4 separate button widgets (one action per widget) that change the `DashboardView` parameter to control conditional visibility.

## Parameter Values

| Button Label | Parameter Value | Config File |
|--------------|-----------------|-------------|
| SUMMARY | `SUMMARY` | `quicksight-btn-summary.json` |
| TEAM NEEDS | `TEAMNEEDS` | `quicksight-btn-teamneeds.json` |
| 2025 RANKS | `2025RANKS` | `quicksight-btn-2025ranks.json` |
| 2026 TRACKER | `2026TRACKER` | `quicksight-btn-2026tracker.json` |

## QuickSight Setup

### 1. Create Parameter

1. Go to **Parameters** → **Create parameter**
2. Name: `DashboardView`
3. Data type: **String**
4. Default value: `SUMMARY`

### 2. Create Calculated Field

On any dataset:

1. Add calculated field: `SelectedView`
2. Expression: `${DashboardView}`

### 3. Create 4 Highcharts Visuals

For each button, create a separate Highcharts visual:

| Visual | Config File | Navigation Action |
|--------|-------------|-------------------|
| Button 1 | `quicksight-btn-summary.json` | Set `DashboardView` = `SUMMARY` |
| Button 2 | `quicksight-btn-teamneeds.json` | Set `DashboardView` = `TEAMNEEDS` |
| Button 3 | `quicksight-btn-2025ranks.json` | Set `DashboardView` = `2025RANKS` |
| Button 4 | `quicksight-btn-2026tracker.json` | Set `DashboardView` = `2026TRACKER` |

For each visual:
1. Paste the corresponding config
2. Field Wells: Add `SelectedView` to **GROUP BY**
3. Add Navigation Action: On select → Set parameter `DashboardView` to the value

### 4. Arrange Buttons

Place the 4 button widgets side-by-side horizontally in your dashboard layout.

### 5. Configure Conditional Visibility

For widgets to show/hide based on selection:
- Show when: `${DashboardView} = 'SUMMARY'` (etc.)

## Files

- `quicksight-btn-summary.json` - SUMMARY button
- `quicksight-btn-teamneeds.json` - TEAM NEEDS button  
- `quicksight-btn-2025ranks.json` - 2025 RANKS button
- `quicksight-btn-2026tracker.json` - 2026 TRACKER button
- `test-dashboard-nav-buttons.html` - Local test file

## Styling

- Selected: Navy background (#1a2b4c), white text
- Unselected: White background, navy text
- 1px gray border on all buttons
