import math
import os
from lib import *

OUT = os.environ.get("OUT", "out")

W, H, N = 128, 80, 24


def board(cv, x, y, t, k):
    cv.frame(x, y, 30, 13, "k", "d")
    cv.rect(x + 1, y + 1, 28, 1, "E")
    cv.rect(x + 9, y + 3, 7, 7, "k"); cv.rect(x + 10, y + 4, 5, 5, "M")
    cv.px(x + 11, y + 5, "m")
    cv.rect(x + 22, y + 2, 7, 4, "m"); cv.rect(x + 22, y + 7, 7, 4, "M")
    # LEDs
    cv.px(x + 3, y + 3, "e" if (t // (3 + k)) % 2 == 0 else "E")
    cv.px(x + 3, y + 5, "r" if (t // (2 + k * 2)) % 2 == 0 else "R")
    # progress bar
    fill = ((t + k * 8) % N) * 14 // N
    cv.rect(x + 3, y + 9, 15, 2, "k")
    cv.rect(x + 3, y + 9, 1 + fill, 2, "c")
    # sockets
    for i in range(3):
        cv.px(x + 18 + i * 1, y + 11, "y")


def frame(t):
    cv = Canvas(W, H)
    cv.rect(0, 0, W, H, "b")
    for sx, sy in [(10, 8), (30, 14), (58, 6), (96, 10), (118, 8), (80, 4)]:
        star(cv, sx, sy, (t // 6 + sx) % 2 == 0)
    cv.rect(0, 62, W, 18, "B"); cv.rect(0, 62, W, 1, "g")
    # database
    for j, yy in enumerate((26, 34, 42)):
        cv.rect(6, yy, 16, 8, "C"); cv.rect(6, yy, 1, 8, "k"); cv.rect(21, yy, 1, 8, "k")
        cv.rect(7, yy, 14, 1, "c"); cv.rect(7, yy + 7, 14, 1, "k")
        cv.px(9, yy + 3, "e" if (t // 4 + j) % 2 else "w")
        cv.rect(12, yy + 3, 6, 1, "k")
    cv.rect(6, 24, 16, 2, "c"); cv.rect(6, 24, 16, 1, "w")
    # input pipe + packets
    cv.rect(22, 37, 30, 6, "k"); cv.rect(22, 38, 30, 4, "M"); cv.rect(22, 38, 30, 1, "m")
    for i in range(-1, 3):
        px_ = 24 + i * 12 + (3 * t) % 12
        if 22 <= px_ <= 48:
            cv.rect(px_, 39, 3, 2, ["c", "o", "e"][(i + (3 * t) // 12) % 3])
    # rack
    cv.frame(50, 12, 36, 52, "k", "M")
    cv.rect(51, 13, 34, 1, "m")
    for k, y in enumerate((16, 32, 48)):
        board(cv, 53, y, t, k)
    # output pipe + packets
    cv.rect(86, 37, 16, 6, "k"); cv.rect(86, 38, 16, 4, "M"); cv.rect(86, 38, 16, 1, "m")
    for i in range(-1, 2):
        px_ = 86 + i * 12 + (3 * t) % 12
        if 86 <= px_ <= 98:
            cv.rect(px_, 39, 3, 2, "y")
    # chart
    cv.frame(100, 18, 26, 42, "g", "b")
    cv.rect(103, 55, 20, 1, "G")
    for i, c in enumerate("cey"):
        h = 4 + round(14 * (0.5 + 0.5 * math.sin(2 * math.pi * t / N + i * 1.3)))
        cv.rect(104 + i * 6, 55 - h, 4, h, c)
        cv.rect(104 + i * 6, 55 - h, 4, 1, "w")
    cv.rect(104, 22, 10, 1, "G"); cv.rect(104, 25, 6, 1, "g")
    # Mang at a laptop
    mang(cv, 12, 62, blink=t % 24 in (9, 10), legs=0)
    cv.rect(24, 70, 14, 2, "M"); cv.rect(24, 72, 14, 1, "k")
    cv.frame(26, 62, 11, 8, "k", "k")
    cv.rect(27, 63, 9, 6, "b")
    for r in range(3):
        cv.rect(28, 64 + r * 2, 3 + (t // 3 + r) % 5, 1, "e")
    cv.px(23, 69 if t % 2 else 68, "s")
    # job done bubble
    if t % N >= 16:
        cv.frame(6, 48, 11, 9, "k", "w")
        cv.px(8, 53, "e"); cv.px(9, 54, "e"); cv.px(10, 53, "e"); cv.px(11, 52, "e"); cv.px(12, 51, "e")
        cv.px(11, 57, "k"); cv.px(12, 58, "k")
    cv.round_corners()
    return cv


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    frames = [(frame(t), 90) for t in range(N)]
    save(os.path.join(OUT, "data.json"), recipe("data", frames, W, H))
