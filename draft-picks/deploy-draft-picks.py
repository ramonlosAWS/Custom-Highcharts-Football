#!/usr/bin/env python3
"""
Deploy NFL Draft Picks widget to QuickSight analysis.

This script deploys a Highcharts visual showing a team's draft picks
for 2026 (current year) and 2027 (next year).
"""

import boto3
import json
import sys
from datetime import datetime

# Configuration
AWS_REGION = "us-east-1"
AWS_ACCOUNT = "079495165177"
ANALYSIS_ID = "afdeb116-3da4-42a7-a430-24bcba19b208"
SHEET_ID = "c8901a01-414f-44e6-acf9-9a939f09f129"
VISUAL_ID = "draft-picks-visual-001"
DATASET_ID = "769b5fe5-d563-4a0e-8a1e-0e602789d328"

# Column mapping (update indices based on actual field wells order)
COLUMNS = {
    "current_year_picks": 0,  # Current Year Draft Picks
    "next_year_picks": 1      # Next Year Draft Picks
}

def load_config():
    """Load Highcharts configuration from JSON file."""
    with open('draft-picks/quicksight-draft-picks.json', 'r') as f:
        return json.load(f)

def create_backup(quicksight, analysis_id):
    """Create backup of current analysis."""
    try:
        response = quicksight.describe_analysis_definition(
            AwsAccountId=AWS_ACCOUNT,
            AnalysisId=analysis_id
        )
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        backup_file = f'backups/analysis-{analysis_id}-{timestamp}.json'
        
        with open(backup_file, 'w') as f:
            json.dump(response['Definition'], f, indent=2)
        
        print(f"✓ Backup created: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"⚠ Backup failed: {e}")
        return None

def create_visual_definition(config):
    """Create the PluginVisual definition for Highcharts."""
    return {
        "PluginVisual": {
            "VisualId": VISUAL_ID,
            "PluginArn": "arn:aws:quicksight::aws:visualplugin/highcharts/alias/V1",
            "Title": {
                "Visibility": "HIDDEN"
            },
            "Subtitle": {
                "Visibility": "HIDDEN"
            },
            "ChartConfiguration": {
                "FieldWells": [
                    {
                        "AxisName": "GROUP_BY",
                        "Dimensions": [
                            {
                                "CategoricalDimensionField": {
                                    "FieldId": f"{DATASET_ID}.current_year_picks.{datetime.now().timestamp()}",
                                    "Column": {
                                        "DataSetIdentifier": DATASET_ID,
                                        "ColumnName": "Current Year Draft Picks"
                                    }
                                }
                            },
                            {
                                "CategoricalDimensionField": {
                                    "FieldId": f"{DATASET_ID}.next_year_picks.{datetime.now().timestamp()}",
                                    "Column": {
                                        "DataSetIdentifier": DATASET_ID,
                                        "ColumnName": "Next Year Draft Picks"
                                    }
                                }
                            }
                        ]
                    }
                ],
                "VisualOptions": {
                    "VisualProperties": [
                        {
                            "Name": "codeEditor",
                            "Value": json.dumps(config)
                        }
                    ]
                }
            },
            "Actions": []
        }
    }

def deploy_visual(dry_run=False):
    """Deploy the visual to QuickSight."""
    quicksight = boto3.client('quicksight', region_name=AWS_REGION)
    
    print("=" * 60)
    print("NFL Draft Picks Widget Deployment")
    print("=" * 60)
    print(f"Analysis ID: {ANALYSIS_ID}")
    print(f"Sheet ID: {SHEET_ID}")
    print(f"Visual ID: {VISUAL_ID}")
    print(f"Dataset ID: {DATASET_ID}")
    print("=" * 60)
    
    # Create backup
    if not dry_run:
        create_backup(quicksight, ANALYSIS_ID)
    
    # Load configuration
    config = load_config()
    print(f"✓ Loaded Highcharts config")
    
    # Create visual definition
    visual_def = create_visual_definition(config)
    print(f"✓ Created visual definition")
    
    if dry_run:
        print("\n[DRY RUN] Would deploy visual with configuration:")
        print(json.dumps(visual_def, indent=2)[:500] + "...")
        return
    
    try:
        # Get current analysis definition
        response = quicksight.describe_analysis_definition(
            AwsAccountId=AWS_ACCOUNT,
            AnalysisId=ANALYSIS_ID
        )
        
        definition = response['Definition']
        
        # Add dataset declaration if not present
        dataset_declarations = definition.get('DataSetIdentifierDeclarations', [])
        dataset_exists = any(d['Identifier'] == DATASET_ID for d in dataset_declarations)
        
        if not dataset_exists:
            dataset_declarations.append({
                'Identifier': DATASET_ID,
                'DataSetArn': f'arn:aws:quicksight:{AWS_REGION}:{AWS_ACCOUNT}:dataset/{DATASET_ID}'
            })
            definition['DataSetIdentifierDeclarations'] = dataset_declarations
            print(f"✓ Added dataset declaration")
        
        # Find the sheet
        sheet_found = False
        for sheet in definition['Sheets']:
            if sheet['SheetId'] == SHEET_ID:
                sheet_found = True
                
                # Check if visual exists
                visual_exists = False
                for i, visual in enumerate(sheet['Visuals']):
                    if visual.get('PluginVisual', {}).get('VisualId') == VISUAL_ID:
                        sheet['Visuals'][i] = visual_def
                        visual_exists = True
                        print(f"✓ Updated existing visual")
                        break
                
                if not visual_exists:
                    sheet['Visuals'].append(visual_def)
                    print(f"✓ Added new visual")
                
                break
        
        if not sheet_found:
            print(f"✗ Sheet {SHEET_ID} not found")
            return
        
        # Get analysis name
        analysis_info = quicksight.describe_analysis(
            AwsAccountId=AWS_ACCOUNT,
            AnalysisId=ANALYSIS_ID
        )
        
        # Update analysis
        quicksight.update_analysis(
            AwsAccountId=AWS_ACCOUNT,
            AnalysisId=ANALYSIS_ID,
            Name=analysis_info['Analysis']['Name'],
            Definition=definition
        )
        
        print(f"✓ Visual deployed successfully")
        print("\nNext steps:")
        print("1. Add a filter control for 'Team Abbr' to select team")
        print("2. Verify draft picks display correctly")
        print("3. Adjust widget height if needed (currently 180px)")
        
    except Exception as e:
        print(f"✗ Deployment failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    deploy_visual(dry_run)
