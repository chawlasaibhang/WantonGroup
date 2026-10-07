/* Wanton Group: navigation and quiet interactions. No dependencies.
   Everything here is an enhancement; the pages are complete without it. */
(function () {
  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---- Mobile menu ---- */
  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');
  if (toggle && links) {
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      links.classList.toggle('open', open);
      root.classList.toggle('menu-open', open);
    };
    toggle.addEventListener('click', function () { setOpen(toggle.getAttribute('aria-expanded') !== 'true'); });
    links.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && links.classList.contains('open')) { setOpen(false); toggle.focus(); }
    });
    window.matchMedia('(min-width: 901px)').addEventListener('change', function (e) { if (e.matches) setOpen(false); });
  }

  /* ---- Stagger siblings inside [data-stagger] ---- */
  document.querySelectorAll('[data-stagger]').forEach(function (group) {
    group.querySelectorAll(':scope > .reveal').forEach(function (el, i) { el.style.setProperty('--d', (i * 0.09) + 's'); });
  });

  /* ---- Ajuni icons draw themselves in ---- */
  document.querySelectorAll('.aj-card svg *').forEach(function (s) { s.setAttribute('pathLength', '1'); });

  /* ---- Statement: split into words that light up as you read ---- */
  var statements = [].slice.call(document.querySelectorAll('[data-words]'));
  statements.forEach(function (p) {
    var walk = function (node) {
      [].slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var span = document.createElement('span');
            span.className = 'w';
            span.textContent = part;
            frag.appendChild(span);
          });
          child.replaceWith(frag);
        } else if (child.nodeType === 1) { walk(child); }
      });
    };
    walk(p);
    p._words = [].slice.call(p.querySelectorAll('.w'));
  });

  /* ---- Count up numbers once they are seen ---- */
  var countUp = function (el) {
    var to = parseFloat(el.getAttribute('data-count'));
    var from = parseFloat(el.getAttribute('data-from') || '0');
    var suffix = el.getAttribute('data-suffix') || '';
    if (reduced) { el.textContent = to + suffix; return; }
    var start = null, dur = 1600;
    var step = function (t) {
      if (!start) start = t;
      var k = Math.min(1, (t - start) / dur);
      var eased = 1 - Math.pow(1 - k, 4);
      el.textContent = Math.round(from + (to - from) * eased) + suffix;
      if (k < 1) requestAnimationFrame(step);
    };
    el.textContent = from + suffix;
    requestAnimationFrame(step);
  };

  /* ---- Reveal on scroll (once) ---- */
  var revealables = document.querySelectorAll('.reveal, .develop, .titem, [data-count]');
  var show = function (el) {
    el.classList.add('is-visible');
    if (el.hasAttribute('data-count')) countUp(el);
  };
  if (!('IntersectionObserver' in window) || reduced) {
    revealables.forEach(show);
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { show(entry.target); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    revealables.forEach(function (el) { io.observe(el); });
  }

  /* ---- Scroll-linked details, batched into one frame ---- */
  var header = document.querySelector('.site-header');
  var spinners = [].slice.call(document.querySelectorAll('[data-spin]'));
  var parallax = [].slice.call(document.querySelectorAll('[data-parallax]'));
  var queued = false;
  var tick = function () {
    queued = false;
    var y = window.scrollY, vh = window.innerHeight;
    var max = document.documentElement.scrollHeight - vh;
    if (header) {
      header.classList.toggle('is-scrolled', y > 8);
      header.style.setProperty('--progress', max > 0 ? (y / max).toFixed(4) : 0);
    }
    statements.forEach(function (p) {
      var r = p.getBoundingClientRect();
      var k = reduced ? 1 : Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (r.height + vh * 0.35)));
      var lit = Math.round(k * p._words.length);
      p._words.forEach(function (w, i) { w.classList.toggle('on', i < lit); });
    });
    if (reduced) return;
    spinners.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var t = Math.min(1, Math.max(0, (vh - r.top) / (vh + r.height)));
      el.style.transform = 'rotate(' + ((t - 0.5) * parseFloat(el.getAttribute('data-spin'))).toFixed(2) + 'deg)';
    });
    parallax.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var offset = (r.top + r.height / 2 - vh / 2) * parseFloat(el.getAttribute('data-parallax'));
      el.style.transform = 'translate3d(0,' + offset.toFixed(1) + 'px,0)';
    });
  };
  var request = function () { if (!queued) { queued = true; requestAnimationFrame(tick); } };
  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request);
  tick();

  /* ---- Lantern light follows the pointer (desktop only) ---- */
  if (finePointer && !reduced) {
    document.querySelectorAll('[data-glow]').forEach(function (el) {
      var glow = el.querySelector('.wh-glow') || el;
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        glow.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%');
        glow.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%');
      });
    });
  }

  /* ---- Gentle tilt toward the pointer (desktop only) ---- */
  if (finePointer && !reduced) {
    document.querySelectorAll('[data-tilt]').forEach(function (el) {
      var max = parseFloat(el.getAttribute('data-tilt')) || 5;
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'perspective(900px) rotateY(' + (x * max).toFixed(2) + 'deg) rotateX(' + (-y * max).toFixed(2) + 'deg)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }
})();
