#!/usr/bin/env python3
"""Render carousel slides (1080x1920) from a batch JSON file.

Usage: python3 tools/render.py content/batch-2026-10-w1.json
Output: images/<post_id>/slide_<n>.png
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FONTS = "/usr/share/fonts/truetype/google-fonts/"
NAVY_TOP, NAVY_BOT = (11, 18, 40), (22, 30, 64)
GOLD = (232, 196, 120)
WHITE = (244, 244, 248)
MUTED = (150, 160, 190)
MARGIN = 100


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def gradient():
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / H
        c = tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3))
        for x in range(W):
            px[x, y] = c
    return img


_BG = None


def background():
    global _BG
    if _BG is None:
        _BG = gradient()
    return _BG.copy()


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            test = (cur + " " + w).strip()
            if draw.textlength(test, font=fnt) <= max_w:
                cur = test
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def fit(draw, text, name, max_size, min_size, max_w, max_h, spacing=1.25):
    for size in range(max_size, min_size - 1, -4):
        fnt = font(name, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) * size * spacing <= max_h:
            return fnt, lines, size
    fnt = font(name, min_size)
    return fnt, wrap(draw, text, fnt, max_w), min_size


def moon(draw, cx, cy, r):
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GOLD)
    t = cy / H
    bg = tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3))
    draw.ellipse((cx - r + r // 2, cy - r - r // 6, cx + r + r // 2, cy + r - r // 6), fill=bg)


def render_slide(kind, slide, idx, total, out):
    img = background()
    d = ImageDraw.Draw(img)
    max_w = W - 2 * MARGIN

    if kind == "hook":
        moon(d, W // 2, 380, 90)
        fnt, lines, size = fit(d, slide["text"], "Poppins-Bold.ttf", 104, 64, max_w, 780)
        y = 640
        for ln in lines:
            w = d.textlength(ln, font=fnt)
            d.text(((W - w) / 2, y), ln, font=fnt, fill=WHITE)
            y += int(size * 1.25)
        sub = slide.get("sub")
        if sub:
            sf = font("Poppins-Medium.ttf", 44)
            y += 40
            for ln in wrap(d, sub, sf, max_w):
                w = d.textlength(ln, font=sf)
                d.text(((W - w) / 2, y), ln, font=sf, fill=GOLD)
                y += 62
        sw = font("Poppins-Medium.ttf", 40)
        t = "swipe"
        tw = d.textlength(t, font=sw)
        x0 = (W - (tw + 80)) / 2
        d.text((x0, H - 260), t, font=sw, fill=MUTED)
        ax, ay = x0 + tw + 20, H - 236
        d.line((ax, ay, ax + 50, ay), fill=MUTED, width=5)
        d.line((ax + 34, ay - 16, ax + 50, ay), fill=MUTED, width=5)
        d.line((ax + 34, ay + 16, ax + 50, ay), fill=MUTED, width=5)

    elif kind == "point":
        num = slide.get("label")
        y = 420
        if num:
            nf = font("Poppins-Bold.ttf", 64)
            d.text((MARGIN, y), num, font=nf, fill=GOLD)
            y += 130
        d.rectangle((MARGIN, y, MARGIN + 120, y + 8), fill=GOLD)
        y += 70
        hf, hl, hs = fit(d, slide["title"], "Poppins-Bold.ttf", 88, 56, max_w, 520)
        for ln in hl:
            d.text((MARGIN, y), ln, font=hf, fill=WHITE)
            y += int(hs * 1.25)
        y += 50
        bf, bl, bs = fit(d, slide["body"], "Poppins-Regular.ttf", 62, 42, max_w, H - y - 340, 1.4)
        for ln in bl:
            d.text((MARGIN, y), ln, font=bf, fill=(205, 210, 230))
            y += int(bs * 1.4)

    elif kind == "cta":
        moon(d, W // 2, 520, 90)
        fnt, lines, size = fit(d, slide["text"], "Poppins-Bold.ttf", 96, 60, max_w, 520)
        y = 760
        for ln in lines:
            w = d.textlength(ln, font=fnt)
            d.text(((W - w) / 2, y), ln, font=fnt, fill=WHITE)
            y += int(size * 1.25)
        sf = font("Poppins-Medium.ttf", 46)
        y += 40
        for ln in wrap(d, slide.get("sub", "Follow for daily sleep science"), sf, max_w):
            w = d.textlength(ln, font=sf)
            d.text(((W - w) / 2, y), ln, font=sf, fill=GOLD)
            y += 64

    # footer: source + slide counter
    ff = font("Poppins-Regular.ttf", 34)
    src = slide.get("source")
    if src:
        d.text((MARGIN, H - 150), src, font=ff, fill=MUTED)
    if kind != "hook":
        ct = f"{idx}/{total}"
        d.text((W - MARGIN - d.textlength(ct, font=ff), H - 110), ct, font=ff, fill=MUTED)
    img.save(out, optimize=True)


def main(path):
    batch = json.load(open(path))
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for post in batch["posts"]:
        outdir = os.path.join(root, "images", post["id"])
        os.makedirs(outdir, exist_ok=True)
        total = len(post["slides"])
        for i, s in enumerate(post["slides"], 1):
            kind = s.get("kind") or ("hook" if i == 1 else "cta" if i == total else "point")
            suffix = f"_r{post['rev']}" if post.get("rev") else ""
            render_slide(kind, s, i, total, os.path.join(outdir, f"slide_{i}{suffix}.png"))
        print("rendered", post["id"], total, "slides")


if __name__ == "__main__":
    main(sys.argv[1])
