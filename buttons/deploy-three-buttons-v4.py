#!/usr/bin/env python3
"""Deploy 3 button widgets using the single Sheet1 dataset with Data Type filters.

UPDATED based on working analysis snapshot (4bed62ce-9343-4662-9e4f-74cf29501a64).

Key learnings from manual fix:
- ID columns are INTEGER type -> must use NumericalDimensionField (not Categorical)
- Calc field names are lowercase with spaces (e.g. 'selected fa filter')
- Filters use CONTAINS operator on Data Type column with NON_NULLS_ONLY
- Each filter is scoped to SELECTED_VISUALS with only that button's visual ID
"""

import boto3
import json
import time

REGION = "us-east-1"
ACCOUNT_ID = "079495165177"
ANALYSIS_ID = "7f2779f2-8edd-474a-86d2-65f80c2ba4d6"
DS_ID = "Sheet1"  # The dataset identifier in the analysis

qs = boto3.client("quicksight", region_name=REGION)

BUTTONS = [
    {
        "id": "fa-board-filter",
        "data_type": "Free Agent Board Filter",
        "param_name": "FABoardFilter",
        "param_default": "STREET FA",
        "calc_field_name": "selected fa filter",  # lowercase with spaces
        "id_col": "FA Board Filter ID",            # INTEGER -> NumericalDimensionField
        "label_col": "FA Board Filter",
        "start_x": 14,
        "spacing": 19,
        "div_width": 163,
        "last_index": 3,
        "visual_width": "928px",
        "visual_height": "80px",
    },
    {
        "id": "team-draft-view-selector",
        "data_type": "Team Draft View Selector",
        "param_name": "TeamDraftView",
        "param_default": "MOCK DRAFT TRACKER",
        "calc_field_name": "team draft view selector selected",  # lowercase with spaces
        "id_col": "Team Draft View Selector ID",                  # INTEGER -> NumericalDimensionField
        "label_col": "Team Draft View Selector",
        "start_x": 25,
        "spacing": 25,
        "div_width": 180,
        "last_index": 1,
        "visual_width": "800px",
        "visual_height": "64px",
    },
    {
        "id": "team-strip-selector",
        "data_type": "Team Strip Selector",
        "param_name": "TeamStripSelector",
        "param_default": "OFFSEASON PREVIEW",
        "calc_field_name": "team strip selector selected",  # lowercase with spaces
        "id_col": "Team Strip Selector ID",                  # INTEGER -> NumericalDimensionField
        "label_col": "Team Strip Selector",
        "start_x": 25,
        "spacing": 25,
        "div_width": 180,
        "last_index": 1,
        "visual_width": "800px",
        "visual_height": "64px",
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
    ts = str(int(time.time()))

    # Field IDs — using dataset name prefix like QuickSight generates
    id_field_id = f"sheet1-{btn['id_col'].lower().replace(' ', '_')[:10]}-{ts[:6]}.0.{ts}"
    label_field_id = f"sheet1-{btn['label_col'].lower().replace(' ', '_')[:10]}-{ts[:6]}.1.{ts}"
    calc_field_id = f"{btn['calc_field_name'].replace(' ', '-')}.2.{ts}"

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
                                # ID columns are INTEGER -> NumericalDimensionField
                                "NumericalDimensionField": {
                                    "FieldId": id_field_id,
                                    "Column": {
                                        "DataSetIdentifier": DS_ID,
                                        "ColumnName": btn["id_col"],
                                    },
                                }
                            },
                            {
                                "CategoricalDimensionField": {
                                    "FieldId": label_field_id,
                                    "Column": {
                                        "DataSetIdentifier": DS_ID,
                                        "ColumnName": btn["label_col"],
                                    },
                                }
                            },
                            {
                                "CategoricalDimensionField": {
                                    "FieldId": calc_field_id,
                                    "Column": {
                                        "DataSetIdentifier": DS_ID,
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
                                            "SourceField": label_field_id,
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


def build_filter_group(btn, visual_id, sheet_id):
    """Create a filter group that filters Data Type to this button's data type.
    Uses CONTAINS operator with NON_NULLS_ONLY, scoped to this visual only."""
    return {
        "FilterGroupId": f"filter-{btn['id']}",
        "Filters": [
            {
                "CategoryFilter": {
                    "FilterId": f"cat-filter-{btn['id']}",
                    "Column": {
                        "DataSetIdentifier": DS_ID,
                        "ColumnName": "Data Type",
                    },
                    "Configuration": {
                        "FilterListConfiguration": {
                            "MatchOperator": "CONTAINS",
                            "CategoryValues": [btn["data_type"]],
                            "NullOption": "NON_NULLS_ONLY",
                        }
                    },
                }
            }
        ],
        "ScopeConfiguration": {
            "SelectedSheets": {
                "SheetVisualScopingConfigurations": [
                    {
                        "SheetId": sheet_id,
                        "Scope": "SELECTED_VISUALS",
                        "VisualIds": [visual_id],
                    }
                ]
            }
        },
        "Status": "ENABLED",
        "CrossDataset": "SINGLE_DATASET",
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
    layout_config = sheet["Layouts"][0]["Configuration"]

    if "FreeFormLayout" in layout_config:
        layout = layout_config["FreeFormLayout"]
    elif "GridLayout" in layout_config:
        layout = layout_config["GridLayout"]
    else:
        raise ValueError(f"Unknown layout type: {list(layout_config.keys())}")

    # Remove old visuals from previous deploy attempts
    old_visual_ids = {"visual-fa-board-filter", "visual-team-draft-view-selector", "visual-team-strip-selector"}
    sheet["Visuals"] = [v for v in sheet["Visuals"]
                        if not any(vd.get("VisualId", "") in old_visual_ids
                                   for vd in v.values())]
    layout["Elements"] = [e for e in layout["Elements"]
                          if e["ElementId"] not in old_visual_ids]

    # Remove old separate dataset declarations (keep Sheet1)
    old_ds = {"fa-board-filter-data", "team-draft-view-selector-data", "team-strip-selector-data"}
    definition["DataSetIdentifierDeclarations"] = [
        d for d in definition["DataSetIdentifierDeclarations"]
        if d["Identifier"] not in old_ds
    ]

    # Remove old calc fields, then add correct ones on Sheet1
    existing_calc_names = {btn["calc_field_name"] for btn in BUTTONS}
    old_calc_names = {"SelectedFABoard", "SelectedDraftView", "SelectedStrip"}
    definition["CalculatedFields"] = [
        c for c in definition.get("CalculatedFields", [])
        if c["Name"] not in old_calc_names and c["Name"] not in existing_calc_names
    ]

    for btn in BUTTONS:
        definition["CalculatedFields"].append({
            "DataSetIdentifier": DS_ID,
            "Name": btn["calc_field_name"],
            "Expression": "${" + btn["param_name"] + "}",
        })
        print(f"  Added calc field: {btn['calc_field_name']} on {DS_ID}")

    # Ensure parameters exist
    existing_params = {p.get("StringParameterDeclaration", {}).get("Name")
                       for p in definition.get("ParameterDeclarations", [])}
    for btn in BUTTONS:
        if btn["param_name"] not in existing_params:
            definition.setdefault("ParameterDeclarations", []).append({
                "StringParameterDeclaration": {
                    "ParameterValueType": "SINGLE_VALUED",
                    "Name": btn["param_name"],
                    "DefaultValues": {"StaticValues": [btn["param_default"]]},
                    "ValueWhenUnset": {"ValueWhenUnsetOption": "NULL"},
                }
            })
            print(f"  Added parameter: {btn['param_name']}")

    # Add visuals and filters
    if "FilterGroups" not in definition:
        definition["FilterGroups"] = []

    y_positions = [176, 432, 528]  # Match the working analysis layout positions

    for i, btn in enumerate(BUTTONS):
        visual_id = f"visual-{btn['id']}"
        visual = build_plugin_visual(btn, visual_id, sheet_id)
        sheet["Visuals"].append(visual)

        layout["Elements"].append({
            "ElementId": visual_id,
            "ElementType": "VISUAL",
            "XAxisLocation": "32px",
            "YAxisLocation": f"{y_positions[i]}px",
            "Width": btn["visual_width"],
            "Height": btn["visual_height"],
            "Visibility": "VISIBLE",
        })
        print(f"  Added visual: {visual_id}")

        fg = build_filter_group(btn, visual_id, sheet_id)
        definition["FilterGroups"].append(fg)
        print(f"  Added filter: {fg['FilterGroupId']}")

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
        with open("/tmp/failed-def-v4.json", "w") as f:
            json.dump(definition, f, indent=2, default=str)
        print("Saved to /tmp/failed-def-v4.json")
        raise


if __name__ == "__main__":
    main()
