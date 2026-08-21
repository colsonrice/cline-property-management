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
      var before = Math.round(pct);
      ba.setAttribute('aria-valuenow', before);
      ba.setAttribute('aria-valuetext', before === 0 ? 'After image only'
        : before === 100 ? 'Before image only'
        : before + '% before, ' + (100 - before) + '% after');
    };
    var fromPoint = function (clientX) {
      var r = ba.getBoundingClientRect();
      var x = clientX - r.left;
      set((x / r.width) * 100);
    };
    var dragging = false;
    var activePointer = null;
    var finish = function (e) {
      if (!dragging || (e && activePointer !== null && e.pointerId !== activePointer)) return;
      dragging = false;
      ba.classList.remove('is-dragging');
      ba.classList.add('is-used');
      if (e && ba.hasPointerCapture && ba.hasPointerCapture(e.pointerId)) ba.releasePointerCapture(e.pointerId);
      activePointer = null;
    };

    ba.addEventListener('pointerdown', function (e) {
      if (e.button !== undefined && e.button !== 0) return;
      dragging = true;
      activePointer = e.pointerId;
      ba.classList.add('is-dragging', 'is-used');
      if (ba.setPointerCapture) ba.setPointerCapture(e.pointerId);
      fromPoint(e.clientX);
    });
    ba.addEventListener('pointermove', function (e) {
      if (!dragging || e.pointerId !== activePointer) return;
      fromPoint(e.clientX);
      if (e.cancelable) e.preventDefault();
    });
    ba.addEventListener('pointerup', finish);
    ba.addEventListener('pointercancel', finish);
    ba.addEventListener('lostpointercapture', function () { finish(); });

    ba.addEventListener('keydown', function (e) {
      var now = parseFloat(ba.getAttribute('aria-valuenow') || '50');
      if (e.key === 'ArrowLeft') { e.preventDefault(); set(now - 5); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); set(now + 5); }
      else if (e.key === 'Home') { e.preventDefault(); set(0); }
      else if (e.key === 'End') { e.preventDefault(); set(100); }
      else return;
      ba.classList.add('is-used');
    });

    set(50);
  });


  /* ---------- Motion reel ----------
     Clips carry no audio track and never fetch a byte until they scroll into
     view. Autoplay is paused again on exit so a backgrounded tab is not
     decoding video nobody is watching. */
  var clips = document.querySelectorAll('.clip');
  if (clips.length) {
    var canObserve = 'IntersectionObserver' in window;

    clips.forEach(function (clip) {
      var video = clip.querySelector('video');
      var btn = clip.querySelector('.clip__btn');
      if (!video) return;

      var wanted = false;   // user asked for it explicitly
      var loaded = false;

      // Two hazards to avoid here. Calling play() immediately after
      // video.load() aborts the load it depends on; but waiting on a single
      // readiness event hangs forever if that event never arrives. So: try
      // once now, and try again on canplay. Both attempts swallow rejection.
      var load = function () {
        if (loaded) return;
        loaded = true;
        clip.querySelectorAll('source[data-src]').forEach(function (s) {
          s.src = s.dataset.src;
        });
        video.load();
      };

      var attempt = function () {
        if (video.error) return;
        var p = video.play();
        if (p && p.catch) p.catch(function () { /* poster stays; button still works */ });
      };

      var play = function () {
        load();
        attempt();
        video.addEventListener('canplay', attempt, { once: true });
      };

      var pause = function () { if (!video.paused) video.pause(); };

      video.addEventListener('playing', function () { clip.classList.add('is-playing'); });
      video.addEventListener('pause', function () { clip.classList.remove('is-playing'); });

      if (btn) {
        btn.addEventListener('click', function () {
          if (video.paused) { wanted = true; play(); }
          else { wanted = false; pause(); }
        });
      }

      if (canObserve) {
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting) {
              if (!reduced || wanted) play();
              else load();
            } else if (!wanted) {
              pause();
            }
          });
        }, { threshold: 0.4 });
        io.observe(clip);
      } else if (!reduced) {
        play();
      }
    });
  }

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

      // FormSubmit delivers straight to Mike's inbox. Posting normally would
      // bounce the visitor to formsubmit.co's own thank-you page, so send it
      // over fetch and keep them here. The /ajax/ prefix is what makes
      // FormSubmit answer with JSON instead of a redirect.
      if (!window.fetch || !form.action || form.action.indexOf('formsubmit.co') === -1) return;
      e.preventDefault();

      var btn = form.querySelector('button[type="submit"]');
      var label = btn ? btn.innerHTML : '';
      if (btn) { btn.disabled = true; btn.innerHTML = 'Sending\u2026'; }

      // Let Mike hit reply and have it go to the customer.
      var em = form.elements['email'];
      var rt = form.elements['_replyto'];
      if (em && rt) rt.value = em.value;

      // Every subject carries the [Cline Web] tag so one Gmail filter catches
      // the lot, then the service and town so the inbox is sortable at a
      // glance without opening anything.
      var subj = form.elements['_subject'];
      if (subj) {
        var picked = Array.prototype.slice
          .call(form.querySelectorAll('input[name="services"]:checked'))
          .map(function (c) {
            var lab = c.parentNode.querySelector('span');
            return lab ? lab.textContent.trim() : c.value;
          });
        var who = (form.elements['name'] || {}).value || '';
        var where = (form.elements['address'] || {}).value || '';
        var what = picked.length === 0 ? 'General enquiry'
                 : picked.length <= 2 ? picked.join(' + ')
                 : picked.length + ' services';
        var bits = ['[Cline Web]', what];
        if (where) bits.push('\u00b7 ' + where);
        if (who) bits.push('\u2014 ' + who);
        subj.value = bits.join(' ');
      }

      // Tell Mike which page they were reading when they asked.
      var src = form.elements['Submitted from'];
      if (src) src.value = document.referrer && document.referrer.indexOf(location.host) > -1
        ? document.referrer.replace(location.origin, '') + ' \u2192 ' + location.pathname
        : location.pathname;

      fetch(form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/'), {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      }).then(function (r) {
        if (!r.ok) throw new Error('send failed');
        if (ok) {
          ok.classList.add('is-on');
          form.hidden = true;
          ok.setAttribute('tabindex', '-1');
          ok.focus();
        }
      }).catch(function () {
        if (btn) { btn.disabled = false; btn.innerHTML = label; }
        var err = form.querySelector('.qsend-err');
        if (err) { err.hidden = false; }
      });
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
