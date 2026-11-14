"""Draw the README's tech toolkit as SVG pills: assets/toolkit/<slug>.svg.

Logos come from simple-icons (CC0), saved in art/icons/ so the build works offline.
Standard library only.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "assets", "toolkit")

BASE = (13, 17, 23)  # the dark panel the pill is mixed into

# (slug, label, brand colour). Brand colours that are too dark on a dark panel are lifted.
TOOLS = [
    ("python", "Python", "3776AB"), ("javascript", "JavaScript", "F7DF1E"),
    ("typescript", "TypeScript", "3178C6"), ("gnubash", "Bash", "4EAA25"),
    ("php", "PHP", "777BB4"), ("fortran", "Fortran", "734F96"),
    ("html5", "HTML5", "E34F26"), ("css3", "CSS3", "1572B6"),
    ("react", "React", "61DAFB"), ("vite", "Vite", "646CFF"),
    ("nodedotjs", "Node.js", "5FA04E"), ("npm", "npm", "CB3837"),
    ("streamlit", "Streamlit", "FF4B4B"), ("googlechrome", "Chrome", "4285F4"),
    ("googleappsscript", "Apps Script", "4285F4"), ("hugo", "Hugo", "FF4088"),
    ("latex", "LaTeX", "2DB5B5"), ("canva", "Canva", "00C4CC"),
    ("postgresql", "PostgreSQL", "4169E1"), ("mysql", "MySQL", "4479A1"),
    ("apachespark", "Spark", "E25A1C"), ("apachehadoop", "Hadoop", "66CCFF"),
    ("jupyter", "Jupyter", "F37626"), ("pandas", "Pandas", "8A7CF0"),
    ("numpy", "NumPy", "4DABCF"), ("docker", "Docker", "2496ED"),
    ("linux", "Linux", "FCC624"), ("raspberrypi", "Raspberry Pi", "C51A4A"),
    ("pihole", "Pi-hole", "E5484D"), ("apache", "Apache", "D42029"),
    ("claude", "Claude Code", "D97757"), ("git", "Git", "F05032"),
    ("github", "GitHub", "C9D1D9"), ("githubactions", "GitHub Actions", "2088FF"),
]


def mix(rgb, other, t):
    return tuple(round(a * (1 - t) + b * t) for a, b in zip(rgb, other))


def hexs(rgb):
    return "#%02x%02x%02x" % rgb


def pill(slug, label, brand):
    path = open(os.path.join(ROOT, "icons", slug + ".svg")).read()
    d = re.search(r' d="([^"]+)"', path).group(1)
    c = tuple(int(brand[i:i + 2], 16) for i in (0, 2, 4))
    border, body, cell = mix(BASE, c, .55), mix(BASE, c, .16), mix(BASE, c, .07)
    text = mix(c, (255, 255, 255), .6)
    h, cw = 40, 40
    tw = round(len(label) * 8.2)
    w = cw + tw + 28
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
<title>{label}</title>
<defs><clipPath id="r"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="11"/></clipPath></defs>
<g clip-path="url(#r)"><rect width="{w}" height="{h}" fill="{hexs(body)}"/><rect width="{cw}" height="{h}" fill="{hexs(cell)}"/></g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="11" fill="none" stroke="{hexs(border)}" stroke-width="1.5"/>
<path d="M{cw} 6v28" stroke="{hexs(border)}" stroke-opacity=".5"/>
<g transform="translate(10 10) scale(.8333)" fill="#{brand}"><path d="{d}"/></g>
<text x="{cw + 14}" y="25" font-family="Verdana,'DejaVu Sans',Arial,sans-serif" font-size="11" font-weight="700" letter-spacing=".6" fill="{hexs(text)}" textLength="{tw}" lengthAdjust="spacingAndGlyphs">{label.upper()}</text>
</svg>
'''


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for slug, label, brand in TOOLS:
        open(os.path.join(OUT, slug + ".svg"), "w").write(pill(slug, label, brand))
    print(f"built {len(TOOLS)} toolkit pills")
