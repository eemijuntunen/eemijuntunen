"""Solar system — repos as unique planets orbiting a central star."""
import math, random
from shared import get_repos, fmt, now_str, starfield, COLORS

random.seed(42)

LANG_COLORS = {"Java": "#f89820", "TypeScript": "#3178c6", "Python": "#3572A5",
               "Kotlin": "#A97BFF", "Shell": "#89e051", "Go": "#00ADD8"}

def circle_path(cx, cy, r):
    return f"M{cx + r},{cy} A{r},{r} 0 1,1 {cx - r},{cy} A{r},{r} 0 1,1 {cx + r},{cy}"

def planet_style(i, pr, color):
    """Return unique SVG elements for each planet index, drawn at origin (0,0)."""
    s = ""

    if i == 0:
        # Gas giant — horizontal bands + large glow
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        for band_y in [-pr*0.5, -pr*0.15, pr*0.2, pr*0.55]:
            bw = math.sqrt(max(0, pr**2 - band_y**2)) * 2
            s += f'<rect x="{-bw/2:.0f}" y="{band_y - 1.5:.0f}" width="{bw:.0f}" height="3" rx="1.5" fill="#fff" opacity="0.08"/>'
        s += f'<circle cx="0" cy="0" r="{pr}" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.15"/>'

    elif i == 1:
        # Ringed planet (Saturn style)
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        s += f'<ellipse cx="0" cy="0" rx="{pr*1.8:.0f}" ry="{pr*0.35:.0f}" fill="none" stroke="{color}" stroke-width="2.5" opacity="0.4"/>'
        s += f'<ellipse cx="0" cy="0" rx="{pr*2.0:.0f}" ry="{pr*0.4:.0f}" fill="none" stroke="{color}" stroke-width="1" opacity="0.2"/>'

    elif i == 2:
        # Cratered moon style — spots on surface
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        for cx_, cy_, cr in [(-pr*0.3, -pr*0.2, pr*0.18), (pr*0.25, pr*0.15, pr*0.12), (-pr*0.1, pr*0.35, pr*0.1), (pr*0.35, -pr*0.3, pr*0.08)]:
            s += f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="{cr:.1f}" fill="#000" opacity="0.15"/>'
            s += f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="{cr*0.7:.1f}" fill="#fff" opacity="0.05"/>'

    elif i == 3:
        # Glowing energy planet — double halo pulse
        s += f'<circle cx="0" cy="0" r="{pr+6}" fill="{color}" opacity="0.1">'
        s += f'<animate attributeName="r" values="{pr+4};{pr+10};{pr+4}" dur="2s" repeatCount="indefinite"/></circle>'
        s += f'<circle cx="0" cy="0" r="{pr+3}" fill="none" stroke="{color}" stroke-width="1" opacity="0.3">'
        s += f'<animate attributeName="r" values="{pr+2};{pr+6};{pr+2}" dur="3s" repeatCount="indefinite"/></circle>'
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.9" filter="url(#glow)"/>'

    elif i == 4:
        # Ice planet — crystalline facets
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.75" filter="url(#glow)"/>'
        for a in range(0, 360, 60):
            rad = math.radians(a)
            x1 = pr * 0.4 * math.cos(rad)
            y1 = pr * 0.4 * math.sin(rad)
            x2 = pr * 0.85 * math.cos(rad + 0.3)
            y2 = pr * 0.85 * math.sin(rad + 0.3)
            s += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#fff" stroke-width="0.5" opacity="0.2"/>'
        s += f'<circle cx="0" cy="0" r="{pr}" fill="none" stroke="#fff" stroke-width="0.8" opacity="0.25"/>'

    elif i == 5:
        # Lava planet — glowing cracks
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        cracks = [(-pr*0.4, -pr*0.3, pr*0.1, pr*0.4), (pr*0.1, -pr*0.5, pr*0.3, pr*0.2),
                  (-pr*0.2, pr*0.1, pr*0.4, pr*0.45), (pr*0.2, -pr*0.1, -pr*0.1, pr*0.3)]
        for x1, y1, x2, y2 in cracks:
            s += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#ffe066" stroke-width="1" opacity="0.4" stroke-linecap="round"/>'
        s += f'<circle cx="0" cy="0" r="{pr*0.92}" fill="none" stroke="#ff6b35" stroke-width="0.8" opacity="0.3"/>'

    elif i == 6:
        # Planet with moon
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        moon_r = pr * 0.25
        moon_orbit = pr + 8
        s += f'<circle cx="0" cy="0" r="{moon_orbit}" fill="none" stroke="#fff" stroke-width="0.3" opacity="0.15"/>'
        s += f'<circle r="{moon_r:.0f}" fill="#c0d0e0" opacity="0.7">'
        s += f'<animateMotion dur="6s" repeatCount="indefinite" rotate="0" path="{circle_path(0, 0, moon_orbit)}"/>'
        s += f'</circle>'

    elif i == 7:
        # Hexagon planet (crystalline)
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.8" filter="url(#glow)"/>'
        pts = " ".join(f"{pr*0.7*math.cos(math.radians(a)):.1f},{pr*0.7*math.sin(math.radians(a)):.1f}" for a in range(0, 360, 60))
        s += f'<polygon points="{pts}" fill="none" stroke="#fff" stroke-width="0.8" opacity="0.2"/>'
        pts2 = " ".join(f"{pr*0.4*math.cos(math.radians(a+30)):.1f},{pr*0.4*math.sin(math.radians(a+30)):.1f}" for a in range(0, 360, 60))
        s += f'<polygon points="{pts2}" fill="none" stroke="#fff" stroke-width="0.5" opacity="0.12"/>'

    elif i == 8:
        # Storm planet — swirling spot
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        s += f'<ellipse cx="{pr*0.2}" cy="{-pr*0.1}" rx="{pr*0.35}" ry="{pr*0.2}" fill="#fff" opacity="0.1">'
        s += f'<animateTransform attributeName="transform" type="rotate" from="0 {pr*0.2} {-pr*0.1}" to="360 {pr*0.2} {-pr*0.1}" dur="8s" repeatCount="indefinite"/>'
        s += f'</ellipse>'
        s += f'<ellipse cx="{-pr*0.15}" cy="{pr*0.25}" rx="{pr*0.2}" ry="{pr*0.12}" fill="#000" opacity="0.12"/>'

    else:
        # Gradient planet with atmosphere
        s += f'<circle cx="0" cy="0" r="{pr+3}" fill="{color}" opacity="0.12"/>'
        s += f'<circle cx="0" cy="0" r="{pr}" fill="{color}" opacity="0.85" filter="url(#glow)"/>'
        s += f'<circle cx="0" cy="0" r="{pr}" fill="none" stroke="#fff" stroke-width="1" opacity="0.1"/>'

    # Universal highlight
    s += f'<circle cx="{-pr*0.25:.0f}" cy="{-pr*0.25:.0f}" r="{pr*0.3:.0f}" fill="#fff" opacity="0.1"/>'
    return s

def generate(repos):
    w, h = 720, 720
    cx, cy = w // 2, h // 2
    max_stars = max(r["stargazers_count"] for r in repos) or 1

    defs = '''<defs>
    <radialGradient id="sun" cx="45%" cy="40%">
      <stop offset="0%" stop-color="#ffe066"/><stop offset="40%" stop-color="#ff9f1c"/>
      <stop offset="100%" stop-color="#e63946"/>
    </radialGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="sunGlow"><feGaussianBlur stdDeviation="12" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="nebula"><feGaussianBlur stdDeviation="50"/></filter>
  </defs>'''

    bg = f'<rect width="{w}" height="{h}" rx="16" fill="#03060d"/>'
    bg += starfield(w, h, 140)
    bg += f'<circle cx="{cx+100}" cy="{cy-80}" r="200" fill="#8338ec" opacity="0.02" filter="url(#nebula)"/>'
    bg += f'<circle cx="{cx-120}" cy="{cy+100}" r="160" fill="#00b4d8" opacity="0.025" filter="url(#nebula)"/>'

    sun = (f'<circle cx="{cx}" cy="{cy}" r="50" fill="#ff9f1c" opacity="0.08" filter="url(#sunGlow)"/>'
           f'<circle cx="{cx}" cy="{cy}" r="36" fill="url(#sun)" filter="url(#glow)">'
           f'<animate attributeName="r" values="36;38;36" dur="3s" repeatCount="indefinite"/></circle>'
           f'<text x="{cx}" y="{cy-4}" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">OpenSearch</text>'
           f'<text x="{cx}" y="{cy+10}" text-anchor="middle" fill="#ffe066" font-size="7" letter-spacing="2">PROJECT</text>')

    orbits = ""
    planets = ""
    n = len(repos)
    for i, r in enumerate(repos):
        orbit_r = 80 + i * 28
        ratio = r["stargazers_count"] / max_stars
        pr = 8 + ratio * 16
        color = LANG_COLORS.get(r.get("language", ""), COLORS[i % len(COLORS)])
        dur = 40 + i * 15
        begin = random.uniform(0, dur)
        path = circle_path(cx, cy, orbit_r)

        orbits += f'<circle cx="{cx}" cy="{cy}" r="{orbit_r}" fill="none" stroke="#1a2a44" stroke-width="0.5" opacity="0.3"/>\n'

        planet_svg = planet_style(i, pr, color)

        planets += f'''<g>
  <animateMotion dur="{dur}s" repeatCount="indefinite" begin="-{begin:.1f}s" rotate="0" path="{path}"/>
  {planet_svg}
  <text x="0" y="{pr + 16}" text-anchor="middle" fill="#a0b8d0" font-size="8" font-weight="600">{r["name"][:18]}</text>
  <text x="0" y="{pr + 27}" text-anchor="middle" fill="{color}" font-size="8" font-weight="bold">&#9733; {fmt(r["stargazers_count"])}</text>
</g>\n'''

    title = (f'<text x="{cx}" y="30" text-anchor="middle" fill="#e0f0ff" font-size="17" font-weight="bold" letter-spacing="1">OpenSearch Solar System</text>'
             f'<text x="{cx}" y="48" text-anchor="middle" fill="#3a6a8a" font-size="10">Repos orbit by activity · Planet size = stars · Color = language</text>')

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
  {defs}{bg}{title}{orbits}{sun}{planets}{leg}{footer}
</svg>'''

if __name__ == "__main__":
    repos = get_repos()
    with open("solar-system.svg", "w") as f:
        f.write(generate(repos))
    print("Generated solar-system.svg")
