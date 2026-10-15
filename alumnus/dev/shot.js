const { chromium } = require('playwright');
(async () => {
  const [, , url, out, width = '1440', height = '900', mode = 'full'] = process.argv;
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const page = await browser.newPage({ viewport: { width: Number(width), height: Number(height) }, deviceScaleFactor: 1 });
  const logs = [];
  page.on('console', (m) => { if (['error', 'warning'].includes(m.type())) logs.push(`${m.type()}: ${m.text()}`); });
  page.on('pageerror', (e) => logs.push(`pageerror: ${e.message}`));
  await page.goto(url, { waitUntil: 'networkidle' }).catch(() => page.goto(url, { waitUntil: 'load' }));
  // reveal everything (scroll through so observers fire) then return to top
  await page.addStyleTag({ content: 'html{scroll-behavior:auto !important}' + (process.env.CLEAN ? ' discount-popup,.popup-teaser,sticky-buy{display:none !important}' : '') });
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); }
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-in'));
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(800);
  if (mode === 'full') await page.screenshot({ path: out, fullPage: true });
  else await page.screenshot({ path: out });
  console.log(logs.join('\n') || 'no console errors');
  await browser.close();
})();
