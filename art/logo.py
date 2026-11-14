import math
import os
from lib import *

OUT = os.environ.get("OUT", "out")

W, H, N = 160, 48, 24


def big_mang(cv, x, y, blink, bob):
    tmp = Canvas(12, 18)
    mang(tmp, 1, 0, blink=blink, legs=0)
    for j in range(18):
        for i in range(12):
            c = tmp.g[j][i]
            if c != ".":
                cv.rect(x + i * 2, y + j * 2 + bob, 2, 2, c)


def frame(t):
    cv = Canvas(W, H)
    cv.rect(0, 0, W, H, "b")
    cv.rect(0, H - 1, W, 1, "g")
    cv.rect(0, 0, W, 1, "g")
    # bobbing mascot
    bob = 0 if (t // 6) % 2 == 0 else 1
    big_mang(cv, 10, 6, t % 24 in (16, 17), bob)
    cv.rect(11, 42, 24, 2, "k")
    # sparkles
    for (sx, sy, off) in [(44, 9, 0), (150, 12, 6), (120, 40, 12), (60, 40, 18)]:
        star(cv, sx, sy, (t + off) % 24 < 8)
    # underscore cursor
    if t % 12 < 7:
        cv.rect(106, 22, 5, 2, "y")
    cv.round_corners()
    return cv


def extra(i):
    return [
        {"op": "text", "x": 48, "y": 14, "text": "AIMAN", "color": "w", "scale": 2} if False else
        {"op": "text", "x": 48, "y": 16, "text": "aiman amri", "color": "w"},
        {"op": "text", "x": 48, "y": 28, "text": "tools - data - ai", "color": "c"},
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    frames = [(frame(t), 110) for t in range(N)]
    save(os.path.join(OUT, "logo.json"), recipe("logo", frames, W, H, extra))
