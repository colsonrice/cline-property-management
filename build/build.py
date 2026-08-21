#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static site generator for Cline Property Management."""

import json
import os
import re
import shutil
import sys
from html import escape as esc

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import (SITE, SERVICES, AREAS, SEASONS, HOME_FAQS, PROCESS, MOW_AREAS,
                  GALLERY_EXTRA, STAGING)  # noqa

OUT = os.path.join(os.path.dirname(HERE), "site")
IMG = os.path.join(OUT, "assets", "img")

SVC_BY_SLUG = {s["slug"]: s for s in SERVICES}


def asset_ver(relpath):
    """Short content hash so CSS/JS changes bust caches on deploy."""
    import hashlib
    p = os.path.join(OUT, relpath)
    try:
        with open(p, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()[:8]
    except OSError:
        return "1"


CSS_V = asset_ver("assets/css/site.css")
JS_V = asset_ver("assets/js/site.js")

# Which images actually have a 1920 rendition
HERO_SIZES = set()
for _root, _dirs, _files in os.walk(IMG):
    for _f in _files:
        if _f.endswith("-1280.webp"):
            HERO_SIZES.add(_f[:-len("-1280.webp")])


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def rel(depth):
    return "../" * depth if depth else ""


def img_src(cat, slug, w):
    return f"assets/img/{cat}/{slug}-{w}"


def picture(cat, slug, alt, depth=0, sizes="100vw", cls="", eager=False,
            ratio=None, width=None, height=None):
    """Responsive <picture> with webp + jpg."""
    r = rel(depth)
    base = f"{r}assets/img/{cat}/{slug}"
    ws = [480, 800, 1280]
    webp = ", ".join(f"{base}-{w}.webp {w}w" for w in ws)
    jpg = ", ".join(f"{base}-{w}.jpg {w}w" for w in ws)
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    dim = ""
    if width and height:
        dim = f' width="{width}" height="{height}"'
    style = f' style="aspect-ratio:{ratio}"' if ratio else ""
    c = f' class="{cls}"' if cls else ""
    return (
        f'<picture{c}>'
        f'<source type="image/webp" srcset="{webp}" sizes="{sizes}">'
        f'<img src="{base}-800.jpg" srcset="{jpg}" sizes="{sizes}" '
        f'alt="{esc(alt)}" {loading} decoding="async"{dim}{style}>'
        f'</picture>'
    )


def icon(name, cls="card__ic"):
    p = {
        "mow": '<path d="M3 17h5l2-9h4l2 5h5"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="19" r="2"/>',
        "mulch": '<path d="M3 18c3-4 6-4 9 0s6 4 9 0"/><path d="M7 12l2-4 2 4"/><path d="M14 12l2-5 2 5"/>',
        "broom": '<path d="M14 3l7 7"/><path d="M5 21l6-6"/><path d="M9 12l3 3-5 5-4-1 1-4z"/>',
        "leaf": '<path d="M4 20c0-9 6-15 16-16 0 10-6 16-16 16z"/><path d="M4 20c4-4 7-6 12-8"/>',
        "snow": '<path d="M12 2v20M2 12h20M5 5l14 14M19 5L5 19"/>',
        "spray": '<path d="M7 8h6v13H7z"/><path d="M13 5h3M16 3v4"/><path d="M19 8l2 1M19 11l2 1M19 14l2 1"/>',
        "wash": '<path d="M4 20h16"/><path d="M6 20V9l6-5 6 5v11"/><path d="M10 20v-5h4v5"/>',
        "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
        "phone": '<path d="M4 4h4l2 5-2.5 1.5a12 12 0 0 0 6 6L15 14l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 3 5a1 1 0 0 1 1-1z"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3 7l9 6 9-6"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "check": '<path d="M4 12l5 5L20 6"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "shield": '<path d="M12 3l8 3v6c0 5-3.5 8.2-8 9-4.5-.8-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
        "route": '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.5 6H14a4 4 0 0 1 0 8H9a4 4 0 0 0 0 8h.5"/>',
    }[name]
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>')



def winterscape():
    """Graphic winter panel used where we have no real winter photography yet.

    viewBox is landscape-ish to match the header figure slot, so the horizon
    and tree line survive the `slice` crop at every breakpoint.
    """
    flakes = []
    for i in range(28):
        x = (i * 137.0) % 100
        r = 1.0 + (i % 4) * 0.5
        dur = 7 + (i % 5) * 2.6
        delay = -(i * 0.83) % 12
        flakes.append(
            f'<circle class="flake" cx="{x:.1f}%" cy="0" r="{r:.2f}" '
            f'style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s;'
            f'opacity:{0.28 + (i % 5) * 0.13:.2f}"/>')
    return (
        '<svg class="winterscape" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice" '
        'aria-hidden="true" focusable="false">'
        # tree line
        '<path d="M0 122 L28 96 L44 122 L74 88 L96 122 L128 100 L150 122 L184 84 '
        'L210 122 L244 102 L266 122 L302 90 L328 122 L360 100 L384 122 L420 86 '
        'L446 122 L482 102 L506 122 L542 94 L566 122 L600 108 L600 150 L0 150 Z" '
        'fill="#16242F" opacity=".5"/>'
        '<path class="sky-line" d="M0 124h600" opacity=".45"/>'
        # far snow field
        '<path class="drift-3" d="M0 140 C110 130 210 152 310 144 C410 136 512 156 600 142 '
        'L600 400 L0 400 Z" opacity=".5"/>'
        # cleared lane, converging
        '<path class="drift-2" d="M258 146 L342 146 L556 400 L44 400 Z" opacity=".5"/>'
        '<path d="M274 146 L326 146 L470 400 L130 400 Z" fill="#16242F" opacity=".24"/>'
        # banks either side
        '<path class="drift" d="M0 176 C86 156 168 196 258 178 L120 400 L0 400 Z" opacity=".93"/>'
        '<path class="drift" d="M600 172 C516 152 430 194 342 176 L492 400 L600 400 Z" opacity=".93"/>'
        '<path class="drift-2" d="M0 244 C66 226 132 262 190 250 L88 400 L0 400 Z" opacity=".72"/>'
        '<path class="drift-2" d="M600 238 C538 222 470 260 412 246 L516 400 L600 400 Z" opacity=".72"/>'
        # blade marks
        '<path class="sky-line" d="M292 178 L212 400 M310 178 L392 400" opacity=".16"/>'
        + "".join(flakes) +
        '</svg>')


SVC_ICON = {
    "lawn-mowing": "mow", "mulching": "mulch", "spring-fall-cleanups": "broom",
    "leaf-removal": "leaf", "snow-removal": "snow", "soft-washing": "spray",
    "pressure-washing": "wash",
}


# --------------------------------------------------------------------------
# chrome
# --------------------------------------------------------------------------
def head(title, desc, depth, canonical, og_img=None, extra_ld=None, page_cls="", noindex=False):
    r = rel(depth)
    og = og_img or "assets/img/mowing/lawn-mowing-striped-residential-800.jpg"
    ld = [local_business_ld()]
    if extra_ld:
        ld.extend(extra_ld)
    ld_tags = "\n".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f"""<!doctype html>
<html lang="en-US" class="{page_cls}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE['base']}{canonical}">
<meta name="robots" content="{'noindex,follow' if (noindex or STAGING) else 'index,follow,max-image-preview:large'}">
<meta name="theme-color" content="#1B3324">
<meta name="format-detection" content="telephone=yes">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE['base']}{canonical}">
<meta property="og:image" content="{SITE['base']}/{og}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE['base']}/{og}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..700,0..100,0..1;1,9..144,300..700,0..100,0..1&family=Archivo:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/site.css?v={CSS_V}">
<noscript><style>
  /* Scroll-reveal hides content until JS marks it visible. Without JS that
     would leave most of the page blank, so opt out of the animation entirely. */
  .rv,.rise{{opacity:1!important;transform:none!important;animation:none!important}}
  .seasons__panel[hidden]{{display:grid!important}}
</style></noscript>
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{r}assets/favicon.svg">
{ld_tags}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def local_business_ld():
    return {
        "@context": "https://schema.org",
        "@type": "LandscapingBusiness",
        "@id": SITE["base"] + "/#business",
        "name": SITE["name"],
        "url": SITE["base"] + "/",
        "telephone": SITE["phone_display"],
        "email": SITE["email"],
        "image": SITE["base"] + "/assets/img/mowing/lawn-mowing-striped-residential-800.jpg",
        "description": ("Full-service grounds care and property maintenance in Boone County, Indiana — "
                        "mowing, mulching, seasonal cleanups, leaf removal, snow removal, soft washing "
                        "and pressure washing for residential, commercial, HOA and municipal properties."),
        "address": {
            "@type": "PostalAddress",
            "addressLocality": SITE["city"],
            "addressRegion": SITE["region"],
            "addressCountry": "US",
        },
        "areaServed": [{"@type": "City", "name": f"{a}, IN"} for a in
                       ["Whitestown", "Zionsville", "Carmel", "Lebanon", "Brownsburg", "Advance", "Jamestown"]],
        "priceRange": "$$",
        "knowsAbout": [s["name"] for s in SERVICES],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Grounds care services",
            "itemListElement": [
                {"@type": "Offer",
                 "itemOffered": {"@type": "Service", "name": s["name"], "description": s["short"],
                                 "url": f"{SITE['base']}/services/{s['slug']}.html"}}
                for s in SERVICES
            ],
        },
    }


def breadcrumb_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n,
             "item": SITE["base"] + u} for i, (n, u) in enumerate(items)
        ],
    }


def faq_ld(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
        ],
    }


def logo(depth=0):
    return ('<svg class="brand__mark" viewBox="0 0 40 40" fill="none" aria-hidden="true">'
            '<rect width="40" height="40" rx="3" fill="#1B3324"/>'
            '<path d="M20 8c0 7-4 10-4 14a4 4 0 0 0 8 0c0-4-4-7-4-14z" fill="#D2A03E"/>'
            '<path d="M11 27c3.5 2.4 5.8 3.2 9 3.2s5.5-.8 9-3.2" stroke="#7C9A84" '
            'stroke-width="1.8" stroke-linecap="round"/>'
            '<path d="M11 31.5c3.5 2.4 5.8 3.2 9 3.2s5.5-.8 9-3.2" stroke="#7C9A84" '
            'stroke-width="1.8" stroke-linecap="round" opacity=".55"/></svg>')


def header(depth, active=""):
    r = rel(depth)
    svc_links = "".join(
        f'<a href="{r}services/{s["slug"]}.html">{esc(s["nav"])}</a>' for s in SERVICES)
    area_links = "".join(
        f'<a href="{r}service-areas/{a["slug"]}.html">{esc(a["name"])}, IN</a>' for a in AREAS)

    def cur(k):
        return ' aria-current="page"' if active == k else ""

    drawer_svc = "".join(
        f'<a href="{r}services/{s["slug"]}.html">{esc(s["nav"])}</a>' for s in SERVICES)
    drawer_area = "".join(
        f'<a href="{r}service-areas/{a["slug"]}.html">{esc(a["name"])}, IN</a>' for a in AREAS)

    return f"""<header class="hdr">
<div class="hdr__in">
  <a class="brand" href="{r}index.html" aria-label="{esc(SITE['name'])} — home">
    {logo(depth)}
    <span class="brand__txt">
      <span class="brand__name">Cline</span>
      <span class="brand__sub">Property Management</span>
    </span>
  </a>
  <nav class="nav" aria-label="Primary">
    <div class="has-sub">
      <a href="{r}services/index.html"{cur('services')}>Services</a>
      <div class="sub">{svc_links}</div>
    </div>
    <div class="has-sub">
      <a href="{r}service-areas/index.html"{cur('areas')}>Service Areas</a>
      <div class="sub">{area_links}</div>
    </div>
    <a href="{r}gallery.html"{cur('gallery')}>Our Work</a>
    <a href="{r}about.html"{cur('about')}>About</a>
    <a href="{r}contact.html"{cur('contact')}>Contact</a>
  </nav>
  <div class="hdr__cta">
    <a class="tel" href="tel:{SITE['phone_href']}">{icon('phone','')}<span>{SITE['phone_display']}</span></a>
    <a class="btn btn--primary" href="{r}contact.html">Free Estimate</a>
    <button class="burger" aria-expanded="false" aria-controls="drawer" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</div>
<div class="drawer" id="drawer">
  <div class="drawer__grp">Services</div>
  {drawer_svc}
  <div class="drawer__grp">Service Areas</div>
  {drawer_area}
  <div class="drawer__grp">Company</div>
  <a href="{r}gallery.html">Our Work</a>
  <a href="{r}about.html">About</a>
  <a href="{r}contact.html">Contact</a>
  <a class="btn btn--primary" href="tel:{SITE['phone_href']}">Call {SITE['phone_display']}</a>
</div>
</header>
"""


def footer(depth):
    r = rel(depth)
    svc = "".join(f'<li><a href="{r}services/{s["slug"]}.html">{esc(s["nav"])}</a></li>' for s in SERVICES)
    area = "".join(f'<li><a href="{r}service-areas/{a["slug"]}.html">{esc(a["name"])}, IN</a></li>' for a in AREAS)
    return f"""<footer class="ftr">
<div class="wrap">
  <div class="ftr__top">
    <div class="ftr__brand">
      <a class="brand" href="{r}index.html" aria-label="{esc(SITE['name'])} — home">
        {logo(depth)}
        <span class="brand__txt">
          <span class="brand__name">Cline</span>
          <span class="brand__sub">Property Management</span>
        </span>
      </a>
      <p class="ftr__blurb">Year-round grounds care for homes, businesses, HOAs and municipalities
      across Boone County and the northwest side of Indianapolis.</p>
    </div>
    <div>
      <h4>Services</h4>
      <ul>{svc}</ul>
    </div>
    <div>
      <h4>Service Areas</h4>
      <ul>{area}</ul>
      <h4 style="margin-top:1.6rem">Company</h4>
      <ul>
        <li><a href="{r}gallery.html">Our Work</a></li>
        <li><a href="{r}about.html">About</a></li>
        <li><a href="{r}contact.html">Contact</a></li>
      </ul>
    </div>
    <div>
      <h4>Get In Touch</h4>
      <div class="ftr__nap">
        <a href="tel:{SITE['phone_href']}">{icon('phone','')}<span>{SITE['phone_display']}</span></a>
        <a href="mailto:{SITE['email']}">{icon('mail','')}<span>Email us</span></a>
        <span style="display:inline-flex;gap:.5rem;align-items:flex-start;color:var(--sage-dim);font-size:.92rem">
          {icon('pin','')}<span>{esc(SITE['city'])}, {SITE['region']} &middot; serving {esc(SITE['county'])}<br>and NW Indianapolis</span>
        </span>
      </div>
      <a class="btn btn--primary" style="margin-top:1.3rem" href="{r}contact.html">
        Request an Estimate {icon('arrow','arw')}
      </a>
    </div>
  </div>
  <div class="ftr__bot">
    <span>&copy; <span data-year>2026</span> {esc(SITE['name'])}. All rights reserved.</span>
    <span>Mowing service area: {esc(SITE['areas_short'])}</span>
  </div>
</div>
</footer>
<div class="callbar">
  <a class="btn btn--solid-dark" href="tel:{SITE['phone_href']}">{icon('phone','')} Call</a>
  <a class="btn btn--primary" href="{r}contact.html">Free Estimate</a>
</div>
<script src="{r}assets/js/site.js?v={JS_V}" defer></script>
</body>
</html>
"""


def crumbs(items, depth):
    r = rel(depth)
    out = []
    for i, (name, href) in enumerate(items):
        if href:
            out.append(f'<a href="{r}{href}">{esc(name)}</a>')
        else:
            out.append(f'<span aria-current="page">{esc(name)}</span>')
        if i < len(items) - 1:
            out.append('<span class="sep">/</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(out)}</nav>'


def cta_band(depth, cat="mowing", slug="large-property-mowing-roadside",
             head_txt="Let's get your property on the schedule.",
             sub="Free estimates. Straight answers. A crew that shows up when we said we would."):
    r = rel(depth)
    return f"""<section class="cta-band">
  <div class="cta-band__bg">{picture(cat, slug, "", depth, sizes="100vw")}</div>
  <div class="wrap"><div class="cta-band__in">
    <span class="eyebrow" style="color:var(--gold)">Get started</span>
    <h2 class="display h-1 rv">{esc(head_txt)}</h2>
    <p class="rv rv-d1">{esc(sub)}</p>
    <div class="cta-band__acts rv rv-d2">
      <a class="btn btn--primary" href="{r}contact.html">Request an Estimate {icon('arrow','arw')}</a>
      <a class="btn btn--ghost" href="tel:{SITE['phone_href']}">{icon('phone','')} {SITE['phone_display']}</a>
    </div>
  </div></div>
</section>"""


def faq_block(faqs, title="Common questions"):
    items = "".join(
        f'<details><summary>{esc(q)}<span class="pm"></span></summary>'
        f'<div class="faq__a"><p>{esc(a)}</p></div></details>'
        for q, a in faqs)
    return f"""<div class="shead"><span class="eyebrow">FAQ</span>
  <h2 class="display h-2">{esc(title)}</h2></div>
  <div class="faq rv">{items}</div>"""


def ba_block(cat, before, after, label, note, depth):
    return f"""<div class="rv">
  <div class="ba" role="slider" tabindex="0" aria-label="{esc(label)} before and after comparison"
       aria-valuemin="0" aria-valuemax="100" aria-valuenow="50" aria-valuetext="Half before, half after">
    {picture(cat, before, f"{label} before", depth, sizes="(max-width:820px) 92vw, 560px")}
    {picture(cat, after, f"{label} after", depth, sizes="(max-width:820px) 92vw, 560px", cls="ba__after")}
    <span class="ba__tag ba__tag--b">Before</span>
    <span class="ba__tag ba__tag--a">After</span>
    <span class="ba__handle"><span class="ba__grip">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
           stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l-5 6 5 6M15 6l5 6-5 6"/></svg>
    </span></span>
  </div>
  <div class="ba-cap"><b>{esc(label)}</b><span>{esc(note)}</span></div>
</div>"""


def render_body(blocks, depth):
    out = []
    for kind, val in blocks:
        if kind == "h2":
            out.append(f"<h2>{esc(val)}</h2>")
        elif kind == "p":
            out.append(f"<p>{esc(val)}</p>")
        elif kind == "ul":
            lis = "".join(f"<li>{esc(x)}</li>" for x in val)
            out.append(f"<ul>{lis}</ul>")
        elif kind == "cards":
            cs = "".join(
                f'<div class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in val)
            out.append(f'</div><div class="grid g-2 rv" style="margin:2rem 0">{cs}</div><div class="prose">')
    return "".join(out)


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------
def page_home():
    depth = 0
    title = "Lawn Care & Property Maintenance in Whitestown, IN | Cline"
    desc = ("Year-round grounds care in Whitestown, Zionsville and West Carmel, Indiana. Mowing, mulch, "
            "cleanups, leaf and snow removal, plus soft and pressure washing.")

    # season rail
    rail = ""
    panels = ""
    for i, s in enumerate(SEASONS):
        rail += (f'<button class="season" role="tab" aria-selected="false" '
                 f'style="--seas:{s["color"]}" id="seas-{s["key"]}" aria-controls="panel-{s["key"]}">'
                 f'<span class="season__mo">{esc(s["months"])}</span>'
                 f'<span class="season__nm">{esc(s["name"])}</span>'
                 f'<span class="season__ct">{esc(s["count"])}</span></button>')
        chips = "".join(
            f'<a class="chip" href="services/{sl}.html"><span class="dot"></span>{esc(SVC_BY_SLUG[sl]["name"])}</a>'
            for sl in s["services"])
        cat, slug, alt = s["img"]
        panels += f"""<div class="seasons__panel" id="panel-{s['key']}" role="tabpanel"
             aria-labelledby="seas-{s['key']}" style="--seas:{s['color']}" hidden>
          <div class="seasons__body">
            <span class="eyebrow eyebrow--plain" style="color:{s['color']}">{esc(s['months'])}</span>
            <h3 style="margin-top:.5rem">{esc(s['head'])}</h3>
            <p>{esc(s['body'])}</p>
            <div class="seasons__list">{chips}</div>
          </div>
          <div class="seasons__fig">{picture(cat, slug, alt, depth, sizes="(max-width:860px) 92vw, 46vw")}</div>
        </div>"""

    svc_rows = ""
    for i, s in enumerate(SERVICES):
        svc_rows += f"""<a class="svc-row" href="services/{s['slug']}.html">
      <span class="svc-row__no">{i+1:02d}</span>
      <span class="svc-row__nm display">{esc(s['name'])}</span>
      <span class="svc-row__ds">{esc(s['short'])}</span>
      <span class="svc-row__go">{icon('arrow','')}</span>
    </a>"""

    area_cards = "".join(
        f'''<a class="area" href="service-areas/{a['slug']}.html">
          {icon('pin','area__pin')}
          <span class="area__nm display">{esc(a['name'])}</span>
          <span class="area__mt">{esc(a['blurb'][:78])}…</span>
        </a>''' for a in AREAS)

    steps = "".join(
        f'<div class="step"><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></div>' for t, d in PROCESS)

    ba = "".join([
        ba_block("pressure-washing", "driveway-pressure-washing-before",
                 "driveway-pressure-washing-after", "Driveway wash",
                 "Same driveway, same day — 10:40am and 2:04pm", depth),
        ba_block("soft-washing", "soft-wash-siding-before", "soft-wash-siding-after",
                 "Siding soft wash", "Algae on a shaded elevation, removed at low pressure", depth),
        ba_block("mulching", "mulch-refresh-before", "mulch-refresh-after", "Bed refresh",
                 "Edges re-cut and topped with fresh hardwood mulch", depth),
    ])

    ld = [breadcrumb_ld([("Home", "/")]), faq_ld(HOME_FAQS)]

    return head(title, desc, depth, "/", extra_ld=ld) + header(depth) + f"""
<main id="main">

<section class="hero-s">
  <div class="hero-s__grid">
    <div class="hero-s__body">
      <span class="hero-s__kicker rise d1"><span class="dot"></span>{esc(SITE['areas_short'])}</span>
      <h1 class="display h-hero rise d2">Grounds care for <em>every season</em>.</h1>
      <p class="hero-s__lede rise d3">Mowing, mulch, leaves and snow &mdash; handled by one crew, on a schedule
        you can actually plan around. Homes, businesses, HOAs and municipalities across Boone County.</p>
      <div class="hero-s__acts rise d4">
        <a class="btn btn--primary" href="contact.html">Get a Free Estimate {icon('arrow','arw')}</a>
        <a class="btn btn--ghost" href="tel:{SITE['phone_href']}">{icon('phone','')} {SITE['phone_display']}</a>
      </div>
      <div class="hero-s__foot rise d5">
        <div class="hero-s__stat"><b>Residential &amp; Commercial</b><span>Homes, retail, office</span></div>
        <div class="hero-s__stat"><b>HOA &amp; Municipal</b><span>Common areas, right-of-way</span></div>
        <div class="hero-s__stat"><b>Year-Round</b><span>Mowing through snow</span></div>
      </div>
    </div>
    <div class="hero-s__fig">
      {picture('mowing','lawn-mowing-striped-residential',
        'Freshly mowed and striped residential lawn in Zionsville, Indiana', depth,
        sizes="(max-width:900px) 100vw, 50vw", eager=True)}
      <div class="hero-s__badge">
        <b>Zionsville, IN</b>
        <span>Weekly cut, edged and blown off &mdash; every visit</span>
      </div>
    </div>
  </div>
</section>

<!-- SEASONS -->
<section class="section">
  <div class="wrap">
    <div class="shead">
      <div class="shead__top">
        <div>
          <span class="eyebrow">The whole year</span>
          <h2 class="display h-1" style="margin-top:.7rem">What your property<br>needs right now</h2>
        </div>
        <p>Most companies handle one slice of the year. We're on the property in all four —
        which means nothing falls through the gap between vendors.</p>
      </div>
    </div>
    <div class="seasons rv">
      <div class="seasons__rail" role="tablist" aria-label="Services by season">{rail}</div>
      {panels}
    </div>
  </div>
</section>

<!-- SERVICES -->
<section class="section on-dark">
  <div class="wrap">
    <div class="shead">
      <div class="shead__top">
        <div>
          <span class="eyebrow">What we do</span>
          <h2 class="display h-1" style="margin-top:.7rem">Seven services,<br>one phone number</h2>
        </div>
        <p>Everything below is done by our own crew. You're not being handed off to a
        subcontractor you've never met.</p>
      </div>
    </div>
    <div class="svc-list rv">{svc_rows}</div>
  </div>
</section>

<!-- BEFORE / AFTER -->
<section class="section">
  <div class="wrap">
    <div class="shead">
      <div class="shead__top">
        <div>
          <span class="eyebrow">Real jobs</span>
          <h2 class="display h-1" style="margin-top:.7rem">Drag to see<br>the difference</h2>
        </div>
        <p>Every photo on this site is our own work on real properties around Boone County.
        No stock photography, no other company's portfolio.</p>
      </div>
    </div>
    <div class="grid g-3">{ba}</div>
  </div>
</section>

<!-- COMMERCIAL -->
<section class="section rule-top">
  <div class="wrap">
    <div class="split">
      <div class="split__fig stackfig rv">
        <div class="stackfig__a">{picture('commercial','commercial-median-crew',
          'Crew in high-visibility gear maintaining a commercial road median', depth,
          sizes="(max-width:820px) 92vw, 46vw")}</div>
        <div class="stackfig__b">{picture('commercial','commercial-median-sunset',
          'Commercial median planting at sunset', depth, sizes="(max-width:820px) 46vw, 24vw")}</div>
      </div>
      <div class="rv rv-d1">
        <span class="eyebrow">Commercial · HOA · Municipal</span>
        <h2 class="display h-1" style="margin-top:.9rem">Work that has to be<br>right in public.</h2>
        <div class="prose" style="margin-top:1.2rem">
          <p>Median and right-of-way work happens in live traffic, on a schedule, in high-visibility gear.
          HOA entrances are the first thing residents see every day. Commercial frontage is a customer's
          first impression before they reach the door.</p>
          <p>That work carries different expectations than a back yard, and we run it accordingly —
          scheduled rotations, written scope, and certificates of insurance on file before we start.</p>
        </div>
        <div class="grid g-2" style="margin-top:1.8rem;gap:1rem">
          <div class="card">{icon('route')}<h3>Scheduled rotations</h3>
            <p>Contracted properties run on a set cycle, not a call-when-you-notice basis.</p></div>
          <div class="card">{icon('shield')}<h3>Insured &amp; documented</h3>
            <p>COIs available on request — standard for HOA boards and property managers.</p></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- AREAS -->
<section class="section on-dark">
  <div class="wrap">
    <div class="shead">
      <div class="shead__top">
        <div>
          <span class="eyebrow">Where we work</span>
          <h2 class="display h-1" style="margin-top:.7rem">Close to home,<br>on purpose</h2>
        </div>
        <p><strong style="color:var(--bone)">Mowing routes</strong> stay inside Whitestown, Zionsville and
        West Carmel so we can hold a reliable day-of-week schedule. Our other services travel further
        across Boone County — worth asking.</p>
      </div>
    </div>
    <div class="areas rv">{area_cards}</div>
  </div>
</section>

<!-- PROCESS -->
<section class="section">
  <div class="wrap wrap--tight">
    <div class="shead"><span class="eyebrow">How it works</span>
      <h2 class="display h-1">Four steps, no runaround</h2></div>
    <div class="steps rv">{steps}</div>
  </div>
</section>

<!-- FAQ -->
<section class="section rule-top">
  <div class="wrap wrap--tight">{faq_block(HOME_FAQS)}</div>
</section>

{cta_band(depth)}
</main>
""" + footer(depth)


def page_services_index():
    depth = 1
    title = "Our Services | Lawn, Mulch, Snow & Washing | Cline"
    desc = ("Seven grounds care services for Boone County, Indiana: lawn mowing, mulching, seasonal "
            "cleanups, leaf removal, snow removal, soft washing and pressure washing.")
    cards = ""
    for s in SERVICES:
        cat, slug = s["hero"]
        cards += f"""<a class="pcard rv" href="{s['slug']}.html">
      {picture(cat, slug, s['hero_alt'], depth, sizes="(max-width:700px) 92vw, 30vw")}
      <span class="pcard__cap"><b>{esc(s['name'])}</b><span>{esc(s['short'])}</span></span>
    </a>"""
    ld = [breadcrumb_ld([("Home", "/"), ("Services", "/services/")])]
    return head(title, desc, depth, "/services/", extra_ld=ld) + header(depth, "services") + f"""
<main id="main">
<section class="phead">
  <div class="phead__grid">
    <div class="phead__in">
    {crumbs([("Home","index.html"),("Services",None)], depth)}
    <span class="eyebrow" style="color:var(--gold)">Services</span>
    <h1 class="display h-1">Everything the property needs, from one crew.</h1>
    <p>Seven services covering all four seasons — so you're not chasing a different vendor
    every time the weather changes.</p>
    </div>
    <div class="phead__fig">{picture('mulching','mulch-install-front-entry','',depth,sizes="(max-width:900px) 100vw, 46vw")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g-3">{cards}</div>
  </div>
</section>

<section class="section on-dark rule-top">
  <div class="wrap wrap--tight">{faq_block(HOME_FAQS, "Questions we get a lot")}</div>
</section>

{cta_band(depth)}
</main>
""" + footer(depth)


def page_service(s):
    depth = 1
    cat, hslug = s["hero"]
    ld = [
        breadcrumb_ld([("Home", "/"), ("Services", "/services/"),
                       (s["name"], f"/services/{s['slug']}.html")]),
        {
            "@context": "https://schema.org", "@type": "Service",
            "name": s["name"], "description": s["desc"],
            "serviceType": s["name"],
            "provider": {"@id": SITE["base"] + "/#business"},
            "areaServed": [{"@type": "City", "name": f"{a}, IN"} for a in
                           (MOW_AREAS if s["slug"] == "lawn-mowing" else
                            ["Whitestown", "Zionsville", "Carmel", "Lebanon", "Brownsburg"])],
            "url": f"{SITE['base']}/services/{s['slug']}.html",
        },
    ]
    if s.get("faqs"):
        ld.append(faq_ld(s["faqs"]))

    body = f'<div class="prose rv">{render_body(s["body"], depth)}</div>'

    ba = ""
    if s.get("beforeafter"):
        blocks = "".join(ba_block(c, b, a, l, n, depth) for c, b, a, l, n in s["beforeafter"])
        cls = "g-2" if len(s["beforeafter"]) > 1 else "g-2"
        ba = f"""<section class="section rule-top">
      <div class="wrap">
        <div class="shead"><span class="eyebrow">Before &amp; after</span>
          <h2 class="display h-2">Drag the handle</h2></div>
        <div class="grid {cls}">{blocks}</div>
      </div></section>"""

    gal = ""
    if s.get("gallery"):
        figs = "".join(
            f'<a class="pcard rv" href="../gallery.html">'
            f'{picture(c, sl, alt, depth, sizes="(max-width:700px) 92vw, 30vw")}'
            f'<span class="pcard__cap"><span>{esc(alt)}</span></span></a>'
            for c, sl, alt in s["gallery"])
        gal = f"""<section class="section">
      <div class="wrap">
        <div class="shead"><span class="eyebrow">Our work</span>
          <h2 class="display h-2">{esc(s['name'])} around Boone County</h2></div>
        <div class="grid g-3">{figs}</div>
      </div></section>"""

    area_note = ""
    if s.get("area_note"):
        area_note = f"""<div class="pricebox rv" style="margin-top:2rem">
      <span class="tag">Mowing service area</span>
      <p style="margin-top:.8rem">Our mowing routes cover <strong>{esc(", ".join(MOW_AREAS))}</strong>.
      Keeping the route tight is what lets us hold a consistent day-of-week schedule.
      Our other services travel further — if you're outside these three, it's still worth calling.</p>
    </div>"""

    photo_note = ""
    if s.get("needs_photos"):
        photo_note = ""

    faqs = ""
    if s.get("faqs"):
        faqs = f'<section class="section on-dark"><div class="wrap wrap--tight">{faq_block(s["faqs"])}</div></section>'

    others = "".join(
        f'<a class="chip" href="{o["slug"]}.html"><span class="dot"></span>{esc(o["name"])}</a>'
        for o in SERVICES if o["slug"] != s["slug"])

    return head(s["title"], s["desc"], depth, f"/services/{s['slug']}.html",
                og_img=f"assets/img/{cat}/{hslug}-800.jpg", extra_ld=ld) + header(depth, "services") + f"""
<main id="main">
<section class="phead{' phead--winter' if s.get('needs_photos') else ''}">
  <div class="phead__grid">
    <div class="phead__in">
    {crumbs([("Home","index.html"),("Services","services/index.html"),(s['name'],None)], depth)}
    <span class="eyebrow" style="color:var(--gold)">{esc(SITE['areas_short'])}</span>
    <h1 class="display h-1">{esc(s['name'])}</h1>
    <p>{esc(s['lede'])}</p>
    <div class="hero__acts" style="margin-top:.6rem">
      <a class="btn btn--primary" href="../contact.html?service={s['slug']}">Get a Free Estimate {icon('arrow','arw')}</a>
      <a class="btn btn--ghost" href="tel:{SITE['phone_href']}">{icon('phone','')} {SITE['phone_display']}</a>
    </div>
    </div>
    <div class="phead__fig">{winterscape() if s.get('needs_photos') else picture(cat, hslug, "", depth, sizes="(max-width:900px) 100vw, 46vw", eager=True)}</div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--tight">
    {body}
    {area_note}
    {photo_note}
  </div>
</section>

{ba}
{gal}
{faqs}

<section class="section rule-top">
  <div class="wrap wrap--tight" style="text-align:center">
    <span class="eyebrow eyebrow--plain" style="justify-content:center">Also available</span>
    <h2 class="display h-2" style="margin:.7rem 0 1.4rem">Other services</h2>
    <div class="seasons__list" style="justify-content:center">{others}</div>
  </div>
</section>

{cta_band(depth)}
</main>
""" + footer(depth)


def page_areas_index():
    depth = 1
    title = "Service Areas | Whitestown, Zionsville & West Carmel IN"
    desc = ("Cline Property Management serves Whitestown, Zionsville and West Carmel, Indiana with "
            "mowing, mulch, cleanups, leaf and snow removal, and exterior washing.")
    cards = ""
    for a in AREAS:
        c, sl = a["img"]
        cards += f"""<a class="pcard rv" href="{a['slug']}.html">
      {picture(c, sl, a['img_alt'], depth, sizes="(max-width:700px) 92vw, 31vw")}
      <span class="pcard__cap"><b>{esc(a['name'])}, IN</b><span>{esc(a['blurb'][:70])}…</span></span>
    </a>"""
    ld = [breadcrumb_ld([("Home", "/"), ("Service Areas", "/service-areas/")])]
    return head(title, desc, depth, "/service-areas/", extra_ld=ld) + header(depth, "areas") + f"""
<main id="main">
<section class="phead">
  <div class="phead__grid">
    <div class="phead__in">
    {crumbs([("Home","index.html"),("Service Areas",None)], depth)}
    <span class="eyebrow" style="color:var(--gold)">Service areas</span>
    <h1 class="display h-1">Boone County and the northwest side.</h1>
    <p>Mowing runs on tight routes through three towns. Everything else travels further —
    if you're close, ask.</p>
    </div>
    <div class="phead__fig">{picture('commercial','commercial-median-landscape','',depth,sizes="(max-width:900px) 100vw, 46vw")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g-3">{cards}</div>
    <div class="pricebox rv" style="margin-top:2.5rem">
      <h3 class="display h-3">Outside these three towns?</h3>
      <p style="margin-top:.7rem;color:var(--muted)">The three-town limit applies to <strong>mowing</strong>,
      because weekly routes only work when they're geographically tight. Mulching, cleanups, leaf removal,
      snow removal, soft washing and pressure washing all travel further across Boone County and the
      northwest side of Indianapolis — including Lebanon, Brownsburg, Advance and Jamestown.
      Call and we'll tell you straight whether we can get to you.</p>
      <a class="btn btn--solid-dark" style="margin-top:1.2rem" href="../contact.html">Ask about your address {icon('arrow','arw')}</a>
    </div>
  </div>
</section>

{cta_band(depth)}
</main>
""" + footer(depth)


def page_area(a):
    depth = 1
    title = f"Lawn Care & Snow Removal in {a['name']}, IN | Cline"
    desc = (f"Mowing, mulch, leaf removal, snow removal and exterior washing in {a['full']}. "
            f"Residential, commercial and HOA grounds care from a local crew.")
    c, sl = a["img"]
    hl = "".join(f'<li>{esc(h)}</li>' for h in a["highlights"])
    paras = "".join(f"<p>{esc(p)}</p>" for p in a["detail"])
    svc_chips = "".join(
        f'<a class="chip" href="../services/{s["slug"]}.html"><span class="dot"></span>{esc(s["name"])}</a>'
        for s in SERVICES)
    ld = [
        breadcrumb_ld([("Home", "/"), ("Service Areas", "/service-areas/"),
                       (a["name"], f"/service-areas/{a['slug']}.html")]),
        {"@context": "https://schema.org", "@type": "Service",
         "name": f"Property maintenance in {a['full']}",
         "provider": {"@id": SITE["base"] + "/#business"},
         "areaServed": {"@type": "City", "name": a["full"]},
         "description": desc},
    ]
    return head(title, desc, depth, f"/service-areas/{a['slug']}.html",
                og_img=f"assets/img/{c}/{sl}-800.jpg", extra_ld=ld) + header(depth, "areas") + f"""
<main id="main">
<section class="phead">
  <div class="phead__grid">
    <div class="phead__in">
    {crumbs([("Home","index.html"),("Service Areas","service-areas/index.html"),(a['name'],None)], depth)}
    <span class="eyebrow" style="color:var(--gold)">Service area</span>
    <h1 class="display h-1">{esc(a['name'])}, Indiana</h1>
    <p>{esc(a['blurb'])}</p>
    <div class="hero__acts" style="margin-top:.6rem">
      <a class="btn btn--primary" href="../contact.html">Get a Free Estimate {icon('arrow','arw')}</a>
      <a class="btn btn--ghost" href="tel:{SITE['phone_href']}">{icon('phone','')} {SITE['phone_display']}</a>
    </div>
    </div>
    <div class="phead__fig">{picture(c, sl, "", depth, sizes="(max-width:900px) 100vw, 46vw", eager=True)}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="rv">
        <span class="eyebrow">What {esc(a['name'])} properties need</span>
        <h2 class="display h-2" style="margin-top:.8rem">Local knowledge, not a franchise script.</h2>
        <div class="prose" style="margin-top:1.1rem">{paras}
          <ul>{hl}</ul>
        </div>
      </div>
      <div class="split__fig rv rv-d1">{picture(c, sl, a['img_alt'], depth,
        sizes="(max-width:820px) 92vw, 46vw")}</div>
    </div>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap wrap--tight" style="text-align:center">
    <span class="eyebrow eyebrow--plain" style="justify-content:center">Available in {esc(a['name'])}</span>
    <h2 class="display h-2" style="margin:.7rem 0 1.5rem">All seven services</h2>
    <div class="seasons__list" style="justify-content:center">{svc_chips}</div>
  </div>
</section>

{cta_band(depth, 'mulching', 'hoa-entrance-mulch-harcourt-springs',
          f"Serving {a['name']} and the surrounding area.",
          "Tell us the address and what's been bugging you about the property. We'll take it from there.")}
</main>
""" + footer(depth)


def page_gallery():
    depth = 0
    title = "Our Work | Project Photo Gallery | Cline"
    desc = ("Real project photos from Cline Property Management: mowing, mulching, leaf removal, "
            "commercial grounds care and exterior washing across Boone County, Indiana.")
    cats = [
        ("all", "Everything"), ("mowing", "Mowing"), ("mulching", "Mulching"),
        ("leaf-removal", "Leaf Removal"), ("commercial", "Commercial & HOA"),
        ("pressure-washing", "Pressure Washing"), ("soft-washing", "Soft Washing"),
        ("cleanups", "Cleanups"),
    ]
    btns = "".join(
        f'<button data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{esc(lbl)}</button>'
        for k, lbl in cats)

    seen = set()
    figs = ""
    for s in SERVICES:
        for c, sl, alt in s.get("gallery", []):
            if sl in seen:
                continue
            seen.add(sl)
            figs += (f'<figure data-cat="{c}">'
                     f'{picture(c, sl, alt, depth, sizes="(max-width:520px) 92vw, (max-width:900px) 46vw, 31vw")}'
                     f'<figcaption>{esc(alt)}</figcaption></figure>')
    # sweep in anything not referenced by a service gallery
    for c in sorted(os.listdir(IMG)):
        d = os.path.join(IMG, c)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith("-480.webp"):
                continue
            sl = f[:-len("-480.webp")]
            if sl in seen:
                continue
            seen.add(sl)
            alt = GALLERY_EXTRA.get(sl) or sl.replace("-", " ").capitalize()
            figs += (f'<figure data-cat="{c}">'
                     f'{picture(c, sl, alt, depth, sizes="(max-width:520px) 92vw, (max-width:900px) 46vw, 31vw")}'
                     f'<figcaption>{esc(alt)}</figcaption></figure>')

    ld = [breadcrumb_ld([("Home", "/"), ("Our Work", "/gallery.html")])]
    return head(title, desc, depth, "/gallery.html", extra_ld=ld) + header(depth, "gallery") + f"""
<main id="main">
<section class="phead">
  <div class="phead__grid">
    <div class="phead__in">
    {crumbs([("Home","index.html"),("Our Work",None)], depth)}
    <span class="eyebrow" style="color:var(--gold)">Our work</span>
    <h1 class="display h-1">{len(seen)} photos. All ours.</h1>
    <p>Every image on this site is a real Cline job on a real property around Boone County.
    Nothing here is stock photography.</p>
    </div>
    <div class="phead__fig">{picture('leaf-removal','leaf-vacuum-truck-curb','',depth,sizes="(max-width:900px) 100vw, 46vw")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="gal-filter">{btns}</div>
    <div class="gal">{figs}</div>
  </div>
</section>

{cta_band(depth)}
</main>
""" + footer(depth)


def page_about():
    depth = 0
    title = "About Cline Property Management | Whitestown, IN"
    desc = ("A local Boone County grounds care company handling mowing, landscape, cleanups, snow "
            "removal and exterior washing for homes, HOAs and businesses.")
    steps = "".join(f'<div class="step"><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></div>' for t, d in PROCESS)
    ld = [breadcrumb_ld([("Home", "/"), ("About", "/about.html")])]
    return head(title, desc, depth, "/about.html", extra_ld=ld) + header(depth, "about") + f"""
<main id="main">
<section class="phead">
  <div class="phead__grid">
    <div class="phead__in">
    {crumbs([("Home","index.html"),("About",None)], depth)}
    <span class="eyebrow" style="color:var(--gold)">About</span>
    <h1 class="display h-1">One crew. The whole property. All year.</h1>
    <p>Cline Property Management is a Boone County grounds care company built around
    doing the whole job rather than one slice of it.</p>
    </div>
    <div class="phead__fig">{picture('commercial','commercial-median-crew','',depth,sizes="(max-width:900px) 100vw, 46vw")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="rv">
        <div class="prose">
          <h2 style="margin-top:0">Why one company for all of it</h2>
          <p>Most properties end up with a mowing company, someone else for mulch, a third outfit for
          leaves, and a fourth for snow. Four schedules, four invoices, and four different people to
          call when something looks wrong — plus the gap between them where things quietly don't get done.</p>
          <p>We built the business the other way. The same crew that mows your turf in July clears
          your leaves in November and plows your drive in January. They know the property, they know
          where the sprinkler heads are, and they know what it's supposed to look like.</p>
          <h2>Who we work for</h2>
          <p>Roughly half our work is residential — weekly mowing, beds, seasonal cleanups and washing
          for homeowners in Whitestown, Zionsville and West Carmel. The other half is commercial,
          HOA and municipal: entrance landscaping, common areas, retail frontage, and right-of-way
          and median maintenance that happens in live traffic under a scheduled contract.</p>
          <p>Those are genuinely different jobs. A homeowner wants their Saturday back. An HOA board
          wants the entrance to look right and the invoices to match the contract. A property manager
          wants a certificate of insurance on file and someone who answers the phone. We're set up
          for all three.</p>
          <h2>How we actually operate</h2>
          <p>Recurring work goes on a fixed day of the week. Edging, trimming and blow-off happen
          every visit, not when there's time left over. If weather moves us, you hear about it
          instead of wondering. And if something isn't right, we come back — that's not a marketing
          line, it's just cheaper than losing a customer over a strip of missed trim.</p>
        </div>
      </div>
      <div class="rv rv-d1">
        <div class="stackfig">
          <div class="stackfig__a">{picture('mowing','lawn-mowing-striped-residential',
            'Finished residential lawn with mowing stripes', depth, sizes="(max-width:820px) 92vw, 46vw")}</div>
          <div class="stackfig__b">{picture('leaf-removal','leaf-removal-backpack-blower',
            'Crew member clearing leaves', depth, sizes="(max-width:820px) 46vw, 24vw")}</div>
        </div>
        <div class="pricebox" style="margin-top:2.5rem">
          <h3 class="display h-3">At a glance</h3>
          <div class="grid" style="gap:1.1rem;margin-top:1.1rem">
            <dl class="kv"><dt>Based in</dt><dd>{esc(SITE['city'])}, {SITE['region_long']}</dd></dl>
            <dl class="kv"><dt>Mowing area</dt><dd>{esc(SITE['areas_short'])}</dd></dl>
            <dl class="kv"><dt>Other services</dt><dd>Boone County &amp; NW Indianapolis</dd></dl>
            <dl class="kv"><dt>Property types</dt><dd>Residential · Commercial · HOA · Municipal</dd></dl>
            <dl class="kv"><dt>Insurance</dt><dd>Certificates available on request</dd></dl>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap wrap--tight">
    <div class="shead"><span class="eyebrow">How it works</span>
      <h2 class="display h-1">From first call to finished</h2></div>
    <div class="steps rv">{steps}</div>
  </div>
</section>

{cta_band(depth)}
</main>
""" + footer(depth)


def page_contact():
    depth = 0
    title = "Contact & Free Estimate | (317) 677-4709 | Cline"
    desc = ("Request a free estimate for lawn care, mulch, cleanups, leaf or snow removal in "
            "Whitestown, Zionsville and West Carmel, Indiana. Call (317) 677-4709.")
    checks = "".join(
        f'<label class="check"><input type="checkbox" name="services" value="{s["slug"]}">'
        f'<span>{esc(s["name"])}</span></label>' for s in SERVICES)
    ld = [breadcrumb_ld([("Home", "/"), ("Contact", "/contact.html")])]
    return head(title, desc, depth, "/contact.html", extra_ld=ld) + header(depth, "contact") + f"""
<main id="main">
<section class="phead">
  <div class="phead__grid">
    <div class="phead__in">
    {crumbs([("Home","index.html"),("Contact",None)], depth)}
    <span class="eyebrow" style="color:var(--gold)">Contact</span>
    <h1 class="display h-1">Let's talk about your property.</h1>
    <p>Free estimates on everything we do. Call or text for the fastest answer —
    or send the form and we'll come back to you.</p>
    </div>
    <div class="phead__fig">{picture('mulching','mulch-install-entry-walkway','',depth,sizes="(max-width:900px) 100vw, 46vw")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split" style="align-items:start">
      <div class="rv">
        <span class="eyebrow">Request an estimate</span>
        <h2 class="display h-2" style="margin:.8rem 0 1.4rem">Tell us what you need</h2>

        <div class="qok" role="status">
          <b>Thanks — that's on its way.</b>
          <span>We'll get back to you shortly. If it's urgent, call
          <a href="tel:{SITE['phone_href']}">{SITE['phone_display']}</a>.</span>
        </div>

        <form class="qform" name="estimate" method="POST" data-netlify="true"
              netlify-honeypot="company-website" action="thanks.html" data-mode="mailto">
          <input type="hidden" name="form-name" value="estimate">
          <p style="display:none"><label>Leave blank <input name="company-website"></label></p>

          <div class="qrow">
            <div class="field">
              <label for="f-name">Name *</label>
              <input id="f-name" name="name" required autocomplete="name">
              <span class="field__err">Please tell us your name.</span>
            </div>
            <div class="field">
              <label for="f-phone">Phone *</label>
              <input id="f-phone" name="phone" type="tel" required autocomplete="tel" placeholder="(317) 555-0100">
              <span class="field__err">A 10-digit phone number, please.</span>
            </div>
          </div>

          <div class="qrow">
            <div class="field">
              <label for="f-email">Email *</label>
              <input id="f-email" name="email" type="email" required autocomplete="email">
              <span class="field__err">That email doesn't look right.</span>
            </div>
            <div class="field">
              <label for="f-property">Property type</label>
              <select id="f-property" name="property">
                <option>Residential</option>
                <option>Commercial</option>
                <option>HOA / Common area</option>
                <option>Municipal</option>
              </select>
            </div>
          </div>

          <div class="field">
            <label for="f-address">Address or area *</label>
            <input id="f-address" name="address" required autocomplete="street-address"
                   placeholder="Street address, or just the town">
            <span class="field__err">We need to know where the property is.</span>
          </div>

          <div class="field">
            <label>What do you need?</label>
            <div class="checks">{checks}</div>
          </div>

          <div class="field">
            <label for="f-msg">Anything else</label>
            <textarea id="f-msg" name="message"
              placeholder="Lot size, how long it's been since it was last done, what's been bugging you about it…"></textarea>
          </div>

          <button class="btn btn--primary" type="submit" style="justify-self:start">
            Send Request {icon('arrow','arw')}
          </button>
          <p class="qnote">We'll only use this to get back to you about your property. No lists, no sharing.</p>
        </form>
      </div>

      <div class="rv rv-d1">
        <div class="pricebox">
          <h3 class="display h-3">Reach us directly</h3>
          <div class="ftr__nap" style="margin-top:1.2rem;gap:1rem">
            <a class="contact-tel" href="tel:{SITE['phone_href']}">{icon('phone','')}<span>{SITE['phone_display']}</span></a>
            <a class="contact-mail" href="mailto:{SITE['email']}">{icon('mail','')}<span>{esc(SITE['email'])}</span></a>
          </div>
          <hr style="border:0;border-top:1px solid var(--rule);margin:1.5rem 0">
          <dl class="kv" style="gap:.9rem">
            <div><dt>Mowing service area</dt><dd>{esc(SITE['areas_short'])}</dd></div>
            <div><dt>All other services</dt><dd>Boone County &amp; NW Indianapolis</dd></div>
            <div><dt>Estimates</dt><dd>Free, and we'll tell you if you don't need the work</dd></div>
          </dl>
        </div>

        <div class="pricebox" style="margin-top:1.2rem">
          <h3 class="display h-3">Property managers &amp; HOA boards</h3>
          <p style="margin-top:.7rem;color:var(--muted)">For contracted work we'll walk the property,
          put the scope in writing, and get a certificate of insurance to you before anything starts.
          Mention your board's meeting date and we'll work to it.</p>
        </div>
      </div>
    </div>
  </div>
</section>
</main>
""" + footer(depth)


def page_thanks():
    depth = 0
    return head("Thanks — we got it | Cline Property Management",
                "Your estimate request has been received.", depth, "/thanks.html", noindex=True) + header(depth) + f"""
<main id="main">
<section class="section" style="min-height:60vh;display:grid;place-items:center;text-align:center">
  <div class="wrap wrap--tight">
    <span class="eyebrow eyebrow--plain" style="justify-content:center">Received</span>
    <h1 class="display h-1" style="margin:1rem 0">Thanks — that's in.</h1>
    <p class="lede" style="margin-inline:auto">We'll get back to you shortly. If you'd rather not wait,
    give us a call and we'll pick up.</p>
    <div class="hero__acts" style="justify-content:center;margin-top:2rem">
      <a class="btn btn--primary" href="tel:{SITE['phone_href']}">{icon('phone','')} {SITE['phone_display']}</a>
      <a class="btn btn--ghost" href="index.html">Back to the site</a>
    </div>
  </div>
</section>
</main>
""" + footer(depth)


def page_404():
    depth = 0
    return head("Page not found | Cline Property Management",
                "That page doesn't exist.", depth, "/404.html", noindex=True) + header(depth) + f"""
<main id="main">
<section class="section" style="min-height:60vh;display:grid;place-items:center;text-align:center">
  <div class="wrap wrap--tight">
    <span class="eyebrow eyebrow--plain" style="justify-content:center">404</span>
    <h1 class="display h-1" style="margin:1rem 0">That page has been mowed over.</h1>
    <p class="lede" style="margin-inline:auto">The link's dead, but the phone works.</p>
    <div class="hero__acts" style="justify-content:center;margin-top:2rem">
      <a class="btn btn--primary" href="index.html">Back to the home page</a>
      <a class="btn btn--ghost" href="services/index.html">See our services</a>
    </div>
  </div>
</section>
</main>
""" + footer(depth)


# --------------------------------------------------------------------------
# write
# --------------------------------------------------------------------------
def w(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def main():
    written = []
    written.append(w("index.html", page_home()))
    written.append(w("services/index.html", page_services_index()))
    for s in SERVICES:
        written.append(w(f"services/{s['slug']}.html", page_service(s)))
    written.append(w("service-areas/index.html", page_areas_index()))
    for a in AREAS:
        written.append(w(f"service-areas/{a['slug']}.html", page_area(a)))
    written.append(w("gallery.html", page_gallery()))
    written.append(w("about.html", page_about()))
    written.append(w("contact.html", page_contact()))
    written.append(w("thanks.html", page_thanks()))
    written.append(w("404.html", page_404()))

    # favicon
    w("assets/favicon.svg",
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">'
      '<rect width="40" height="40" rx="6" fill="#1B3324"/>'
      '<path d="M20 8c0 7-4 10-4 14a4 4 0 0 0 8 0c0-4-4-7-4-14z" fill="#D2A03E"/>'
      '<path d="M11 27c3.5 2.4 5.8 3.2 9 3.2s5.5-.8 9-3.2" stroke="#7C9A84" stroke-width="2" '
      'stroke-linecap="round" fill="none"/></svg>')

    # sitemap
    urls = ["/", "/services/", "/service-areas/", "/gallery.html", "/about.html", "/contact.html"]
    urls += [f"/services/{s['slug']}.html" for s in SERVICES]
    urls += [f"/service-areas/{a['slug']}.html" for a in AREAS]
    prio = {"/": "1.0", "/services/": "0.9", "/contact.html": "0.9", "/service-areas/": "0.8"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{SITE['base']}{u}</loc>"
                  f"<changefreq>monthly</changefreq>"
                  f"<priority>{prio.get(u, '0.7')}</priority></url>")
    sm.append("</urlset>")
    w("sitemap.xml", "\n".join(sm))

    if STAGING:
        w("robots.txt",
          "# Temporary preview URL -- not the final home of this site.\n"
          "# Remove this block (set STAGING = False in build/data.py) once the\n"
          "# site is on its own domain.\n"
          "User-agent: *\nDisallow: /\n")
    else:
        w("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE['base']}/sitemap.xml\n")

    # Netlify: pretty URLs + security headers
    w("_headers", """/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
/assets/*
  Cache-Control: public, max-age=31536000, immutable
""")

    print(f"wrote {len(written)} pages")
    for p in written:
        print("  ", p)


if __name__ == "__main__":
    main()
