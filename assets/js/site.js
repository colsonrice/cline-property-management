/* Cline Property Management — site behaviour
   Vanilla, no dependencies. Progressive enhancement throughout. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Sticky header shadow ---------- */
  var hdr = document.querySelector('.hdr');
  if (hdr) {
    var onScroll = function () {
      hdr.classList.toggle('is-stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Mobile drawer ---------- */
  var burger = document.querySelector('.burger');
  var drawer = document.querySelector('.drawer');
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      drawer.classList.toggle('is-open', !open);
      document.body.style.overflow = !open ? 'hidden' : '';
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        burger.setAttribute('aria-expanded', 'false');
        drawer.classList.remove('is-open');
        document.body.style.overflow = '';
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) burger.click();
    });
  }

  /* ---------- Scroll reveal ---------- */
  var rvs = document.querySelectorAll('.rv');
  if (rvs.length) {
    if (reduced || !('IntersectionObserver' in window)) {
      rvs.forEach(function (el) { el.classList.add('in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
      rvs.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---------- Season tabs ---------- */
  var rail = document.querySelector('.seasons__rail');
  if (rail) {
    var tabs = Array.prototype.slice.call(rail.querySelectorAll('.season'));
    var panels = Array.prototype.slice.call(document.querySelectorAll('.seasons__panel'));
    var select = function (i) {
      tabs.forEach(function (t, n) { t.setAttribute('aria-selected', String(n === i)); t.tabIndex = n === i ? 0 : -1; });
      panels.forEach(function (p, n) { p.hidden = n !== i; });
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(i); });
      t.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var n = (i + d + tabs.length) % tabs.length;
        select(n); tabs[n].focus();
      });
    });
    // default to the current season
    var m = new Date().getMonth();
    var cur = (m >= 2 && m <= 4) ? 0 : (m >= 5 && m <= 7) ? 1 : (m >= 8 && m <= 10) ? 2 : 3;
    select(cur);
  }

  /* ---------- Before / after sliders ---------- */
  document.querySelectorAll('.ba').forEach(function (ba) {
    var set = function (pct) {
      pct = Math.max(0, Math.min(100, pct));
      ba.style.setProperty('--pos', pct + '%');
      ba.setAttribute('aria-valuenow', Math.round(pct));
    };
    var fromEvent = function (e) {
      var r = ba.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      set((x / r.width) * 100);
    };
    var dragging = false;
    var start = function (e) { dragging = true; fromEvent(e); };
    var move = function (e) { if (dragging) { fromEvent(e); } };
    var end = function () { dragging = false; };

    ba.addEventListener('mousedown', function (e) { e.preventDefault(); start(e); });
    window.addEventListener('mousemove', move);
    window.addEventListener('mouseup', end);
    ba.addEventListener('touchstart', start, { passive: true });
    ba.addEventListener('touchmove', move, { passive: true });
    ba.addEventListener('touchend', end);
    ba.addEventListener('click', fromEvent);

    ba.addEventListener('keydown', function (e) {
      var now = parseFloat(ba.getAttribute('aria-valuenow') || '50');
      if (e.key === 'ArrowLeft') { e.preventDefault(); set(now - 4); }
      if (e.key === 'ArrowRight') { e.preventDefault(); set(now + 4); }
      if (e.key === 'Home') { e.preventDefault(); set(0); }
      if (e.key === 'End') { e.preventDefault(); set(100); }
    });

    set(50);

    // gentle nudge on first view so the control is discoverable
    if (!reduced && 'IntersectionObserver' in window) {
      var seen = false;
      var o = new IntersectionObserver(function (en) {
        if (en[0].isIntersecting && !seen) {
          seen = true;
          var t0 = null;
          var tick = function (t) {
            if (!t0) t0 = t;
            var k = (t - t0) / 1100;
            if (k >= 1) { set(50); return; }
            set(50 + Math.sin(k * Math.PI * 2) * 14);
            requestAnimationFrame(tick);
          };
          setTimeout(function () { requestAnimationFrame(tick); }, 320);
          o.disconnect();
        }
      }, { threshold: 0.45 });
      o.observe(ba);
    }
  });

  /* ---------- Gallery filter ---------- */
  var gf = document.querySelector('.gal-filter');
  if (gf) {
    var figs = Array.prototype.slice.call(document.querySelectorAll('.gal figure'));
    gf.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      var key = b.dataset.filter;
      gf.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      figs.forEach(function (f) {
        var show = key === 'all' || f.dataset.cat === key;
        f.style.display = show ? '' : 'none';
      });
    });
  }

  /* ---------- Quote form ---------- */
  var form = document.querySelector('.qform');
  if (form) {
    var ok = document.querySelector('.qok');

    var showErr = function (field, on) {
      field.closest('.field').classList.toggle('field--err', on);
    };

    form.addEventListener('submit', function (e) {
      var valid = true;
      var required = form.querySelectorAll('[required]');
      required.forEach(function (f) {
        var bad = !f.value.trim() || (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        if (f.name === 'phone') {
          bad = f.value.replace(/\D/g, '').length < 10;
        }
        showErr(f, bad);
        if (bad && valid) { f.focus(); }
        if (bad) valid = false;
      });
      if (!valid) { e.preventDefault(); return; }

      // GitHub Pages (and file://) have no form backend -- a plain POST would
      // silently discard the enquiry. Hand the filled-in details to the user's
      // mail client instead. Set data-mode="post" once a real endpoint exists.
      var handoff = form.dataset.mode === 'mailto' || location.protocol === 'file:';
      if (handoff) {
        e.preventDefault();
        var g = function (n) { var el = form.elements[n]; return el ? el.value : ''; };
        var svcs = Array.prototype.slice.call(form.querySelectorAll('input[name="services"]:checked'))
          .map(function (c) { return c.value; }).join(', ');
        var body = [
          'Name: ' + g('name'),
          'Phone: ' + g('phone'),
          'Email: ' + g('email'),
          'Property type: ' + g('property'),
          'Address / area: ' + g('address'),
          'Services: ' + (svcs || '—'),
          '',
          g('message')
        ].join('\n');
        window.location.href = 'mailto:Clinepropertymanagement@gmail.com'
          + '?subject=' + encodeURIComponent('Quote request — ' + (g('name') || 'Website'))
          + '&body=' + encodeURIComponent(body);
        if (ok) { ok.classList.add('is-on'); form.style.display = 'none'; }
      }
    });

    form.querySelectorAll('[required]').forEach(function (f) {
      f.addEventListener('input', function () { showErr(f, false); });
    });

    // Light phone formatting
    var tel = form.elements['phone'];
    if (tel) {
      tel.addEventListener('input', function () {
        var d = tel.value.replace(/\D/g, '').slice(0, 10);
        tel.value = d.length > 6 ? '(' + d.slice(0, 3) + ') ' + d.slice(3, 6) + '-' + d.slice(6)
          : d.length > 3 ? '(' + d.slice(0, 3) + ') ' + d.slice(3)
          : d;
      });
    }

    // Pre-select a service when arriving from a service page (?service=slug)
    var q = new URLSearchParams(location.search).get('service');
    if (q) {
      var box = form.querySelector('input[name="services"][value="' + CSS.escape(q) + '"]');
      if (box) box.checked = true;
    }
  }

  /* ---------- Current year ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
