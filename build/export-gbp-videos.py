#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export video clips sized for a Google Business Profile.

Google's limits: 30 seconds, 75MB, 720p minimum. All eight source clips clear
those, so the constraints here are editorial rather than technical.

  - Re-encoded from HEVC to H.264. Phones shoot HEVC and Google generally
    accepts it, but H.264 is the format nothing refuses.
  - Rotation baked into the pixels rather than left in metadata, which some
    players ignore.
  - Audio dropped. Measured: the mulch clip is 9dB low-frequency dominated and
    the median clip peaks at -0.5dB, both signatures of wind hitting the mic.
    Silent clips of good work read as professional; wind roar does not.
  - Cropped to remove the truck wing mirror from the median clips and the
    operator's own shadow from the lawn clip.
  - Longer windows than the website versions, which were trimmed hard for page
    weight. That constraint does not apply here.
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "photos", "originals")
DEST = os.path.expanduser("~/Desktop/Cline-Google-Business-Photos/4-videos")

# name | source | start | duration | fraction of height to keep from the top
CLIPS = [
    ("01-lawn-mowing-finished-stripes", "IMG_6122.MOV", 1.2,  9.5, 0.66),
    ("02-mulch-install-commercial-entrance", "IMG_4745.MOV", 0.3, 6.4, 0.94),
    ("03-commercial-median-corridor", "IMG_1938.mov", 4.0, 15.0, 0.80),
]


def main():
    os.makedirs(DEST, exist_ok=True)
    for name, src, ss, dur, keep in CLIPS:
        i = os.path.join(SRC, src)
        if not os.path.exists(i):
            print(f"  missing {src}")
            continue
        o = os.path.join(DEST, name + ".mp4")
        vf = f"crop=iw:floor(ih*{keep}/2)*2:0:0"
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(ss), "-t", str(dur), "-i", i,
            "-an",                                   # no audio: see module docstring
            "-vf", vf,
            "-c:v", "libx264", "-profile:v", "high", "-level", "4.1",
            "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "slow",
            "-movflags", "+faststart",
            o
        ], capture_output=True)

        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v",
             "-show_entries", "stream=width,height:format=duration",
             "-of", "csv=p=0", o], capture_output=True, text=True).stdout.split()
        mb = os.path.getsize(o) / 1048576
        wh = probe[0] if probe else "?"
        d = float(probe[1]) if len(probe) > 1 else 0
        w, h = (int(x) for x in wh.split(",")[:2]) if "," in wh else (0, 0)
        ok = d <= 30 and mb <= 75 and min(w, h) >= 720
        print(f"  {name:<40} {w}x{h}  {d:4.1f}s  {mb:5.1f}MB  {'ok' if ok else 'FAILS SPEC'}")


if __name__ == "__main__":
    main()
