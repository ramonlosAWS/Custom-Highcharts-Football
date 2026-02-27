#!/usr/bin/env python3
"""Update all 4 Highcharts visuals in the TeamCap analysis with latest configs."""
import json
import boto3
import time

REGION = "us-east-1"
ANALYSIS_ID = "10f40472-d0d5-4b34-b830-1bb0fa0547da"

# Visual ID -> config file mapping
VISUAL_CONFIGS = {
    "f82b137d-b42f-4fd9-9419-7dee1f7b1552": "Custom-Highcharts-Football/CapSpace/quicksight-draft-capital-bullet.json",
    "250299e9-9c0d-4a17-97c3-bd4c9e40da67": "Custom-Highcharts-Football/CapSpace/quicksight-draft-capital-thermometer.json",
    "12a7b52c-acb2-46d8-8844-12ace6372c72": "Custom-Highcharts-Football/CapSpace/quicksight-draft-capital-rank.json",
    "cap-metrics-visual-001": "Custom-Highcharts-Football/CapSpace/quicksight-cap-metrics.json",
}

def main():
    sts = boto3.client("sts", region_name=REGION)
    account_id = sts.get_caller_identity()["Account"]
    qs = boto3.client("quicksight", region_name=REGION)

    # Load all configs
    configs = {}
    for vid, path in VISUAL_CONFIGS.items():
        with open(path) as f:
            configs[vid] = json.dumps(json.load(f))
        print(f"Loaded config for {vid} from {path}")

    # Get current analysis
    print("\nDescribing analysis...")
    resp = qs.describe_analysis_definition(
        AwsAccountId=account_id,
        AnalysisId=ANALYSIS_ID
    )
    definition = resp["Definition"]
    name = resp["Name"]

    # Update each visual's codeEditor
    updated = []
    for sheet in definition["Sheets"]:
        for visual in sheet.get("Visuals", []):
            pv = visual.get("PluginVisual")
            if not pv:
                continue
            vid = pv["VisualId"]
            if vid not in configs:
                continue

            # Find and update codeEditor property
            vis_opts = pv.get("ChartConfiguration", {}).get("VisualOptions", {})
            props = vis_opts.get("VisualProperties", [])
            found = False
            for prop in props:
                if prop.get("Name") == "codeEditor":
                    prop["Value"] = configs[vid]
                    found = True
                    break
            if not found:
                props.append({"Name": "codeEditor", "Value": configs[vid]})
                vis_opts["VisualProperties"] = props

            updated.append(vid)
            print(f"Updated codeEditor for visual {vid}")

    if not updated:
        print("No visuals found to update!")
        return

    print(f"\nUpdating analysis with {len(updated)} visual changes...")
    qs.update_analysis(
        AwsAccountId=account_id,
        AnalysisId=ANALYSIS_ID,
        Name=name,
        Definition=definition
    )
    print("Done! Refresh QuickSight to see changes.")

if __name__ == "__main__":
    main()
