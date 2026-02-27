# Team Needs Widget

A compact 350px wide sidebar widget displaying top 5 team needs with team color accent.

## Visual Design

- **Width**: 350px
- **Team color bar**: 4px left border
- **Header**: "TOP 5 TEAM NEEDS" (14px bold)
- **Subheader**: "ENTERING FREE AGENCY" (11px uppercase)
- **Data**: Team needs from NFL.com (16px bold)
- **Background**: Light gray (#f8f8f8)

## Files

- `quicksight-team-needs.json` - Highcharts configuration
- `test-team-needs.html` - Local test file
- `prepare-team-needs-data.py` - Data preparation script
- `team-needs-data.csv` - Prepared dataset (32 teams)

## Data Structure

### Columns (8 total)
1. UniqueID - Unique identifier (1-32)
2. TeamAbbr - Team abbreviation (e.g., "KC")
3. TeamColor - Team primary color hex (e.g., "#E31837")
4. TeamNeeds - Top 5 needs (e.g., "RB, WR, CB, OL, LB")
5. GMName - General Manager name
6. HCName - Head Coach name
7. OCName - Offensive Coordinator name
8. DCName - Defensive Coordinator name

**Note**: Only columns 0-3 are used in the visual. Columns 4-7 are included for potential future use.

## QuickSight Setup

### Field Wells
- **GROUP BY**: Add columns 0-3 (UniqueID, TeamAbbr, TeamColor, TeamNeeds)
- **VALUE**: Leave empty

### Filter Required
Add a filter control for `TeamAbbr` to display one team at a time.

## Usage

1. **Prepare data**:
   ```bash
   python3 team-needs/prepare-team-needs-data.py
   ```

2. **Test locally**:
   ```bash
   open team-needs/test-team-needs.html
   ```

3. **Deploy to QuickSight**:
   - Upload `team-needs-data.csv` to S3
   - Create dataset in QuickSight
   - Add Highcharts visual
   - Configure field wells (GROUP BY: columns 0-3)
   - Copy config from `quicksight-team-needs.json`
   - Add TeamAbbr filter control

## Customization

### Change Width
Modify the width in the format string:
```json
"format": "<div style='width:350px;..."
```

### Adjust Spacing
Change margin-bottom values:
```json
"margin-bottom:5px"   // After "TOP 5 TEAM NEEDS"
"margin-bottom:18px"  // After "ENTERING FREE AGENCY"
```

### Font Sizes
```json
"font-size:14px"  // Header
"font-size:11px"  // Subheader
"font-size:16px"  // Team needs data
```

## Team Colors

Colors are mapped from team abbreviations in the data preparation script. All 32 NFL teams are included with their official primary colors.

## Integration

This widget is designed to be used as a sidebar element alongside:
- Team logo header
- Roster table
- Depth chart
- Draft picks visualization

The 350px width fits well in a sidebar layout with main content at 900-1000px.
