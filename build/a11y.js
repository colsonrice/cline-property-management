/* In-page accessibility audit. Walks the rendered DOM, resolves the real
   painted background behind each text node, and reports WCAG AA failures
   plus the structural issues automated tools can actually be sure about. */
(function () {
  var out = { contrast: [], structure: [], targets: [], counts: {} };

  function parse(c) {
    if (!c) return null;
    // color-mix() resolves to color(srgb r g b / a) with 0-1 channels. Missing
    // this made every color-mix background look transparent, so the walker ran
    // past it to the section behind and reported false contrast failures.
    var s = c.match(/color\(\s*srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?/i);
    if (s) return [+s[1]*255, +s[2]*255, +s[3]*255, s[4] === undefined ? 1 : +s[4]];
    var m = c.match(/rgba?\(([\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)(?:[ ,/]+([\d.]+))?/);
    if (m) return [+m[1], +m[2], +m[3], m[4] === undefined ? 1 : +m[4]];
    return null;
  }
  function over(fg, bg) {              // composite fg (with alpha) onto bg
    var a = fg[3];
    return [fg[0]*a + bg[0]*(1-a), fg[1]*a + bg[1]*(1-a), fg[2]*a + bg[2]*(1-a), 1];
  }
  function lum(c) {
    var f = function (v) { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
    return 0.2126*f(c[0]) + 0.7152*f(c[1]) + 0.0722*f(c[2]);
  }
  function ratio(a, b) {
    var la = lum(a), lb = lum(b), hi = Math.max(la, lb), lo = Math.min(la, lb);
    return (hi + 0.05) / (lo + 0.05);
  }
  function effBg(el) {
    var acc = null, n = el;
    while (n && n !== document.documentElement) {
      var cs = getComputedStyle(n);
      var bg = parse(cs.backgroundColor);
      var hasImg = cs.backgroundImage && cs.backgroundImage !== 'none';
      if (hasImg) return { c: null, img: true };
      if (bg && bg[3] > 0) {
        acc = acc ? over(acc, bg) : bg;
        if (acc[3] >= 0.999) return { c: acc, img: false };
      }
      n = n.parentElement;
    }
    return { c: acc || [252,250,244,1], img: false };
  }
  function label(el) {
    var t = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 42);
    return el.tagName.toLowerCase() + (el.className && typeof el.className === 'string'
      ? '.' + el.className.trim().split(/\s+/).slice(0,2).join('.') : '') + ' — "' + t + '"';
  }

  // ---- contrast on every element holding its own text ----
  var seen = {};
  document.querySelectorAll('body *').forEach(function (el) {
    if (el.closest('.vh, [hidden], [aria-hidden="true"]')) return;
    // Sections that lay text over a photo have no solid background to
    // measure; their legibility comes from a gradient scrim. Static
    // contrast maths cannot judge those, so skip rather than cry wolf.
    if (el.closest('.hero, .hero-s, .phead, .cta-band, .pcard, .clip, .gal figure')
        && !el.closest('.hero-s__badge')) return;
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return;
    var own = Array.prototype.filter.call(el.childNodes, function (n) {
      return n.nodeType === 3 && n.textContent.trim();
    });
    if (!own.length) return;
    var fg = parse(cs.color); if (!fg) return;
    var bgr = effBg(el);
    if (bgr.img || !bgr.c) return;              // over imagery: can't judge statically
    var eff = fg[3] < 1 ? over(fg, bgr.c) : fg;
    var r = ratio(eff, bgr.c);
    var px = parseFloat(cs.fontSize);
    var wt = parseInt(cs.fontWeight, 10) || 400;
    var large = px >= 24 || (px >= 18.66 && wt >= 700);
    var need = large ? 3.0 : 4.5;
    out.counts.checked = (out.counts.checked || 0) + 1;
    if (r < need) {
      var k = label(el) + '|' + r.toFixed(2);
      if (!seen[k]) { seen[k] = 1;
        out.contrast.push({ el: label(el), ratio: +r.toFixed(2), need: need,
                            px: Math.round(px), weight: wt,
                            color: cs.color, bg: 'rgb(' + bgr.c.slice(0,3).map(Math.round).join(',') + ')' });
      }
    }
  });

  // ---- structure ----
  var S = out.structure;
  if (!document.documentElement.lang) S.push('html element has no lang attribute');
  var h1 = document.querySelectorAll('h1');
  if (h1.length !== 1) S.push(h1.length + ' <h1> elements (expected exactly 1)');
  if (!document.querySelector('main')) S.push('no <main> landmark');
  if (!document.querySelector('nav')) S.push('no <nav> landmark');

  var lvl = 0;
  document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(function (h) {
    var n = +h.tagName[1];
    if (lvl && n > lvl + 1) S.push('heading jumps h' + lvl + ' -> h' + n + ': "' + h.textContent.trim().slice(0,40) + '"');
    lvl = n;
  });

  document.querySelectorAll('img').forEach(function (i) {
    if (!i.hasAttribute('alt')) S.push('img without alt: ' + (i.getAttribute('src')||'').split('/').pop());
  });
  document.querySelectorAll('a[href]').forEach(function (a) {
    var t = (a.textContent||'').trim() || a.getAttribute('aria-label') || a.querySelector('img,svg') ? null : 'empty';
    if (t === 'empty') S.push('link with no accessible name: ' + a.getAttribute('href'));
  });
  document.querySelectorAll('button').forEach(function (b) {
    if (!(b.textContent||'').trim() && !b.getAttribute('aria-label')) S.push('button with no accessible name');
  });
  document.querySelectorAll('input,select,textarea').forEach(function (f) {
    if (f.type === 'hidden') return;
    var id = f.id;
    var lab = id && document.querySelector('label[for="' + CSS.escape(id) + '"]');
    if (!lab && !f.closest('label') && !f.getAttribute('aria-label') && !f.getAttribute('aria-labelledby')) {
      S.push('form control with no label: ' + (f.name || f.type));
    }
  });

  // ---- touch targets (WCAG 2.2 AA = 24x24 css px) ----
  document.querySelectorAll('a,button,input[type=checkbox],select').forEach(function (el) {
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    var r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    if (r.width < 24 || r.height < 24) {
      if (el.closest('p, li, .prose')) return;   // inline text links are exempt
      out.targets.push(label(el) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
    }
  });

  out.counts.contrastFails = out.contrast.length;
  return JSON.stringify(out);
})();
