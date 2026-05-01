"""Solar system — repos as planets orbiting a central star. Labels always upright."""
import math, random
from shared import get_repos, fmt, now_str, starfield, COLORS

random.seed(42)

LANG_COLORS = {"Java": "#f89820", "TypeScript": "#3178c6", "Python": "#3572A5",
               "Kotlin": "#A97BFF", "Shell": "#89e051", "Go": "#00ADD8"}

def circle_path(cx, cy, r):
    """SVG path describing a circle (for animateMotion)."""
    return f"M{cx + r},{cy} A{r},{r} 0 1,1 {cx - r},{cy} A{r},{r} 0 1,1 {cx + r},{cy}"

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
        begin = random.uniform(0, dur)  # stagger start positions
        path = circle_path(cx, cy, orbit_r)

        orbits += f'<circle cx="{cx}" cy="{cy}" r="{orbit_r}" fill="none" stroke="#1a2a44" stroke-width="0.5" opacity="0.3"/>\n'

        # Everything in one group that moves along the circular path
        # animateMotion with rotate="0" keeps orientation fixed (upright)
        planets += f'''<g>
  <animateMotion dur="{dur}s" repeatCount="indefinite" begin="-{begin:.1f}s" rotate="0" path="{path}"/>
  <circle cx="0" cy="0" r="{pr+4:.0f}" fill="{color}" opacity="0.08" filter="url(#glow)"/>
  <circle cx="0" cy="0" r="{pr:.0f}" fill="{color}" opacity="0.85" filter="url(#glow)">
    <animate attributeName="r" values="{pr:.0f};{pr+1:.0f};{pr:.0f}" dur="3s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{-pr*0.3:.0f}" cy="{-pr*0.3:.0f}" r="{pr*0.3:.0f}" fill="#fff" opacity="0.12"/>
  <text x="0" y="{pr + 14}" text-anchor="middle" fill="#a0b8d0" font-size="8" font-weight="600">{r["name"][:18]}</text>
  <text x="0" y="{pr + 25}" text-anchor="middle" fill="{color}" font-size="8" font-weight="bold">&#9733; {fmt(r["stargazers_count"])}</text>
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
