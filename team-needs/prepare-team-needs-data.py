#!/usr/bin/env python3
"""
Prepare Team Summary Data from Team Master CSV

This script extracts the necessary columns from the NFL Team Master CSV
and creates a clean dataset for the team summary visualization.
"""

import pandas as pd
import sys

def prepare_data(input_file, output_file):
    """Extract and prepare team summary data"""
    
    print(f"Reading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    print(f"Found {len(df)} teams")
    
    # Team colors mapping (primary colors)
    team_colors = {
        'ARI': '#97233F', 'ATL': '#A71930', 'BAL': '#241773', 'BUF': '#00338D',
        'CAR': '#0085CA', 'CHI': '#0B162A', 'CIN': '#FB4F14', 'CLE': '#311D00',
        'DAL': '#041E42', 'DEN': '#FB4F14', 'DET': '#0076B6', 'GB': '#203731',
        'HOU': '#03202F', 'IND': '#002C5F', 'JAX': '#006778', 'KC': '#E31837',
        'LAC': '#0080C6', 'LAR': '#003594', 'LV': '#000000', 'MIA': '#008E97',
        'MIN': '#4F2683', 'NE': '#002244', 'NO': '#D3BC8D', 'NYG': '#0B2265',
        'NYJ': '#125740', 'PHI': '#004C54', 'PIT': '#FFB612', 'SF': '#AA0000',
        'SEA': '#002244', 'TB': '#D50A0A', 'TEN': '#0C2340', 'WAS': '#5A1414'
    }
    
    # Select and rename columns
    summary_df = pd.DataFrame({
        'UniqueID': range(1, len(df) + 1),
        'TeamAbbr': df['Team Abbr'],
        'TeamColor': df['Team Abbr'].map(team_colors),
        'TeamNeeds': df['NFL.com Team Needs'],
        'GMName': df['GM Name'],
        'HCName': df['HC Name'],
        'OCName': df['OC Name'],
        'DCName': df['DC Name']
    })
    
    # Clean up any NaN values
    summary_df = summary_df.fillna('')
    
    # Save to CSV
    summary_df.to_csv(output_file, index=False)
    print(f"✓ Data saved to {output_file}")
    
    # Print sample
    print("\nSample data (first team):")
    print("-" * 80)
    for col in summary_df.columns:
        value = str(summary_df[col].iloc[0])
        if len(value) > 60:
            value = value[:57] + "..."
        print(f"{col:25s}: {value}")
    
    return summary_df

def main():
    """Main function"""
    input_file = "NFL IQ Live Data - TeamMaster.csv"
    output_file = "team-summary/team-summary-data.csv"
    
    try:
        df = prepare_data(input_file, output_file)
        print(f"\n✓ Successfully prepared data for {len(df)} teams")
        return 0
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
