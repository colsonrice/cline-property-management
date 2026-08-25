# Task: add a snow-removal before/after to the Cline site

Repo: `/Users/Web Projects/mike-property-management-site`
Live: https://clinepropertymgmt.com

Snow Removal is the only one of the seven services with no photography at all.
Mike has not sent winter photos yet. Build a **clearly labelled illustration**
of a snowfall before/after so the service page and the gallery aren't empty,
without implying it is a photograph of Cline's work.

---

## Non-negotiable: it must not read as a real job photo

The site currently asserts, in two places:

- `build/build.py` ~line 689 (home): "None of it is stock photography."
- `build/build.py` ~line 1055 (gallery): "Nothing here is stock photography."

Every other image on the site is a genuine Cline job. If you add a synthetic
image you **must** do all three of these:

1. **Caption and alt text say it is an illustration.** Not "our snow work."
   Something like "Illustration — how a trigger-depth clearing works." The word
   *illustration* must appear in the visible caption, not only in alt text.
2. **Amend those two sentences** so they stay true. Suggested rewrite:
   "Every photograph here is our own work on a real property. The one winter
   illustration is marked as such."
3. **Add a visible marker on the image itself** — a small corner badge reading
   `ILLUSTRATION`, baked into the rendered file, so it survives being
   right-clicked and saved or scraped into a search result.

If you cannot satisfy all three, stop and report back rather than shipping it.

Prefer a **diagrammatic / illustrated** treatment over photoreal. A stylised
rendering that is obviously a drawing is safer and ages better than a
photoreal fake, and it will sit fine next to the existing `winterscape()` SVG
already in `build/build.py`.

---

## Image specification — these constraints are load-bearing

The before/after component is a drag slider. It only reads as a *reveal* if the
two frames are registered. We already had to re-crop the mulch pair for exactly
this reason (see `build/recrop.sh`), so:

- **Both frames must be the identical scene from the identical viewpoint.**
  Same driveway, same house, same trees, same camera position and focal length.
  Only the snow differs: covered in `before`, cleared with visible plough edges
  and banked snow either side in `after`.
- **Aspect ratio must be exactly 3:4 portrait** and **identical between the two
  frames**. The slider box is `aspect-ratio: 3/4` in `site/assets/css/site.css`.
  Anything else gets cropped at the sides. Every other pair on the site is
  `600x800` at the 800w size — match that.

Content that makes it credible:
- Residential asphalt or concrete drive, Midwestern suburban house
- Overcast winter light, bare deciduous trees, dormant lawn under snow
- `after`: clean pavement, snow banked at the edges, a little residual scatter
  — not surgically perfect
- No people, no faces, no readable signage, no branded vehicle, no logos

## Files to produce

```
site/assets/img/snow-removal/snow-clearing-before-480.jpg   (and -800, -1280)
site/assets/img/snow-removal/snow-clearing-before-480.webp  (and -800, -1280)
site/assets/img/snow-removal/snow-clearing-after-480.jpg    (and -800, -1280)
site/assets/img/snow-removal/snow-clearing-after-480.webp   (and -800, -1280)
```

Match the existing encoding ladder:

```bash
sips -s format jpeg -s formatOptions 66 -Z 480  master.png --out out-480.jpg
sips -s format jpeg -s formatOptions 62 -Z 800  master.png --out out-800.jpg
sips -s format jpeg -s formatOptions 62 -Z 1280 master.png --out out-1280.jpg
cwebp -quiet -q 70 -resize 480 0  master.png -o out-480.webp
cwebp -quiet -q 70 -resize 800 0  master.png -o out-800.webp
cwebp -quiet -q 70 -resize 1280 0 master.png -o out-1280.webp
```

Verify both slugs come out at ratio `0.750`:

```bash
sips -g pixelWidth -g pixelHeight site/assets/img/snow-removal/snow-clearing-{before,after}-800.jpg
```

---

## Wiring it in

All content lives in `build/data.py`; `site/` is generated — never hand-edit it.

**1. `build/data.py`, the `snow-removal` entry in `SERVICES`:**

- Add a `beforeafter` list, same shape as the other services:
  `[("snow-removal", "snow-clearing-before", "snow-clearing-after", "<label>", "<note>")]`
  The label/note render under the slider. The note is where you say
  "Illustration, not a photograph."
- Add a `gallery` list with both slugs, before first.
- `needs_photos: True` currently makes the page header render the
  `winterscape()` SVG instead of a photo (`build/build.py` ~line 914). Decide
  whether to keep that — keeping it is fine and arguably better than promoting
  an illustration to hero.

**2. `build/build.py`:**

- Add `("snow-removal", "Snow Removal")` to the gallery `cats` list (~line 968).
- Add `"snow-removal"` to `CAT_ORDER` (~line 982) — put it after
  `"leaf-removal"` so the gallery runs in season order.
- Add `"snow-removal": "snow-removal"` to `CAT_OWNER` (~line 991).
- Amend the two "stock photography" sentences as described above.

**3. Captions:** if a slug is not listed in a service `gallery`, the gallery
sweeps it up and needs a caption in `GALLERY_EXTRA` in `build/data.py`.

---

## Ordering rules you must not break

The gallery was recently fixed and it is easy to regress:

- Pairs must render **before → after**, adjacent.
- Images group by category; a category must appear exactly once.
- Slugs ending `-before` / `-after` are paired automatically by the `sequenced()`
  helper in `page_gallery()`. **Name the files exactly as specified** and this
  works for free. Deviate and the pair will split.

---

## Verify before you commit

```bash
python3 build/build.py
python3 build/qa.py          # must end: PROBLEMS: none / WARNINGS: none
```

Then confirm by inspection, not assumption:

- The slider on `site/services/snow-removal.html` has `before` as the base
  layer and `after` as the `.ba__after` overlay.
- In `site/gallery.html`, the two snow tiles are adjacent, before first, inside
  a single `snow-removal` group.
- Both rendered images carry the visible `ILLUSTRATION` badge.
- Both files are ratio 0.750.

## Deploy

```bash
git add -A
git commit -m "Add a labelled snow-removal illustration and before/after"
git push origin main
git subtree push --prefix site origin gh-pages
```

Then verify live at https://clinepropertymgmt.com/services/snow-removal.html
(append `?x=1` to bypass GitHub's CDN cache).

---

## When Mike sends real winter photos

Replace the illustration rather than adding alongside it, restore the two
"stock photography" sentences to their original wording, and drop the
`ILLUSTRATION` badge. Real before/after of one snowfall — same driveway,
covered then cleared — is the single most valuable image this site is missing.
