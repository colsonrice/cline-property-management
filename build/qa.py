#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static QA sweep: links, images, meta, schema, headings, a11y basics."""

import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
sys.path.insert(0, os.path.join(ROOT, "build"))
from data import SITE as CFG  # noqa
# Project sites (e.g. GitHub Pages) live under a path prefix; strip it before
# comparing sitemap <loc> paths with on-disk file paths.
BASE_PATH = urlparse(CFG["base"]).path.rstrip("/")

problems = []
warnings = []


def prob(page, msg):
    problems.append(f"{page}: {msg}")


def warn(page, msg):
    warnings.append(f"{page}: {msg}")


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.imgs, self.srcsets = [], [], []
        self.h = []
        self.title = None
        self._in_title = False
        self.metas = {}
        self.ld = []
        self._in_ld = False
        self._ld_buf = ""
        self.labels = 0
        self.inputs = []
        self.langs = None
        self.canonical = None
        self.css = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.langs = a.get("lang")
        if tag == "title":
            self._in_title = True
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.imgs.append(a)
        if tag == "source" and a.get("srcset"):
            self.srcsets.append(a["srcset"])
        if tag in ("h1", "h2", "h3", "h4"):
            self.h.append(tag)
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.metas[k] = a.get("content", "")
        if tag == "link":
            if a.get("rel") == "canonical":
                self.canonical = a.get("href")
            if a.get("rel") == "stylesheet":
                self.css.append(a.get("href", ""))
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True
            self._ld_buf = ""
        if tag == "label":
            self.labels += 1
        if tag in ("input", "select", "textarea"):
            self.inputs.append(a)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_ld:
            self.ld.append(self._ld_buf)
            self._in_ld = False

    def handle_data(self, d):
        if self._in_title:
            self.title = (self.title or "") + d
        if self._in_ld:
            self._ld_buf += d


def check(path):
    rel = os.path.relpath(path, SITE)
    pdir = os.path.dirname(path)
    html = open(path, encoding="utf-8").read()
    p = P()
    p.feed(html)

    # Redirect stubs are intentionally bare: noindex, a canonical pointing at
    # the surviving page, and a meta refresh. Holding them to full-page SEO
    # rules just produces noise. Same for local-only scratch pages.
    is_stub = ('http-equiv="refresh"' in html and "noindex" in html)
    is_scratch = os.path.basename(rel).startswith("_")
    if is_stub or is_scratch:
        if is_stub and not p.canonical:
            prob(rel, "redirect stub without canonical")
        return

    # --- meta / seo
    if not p.title:
        prob(rel, "missing <title>")
    elif len(p.title) > 65 and "noindex" not in p.metas.get("robots", ""):
        warn(rel, f"title {len(p.title)} chars (>65 may truncate in SERPs)")
    noindex = "noindex" in p.metas.get("robots", "")
    d = p.metas.get("description", "")
    if not d:
        prob(rel, "missing meta description")
    elif not noindex and not (110 <= len(d) <= 165):
        warn(rel, f"meta description {len(d)} chars (ideal 110-165)")
    if not p.canonical:
        prob(rel, "missing canonical")
    if not p.langs:
        prob(rel, "missing <html lang>")
    for m in ("og:title", "og:description", "og:image", "twitter:card"):
        if m not in p.metas:
            prob(rel, f"missing {m}")

    # --- headings
    h1s = p.h.count("h1")
    if h1s == 0:
        prob(rel, "no <h1>")
    elif h1s > 1:
        prob(rel, f"{h1s} <h1> elements (should be 1)")

    # --- json-ld
    for i, blob in enumerate(p.ld):
        try:
            json.loads(blob)
        except Exception as e:
            prob(rel, f"JSON-LD block {i} invalid: {e}")

    # --- internal links
    for href in p.links:
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
            continue
        clean = unquote(urlparse(href).path)
        if not clean:
            continue
        target = os.path.normpath(os.path.join(pdir, clean))
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            prob(rel, f"broken link -> {href}")

    # --- images
    for a in p.imgs:
        src = a.get("src", "")
        if "alt" not in a:
            prob(rel, f"img missing alt attribute: {src}")
        if src and not src.startswith(("http", "data:")):
            t = os.path.normpath(os.path.join(pdir, unquote(src)))
            if not os.path.exists(t):
                prob(rel, f"missing image file -> {src}")
        if not a.get("loading") and not a.get("fetchpriority"):
            warn(rel, f"img without loading hint: {src}")
    for ss in p.srcsets:
        for cand in ss.split(","):
            u = cand.strip().split(" ")[0]
            if not u or u.startswith(("http", "data:")):
                continue
            t = os.path.normpath(os.path.join(pdir, unquote(u.split("?")[0])))
            if not os.path.exists(t):
                prob(rel, f"missing srcset file -> {u}")

    # --- css exists
    for c in p.css:
        if c.startswith("http"):
            continue
        t = os.path.normpath(os.path.join(pdir, c.split("?")[0]))
        if not os.path.exists(t):
            prob(rel, f"missing stylesheet -> {c}")

    # --- form labels
    named = [i for i in p.inputs if i.get("name") and i.get("type") != "hidden"]
    if named and p.labels < len([i for i in named if i.get("type") != "checkbox"]):
        warn(rel, "possible unlabelled form control")

    return p


def main():
    pages = []
    for r, _d, fs in os.walk(SITE):
        for f in fs:
            if f.endswith(".html"):
                pages.append(os.path.join(r, f))
    pages.sort()

    titles = {}
    descs = {}
    for pg in pages:
        p = check(pg)
        rel = os.path.relpath(pg, SITE)
        if p is None:          # redirect stub or scratch page
            continue
        if p.title:
            titles.setdefault(p.title.strip(), []).append(rel)
        dsc = p.metas.get("description", "")
        if dsc:
            descs.setdefault(dsc, []).append(rel)

    for t, ps in titles.items():
        if len(ps) > 1:
            prob("SEO", f"duplicate <title> across {ps}: {t[:50]}…")
    for dsc, ps in descs.items():
        if len(ps) > 1:
            prob("SEO", f"duplicate meta description across {ps}")

    # sitemap coverage
    sm = os.path.join(SITE, "sitemap.xml")
    if os.path.exists(sm):
        locs = re.findall(r"<loc>(.*?)</loc>", open(sm).read())
        paths = set()
        for l in locs:
            pp = urlparse(l).path
            if BASE_PATH and pp.startswith(BASE_PATH):
                pp = pp[len(BASE_PATH):] or "/"
            paths.add(pp if pp != "/" else "/index.html")
        indexable = {"/" + os.path.relpath(p, SITE).replace(os.sep, "/") for p in pages}
        indexable = {p for p in indexable if not p.endswith(("404.html", "thanks.html"))}

        def sitemap_exempt(relurl):
            """Redirect stubs and local scratch pages are excluded on purpose."""
            if os.path.basename(relurl).startswith("_"):
                return True
            fp = os.path.join(SITE, relurl.lstrip("/"))
            if not os.path.exists(fp):
                return False
            h = open(fp, encoding="utf-8").read()
            return 'http-equiv="refresh"' in h and "noindex" in h

        indexable = {p for p in indexable if not sitemap_exempt(p)}
        for p in sorted(indexable):
            alt = p.replace("/index.html", "/")
            if p not in paths and alt not in paths:
                warn("sitemap", f"not listed: {p}")

    print(f"Checked {len(pages)} pages\n")
    if problems:
        print(f"PROBLEMS ({len(problems)}):")
        for x in problems:
            print("  ✗", x)
    else:
        print("PROBLEMS: none")
    print()
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for x in warnings[:40]:
            print("  !", x)
        if len(warnings) > 40:
            print(f"  … +{len(warnings)-40} more")
    else:
        print("WARNINGS: none")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
