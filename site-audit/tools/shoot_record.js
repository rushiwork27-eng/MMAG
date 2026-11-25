const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [IN, OUT] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto('file://' + path.resolve(IN), { waitUntil: 'networkidle', timeout: 90000 }).catch(() => {});
  await p.waitForTimeout(1000);
  await p.screenshot({ path: OUT, fullPage: true, type: 'jpeg', quality: 75 });
  console.log(OUT, await p.evaluate(() => document.documentElement.scrollHeight), 'broken imgs:', await p.evaluate(() => [...document.images].filter(i => !i.naturalWidth).length));
  await b.close();
})();
