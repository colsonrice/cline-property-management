#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image pipeline.

HEIC/JPEG originals -> orientation-baked, resized JPG + WebP renditions.

The important part: iPhone photos carry an EXIF orientation flag rather than
storing rotated pixels. cwebp drops that flag, so browsers render the WebP
sideways while the JPEG looks fine. We bake the rotation into the pixels with
ImageOps.exif_transpose() and strip EXIF entirely, so every rendition is
correct regardless of format or decoder.
"""

import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "photos", "originals")
OUT = os.path.join(ROOT, "site", "assets", "img")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imagemap import MAP, HEROES  # noqa

# Sources are 3:4 portrait, so "width" costs ~1.78x the pixels a landscape
# tier of the same number would. Tiers are chosen for the real display slots:
# 480 = card at 1x, 800 = card at 2x / hero column at 1x, 1280 = hero at 2x.
# No 1920 tier: nothing on the site displays an image wider than a 50vw column.
WIDTHS = [480, 800, 1280]
HERO_WIDTHS = [480, 800, 1280]
JPG_Q = {480: 74, 800: 70, 1280: 64}
WEBP_Q = {480: 72, 800: 66, 1280: 58}

# Fractional crops for comparison frames that need to register against each
# other. Keeping these in the main pipeline means a routine image rebuild
# cannot silently undo the aligned mulch before/after created for the slider.
# Values are crop width, crop height, left offset, and top offset.
CROPS = {
    "mulch-refresh-before": (0.74, 0.74, 0.13, 0.13),
    "mulch-refresh-after": (0.74, 0.74, 0.04, 0.22),
}

# These camera-roll exports are screenshots with solid black letterboxing
# around the actual photo. Trim only those known sources so the untouched
# iPhone originals elsewhere in the library keep their full frame.
LETTERBOX_TRIM = {
    "leaf-cleanup-blue-house-front-before", "leaf-cleanup-blue-house-front-after",
    "leaf-cleanup-blue-house-driveway-before", "leaf-cleanup-blue-house-driveway-after",
    "leaf-cleanup-blue-house-side-before", "leaf-cleanup-blue-house-side-after",
    "leaf-cleanup-pool-yard-before", "leaf-cleanup-pool-yard-after",
    "leaf-cleanup-roadside-house-before", "leaf-cleanup-roadside-house-after",
    "soft-wash-two-story-siding-before", "soft-wash-two-story-siding-after",
    "soft-wash-gray-siding-before", "soft-wash-gray-siding-after",
    "pressure-wash-front-walk-before", "pressure-wash-front-walk-after",
    "pressure-wash-outdoor-counter-before", "pressure-wash-outdoor-counter-after",
}


def find_src(name):
    for ext in ("heic", "HEIC", "jpeg", "jpg", "JPG", "png"):
        p = os.path.join(SRC, f"{name}.{ext}")
        if os.path.exists(p):
            return p
    return None


def load_upright(path):
    """Return a correctly-rotated RGB PIL image, EXIF stripped."""
    if path.lower().endswith((".heic",)):
        # Pillow has no HEIC decoder here; let sips produce a temp master.
        tmp = tempfile.mktemp(suffix=".jpg")
        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "100",
             "--resampleHeightWidthMax", "2600", path, "--out", tmp],
            check=True, capture_output=True)
        im = Image.open(tmp)
        im.load()
        os.unlink(tmp)
    else:
        im = Image.open(path)
        im.load()

    im = ImageOps.exif_transpose(im)          # bake rotation into pixels
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    elif im.mode == "L":
        im = im.convert("RGB")
    return im


def apply_crop(im, slug):
    """Apply a slug-specific fractional crop without changing aspect ratio."""
    spec = CROPS.get(slug)
    if not spec:
        return im
    cw, ch, cx, cy = spec
    w, h = im.size
    left, top = round(w * cx), round(h * cy)
    right, bottom = round(left + w * cw), round(top + h * ch)
    return im.crop((left, top, min(w, right), min(h, bottom)))


def trim_letterbox(im, slug):
    """Remove the solid black bars from known camera-roll screenshots."""
    if slug not in LETTERBOX_TRIM:
        return im
    light = im.convert("L").point(lambda p: 255 if p > 8 else 0)
    box = light.getbbox()
    return im.crop(box) if box else im


def main():
    manifest = {}
    made = 0
    for name, cat, slug in MAP:
        src = find_src(name)
        if not src:
            print("MISSING:", name)
            continue
        im = load_upright(src)
        im = apply_crop(trim_letterbox(im, slug), slug)
        w0, h0 = im.size
        os.makedirs(os.path.join(OUT, cat), exist_ok=True)

        widths = HERO_WIDTHS if slug in HEROES else WIDTHS
        emitted = []
        for w in widths:
            if w > w0:
                # never upscale; emit at native width instead
                tw, th = w0, h0
            else:
                tw = w
                th = max(1, round(h0 * (w / w0)))
            r = im.resize((tw, th), Image.LANCZOS)
            base = os.path.join(OUT, cat, f"{slug}-{w}")
            r.save(base + ".jpg", "JPEG", quality=JPG_Q[w], optimize=True, progressive=True)
            # cwebp beats Pillow's encoder on this material, but it must be fed a
            # LOSSLESS source -- handing it the JPEG above makes it spend bits
            # encoding JPEG artefacts and the result comes out bigger than the JPEG.
            png = base + ".tmp.png"
            r.save(png, "PNG", optimize=False, compress_level=1)
            subprocess.run(["cwebp", "-quiet", "-q", str(WEBP_Q[w]), "-m", "6",
                            "-sharp_yuv", png, "-o", base + ".webp"], check=True)
            os.unlink(png)
            emitted.append(w)
            made += 2

        manifest[slug] = {
            "cat": cat, "w": w0, "h": h0,
            "orient": "landscape" if w0 >= h0 else "portrait",
            "widths": emitted,
        }
        print(f"  {cat}/{slug}  {w0}x{h0} {'L' if w0>=h0 else 'P'}")

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)

    n_p = sum(1 for v in manifest.values() if v["orient"] == "portrait")
    print(f"\n{len(manifest)} images, {made} files")
    print(f"portrait: {n_p}   landscape: {len(manifest)-n_p}")


if __name__ == "__main__":
    main()
