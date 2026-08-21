# Cline Property Management — website

Static marketing site for Cline Property Management (Whitestown, IN).
No framework, no build dependencies beyond Python + Pillow. Every page is
plain HTML served straight from disk, which is the fastest and most
SEO-friendly option for a local service business.

**Live:** https://colsonrice.github.io/cline-property-management/

---

## Layout

```
build/
  data.py       all copy, services, service areas, FAQs, SEO strings
  build.py      generates the 18 HTML pages + sitemap.xml + robots.txt
  images.py     originals -> orientation-corrected JPG + WebP renditions
  imagemap.py   original filename -> category + web slug
  qa.py         link/image/meta/schema/heading/a11y sweep
  devserver.py  local preview with caching disabled
  manifest.json image dimensions written by images.py

site/           the built site — this folder is what gets deployed
photos/
  originals/    Mike's untouched phone photos (git-ignored, back these up)
```

## Working on it

```bash
python3 build/build.py     # regenerate all HTML
python3 build/qa.py        # must report 0 problems before deploying
python3 build/devserver.py 4180   # preview at http://localhost:4180
```

Re-run `python3 build/images.py` only when photos are added or changed —
it's the slow step.

### Adding photos

1. Drop the originals into `photos/originals/`.
2. Add a row to `MAP` in `build/imagemap.py`:
   `("IMG_1234", "mowing", "descriptive-web-slug")`
3. Add a caption in the relevant service's `gallery` list in `build/data.py`,
   or in `GALLERY_EXTRA` if it isn't tied to one service.
4. `python3 build/images.py && python3 build/build.py && python3 build/qa.py`

### Why images go through Pillow

iPhone photos store an EXIF *orientation flag* rather than rotated pixels, and
`cwebp` discards that flag — so a naive convert produces WebP files that render
sideways in the browser while the JPEG fallback looks fine. `images.py` bakes
the rotation into the pixels with `ImageOps.exif_transpose()` and strips EXIF,
so every rendition is correct in every format.

42 of the 44 source photos are 3:4 portrait, so the layouts are built
portrait-first — the hero and page headers are split (type in one column,
photo in the other) rather than full-bleed bands that would crop them badly.

## Deploying

`main` holds the source; the `gh-pages` branch holds the contents of `site/`.

```bash
python3 build/build.py && python3 build/qa.py
git add -A && git commit -m "Update site"
git push origin main
git subtree push --prefix site origin gh-pages
```

## Things to change when a real domain is ready

1. `SITE["base"]` in `build/data.py` — this drives every canonical tag,
   Open Graph URL, sitemap entry and schema block.
2. `python3 build/build.py` and redeploy.
3. Point the domain at GitHub Pages and add a `CNAME` file to `site/`.

## The contact form

Static hosting has no backend, so the form validates in the browser and then
hands the completed details to the visitor's mail client
(`build/build.py` sets `data-mode="mailto"` on the form).

To upgrade to a real form backend later, either deploy to Netlify — the
`data-netlify` attributes are already in place — or point the form at a
Formspree endpoint and change `data-mode` to `post`.
