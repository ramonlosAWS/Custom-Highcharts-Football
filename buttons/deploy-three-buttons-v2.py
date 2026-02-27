#!/usr/bin/env python3
"""Deploy 3 button widgets to QuickSight analysis (datasets already exist)."""

import boto3
import json
import time

REGION = "us-east-1"
ACCOUNT_ID = "079495165177"
ANALYSIS_ID = "7f2779f2-8edd-474a-86d2-65f80c2ba4d6"

qs = boto3.client("quicksight", region_name=REGION)

BUTTONS = [
    {
        "id": "fa-board-filter",
        "ds_id": "fa-board-filter-data",
        "name": "FA Board Filter",
        "param_name": "FABoardFilter",
        "param_default": "STREET FA",
        "calc_field_name": "SelectedFABoard",
        "start_x": 14,
        "spacing": 19,
        "div_width": 163,
        "last_index": 3,
        "col_span": 18,
    },
    {
        "id": "team-draft-view-selector",
        "ds_id": "team-draft-view-selector-data",
        "name": "Team Draft View Selector",
        "param_name": "TeamDraftView",
        "param_default": "MOCK DRAFT TRACKER",
        "calc_field_name": "SelectedDraftView",
        "start_x": 25,
        "spacing": 25,
        "div_width": 180,
        "last_index": 1,
        "col_span": 12,
    },
    {
        "id": "team-strip-selector",
        "ds_id": "team-strip-selector-data",
        "name": "Team Strip Selector",
        "param_name": "TeamStripSelector",
        "param_default": "OFFSEASON PREVIEW",
        "calc_field_name": "SelectedStrip",
        "start_x": 25,
        "spacing": 25,
        "div_width": 180,
        "last_index": 1,
        "col_span": 12,
    },
]


def build_highcharts_config(btn):
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


def build_plugin_visual(btn, visual_id, sheet_id):
    ds_id = btn["ds_id"]
    ts = str(int(time.time()))
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
                                    "FieldId": f"{ds_id}.SortOrder.0.{ts}",
                                    "Column": {
                                        "DataSetIdentifier": ds_id,
                                        "ColumnName": "SortOrder",
                                    },
                                }
                            },
                            {
                                "CategoricalDimensionField": {
                                    "FieldId": f"{ds_id}.ButtonLabel.1.{ts}",
                                    "Column": {
                                        "DataSetIdentifier": ds_id,
                                        "ColumnName": "ButtonLabel",
                                    },
                                }
                            },
                            {
                                "CategoricalDimensionField": {
                                    "FieldId": f"{ds_id}.{btn['calc_field_name']}.2.{ts}",
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
                                    "TargetSheetId": sheet_id
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
    print("Fetching analysis definition...")
    resp = qs.describe_analysis_definition(
        AwsAccountId=ACCOUNT_ID, AnalysisId=ANALYSIS_ID
    )
    definition = resp["Definition"]
    name = resp["Name"]
    sheet = definition["Sheets"][0]
    sheet_id = sheet["SheetId"]

    # Add dataset declarations
    existing_ds = {d["Identifier"] for d in definition["DataSetIdentifierDeclarations"]}
    for btn in BUTTONS:
        if btn["ds_id"] not in existing_ds:
            definition["DataSetIdentifierDeclarations"].append({
                "Identifier": btn["ds_id"],
                "DataSetArn": f"arn:aws:quicksight:{REGION}:{ACCOUNT_ID}:dataset/{btn['ds_id']}",
            })
            print(f"  Added dataset: {btn['ds_id']}")

    # Add parameters
    if "ParameterDeclarations" not in definition:
        definition["ParameterDeclarations"] = []
    existing_params = set()
    for p in definition["ParameterDeclarations"]:
        for ptype in p.values():
            if isinstance(ptype, dict):
                existing_params.add(ptype.get("Name", ""))
    for btn in BUTTONS:
        if btn["param_name"] not in existing_params:
            definition["ParameterDeclarations"].append({
                "StringParameterDeclaration": {
                    "ParameterValueType": "SINGLE_VALUED",
                    "Name": btn["param_name"],
                    "DefaultValues": {"StaticValues": [btn["param_default"]]},
                    "ValueWhenUnset": {"ValueWhenUnsetOption": "NULL"},
                }
            })
            print(f"  Added parameter: {btn['param_name']}")

    # Add calculated fields
    if "CalculatedFields" not in definition:
        definition["CalculatedFields"] = []
    existing_calcs = {c["Name"] for c in definition["CalculatedFields"]}
    for btn in BUTTONS:
        if btn["calc_field_name"] not in existing_calcs:
            definition["CalculatedFields"].append({
                "DataSetIdentifier": btn["ds_id"],
                "Name": btn["calc_field_name"],
                "Expression": "${" + btn["param_name"] + "}",
            })
            print(f"  Added calc field: {btn['calc_field_name']}")

    # Add visuals
    layout = sheet["Layouts"][0]["Configuration"]["GridLayout"]
    for btn in BUTTONS:
        visual_id = f"visual-{btn['id']}"
        visual = build_plugin_visual(btn, visual_id, sheet_id)
        sheet["Visuals"].append(visual)
        layout["Elements"].append({
            "ElementId": visual_id,
            "ElementType": "VISUAL",
            "ColumnSpan": btn["col_span"],
            "RowSpan": 3,
        })
        print(f"  Added visual: {visual_id}")

    # Update analysis
    print("\nUpdating analysis...")
    try:
        qs.update_analysis(
            AwsAccountId=ACCOUNT_ID,
            AnalysisId=ANALYSIS_ID,
            Name=name,
            Definition=definition,
        )
        print("SUCCESS!")
        print(f"\nhttps://us-east-1.quicksight.aws.amazon.com/sn/account/rl-enterprise/analyses/{ANALYSIS_ID}")
    except Exception as e:
        print(f"Error: {e}")
        with open("/tmp/failed-def-v2.json", "w") as f:
            json.dump(definition, f, indent=2, default=str)
        print("Saved to /tmp/failed-def-v2.json")
        raise


if __name__ == "__main__":
    main()
