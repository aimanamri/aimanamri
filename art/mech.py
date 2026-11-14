import math, os
from lib import *

OUT = os.environ.get("OUT", "out")
W, H, N = 128, 80, 32


def frame(t):
    cv = Canvas(W, H)
    cv.rect(0, 0, W, H, "b")
    for sx, sy in [(8, 8), (66, 6), (118, 10), (100, 20)]:
        star(cv, sx, sy, (t // 8 + sx) % 2 == 0)
    cv.rect(0, 62, W, 18, "B"); cv.rect(0, 62, W, 1, "g")
    th = 2 * math.pi * t / N
    # --- engine: flywheel, crank, piston, cylinder ---
    cx, cy, r, L = 24, 42, 7, 22
    pin = (cx + r * math.cos(th), cy + r * math.sin(th))
    px = pin[0] + math.sqrt(L * L - (pin[1] - cy) ** 2)
    cv.rect(0, 56, 66, 6, "M"); cv.rect(0, 56, 66, 1, "m")      # engine bed
    cv.frame(38, 35, 28, 14, "k", "B")                         # cylinder
    cv.rect(39, 36, 26, 12, "b")
    if 0.85 < (th % (2 * math.pi)) / (2 * math.pi) or (th % (2 * math.pi)) / (2 * math.pi) < 0.1:
        cv.rect(60, 38, 4, 8, "o"); cv.rect(62, 40, 2, 4, "y")  # combustion glow
    cv.rect(round(px) - 1, 37, 6, 10, "m"); cv.rect(round(px) - 1, 37, 6, 1, "w")
    cv.line(round(pin[0]), round(pin[1]), round(px), cy, "m")
    cv.line(round(pin[0]), round(pin[1]) + 1, round(px), cy + 1, "M")
    cv.disc(cx, cy, 13, "k"); cv.disc(cx, cy, 12, "M"); cv.disc(cx, cy, 10, "b")
    for i in range(4):
        a = th + i * math.pi / 2
        cv.line(cx, cy, round(cx + 11 * math.cos(a)), round(cy + 11 * math.sin(a)), "m")
    cv.disc(cx, cy, 3, "o"); cv.disc(round(pin[0]), round(pin[1]), 1, "y")
    # --- pressure gauge ---
    gx, gy = 52, 14
    cv.disc(gx, gy, 8, "k"); cv.disc(gx, gy, 7, "w")
    for i in range(7):
        a = math.pi * (0.85 + i * 0.3 / 1)
        cv.px(round(gx + 6 * math.cos(a)), round(gy + 6 * math.sin(a)), "G")
    na = math.pi * (0.9 + 1.2 * (0.5 + 0.5 * math.sin(th)))
    cv.line(gx, gy, round(gx + 6 * math.cos(na)), round(gy + 6 * math.sin(na)), "r")
    cv.px(gx, gy, "k")
    # --- spring and mass ---
    sx = 84
    cv.rect(sx - 8, 8, 16, 3, "M"); cv.rect(sx - 8, 8, 16, 1, "m")
    my = 36 + round(7 * math.sin(2 * th))
    zig = [(0, 0), (4, 1), (-4, 2), (4, 3), (-4, 4), (4, 5), (-4, 6), (0, 7)]
    top, bot = 11, my
    prev = (sx, top)
    for (zx, zi) in zig:
        p = (sx + zx, top + round((bot - top) * (zi + 1) / 8))
        cv.line(prev[0], prev[1], p[0], p[1], "c"); prev = p
    cv.line(prev[0], prev[1], sx, bot, "c")
    cv.frame(sx - 7, my, 14, 9, "k", "p"); cv.rect(sx - 6, my + 1, 12, 1, "w")
    cv.px(sx - 3, my + 4, "k"); cv.px(sx + 3, my + 4, "k")
    # --- projectile arc ---
    u = t / N
    cv.rect(94, 56, 8, 6, "M"); cv.rect(96, 52, 6, 4, "m")
    for k in range(5, 0, -1):
        uu = (u - k * 0.04) % 1
        cv.px(round(100 + 26 * uu), round(56 - 4 * 28 * uu * (1 - uu)), "G" if k > 2 else "y")
    bx, by = round(100 + 26 * u), round(56 - 4 * 28 * u * (1 - u))
    cv.disc(bx, by, 2, "o"); cv.px(bx - 1, by - 1, "y")
    cv.rect(100, 61, 28, 1, "G")
    # --- Mang the engineer, hard hat + clipboard ---
    mang(cv, 66, 63, blink=t % 24 in (14, 15), legs=0)
    cv.rect(67, 64, 8, 2, "y"); cv.rect(66, 66, 10, 1, "O")
    cv.frame(77, 71, 7, 6, "k", "w")
    for j in range(3):
        cv.rect(78, 72 + j * 2, 2 + (t // 4 + j) % 4, 1, "G")
    cv.round_corners()
    return cv


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    save(os.path.join(OUT, "mech.json"), recipe("mech", [(frame(t), 80) for t in range(N)], W, H))
