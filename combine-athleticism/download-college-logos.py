#!/usr/bin/env python3
"""
Download ALL FBS college team logos from ESPN CDN, encode as base64, save to CSV.
Format: CollegeName,ESPNId,LogoBase64
LogoBase64 is stored as url(data:image/png;base64,...) for direct use in QuickSight bubble markers.
"""

import requests
import base64
import csv
import time
from io import BytesIO
from PIL import Image

# All FBS teams with ESPN IDs (2025 season - 134 teams across all conferences)
# Source: ESPN team pages
FBS_TEAMS = [
    # SEC (16)
    ("Alabama", 333), ("Arkansas", 8), ("Auburn", 2), ("Florida", 57),
    ("Georgia", 61), ("Kentucky", 96), ("LSU", 99), ("Mississippi State", 344),
    ("Missouri", 142), ("Oklahoma", 201), ("Ole Miss", 145), ("South Carolina", 2579),
    ("Tennessee", 2633), ("Texas", 251), ("Texas A&M", 245), ("Vanderbilt", 238),
    # Big Ten (18)
    ("Illinois", 356), ("Indiana", 84), ("Iowa", 2294), ("Maryland", 120),
    ("Michigan", 130), ("Michigan State", 127), ("Minnesota", 135), ("Nebraska", 158),
    ("Northwestern", 77), ("Ohio State", 194), ("Oregon", 2483), ("Penn State", 213),
    ("Purdue", 2509), ("Rutgers", 164), ("UCLA", 26), ("USC", 30),
    ("Washington", 264), ("Wisconsin", 275),
    # Big 12 (16)
    ("Arizona", 12), ("Arizona State", 9), ("BYU", 252), ("Baylor", 239),
    ("Cincinnati", 2132), ("Colorado", 38), ("Houston", 248), ("Iowa State", 66),
    ("Kansas", 2305), ("Kansas State", 2306), ("Oklahoma State", 197), ("TCU", 2628),
    ("Texas Tech", 2641), ("UCF", 2116), ("Utah", 254), ("West Virginia", 277),
    # ACC (17)
    ("Boston College", 103), ("California", 25), ("Clemson", 228), ("Duke", 150),
    ("Florida State", 52), ("Georgia Tech", 59), ("Louisville", 97), ("Miami", 2390),
    ("NC State", 152), ("North Carolina", 153), ("Notre Dame", 87), ("Pitt", 221),
    ("SMU", 2567), ("Stanford", 24), ("Syracuse", 183), ("Virginia", 258),
    ("Virginia Tech", 259), ("Wake Forest", 154),
    # AAC (14)
    ("Army", 349), ("Charlotte", 2429), ("East Carolina", 151), ("FAU", 2226),
    ("Memphis", 235), ("Navy", 2426), ("North Texas", 249), ("Rice", 242),
    ("South Florida", 58), ("Temple", 218), ("Tulane", 2655), ("Tulsa", 202),
    ("UAB", 5), ("UTSA", 2636),
    # Sun Belt (14)
    ("Appalachian State", 2026), ("Arkansas State", 2032), ("Coastal Carolina", 324),
    ("Georgia Southern", 290), ("Georgia State", 2247), ("James Madison", 256),
    ("Louisiana", 309), ("Louisiana Monroe", 2433), ("Marshall", 276),
    ("Old Dominion", 295), ("South Alabama", 6), ("Southern Miss", 2572),
    ("Texas State", 326), ("Troy", 2653),
    # Mountain West (12)
    ("Air Force", 2005), ("Boise State", 68), ("Colorado State", 36),
    ("Fresno State", 278), ("Hawaii", 62), ("Nevada", 2440),
    ("New Mexico", 167), ("San Diego State", 21), ("San Jose State", 23),
    ("UNLV", 2439), ("Utah State", 328), ("Wyoming", 2704),
    # MAC (12)
    ("Akron", 2006), ("Ball State", 2050), ("Bowling Green", 189),
    ("Buffalo", 2084), ("Central Michigan", 2117), ("Eastern Michigan", 2199),
    ("Kent State", 2309), ("Miami (OH)", 193), ("Northern Illinois", 2459),
    ("Ohio", 195), ("Toledo", 2649), ("Western Michigan", 2711),
    # C-USA (10)
    ("FIU", 2229), ("Jacksonville State", 55), ("Kennesaw State", 338),
    ("Liberty", 2335), ("Louisiana Tech", 2348), ("Middle Tennessee", 2393),
    ("New Mexico State", 166), ("Sam Houston", 2534), ("UTEP", 2638),
    ("Western Kentucky", 98),
    # Independents
    ("UConn", 41),
]

LOGO_SIZE = 40  # pixels


def download_and_encode(espn_id, size=LOGO_SIZE):
    """Download logo from ESPN CDN, resize, return base64 url() string."""
    url = f"https://a.espncdn.com/i/teamlogos/ncaa/500/{espn_id}.png"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    img = Image.open(BytesIO(resp.content))
    img = img.convert('RGBA')
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    buf = BytesIO()
    img.save(buf, format='PNG', optimize=True)
    buf.seek(0)

    b64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"url(data:image/png;base64,{b64})"


def main():
    print(f"Downloading {len(FBS_TEAMS)} college logos...")
    print()

    results = []
    failed = []

    for i, (name, espn_id) in enumerate(FBS_TEAMS):
        try:
            logo_b64 = download_and_encode(espn_id)
            results.append((name, espn_id, logo_b64))
            print(f"  [{i+1}/{len(FBS_TEAMS)}] ✓ {name} ({len(logo_b64)} chars)")
        except Exception as e:
            failed.append((name, espn_id, str(e)))
            print(f"  [{i+1}/{len(FBS_TEAMS)}] ✗ {name}: {e}")

        # Small delay to be nice to ESPN CDN
        if (i + 1) % 20 == 0:
            time.sleep(0.5)

    # Write CSV
    csv_path = "college-logos-base64.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["CollegeName", "ESPNId", "LogoBase64"])
        for name, espn_id, logo in results:
            writer.writerow([name, espn_id, logo])

    print()
    print(f"✓ Saved {len(results)} logos to {csv_path}")
    if failed:
        print(f"✗ Failed: {len(failed)} teams:")
        for name, eid, err in failed:
            print(f"    {name} (ID {eid}): {err}")
    print()
    print(f"Total teams: {len(FBS_TEAMS)}")
    print(f"Successful: {len(results)}")
    print(f"Failed: {len(failed)}")


if __name__ == "__main__":
    main()
