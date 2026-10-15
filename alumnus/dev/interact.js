const { chromium } = require('playwright');
const base = process.env.PREVIEW_URL || 'http://127.0.0.1:8765/';
(async () => {
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const results = [];
  const check = (name, ok, detail = '') => results.push(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  (' + detail + ')' : ''}`);

  // ---------- desktop homepage ----------
  let page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await page.addInitScript(() => localStorage.setItem('alumnus-popup-dismissed', String(Date.now())));
  await page.goto(base + 'index.html', { waitUntil: 'load' });
  await page.addStyleTag({ content: 'html{scroll-behavior:auto !important}' });

  // bundle tiers -> button price + quantity
  const btnPrice = async () => (await page.textContent('[data-button-price]')).trim();
  check('default tier (Duo) selected', (await btnPrice()) === '$250.20', await btnPrice());
  await page.click('input[id$="-tier-3"]');
  check('3-pack tier updates button price', (await btnPrice()) === '$354.45', await btnPrice());
  check('3-pack sets quantity input', (await page.inputValue('[data-qty-input]')) === '3');
  await page.click('input[id$="-tier-1"]');
  check('solo tier updates price', (await btnPrice()) === '$139.00', await btnPrice());

  // color swatch -> variant id + label
  await page.click('.option__value input[value="Silver"]');
  check('color change updates variant id', (await page.inputValue('[data-variant-input]')) === '4402');
  check('color legend updates', (await page.textContent('[data-option-selected="0"]')).trim() === 'Silver');

  // countdown running
  const cd1 = await page.textContent('.buy__countdown .countdown__value');
  await page.waitForTimeout(1100);
  const cd2 = await page.textContent('.buy__countdown .countdown__value');
  check('countdown ticks', cd1 !== cd2 && /\d/.test(cd2), cd2.trim());

  // sticky bar hidden at top, visible after scrolling past buy box
  check('sticky bar hidden at top', !(await page.$eval('sticky-buy', (el) => el.classList.contains('is-visible'))));
  await page.evaluate(() => window.scrollTo(0, document.querySelector('#specs').offsetTop));
  await page.waitForTimeout(500);
  check('sticky bar visible after buy box', await page.$eval('sticky-buy', (el) => el.classList.contains('is-visible')));

  // sticky header stays pinned to the top after scrolling
  const headerTop = await page.$eval('.header', (el) => Math.round(el.getBoundingClientRect().top));
  check('header sticks to the top while scrolling', headerTop === 0, `top=${headerTop}`);

  // FAQ tabs
  await page.click('.faq__tab[data-tab="shipping"]');
  const visible = await page.$$eval('details[data-category]', (els) => els.filter((e) => !e.hidden).map((e) => e.dataset.category));
  check('FAQ tab filters questions', visible.length > 0 && visible.every((c) => c === 'shipping'), visible.join(','));

  check('no JS errors on homepage', errors.length === 0, errors.join(' | '));
  check('popup respects recent dismissal', !(await page.$eval('discount-popup', (el) => el.classList.contains('is-open'))));
  check('teaser shown for dismissed visitor', await page.$eval('.popup-teaser', (el) => !el.hidden));
  await page.close();

  // ---------- popup (fresh visitor) ----------
  page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(base + 'index.html', { waitUntil: 'load' });
  await page.addStyleTag({ content: 'html{scroll-behavior:auto !important}' });
  check('popup closed on arrival', !(await page.$eval('discount-popup', (el) => el.classList.contains('is-open'))));
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.6));
  await page.waitForTimeout(600);
  check('popup opens on scroll', await page.$eval('discount-popup', (el) => el.classList.contains('is-open')));
  await page.screenshot({ path: 'shots/popup-desktop.png' });
  await page.click('discount-popup .popup__close');
  await page.waitForTimeout(400);
  check('popup closes', !(await page.$eval('discount-popup', (el) => el.classList.contains('is-open'))));
  check('teaser shows after close', await page.$eval('.popup-teaser', (el) => !el.hidden));
  const dismissed = await page.evaluate(() => localStorage.getItem('alumnus-popup-dismissed'));
  check('dismissal remembered', !!dismissed);
  await page.close();

  // ---------- cart drawer ----------
  page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.addInitScript(() => localStorage.setItem('alumnus-popup-dismissed', String(Date.now())));
  await page.goto(base + 'index-cart.html', { waitUntil: 'load' });
  await page.click('[data-cart-toggle]');
  await page.waitForTimeout(500);
  check('cart drawer opens from header icon', await page.$eval('cart-drawer', (el) => el.classList.contains('is-open')));
  await page.screenshot({ path: 'shots/cart-drawer.png' });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  check('Escape closes cart drawer', !(await page.$eval('cart-drawer', (el) => el.classList.contains('is-open'))));
  await page.close();

  // ---------- mobile ----------
  page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await page.addInitScript(() => localStorage.setItem('alumnus-popup-dismissed', String(Date.now())));
  await page.goto(base + 'index.html', { waitUntil: 'load' });
  await page.waitForTimeout(600);
  await page.screenshot({ path: 'shots/mobile-hero.png' });
  await page.click('[data-menu-open]');
  await page.waitForTimeout(450);
  check('mobile menu opens', await page.$eval('[data-menu-drawer]', (el) => el.hasAttribute('open')));
  await page.screenshot({ path: 'shots/mobile-menu.png' });
  await page.click('.menu-drawer__panel [data-menu-close].icon-btn');
  await page.waitForTimeout(400);
  check('mobile menu closes', !(await page.$eval('[data-menu-drawer]', (el) => el.hasAttribute('open'))));
  await page.evaluate(() => document.querySelector('#buy').scrollIntoView());
  await page.waitForTimeout(400);
  await page.screenshot({ path: 'shots/mobile-buy.png' });
  await page.evaluate(() => window.scrollTo(0, document.querySelector('#plans').offsetTop));
  await page.waitForTimeout(500);
  check('mobile sticky bar visible', await page.$eval('sticky-buy', (el) => el.classList.contains('is-visible')));
  await page.screenshot({ path: 'shots/mobile-sticky.png' });
  const sw = await page.evaluate(() => document.documentElement.scrollWidth);
  check('no horizontal scroll on mobile', sw === 390, String(sw));
  await page.close();

  // ---------- other templates load without JS errors ----------
  for (const t of ['product', 'landing', 'cart', 'index-fresh', 'collection', 'search', 'page.contact', '404', 'password']) {
    page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    const errs = [];
    page.on('pageerror', (e) => errs.push(e.message));
    await page.goto(base + t + '.html', { waitUntil: 'load' });
    await page.waitForTimeout(300);
    check(`${t} renders without JS errors`, errs.length === 0, errs.join(' | '));
    await page.close();
  }
  console.log(results.join('\n'));
  await browser.close();
})();
