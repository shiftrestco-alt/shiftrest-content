/* Local preview renderer for the Alumnus Shopify theme.
   Emulates the Shopify Liquid objects, tags and filters the theme uses, renders a JSON
   template through layout/theme.liquid and writes static HTML for screenshots.
   Usage: node preview.js <themeDir> <outDir> <template> [--product] [--cart] [--popup] */
const fs = require('fs');
const path = require('path');
const { Liquid, Tag, Drop, TokenKind } = require('liquidjs');

const [, , themeDir, outDir, templateName = 'index', ...flags] = process.argv;
const withProduct = flags.includes('--product');
const withCart = flags.includes('--cart');
const outName = (flags.find((f) => f.startsWith('--out=')) || '').slice(6) || `${templateName}.html`;

const read = (p) => fs.readFileSync(path.join(themeDir, p), 'utf8');
const locale = JSON.parse(read('locales/en.default.json'));

/* ---------------- money & helpers ---------------- */
const money = (cents) => {
  const n = Number(cents) || 0;
  return '$' + (n / 100).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};
const handleize = (s) => String(s == null ? '' : s).toLowerCase().trim().replace(/['"]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
const kwargs = (args) => {
  const out = {};
  for (const a of args) if (Array.isArray(a)) out[a[0]] = a[1];
  return out;
};
const attrs = (obj) => Object.entries(obj)
  .filter(([, v]) => v !== undefined && v !== null && v !== false && v !== '')
  .map(([k, v]) => (v === true ? k : `${k}="${String(v).replace(/"/g, '&quot;')}"`)).join(' ');

/* ---------------- mock data ---------------- */
class OptionValue extends Drop {
  constructor(name) { super(); this.name = name; this.available = true; this.swatch = null; }
  valueOf() { return this.name; }
  toString() { return this.name; }
}
class FontDrop extends Drop {
  constructor(weight) { super(); this.family = 'Inter'; this.fallback_families = 'sans-serif'; this.weight = weight; this.style = 'normal'; this['system?'] = false; }
}

function settingsFromSchema() {
  const schema = JSON.parse(read('config/settings_schema.json'));
  const data = JSON.parse(read('config/settings_data.json')).current;
  const s = {};
  for (const group of schema) for (const st of group.settings || []) if (st.id) s[st.id] = st.default;
  Object.assign(s, data);
  s.type_heading_font = new FontDrop(400);
  s.type_body_font = new FontDrop(400);
  s.sale_end_date = '2026-11-30 23:59';
  return s;
}
const settings = settingsFromSchema();

const variants = [
  { id: 4401, title: 'Graphite', options: ['Graphite'], option1: 'Graphite', price: 13900, compare_at_price: 19900, available: true, inventory_management: 'shopify', inventory_quantity: 42, featured_media: null },
  { id: 4402, title: 'Silver', options: ['Silver'], option1: 'Silver', price: 13900, compare_at_price: 19900, available: true, inventory_management: 'shopify', inventory_quantity: 18, featured_media: null },
];
const product = {
  id: 9001, title: 'Alumnus AI Recorder', handle: 'alumnus-ai-recorder', url: '/products/alumnus-ai-recorder',
  price: 13900, price_min: 13900, compare_at_price: 19900, price_varies: false, available: true,
  has_only_default_variant: false, variants, selected_or_first_available_variant: variants[0],
  options_with_values: [{ name: 'Color', position: 1, selected_value: new OptionValue('Graphite'), values: [new OptionValue('Graphite'), new OptionValue('Silver')] }],
  media: [], featured_media: null, description: '<p>An ultra-thin AI voice recorder that snaps to your phone.</p>', metafields: {},
};
const upsell = {
  id: 9002, title: 'Alumnus sleeve', url: '/products/sleeve', available: true, featured_media: null,
  selected_or_first_available_variant: { id: 4501, price: 1900, compare_at_price: 2900 },
};
if (withProduct) { settings.cart_upsell_product = upsell; settings.main_product = product; }

const emptyCart = { item_count: 0, items: [], total_price: 0, original_total_price: 0, total_discount: 0, discount_applications: [], currency: { iso_code: 'USD' } };
const fullCart = (() => {
  const bundle = { title: 'Duo bundle 10% off', type: 'automatic', total_allocated_amount: 2780 };
  const item = {
    id: 4401, product_id: 9001, title: 'Alumnus AI Recorder - Graphite', url: '/products/alumnus-ai-recorder?variant=4401',
    quantity: 2, image: null, product: { title: 'Alumnus AI Recorder', has_only_default_variant: false }, variant: { title: 'Graphite' },
    original_line_price: 27800, final_line_price: 25020, line_level_discount_allocations: [{ amount: 2780, discount_application: bundle }],
  };
  return { item_count: 2, items: [item], total_price: 25020, original_total_price: 27800, total_discount: 2780, discount_applications: [bundle], currency: { iso_code: 'USD' } };
})();

const globals = {
  settings,
  shop: {
    name: 'Alumnus', url: 'https://alumnus.example', description: 'Your AI note-taker.', money_format: '${{amount}}', customer_accounts_enabled: true,
    enabled_payment_types: ['visa', 'master', 'american_express', 'paypal', 'apple_pay', 'google_pay', 'shopify_pay'],
    policies: [{ title: 'Privacy policy', url: '/policies/privacy-policy' }, { title: 'Refund policy', url: '/policies/refund-policy' }],
  },
  routes: { root_url: '/', cart_url: '/cart', cart_add_url: '/cart/add', cart_change_url: '/cart/change', cart_update_url: '/cart/update', search_url: '/search' },
  request: { design_mode: flags.includes('--editor'), page_type: templateName.split('.')[0], locale: { iso_code: 'en' }, origin: 'https://alumnus.example', path: '/' },
  template: { name: templateName.split('.')[0], suffix: templateName.split('.')[1] || null },
  cart: withCart ? fullCart : emptyCart,
  canonical_url: 'https://alumnus.example/', page_title: 'Alumnus · Your AI note-taker', page_description: 'One press records your lecture, meeting or call.',
  content_for_header: '', current_page: 1, additional_checkout_buttons: true,
  content_for_additional_checkout_buttons: '<div style="display:grid;gap:8px"><button type="button" style="height:48px;border-radius:999px;border:0;background:#5A31F4;color:#fff;font-weight:700">shop Pay</button></div>',
  product: templateName === 'product' ? product : undefined,
  collections: [], linklists: {},
};

/* ---------------- engine ---------------- */
const engine = new Liquid({
  root: [path.join(themeDir, 'sections'), path.join(themeDir, 'snippets'), path.join(themeDir, 'layout'), path.join(themeDir, 'templates')],
  partials: [path.join(themeDir, 'snippets')],
  extname: '.liquid',
  dynamicPartials: true,
  strictFilters: true,
  strictVariables: false,
  jsTruthy: false,
  greedy: false,
});

function translate(key, vars = {}) {
  let node = key.split('.').reduce((o, k) => (o ? o[k] : undefined), locale);
  if (node === undefined) throw new Error(`Missing translation: ${key}`);
  if (typeof node === 'object') {
    const count = Number(vars.count);
    node = (count === 0 && node.zero) || (count === 1 && node.one) || node.other;
  }
  return node.replace(/\{\{\s*(\w+)\s*\}\}/g, (_, v) => (vars[v] === undefined ? '' : vars[v]));
}

const f = engine.registerFilter.bind(engine);
f('t', (key, ...args) => translate(key, kwargs(args)));
f('asset_url', (name) => `/assets/${name}`);
f('shopify_asset_url', (name) => `https://cdn.shopify.com/s/shopify/${name}`);
f('stylesheet_tag', (url) => `<link href="${url}" rel="stylesheet" type="text/css" media="all" />`);
f('script_tag', (url) => `<script src="${url}" type="text/javascript"></script>`);
f('image_url', (img, ...args) => (img && img.src ? img.src : ''));
f('image_tag', (src, ...args) => `<img src="${src}" ${attrs(kwargs(args))}>`);
f('video_tag', (video, ...args) => {
  const o = kwargs(args);
  return `<video ${attrs({ autoplay: o.autoplay, loop: o.loop, muted: o.muted, playsinline: o.playsinline, controls: o.controls, preload: o.preload })}><source src="${video.src}"></video>`;
});
f('external_video_tag', () => '<iframe></iframe>');
f('media_tag', () => '');
f('money', money);
f('money_with_currency', (c) => `${money(c)} USD`);
f('money_without_trailing_zeros', (c) => money(c).replace(/\.00$/, ''));
f('money_without_currency', (c) => money(c).replace('$', ''));
f('json', (v) => JSON.stringify(v === undefined ? null : v));
f('handle', handleize);
f('handleize', handleize);
f('font_face', () => '');
f('font_url', () => '');
f('font_modify', (font, prop, value) => (prop === 'weight' ? new FontDrop(Number(value) || 400) : font));
f('preload_tag', () => '');
f('payment_terms', () => '<span class="shopify-installments">Pay in 4 interest-free installments with <b>Shop Pay</b>. <u>Learn more</u></span>');
f('payment_button', () => '<div class="shopify-payment-button"><button type="button" class="shopify-payment-button__button" style="width:100%;background:#5A31F4;color:#fff;border:0;font-weight:700;font-size:1.05rem">Buy with <i>shop</i>Pay</button><button type="button" class="shopify-payment-button__more-options" style="width:100%;margin-top:8px;background:none;border:0;text-decoration:underline">More payment options</button></div>');
f('payment_type_svg_tag', (type) => `<svg viewBox="0 0 38 24" width="38" height="24" role="img" aria-label="${type}"><rect width="38" height="24" rx="4" fill="#fff" stroke="#ddd"/><text x="19" y="15" font-size="6" text-anchor="middle" fill="#333">${String(type).slice(0, 6)}</text></svg>`);
f('structured_data', (p) => JSON.stringify({ '@context': 'http://schema.org/', '@type': 'Product', name: p && p.title }));
f('login_button', () => '<button type="button" class="btn btn--sm" style="background:#5A31F4;color:#fff">Follow on Shop</button>');
f('default_errors', () => '');
f('time_tag', (d) => `<time>${d}</time>`);
f('format_code', (c) => c);
f('url_encode', (s) => encodeURIComponent(s));
f('divided_by', (a, b) => (Number.isInteger(Number(a)) && Number.isInteger(Number(b)) ? Math.floor(Number(a) / Number(b)) : Number(a) / Number(b)));

/* {% schema %}: drop the JSON */
engine.registerTag('schema', class extends Tag {
  constructor(token, remainTokens, liquid) {
    super(token, remainTokens, liquid);
    while (remainTokens.length) {
      const t = remainTokens.shift();
      if (t.kind === TokenKind.Tag && t.name === 'endschema') return;
    }
    throw new Error('schema not closed');
  }
  * render() {}
});

function blockTag(endName, wrap) {
  return class extends Tag {
    constructor(token, remainTokens, liquid, parser) {
      super(token, remainTokens, liquid);
      this.args = token.args;
      this.templates = [];
      const stream = parser.parseStream(remainTokens)
        .on(`tag:${endName}`, () => stream.stop())
        .on('template', (tpl) => this.templates.push(tpl))
        .on('end', () => { throw new Error(`${endName} not closed`); });
      stream.start();
    }
    * render(ctx, emitter) {
      yield* wrap.call(this, ctx, emitter);
    }
  };
}

engine.registerTag('style', blockTag('endstyle', function* (ctx, emitter) {
  const html = yield this.liquid.renderer.renderTemplates(this.templates, ctx);
  emitter.write(`<style data-shopify>${html}</style>`);
}));

engine.registerTag('paginate', blockTag('endpaginate', function* (ctx, emitter) {
  ctx.push({ paginate: { pages: 1, current_page: 1, parts: [] } });
  const html = yield this.liquid.renderer.renderTemplates(this.templates, ctx);
  ctx.pop();
  emitter.write(html);
}));

function splitArgs(str) {
  const parts = []; let cur = ''; let q = null;
  for (const ch of str) {
    if (q) { cur += ch; if (ch === q) q = null; continue; }
    if (ch === '"' || ch === "'") { q = ch; cur += ch; continue; }
    if (ch === ',') { parts.push(cur.trim()); cur = ''; continue; }
    cur += ch;
  }
  if (cur.trim()) parts.push(cur.trim());
  return parts;
}

engine.registerTag('form', blockTag('endform', function* (ctx, emitter) {
  const parts = splitArgs(this.args);
  const type = this.liquid.evalValueSync(parts[0], ctx);
  const html = {};
  for (const p of parts.slice(1)) {
    const m = p.match(/^([\w-]+)\s*:\s*(.+)$/);
    if (m) html[m[1]] = this.liquid.evalValueSync(m[2], ctx);
  }
  const action = { product: '/cart/add', cart: '/cart', customer: '/contact#' + (html.id || ''), contact: '/contact', storefront_password: '/password' }[type] || '/';
  ctx.push({ form: { 'posted_successfully?': false, errors: null, email: '', name: '', body: '', order: '' } });
  const inner = yield this.liquid.renderer.renderTemplates(this.templates, ctx);
  ctx.pop();
  emitter.write(`<form method="post" action="${action}" accept-charset="UTF-8" ${attrs(html)}><input type="hidden" name="form_type" value="${type}" />${inner}</form>`);
}));

engine.registerTag('layout', class extends Tag { * render() {} });

/* ---------------- sections ---------------- */
function schemaOf(type) {
  const text = read(`sections/${type}.liquid`);
  return JSON.parse(text.match(/{%-?\s*schema\s*-?%}([\s\S]*?){%-?\s*endschema\s*-?%}/)[1]);
}
function withDefaults(defs, values) {
  const out = {};
  for (const st of defs || []) if (st.id) out[st.id] = st.default;
  Object.assign(out, values || {});
  for (const st of defs || []) {
    if (!st.id) continue;
    if (['image_picker', 'video', 'link_list', 'video_url'].includes(st.type) && !out[st.id]) out[st.id] = null;
  }
  return out;
}
let sectionCounter = 0;
function renderSection(type, key, data, wrapperId, extraClass = '') {
  const schema = schemaOf(type);
  const blockDefs = Object.fromEntries((schema.blocks || []).map((b) => [b.type, b]));
  const order = data.block_order || Object.keys(data.blocks || {});
  const blocks = order.map((bk) => {
    const b = data.blocks[bk];
    return { id: bk, type: b.type, settings: withDefaults((blockDefs[b.type] || {}).settings, b.settings), shopify_attributes: '' };
  });
  const section = { id: wrapperId.replace('shopify-section-', ''), settings: withDefaults(schema.settings, data.settings), blocks };
  const tpl = engine.parse(read(`sections/${type}.liquid`), `sections/${type}.liquid`);
  const html = engine.renderSync(tpl, { section }, { globals });
  return `<div id="${wrapperId}" class="shopify-section ${extraClass} ${schema.class || ''}">${html}</div>`;
}

engine.registerTag('section', class extends Tag {
  constructor(token, remainTokens, liquid) { super(token, remainTokens, liquid); this.name = token.args.trim().replace(/['"]/g, ''); }
  * render(ctx, emitter) { emitter.write(renderSection(this.name, this.name, { settings: {}, blocks: {} }, `shopify-section-${this.name}`)); }
});
engine.registerTag('sections', class extends Tag {
  constructor(token, remainTokens, liquid) { super(token, remainTokens, liquid); this.name = token.args.trim().replace(/['"]/g, ''); }
  * render(ctx, emitter) {
    const group = JSON.parse(read(`sections/${this.name}.json`));
    for (const key of group.order) {
      emitter.write(renderSection(group.sections[key].type, key, group.sections[key], `shopify-section-sections--1__${key}`, `shopify-section-group-${this.name}`));
    }
  }
});

/* ---------------- render ---------------- */
const tplJson = JSON.parse(read(`templates/${templateName}.json`));
const body = tplJson.order.map((key) => renderSection(tplJson.sections[key].type, key, tplJson.sections[key], `shopify-section-template--1__${key}`)).join('\n');
const layoutName = tplJson.layout || 'theme';
const layout = engine.parse(read(`layout/${layoutName}.liquid`), `layout/${layoutName}.liquid`);
let html = engine.renderSync(layout, { content_for_layout: body }, { globals });
html = html.replace('</head>', '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"></head>');
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, outName), html);
console.log(`rendered ${templateName} -> ${path.join(outDir, outName)} (${html.length} bytes)`);
