import os
from lib import *

OUT = os.environ.get("OUT", "out")

W, H, N = 128, 80, 32

CELLS = {
    "A": (10, 17, 34, 27), "B": (48, 17, 44, 13), "C": (48, 33, 20, 11),
    "D": (72, 33, 20, 11), "E": (10, 47, 82, 23),
}
TARGETS = ["A", "B", "D", "E"]
COLORS = ["y", "p", "c", "e"]


def draw_cell(cv, key, t, flash):
    x, y, w, h = CELLS[key]
    cv.frame(x, y, w, h, "y" if flash else "g", "B")
    if key == "A":
        for r, ln in enumerate((22, 28, 16, 25)):
            cv.rect(x + 4, y + 5 + r * 5, ln, 1, "G")
        if t % 8 < 4:
            cv.rect(x + 4 + 16, y + 20, 2, 4, "w")
    elif key == "B":
        cv.frame(x + 4, y + 3, 14, 7, "k", "p"); cv.px(x + 6, y + 10, "p")
        cv.px(x + 8, y + 6, "w"); cv.px(x + 10, y + 6, "w"); cv.px(x + 12, y + 6, "w")
        cv.rect(x + 22, y + 5, 16, 1, "G"); cv.rect(x + 22, y + 8, 10, 1, "g")
    elif key == "C":
        for (dx, dy) in [(9, 2), (8, 4), (10, 4), (7, 6), (11, 6), (9, 6), (8, 8), (10, 8)]:
            cv.px(x + dx, y + dy, "y")
    elif key == "D":
        for p in [(4, 3), (3, 4), (4, 5), (15, 3), (16, 4), (15, 5)]:
            cv.px(x + p[0], y + p[1], "c")
        cv.px(x + 10, y + 3, "w"); cv.px(x + 9, y + 5, "w"); cv.px(x + 8, y + 7, "w") if False else None
        cv.line(x + 9, y + 7, x + 11, y + 2, "e")
    elif key == "E":
        for r, (a, b, c) in enumerate([(30, "c", 12), (20, "e", 28), (40, "o", 8)]):
            cv.rect(x + 4, y + 5 + r * 6, 3, 1, b); cv.rect(x + 9, y + 5 + r * 6, a, 1, "G")
            cv.rect(x + 11 + a, y + 5 + r * 6, c, 1, b)


def frame(t):
    cv = Canvas(W, H)
    cv.rect(0, 0, W, H, "b")
    cv.rect(0, 70, W, 10, "B"); cv.rect(0, 70, W, 1, "g")
    # window
    cv.frame(6, 6, 90, 68, "g", "b")
    cv.rect(7, 7, 88, 7, "B")
    cv.px(10, 10, "r"); cv.px(15, 10, "y"); cv.px(20, 10, "e")
    cv.rect(34, 9, 40, 3, "g")
    cycle = t // 8
    phase = t % 8
    for key in CELLS:
        draw_cell(cv, key, t, flash=(TARGETS[cycle] == key and phase >= 6) or (key == "C" and t % 16 < 3))
    # flying card
    tx, ty, tw, th = CELLS[TARGETS[cycle]]
    sx, sy = 103, 55
    ex, ey = tx + tw // 2 - 3, ty + th // 2 - 2
    if phase < 6:
        f = phase / 5
        cx = round(sx + (ex - sx) * f)
        cy = round(sy + (ey - sy) * f - 10 * math.sin(math.pi * f))
        cv.frame(cx, cy, 7, 5, "k", COLORS[cycle]); cv.px(cx + 2, cy + 2, "k"); cv.px(cx + 4, cy + 2, "k")
    # Mang, tossing cards
    mang(cv, 108, 54, blink=t % 20 in (13, 14), legs=0, hand_up=phase < 3)
    # held stack of cards
    cv.frame(100, 66, 7, 4, "k", COLORS[(cycle + 1) % 4]); cv.rect(101, 65, 5, 1, "w")
    # little lamp
    cv.rect(121, 52, 1, 18, "M"); cv.rect(118, 50, 7, 3, "y"); cv.rect(119, 53, 5, 1, "w" if t % 16 < 12 else "y")
    cv.round_corners()
    return cv


import math  # noqa: E402

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    frames = [(frame(t), 90) for t in range(N)]
    save(os.path.join(OUT, "kb.json"), recipe("kb", frames, W, H))
