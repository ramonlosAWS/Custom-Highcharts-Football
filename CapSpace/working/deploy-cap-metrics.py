#!/usr/bin/env python3
"""Deploy cap-metrics Highcharts visual to the TeamCap analysis."""
import json
import boto3
import sys

REGION = "us-east-1"
ANALYSIS_ID = "10f40472-d0d5-4b34-b830-1bb0fa0547da"
SHEET_ID = "94defe33-cac0-41d2-815e-52d8d09be455"
DATASET_IDENTIFIER = "NFL IQ Live Data#TeamCap"
NEW_VISUAL_ID = "cap-metrics-visual-001"
CONFIG_FILE = "Custom-Highcharts-Football/CapSpace/quicksight-cap-metrics.json"

# Columns needed in GROUP BY (all columns from CSV)
COLUMNS = [
    ("Draft Order", "CategoricalDimensionField"),
    ("Team City", "CategoricalDimensionField"),
    ("Team Name", "CategoricalDimensionField"),
    ("Full Team Name", "CategoricalDimensionField"),
    ("Team Abbr", "CategoricalDimensionField"),
    ("Cap Space", "CategoricalDimensionField"),
    ("Effective Cap Space", "CategoricalDimensionField"),
    ("Active Cap Spending", "CategoricalDimensionField"),
    ("Dead Money", "CategoricalDimensionField"),
]

def main():
    sts = boto3.client("sts", region_name=REGION)
    account_id = sts.get_caller_identity()["Account"]

    qs = boto3.client("quicksight", region_name=REGION)

    # Load config JSON
    with open(CONFIG_FILE) as f:
        config_json = json.load(f)
    config_str = json.dumps(config_json)

    # Get current analysis definition
    print("Describing analysis...")
    resp = qs.describe_analysis_definition(
        AwsAccountId=account_id,
        AnalysisId=ANALYSIS_ID
    )
    definition = resp["Definition"]

    # Build field wells
    dimensions = []
    for i, (col_name, field_type) in enumerate(COLUMNS):
        field_id = f"{DATASET_IDENTIFIER}.{col_name}.{i}.{int(__import__('time').time())}"
        dim = {
            field_type: {
                "FieldId": field_id,
                "Column": {
                    "DataSetIdentifier": DATASET_IDENTIFIER,
                    "ColumnName": col_name
                }
            }
        }
        dimensions.append(dim)

    # Build the new PluginVisual
    new_visual = {
        "PluginVisual": {
            "VisualId": NEW_VISUAL_ID,
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
                            "Value": config_str
                        }
                    ]
                }
            },
            "Actions": []
        }
    }

    # Add visual to sheet
    for sheet in definition["Sheets"]:
        if sheet["SheetId"] == SHEET_ID:
            sheet["Visuals"].append(new_visual)
            print(f"Added visual {NEW_VISUAL_ID} to sheet {SHEET_ID}")
            break

    # Update analysis
    print("Updating analysis...")
    qs.update_analysis(
        AwsAccountId=account_id,
        AnalysisId=ANALYSIS_ID,
        Name=resp["Name"],
        Definition=definition
    )
    print("Done! Refresh QuickSight to see the new visual.")

if __name__ == "__main__":
    main()
