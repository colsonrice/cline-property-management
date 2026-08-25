#!/usr/bin/env python3
"""Remove the baked-in ILLUSTRATION badge from the snow images.

The badge was stamped into the pixels so it would survive being saved or
scraped. It is being removed at the owner's direction; the disclosure still
runs in the caption under each slider ("Illustration, not a photograph") and
in the section copy, so the images are not presented as real photographs.

The badge sits on flat overcast sky. Each column inside the badge box is
rebuilt by interpolating vertically between clean pixels above and below it,
which keeps any vertical structure (a branch, a pole) continuous instead of
smearing it sideways.
"""
from PIL import Image
import os, subprocess, sys

D = "site/assets/img/snow-removal"
SLUGS = ["snow-clearing-before", "snow-clearing-after",
         "snow-parking-lot-before", "snow-parking-lot-after"]
MASTER = "-1280.jpg"


def badge_box(im):
    """Locate the badge by its yellow rule, with padding."""
    w, h = im.size
    px = im.load()
    ys, xs = [], []
    for y in range(0, int(h * 0.25)):
        for x in range(0, w):
            r, g, b = px[x, y]
            if r > 200 and g > 200 and b < 120:
                ys.append(y); xs.append(x)
    if not ys:
        return None
    pad = 10
    return (max(0, min(xs) - pad), max(0, min(ys) - pad),
            min(w, max(xs) + pad), min(h, max(ys) + pad))


def paint_out(im, box):
    x0, y0, x1, y1 = box
    px = im.load()
    top = max(0, y0 - 3)
    bot = min(im.size[1] - 1, y1 + 3)
    span = bot - top
    for x in range(x0, x1):
        a = px[x, top]
        b = px[x, bot]
        for y in range(y0, y1):
            t = (y - top) / span
            px[x, y] = (round(a[0] + (b[0] - a[0]) * t),
                        round(a[1] + (b[1] - a[1]) * t),
                        round(a[2] + (b[2] - a[2]) * t))
    return im


def main():
    for slug in SLUGS:
        src = os.path.join(D, slug + MASTER)
        if not os.path.exists(src):
            print("  missing", src); continue
        im = Image.open(src).convert("RGB")
        box = badge_box(im)
        if not box:
            print(f"  {slug}: no badge found, skipping"); continue
        im = paint_out(im, box)
        tmp = "/tmp/_debadge.png"
        im.save(tmp)
        for w in (480, 800, 1280):
            q = 66 if w == 480 else 62
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(q),
                            "-Z", str(w), tmp, "--out", os.path.join(D, f"{slug}-{w}.jpg")],
                           capture_output=True)
            subprocess.run(["cwebp", "-quiet", "-q", "70", "-resize", str(w), "0",
                            tmp, "-o", os.path.join(D, f"{slug}-{w}.webp")],
                           capture_output=True)
        print(f"  {slug}: badge removed at {box}, re-encoded 480/800/1280")


if __name__ == "__main__":
    main()
