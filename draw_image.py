#!/usr/bin/env python3
"""Draw the World News front page for Wednesday, 25 November 2026.

Renders entry.png (1024x1024) straight into this repository directory.
Run:  python3 draw_image.py
Everything is drawn with Pillow primitives; no network, no downloaded assets.
"""

import math
import os
import random
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

PAPER = (248, 244, 233)
INK = (20, 24, 32)
NAVY = (16, 32, 58)
NAVY_LIGHT = (29, 74, 122)
GOLD = (217, 164, 65)
RED = (178, 34, 34)
GREY = (90, 92, 96)
LIGHT_GREY = (226, 222, 210)
CARD_BG = (255, 252, 244)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_BIG = font("DejaVuSerif-Bold.ttf", 64)
F_SERIF = font("DejaVuSerif.ttf", 20)
F_SANS_B = font("DejaVuSans-Bold.ttf", 44)
F_SANS_B20 = font("DejaVuSans-Bold.ttf", 20)
F_SANS_B19 = font("DejaVuSans-Bold.ttf", 19)
F_SANS = font("DejaVuSans.ttf", 20)
F_SANS15 = font("DejaVuSans.ttf", 15)
F_SANS14 = font("DejaVuSans.ttf", 14)
F_SANS13B = font("DejaVuSans-Bold.ttf", 13)
F_SANS12 = font("DejaVuSans.ttf", 13)


def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_sky(draw, box, top, bottom, rng):
    x0, y0, x1, y1 = box
    steps = y1 - y0
    for i in range(steps):
        t = i / max(steps - 1, 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b))
    for _ in range(90):
        sx = rng.randint(x0 + 4, x1 - 4)
        sy = rng.randint(y0 + 4, y1 - 4)
        s = rng.choice([1, 1, 2])
        draw.ellipse([sx, sy, sx + s, sy + s], fill=(235, 238, 245))


def draw_rocket(draw, cx, base_y, scale):
    """A stylised ascending rocket with flame and smoke, centred on cx."""
    body_w = int(46 * scale)
    body_h = int(150 * scale)
    nose_h = int(52 * scale)
    top = base_y - body_h - nose_h
    # flame
    flame = [
        (cx - 16 * scale, base_y),
        (cx - 34 * scale, base_y + 62 * scale),
        (cx - 12 * scale, base_y + 44 * scale),
        (cx, base_y + 78 * scale),
        (cx + 12 * scale, base_y + 44 * scale),
        (cx + 34 * scale, base_y + 62 * scale),
        (cx + 16 * scale, base_y),
    ]
    draw.polygon(flame, fill=(255, 140, 40))
    inner = [
        (cx - 9 * scale, base_y),
        (cx - 16 * scale, base_y + 34 * scale),
        (cx, base_y + 48 * scale),
        (cx + 16 * scale, base_y + 34 * scale),
        (cx + 9 * scale, base_y),
    ]
    draw.polygon(inner, fill=(255, 214, 90))
    # fins
    draw.polygon(
        [(cx - body_w / 2, base_y - 8), (cx - body_w / 2 - 26 * scale, base_y + 26 * scale),
         (cx - body_w / 2, base_y + 14)], fill=(178, 34, 34))
    draw.polygon(
        [(cx + body_w / 2, base_y - 8), (cx + body_w / 2 + 26 * scale, base_y + 26 * scale),
         (cx + body_w / 2, base_y + 14)], fill=(178, 34, 34))
    # body
    draw.rectangle([cx - body_w / 2, top + nose_h, cx + body_w / 2, base_y],
                   fill=(240, 242, 245), outline=(120, 130, 145))
    # nose cone
    draw.polygon([(cx - body_w / 2, top + nose_h), (cx, top),
                  (cx + body_w / 2, top + nose_h)], fill=(178, 34, 34))
    # red band + window
    draw.rectangle([cx - body_w / 2, top + nose_h + 52 * scale,
                    cx + body_w / 2, top + nose_h + 66 * scale], fill=(178, 34, 34))
    draw.ellipse([cx - 11 * scale, top + nose_h + 22 * scale,
                  cx + 11 * scale, top + nose_h + 44 * scale],
                 fill=(29, 74, 122), outline=(120, 130, 145))
    # smoke puffs at the base
    for dx, dy, r in [(-58, 66, 26), (52, 70, 30), (-20, 82, 22), (18, 86, 26)]:
        draw.ellipse([cx + dx * scale - r, base_y + dy * scale - r * 0.6,
                      cx + dx * scale + r, base_y + dy * scale + r * 0.6],
                     fill=(214, 216, 222))


def draw_station(draw, cx, cy, scale):
    """Small Tiangong-style station: core module with two solar wings."""
    draw.rectangle([cx - 34 * scale, cy - 9 * scale, cx + 34 * scale, cy + 9 * scale],
                   fill=(200, 205, 215), outline=(120, 130, 145))
    draw.polygon([(cx + 34 * scale, cy - 9 * scale), (cx + 46 * scale, cy),
                  (cx + 34 * scale, cy + 9 * scale)], fill=(178, 34, 34))
    for side in (-1, 1):
        x0 = cx + side * 40 * scale
        x1 = cx + side * 108 * scale
        draw.rectangle([min(x0, x1), cy - 13 * scale, max(x0, x1), cy + 13 * scale],
                       fill=(36, 68, 140), outline=(200, 205, 215))
        for k in range(1, 4):
            xk = cx + side * (40 + k * 17) * scale
            draw.line([(xk, cy - 13 * scale), (xk, cy + 13 * scale)], fill=(200, 205, 215))


def icon_burst(draw, x, y, s, color):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        r = s if i % 2 == 0 else s * 0.45
        pts.append((x + r * math.cos(ang), y + r * math.sin(ang)))
    draw.polygon(pts, fill=color)


def icon_shield(draw, x, y, s):
    draw.polygon([(x, y - s), (x + s * 0.85, y - s * 0.55), (x + s * 0.85, y + s * 0.1),
                  (x, y + s), (x - s * 0.85, y + s * 0.1), (x - s * 0.85, y - s * 0.55)],
                 outline=(29, 74, 122), width=4)
    draw.line([(x - s * 0.45, y), (x - s * 0.1, y + s * 0.4), (x + s * 0.55, y - s * 0.4)],
              fill=(29, 74, 122), width=5)


def icon_lock(draw, x, y, s):
    draw.arc([x - s * 0.55, y - s * 0.85, x + s * 0.55, y + s * 0.1], 180, 360,
             fill=(178, 34, 34), width=5)
    draw.rounded_rectangle([x - s * 0.7, y - s * 0.1, x + s * 0.7, y + s * 0.8],
                           radius=6, fill=(178, 34, 34))
    draw.ellipse([x - 4, y + s * 0.18, x + 4, y + s * 0.26], fill=(255, 255, 255))
    draw.line([(x, y + s * 0.26), (x, y + s * 0.5)], fill=(255, 255, 255), width=3)


def icon_ship(draw, x, y, s):
    draw.polygon([(x - s, y + s * 0.35), (x + s, y + s * 0.35),
                  (x + s * 0.7, y + s * 0.8), (x - s * 0.7, y + s * 0.8)],
                 fill=(29, 74, 122))
    draw.rectangle([x - s * 0.7, y - s * 0.15, x - s * 0.1, y + s * 0.35], fill=(217, 164, 65))
    draw.rectangle([x + s * 0.05, y - s * 0.35, x + s * 0.65, y + s * 0.35], fill=(178, 34, 34))
    draw.line([(x - s * 1.1, y + s * 0.95), (x + s * 1.1, y + s * 0.95)], fill=(90, 92, 96), width=3)


def icon_mine(draw, x, y, s):
    for i in range(8):
        ang = math.pi * i / 4
        draw.line([(x + s * 0.55 * math.cos(ang), y + s * 0.55 * math.sin(ang)),
                   (x + s * 1.05 * math.cos(ang), y + s * 1.05 * math.sin(ang))],
                  fill=(20, 24, 32), width=4)
    draw.ellipse([x - s * 0.6, y - s * 0.6, x + s * 0.6, y + s * 0.6], fill=(20, 24, 32))
    draw.polygon([(x + s * 0.1, y - s * 1.25), (x + s * 0.35, y - s * 0.6),
                  (x + s * 0.6, y - s * 1.2), (x + s * 0.75, y - s * 0.55),
                  (x + s * 0.4, y - s * 0.85)], fill=(255, 140, 40))


def icon_storm(draw, x, y, s):
    draw.ellipse([x - s, y - s * 0.35, x - s * 0.1, y + s * 0.35], fill=(90, 92, 96))
    draw.ellipse([x - s * 0.45, y - s * 0.6, x + s * 0.45, y + s * 0.35], fill=(120, 124, 130))
    draw.ellipse([x + s * 0.1, y - s * 0.3, x + s, y + s * 0.35], fill=(90, 92, 96))
    draw.polygon([(x + s * 0.15, y + s * 0.35), (x - s * 0.15, y + s * 0.75),
                  (x + s * 0.05, y + s * 0.75), (x - s * 0.25, y + s * 1.2),
                  (x + s * 0.35, y + s * 0.35)], fill=(255, 214, 90))
    for dx in (-0.6, 0.0, 0.6):
        draw.line([(x + dx * s, y + s * 0.8), (x + dx * s - 4, y + s * 1.15)],
                  fill=(29, 74, 122), width=3)


ICONS = {
    "burst": lambda d, x, y, s: icon_burst(d, x, y, s, (255, 140, 40)),
    "shield": icon_shield,
    "lock": icon_lock,
    "ship": icon_ship,
    "mine": icon_mine,
    "storm": icon_storm,
}

STORIES = [
    ("MIDDLE EAST", "Houthis claim new strikes on Saudi refinery and Riyadh",
     "Ras Tanura refinery hit; district attacked in three phases. Tuesday's strike wounded 11.", "burst"),
    ("PACIFIC", "Solomons name Australia top security partner",
     "Canberra treaty bars foreign bases; the Solomons are set to drop their 2022 pact with China.", "shield"),
    ("UNITED STATES", "CIA and spy chief's office hit by cyberattack",
     "CNN reports a suspected breach of US intelligence systems; unclassified data was exposed.", "lock"),
    ("EUROPE", "Zelenskiy confirms Ukraine hit Russian ship",
     "Kyiv says it struck the cargo vessel Sparta II in the Gulf of Finland; Norway urges caution.", "ship"),
    ("ENERGY", "Two tankers hit mines in Strait of Hormuz",
     "Iran's navy says the tankers caught fire, raising fears for the busiest oil chokepoint.", "mine"),
    ("WEATHER", "Nor'easter bears down on Thanksgiving",
     "Storm threatens the Macy's parade and holiday travel along the US East Coast.", "storm"),
]


def main():
    rng = random.Random(20261125)
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead ----
    draw.rectangle([0, 0, W, 108], fill=NAVY)
    draw.text((W / 2, 44), "WORLD NEWS", font=F_SERIF_BIG, fill=(255, 255, 255),
              anchor="mm")
    draw.text((W / 2, 92), "W E D N E S D A Y ,  2 5  N O V E M B E R  2 0 2 6",
              font=F_SANS13B, fill=GOLD, anchor="mm")
    draw.rectangle([0, 108, W, 112], fill=GOLD)

    # ---- hero kicker + headline ----
    draw.text((36, 132), "SPACE  •  CHINA", font=F_SANS13B, fill=RED)
    hero_head = "China sends first foreign astronaut to its space station"
    lines = wrap_text(draw, hero_head, F_SANS_B, W - 72)
    y = 152
    for line in lines:
        draw.text((36, y), line, font=F_SANS_B, fill=INK)
        y += 48
    standfirst = ("Pakistan's Muhammad Zeeshan Ali rides Shenzhou-24 into orbit — the first "
                  "Pakistani in space and the first foreign crew member aboard Tiangong.")
    slines = wrap_text(draw, standfirst, F_SANS, W - 72)
    y += 4
    for line in slines:
        draw.text((36, y), line, font=F_SANS, fill=GREY)
        y += 24

    # ---- hero art (drawn on its own layer so nothing spills past the frame) ----
    art = (36, 308, W - 36, 520)
    aw, ah = art[2] - art[0], art[3] - art[1]
    layer = Image.new("RGB", (aw, ah), NAVY)
    adraw = ImageDraw.Draw(layer)
    draw_sky(adraw, (0, 0, aw, ah), (11, 30, 58), (29, 74, 122), rng)
    adraw.ellipse([aw - 150, 18, aw - 78, 90], fill=(238, 240, 220))
    draw_station(adraw, 150, 64, 1.0)
    adraw.rectangle([0, ah - 34, aw, ah], fill=(10, 16, 28))
    adraw.rectangle([660, ah - 96, 672, ah - 34], fill=(10, 16, 28))
    adraw.rectangle([700, ah - 70, 712, ah - 34], fill=(10, 16, 28))
    draw_rocket(adraw, 470, ah - 40, 0.7)
    img.paste(layer, (art[0], art[1]))
    draw.rectangle(art, outline=INK, width=2)
    # caption strip under the art
    cy = 520
    draw.text((36, cy + 8),
              "Shenzhou-24 lifts off from Jiuquan, Wednesday morning, and docks with Tiangong hours later.",
              font=F_SANS12, fill=GREY)

    # ---- divider ----
    draw.line([(36, 552), (W - 36, 552)], fill=INK, width=2)

    # ---- story grid: 2 columns x 3 rows ----
    col_w = (W - 72 - 24) // 2
    row_h = 132
    x0s = [36, 36 + col_w + 24]
    y0 = 566
    for idx, (kicker, head, body, icon) in enumerate(STORIES):
        cx = x0s[idx % 2]
        cy = y0 + (idx // 2) * row_h
        draw.rounded_rectangle([cx, cy, cx + col_w, cy + row_h - 12],
                               radius=8, fill=CARD_BG, outline=LIGHT_GREY)
        ix, iy = cx + 34, cy + 34
        ICONS[icon](draw, ix, iy, 22)
        tx = cx + 68
        draw.text((tx, cy + 12), kicker, font=F_SANS13B, fill=RED)
        hlines = wrap_text(draw, head, F_SANS_B19, col_w - 68 - 16)
        hy = cy + 30
        for line in hlines[:2]:
            draw.text((tx, hy), line, font=F_SANS_B19, fill=INK)
            hy += 22
        blines = wrap_text(draw, body, F_SANS14, col_w - 68 - 16)
        by = hy + 4
        for line in blines[:2]:
            draw.text((tx, by), line, font=F_SANS14, fill=GREY)
            by += 17

    # ---- footer ----
    draw.line([(36, 978), (W - 36, 978)], fill=LIGHT_GREY, width=1)
    draw.text((W / 2, 992),
              "Sources: Reuters  •  AP  •  CNN  •  BBC   —   All events of 25 November 2026",
              font=F_SANS12, fill=GREY, anchor="mm")

    img.save(OUT_PATH, "PNG", optimize=True)
    size = os.path.getsize(OUT_PATH)
    print(f"Wrote {OUT_PATH}: {img.size[0]}x{img.size[1]}, {size} bytes")


if __name__ == "__main__":
    main()
