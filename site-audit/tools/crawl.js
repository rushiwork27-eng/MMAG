// Full-site crawl of mmag.in: content, structure, assets, styles, interactions, screenshots.
// Usage: node crawl.js <outDir> <seedUrlsFile>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = process.argv[2];
const SEEDS = fs.readFileSync(process.argv[3], 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
const HOST = 'mmag.in';
const MAX_PAGES = 60;

const mk = d => fs.mkdirSync(d, { recursive: true });
['data/pages', 'screenshots/desktop', 'screenshots/mobile', 'screenshots/interactions', 'backend/custom-code'].forEach(d => mk(path.join(OUT, d)));

const slugOf = u => {
  const p = new URL(u).pathname.replace(/^\/|\/$/g, '');
  return p ? p.replace(/\//g, '__') : 'home';
};
const norm = u => {
  try {
    const x = new URL(u);
    if (x.hostname.replace(/^www\./, '') !== HOST) return null;
    if (/^\/(wp-admin|wp-content|wp-includes|wp-json|feed|comments)/.test(x.pathname)) return null;
    if (/\.(xml|php|jpg|jpeg|png|webp|svg|gif|pdf|mp4|json|zip)$/i.test(x.pathname)) return null;
    x.hash = ''; x.search = '';
    if (!x.pathname.endsWith('/')) x.pathname += '/';
    return x.toString();
  } catch { return null; }
};

async function autoScroll(page) {
  await page.evaluate(async () => {
    const step = 350;
    for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await new Promise(r => setTimeout(r, 120));
    }
    window.scrollTo(0, document.documentElement.scrollHeight);
    await new Promise(r => setTimeout(r, 800));
  });
}

// ---------- in-page extraction ----------
function extract() {
  const clean = s => (s || '').replace(/ /g, ' ').replace(/[ \t]+/g, ' ').replace(/\n\s*\n+/g, '\n').trim();
  const txt = el => { if (!el) return ''; const t = clean(el.innerText); return t || clean(el.textContent); };
  const abs = u => { try { return u ? new URL(u, location.href).href : null; } catch { return u; } };
  const region = el => {
    const d = el.closest('[data-elementor-type]');
    if (!d) return el.closest('header') ? 'header' : el.closest('footer') ? 'footer' : 'other';
    const t = d.dataset.elementorType;
    const top = [...document.querySelectorAll('[data-elementor-type]')].filter(x => !x.parentElement.closest('[data-elementor-type]'));
    const root = top.find(x => x.contains(el)) || d;
    return root.dataset.elementorType === 'wp-page' ? 'main' : root.dataset.elementorType + (root.dataset.elementorType === 'popup' ? ':' + root.dataset.elementorId : '');
  };
  const hiddenOn = el => {
    const h = [];
    let n = el;
    while (n && n !== document.body) {
      (n.classList || []).forEach(c => { const m = c.match(/^elementor-hidden-(desktop|tablet|mobile|laptop|widescreen|mobile_extra|tablet_extra)$/); if (m && !h.includes(m[1])) h.push(m[1]); });
      n = n.parentElement;
    }
    return h;
  };
  const isVisible = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
  const notDup = el => !el.closest('.swiper-slide-duplicate');
  const img = i => ({ src: abs(i.getAttribute('src')), currentSrc: i.currentSrc || null, alt: i.getAttribute('alt'), title: i.getAttribute('title'), w: i.naturalWidth, h: i.naturalHeight, srcset: i.getAttribute('srcset') || null });

  const out = { url: location.href };
  // ---- head / SEO ----
  out.title = document.title;
  out.lang = document.documentElement.lang;
  out.meta = [...document.querySelectorAll('meta')].map(m => ({ name: m.getAttribute('name') || m.getAttribute('property') || m.getAttribute('http-equiv') || m.getAttribute('charset') && 'charset', content: m.getAttribute('content') || m.getAttribute('charset') })).filter(m => m.name);
  out.headLinks = [...document.querySelectorAll('head link')].filter(l => !/stylesheet|preload|dns-prefetch|preconnect|modulepreload/.test(l.rel)).map(l => ({ rel: l.rel, href: l.href, type: l.type, sizes: l.sizes && l.sizes.value }));
  out.jsonld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => { try { return JSON.parse(s.textContent); } catch { return s.textContent; } });
  out.headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(notDup).map(h => ({ level: h.tagName, text: txt(h), region: region(h), hiddenOn: hiddenOn(h) }));

  // ---- elementor documents ----
  out.documents = [...document.querySelectorAll('[data-elementor-type]')].map(e => ({ type: e.dataset.elementorType, id: e.dataset.elementorId, nested: !!e.parentElement.closest('[data-elementor-type]') }));

  // ---- widgets in document order ----
  const widgetData = w => {
    const t = w.dataset.widget_type || '';
    const base = { type: t, id: w.dataset.id, cssId: w.id || null, classes: [...w.classList].filter(c => !/^elementor-(element|widget|widget-[a-z-]+)$|^e-|^animated$|^elementor-invisible$/.test(c) && !c.startsWith('elementor-element-')).join(' ') || null, region: region(w), hiddenOn: hiddenOn(w), insideWidget: (w.parentElement.closest('[data-widget_type]') || {}).dataset?.widget_type || null };
    let s = {};
    try { s = JSON.parse(w.dataset.settings || '{}'); } catch {}
    if (s._animation || s.animation) base.animation = s._animation || s.animation;
    if (s.motion_fx_motion_fx_scrolling || s.motion_fx_motion_fx_mouse) base.motionFx = true;
    const q = sel => w.querySelector(sel);
    const qa = sel => [...w.querySelectorAll(sel)].filter(notDup);
    if (t.startsWith('heading')) { const h = q('.elementor-heading-title'); base.tag = h && h.tagName; base.text = txt(h); const a = h && h.querySelector('a'); if (a) base.href = a.href; }
    else if (t.startsWith('text-editor')) { base.text = txt(w); base.html = (q('.elementor-widget-container') || w).innerHTML.replace(/\s+/g, ' ').trim().slice(0, 4000); }
    else if (t.startsWith('button')) { const a = q('a,button'); base.text = txt(a); base.href = a && a.getAttribute('href'); base.target = a && a.getAttribute('target'); const ic = q('.elementor-button-icon i, .elementor-button-icon svg'); base.icon = ic ? (ic.className.baseVal ?? ic.className) : null; }
    else if (t.startsWith('image-carousel')) { base.slides = qa('.swiper-slide').map(sl => { const i = sl.querySelector('img'); const a = sl.querySelector('a'); return { ...(i ? img(i) : {}), link: a && a.href, caption: txt(sl.querySelector('figcaption')) }; }); base.settings = { autoplay: s.autoplay, speed: s.autoplay_speed, slides_to_show: s.slides_to_show, navigation: s.navigation, infinite: s.infinite }; }
    else if (t.startsWith('image-box')) { const i = q('img'); base.image = i && img(i); base.title = txt(q('.elementor-image-box-title')); base.description = txt(q('.elementor-image-box-description')); const a = q('a'); base.href = a && a.href; }
    else if (t.startsWith('image')) { const i = q('img'); base.image = i && img(i); const a = q('a'); base.href = a && a.href; base.caption = txt(q('figcaption')); }
    else if (t.startsWith('icon-box')) { base.title = txt(q('.elementor-icon-box-title')); base.description = txt(q('.elementor-icon-box-description')); const ic = q('.elementor-icon i, .elementor-icon svg'); base.icon = ic ? (ic.className.baseVal ?? ic.className) || ic.outerHTML.slice(0, 300) : null; const a = q('a'); base.href = a && a.href; }
    else if (t.startsWith('icon-list')) { base.items = qa('.elementor-icon-list-item').map(li => { const a = li.querySelector('a'); const ic = li.querySelector('.elementor-icon-list-icon i, .elementor-icon-list-icon svg'); return { text: txt(li), href: a && a.href, icon: ic ? (ic.className.baseVal ?? ic.className) : null }; }); }
    else if (t.startsWith('icon.')) { const ic = q('.elementor-icon i, .elementor-icon svg'); base.icon = ic ? (ic.className.baseVal ?? ic.className) || 'inline-svg' : null; const a = q('a'); base.href = a && a.href; }
    else if (t.startsWith('counter')) { const n = q('.elementor-counter-number'); base.prefix = txt(q('.elementor-counter-number-prefix')); base.number = n && (n.dataset.toValue || txt(n)); base.from = n && n.dataset.fromValue; base.suffix = txt(q('.elementor-counter-number-suffix')); base.title = txt(q('.elementor-counter-title')); }
    else if (t.startsWith('video')) { const v = q('video'); const f = q('iframe'); base.video = v ? { src: abs(v.getAttribute('src')) || v.currentSrc, poster: v.getAttribute('poster'), autoplay: v.autoplay, loop: v.loop, muted: v.muted, controls: v.controls } : null; base.iframe = f && (f.src || f.dataset.src || f.dataset.lazyLoad); base.settings = { video_type: s.video_type, youtube_url: s.youtube_url, hosted_url: s.hosted_url && s.hosted_url.url, autoplay: s.autoplay, loop: s.loop, mute: s.mute, controls: s.controls, lightbox: s.lightbox, image_overlay: s.image_overlay && s.image_overlay.url }; }
    else if (t.startsWith('nested-carousel') || t.startsWith('loop-carousel')) { base.slides = qa('.swiper-slide, .e-n-carousel > .e-con').map(sl => txt(sl)); base.settings = { autoplay: s.autoplay, speed: s.autoplay_speed, slides_to_show: s.slides_to_show, navigation: s.navigation, pagination: s.pagination, infinite: s.infinite }; }
    else if (t.startsWith('social-icons')) { base.items = qa('a').map(a => ({ href: a.href, label: a.getAttribute('aria-label') || txt(a), icon: (a.querySelector('i, svg') || {}).className?.baseVal ?? (a.querySelector('i') || {}).className })); }
    else if (t.startsWith('nav-menu')) { base.items = qa('nav.elementor-nav-menu--main a').map(a => ({ text: txt(a), href: a.href, depth: a.closest('ul.sub-menu') ? 1 : 0 })); }
    else if (t.startsWith('theme-site-logo') || t.startsWith('site-logo')) { const i = q('img'); base.image = i && img(i); const a = q('a'); base.href = a && a.href; }
    else if (t.startsWith('html')) { base.text = txt(w); base.html = w.innerHTML.replace(/\s+/g, ' ').trim().slice(0, 6000); }
    else if (t.startsWith('form')) { /* captured in forms */ base.formName = (q('form') || {}).name; }
    else if (t.startsWith('divider')) { const tx = q('.elementor-divider__text'); base.text = tx ? txt(tx) : null; }
    else if (t.startsWith('template')) { base.templateIds = [...w.querySelectorAll('[data-elementor-type]')].map(d => d.dataset.elementorId); }
    else { base.text = txt(w).slice(0, 3000); }
    return base;
  };
  out.widgets = [...document.querySelectorAll('[data-widget_type]')].filter(notDup).map(widgetData);
  out.widgetCounts = out.widgets.reduce((a, w) => (a[w.type] = (a[w.type] || 0) + 1, a), {});

  // ---- top-level sections (containers) with ordered text ----
  const topDocs = [...document.querySelectorAll('[data-elementor-type]')].filter(x => !x.parentElement.closest('[data-elementor-type]'));
  out.sections = [];
  topDocs.forEach(d => {
    const secs = [...d.children].filter(c => c.classList.contains('elementor-element') || c.classList.contains('e-con') || c.classList.contains('elementor-section'));
    secs.forEach((sec, i) => {
      const cs = getComputedStyle(sec);
      const bgEls = [sec, ...sec.querySelectorAll(':scope > .elementor-background-overlay, :scope > .e-con-inner')];
      const bg = bgEls.map(e => { const c = getComputedStyle(e); return { color: c.backgroundColor, image: c.backgroundImage !== 'none' ? c.backgroundImage : null }; });
      const vid = sec.querySelector(':scope > .elementor-background-video-container video');
      out.sections.push({ doc: d.dataset.elementorType + ':' + d.dataset.elementorId, index: i, dataId: sec.dataset.id, cssId: sec.id || null, classes: [...sec.classList].filter(c => !/^elementor-element|^e-con$|^e-flex$|^e-parent$|^e-lazyloaded$|^elementor-element-/.test(c)).join(' '), hiddenOn: hiddenOn(sec), height: Math.round(sec.getBoundingClientRect().height), background: bg, backgroundVideo: vid && (vid.currentSrc || vid.src), headings: [...sec.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(notDup).map(h => h.tagName + ': ' + txt(h)), text: txt(sec) });
    });
  });

  // ---- links ----
  out.links = [...document.querySelectorAll('a[href]')].filter(notDup).map(a => ({ href: a.getAttribute('href'), abs: a.href, text: txt(a).slice(0, 200), aria: a.getAttribute('aria-label'), title: a.getAttribute('title'), target: a.getAttribute('target'), rel: a.getAttribute('rel'), region: region(a), visible: isVisible(a), isButton: a.classList.contains('elementor-button') }));

  // ---- images (img + css backgrounds + svg inline count) ----
  out.images = [...document.querySelectorAll('img')].filter(notDup).map(i => ({ ...img(i), region: region(i), widget: (i.closest('[data-widget_type]') || {}).dataset?.widget_type || null, displayed: [Math.round(i.getBoundingClientRect().width), Math.round(i.getBoundingClientRect().height)], loading: i.getAttribute('loading') }));
  const bgs = new Map();
  document.querySelectorAll('*').forEach(e => { const b = getComputedStyle(e).backgroundImage; if (b && b !== 'none' && b.includes('url(')) { (b.match(/url\(["']?([^"')]+)["']?\)/g) || []).forEach(m => { const u = m.replace(/^url\(["']?|["']?\)$/g, ''); if (!bgs.has(u)) bgs.set(u, { url: u, region: region(e), tag: e.tagName, cls: String(e.className).slice(0, 100) }); }); } });
  out.backgroundImages = [...bgs.values()];
  out.inlineSvgCount = document.querySelectorAll('svg').length;

  // ---- media ----
  out.videos = [...document.querySelectorAll('video')].filter(notDup).map(v => ({ src: v.currentSrc || abs(v.getAttribute('src')) || abs((v.querySelector('source') || {}).src), poster: v.getAttribute('poster'), autoplay: v.autoplay, loop: v.loop, muted: v.muted, controls: v.controls, playsinline: v.playsInline, region: region(v), widget: (v.closest('[data-widget_type]') || {}).dataset?.widget_type || 'background' }));
  out.iframes = [...document.querySelectorAll('iframe')].map(f => ({ src: f.src || f.dataset.src, title: f.title, w: f.width, h: f.height }));
  out.lottie = [...document.querySelectorAll('[data-widget_type^="lottie"], lottie-player, dotlottie-player')].map(l => ({ settings: l.dataset.settings ? JSON.parse(l.dataset.settings).source_json : null, src: l.getAttribute('src') }));

  // ---- forms ----
  out.forms = [...document.querySelectorAll('form')].map(f => ({
    name: f.getAttribute('name'), id: f.id, action: f.getAttribute('action'), method: f.getAttribute('method'), region: region(f),
    fields: [...f.querySelectorAll('input,select,textarea')].map(i => {
      const grp = i.closest('.elementor-field-group');
      const lab = (i.id && f.querySelector(`label[for="${CSS.escape(i.id)}"]`)) || (grp && grp.querySelector('label'));
      return { tag: i.tagName.toLowerCase(), type: i.type, name: i.name, id: i.id, label: lab ? txt(lab) : null, placeholder: i.placeholder || null, required: i.required || i.getAttribute('aria-required') === 'true', pattern: i.getAttribute('pattern'), options: i.tagName === 'SELECT' ? [...i.options].map(o => o.text) : undefined, width: grp ? [...grp.classList].find(c => /elementor-col-/.test(c)) : null };
    }).filter(x => x.type !== 'hidden' || /form_id|queried_id|post_id/.test(x.name)),
    submit: [...f.querySelectorAll('button[type=submit], input[type=submit]')].map(b => txt(b) || b.value),
    hasRecaptcha: !!f.querySelector('.elementor-g-recaptcha, .g-recaptcha, [data-sitekey]'),
  }));

  // ---- buttons (non-anchor) ----
  out.buttons = [...document.querySelectorAll('button, [role=button]')].filter(notDup).map(b => ({ text: txt(b).slice(0, 120), aria: b.getAttribute('aria-label'), cls: String(b.className).slice(0, 120), region: region(b), visible: isVisible(b) }));

  // ---- interactive components ----
  out.components = {
    swipers: [...document.querySelectorAll('.swiper')].map(sw => ({ widget: (sw.closest('[data-widget_type]') || {}).dataset?.widget_type, slides: sw.querySelectorAll('.swiper-slide:not(.swiper-slide-duplicate)').length, hasNav: !!sw.closest('[data-widget_type]')?.querySelector('.elementor-swiper-button, .swiper-button-next'), hasPagination: !!sw.closest('[data-widget_type]')?.querySelector('.swiper-pagination') })),
    jetTabs: [...document.querySelectorAll('.jet-tabs')].map(t => ({ tabs: [...t.querySelectorAll(':scope > .jet-tabs__control-wrapper .jet-tabs__control, .jet-tabs__control')].map(c => txt(c)) })),
    nTabs: [...document.querySelectorAll('.e-n-tabs')].map(t => [...t.querySelectorAll('.e-n-tab-title')].map(txt)),
    accordions: [...document.querySelectorAll('.e-n-accordion-item, .elementor-accordion-item, .elementor-toggle-item, details')].map(a => ({ title: txt(a.querySelector('summary, .elementor-tab-title, .e-n-accordion-item-title')), body: clean(a.textContent).slice(0, 1500) })),
    popupsInDom: [...document.querySelectorAll('[data-elementor-type="popup"]')].map(p => ({ id: p.dataset.elementorId, text: clean(p.textContent).slice(0, 3000) })),
    popupTriggers: [...document.querySelectorAll('a[href*="elementor-action"]')].map(a => ({ text: txt(a), href: decodeURIComponent(a.getAttribute('href')) })),
    floatingButtons: [...document.querySelectorAll('[data-elementor-type="floating-buttons"], .e-floating-buttons, .e-contact-buttons')].map(f => ({ text: clean(f.textContent).slice(0, 500), links: [...f.querySelectorAll('a')].map(a => a.href) })),
    customIds: [...document.querySelectorAll('[id]')].map(e => e.id).filter(id => !/^(elementor|wp-|e-n-|jet-|swiper|menu-item|ccfef|form-field|g-recaptcha|rc-|__|cf-)/.test(id)).slice(0, 80),
    stickyElements: [...document.querySelectorAll('[data-settings*="sticky"]')].map(e => { try { const s = JSON.parse(e.dataset.settings); return { dataId: e.dataset.id, sticky: s.sticky, on: s.sticky_on, offset: s.sticky_offset, effectsOffset: s.sticky_effects_offset }; } catch { return null; } }).filter(x => x && x.sticky),
    animatedCount: [...document.querySelectorAll('[data-settings*="animation"]')].length,
  };

  // ---- scripts / tracking ----
  out.scripts = [...document.scripts].map(s => s.src).filter(Boolean);
  out.inlineScripts = [...document.scripts].filter(s => !s.src && !/application\/ld\+json|speculationrules/.test(s.type)).map(s => s.textContent);
  out.inlineStyles = [...document.querySelectorAll('style')].map(s => ({ id: s.id, css: s.textContent })).filter(s => s.css.length > 0);
  out.stylesheets = [...document.querySelectorAll('link[rel=stylesheet]')].map(l => l.href);

  // ---- style tally (colours / typography) ----
  const colors = {}, fonts = {}, sizes = {};
  const bump = (o, k, n = 1) => { if (k) o[k] = (o[k] || 0) + n; };
  document.querySelectorAll('body *').forEach(e => {
    if (!isVisible(e)) return;
    const c = getComputedStyle(e);
    const hasText = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (hasText) { bump(colors, 'text ' + c.color); bump(fonts, c.fontFamily.split(',')[0].replace(/"/g, '') + ' ' + c.fontWeight); bump(sizes, c.fontSize + '/' + c.lineHeight + ' ' + c.fontWeight + ' ' + e.tagName); }
    if (c.backgroundColor !== 'rgba(0, 0, 0, 0)') bump(colors, 'bg ' + c.backgroundColor);
    if (parseFloat(c.borderTopWidth) > 0 && c.borderTopStyle !== 'none') bump(colors, 'border ' + c.borderTopColor);
    if (c.backgroundImage.includes('gradient')) bump(colors, 'gradient ' + c.backgroundImage.slice(0, 200));
  });
  out.styleTally = { colors, fonts, sizes };
  const rootCs = getComputedStyle(document.documentElement);
  out.cssVars = {};
  [...document.styleSheets].forEach(ss => { try { [...ss.cssRules].forEach(r => { if (r.style) for (const p of r.style) if (p.startsWith('--e-global') || p.startsWith('--mmag')) out.cssVars[p] = rootCs.getPropertyValue(p).trim() || r.style.getPropertyValue(p).trim(); }); } catch {} });
  out.pageHeight = document.documentElement.scrollHeight;
  out.bodyText = clean(document.body.innerText);
  return out;
}

// ---------- interactions ----------
async function interactDesktop(page, slug, res) {
  const log = [];
  // nav hover — detect dropdowns
  const navItems = await page.$$('header nav.elementor-nav-menu--main > ul > li, [data-elementor-type="header"] nav.elementor-nav-menu--main > ul > li');
  for (const [i, li] of navItems.entries()) {
    try {
      if (!(await li.isVisible())) continue;
      await li.hover(); await page.waitForTimeout(350);
      const r = await li.evaluate(el => ({ text: el.querySelector('a').innerText.trim(), sub: [...el.querySelectorAll('.sub-menu a')].map(a => ({ text: a.innerText.trim(), href: a.href })), color: getComputedStyle(el.querySelector('a')).color }));
      log.push({ action: 'hover-nav', ...r });
      if (r.sub.length) await page.screenshot({ path: path.join(OUT, 'screenshots/interactions', `${slug}-nav-${i}.png`) });
    } catch (e) { log.push({ action: 'hover-nav', error: e.message.slice(0, 120) }); }
  }
  // button hover states
  const btns = await page.$$('a.elementor-button, button.elementor-button');
  const seen = new Set();
  for (const b of btns) {
    try {
      if (!(await b.isVisible())) continue;
      const before = await b.evaluate(e => { const c = getComputedStyle(e); return { text: e.innerText.trim(), bg: c.backgroundColor, color: c.color, border: c.borderColor + ' ' + c.borderWidth, radius: c.borderRadius, padding: c.padding, font: c.fontFamily.split(',')[0] + ' ' + c.fontSize + ' ' + c.fontWeight, transition: c.transition.slice(0, 80) }; });
      const key = before.bg + before.color + before.radius + before.font;
      if (seen.has(key)) continue; seen.add(key);
      await b.scrollIntoViewIfNeeded(); await b.hover(); await page.waitForTimeout(450);
      const after = await b.evaluate(e => { const c = getComputedStyle(e); return { bg: c.backgroundColor, color: c.color, border: c.borderColor, transform: c.transform }; });
      log.push({ action: 'hover-button', before, after });
    } catch (e) { }
  }
  // image-box / icon-box hover sample
  // tabs (jet-tabs / nested tabs / accordions)
  for (const sel of ['.jet-tabs__control', '.e-n-tab-title', '.elementor-tab-title', '.e-n-accordion-item-title', 'summary']) {
    const els = await page.$$(sel);
    for (const [i, el] of els.entries()) {
      try {
        if (!(await el.isVisible())) continue;
        await el.scrollIntoViewIfNeeded({ timeout: 4000 }); await el.click({ timeout: 3000 }); await page.waitForTimeout(500);
        const r = await el.evaluate((e, sel) => {
          const t = e.innerText.trim();
          let panel = null;
          if (sel === '.jet-tabs__control') { const tabs = e.closest('.jet-tabs'); panel = tabs.querySelector('.jet-tabs__content.active-content') || tabs.querySelector('.jet-tabs__content-wrapper'); }
          else if (sel === '.e-n-tab-title') { panel = document.getElementById(e.getAttribute('aria-controls')); }
          else { panel = e.parentElement; }
          return { title: t, content: panel ? panel.innerText.replace(/\s+\n/g, '\n').trim().slice(0, 3000) : null };
        }, sel);
        log.push({ action: 'click-tab', selector: sel, ...r });
        if (i < 6) await el.evaluate(e => e.closest('.jet-tabs, .e-n-tabs, .elementor-widget, details') || e).then(() => null);
      } catch (e) { log.push({ action: 'click-tab', selector: sel, error: e.message.slice(0, 120) }); }
    }
  }
  // carousels: click next arrow, verify slide change
  const carousels = await page.$$('[data-widget_type^="image-carousel"], [data-widget_type^="nested-carousel"], [data-widget_type^="testimonial-carousel"], [data-widget_type^="loop-carousel"]');
  for (const [i, c] of carousels.entries()) {
    try {
      if (!(await c.isVisible())) { log.push({ action: 'carousel', widget: await c.getAttribute('data-widget_type'), note: 'hidden on this breakpoint (elementor-hidden-*), not interactive' }); continue; }
      await c.scrollIntoViewIfNeeded({ timeout: 5000 }); await page.waitForTimeout(300);
      const next = await c.$('.elementor-swiper-button-next, .swiper-button-next');
      const before = await c.evaluate(e => { const s = e.querySelector('.swiper'); return s && s.swiper ? s.swiper.realIndex : (e.querySelector('.swiper-slide-active') || {}).dataset?.swiperSlideIndex; });
      if (next && await next.isVisible()) { await next.click(); await page.waitForTimeout(700); }
      const after = await c.evaluate(e => { const s = e.querySelector('.swiper'); return s && s.swiper ? s.swiper.realIndex : (e.querySelector('.swiper-slide-active') || {}).dataset?.swiperSlideIndex; });
      log.push({ action: 'carousel', widget: await c.getAttribute('data-widget_type'), hasNextArrow: !!next, indexBefore: before, indexAfter: after });
      await c.screenshot({ path: path.join(OUT, 'screenshots/interactions', `${slug}-carousel-${i}.png`) }).catch(() => {});
    } catch (e) { log.push({ action: 'carousel', error: e.message.slice(0, 120) }); }
  }
  // popup / '#' / javascript: triggers — click and see what opens
  const triggers = await page.$$('a[href*="elementor-action"], a[href="#"], a[href^="javascript"]');
  for (const [i, t] of triggers.entries()) {
    try {
      if (!(await t.isVisible())) continue;
      const label = (await t.innerText()).trim().slice(0, 60) || await t.getAttribute('aria-label');
      await t.scrollIntoViewIfNeeded({ timeout: 4000 }); await t.click({ timeout: 3000 }); await page.waitForTimeout(1200);
      const popup = await page.evaluate(() => { const m = [...document.querySelectorAll('.elementor-popup-modal, .dialog-widget, .elementor-lightbox')].find(e => getComputedStyle(e).display !== 'none'); if (!m) return null; const f = m.querySelector('iframe, video'); return { kind: m.classList.contains('elementor-lightbox') ? 'lightbox' : 'popup', id: (m.id || ''), text: m.innerText.trim().slice(0, 3000), media: f ? (f.src || f.currentSrc) : null }; });
      const href = await t.getAttribute('href');
      let decoded = null; try { const m = decodeURIComponent(href).match(/settings=([^&]+)/); if (m) decoded = JSON.parse(Buffer.from(m[1], 'base64').toString()); } catch {}
      log.push({ action: 'click-trigger', label, href, decodedSettings: decoded, opened: popup, scrollY: await page.evaluate(() => scrollY) });
      if (popup) {
        await page.screenshot({ path: path.join(OUT, 'screenshots/interactions', `${slug}-${popup.kind}-${i}.png`) });
        await page.keyboard.press('Escape').catch(() => {}); await page.waitForTimeout(300);
        await page.evaluate(() => { document.querySelectorAll('.dialog-close-button, .dialog-lightbox-close-button, .elementor-popup-modal .eicon-close').forEach(b => { try { b.click(); } catch {} }); });
        await page.waitForTimeout(500);
      }
    } catch (e) { log.push({ action: 'click-trigger', error: e.message.slice(0, 120) }); }
  }
  // form: check client-side validation WITHOUT submitting
  const forms = await page.$$('form');
  for (const f of forms) {
    try {
      const r = await f.evaluate(form => ({ name: form.getAttribute('name'), valid: form.checkValidity(), invalid: [...form.querySelectorAll(':invalid')].map(i => ({ name: i.name, msg: i.validationMessage })) }));
      log.push({ action: 'form-validation-check (not submitted)', ...r });
    } catch {}
  }
  // scroll behaviours: sticky header, back-to-top, progress line
  await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(400);
  const hdr0 = await page.evaluate(() => { const h = document.querySelector('[data-elementor-type="header"] > .e-con, [data-elementor-type="header"] > .elementor-element, [data-elementor-type="header"] section'); if (!h) return null; const c = getComputedStyle(h); return { position: c.position, bg: c.backgroundColor, height: h.getBoundingClientRect().height, top: h.getBoundingClientRect().top }; });
  await page.evaluate(() => window.scrollTo(0, 1600)); await page.waitForTimeout(900);
  const hdr1 = await page.evaluate(() => { const hs = [...document.querySelectorAll('[data-elementor-type="header"] .elementor-sticky--active, [data-elementor-type="header"] > .e-con, [data-elementor-type="header"] > .elementor-element')]; const h = hs.find(x => x.classList.contains('elementor-sticky--active')) || hs[0]; if (!h) return null; const c = getComputedStyle(h); return { position: c.position, bg: c.backgroundColor, height: h.getBoundingClientRect().height, top: h.getBoundingClientRect().top, stickyActive: !!document.querySelector('.elementor-sticky--active'), shadow: c.boxShadow }; });
  const extras = await page.evaluate(() => {
    const vis = id => { const e = document.getElementById(id) || document.querySelector(id); if (!e) return null; const c = getComputedStyle(e); return { display: c.display, opacity: c.opacity, visibility: c.visibility, html: e.outerHTML.slice(0, 400) }; };
    return { cursorImage: vis('cursor-image'), progressLine: vis('progressLine'), backToTop: vis('.back-to-top, #back-to-top, .scroll-top, #scrollTop, .go-top') };
  });
  log.push({ action: 'scroll-behaviour', headerAtTop: hdr0, headerAfterScroll1600: hdr1, ...extras });
  await page.screenshot({ path: path.join(OUT, 'screenshots/interactions', `${slug}-scrolled-header.png`) });
  res.interactions = log;
}

async function interactMobile(page, slug, res) {
  const log = [];
  try {
    const toggle = await page.$('.elementor-menu-toggle');
    if (toggle && await toggle.isVisible()) {
      await toggle.click(); await page.waitForTimeout(700);
      const items = await page.evaluate(() => [...document.querySelectorAll('nav.elementor-nav-menu--dropdown a')].filter(a => a.getBoundingClientRect().height > 0).map(a => ({ text: a.innerText.trim(), href: a.href })));
      log.push({ action: 'mobile-menu-open', items });
      await page.screenshot({ path: path.join(OUT, 'screenshots/interactions', `${slug}-mobile-menu.png`) });
      await toggle.click(); await page.waitForTimeout(400);
    } else log.push({ action: 'mobile-menu-open', note: 'no visible .elementor-menu-toggle' });
  } catch (e) { log.push({ action: 'mobile-menu-open', error: e.message.slice(0, 120) }); }
  res.mobileInteractions = log;
  res.mobileHeadings = await page.evaluate(() => [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(h => h.getBoundingClientRect().height > 0 && !h.closest('.swiper-slide-duplicate')).map(h => h.tagName + ': ' + h.innerText.trim()));
  res.mobileHorizontalOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth ? document.documentElement.scrollWidth : false);
}

(async () => {
  const browser = await chromium.launch();
  const desk = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  const mob = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
  const queue = SEEDS.map(norm).filter(Boolean);
  const done = new Set();
  const summary = [];
  while (queue.length && done.size < MAX_PAGES) {
    const url = queue.shift();
    if (done.has(url)) continue;
    done.add(url);
    const slug = slugOf(url);
    const t0 = Date.now();
    process.stdout.write(`[${done.size}] ${url} ... `);
    const page = await desk.newPage(); page.setDefaultTimeout(8000);
    const net = { requests: 0, bytes: 0, failed: [], thirdParty: new Set(), statusMain: null, redirects: [] };
    page.on('requestfinished', async r => { net.requests++; try { const s = await r.sizes(); net.bytes += s.responseBodySize; } catch {} try { const h = new URL(r.url()).hostname; if (!h.endsWith(HOST)) net.thirdParty.add(h); } catch {} });
    page.on('requestfailed', r => net.failed.push(r.url() + ' :: ' + (r.failure() || {}).errorText));
    const consoleErrors = [];
    page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 300)); });
    page.on('pageerror', e => consoleErrors.push('pageerror: ' + e.message.slice(0, 300)));
    let resp;
    try { resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 90000 }); }
    catch (e) { try { resp = await page.goto(url, { waitUntil: 'load', timeout: 90000 }); } catch (e2) { console.log('FAILED', e2.message); summary.push({ url, error: e2.message }); await page.close(); continue; } }
    net.statusMain = resp && resp.status();
    let chain = resp && resp.request().redirectedFrom(); while (chain) { net.redirects.push(chain.url()); chain = chain.redirectedFrom(); }
    const timing = await page.evaluate(() => { const n = performance.getEntriesByType('navigation')[0]; return n ? { ttfb: Math.round(n.responseStart), domContentLoaded: Math.round(n.domContentLoadedEventEnd), load: Math.round(n.loadEventEnd), transferKB: Math.round(n.transferSize / 1024) } : null; });
    await autoScroll(page);
    await page.waitForTimeout(1200);
    const data = await page.evaluate(extract);
    data.slug = slug; data.httpStatus = net.statusMain; data.finalUrl = page.url(); data.redirectsFrom = net.redirects; data.timing = timing;
    // full-page desktop screenshot
    await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(600);
    await page.screenshot({ path: path.join(OUT, 'screenshots/desktop', `${slug}.jpg`), fullPage: true, type: 'jpeg', quality: 70 }).catch(e => data.screenshotError = e.message);
    await page.screenshot({ path: path.join(OUT, 'screenshots/desktop', `${slug}-fold.png`) });
    await interactDesktop(page, slug, data);
    data.network = { requests: net.requests, totalKB: Math.round(net.bytes / 1024), failed: net.failed, thirdPartyHosts: [...net.thirdParty] };
    data.consoleErrors = consoleErrors;
    await page.close();
    // mobile
    const mp = await mob.newPage();
    try {
      await mp.goto(url, { waitUntil: 'networkidle', timeout: 90000 }).catch(() => mp.goto(url, { waitUntil: 'load', timeout: 90000 }));
      await autoScroll(mp); await mp.waitForTimeout(1000);
      await mp.evaluate(() => window.scrollTo(0, 0)); await mp.waitForTimeout(500);
      await mp.screenshot({ path: path.join(OUT, 'screenshots/mobile', `${slug}.jpg`), fullPage: true, type: 'jpeg', quality: 70 }).catch(() => {});
      await interactMobile(mp, slug, data);
    } catch (e) { data.mobileError = e.message; }
    await mp.close();
    // discover links
    for (const l of data.links) { const n = norm(l.abs); if (n && !done.has(n) && !queue.includes(n)) queue.push(n); }
    fs.writeFileSync(path.join(OUT, 'data/pages', `${slug}.json`), JSON.stringify(data, null, 1));
    summary.push({ url, slug, status: data.httpStatus, title: data.title, h1: data.headings.filter(h => h.level === 'H1').map(h => h.text), words: data.bodyText.split(/\s+/).length, widgets: data.widgets.length, images: data.images.length, videos: data.videos.length, links: data.links.length, forms: data.forms.length, height: data.pageHeight, consoleErrors: consoleErrors.length, ms: Date.now() - t0 });
    console.log(`${data.httpStatus} ${Date.now() - t0}ms`);
  }
  fs.writeFileSync(path.join(OUT, 'data/crawl-summary.json'), JSON.stringify({ crawledAt: new Date().toISOString(), pages: summary, notCrawled: queue }, null, 1));
  await browser.close();
})();
