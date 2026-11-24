// Second pass: widget -> section mapping, popup form fields, Elementor breakpoints.
// Usage: node pass2.js <siteAuditDir>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const OUT = process.argv[2];
const pagesDir = path.join(OUT, 'data/pages');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const files = fs.readdirSync(pagesDir).filter(f => f.endsWith('.json'));
  const popups = {};
  let breakpoints = null;
  for (const f of files) {
    const d = JSON.parse(fs.readFileSync(path.join(pagesDir, f)));
    if (d.httpStatus !== 200) continue;
    const page = await ctx.newPage(); page.setDefaultTimeout(8000);
    await page.goto(d.url, { waitUntil: 'networkidle', timeout: 90000 }).catch(() => {});
    const r = await page.evaluate(() => {
      const top = [...document.querySelectorAll('[data-elementor-type]')].filter(x => !x.parentElement.closest('[data-elementor-type]'));
      const map = {};
      top.forEach(doc => {
        [...doc.children].forEach((sec, i) => {
          sec.querySelectorAll('[data-widget_type]').forEach(w => { if (!w.closest('.swiper-slide-duplicate')) map[w.dataset.id] = doc.dataset.elementorType + ':' + doc.dataset.elementorId + '#' + i; });
        });
      });
      const cfg = window.elementorFrontendConfig || {};
      return { map, breakpoints: cfg.responsive && cfg.responsive.activeBreakpoints, kit: cfg.kit };
    });
    d.widgetSection = r.map;
    if (!breakpoints) breakpoints = { activeBreakpoints: r.breakpoints, kit: r.kit };
    // popups: open each distinct popup trigger and read its form
    const triggers = await page.$$('a[href*="popup%3Aopen"], a[href*="popup:open"]');
    for (const t of triggers) {
      try {
        const href = decodeURIComponent(await t.getAttribute('href'));
        const m = href.match(/settings=([^&]+)/); const id = m ? JSON.parse(Buffer.from(m[1], 'base64').toString()).id : href;
        if (popups[id] || !(await t.isVisible())) continue;
        await t.scrollIntoViewIfNeeded({ timeout: 4000 }); await t.click({ timeout: 3000 }); await page.waitForTimeout(1500);
        const p = await page.evaluate(() => {
          const modal = [...document.querySelectorAll('.elementor-popup-modal')].find(e => getComputedStyle(e).display !== 'none');
          if (!modal) return null;
          const clean = s => (s || '').replace(/\s+/g, ' ').trim();
          const forms = [...modal.querySelectorAll('form')].map(f => ({
            name: f.getAttribute('name'),
            fields: [...f.querySelectorAll('input,select,textarea')].filter(i => i.type !== 'hidden').map(i => {
              const g = i.closest('.elementor-field-group'); const l = g && g.querySelector('label');
              return { tag: i.tagName.toLowerCase(), type: i.type, name: i.name, label: l ? clean(l.textContent) : null, placeholder: i.placeholder || null, required: i.required, options: i.tagName === 'SELECT' ? [...i.options].map(o => o.text) : undefined };
            }),
            submit: [...f.querySelectorAll('button[type=submit]')].map(b => clean(b.textContent)),
            recaptcha: !!f.querySelector('.elementor-g-recaptcha, [data-sitekey]'),
          }));
          const imgs = [...modal.querySelectorAll('img')].map(i => ({ src: i.currentSrc || i.src, alt: i.alt }));
          const box = modal.querySelector('.dialog-message, .dialog-widget-content'); const cs = box ? getComputedStyle(box) : null;
          return { modalId: modal.id, text: modal.innerText.trim(), headings: [...modal.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => h.tagName + ': ' + clean(h.textContent)), forms, images: imgs, size: box ? [box.getBoundingClientRect().width, box.getBoundingClientRect().height] : null, bg: cs && cs.backgroundColor, radius: cs && cs.borderRadius };
        });
        if (p) { popups[id] = { trigger: (await t.innerText()).trim(), foundOn: d.url, ...p }; await page.screenshot({ path: path.join(OUT, 'screenshots/interactions', `popup-${id}.png`) }); }
        await page.keyboard.press('Escape').catch(() => {});
        await page.evaluate(() => document.querySelectorAll('.dialog-close-button').forEach(b => { try { b.click(); } catch {} }));
        await page.waitForTimeout(500);
      } catch (e) { console.log('popup err', e.message.slice(0, 100)); }
    }
    fs.writeFileSync(path.join(pagesDir, f), JSON.stringify(d, null, 1));
    console.log('ok', f, Object.keys(r.map).length, 'widgets mapped');
    await page.close();
  }
  fs.writeFileSync(path.join(OUT, 'data/popups.json'), JSON.stringify(popups, null, 1));
  fs.writeFileSync(path.join(OUT, 'data/elementor-config.json'), JSON.stringify(breakpoints, null, 1));
  console.log('popups', Object.keys(popups));
  await browser.close();
})();
