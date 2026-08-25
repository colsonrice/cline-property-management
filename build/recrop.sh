#!/bin/zsh
# Re-crop specific photos so before/after pairs register against each other.
#
# A drag slider only reads as a reveal when the two frames line up. Mike shot
# the mulch pair 46 minutes apart and moved between them, so the barrel planter
# slid sideways under the handle instead of the mulch changing. These crops pull
# both frames onto the bed, the stone edging and the sidewalk line, which is
# enough for the comparison to read.
#
# slug|source|crop w|crop h|crop x|crop y   (fractions of the original)
set -e
cd "$(dirname "$0")/.."
SRC=photos/originals
OUT=site/assets/img

CROPS=(
  "mulching/mulch-refresh-before|IMG_5473|0.74|0.74|0.13|0.13"
  "mulching/mulch-refresh-after|IMG_5477|0.74|0.74|0.04|0.22"
)

for row in "${CROPS[@]}"; do
  IFS='|' read -r dest name cw ch cx cy <<< "$row"
  src=""
  for ext in heic HEIC jpeg jpg; do
    [ -f "$SRC/$name.$ext" ] && src="$SRC/$name.$ext" && break
  done
  [ -z "$src" ] && { echo "  MISSING $name"; continue; }

  sips -s format jpeg -s formatOptions 95 -Z 2400 "$src" --out /tmp/_rc.jpg >/dev/null 2>&1
  ffmpeg -y -i /tmp/_rc.jpg \
    -vf "crop=iw*${cw}:ih*${ch}:iw*${cx}:ih*${cy}" -frames:v 1 /tmp/_rc_crop.png >/dev/null 2>&1

  for w in 480 800 1280; do
    sips -s format jpeg -s formatOptions 66 -Z $w /tmp/_rc_crop.png --out "$OUT/${dest}-${w}.jpg" >/dev/null 2>&1
    cwebp -quiet -q 70 -resize $w 0 /tmp/_rc_crop.png -o "$OUT/${dest}-${w}.webp" >/dev/null 2>&1
  done
  d=$(sips -g pixelWidth -g pixelHeight "$OUT/${dest}-800.jpg" 2>/dev/null | awk '/pixelWidth/{w=$2}/pixelHeight/{h=$2}END{print w"x"h}')
  echo "  recropped ${dest}  (800w = $d)"
done
