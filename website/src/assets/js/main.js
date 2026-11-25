/* =====================================================================
   MMAG website: interactions (unminified)
   GSAP 3.15 (ScrollTrigger, SplitText) + Lenis smooth scroll.
   Everything degrades: no JS → readable page; reduced motion → no pins,
   no smooth scroll, no split animations.
   ===================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var CFG = window.MMAG_CONFIG || {};
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(pointer: fine)").matches;
  var hasGSAP = typeof window.gsap !== "undefined" && typeof window.ScrollTrigger !== "undefined";
  if (reduced) root.classList.add("reduced");
  if (hasGSAP) {
    gsap.registerPlugin(ScrollTrigger);
    if (window.SplitText) gsap.registerPlugin(SplitText);
  }

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* ---------------- analytics (only when a GA4 ID is configured) ---------------- */
  window.dataLayer = window.dataLayer || [];
  function track(name, params) {
    if (CFG.ga4Id && typeof window.gtag === "function") window.gtag("event", name, params || {});
  }
  window.MMAG_TRACK = track;
  if (CFG.ga4Id) {
    var ga = document.createElement("script");
    ga.async = true;
    ga.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(CFG.ga4Id);
    document.head.appendChild(ga);
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", CFG.ga4Id);
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[href^='tel:']");
    if (a) track("phone_click", { location: a.getAttribute("data-loc") || "page" });
  });

  /* ---------------- smooth scroll ---------------- */
  var lenis = null;
  if (!reduced && hasGSAP && window.Lenis) {
    lenis = new window.Lenis({ lerp: 0.1, wheelMultiplier: 1, smoothWheel: true });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
  }
  window.MMAG_LENIS = lenis;
  function lockScroll(on) {
    if (lenis) { if (on) lenis.stop(); else lenis.start(); }
    document.body.style.overflow = on ? "hidden" : "";
  }

  /* ---------------- preloader ---------------- */
  function preloader() {
    return new Promise(function (resolve) {
      var pl = $(".preloader");
      if (!pl || !root.classList.contains("is-first")) { if (pl) pl.remove(); resolve(); return; }
      try { sessionStorage.setItem("mmag-loaded", "1"); } catch (e) { /* storage blocked */ }
      if (!hasGSAP || reduced) { pl.remove(); root.classList.remove("is-first"); resolve(); return; }
      var count = $(".preloader__count", pl);
      var o = { v: 0 };
      gsap.to(o, { v: 100, duration: 1.1, ease: "power2.inOut", onUpdate: function () { count.textContent = Math.round(o.v); } });
      gsap.to(pl, {
        yPercent: -100, duration: 0.9, ease: "expo.inOut", delay: 1.2,
        onComplete: function () { pl.remove(); root.classList.remove("is-first"); }
      });
      setTimeout(resolve, 1300);
    });
  }

  /* ---------------- page transitions ---------------- */
  var pt = $(".pt");
  function transitionIn() {
    if (!pt || !root.classList.contains("pt-in")) return;
    if (!hasGSAP || reduced) { root.classList.remove("pt-in"); return; }
    gsap.fromTo(pt, { yPercent: 0 }, {
      yPercent: -100, duration: 0.85, ease: "expo.inOut", delay: 0.05,
      onComplete: function () { root.classList.remove("pt-in"); gsap.set(pt, { clearProps: "transform" }); }
    });
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[href]");
    if (!a || e.defaultPrevented || e.button !== 0) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (a.target === "_blank" || a.hasAttribute("download") || a.hasAttribute("data-no-transition")) return;
    var href = a.getAttribute("href");
    if (!href || href.charAt(0) === "#" || /^(mailto|tel):/.test(href)) return;
    var url = new URL(a.href, window.location.href);
    if (url.origin !== window.location.origin) return;
    if (url.pathname === window.location.pathname && url.hash) return;
    if (!pt || !hasGSAP || reduced) return;
    e.preventDefault();
    try { sessionStorage.setItem("mmag-pt", "1"); } catch (err) { /* ignore */ }
    var go = function () { window.location.href = url.href; };
    gsap.fromTo(pt, { yPercent: 100 }, { yPercent: 0, duration: 0.6, ease: "expo.inOut", onComplete: go });
    setTimeout(go, 1200);
  });
  window.addEventListener("pageshow", function (e) {
    if (e.persisted && pt) { root.classList.remove("pt-in"); if (hasGSAP) gsap.set(pt, { yPercent: 100 }); }
  });

  /* ---------------- header ---------------- */
  var nav = $(".nav");
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    if (!nav) return;
    nav.classList.toggle("is-scrolled", y > 30);
    var menuOpen = root.classList.contains("menu-open");
    if (!menuOpen && y > lastY + 4 && y > 220) nav.classList.add("is-hidden");
    else if (y < lastY - 4 || y < 220) nav.classList.remove("is-hidden");
    lastY = y;
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  function navThemes() {
    if (!nav || !hasGSAP) return;
    $$("[data-nav-theme]").forEach(function (sec) {
      ScrollTrigger.create({
        trigger: sec, start: "top 44px", end: "bottom 44px",
        onToggle: function (self) { if (self.isActive) nav.setAttribute("data-theme", sec.getAttribute("data-nav-theme")); }
      });
    });
  }

  /* ---------------- mobile menu ---------------- */
  var burger = $(".burger");
  var menu = $("#menu");
  function setMenu(open) {
    root.classList.toggle("menu-open", open);
    if (burger) {
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
    if (menu) menu.setAttribute("aria-hidden", open ? "false" : "true");
    lockScroll(open);
    if (open && hasGSAP && !reduced) {
      gsap.fromTo($$(".menu__link, .menu .btn, .menu__meta", menu), { y: 60, opacity: 0 }, { y: 0, opacity: 1, stagger: 0.06, duration: 0.8, ease: "expo.out", delay: 0.25 });
    }
  }
  if (burger) burger.addEventListener("click", function () { setMenu(!root.classList.contains("menu-open")); });
  if (menu) $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });

  /* ---------------- text animation ---------------- */
  function initText(heroDelay) {
    if (!hasGSAP || reduced || !window.SplitText) {
      $$("[data-reveal]").forEach(function (el) { el.style.opacity = 1; el.style.transform = "none"; });
      return;
    }
    $$("[data-split]").forEach(function (el) {
      var split = SplitText.create(el, { type: "lines", mask: "lines", linesClass: "split-line" });
      var inHero = !!el.closest(".hero, .page-hero");
      gsap.from(split.lines, {
        yPercent: 110, duration: 1.25, ease: "expo.out", stagger: 0.09,
        delay: inHero ? heroDelay : 0,
        scrollTrigger: inHero ? null : { trigger: el, start: "top 86%" }
      });
    });
    $$("[data-scrub]").forEach(function (el) {
      var split = SplitText.create(el, { type: "words,chars", charsClass: "char" });
      gsap.to(split.chars, {
        opacity: 1, ease: "none", stagger: 0.03,
        scrollTrigger: { trigger: el, start: "top 82%", end: "bottom 45%", scrub: true }
      });
    });
    $$("[data-reveal]").forEach(function (el) {
      var inHero = !!el.closest(".hero, .page-hero");
      gsap.to(el, {
        opacity: 1, y: 0, duration: 1.2, ease: "expo.out",
        delay: (inHero ? heroDelay + 0.35 : 0) + (parseFloat(el.getAttribute("data-reveal")) || 0),
        scrollTrigger: inHero ? null : { trigger: el, start: "top 90%" }
      });
    });
  }

  /* ---------------- counters ---------------- */
  function formatNumber(v, fmt) {
    if (fmt === "comma") return Math.round(v).toLocaleString("en-US");
    if (fmt === "dec2") return v.toFixed(2);
    return String(Math.round(v));
  }
  function initCounters() {
    $$("[data-count]").forEach(function (el) {
      var end = parseFloat(el.getAttribute("data-count"));
      var fmt = el.getAttribute("data-format") || "";
      if (!hasGSAP || reduced || isNaN(end)) { el.textContent = formatNumber(end, fmt); return; }
      var o = { v: 0 };
      el.textContent = formatNumber(0, fmt);
      gsap.to(o, {
        v: end, duration: 2, ease: "expo.out",
        scrollTrigger: { trigger: el, start: "top 88%" },
        onUpdate: function () { el.textContent = formatNumber(o.v, fmt); }
      });
    });
  }

  /* ---------------- the one horizontal scroll ---------------- */
  function initHorizontal(sec) {
    if (!sec || !hasGSAP || reduced) return;
    var track = $(".hz__track", sec);
    var bar = $(".hz__progress i", sec);
    var distance = function () { return Math.max(0, track.scrollWidth - window.innerWidth); };
    gsap.to(track, {
      x: function () { return -distance(); },
      ease: "none",
      scrollTrigger: {
        trigger: sec, pin: true, scrub: 1, start: "top top",
        end: function () { return "+=" + distance(); },
        invalidateOnRefresh: true, anticipatePin: 1,
        onUpdate: function (self) { if (bar) gsap.set(bar, { scaleX: self.progress }); }
      }
    });
  }

  /* ---------------- stacking cards ---------------- */
  function initStack(sec) {
    (function () {
      var cards = $$(".card", sec);
      var scene = $("[data-scene]", sec);
      if (!hasGSAP || reduced || cards.length < 2) { sec.classList.add("stack--static"); return; }
      gsap.set(cards.slice(1), { yPercent: 115 });
      var current = 0;
      var tl = gsap.timeline({
        scrollTrigger: {
          trigger: sec, pin: true, start: "top top", scrub: 1,
          end: function () { return "+=" + (cards.length - 1) * window.innerHeight * 0.75; },
          onUpdate: function (self) {
            var i = Math.min(cards.length - 1, Math.round(self.progress * (cards.length - 1)));
            if (i !== current) {
              current = i;
              if (scene) scene.dispatchEvent(new CustomEvent("scene:index", { detail: i }));
            }
          }
        }
      });
      cards.slice(1).forEach(function (card, i) {
        tl.to(card, { yPercent: 0, ease: "none", duration: 1 }, i);
        tl.to(cards[i], { scale: 0.9, opacity: 0.35, ease: "none", duration: 1 }, i);
      });
    })();
  }

  /* ---------------- pinned steps ---------------- */
  function initStep(sec) {
    (function () {
      var steps = $$(".step", sec);
      var scene = $("[data-scene]", sec);
      var setActive = function (i) {
        steps.forEach(function (s, k) { s.classList.toggle("is-active", k === i); });
        if (scene) scene.dispatchEvent(new CustomEvent("scene:index", { detail: i }));
      };
      setActive(0);
      if (!hasGSAP || reduced) { steps.forEach(function (s) { s.classList.add("is-active"); }); return; }
      var current = 0;
      ScrollTrigger.create({
        trigger: sec, pin: true, start: "top top",
        end: function () { return "+=" + steps.length * window.innerHeight * 0.55; },
        onUpdate: function (self) {
          var i = Math.min(steps.length - 1, Math.floor(self.progress * steps.length));
          if (i !== current) { current = i; setActive(i); }
        }
      });
    })();
  }

  /* pinned sections must be created top-to-bottom so ScrollTrigger spaces them correctly */
  function initPins() {
    $$("[data-steps], [data-stack], [data-horizontal]").forEach(function (sec) {
      if (sec.hasAttribute("data-steps")) initStep(sec);
      else if (sec.hasAttribute("data-stack")) initStack(sec);
      else initHorizontal(sec);
    });
  }

  /* ---------------- timeline bar ---------------- */
  function initTimelines() {
    if (!hasGSAP || reduced) return;
    $$(".timeline").forEach(function (tl) {
      var bar = $(".timeline__bar", tl);
      if (!bar) return;
      gsap.to(bar, { scaleY: 1, ease: "none", scrollTrigger: { trigger: tl, start: "top 70%", end: "bottom 55%", scrub: true } });
    });
  }

  /* ---------------- quotes carousel ---------------- */
  function initQuotes() {
    $$("[data-quotes]").forEach(function (box) {
      var quotes = $$(".quote", box);
      var count = $(".quote-count", box);
      var i = 0, timer = null;
      function show(n) {
        var prev = quotes[i];
        i = (n + quotes.length) % quotes.length;
        var next = quotes[i];
        if (count) count.textContent = String(i + 1).padStart(2, "0") + " / " + String(quotes.length).padStart(2, "0");
        if (hasGSAP && !reduced && prev !== next) {
          gsap.to(prev, { opacity: 0, y: -30, duration: 0.5, ease: "power2.in", onComplete: function () { prev.classList.remove("is-active"); } });
          next.classList.add("is-active");
          gsap.fromTo(next, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.9, ease: "expo.out", delay: 0.35 });
        } else {
          quotes.forEach(function (q, k) { q.classList.toggle("is-active", k === i); q.style.opacity = k === i ? 1 : 0; });
        }
      }
      function auto() { if (reduced) return; clearInterval(timer); timer = setInterval(function () { show(i + 1); }, 7000); }
      var prevBtn = $("[data-prev]", box), nextBtn = $("[data-next]", box);
      if (prevBtn) prevBtn.addEventListener("click", function () { show(i - 1); auto(); });
      if (nextBtn) nextBtn.addEventListener("click", function () { show(i + 1); auto(); });
      box.addEventListener("mouseenter", function () { clearInterval(timer); });
      box.addEventListener("mouseleave", auto);
      show(0);
      auto();
    });
  }

  /* ---------------- work filters ---------------- */
  function initFilters() {
    var bar = $("[data-filters]");
    if (!bar) return;
    var cards = $$("[data-tags]");
    var buttons = $$(".filter", bar);
    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var f = btn.getAttribute("data-filter");
        buttons.forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
        cards.forEach(function (c) {
          var show = f === "all" || (" " + c.getAttribute("data-tags") + " ").indexOf(" " + f + " ") > -1;
          c.classList.toggle("is-hidden", !show);
        });
        if (hasGSAP && !reduced) {
          gsap.fromTo(cards.filter(function (c) { return !c.classList.contains("is-hidden"); }), { opacity: 0, y: 30 }, { opacity: 1, y: 0, stagger: 0.06, duration: 0.7, ease: "expo.out" });
          ScrollTrigger.refresh();
        }
        var live = $("[data-filter-count]");
        if (live) live.textContent = cards.filter(function (c) { return !c.classList.contains("is-hidden"); }).length + " case studies shown";
      });
    });
  }

  /* ---------------- FAQ accordion ---------------- */
  function initFaq() {
    $$(".faq details").forEach(function (d) {
      var summary = $("summary", d);
      var body = $(".faq__a", d);
      summary.addEventListener("click", function (e) {
        if (!hasGSAP || reduced) return;
        e.preventDefault();
        if (d.open) {
          gsap.to(body, { height: 0, duration: 0.5, ease: "power3.inOut", onComplete: function () { d.open = false; body.style.height = ""; ScrollTrigger.refresh(); } });
        } else {
          d.open = true;
          gsap.fromTo(body, { height: 0 }, { height: "auto", duration: 0.6, ease: "expo.out", onComplete: function () { ScrollTrigger.refresh(); } });
        }
      });
    });
  }

  /* ---------------- tilt + magnetic + cursor ---------------- */
  function initPointer() {
    if (!finePointer || reduced) return;
    $$("[data-tilt]").forEach(function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = "perspective(1000px) rotateX(" + (-y * 8) + "deg) rotateY(" + (x * 10) + "deg) translateZ(0)";
      });
      el.addEventListener("pointerleave", function () { el.style.transform = ""; });
    });
    if (hasGSAP) {
      $$("[data-magnetic]").forEach(function (el) {
        var xTo = gsap.quickTo(el, "x", { duration: 0.6, ease: "elastic.out(1, 0.4)" });
        var yTo = gsap.quickTo(el, "y", { duration: 0.6, ease: "elastic.out(1, 0.4)" });
        el.addEventListener("pointermove", function (e) {
          var r = el.getBoundingClientRect();
          xTo((e.clientX - (r.left + r.width / 2)) * 0.3);
          yTo((e.clientY - (r.top + r.height / 2)) * 0.35);
        });
        el.addEventListener("pointerleave", function () { xTo(0); yTo(0); });
      });
      var cursor = $(".cursor");
      if (cursor) {
        root.classList.add("has-cursor");
        var dot = $(".cursor__dot", cursor), ring = $(".cursor__ring", cursor);
        var dx = gsap.quickTo(dot, "x", { duration: 0.08 }), dy = gsap.quickTo(dot, "y", { duration: 0.08 });
        var rx = gsap.quickTo(ring, "x", { duration: 0.45, ease: "power3" }), ry = gsap.quickTo(ring, "y", { duration: 0.45, ease: "power3" });
        window.addEventListener("pointermove", function (e) { dx(e.clientX); dy(e.clientY); rx(e.clientX); ry(e.clientY); });
        document.addEventListener("pointerover", function (e) {
          var t = e.target.closest("[data-cursor]");
          cursor.classList.toggle("is-active", !!t);
          ring.textContent = t ? t.getAttribute("data-cursor") : "";
        });
      }
    }
  }

  /* ---------------- generated card art (canvas 2D, no image files) ---------------- */
  function hash(str) { var h = 2166136261; for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function rand(seed) { var s = seed; return function () { s += 0x6D2B79F5; var t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  function paintArt(cv) {
    var key = cv.getAttribute("data-art") || "mmag";
    var r = rand(hash(key));
    var W = cv.width, H = cv.height, g = cv.getContext("2d");
    var bg = g.createLinearGradient(0, 0, W, H);
    bg.addColorStop(0, "#2A0548"); bg.addColorStop(1, r() > 0.5 ? "#54078B" : "#12061F");
    g.fillStyle = bg; g.fillRect(0, 0, W, H);
    var palette = ["#F3C01F", "#B98CE8", "#7A2FC0", "#FFFFFF", "#54078B"];
    for (var i = 0; i < 5; i++) {
      var x = r() * W, y = r() * H, rad = (0.25 + r() * 0.5) * W;
      var c = palette[Math.floor(r() * palette.length)];
      var rg = g.createRadialGradient(x, y, 0, x, y, rad);
      rg.addColorStop(0, c + "AA"); rg.addColorStop(1, c + "00");
      g.fillStyle = rg; g.beginPath(); g.arc(x, y, rad, 0, Math.PI * 2); g.fill();
    }
    g.strokeStyle = "rgba(255,255,255,0.08)"; g.lineWidth = 1;
    for (var gx = 0; gx < W; gx += 60) { g.beginPath(); g.moveTo(gx, 0); g.lineTo(gx, H); g.stroke(); }
    for (var gy = 0; gy < H; gy += 60) { g.beginPath(); g.moveTo(0, gy); g.lineTo(W, gy); g.stroke(); }
    g.save();
    g.translate(W * (0.55 + r() * 0.2), H * (0.4 + r() * 0.2));
    g.rotate(-0.5 + r());
    for (var k = 0; k < 7; k++) {
      g.strokeStyle = k % 2 ? "rgba(243,192,31,0.55)" : "rgba(255,255,255,0.25)";
      g.lineWidth = 2 + k * 1.2;
      g.beginPath(); g.arc(0, 0, 70 + k * 48, -1.1, 1.6); g.stroke();
    }
    g.restore();
  }
  function initArt() { $$("canvas[data-art]").forEach(paintArt); }

  /* ---------------- modals ---------------- */
  var lastFocus = null;
  function openModal(id) {
    var m = document.getElementById("modal-" + id);
    if (!m) return;
    lastFocus = document.activeElement;
    m.classList.add("is-open");
    m.setAttribute("aria-hidden", "false");
    lockScroll(true);
    if (id === "video") {
      var frame = $(".video-frame", m);
      if (frame && !$("iframe", frame)) {
        var ifr = document.createElement("iframe");
        ifr.src = CFG.showreelEmbed;
        ifr.title = "MMAG showreel";
        ifr.allow = "autoplay; encrypted-media; picture-in-picture";
        ifr.allowFullscreen = true;
        frame.appendChild(ifr);
      }
    }
    setTimeout(function () {
      var f = $$("input:not([type=hidden]), select, textarea, button", $(".modal__panel", m)).filter(function (x) {
        return !x.closest(".hp") && !x.classList.contains("modal__close") && x.offsetParent !== null;
      })[0];
      if (f) f.focus();
    }, 60);
    track("modal_open", { modal: id });
  }
  function closeModal(m) {
    if (!m) return;
    m.classList.remove("is-open");
    m.setAttribute("aria-hidden", "true");
    if (m.id === "modal-video") { var fr = $(".video-frame iframe", m); if (fr) fr.remove(); }
    lockScroll(false);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  document.addEventListener("click", function (e) {
    var opener = e.target.closest("[data-open]");
    if (opener) { e.preventDefault(); if (root.classList.contains("menu-open")) setMenu(false); openModal(opener.getAttribute("data-open")); return; }
    var closer = e.target.closest("[data-close]");
    if (closer) { e.preventDefault(); closeModal(closer.closest(".modal")); }
  });
  document.addEventListener("keydown", function (e) {
    var open = $(".modal.is-open");
    if (e.key === "Escape") {
      if (open) closeModal(open);
      else if (root.classList.contains("menu-open")) setMenu(false);
    }
    if (e.key === "Tab" && open) {
      var f = $$("a[href], button:not([disabled]), input:not([type=hidden]), select, textarea, iframe", open).filter(function (x) { return x.offsetParent !== null && !x.closest(".hp"); });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  if (window.location.hash === "#download-portfolio") setTimeout(function () { openModal("portfolio"); }, 600);
  if (window.location.hash === "#schedule-a-call") setTimeout(function () { openModal("call"); }, 600);

  /* ---------------- misc ---------------- */
  $$("[data-year]").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });
  $$("[data-top]").forEach(function (el) {
    el.addEventListener("click", function (e) {
      e.preventDefault();
      if (lenis) lenis.scrollTo(0, { duration: 1.6 }); else window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
    });
  });

  /* ---------------- boot ---------------- */
  initArt();
  transitionIn();
  var fonts = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
  Promise.all([preloader(), fonts]).then(function () {
    var heroDelay = root.classList.contains("pt-in") ? 0.45 : 0.1;
    initText(heroDelay);
    initPins();
    initCounters();
    initTimelines();
    initQuotes();
    initFilters();
    initFaq();
    initPointer();
    navThemes();
    onScroll();
    if (hasGSAP) {
      ScrollTrigger.refresh();
      window.addEventListener("load", function () { ScrollTrigger.refresh(); });
    }
  });
})();
