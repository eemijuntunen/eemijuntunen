"""Solar system — repos as unique planets with full space features."""
import math, random
from shared import get_repos, fmt, now_str, starfield, COLORS

random.seed(42)

LANG_COLORS = {"Java": "#f89820", "TypeScript": "#3178c6", "Python": "#3572A5",
               "Kotlin": "#A97BFF", "Shell": "#89e051", "Go": "#00ADD8"}

def circle_path(cx, cy, r):
    return f"M{cx + r},{cy} A{r},{r} 0 1,1 {cx - r},{cy} A{r},{r} 0 1,1 {cx + r},{cy}"

def planet_style(i, pr, color):
    s = ""
    if i == 0:
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        for band_y in [-pr*0.5, -pr*0.15, pr*0.2, pr*0.55]:
            bw = math.sqrt(max(0, pr**2 - band_y**2)) * 2
            s += f'<rect x="{-bw/2:.0f}" y="{band_y-1.5:.0f}" width="{bw:.0f}" height="3" rx="1.5" fill="#fff" opacity="0.08"/>'
    elif i == 1:
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        s += f'<ellipse cx="0" cy="0" rx="{pr*1.8:.0f}" ry="{pr*0.35:.0f}" fill="none" stroke="{color}" stroke-width="2.5" opacity="0.4"/>'
        s += f'<ellipse cx="0" cy="0" rx="{pr*2.0:.0f}" ry="{pr*0.4:.0f}" fill="none" stroke="{color}" stroke-width="1" opacity="0.2"/>'
    elif i == 2:
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        for cx_, cy_, cr in [(-pr*0.3,-pr*0.2,pr*0.18),(pr*0.25,pr*0.15,pr*0.12),(-pr*0.1,pr*0.35,pr*0.1),(pr*0.35,-pr*0.3,pr*0.08)]:
            s += f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="{cr:.1f}" fill="#000" opacity="0.15"/>'
    elif i == 3:
        s += f'<circle cx="0" cy="0" r="{pr+6}" fill="{color}" opacity="0.1"><animate attributeName="r" values="{pr+4};{pr+10};{pr+4}" dur="2s" repeatCount="indefinite"/></circle>'
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.9" filter="url(#glow)"/>'
    elif i == 4:
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.75" filter="url(#glow)"/>'
        for a in range(0, 360, 60):
            rad = math.radians(a)
            s += f'<line x1="{pr*0.4*math.cos(rad):.1f}" y1="{pr*0.4*math.sin(rad):.1f}" x2="{pr*0.85*math.cos(rad+0.3):.1f}" y2="{pr*0.85*math.sin(rad+0.3):.1f}" stroke="#fff" stroke-width="0.5" opacity="0.2"/>'
    elif i == 5:
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        for x1,y1,x2,y2 in [(-pr*0.4,-pr*0.3,pr*0.1,pr*0.4),(pr*0.1,-pr*0.5,pr*0.3,pr*0.2),(-pr*0.2,pr*0.1,pr*0.4,pr*0.45)]:
            s += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#ffe066" stroke-width="1" opacity="0.4" stroke-linecap="round"/>'
    elif i == 6:
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        mo = pr + 8
        s += f'<circle r="{pr*0.25:.0f}" fill="#c0d0e0" opacity="0.7"><animateMotion dur="6s" repeatCount="indefinite" rotate="0" path="{circle_path(0,0,mo)}"/></circle>'
    elif i == 7:
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.8" filter="url(#glow)"/>'
        pts = " ".join(f"{pr*0.7*math.cos(math.radians(a)):.1f},{pr*0.7*math.sin(math.radians(a)):.1f}" for a in range(0,360,60))
        s += f'<polygon points="{pts}" fill="none" stroke="#fff" stroke-width="0.8" opacity="0.2"/>'
    elif i == 8:
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        s += f'<ellipse cx="{pr*0.2}" cy="{-pr*0.1}" rx="{pr*0.35}" ry="{pr*0.2}" fill="#fff" opacity="0.1"><animateTransform attributeName="transform" type="rotate" from="0 {pr*0.2} {-pr*0.1}" to="360 {pr*0.2} {-pr*0.1}" dur="8s" repeatCount="indefinite"/></ellipse>'
    else:
        s += f'<circle cx="0" cy="0" r="{pr+3}" fill="{color}" opacity="0.12"/>'
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
    s += f'<circle cx="{-pr*0.25:.0f}" cy="{-pr*0.25:.0f}" r="{pr*0.3:.0f}" fill="#fff" opacity="0.1"/>'
    return s

# ── NEW FEATURES ──

def shooting_stars(w, h, count=5):
    s = ""
    for i in range(count):
        x1 = random.uniform(50, w - 50)
        y1 = random.uniform(20, h * 0.4)
        length = random.uniform(60, 140)
        angle = random.uniform(0.3, 0.8)  # shallow angle
        x2 = x1 + length * math.cos(angle)
        y2 = y1 + length * math.sin(angle)
        delay = random.uniform(0, 12)
        dur = random.uniform(0.6, 1.2)
        period = dur + random.uniform(6, 14)  # time between appearances

        s += f'''<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="url(#shootingStar)" stroke-width="1.5" stroke-linecap="round" opacity="0">
  <animate attributeName="opacity" values="0;0;0.8;0" keyTimes="0;{0.7};{0.85};1" dur="{period:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>
</line>
<circle cx="{x2:.0f}" cy="{y2:.0f}" r="2" fill="#fff" opacity="0">
  <animate attributeName="opacity" values="0;0;1;0" keyTimes="0;{0.7};{0.85};1" dur="{period:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>
</circle>\n'''
    return s

def asteroid_belt(cx, cy, inner_r, outer_r, count=60):
    s = ""
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(inner_r, outer_r)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        size = random.uniform(0.5, 2.0)
        opacity = random.uniform(0.15, 0.4)
        dur = random.uniform(80, 200)
        # Slowly orbit
        s += f'''<circle cx="{x:.0f}" cy="{y:.0f}" r="{size:.1f}" fill="#8899aa" opacity="{opacity:.2f}">
  <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{dur:.0f}s" repeatCount="indefinite"/>
</circle>\n'''
    return s

def comet_trails(cx, cy, w, h, count=3):
    s = ""
    for i in range(count):
        # Elliptical comet path across the scene
        rx = random.uniform(200, 340)
        ry = random.uniform(120, 220)
        dur = random.uniform(18, 35)
        delay = random.uniform(0, 15)
        color = random.choice(["#00e5a0", "#00b4d8", "#ffbe0b"])
        path = f"M{cx+rx},{cy} A{rx},{ry} 0 1,1 {cx-rx},{cy} A{rx},{ry} 0 1,1 {cx+rx},{cy}"

        # Comet head
        s += f'''<g opacity="0.7">
  <animateMotion dur="{dur:.0f}s" begin="-{delay:.1f}s" repeatCount="indefinite" rotate="auto" path="{path}"/>
  <circle cx="0" cy="0" r="2.5" fill="{color}" filter="url(#glow)"/>
  <line x1="0" y1="0" x2="-18" y2="0" stroke="{color}" stroke-width="2" opacity="0.5" stroke-linecap="round"/>
  <line x1="0" y1="0" x2="-35" y2="0" stroke="{color}" stroke-width="1" opacity="0.2" stroke-linecap="round"/>
  <line x1="0" y1="0" x2="-50" y2="0" stroke="{color}" stroke-width="0.5" opacity="0.08"/>
</g>\n'''
    return s

def constellation_lines(repos, cx, cy, orbit_base=80, orbit_step=28):
    """Connect planets that share the same language with faint lines."""
    s = ""
    # Group repos by language
    lang_groups = {}
    for i, r in enumerate(repos):
        lang = r.get("language", "")
        if lang:
            lang_groups.setdefault(lang, []).append(i)

    # For each language with 2+ repos, draw connecting lines
    for lang, indices in lang_groups.items():
        if len(indices) < 2:
            continue
        color = LANG_COLORS.get(lang, "#555")
        # We can't know exact positions (they animate), so draw faint orbit-to-orbit arcs
        for j in range(len(indices) - 1):
            i1, i2 = indices[j], indices[j + 1]
            r1 = orbit_base + i1 * orbit_step
            r2 = orbit_base + i2 * orbit_step
            # Static decorative arc between orbit rings
            a1 = random.uniform(0, 2 * math.pi)
            x1 = cx + r1 * math.cos(a1)
            y1 = cy + r1 * math.sin(a1)
            x2 = cx + r2 * math.cos(a1 + 0.3)
            y2 = cy + r2 * math.sin(a1 + 0.3)
            mx = (x1 + x2) / 2 + random.uniform(-20, 20)
            my = (y1 + y2) / 2 + random.uniform(-20, 20)
            s += f'<path d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" fill="none" stroke="{color}" stroke-width="0.5" opacity="0.12" stroke-dasharray="4,4"/>\n'
    return s

def satellite_swarm(cx, cy, r, count=20):
    s = ""
    for i in range(count):
        angle = random.uniform(0, 2 * math.pi)
        offset = random.uniform(-6, 6)
        dur = random.uniform(8, 18)
        delay = random.uniform(0, dur)
        path = circle_path(cx, cy, r + offset)
        s += f'''<circle r="0.8" fill="#ffe066" opacity="0.4">
  <animateMotion dur="{dur:.1f}s" begin="-{delay:.1f}s" repeatCount="indefinite" rotate="0" path="{path}"/>
</circle>\n'''
    return s

def wormhole_portal(x, y, link_url):
    s = f'<a href="{link_url}" target="_blank">\n'
    # Swirling rings
    for j in range(4):
        r = 18 - j * 3
        dur = 3 + j * 0.5
        opacity = 0.15 + j * 0.05
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#8338ec" stroke-width="1.5" opacity="{opacity}">'
        s += f'<animateTransform attributeName="transform" type="rotate" from="0 {x} {y}" to="{"360" if j%2==0 else "-360"} {x} {y}" dur="{dur:.1f}s" repeatCount="indefinite"/>'
        s += f'<animate attributeName="r" values="{r};{r+2};{r}" dur="{dur+1:.1f}s" repeatCount="indefinite"/>'
        s += f'</circle>\n'
    # Core glow
    s += f'<circle cx="{x}" cy="{y}" r="6" fill="#8338ec" opacity="0.3" filter="url(#glow)">'
    s += f'<animate attributeName="r" values="4;8;4" dur="2s" repeatCount="indefinite"/></circle>'
    s += f'<circle cx="{x}" cy="{y}" r="3" fill="#c0a0ff" opacity="0.5"/>'
    # Label
    s += f'<text x="{x}" y="{y + 28}" text-anchor="middle" fill="#8338ec" font-size="7" opacity="0.6">explore ↗</text>'
    s += f'</a>\n'
    return s

def hover_cards(repos, pr_list, color_list):
    """CSS hover styles for planet tooltips."""
    css = "<style>\n"
    css += ".planet-group .hover-card { opacity: 0; transition: opacity 0.3s; pointer-events: none; }\n"
    css += ".planet-group:hover .hover-card { opacity: 1; }\n"
    css += ".planet-group { cursor: pointer; }\n"
    css += "</style>\n"
    return css

def hover_card_svg(repo, pr, color):
    """Tooltip card drawn at local origin, shown on hover."""
    cw, ch = 130, 58
    x, y = -cw/2, -pr - ch - 20
    lang = repo.get("language", "?")
    forks = repo.get("forks_count", 0)
    issues = repo["open_issues_count"]
    s = f'<g class="hover-card">'
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw}" height="{ch}" rx="8" fill="#0a1628" stroke="{color}" stroke-width="0.8" opacity="0.95"/>'
    s += f'<text x="0" y="{y+16:.0f}" text-anchor="middle" fill="#e0f0ff" font-size="8" font-weight="bold">{repo["name"][:20]}</text>'
    s += f'<text x="0" y="{y+30:.0f}" text-anchor="middle" fill="#5a7a9a" font-size="7">{lang} · {issues} issues · {forks} forks</text>'
    pushed = repo.get("pushed_at", "")[:10]
    s += f'<text x="0" y="{y+43:.0f}" text-anchor="middle" fill="#3a5a7a" font-size="7">last push: {pushed}</text>'
    s += f'</g>'
    return s

# ── MAIN GENERATE ──

def generate(repos):
    w, h = 720, 720
    cx, cy = w // 2, h // 2
    max_stars = max(r["stargazers_count"] for r in repos) or 1

    defs = '''<defs>
    <radialGradient id="sun" cx="45%" cy="40%">
      <stop offset="0%" stop-color="#ffe066"/><stop offset="40%" stop-color="#ff9f1c"/>
      <stop offset="100%" stop-color="#e63946"/>
    </radialGradient>
    <linearGradient id="shootingStar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#fff" stop-opacity="0"/>
      <stop offset="100%" stop-color="#fff" stop-opacity="1"/>
    </linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="sunGlow"><feGaussianBlur stdDeviation="12" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="nebula"><feGaussianBlur stdDeviation="50"/></filter>
  </defs>'''

    # Hover CSS
    css = hover_cards(repos, [], [])

    bg = f'<rect width="{w}" height="{h}" rx="16" fill="#03060d"/>'
    bg += starfield(w, h, 140)
    bg += f'<circle cx="{cx+100}" cy="{cy-80}" r="200" fill="#8338ec" opacity="0.02" filter="url(#nebula)"/>'
    bg += f'<circle cx="{cx-120}" cy="{cy+100}" r="160" fill="#00b4d8" opacity="0.025" filter="url(#nebula)"/>'

    # Shooting stars
    bg += shooting_stars(w, h, 5)

    # Constellation lines (behind everything)
    constellations = constellation_lines(repos, cx, cy)

    # Asteroid belt between orbit 4 and 5 (index-based)
    belt_inner = 80 + 4 * 28 - 8
    belt_outer = 80 + 4 * 28 + 8
    belt = asteroid_belt(cx, cy, belt_inner, belt_outer, 50)

    # Satellite swarm close to sun
    satellites = satellite_swarm(cx, cy, 58, 20)

    # Comet trails
    comets = comet_trails(cx, cy, w, h, 3)

    # Sun
    sun = (f'<circle cx="{cx}" cy="{cy}" r="50" fill="#ff9f1c" opacity="0.08" filter="url(#sunGlow)"/>'
           f'<circle cx="{cx}" cy="{cy}" r="36" fill="url(#sun)" filter="url(#glow)">'
           f'<animate attributeName="r" values="36;38;36" dur="3s" repeatCount="indefinite"/></circle>'
           f'<text x="{cx}" y="{cy-4}" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">OpenSearch</text>'
           f'<text x="{cx}" y="{cy+10}" text-anchor="middle" fill="#ffe066" font-size="7" letter-spacing="2">PROJECT</text>')

    orbits = ""
    planets = ""
    for i, r in enumerate(repos):
        orbit_r = 80 + i * 28
        ratio = r["stargazers_count"] / max_stars
        pr = 8 + ratio * 16
        color = LANG_COLORS.get(r.get("language", ""), COLORS[i % len(COLORS)])
        dur = 40 + i * 15
        begin = random.uniform(0, dur)
        path = circle_path(cx, cy, orbit_r)

        orbits += f'<circle cx="{cx}" cy="{cy}" r="{orbit_r}" fill="none" stroke="#1a2a44" stroke-width="0.5" opacity="0.3"/>\n'

        psv = planet_style(i, pr, color)
        hcard = hover_card_svg(r, pr, color)

        planets += f'''<g class="planet-group">
  <animateMotion dur="{dur}s" repeatCount="indefinite" begin="-{begin:.1f}s" rotate="0" path="{path}"/>
  {psv}
  <text x="0" y="{pr+16}" text-anchor="middle" fill="#a0b8d0" font-size="8" font-weight="600">{r["name"][:18]}</text>
  <text x="0" y="{pr+27}" text-anchor="middle" fill="{color}" font-size="8" font-weight="bold">&#9733; {fmt(r["stargazers_count"])}</text>
  {hcard}
</g>\n'''

    # Wormhole portal (bottom right)
    wormhole = wormhole_portal(w - 50, h - 60, "https://github.com/opensearch-project")

    title = (f'<text x="{cx}" y="30" text-anchor="middle" fill="#e0f0ff" font-size="17" font-weight="bold" letter-spacing="1">OpenSearch Solar System</text>'
             f'<text x="{cx}" y="48" text-anchor="middle" fill="#3a6a8a" font-size="10">Repos orbit by activity · Planet size = stars · Color = language · Hover for details</text>')

    ly = h - 40
    leg = ""
    used = {}
    for r in repos:
        lang = r.get("language", "")
        if lang and lang not in used:
            used[lang] = LANG_COLORS.get(lang, "#888")
    lx = 60
    for lang, c in list(used.items())[:6]:
        leg += f'<circle cx="{lx}" cy="{ly}" r="4" fill="{c}"/><text x="{lx+8}" y="{ly+3}" fill="#5a7a9a" font-size="8">{lang}</text>'
        lx += len(lang) * 6 + 30

    footer = f'<text x="{cx}" y="{h-12}" text-anchor="middle" fill="#1a2a3a" font-size="8">{now_str()}</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">
  {defs}{css}{bg}{title}{constellations}{belt}{orbits}{sun}{satellites}{comets}{planets}{wormhole}{leg}{footer}
</svg>'''

if __name__ == "__main__":
    repos = get_repos()
    with open("solar-system.svg", "w") as f:
        f.write(generate(repos))
    print("Generated solar-system.svg")
