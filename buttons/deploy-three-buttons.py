#!/usr/bin/env python3
"""Deploy 3 button widgets to QuickSight analysis."""

import boto3
import json
import time

REGION = "us-east-1"
ACCOUNT_ID = "079495165177"
S3_BUCKET = "quicksight-widget-079495165177"
ANALYSIS_ID = "7f2779f2-8edd-474a-86d2-65f80c2ba4d6"

s3 = boto3.client("s3", region_name=REGION)
qs = boto3.client("quicksight", region_name=REGION)

# Button definitions
BUTTONS = [
    {
        "id": "fa-board-filter",
        "name": "FA Board Filter",
        "csv_path": "Custom-Highcharts-Football/buttons/fa-board-filter/fa-board-filter-data.csv",
        "param_name": "FABoardFilter",
        "param_default": "STREET FA",
        "calc_field_name": "SelectedFABoard",
        "labels": ["STREET FA", "STAFF CONNECTIONS", "OUTGOING", "CTR LIST"],
        "start_x": 14,
        "spacing": 19,
        "div_width": 163,
        "last_index": 3,
    },
    {
        "id": "team-draft-view-selector",
        "name": "Team Draft View Selector",
        "csv_path": "Custom-Highcharts-Football/buttons/team-draft-view-selector/team-draft-view-selector-data.csv",
        "param_name": "TeamDraftView",
        "param_default": "MOCK DRAFT TRACKER",
        "calc_field_name": "SelectedDraftView",
        "labels": ["MOCK DRAFT TRACKER", "DJ'S TOP 50"],
        "start_x": 25,
        "spacing": 25,
        "div_width": 180,
        "last_index": 1,
    },
    {
        "id": "team-strip-selector",
        "name": "Team Strip Selector",
        "csv_path": "Custom-Highcharts-Football/buttons/team-strip-selector/team-strip-selector-data.csv",
        "param_name": "TeamStripSelector",
        "param_default": "OFFSEASON PREVIEW",
        "calc_field_name": "SelectedStrip",
        "labels": ["OFFSEASON PREVIEW", "TEAM NEEDS"],
        "start_x": 25,
        "spacing": 25,
        "div_width": 180,
        "last_index": 1,
    },
]


def upload_csv_and_manifest(btn):
    """Upload CSV and manifest to S3, create data source and dataset."""
    ds_id = btn["id"] + "-data"
    src_id = btn["id"] + "-s3-source"
    s3_csv_key = f"buttons/{btn['id']}/{btn['id']}-data.csv"
    s3_manifest_key = f"buttons/{btn['id']}/{btn['id']}-manifest.json"

    # Upload CSV
    with open(btn["csv_path"], "rb") as f:
        s3.put_object(Bucket=S3_BUCKET, Key=s3_csv_key, Body=f.read())
    print(f"  Uploaded CSV to s3://{S3_BUCKET}/{s3_csv_key}")

    # Create and upload manifest
    manifest = {
        "fileLocations": [{"URIs": [f"s3://{S3_BUCKET}/{s3_csv_key}"]}],
        "globalUploadSettings": {
            "format": "CSV",
            "delimiter": ",",
            "textqualifier": "'",
            "containsHeader": "true",
        },
    }
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=s3_manifest_key,
        Body=json.dumps(manifest),
        ContentType="application/json",
    )
    print(f"  Uploaded manifest to s3://{S3_BUCKET}/{s3_manifest_key}")

    # Create data source
    try:
        qs.create_data_source(
            AwsAccountId=ACCOUNT_ID,
            DataSourceId=src_id,
            Name=f"{btn['name']} S3 Source",
            Type="S3",
            DataSourceParameters={
                "S3Parameters": {
                    "ManifestFileLocation": {
                        "Bucket": S3_BUCKET,
                        "Key": s3_manifest_key,
                    }
                }
            },
            Permissions=[
                {
                    "Principal": f"arn:aws:quicksight:{REGION}:{ACCOUNT_ID}:user/default/adminperson",
                    "Actions": [
                        "quicksight:DescribeDataSource",
                        "quicksight:DescribeDataSourcePermissions",
                        "quicksight:PassDataSource",
                        "quicksight:UpdateDataSource",
                        "quicksight:DeleteDataSource",
                        "quicksight:UpdateDataSourcePermissions",
                    ],
                }
            ],
        )
        print(f"  Created data source: {src_id}")
    except qs.exceptions.ResourceExistsException:
        qs.update_data_source(
            AwsAccountId=ACCOUNT_ID,
            DataSourceId=src_id,
            Name=f"{btn['name']} S3 Source",
            DataSourceParameters={
                "S3Parameters": {
                    "ManifestFileLocation": {
                        "Bucket": S3_BUCKET,
                        "Key": s3_manifest_key,
                    }
                }
            },
        )
        print(f"  Updated existing data source: {src_id}")

    # Create dataset
    physical_table = {
        "S3Source": {
            "DataSourceArn": f"arn:aws:quicksight:{REGION}:{ACCOUNT_ID}:datasource/{src_id}",
            "InputColumns": [
                {"Name": "SortOrder", "Type": "STRING"},
                {"Name": "ButtonLabel", "Type": "STRING"},
            ],
        }
    }

    logical_table = {
        "Alias": btn["id"],
        "DataTransforms": [
            {
                "CastColumnTypeOperation": {
                    "ColumnName": "SortOrder",
                    "NewColumnType": "INTEGER",
                }
            }
        ],
        "Source": {"PhysicalTableId": "physical0"},
    }

    try:
        qs.create_data_set(
            AwsAccountId=ACCOUNT_ID,
            DataSetId=ds_id,
            Name=btn["name"],
            PhysicalTableMap={"physical0": physical_table},
            LogicalTableMap={"logical0": logical_table},
            ImportMode="SPICE",
            Permissions=[
                {
                    "Principal": f"arn:aws:quicksight:{REGION}:{ACCOUNT_ID}:user/default/adminperson",
                    "Actions": [
                        "quicksight:DescribeDataSet",
                        "quicksight:DescribeDataSetPermissions",
                        "quicksight:PassDataSet",
                        "quicksight:DescribeIngestion",
                        "quicksight:ListIngestions",
                        "quicksight:UpdateDataSet",
                        "quicksight:DeleteDataSet",
                        "quicksight:CreateIngestion",
                        "quicksight:CancelIngestion",
                        "quicksight:UpdateDataSetPermissions",
                    ],
                }
            ],
        )
        print(f"  Created dataset: {ds_id}")
    except qs.exceptions.ResourceExistsException:
        qs.update_data_set(
            AwsAccountId=ACCOUNT_ID,
            DataSetId=ds_id,
            Name=btn["name"],
            PhysicalTableMap={"physical0": physical_table},
            LogicalTableMap={"logical0": logical_table},
            ImportMode="SPICE",
        )
        print(f"  Updated existing dataset: {ds_id}")

    # Trigger SPICE ingestion
    ingestion_id = f"ingestion-{btn['id']}-{int(time.time())}"
    qs.create_ingestion(
        AwsAccountId=ACCOUNT_ID,
        DataSetId=ds_id,
        IngestionId=ingestion_id,
    )
    print(f"  Triggered SPICE ingestion: {ingestion_id}")

    return ds_id


def build_highcharts_config(btn):
    """Build the Highcharts JSON config string for a button widget."""
    config = {
        "chart": {
            "type": "scatter",
            "backgroundColor": "transparent",
            "height": 38,
            "spacing": [5, 0, 5, 0],
            "animation": False,
            "style": {
                "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
            },
        },
        "title": {"text": None},
        "legend": {"enabled": False},
        "credits": {"enabled": False},
        "xAxis": {"min": 0, "max": 100, "visible": False},
        "yAxis": {"min": 0, "max": 100, "visible": False},
        "tooltip": {"enabled": False},
        "plotOptions": {
            "scatter": {
                "marker": {"enabled": False, "radius": 0},
                "animation": False,
                "states": {
                    "hover": {"enabled": False},
                    "select": {"enabled": False},
                    "inactive": {"enabled": False},
                },
            },
            "series": {
                "enableMouseTracking": True,
                "cursor": "pointer",
                "animation": False,
                "marker": {
                    "enabled": False,
                    "radius": 0,
                    "states": {
                        "hover": {"enabled": False, "radius": 0},
                        "select": {"enabled": False, "radius": 0},
                    },
                },
            },
        },
        "series": [
            {
                "name": btn["param_name"],
                "data": [
                    "map",
                    ["getColumn", 1, 2],
                    {
                        "x": ["+", btn["start_x"], ["*", ["itemIndex"], btn["spacing"]]],
                        "y": 50,
                        "label": ["get", ["item"], 0],
                        "bg": [
                            "case",
                            ["==", ["get", ["item"], 0], ["get", ["item"], 1]],
                            "#1a2b4c",
                            "transparent",
                        ],
                        "tc": [
                            "case",
                            ["==", ["get", ["item"], 0], ["get", ["item"], 1]],
                            "#ffffff",
                            "#1a2b4c",
                        ],
                        "fw": "600",
                        "div": [
                            "case",
                            ["==", ["itemIndex"], btn["last_index"]],
                            "none",
                            "1px solid #c0c8d1",
                        ],
                    },
                ],
                "dataLabels": {
                    "enabled": True,
                    "useHTML": True,
                    "format": f"<div style='width:{btn['div_width']}px;height:31px;line-height:31px;text-align:center;font-size:14px;font-weight:{{point.fw}};color:{{point.tc}};background:{{point.bg}};border-right:{{point.div}};cursor:pointer;box-sizing:border-box;white-space:nowrap;'>{{point.label}}</div>",
                    "align": "center",
                    "verticalAlign": "middle",
                    "overflow": "allow",
                    "crop": False,
                    "style": {"textOutline": "none"},
                },
                "point": {
                    "events": {
                        "click": ["triggerClick", {"rowIndex": "point.index"}]
                    }
                },
            }
        ],
    }
    return json.dumps(config)


def build_plugin_visual(btn, ds_id, visual_id):
    """Build the PluginVisual definition for a button widget."""
    config_str = build_highcharts_config(btn)

    return {
        "PluginVisual": {
            "VisualId": visual_id,
            "PluginArn": "arn:aws:quicksight::aws:visualplugin/highcharts/alias/V1",
            "Title": {"Visibility": "HIDDEN"},
            "Subtitle": {"Visibility": "HIDDEN"},
            "ChartConfiguration": {
                "FieldWells": [
                    {
                        "AxisName": "GROUP_BY",
                        "Dimensions": [
                            {
                                "NumericalDimensionField": {
                                    "FieldId": f"{ds_id}.SortOrder.0.{int(time.time())}",
                                    "Column": {
                                        "DataSetIdentifier": ds_id,
                                        "ColumnName": "SortOrder",
                                    },
                                }
                            },
                            {
                                "CategoricalDimensionField": {
                                    "FieldId": f"{ds_id}.ButtonLabel.1.{int(time.time())}",
                                    "Column": {
                                        "DataSetIdentifier": ds_id,
                                        "ColumnName": "ButtonLabel",
                                    },
                                }
                            },
                            {
                                "CategoricalDimensionField": {
                                    "FieldId": f"{ds_id}.{btn['calc_field_name']}.2.{int(time.time())}",
                                    "Column": {
                                        "DataSetIdentifier": ds_id,
                                        "ColumnName": btn["calc_field_name"],
                                    },
                                }
                            },
                        ],
                    }
                ],
                "VisualOptions": {
                    "VisualProperties": [
                        {"Name": "codeEditor", "Value": config_str}
                    ]
                },
            },
            "Actions": [
                {
                    "CustomActionId": f"action-{btn['id']}",
                    "Name": f"Set {btn['param_name']}",
                    "Status": "ENABLED",
                    "Trigger": "DATA_POINT_CLICK",
                    "ActionOperations": [
                        {
                            "NavigationOperation": {
                                "LocalNavigationConfiguration": {
                                    "TargetSheetId": "b7498f2a-c673-4843-a344-a94cbf20bb8f"
                                }
                            }
                        },
                        {
                            "SetParametersOperation": {
                                "ParameterValueConfigurations": [
                                    {
                                        "DestinationParameterName": btn["param_name"],
                                        "Value": {
                                            "SourceColumn": {
                                                "DataSetIdentifier": ds_id,
                                                "ColumnName": "ButtonLabel",
                                            },
                                        },
                                    }
                                ]
                            }
                        },
                    ],
                }
            ],
        }
    }


def main():
    print("=" * 60)
    print("Deploying 3 button widgets to QuickSight")
    print("=" * 60)

    # Step 1: Upload data and create datasets
    dataset_ids = {}
    for btn in BUTTONS:
        print(f"\n[{btn['name']}]")
        ds_id = upload_csv_and_manifest(btn)
        dataset_ids[btn["id"]] = ds_id

    # Wait for SPICE ingestions
    print("\nWaiting 10s for SPICE ingestions...")
    time.sleep(10)

    # Step 2: Get current analysis definition
    print("\nFetching current analysis definition...")
    resp = qs.describe_analysis_definition(
        AwsAccountId=ACCOUNT_ID, AnalysisId=ANALYSIS_ID
    )
    definition = resp["Definition"]
    name = resp["Name"]

    # Step 3: Add dataset declarations
    existing_ds_ids = {d["Identifier"] for d in definition["DataSetIdentifierDeclarations"]}
    for btn in BUTTONS:
        ds_id = dataset_ids[btn["id"]]
        if ds_id not in existing_ds_ids:
            definition["DataSetIdentifierDeclarations"].append(
                {
                    "Identifier": ds_id,
                    "DataSetArn": f"arn:aws:quicksight:{REGION}:{ACCOUNT_ID}:dataset/{ds_id}",
                }
            )
            print(f"  Added dataset declaration: {ds_id}")

    # Step 4: Add parameters
    if "ParameterDeclarations" not in definition:
        definition["ParameterDeclarations"] = []
    existing_params = {
        p.get("StringParameterDeclaration", {}).get("Name", "")
        for p in definition["ParameterDeclarations"]
    }
    for btn in BUTTONS:
        if btn["param_name"] not in existing_params:
            definition["ParameterDeclarations"].append(
                {
                    "StringParameterDeclaration": {
                        "ParameterValueType": "SINGLE_VALUED",
                        "Name": btn["param_name"],
                        "DefaultValues": {
                            "StaticValues": [btn["param_default"]]
                        },
                        "ValueWhenUnset": {
                            "ValueWhenUnsetOption": "NULL"
                        },
                    }
                }
            )
            print(f"  Added parameter: {btn['param_name']} (default: {btn['param_default']})")

    # Step 5: Add calculated fields
    if "CalculatedFields" not in definition:
        definition["CalculatedFields"] = []
    existing_calcs = {c["Name"] for c in definition["CalculatedFields"]}
    for btn in BUTTONS:
        ds_id = dataset_ids[btn["id"]]
        if btn["calc_field_name"] not in existing_calcs:
            definition["CalculatedFields"].append(
                {
                    "DataSetIdentifier": ds_id,
                    "Name": btn["calc_field_name"],
                    "Expression": "${" + btn["param_name"] + "}",
                }
            )
            print(f"  Added calc field: {btn['calc_field_name']} = ${{{btn['param_name']}}}")

    # Step 6: Add visuals to the sheet
    sheet = definition["Sheets"][0]
    visual_ids = {}
    for i, btn in enumerate(BUTTONS):
        ds_id = dataset_ids[btn["id"]]
        visual_id = f"visual-{btn['id']}"
        visual_ids[btn["id"]] = visual_id
        visual = build_plugin_visual(btn, ds_id, visual_id)
        sheet["Visuals"].append(visual)
        print(f"  Added visual: {visual_id}")

    # Step 7: Add layout elements for new visuals
    layout = sheet["Layouts"][0]["Configuration"]["GridLayout"]
    for i, btn in enumerate(BUTTONS):
        vid = visual_ids[btn["id"]]
        layout["Elements"].append(
            {
                "ElementId": vid,
                "ElementType": "VISUAL",
                "ColumnSpan": 18,
                "RowSpan": 3,
            }
        )

    # Step 8: Update the analysis
    print("\nUpdating analysis...")
    try:
        qs.update_analysis(
            AwsAccountId=ACCOUNT_ID,
            AnalysisId=ANALYSIS_ID,
            Name=name,
            Definition=definition,
        )
        print("Analysis updated successfully!")
    except Exception as e:
        print(f"Error updating analysis: {e}")
        # Save failed definition for debugging
        with open("/tmp/failed-definition.json", "w") as f:
            json.dump(definition, f, indent=2, default=str)
        print("Saved failed definition to /tmp/failed-definition.json")
        raise

    print("\n" + "=" * 60)
    print("DONE! 3 button widgets deployed.")
    print(f"Open: https://us-east-1.quicksight.aws.amazon.com/sn/account/rl-enterprise/analyses/{ANALYSIS_ID}")
    print("=" * 60)


if __name__ == "__main__":
    main()
