#!/bin/zsh
# Transcode Mike's phone clips into web-deliverable loops.
#   - HEVC -> H.264 (Chrome/Firefox cannot play HEVC) + VP9 for smaller payloads
#   - rotation baked into pixels (metadata gets stripped by some CDNs/players)
#   - audio dropped: it is engine and wind noise, and muted is required for autoplay
#   - cropped to drop the truck mirror / operator shadow at the bottom of frame
set -e
cd "$(dirname "$0")/.."
SRC=photos/originals
OUT=site/assets/video

# slug|file|start|dur|keep-fraction-of-height
CLIPS=(
  "striped-lawn|IMG_6122.MOV|1.4|6.0|0.66"
  "mulch-entrance|IMG_4745.MOV|0.4|6.0|0.94"
  "median-corridor|IMG_1938.mov|5.0|6.0|0.80"
)

for row in "${CLIPS[@]}"; do
  IFS='|' read -r slug file ss dur keep <<< "$row"
  in="$SRC/$file"
  vf="crop=iw:floor(ih*${keep}/2)*2:0:0,scale=640:-2"

  ffmpeg -y -ss "$ss" -t "$dur" -i "$in" -an \
    -vf "$vf,fps=25" -c:v libx264 -profile:v main -level 4.0 -pix_fmt yuv420p \
    -crf 33 -preset veryslow -g 50 -movflags +faststart \
    "$OUT/${slug}.mp4" >/dev/null 2>&1


  # poster from ~1s in, so it matches what the loop opens on
  pt=$(python3 -c "print(round(float('$ss')+1.0,2))")
  ffmpeg -y -ss "$pt" -i "$in" -frames:v 1 -vf "$vf" "/tmp/${slug}_poster.png" >/dev/null 2>&1
  sips -s format jpeg -s formatOptions 62 "/tmp/${slug}_poster.png" --out "$OUT/${slug}-poster.jpg" >/dev/null 2>&1
  cwebp -quiet -q 68 "/tmp/${slug}_poster.png" -o "$OUT/${slug}-poster.webp" >/dev/null 2>&1

  d=$(ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0 "$OUT/${slug}.mp4")
  printf "  %-18s %-11s mp4 %5.0fKB  poster %4.0fKB\n" "$slug" "$d" \
    $(( $(stat -f%z "$OUT/${slug}.mp4") / 1024 )) \
    $(( $(stat -f%z "$OUT/${slug}-poster.webp") / 1024 ))
done
