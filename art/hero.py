"""README hero: the mascot waves while two lines of text type themselves out and rotate."""
import os
from lib import *

OUT = os.environ.get("OUT", "out")
W, H = 200, 64

ROLES = ["builds developer tools", "wrangles data pipelines", "ships small web apps", "works with Claude Code"]
STATUS = ["now: Apps Script flows", "learning: prompt design", "learning: context eng.", "now: Apps Script flows"]
WIN = 24                      # frames per role
N = WIN * len(ROLES)          # 96 frames, ~7.7 s at 80 ms


def typed(text, k, per_frame):
    return text[: min(len(text), k * per_frame)]


def big_mang(cv, x, y, blink, bob, wave):
    tmp = Canvas(14, 18)
    mang(tmp, 1, 0, blink=blink, legs=0, hand_up=wave)
    for j in range(18):
        for i in range(14):
            c = tmp.g[j][i]
            if c != ".":
                cv.rect(x + i * 2, y + j * 2 + bob, 2, 2, c)


def frame(t):
    cv = Canvas(W, H)
    cv.rect(0, 0, W, H, "b")
    cv.rect(0, 0, W, 1, "g"); cv.rect(0, H - 1, W, 1, "g")
    phase = t % WIN
    wave = phase < 5 and (phase // 2) % 2 == 0 or (phase < 5 and phase % 2 == 0)
    bob = 0 if (t // 6) % 2 == 0 else 1
    big_mang(cv, 8, 10, t % 30 in (20, 21), bob, phase < 6 and phase % 2 == 0)
    cv.rect(9, 49, 26, 2, "k")
    for (sx, sy, off) in [(46, 6, 0), (186, 10, 8), (150, 56, 16), (62, 58, 4)]:
        star(cv, sx, sy, (t + off) % 24 < 8)
    cv.round_corners()
    return cv


def extra(t):
    role, status = ROLES[t // WIN], STATUS[t // WIN]
    phase = t % WIN
    blink = "_" if t % 8 < 5 else " "
    ops = [
        {"op": "text", "x": 52, "y": 9, "text": "aiman amri", "color": "w", "scale": 2},
        {"op": "text", "x": 52, "y": 29, "text": "> " + typed(role, phase, 2) + blink, "color": "c"},
    ]
    st = typed(status, max(0, phase - 4), 2)
    if st:
        ops.append({"op": "text", "x": 52, "y": 42, "text": st, "color": "y"})
    return ops


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    frames = [(frame(t), 80) for t in range(N)]
    rec = recipe("hero", frames, W, H, lambda i: extra(i))
    save(os.path.join(OUT, "hero.json"), rec)
