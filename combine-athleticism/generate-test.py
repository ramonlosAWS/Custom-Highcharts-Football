#!/usr/bin/env python3
"""
Generate test-combine-athleticism.html with base64-encoded college logos.
Downloads logos from ESPN CDN, resizes to 40x40, encodes as base64.
"""

import requests
import base64
from io import BytesIO

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("PIL not installed - will use raw downloaded images without resize")
    print("Install with: pip install Pillow")

# College logo URLs (ESPN CDN - reliable, public)
COLLEGES = [
    {"rank": 1, "name": "First Last", "college": "Florida",  "score": 92, "barColor": "#0077c8",
     "logoUrl": "https://a.espncdn.com/i/teamlogos/ncaa/500/57.png"},
    {"rank": 2, "name": "First Last", "college": "Georgia",  "score": 72, "barColor": "#ffc000",
     "logoUrl": "https://a.espncdn.com/i/teamlogos/ncaa/500/61.png"},
    {"rank": 3, "name": "First Last", "college": "Alabama",  "score": 77, "barColor": "#00b050",
     "logoUrl": "https://a.espncdn.com/i/teamlogos/ncaa/500/333.png"},
    {"rank": 4, "name": "First Last", "college": "Michigan", "score": 66, "barColor": "#ffc000",
     "logoUrl": "https://a.espncdn.com/i/teamlogos/ncaa/500/130.png"},
    {"rank": 5, "name": "First Last", "college": "Texas",    "score": 55, "barColor": "#c00000",
     "logoUrl": "https://a.espncdn.com/i/teamlogos/ncaa/500/251.png"},
]

def download_and_encode(url, size=40):
    """Download image, resize, return base64 data URI."""
    print(f"  Downloading: {url}")
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    if HAS_PIL:
        img = Image.open(BytesIO(resp.content))
        img = img.convert('RGBA')
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        buf = BytesIO()
        img.save(buf, format='PNG', optimize=True)
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode('utf-8')
    else:
        b64 = base64.b64encode(resp.content).decode('utf-8')

    return f"data:image/png;base64,{b64}"

def build_html(players):
    """Build the complete HTML test file."""
    # Build JS player array
    js_players = []
    for p in players:
        js_players.append(
            '      {{ rank: {rank}, name: "{name}", college: "{college}", score: {score}, '
            'barColor: "{barColor}", logo: "{logo}" }}'.format(**p)
        )
    js_array = "[\n" + ",\n".join(js_players) + "\n    ]"

    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Top Edge Athleticism Scores - 2026 NFL Combine</title>
  <script src="../CapSpace/working/highcharts.js"></script>
  <script src="highcharts-more.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800;900&display=swap" rel="stylesheet">
  <style>
    body {{ background: #2a2a3e; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
    #container {{ width: 820px; }}
  </style>
</head>
<body>
  <div id="container"></div>
  <script>
    var players = {js_array};

    var rowData = players.map(function(p, i) {{
      return {{
        x: 50,
        y: 20 + i * 15,
        rank: p.rank,
        playerName: p.name,
        score: p.score,
        barColor: p.barColor,
        barWidth: p.score - 50,
        logo: p.logo
      }};
    }});

    // Bubble series for logos - positioned at each row's logo spot
    var logoData = players.map(function(p, i) {{
      return {{
        x: 7.5,
        y: 20 + i * 15,
        z: 10,
        name: p.college,
        marker: {{
          symbol: 'url(' + p.logo + ')'
        }}
      }};
    }});

    Highcharts.chart('container', {{
      chart: {{
        type: 'scatter',
        backgroundColor: '#1a1a2e',
        height: 520,
        spacing: [15, 20, 15, 20],
        style: {{ fontFamily: "'Barlow Condensed', sans-serif" }},
        animation: false
      }},
      title: {{ text: null }},
      legend: {{ enabled: false }},
      credits: {{ enabled: false }},
      xAxis: {{ min: 0, max: 100, visible: false }},
      yAxis: {{ min: 0, max: 100, visible: false, reversed: true }},
      tooltip: {{ enabled: false }},
      plotOptions: {{
        scatter: {{ marker: {{ enabled: false }}, enableMouseTracking: false }},
        bubble: {{
          minSize: 44,
          maxSize: 44,
          enableMouseTracking: false
        }}
      }},
      series: [
        {{
          name: 'Title',
          type: 'scatter',
          data: [{{ x: 0, y: 2 }}],
          dataLabels: {{
            enabled: true, useHTML: true,
            formatter: function() {{
              return '<div>'
                + '<div style="font-size:28px;font-weight:900;color:#ffffff;letter-spacing:1px;text-transform:uppercase;">Top Edge Athleticism Scores</div>'
                + '<div style="font-size:16px;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:0.5px;margin-top:2px;">2026 NFL Combine</div>'
                + '</div>';
            }},
            align: 'left', verticalAlign: 'top',
            style: {{ textOutline: 'none' }}
          }}
        }},
        {{
          name: 'DraftBadge',
          type: 'scatter',
          data: [{{ x: 95, y: 3 }}],
          dataLabels: {{
            enabled: true, useHTML: true,
            formatter: function() {{
              return '<div style="background:#1a2744;border:2px solid #c9b037;border-radius:8px;padding:6px 10px;text-align:center;">'
                + '<div style="font-size:9px;font-weight:800;color:#c9b037;letter-spacing:2px;">NFL</div>'
                + '<div style="font-size:13px;font-weight:900;color:#ffffff;letter-spacing:1px;">DRAFT</div>'
                + '</div>';
            }},
            align: 'center', verticalAlign: 'top',
            style: {{ textOutline: 'none' }}
          }}
        }},
        {{
          name: 'CollegeLogos',
          type: 'bubble',
          data: logoData,
          dataLabels: {{ enabled: false }}
        }},
        {{
          name: 'Rows',
          type: 'scatter',
          data: rowData,
          dataLabels: {{
            enabled: true, useHTML: true,
            formatter: function() {{
              var p = this.point;
              return '<div style="display:flex;align-items:center;width:580px;height:56px;">'
                + '<div style="width:30px;font-size:22px;font-weight:700;color:#888;text-align:center;">' + p.rank + '</div>'
                + '<div style="width:60px;"></div>'
                + '<div style="width:160px;"><span style="font-size:18px;font-weight:600;color:#ffffff;">First </span><span style="font-size:18px;font-weight:800;color:#ffffff;">Last</span></div>'
                + '<div style="flex:1;position:relative;height:28px;background:rgba(255,255,255,0.06);border-radius:14px;overflow:visible;">'
                + '<div style="position:absolute;left:0;top:0;height:100%;width:' + p.barWidth + '%;background:linear-gradient(90deg,' + p.barColor + '22,' + p.barColor + ');border-radius:14px;"></div>'
                + '<div style="position:absolute;top:50%;transform:translateY(-50%);left:' + p.barWidth + '%;margin-left:-20px;width:40px;height:40px;border-radius:50%;background:' + p.barColor + ';display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:800;color:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.4);">' + p.score + '</div>'
                + '</div>'
                + '</div>';
            }},
            align: 'left', verticalAlign: 'middle',
            overflow: 'allow', crop: false,
            style: {{ textOutline: 'none' }}
          }}
        }},
        {{
          name: 'Dividers',
          type: 'scatter',
          data: [
            {{ x: 5, y: 28 }}, {{ x: 5, y: 43 }}, {{ x: 5, y: 58 }}, {{ x: 5, y: 73 }}
          ],
          dataLabels: {{
            enabled: true, useHTML: true,
            formatter: function() {{
              return '<div style="width:680px;height:1px;background:rgba(255,255,255,0.08);margin-left:30px;"></div>';
            }},
            align: 'left', verticalAlign: 'middle',
            style: {{ textOutline: 'none' }}
          }}
        }},
        {{
          name: 'NGSLogo',
          type: 'scatter',
          data: [{{ x: 8, y: 95 }}],
          dataLabels: {{
            enabled: true, useHTML: true,
            formatter: function() {{
              return '<div style="position:relative;width:110px;height:45px;">'
                + '<div style="position:absolute;top:0;left:0;width:0;height:0;border-bottom:45px solid #4CAF50;border-right:45px solid transparent;opacity:0.8;"></div>'
                + '<div style="position:absolute;top:6px;left:4px;color:#fff;line-height:1.2;">'
                + '<div style="font-size:8px;font-weight:700;letter-spacing:1px;font-style:italic;">NEXT GEN</div>'
                + '<div style="font-size:13px;font-weight:900;letter-spacing:2px;">STATS</div>'
                + '</div></div>';
            }},
            align: 'left', verticalAlign: 'bottom',
            style: {{ textOutline: 'none' }}
          }}
        }},
        {{
          name: 'LegendBar',
          type: 'scatter',
          data: [{{ x: 58, y: 94 }}],
          dataLabels: {{
            enabled: true, useHTML: true,
            formatter: function() {{
              return '<div style="text-align:center;">'
                + '<div style="width:280px;height:8px;border-radius:4px;background:linear-gradient(90deg,#c00000 0%,#ffc000 25%,#00b050 55%,#0077c8 100%);"></div>'
                + '<div style="display:flex;justify-content:space-between;width:280px;margin-top:3px;">'
                + '<span style="font-size:10px;color:#666;">50</span>'
                + '<span style="font-size:10px;color:#666;">60</span>'
                + '<span style="font-size:10px;color:#666;">75</span>'
                + '<span style="font-size:10px;color:#666;">90</span>'
                + '<span style="font-size:10px;color:#666;">100</span>'
                + '</div>'
                + '<div style="display:flex;justify-content:space-between;width:280px;margin-top:1px;">'
                + '<span style="font-size:9px;color:#555;text-transform:uppercase;letter-spacing:0.5px;">< AVG</span>'
                + '<span style="font-size:9px;color:#555;text-transform:uppercase;letter-spacing:0.5px;">AVERAGE</span>'
                + '<span style="font-size:9px;color:#555;text-transform:uppercase;letter-spacing:0.5px;">GOOD</span>'
                + '<span style="font-size:9px;color:#555;text-transform:uppercase;letter-spacing:0.5px;">ELITE</span>'
                + '</div></div>';
            }},
            align: 'center', verticalAlign: 'bottom',
            style: {{ textOutline: 'none' }}
          }}
        }}
      ]
    }});
  </script>
</body>
</html>'''.format(js_array=js_array)


def main():
    print("Generating test-combine-athleticism.html with base64 college logos...")
    print()

    # Download and encode each logo
    for p in COLLEGES:
        try:
            p['logo'] = download_and_encode(p['logoUrl'], size=40)
            print(f"  ✓ {p['college']}: {len(p['logo'])} chars")
        except Exception as e:
            print(f"  ✗ {p['college']}: {e}")
            # Fallback: 1px colored placeholder
            p['logo'] = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

    print()

    # Generate HTML
    html = build_html(COLLEGES)

    with open('test-combine-athleticism.html', 'w') as f:
        f.write(html)

    print(f"✓ Generated test-combine-athleticism.html ({len(html)} chars)")
    print("  Open in browser to preview.")


if __name__ == "__main__":
    main()
