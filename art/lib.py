"""Tiny canvas + sprite helpers that emit Pixelbolt recipes."""
import json, math

PALETTE = {
    "k": "#12141d", "b": "#1b1f31", "B": "#262c47", "g": "#3a4366", "G": "#6a769b",
    "w": "#f2f0e6", "y": "#ffd166", "o": "#f08a3c", "r": "#e5484d", "p": "#b56cf0",
    "c": "#4cc9f0", "t": "#2ec4a6", "e": "#7bd88f", "d": "#1a8f6a", "s": "#f1c9a0",
    "S": "#c98f66", "h": "#5a3a2a", "n": "#3a4a8a", "m": "#9aa5c0", "M": "#5c667d",
    "C": "#2a8fb5", "O": "#b8621f", "R": "#a02a30", "P": "#7d3fb0", "E": "#4fa862",
}


class Canvas:
    def __init__(self, w, h, fill="."):
        self.w, self.h = w, h
        self.g = [[fill] * w for _ in range(h)]

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h and c != ".":
            self.g[y][x] = c

    def rect(self, x, y, w, h, c):
        for j in range(h):
            for i in range(w):
                self.px(x + i, y + j, c)

    def frame(self, x, y, w, h, edge, fill):
        self.rect(x, y, w, h, fill)
        for i in range(w):
            self.px(x + i, y, edge); self.px(x + i, y + h - 1, edge)
        for j in range(h):
            self.px(x, y + j, edge); self.px(x + w - 1, y + j, edge)

    def line(self, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.px(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)

    def disc(self, cx, cy, r, c):
        for j in range(-r, r + 1):
            for i in range(-r, r + 1):
                if i * i + j * j <= r * r + r // 2:
                    self.px(cx + i, cy + j, c)

    def blit(self, spr, x, y, flip=False):
        for j, row in enumerate(spr):
            row = row[::-1] if flip else row
            for i, ch in enumerate(row):
                self.px(x + i, y + j, ch)

    def rows(self):
        return ["".join(r) for r in self.g]

    def round_corners(self):
        for (x, y) in [(0, 0), (self.w - 1, 0), (0, self.h - 1), (self.w - 1, self.h - 1)]:
            self.g[y][x] = "."


def sp(*rows, w=None):
    w = w or len(rows[0])
    for r in rows:
        assert len(r) == w, (len(r), w, r)
    return list(rows)


def recipe(name, frames, w, h, extra_ops=None):
    """frames: list of (Canvas, duration_ms)."""
    fr = []
    names = []
    for i, (cv, dur) in enumerate(frames):
        n = f"f{i:03d}"
        names.append(n)
        ops = [{"op": "grid", "x": 0, "y": 0, "rows": cv.rows()}]
        if extra_ops:
            ops += extra_ops(i)
        fr.append({"name": n, "duration": dur, "ops": ops})
    return {"version": 1, "name": name, "width": w, "height": h, "palette": PALETTE,
            "frames": fr, "animations": {"loop": {"frames": names}}}


def save(path, rec):
    with open(path, "w") as f:
        json.dump(rec, f)


# ---------- sprites ----------
def mang(cv, x, y, blink=False, legs=0, hand_up=False):
    """Mang: teal beanie, orange hoodie. 10x16."""
    eye = "k" if not blink else "s"
    rows = [
        "..kkkkkk..",
        ".k" + "t" * 6 + "k.",
        "k" + "t" * 6 + "dd" + "k",
        "k" + "d" * 8 + "k",
        ".k" + "s" * 6 + "k.",
        ".ks" + eye + "ss" + eye + "sk.",
        ".k" + "s" * 6 + "k.",
        "..kk" + "ss" + "kk..",
        "kk" + "o" * 6 + "kk",
        "ko" + "o" * 6 + "ok",
        "ko" + "o" * 6 + "ok",
        "ks" + "o" * 6 + "sk",
        ".k" + "n" * 6 + "k.",
        ".k" + "n" * 6 + "k.",
        [".knnkknnk.", "knnk..knnk", ".knnkk.nnk"][legs],
        [".khhkkhhk.", "khhk..khhk", ".khhkk.hhk"][legs],
    ]
    # fix eye row: eyes at idx 3 and 6
    rows[5] = ".ks" + eye + "ss" + eye + "sk."
    rows = [r[:10] for r in rows]
    for r in rows:
        assert len(r) == 10, (len(r), r)
    cv.blit(rows, x, y)
    if hand_up:
        for j in (8, 9, 10, 11):
            cv.px(x + 9, y + j, "o") if False else None
        # raise right arm
        cv.px(x + 9, y + 8, "k"); cv.px(x + 9, y + 11, "o")
        cv.px(x + 10, y + 7, "o"); cv.px(x + 10, y + 8, "o"); cv.px(x + 10, y + 9, "k")
        cv.px(x + 10, y + 6, "s"); cv.px(x + 10, y + 5, "s")


def robot(cv, x, y, blink=False, arm=0, color="c"):
    """Little agent robot. 10x14. arm: 0 down, 1 up, 2 forward."""
    e = "k" if blink else color
    rows = [
        "....".ljust(4,".") + color + ".....",
        "....k.....",
        ".kkkkkkkk.",
        "kmmmmmmmmk",
        "kmkkkkkkmk",
        "km" + "k" + e + "kk" + e + "k" + "mk",
        "km" + "kkkkkk" + "mk",
        ".kmmmmmmk.",
        "..kkkkkk..",
        ".kMMMMMMk.",
        "km" + "MM" + color * 2 + "MM" + "mk",
        ".kMMMMMMk.",
        ".kkkkkkkk.",
        "kkmmmmmmkk",
    ]
    for r in rows:
        assert len(r) == 10, (len(r), r)
    cv.blit(rows, x, y)
    # arms
    if arm == 0:
        cv.px(x - 1, y + 10, "m"); cv.px(x + 10, y + 10, "m")
        cv.px(x - 1, y + 11, "M"); cv.px(x + 10, y + 11, "M")
    elif arm == 1:
        cv.px(x - 1, y + 10, "m"); cv.px(x - 1, y + 9, "m"); cv.px(x - 1, y + 8, "m")
        cv.px(x + 10, y + 10, "m"); cv.px(x + 10, y + 11, "M")
    else:
        cv.px(x - 1, y + 10, "m"); cv.px(x - 2, y + 10, "m"); cv.px(x - 3, y + 10, "m")
        cv.px(x + 10, y + 10, "m"); cv.px(x + 10, y + 11, "M")


def icon_block(cv, x, y):
    cv.frame(x, y, 10, 10, "k", "G")
    cv.rect(x + 1, y + 8, 8, 1, "M")
    cv.px(x + 2, y + 2, "m"); cv.px(x + 3, y + 2, "m")


def icon_code(cv, x, y):
    cv.frame(x, y, 10, 10, "k", "c")
    for p in [(2, 3), (3, 4), (4, 5), (3, 6), (2, 7)]:
        cv.px(x + p[0], y + p[1], "k")
    cv.rect(x + 5, y + 7, 3, 1, "k")


def icon_qr(cv, x, y):
    cv.frame(x, y, 10, 10, "k", "w")
    for (i, j) in [(1, 1), (6, 1), (1, 6)]:
        cv.frame(x + i, y + j, 3, 3, "k", "w")
        cv.px(x + i + 1, y + j + 1, "k")
    for p in [(5, 5), (7, 6), (6, 7), (7, 8), (5, 8), (4, 4), (8, 5)]:
        cv.px(x + p[0], y + p[1], "k")


def icon_pdf(cv, x, y):
    cv.frame(x, y, 10, 10, "k", "w")
    cv.rect(x + 1, y + 1, 8, 3, "r")
    for j in (5, 7):
        cv.rect(x + 2, y + j, 6, 1, "G")
    cv.px(x + 8, y + 9, "G")


ICONS = [icon_code, icon_qr, icon_pdf]


def star(cv, x, y, big):
    cv.px(x, y, "w")
    if big:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            cv.px(x + dx, y + dy, "y")
