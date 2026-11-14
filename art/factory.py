import math
import os
from lib import *

OUT = os.environ.get("OUT", "out")

W, H, N = 128, 80, 40


def gear(cv, cx, cy, r, teeth, ang, body="m", edge="M"):
    cv.disc(cx, cy, r, edge)
    cv.disc(cx, cy, r - 1, body)
    for i in range(teeth):
        a = ang + i * 2 * math.pi / teeth
        tx, ty = round(cx + math.cos(a) * (r + 1)), round(cy + math.sin(a) * (r + 1))
        cv.px(tx, ty, edge)
        cv.px(round(cx + math.cos(a) * r), round(cy + math.sin(a) * r), body)
    cv.disc(cx, cy, max(1, r // 3), "k")


def frame(t):
    cv = Canvas(W, H)
    cv.rect(0, 0, W, H, "b")
    # back wall windows
    for wx in (8, 40, 84):
        cv.frame(wx, 6, 22, 14, "g", "B")
        cv.rect(wx + 10, 7, 1, 12, "g")
        star(cv, wx + 4, 11, False); star(cv, wx + 16, 15, t % 20 < 10)
    # gears on wall
    gear(cv, 20, 34, 7, 8, t * (2 * math.pi / 8) * 2 / N)
    gear(cv, 33, 38, 4, 6, -t * (2 * math.pi / 6) * 2 / N + 0.3, "o", "O")
    # chimney
    cv.rect(100, 24, 11, 32, "O")
    for j in range(26, 56, 4):
        cv.rect(100, j, 11, 1, "h")
    cv.rect(98, 22, 15, 3, "k")
    cv.rect(99, 22, 13, 1, "g")
    # smoke
    for k, off in enumerate((0, 13, 27)):
        ph = (t + off) % N
        y = 20 - round(ph * 0.45)
        x = 105 + round(3 * math.sin(ph / N * 2 * math.pi + k))
        r = 1 + ph // 14
        cv.disc(x, y, r, "G" if ph < 28 else "g")
    # floor
    cv.rect(0, 62, W, 18, "B")
    cv.rect(0, 62, W, 1, "g")
    for x in range(0, W, 16):
        cv.rect(x + (4 if (x // 16) % 2 else 0), 70, 8, 1, "g")
    # agent robots (behind belt)
    blink1 = t % 20 in (7, 8)
    robot(cv, 14, 43, blink1, arm=2 if t % 20 < 10 else 0, color="c")
    robot(cv, 88, 43, t % 27 in (4, 5), arm=1 if (t // 5) % 2 == 0 else 0, color="e")
    # gantry press
    cv.rect(50, 14, 4, 42, "M"); cv.rect(75, 14, 4, 42, "M")
    cv.rect(50, 14, 1, 42, "m"); cv.rect(75, 14, 1, 42, "m")
    cv.frame(48, 10, 32, 8, "k", "m")
    cv.rect(49, 11, 30, 1, "w")
    # nearest item distance
    items = []
    for i in range(-1, 4):
        x = -10 + 40 * i + 3 * t
        if -10 <= x <= 127:
            items.append((i, x))
    down = 0
    for i, x in items:
        d = abs(x + 5 - 64)
        down = max(down, max(0.0, 1 - d / 12))
    hy = 24 + round(18 * down)
    cv.rect(63, 18, 3, hy - 18, "m")
    cv.rect(63, 18, 1, hy - 18, "w")
    cv.frame(58, hy, 13, 4, "k", "r" if down > 0.8 else "o")
    cv.px(64, 12, "r" if down > 0.5 else "e")
    cv.px(66, 12, "y" if t % 8 < 4 else "g")
    if down > 0.85:
        for dx in (-4, 4, -6, 6):
            cv.px(64 + dx, 50 + (t % 3), "y")
    # belt
    cv.rect(4, 56, 120, 1, "m")
    cv.rect(4, 57, 120, 3, "M")
    shift = (3 * t) % 6
    for x in range(-6, W, 6):
        cv.px(x + shift, 58, "g"); cv.px(x + shift + 1, 58, "g")
    cv.rect(4, 60, 120, 1, "k")
    cv.disc(4, 58, 3, "k"); cv.disc(4, 58, 2, "M")
    cv.disc(123, 58, 3, "k"); cv.disc(123, 58, 2, "M")
    # items
    for i, x in items:
        if x + 5 < 64:
            icon_block(cv, x, 46)
        else:
            ICONS[i % 3](cv, x, 46)
    # Mang in the foreground with a tablet
    mang(cv, 52, 63, blink=t % 24 in (11, 12), legs=0)
    cv.frame(63, 71, 7, 5, "k", "c")
    cv.px(65, 73, "k"); cv.px(67, 73, "k") if t % 10 < 5 else cv.px(66, 74, "k")
    cv.px(64, 72, "w")
    # speech blip when item done
    if 14 <= t % N < 20:
        cv.frame(66, 60, 9, 5, "k", "w") if False else None
    cv.round_corners()
    return cv


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    frames = [(frame(t), 70) for t in range(N)]
    save(os.path.join(OUT, "factory.json"), recipe("factory", frames, W, H))
