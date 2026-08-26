# Cline Property Management — website

Static marketing site for Cline Property Management (Whitestown, IN).
No framework, no build dependencies beyond Python + Pillow. Every page is
plain HTML served straight from disk, which is the fastest and most
SEO-friendly option for a local service business.

**Live:** https://clinepropertymgmt.com/

---

## Layout

```
build/
  data.py       all copy, services, service areas, FAQs, SEO strings
  build.py      generates the site pages, legacy redirects, sitemap.xml, and robots.txt
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

Most source photos are portrait-oriented, so the layouts are built portrait-first —
the hero and page headers are split (type in one column, photo in the other)
rather than full-bleed bands that would crop them badly.

## Deploying

`main` holds the source; the `gh-pages` branch holds the contents of `site/`.

```bash
python3 build/build.py && python3 build/qa.py
git add -A && git commit -m "Update site"
git push origin main
git subtree push --prefix site origin gh-pages
```

## Domain and indexing

`SITE["base"]` in `build/data.py` is the canonical production domain used by
Open Graph tags, the sitemap, and structured data. The `site/CNAME` file keeps
GitHub Pages on that domain. Leave `STAGING = False` for production builds;
temporary preview builds should set it to `True` so search engines do not index
the preview address.

## The contact form

The static site submits through FormSubmit to the business email address. After
the first submission, confirm the activation email once, then send a second test
submission and verify that both the message and reply address work correctly.
