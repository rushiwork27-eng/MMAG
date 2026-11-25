// Extract content from an archived (saved DOM) HTML page and render an approximate screenshot.
// The HTML is served under its original URL so site CSS applies; page JS is disabled; only mmag.in
// CSS/images/fonts and Google Fonts may load. The page's own Elementor CSS (post-<id>.css) was deleted
// from the server with the page, so Elementor's default container variables are injected as a fallback.
// Usage: node archive_extract.js <crawl.js path> <siteAuditDir> <html file> <original url> <slug>
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const [CRAWL, OUT, FILE, URL_, SLUG] = process.argv.slice(2);
const src = fs.readFileSync(CRAWL, 'utf8');
const extractSrc = src.slice(src.indexOf('function extract() {'), src.indexOf('// ---------- interactions'));
const FALLBACK_CSS = `
.elementor-invisible{visibility:visible!important;opacity:1!important}
.elementor-popup-modal,.iti__country-list{display:none!important}
[data-elementor-type="wp-page"] .e-con{--display:flex;--flex-direction:column;--container-widget-width:100%;--container-widget-height:initial;--container-widget-flex-grow:0;--container-widget-align-self:initial;--flex-wrap-mobile:wrap;--gap:20px}
[data-elementor-type="wp-page"] .e-con.e-grid{--display:grid;--e-con-grid-template-columns:repeat(3,1fr);--grid-auto-flow:row}
[data-elementor-type="wp-page"] .e-con.e-child:has(> .e-con + .e-con){--flex-direction:row;--flex-wrap:wrap;--container-widget-width:initial}
[data-elementor-type="wp-page"] .e-con.e-child:has(> .e-con + .e-con) > .e-con{flex:1 1 300px;min-width:0}
[data-elementor-type="wp-page"] img{max-height:640px;width:auto!important;max-width:100%;height:auto!important}
html,body{overflow-x:hidden!important;max-width:100vw}
[data-elementor-type="wp-page"] .elementor-absolute,[data-elementor-type="wp-page"] .elementor-fixed,[data-elementor-type="wp-page"] .e-con[style*="position"]{position:relative!important;inset:auto!important;top:auto!important;left:auto!important;right:auto!important;bottom:auto!important}
[data-elementor-type="wp-page"] [style*="transform"],[data-elementor-type="wp-page"] .elementor-motion-effects-element,[data-elementor-type="wp-page"] .elementor-motion-effects-layer{transform:none!important}
[data-elementor-type="wp-page"] .e-con,[data-elementor-type="wp-page"] .elementor-widget{max-width:100%;min-height:0!important}
[data-elementor-type="wp-page"] .e-con.e-parent>.e-con-inner{max-width:1280px;margin:0 auto}
#archive-banner{background:#F3C01F;color:#1E1E1E;font:600 16px/1.45 system-ui,sans-serif;padding:14px 24px;text-align:center}`;

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, javaScriptEnabled: false });
  const body = fs.readFileSync(FILE);
  await ctx.route('**/*', r => {
    const u = r.request().url(); const t = r.request().resourceType();
    if (u === URL_) return r.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body });
    if ((/^https:\/\/mmag\.in\/wp-(content|includes)\//.test(u) && ['stylesheet', 'image', 'font', 'media'].includes(t)) || /fonts\.(googleapis|gstatic)\.com/.test(u)) return r.continue();
    return r.abort();
  });
  const p = await ctx.newPage(); p.setDefaultTimeout(20000);
  await p.goto(URL_, { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(e => console.log('goto', e.message.slice(0, 80)));
  await p.evaluate(css => {
    const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    document.querySelectorAll('.e-con').forEach(e => e.classList.add('e-lazyloaded'));
    document.querySelectorAll('img[data-src],img[data-lazy-src]').forEach(i => { i.src = i.dataset.src || i.dataset.lazySrc; });
  }, FALLBACK_CSS);
  await p.waitForLoadState('load', { timeout: 45000 }).catch(() => console.log('load wait timed out'));
  await p.waitForTimeout(1500);
  const data = await p.evaluate(`(${extractSrc.trim()})()`);
  data.widgetSection = await p.evaluate(() => {
    const top = [...document.querySelectorAll('[data-elementor-type]')].filter(x => !x.parentElement.closest('[data-elementor-type]'));
    const map = {};
    top.forEach(doc => [...doc.children].forEach((sec, i) => sec.querySelectorAll('[data-widget_type]').forEach(w => { if (!w.closest('.swiper-slide-duplicate')) map[w.dataset.id] = doc.dataset.elementorType + ':' + doc.dataset.elementorId + '#' + i; })));
    return map;
  });
  data.url = URL_; data.slug = SLUG;
  data.archived = { source: 'earlier scrape (zip mmag-public-scrape), captured 12 Oct 2026', file: path.basename(FILE), statusNow: 404, layoutNote: 'page CSS post-<id>.css deleted from server; heights/layout approximate' };
  data.httpStatus = 200; data.interactions = []; data.mobileInteractions = []; data.consoleErrors = [];
  data.network = { requests: 0, totalKB: 0, failed: [], thirdPartyHosts: [] }; data.timing = null;
  fs.writeFileSync(path.join(OUT, 'data/pages', SLUG + '.json'), JSON.stringify(data, null, 1));
  await p.evaluate(() => {
    const bn = document.createElement('div'); bn.id = 'archive-banner';
    bn.textContent = 'ARCHIVED COPY, captured 12 Oct 2026. This page has since been removed from mmag.in (404). Its page-specific stylesheet was deleted with it, so spacing and layout are approximate; text and images are original.';
    document.body.prepend(bn);
  });
  await p.waitForTimeout(500);
  const fullH = await p.evaluate(() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight));
  await p.setViewportSize({ width: 1440, height: Math.min(fullH, 16000) });
  await p.waitForTimeout(800);
  await p.screenshot({ path: path.join(OUT, 'screenshots/desktop', SLUG + '.jpg'), type: 'jpeg', quality: 72, timeout: 60000 }).catch(e => console.log('screenshot failed', e.message.slice(0, 120)));
  console.log(SLUG, 'widgets', data.widgets.length, 'height', await p.evaluate(() => document.documentElement.scrollHeight));
  await b.close();
})();
