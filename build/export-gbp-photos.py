#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export a photo set sized and cropped for a Google Business Profile.

Two things drive the choices here.

Google shows profile photos in a square grid and crops the cover to 16:9, so
anything whose subject sits near an edge gets cut. Composites are therefore
built at 3:2 with the seam dead centre, which survives a square crop with both
halves still visible.

Google also requires photos to represent the actual business. The four
AI-generated snow images on the website are deliberately excluded -- they are
the only four slugs on the site with no camera original behind them, and
posting them to a live business listing risks the profile itself.

Sources are the untouched originals, not the web renditions, which are capped
at 1280px.
"""
import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from imagemap import MAP  # noqa

ORIG = os.path.join(ROOT, "photos", "originals")
DEST = os.path.expanduser("~/Desktop/Cline-Google-Business-Photos")
SCRATCH = "/tmp/_gbp"

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

SLUG_TO_ORIG = {s: o for o, c, s in MAP}

# --- selection -------------------------------------------------------------
# Ordered strongest first; Google surfaces recent uploads prominently, so the
# order they get uploaded in matters.
PAIRS = [
    ("leaf-cleanup-blue-house-front",   "Fall cleanup - front lawn"),
    ("leaf-cleanup-pool-yard",          "Fall cleanup - pool surround"),
    ("leaf-cleanup-roadside-house",     "Fall cleanup - roadside lawn"),
    ("soft-wash-siding",                "Soft washing - vinyl siding"),
    ("driveway-pressure-washing",       "Pressure washing - driveway"),
    ("awning-pressure-washing",         "Pressure washing - metal awning"),
    ("leaf-cleanup-blue-house-driveway", "Fall cleanup - driveway"),
    ("mulch-refresh",                   "Mulching - bed refresh"),
    ("leaf-cleanup-blue-house-side",    "Fall cleanup - side yard"),
    ("pressure-wash-front-walk",        "Pressure washing - front walk"),
]

SINGLES = [
    ("lawn-mowing-striped-residential",    "Lawn mowing - striped residential lawn"),
    ("mulch-install-front-entry",          "Mulching - front entry beds"),
    ("hoa-entrance-mulch-harcourt-springs", "HOA entrance landscaping"),
    ("commercial-median-crew",             "Commercial median maintenance"),
    ("leaf-vacuum-truck-curb",             "Leaf removal - truck-mounted vacuum"),
    ("large-property-mowing-roadside",     "Large property mowing"),
    ("mulch-bed-brick-wall",               "Mulching - foundation bed"),
    ("leaf-removal-backpack-blower",       "Leaf removal - crew at work"),
    ("lawn-mowing-stripes-spring",         "Lawn mowing - spring cut"),
    ("commercial-median-landscape",        "Commercial roadside planting"),
    ("rough-mowing-overgrown-lot",         "Rough cutting - overgrown lot"),
    ("mulch-install-entry-walkway",        "Mulching - entry walkway"),
]


def load(slug):
    """Decode an original to RGB with EXIF rotation applied."""
    base = SLUG_TO_ORIG.get(slug)
    if not base:
        return None
    src = None
    for ext in ("heic", "HEIC", "jpeg", "jpg", "JPG", "png", "PNG"):
        p = os.path.join(ORIG, f"{base}.{ext}")
        if os.path.exists(p):
            src = p
            break
    if not src:
        return None
    if src.lower().endswith(".heic"):
        os.makedirs(SCRATCH, exist_ok=True)
        tmp = os.path.join(SCRATCH, base + ".jpg")
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "100",
                        src, "--out", tmp], capture_output=True)
        src = tmp
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)      # bake rotation; sips leaves it in metadata
    return im.convert("RGB")


def cover(im, w, h):
    """Fill w x h, cropping the overflow, centred."""
    return ImageOps.fit(im, (w, h), method=Image.LANCZOS, centering=(0.5, 0.5))


def label(draw, box, text, font, pad=14):
    """Small solid chip. Descriptive, not promotional -- Google strips images
    that are mostly marketing text, so this stays deliberately plain."""
    x, y = box
    tw = draw.textlength(text, font=font)
    th = font.size
    draw.rectangle([x, y, x + tw + pad * 2, y + th + pad * 1.3], fill=(18, 22, 15))
    draw.text((x + pad, y + pad * 0.55), text, font=font, fill=(255, 255, 255))


def build_pair(slug, name, idx):
    b = load(slug + "-before")
    a = load(slug + "-after")
    if b is None or a is None:
        print(f"  skip {slug}: missing source")
        return False

    # 3:2 overall, seam centred, so a square crop still shows both halves.
    W, H = 1800, 1200
    half = W // 2
    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    canvas.paste(cover(b, half, H), (0, 0))
    canvas.paste(cover(a, half, H), (half, 0))

    d = ImageDraw.Draw(canvas)
    d.line([(half, 0), (half, H)], fill=(255, 255, 255), width=5)
    f = ImageFont.truetype(FONT_BOLD, 40)
    label(d, (28, H - 90), "BEFORE", f)
    label(d, (half + 28, H - 90), "AFTER", f)

    out = os.path.join(DEST, "1-before-and-after",
                       f"{idx:02d}-{name.lower().replace(' - ', '-').replace(' ', '-')}.jpg")
    canvas.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    return True


def build_single(slug, name, idx):
    im = load(slug)
    if im is None:
        print(f"  skip {slug}: missing source")
        return False
    # Longest side 2000px keeps well clear of Google's 720px floor and the 5MB
    # ceiling, without shipping 24-megapixel phone files.
    im.thumbnail((2000, 2000), Image.LANCZOS)
    out = os.path.join(DEST, "2-best-work",
                       f"{idx:02d}-{name.lower().replace(' - ', '-').replace(' ', '-')}.jpg")
    im.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    return True


def main():
    for sub in ("1-before-and-after", "2-best-work"):
        os.makedirs(os.path.join(DEST, sub), exist_ok=True)

    print("Before / after composites")
    np = sum(build_pair(s, n, i) for i, (s, n) in enumerate(PAIRS, 1))
    print(f"  {np} written")

    print("Best work")
    ns = sum(build_single(s, n, i) for i, (s, n) in enumerate(SINGLES, 1))
    print(f"  {ns} written")

    # verification: every file inside Google's limits
    print("\nChecks")
    bad = 0
    for sub in ("1-before-and-after", "2-best-work"):
        for f in sorted(os.listdir(os.path.join(DEST, sub))):
            p = os.path.join(DEST, sub, f)
            kb = os.path.getsize(p) / 1024
            w, h = Image.open(p).size
            ok = (10 <= kb <= 5120) and min(w, h) >= 720
            if not ok:
                bad += 1
                print(f"  FAIL {f}: {w}x{h}, {kb:.0f}KB")
    print(f"  all within Google's limits (720px min, 10KB-5MB): {'yes' if bad == 0 else f'{bad} failed'}")
    print(f"\nSaved to {DEST}")


if __name__ == "__main__":
    main()
