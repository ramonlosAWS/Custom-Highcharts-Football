#!/usr/bin/env python3
"""
Deploy Position Filter Buttons Widget to QuickSight

Creates a new Highcharts visual for position filter buttons on the specified sheet.
"""

import boto3
import json
import sys
import time
from botocore.config import Config

# Configuration
AWS_REGION = "us-east-1"
AWS_ACCOUNT = "079495165177"
ANALYSIS_ID = "ce7c0623-4822-47c9-9615-c06115065d96"
SHEET_ID = "4d8565b9-9ffb-455e-b6f1-b856885c6531"
DATASET_ID = "NFL Raw Roster Data"

# Visual ID for the position filter buttons
POSITION_FILTER_VISUAL_ID = "position-filter-buttons-001"

BOTO_CONFIG = Config(connect_timeout=10, read_timeout=60, retries={'max_attempts': 2})

def load_highcharts_config(config_file):
    """Load Highcharts JSON config from file."""
    with open(config_file, 'r') as f:
        config = json.load(f)
    if '_comment' in config:
        del config['_comment']
    return config

def create_backup(qs, account_id, analysis_id):
    """Create backup of current analysis."""
    import os
    response = qs.describe_analysis_definition(
        AwsAccountId=account_id,
        AnalysisId=analysis_id
    )
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    backup_file = f"{backup_dir}/analysis-{analysis_id[:8]}-{timestamp}.json"
    
    backup_data = {
        "AnalysisId": analysis_id,
        "Name": response.get('Name', 'Analysis'),
        "Definition": response['Definition'],
        "BackupTimestamp": timestamp
    }
    
    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, indent=2, default=str)
    
    print(f"✓ Backup saved to: {backup_file}")
    return response

def main():
    config_file = sys.argv[1] if len(sys.argv) > 1 else "position-filter-buttons/quicksight-position-filter-buttons.json"
    
    print(f"Loading config from: {config_file}")
    highcharts_config = load_highcharts_config(config_file)
    
    qs = boto3.client('quicksight', region_name=AWS_REGION, config=BOTO_CONFIG)
    
    # Create backup first
    print("Creating backup...")
    response = create_backup(qs, AWS_ACCOUNT, ANALYSIS_ID)
    
    definition = response['Definition']
    analysis_name = response.get('Name', 'Analysis')
    
    # Add PositionFilter parameter if it doesn't exist
    if 'ParameterDeclarations' not in definition:
        definition['ParameterDeclarations'] = []
    
    param_exists = any(
        p.get('StringParameterDeclaration', {}).get('Name') == 'PositionFilter'
        for p in definition['ParameterDeclarations']
    )
    
    if not param_exists:
        print("Adding PositionFilter parameter...")
        definition['ParameterDeclarations'].append({
            'StringParameterDeclaration': {
                'ParameterValueType': 'SINGLE_VALUED',
                'Name': 'PositionFilter',
                'DefaultValues': {
                    'StaticValues': ['ALL']
                },
                'ValueWhenUnset': {
                    'ValueWhenUnsetOption': 'RECOMMENDED_VALUE'
                }
            }
        })
    
    # Add SelectedPosition calculated field if it doesn't exist
    if 'CalculatedFields' not in definition:
        definition['CalculatedFields'] = []
    
    calc_field_exists = any(
        cf.get('Name') == 'SelectedPosition'
        for cf in definition['CalculatedFields']
    )
    
    if not calc_field_exists:
        print("Adding SelectedPosition calculated field...")
        definition['CalculatedFields'].append({
            'DataSetIdentifier': DATASET_ID,
            'Name': 'SelectedPosition',
            'Expression': '${PositionFilter}'
        })
    
    # Create sheet if it doesn't exist
    if 'Sheets' not in definition or len(definition.get('Sheets', [])) == 0:
        print(f"No sheets found, creating new sheet...")
        definition['Sheets'] = [{
            'SheetId': SHEET_ID,
            'Name': 'Position Filter Test',
            'Visuals': [],
            'Layouts': [{
                'Configuration': {
                    'GridLayout': {
                        'Elements': [],
                        'CanvasSizeOptions': {
                            'ScreenCanvasSizeOptions': {
                                'ResizeOption': 'FIXED',
                                'OptimizedViewPortWidth': '1600px'
                            }
                        }
                    }
                }
            }],
            'ContentType': 'INTERACTIVE'
        }]
    
    # Find the target sheet
    target_sheet = None
    sheet_index = None
    for i, sheet in enumerate(definition.get('Sheets', [])):
        if sheet.get('SheetId') == SHEET_ID:
            target_sheet = sheet
            sheet_index = i
            break
    
    # If still not found, use first sheet
    if not target_sheet and definition.get('Sheets'):
        target_sheet = definition['Sheets'][0]
        sheet_index = 0
        print(f"Using first sheet: {target_sheet.get('SheetId')}")
    
    if not target_sheet:
        print(f"Error: Sheet {SHEET_ID} not found")
        sys.exit(1)
    
    # Check if visual already exists
    existing_visual_index = None
    for i, visual in enumerate(target_sheet.get('Visuals', [])):
        if 'PluginVisual' in visual:
            if visual['PluginVisual'].get('VisualId') == POSITION_FILTER_VISUAL_ID:
                existing_visual_index = i
                print(f"Found existing position filter visual, will update it")
                break
    
    # Column mapping - only need SelectedPosition calculated field
    # This holds the current parameter value for comparison
    columns = [
        ("SelectedPosition", "STRING"),   # 0 - calculated field with parameter value
    ]
    
    # Build dimensions for field wells
    timestamp_ms = int(time.time() * 1000)
    dimensions = []
    for i, (col_name, col_type) in enumerate(columns):
        field_id = f"{DATASET_ID}-{col_name.lower()}.{i}.{timestamp_ms + i}"
        dimensions.append({
            "CategoricalDimensionField": {
                "FieldId": field_id,
                "Column": {
                    "DataSetIdentifier": DATASET_ID,
                    "ColumnName": col_name
                }
            }
        })
    
    # Build the visual configuration
    new_visual = {
        "PluginVisual": {
            "VisualId": POSITION_FILTER_VISUAL_ID,
            "PluginArn": "arn:aws:quicksight::aws:visualplugin/highcharts/alias/V1",
            "Title": {"Visibility": "HIDDEN"},
            "Subtitle": {"Visibility": "HIDDEN"},
            "ChartConfiguration": {
                "FieldWells": [
                    {
                        "AxisName": "GROUP_BY",
                        "Dimensions": dimensions
                    }
                ],
                "VisualOptions": {
                    "VisualProperties": [
                        {
                            "Name": "codeEditor",
                            "Value": json.dumps(highcharts_config)
                        }
                    ]
                }
            },
            "Actions": []
        }
    }
    
    # Add or update the visual
    if existing_visual_index is not None:
        definition['Sheets'][sheet_index]['Visuals'][existing_visual_index] = new_visual
    else:
        definition['Sheets'][sheet_index]['Visuals'].append(new_visual)
        print(f"Adding new position filter visual: {POSITION_FILTER_VISUAL_ID}")
    
    # Update the analysis
    print("Updating analysis...")
    try:
        update_response = qs.update_analysis(
            AwsAccountId=AWS_ACCOUNT,
            AnalysisId=ANALYSIS_ID,
            Name=analysis_name,
            Definition=definition
        )
        print(f"✓ Analysis updated successfully")
        print(f"  Status: {update_response.get('Status')}")
        print(f"\nView at: https://us-east-1.quicksight.aws.amazon.com/sn/account/rl-enterprise/analyses/{ANALYSIS_ID}/sheets/{SHEET_ID}")
        print(f"\n⚠️  IMPORTANT: After deployment, you must:")
        print(f"  1. Go to Actions → Add action → Filter action")
        print(f"  2. Name: 'Filter by Position'")
        print(f"  3. Activation: On select")
        print(f"  4. Filter scope: Same sheet (or All sheets)")
        print(f"  5. Target visuals: Select depth chart and other visuals to filter")
        print(f"  6. The Position field will be used for filtering")
    except Exception as e:
        print(f"✗ Failed to update analysis: {e}")
        with open('position-filter-buttons/failed-definition.json', 'w') as f:
            json.dump(definition, f, indent=2)
        print("  Saved failed definition to position-filter-buttons/failed-definition.json")
        sys.exit(1)

if __name__ == "__main__":
    main()
