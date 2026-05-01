import json
import urllib.request
import datetime
import math
import random

random.seed(42)  # deterministic "stars"

import os, hashlib

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")

def fetch_json(url):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, hashlib.md5(url.encode()).hexdigest() + ".json")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "opensearch-pulse"})
        with urllib.request.urlopen(req) as r:
            data = r.read()
        with open(cache_file, "wb") as f:
            f.write(data)
        return json.loads(data)
    except Exception as e:
        if os.path.exists(cache_file):
            print(f"  (using cache for {url.split('/')[-1]})")
            with open(cache_file) as f:
                return json.load(f)
        raise

def fmt(n):
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)

def days_ago(date_str):
    pushed = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return (datetime.datetime.now(datetime.timezone.utc) - pushed).days

def get_weekly_activity(repo_full):
    try:
        stats = fetch_json(f"https://api.github.com/repos/{repo_full}/stats/participation")
        weekly_commits = stats["all"][-1] if stats.get("all") else 0
    except Exception:
        weekly_commits = 0
    since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        items = fetch_json(f"https://api.github.com/repos/{repo_full}/issues?since={since}&state=all&per_page=100")
        recent_issues = sum(1 for i in items if "pull_request" not in i)
        recent_prs = sum(1 for i in items if "pull_request" in i)
    except Exception:
        recent_issues = recent_prs = 0
    return weekly_commits, recent_issues, recent_prs

COLORS = ["#00e5a0","#00b4d8","#8338ec","#ff006e","#fb5607","#ffbe0b","#3a86ff","#06d6a0","#ef476f","#118ab2"]

def arc_ring(cx, cy, r, val, max_val, color, width=3):
    """SVG arc showing a proportion of a circle."""
    if max_val == 0 or val == 0:
        return ""
    frac = min(val / max_val, 1.0)
    circum = 2 * math.pi * r
    dash = circum * frac
    gap = circum - dash
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" '
        f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
        f'stroke-dasharray="{dash:.1f} {gap:.1f}" '
        f'transform="rotate(-90 {cx:.1f} {cy:.1f})" opacity="0.8">'
        f'<animateTransform attributeName="transform" type="rotate" '
        f'from="-90 {cx:.1f} {cy:.1f}" to="270 {cx:.1f} {cy:.1f}" dur="20s" repeatCount="indefinite"/>'
        f'</circle>\n'
    )

def generate_svg(repos):
    w, h = 720, 640
    cx, cy = w // 2, 300
    now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%b %d, %Y %H:%M UTC")
    max_stars = max(r["stargazers_count"] for r in repos) or 1

    print("Fetching weekly activity...")
    bubbles = []
    for i, r in enumerate(repos):
        print(f"  {r['name']}...")
        try:
            commits, issues, prs = get_weekly_activity(f"opensearch-project/{r['name']}")
        except Exception:
            commits, issues, prs = random.randint(5,80), random.randint(2,40), random.randint(3,50)
        ratio = r["stargazers_count"] / max_stars
        bubbles.append({
            "name": r["name"], "stars": r["stargazers_count"],
            "radius": 20 + ratio * 24, "color": COLORS[i % len(COLORS)],
            "days": days_ago(r["pushed_at"]),
            "commits": commits, "issues": issues, "prs": prs,
        })

    max_c = max(b["commits"] for b in bubbles) or 1
    max_i = max(b["issues"] for b in bubbles) or 1
    max_p = max(b["prs"] for b in bubbles) or 1

    # Position: two staggered arcs
    n = len(bubbles)
    for i, b in enumerate(bubbles):
        angle = (2 * math.pi * i / n) - math.pi / 2
        rx, ry = 220, 175
        b["x"] = cx + rx * math.cos(angle)
        b["y"] = cy + ry * math.sin(angle)

    # --- Background starfield ---
    stars_svg = ""
    for _ in range(120):
        sx = random.uniform(0, w)
        sy = random.uniform(0, h)
        sr = random.uniform(0.3, 1.2)
        so = random.uniform(0.2, 0.6)
        dur = random.uniform(2, 6)
        stars_svg += (
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{sr:.1f}" fill="#fff" opacity="{so:.2f}">'
            f'<animate attributeName="opacity" values="{so:.2f};{so*0.3:.2f};{so:.2f}" dur="{dur:.1f}s" repeatCount="indefinite"/>'
            f'</circle>\n'
        )

    # --- Nebula blobs ---
    nebula = ""
    nebula_spots = [(cx-80, cy-40, 180, "#00b4d8"), (cx+100, cy+60, 140, "#8338ec"), (cx-20, cy+80, 120, "#00e5a0")]
    for nx, ny, nr, nc in nebula_spots:
        nebula += f'<circle cx="{nx}" cy="{ny}" r="{nr}" fill="{nc}" opacity="0.03" filter="url(#nebula)"/>\n'

    # --- Defs ---
    gradients = ""
    for i, b in enumerate(bubbles):
        c = b["color"]
        gradients += f'''<radialGradient id="bg{i}" cx="30%" cy="30%">
      <stop offset="0%" stop-color="{c}" stop-opacity="0.9"/>
      <stop offset="80%" stop-color="{c}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{c}" stop-opacity="0.2"/>
    </radialGradient>\n'''

    defs = f'''<defs>
    {gradients}
    <radialGradient id="centerOrb" cx="40%" cy="35%">
      <stop offset="0%" stop-color="#102a44"/><stop offset="100%" stop-color="#060e1a"/>
    </radialGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="bigGlow"><feGaussianBlur stdDeviation="8" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="nebula"><feGaussianBlur stdDeviation="40"/></filter>
  </defs>'''

    # --- Center ---
    center = f'''
    <circle cx="{cx}" cy="{cy}" r="90" fill="#00b4d8" opacity="0.04" filter="url(#bigGlow)"/>
    <circle cx="{cx}" cy="{cy}" r="44" fill="url(#centerOrb)" stroke="#00b4d8" stroke-width="1" filter="url(#glow)"/>
    <circle cx="{cx}" cy="{cy}" r="44" fill="none" stroke="#00e5ff" stroke-width="0.5" opacity="0.3">
      <animate attributeName="r" values="44;48;44" dur="4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.3;0.1;0.3" dur="4s" repeatCount="indefinite"/>
    </circle>
    <text x="{cx}" y="{cy-6}" text-anchor="middle" fill="#00e5ff" font-size="12" font-weight="bold" letter-spacing="1.5">OpenSearch</text>
    <text x="{cx}" y="{cy+12}" text-anchor="middle" fill="#3a6a8a" font-size="8" letter-spacing="3">ECOSYSTEM</text>'''

    # --- Connection arcs (curved lines from center to each node) ---
    conns = ""
    for b in bubbles:
        mx = (cx + b["x"]) / 2 + random.uniform(-30, 30)
        my = (cy + b["y"]) / 2 + random.uniform(-20, 20)
        conns += (
            f'<path d="M{cx},{cy} Q{mx:.0f},{my:.0f} {b["x"]:.0f},{b["y"]:.0f}" '
            f'fill="none" stroke="{b["color"]}" stroke-width="0.8" opacity="0.15"/>\n'
        )
        # Animated particle along path
        pid = f"p{id(b)}"
        conns += (
            f'<circle r="1.5" fill="{b["color"]}" opacity="0.6">'
            f'<animateMotion dur="{random.uniform(4,8):.1f}s" repeatCount="indefinite" '
            f'path="M{cx},{cy} Q{mx:.0f},{my:.0f} {b["x"]:.0f},{b["y"]:.0f}"/>'
            f'</circle>\n'
        )

    # --- Nodes ---
    nodes = ""
    for i, b in enumerate(bubbles):
        r = b["radius"]
        x, y = b["x"], b["y"]
        dur = max(2, 5 - b["days"] * 0.2)

        # Outer glow
        nodes += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r+10:.0f}" fill="{b["color"]}" opacity="0.06" filter="url(#glow)"/>\n'

        # Activity rings: commits (outer), PRs (mid), issues (inner)
        nodes += arc_ring(x, y, r + 8, b["commits"], max_c, "#00e5a0", 2.5)
        nodes += arc_ring(x, y, r + 12, b["prs"], max_p, "#3a86ff", 2)
        nodes += arc_ring(x, y, r + 16, b["issues"], max_i, "#ff6b6b", 1.5)

        # Main bubble
        nodes += (
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.0f}" fill="url(#bg{i})" filter="url(#glow)">'
            f'<animate attributeName="r" values="{r:.0f};{r+1.5:.1f};{r:.0f}" dur="{dur:.1f}s" repeatCount="indefinite"/>'
            f'</circle>\n'
        )

        # Inner highlight
        nodes += f'<circle cx="{x-r*0.25:.1f}" cy="{y-r*0.25:.1f}" r="{r*0.35:.1f}" fill="#fff" opacity="0.08"/>\n'

        # Star count
        nodes += f'<text x="{x:.1f}" y="{y+1:.1f}" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold" dominant-baseline="middle">&#9733; {fmt(b["stars"])}</text>\n'

        # Name
        name = b["name"][:22]
        nodes += f'<text x="{x:.1f}" y="{y + r + 28:.1f}" text-anchor="middle" fill="#8aa0b8" font-size="9" font-weight="600">{name}</text>\n'

        # Activity numbers below name — pill style
        pill_y = y + r + 42
        pill_w = 72
        nodes += (
            f'<rect x="{x - pill_w/2:.1f}" y="{pill_y - 9:.1f}" width="{pill_w}" height="14" rx="7" fill="#0d1a2a" stroke="#1a2a44" stroke-width="0.5"/>'
            f'<text x="{x:.1f}" y="{pill_y + 2:.1f}" text-anchor="middle" font-size="8.5" font-weight="bold">'
            f'<tspan fill="#00e5a0">{b["commits"]}</tspan>'
            f'<tspan fill="#3a5a6a" font-size="7"> c  </tspan>'
            f'<tspan fill="#ff6b6b">{b["issues"]}</tspan>'
            f'<tspan fill="#3a5a6a" font-size="7"> i  </tspan>'
            f'<tspan fill="#3a86ff">{b["prs"]}</tspan>'
            f'<tspan fill="#3a5a6a" font-size="7"> pr</tspan>'
            f'</text>\n'
        )

    # --- Title ---
    title = f'''
    <text x="{cx}" y="34" text-anchor="middle" fill="#e0f0ff" font-size="18" font-weight="bold" letter-spacing="1" filter="url(#glow)">OpenSearch Ecosystem Pulse</text>
    <text x="{cx}" y="54" text-anchor="middle" fill="#3a6a8a" font-size="10" letter-spacing="0.5">Live constellation of the most active repos · 7-day snapshot</text>'''

    # --- Legend ---
    ly = h - 48
    legend = f'''
    <text x="60" y="{ly}" fill="#5a7a9a" font-size="9" font-weight="bold">Activity rings:</text>
    <line x1="148" y1="{ly-4}" x2="168" y2="{ly-4}" stroke="#00e5a0" stroke-width="2.5" stroke-linecap="round"/>
    <text x="173" y="{ly}" fill="#5a7a9a" font-size="9">commits</text>
    <line x1="218" y1="{ly-4}" x2="238" y2="{ly-4}" stroke="#3a86ff" stroke-width="2" stroke-linecap="round"/>
    <text x="243" y="{ly}" fill="#5a7a9a" font-size="9">PRs</text>
    <line x1="268" y1="{ly-4}" x2="288" y2="{ly-4}" stroke="#ff6b6b" stroke-width="1.5" stroke-linecap="round"/>
    <text x="293" y="{ly}" fill="#5a7a9a" font-size="9">issues</text>
    <text x="345" y="{ly}" fill="#2a4a6a" font-size="9">·  ring fill = proportion of most active  ·  bubble = stars</text>'''

    footer = f'<text x="{cx}" y="{h-12}" text-anchor="middle" fill="#1a2a3a" font-size="8">Auto-updated every 6 hours  ·  {now_str}  ·  github.com/opensearch-project</text>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">
  {defs}
  <rect width="{w}" height="{h}" rx="16" fill="#04080f"/>
  {nebula}
  {stars_svg}
  {title}
  {conns}
  {center}
  {nodes}
  {legend}
  {footer}
</svg>'''
    return svg

def main():
    try:
        repos = fetch_json("https://api.github.com/orgs/opensearch-project/repos?sort=pushed&per_page=10")
    except Exception:
        print("Rate limited — using sample data for preview")
        repos = [
            {"name": "OpenSearch", "stargazers_count": 12800, "open_issues_count": 2800, "pushed_at": "2026-05-01T00:00:00Z"},
            {"name": "OpenSearch-Dashboards", "stargazers_count": 2049, "open_issues_count": 1570, "pushed_at": "2026-05-01T00:00:00Z"},
            {"name": "data-prepper", "stargazers_count": 366, "open_issues_count": 769, "pushed_at": "2026-05-01T00:00:00Z"},
            {"name": "opensearch-build", "stargazers_count": 199, "open_issues_count": 246, "pushed_at": "2026-04-30T00:00:00Z"},
            {"name": "neural-search", "stargazers_count": 114, "open_issues_count": 125, "pushed_at": "2026-05-01T00:00:00Z"},
            {"name": "index-management", "stargazers_count": 76, "open_issues_count": 191, "pushed_at": "2026-05-01T00:00:00Z"},
            {"name": "opensearch-migrations", "stargazers_count": 71, "open_issues_count": 88, "pushed_at": "2026-04-30T00:00:00Z"},
            {"name": "flow-framework", "stargazers_count": 55, "open_issues_count": 46, "pushed_at": "2026-05-01T00:00:00Z"},
            {"name": "opensearch-py", "stargazers_count": 462, "open_issues_count": 120, "pushed_at": "2026-04-28T00:00:00Z"},
            {"name": "opensearch-js", "stargazers_count": 229, "open_issues_count": 102, "pushed_at": "2026-04-29T00:00:00Z"},
        ]
    svg = generate_svg(repos)
    with open("opensearch-pulse.svg", "w") as f:
        f.write(svg)
    print("Done! opensearch-pulse.svg")

if __name__ == "__main__":
    main()
