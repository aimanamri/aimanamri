"""Pixel-style link buttons for the README header: assets/buttons/<id>.svg.

Nav buttons get a pulsing bullet; social buttons get the service's logo (simple-icons, CC0).
Standard library only.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "assets", "buttons")
BASE = (13, 17, 23)

# id, label, colour, icon slug (None = pulsing bullet)
BUTTONS = [
    ("projects", "Projects", "4CC9F0", None),
    ("toolkit", "Toolkit", "FFD166", None),
    ("stats", "Stats", "7BD88F", None),
    ("repos", "All repositories", "B56CF0", "github"),
    ("website", "aimanuddin.com", "F08A3C", None),
    ("linkedin", "LinkedIn", "3E9BE0", "linkedin"),
    ("stackoverflow", "Stack Overflow", "F48024", "stackoverflow"),
    ("kaggle", "Kaggle", "20BEFF", "kaggle"),
]


def mix(a, b, t):
    return tuple(round(x * (1 - t) + y * t) for x, y in zip(a, b))


def hx(c):
    return "#%02x%02x%02x" % c


def notched(x, y, w, h, n=3):
    pts = [(n, 0), (w - n, 0), (w - n, 1), (w - 1, 1), (w - 1, n), (w, n), (w, h - n), (w - 1, h - n), (w - 1, h - 1),
           (w - n, h - 1), (w - n, h), (n, h), (n, h - 1), (1, h - 1), (1, h - n), (0, h - n), (0, n), (1, n), (1, 1), (n, 1)]
    return " ".join(f"{x + px},{y + py}" for px, py in pts)


def button(bid, label, brand, icon):
    c = tuple(int(brand[i:i + 2], 16) for i in (0, 2, 4))
    border, body = mix(BASE, c, .8), mix(BASE, c, .14)
    text = mix(c, (255, 255, 255), .7)
    h = 36
    tw = round(len(label) * 7.6)
    w = 16 + 18 + tw + 18
    if icon:
        d = re.search(r' d="([^"]+)"', open(os.path.join(ROOT, "icons", icon + ".svg")).read()).group(1)
        mark = f'<g transform="translate(16 10) scale(.6667)" fill="#{brand}"><path d="{d}"/></g>'
    else:
        mark = (f'<rect x="18" y="14" width="8" height="8" fill="#{brand}">'
                f'<animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></rect>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}" shape-rendering="crispEdges">
<title>{label}</title>
<polygon points="{notched(0, 0, w, h)}" fill="{hx(border)}"/>
<polygon points="{notched(2, 2, w - 4, h - 4, 2)}" fill="{hx(body)}"/>
{mark}
<text x="40" y="23" font-family="Verdana,'DejaVu Sans',Arial,sans-serif" font-size="12" font-weight="700" fill="{hx(text)}" shape-rendering="auto" textLength="{tw}" lengthAdjust="spacingAndGlyphs">{label}</text>
</svg>
'''


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for bid, label, brand, icon in BUTTONS:
        open(os.path.join(OUT, bid + ".svg"), "w").write(button(bid, label, brand, icon))
    print(f"built {len(BUTTONS)} buttons")
