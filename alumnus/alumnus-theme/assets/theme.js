/* ==========================================================================
   Alumnus theme · theme.js
   Small custom elements, no dependencies. Each one sets itself up when it
   lands on the page, so they keep working after the theme editor re-renders a section.
   ========================================================================== */
(() => {
  const theme = window.theme || {};
  const routes = theme.routes || {};
  const strings = theme.strings || {};
  const root = routes.root || '/';

  /* ---------- helpers ---------- */
  const qs = (sel, ctx = document) => ctx.querySelector(sel);
  const qsa = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  function formatMoney(cents, format = theme.moneyFormat || '${{amount}}') {
    if (typeof cents === 'string') cents = cents.replace('.', '');
    cents = Number(cents) || 0;
    const placeholder = /\{\{\s*(\w+)\s*\}\}/;
    const fmt = (n, precision, thousands = ',', decimal = '.') => {
      const fixed = (n / 100).toFixed(precision);
      const [whole, frac] = fixed.split('.');
      const withSep = whole.replace(/(\d)(?=(\d{3})+(?!\d))/g, `$1${thousands}`);
      return frac ? withSep + decimal + frac : withSep;
    };
    const match = format.match(placeholder);
    let value = '';
    switch (match ? match[1] : 'amount') {
      case 'amount': value = fmt(cents, 2); break;
      case 'amount_no_decimals': value = fmt(cents, 0); break;
      case 'amount_with_comma_separator': value = fmt(cents, 2, '.', ','); break;
      case 'amount_no_decimals_with_comma_separator': value = fmt(cents, 0, '.', ','); break;
      case 'amount_with_apostrophe_separator': value = fmt(cents, 2, "'", '.'); break;
      case 'amount_with_space_separator': value = fmt(cents, 2, ' ', ','); break;
      default: value = fmt(cents, 2);
    }
    return format.replace(placeholder, value);
  }

  const storage = {
    get(key) { try { return window.localStorage.getItem(key); } catch (e) { return null; } },
    set(key, value) { try { window.localStorage.setItem(key, value); } catch (e) { /* storage blocked */ } },
  };

  function trapFocus(container, event) {
    if (event.key !== 'Tab') return;
    const focusable = qsa('a[href], button:not([disabled]), input:not([type="hidden"]), select, textarea, [tabindex]:not([tabindex="-1"])', container)
      .filter((el) => el.offsetParent !== null);
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }

  function lockScroll(lock) {
    document.documentElement.style.overflow = lock ? 'hidden' : '';
  }

  /* ---------- reveal on scroll ---------- */
  const revealObserver = 'IntersectionObserver' in window
    ? new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            revealObserver.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 })
    : null;

  function initReveal(scope = document) {
    qsa('.reveal:not(.is-in)', scope).forEach((el) => {
      if (revealObserver) revealObserver.observe(el);
      else el.classList.add('is-in');
    });
  }

  /* Pause autoplay videos that are off screen to save battery and data. */
  const videoObserver = 'IntersectionObserver' in window
    ? new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          const video = entry.target;
          if (entry.isIntersecting) {
            if (video.preload === 'none') video.preload = 'metadata';
            const playing = video.play();
            if (playing && playing.catch) playing.catch(() => {});
          } else if (!video.paused) {
            video.pause();
          }
        });
      }, { threshold: 0.2 })
    : null;

  function initAutoplayVideos(scope = document) {
    qsa('video[autoplay]', scope).forEach((video) => {
      video.muted = true;
      video.playsInline = true;
      if (videoObserver) videoObserver.observe(video);
    });
  }

  /* ---------- header ---------- */
  class HeaderBar extends HTMLElement {
    connectedCallback() {
      this.header = qs('.header', this);
      this.drawer = qs('[data-menu-drawer]', this);
      this.openBtn = qs('[data-menu-open]', this);
      this.onScroll = () => this.header && this.header.classList.toggle('is-scrolled', window.scrollY > 8);
      window.addEventListener('scroll', this.onScroll, { passive: true });
      this.onScroll();
      if (this.openBtn) this.openBtn.addEventListener('click', () => this.open());
      qsa('[data-menu-close]', this).forEach((el) => el.addEventListener('click', () => this.close()));
      this.onKey = (e) => {
        if (!this.drawer || !this.drawer.hasAttribute('open')) return;
        if (e.key === 'Escape') this.close();
        trapFocus(qs('.menu-drawer__panel', this.drawer), e);
      };
      document.addEventListener('keydown', this.onKey);
      const height = this.offsetHeight;
      if (height) document.documentElement.style.setProperty('--header-height', `${qs('.header', this).offsetHeight}px`);
    }
    disconnectedCallback() {
      window.removeEventListener('scroll', this.onScroll);
      document.removeEventListener('keydown', this.onKey);
    }
    open() {
      this.drawer.setAttribute('open', '');
      this.openBtn.setAttribute('aria-expanded', 'true');
      lockScroll(true);
      const panel = qs('.menu-drawer__panel', this.drawer);
      if (panel) panel.focus();
    }
    close() {
      if (!this.drawer.hasAttribute('open')) return;
      this.drawer.removeAttribute('open');
      this.openBtn.setAttribute('aria-expanded', 'false');
      lockScroll(false);
      this.openBtn.focus();
    }
  }
  customElements.define('header-bar', HeaderBar);

  /* ---------- announcement rotator ---------- */
  class AnnouncementRotator extends HTMLElement {
    connectedCallback() {
      this.messages = qsa('.announcement__message', this);
      if (this.messages.length < 2) return;
      const seconds = Number(this.dataset.interval) || 5;
      this.index = 0;
      this.timer = setInterval(() => this.next(), seconds * 1000);
    }
    disconnectedCallback() { clearInterval(this.timer); }
    next() {
      this.messages[this.index].classList.remove('is-active');
      this.index = (this.index + 1) % this.messages.length;
      this.messages[this.index].classList.add('is-active');
    }
  }
  customElements.define('announcement-rotator', AnnouncementRotator);

  /* ---------- countdown (real end date only, hides when over) ---------- */
  class CountDown extends HTMLElement {
    connectedCallback() {
      const raw = (this.dataset.end || '').trim();
      // Accept "2026-11-30", "2026-11-30 23:59" or full ISO strings.
      const normalized = /^\d{4}-\d{2}-\d{2}$/.test(raw) ? `${raw}T23:59:59` : raw.replace(' ', 'T');
      this.end = new Date(normalized).getTime();
      this.output = qs('.countdown__value', this);
      if (!this.end || Number.isNaN(this.end)) return;
      this.tick();
      this.timer = setInterval(() => this.tick(), 1000);
    }
    disconnectedCallback() { clearInterval(this.timer); }
    tick() {
      const diff = this.end - Date.now();
      if (diff <= 0) {
        clearInterval(this.timer);
        this.hidden = true;
        const wrap = this.closest('.buy__countdown, .announcement__timer');
        if (wrap) wrap.hidden = true;
        return;
      }
      const d = Math.floor(diff / 86400000);
      const h = Math.floor((diff % 86400000) / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      const s = Math.floor((diff % 60000) / 1000);
      const pad = (n) => String(n).padStart(2, '0');
      if (this.dataset.style === 'chips') {
        const unit = (value, label) => `<span class="countdown__unit"><b>${pad(value)}</b><small>${label}</small></span>`;
        this.output.innerHTML = `${unit(d, strings.days || 'd')}${unit(h, strings.hours || 'h')}${unit(m, strings.minutes || 'm')}${unit(s, strings.seconds || 's')}`;
        this.output.style.display = 'inline-flex';
        this.output.style.gap = '6px';
      } else {
        const unit = (value, label) => `<span class="countdown__unit">${pad(value)}${label}</span>`;
        this.output.innerHTML = `${d > 0 ? unit(d, strings.days || 'd') + ' ' : ''}${unit(h, strings.hours || 'h')} ${unit(m, strings.minutes || 'm')} ${unit(s, strings.seconds || 's')}`;
      }
      this.hidden = false;
    }
  }
  customElements.define('count-down', CountDown);

  /* ---------- carousel ---------- */
  class CarouselSlider extends HTMLElement {
    connectedCallback() {
      this.track = qs('[data-track]', this);
      this.prev = qs('[data-prev]', this);
      this.next = qs('[data-next]', this);
      if (!this.track) return;
      const step = () => {
        const slide = this.track.firstElementChild;
        if (!slide) return this.track.clientWidth;
        const gap = parseFloat(getComputedStyle(this.track).columnGap) || 0;
        return slide.getBoundingClientRect().width + gap;
      };
      if (this.prev) this.prev.addEventListener('click', () => this.track.scrollBy({ left: -step(), behavior: 'smooth' }));
      if (this.next) this.next.addEventListener('click', () => this.track.scrollBy({ left: step(), behavior: 'smooth' }));
      this.update = () => {
        const max = this.track.scrollWidth - this.track.clientWidth - 2;
        if (this.prev) this.prev.disabled = this.track.scrollLeft <= 2;
        if (this.next) this.next.disabled = this.track.scrollLeft >= max;
      };
      this.track.addEventListener('scroll', this.update, { passive: true });
      window.addEventListener('resize', this.update);
      this.update();
    }
    disconnectedCallback() { window.removeEventListener('resize', this.update); }
    scrollToItem(el) {
      if (!el || !this.track) return;
      this.track.scrollTo({ left: el.offsetLeft - this.track.offsetLeft, behavior: 'smooth' });
    }
  }
  customElements.define('carousel-slider', CarouselSlider);

  /* ---------- video player (intro film) ---------- */
  class VideoPlayer extends HTMLElement {
    connectedCallback() {
      this.button = qs('.video-player__play', this);
      if (this.button) this.button.addEventListener('click', () => this.play());
    }
    play() {
      const video = qs('video', this);
      if (video) {
        this.classList.add('is-playing');
        video.controls = true;
        const playing = video.play();
        if (playing && playing.catch) playing.catch(() => {});
        return;
      }
      const type = this.dataset.type;
      const id = this.dataset.videoId;
      if (!type || !id) return;
      const src = type === 'youtube'
        ? `https://www.youtube-nocookie.com/embed/${encodeURIComponent(id)}?autoplay=1&rel=0&playsinline=1`
        : `https://player.vimeo.com/video/${encodeURIComponent(id)}?autoplay=1`;
      const frame = document.createElement('iframe');
      frame.src = src;
      frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      frame.title = document.title;
      const media = qs('.media', this);
      media.innerHTML = '';
      media.appendChild(frame);
      this.classList.add('is-playing');
    }
  }
  customElements.define('video-player', VideoPlayer);

  document.addEventListener('click', (event) => {
    const trigger = event.target.closest('[data-play-video]');
    if (!trigger) return;
    const player = document.getElementById(trigger.dataset.playVideo);
    if (player && player.play) {
      player.scrollIntoView({ behavior: 'smooth', block: 'center' });
      player.play();
    }
  });

  /* Sound toggle on video carousel cards. */
  document.addEventListener('click', (event) => {
    const button = event.target.closest('[data-toggle-sound]');
    if (!button) return;
    const card = button.closest('.media-wrap') || button.parentElement;
    const video = card && qs('video', card);
    if (!video) return;
    qsa('video').forEach((other) => { if (other !== video) other.muted = true; });
    qsa('[data-toggle-sound]').forEach((b) => {
      if (b === button) return;
      b.setAttribute('aria-pressed', 'false');
      qs('[data-icon-on]', b).hidden = true;
      qs('[data-icon-off]', b).hidden = false;
    });
    video.muted = !video.muted;
    if (!video.muted) { video.currentTime = 0; video.play().catch(() => {}); }
    button.setAttribute('aria-pressed', String(!video.muted));
    qs('[data-icon-on]', button).hidden = video.muted;
    qs('[data-icon-off]', button).hidden = !video.muted;
  });

  /* ---------- FAQ tabs ---------- */
  class FaqTabs extends HTMLElement {
    connectedCallback() {
      this.tabs = qsa('[role="tab"]', this);
      this.tabs.forEach((tab) => tab.addEventListener('click', () => this.select(tab.dataset.tab)));
    }
    select(handle) {
      this.tabs.forEach((tab) => tab.setAttribute('aria-selected', String(tab.dataset.tab === handle)));
      qsa('details[data-category]', this).forEach((item) => {
        item.hidden = this.tabs.length > 0 && item.dataset.category !== handle;
      });
    }
  }
  customElements.define('faq-tabs', FaqTabs);

  /* ---------- cart ---------- */
  const cart = {
    drawer() { return document.querySelector('cart-drawer'); },
    sectionIds() {
      const ids = ['cart-drawer'];
      const page = document.querySelector('cart-page');
      if (page && page.dataset.section) ids.push(page.dataset.section);
      return ids;
    },
    async request(url, body) {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ ...body, sections: this.sectionIds(), sections_url: window.location.pathname }),
      });
      const data = await response.json();
      if (!response.ok || data.status) throw data;
      return data;
    },
    render(sections) {
      if (!sections) return;
      const drawer = this.drawer();
      if (sections['cart-drawer'] && drawer) {
        const html = new DOMParser().parseFromString(sections['cart-drawer'], 'text/html');
        const fresh = html.querySelector('cart-drawer');
        if (fresh) {
          qs('.drawer__panel', drawer).innerHTML = qs('.drawer__panel', fresh).innerHTML;
          drawer.dataset.itemCount = fresh.dataset.itemCount;
          this.updateCount(Number(fresh.dataset.itemCount));
        }
      }
      const page = document.querySelector('cart-page');
      if (page && sections[page.dataset.section]) {
        const html = new DOMParser().parseFromString(sections[page.dataset.section], 'text/html');
        const fresh = html.querySelector('cart-page');
        if (fresh) page.innerHTML = fresh.innerHTML;
      }
    },
    updateCount(count) {
      qsa('[data-cart-count]').forEach((el) => {
        el.dataset.count = count;
        el.textContent = count > 0 ? count : '';
      });
    },
    async add(items) {
      const data = await this.request(routes.cartAdd + '.js', { items });
      this.render(data.sections);
      return data;
    },
    async change(line, quantity) {
      const data = await this.request(routes.cartChange + '.js', { line, quantity });
      this.render(data.sections);
      return data;
    },
    async discount(codes) {
      const data = await this.request(routes.cartUpdate + '.js', { discount: codes });
      this.render(data.sections);
      return data;
    },
  };
  window.AlumnusCart = cart;

  class CartDrawer extends HTMLElement {
    connectedCallback() {
      this.addEventListener('click', (e) => this.onClick(e));
      this.addEventListener('submit', (e) => this.onSubmit(e));
      this.addEventListener('change', (e) => this.onChange(e));
      this.onKey = (e) => {
        if (!this.classList.contains('is-open')) return;
        if (e.key === 'Escape') this.close();
        trapFocus(qs('.drawer__panel', this), e);
      };
      document.addEventListener('keydown', this.onKey);
    }
    disconnectedCallback() { document.removeEventListener('keydown', this.onKey); }
    open() {
      this.previousFocus = document.activeElement;
      this.classList.add('is-open');
      lockScroll(true);
      const panel = qs('.drawer__panel', this);
      setTimeout(() => panel && panel.focus(), 50);
    }
    close() {
      this.classList.remove('is-open');
      lockScroll(false);
      if (this.previousFocus && this.previousFocus.focus) this.previousFocus.focus();
    }
    onClick(e) {
      if (e.target.closest('[data-cart-close]')) { e.preventDefault(); this.close(); return; }
      handleCartActions(e, this);
    }
    onSubmit(e) { handleDiscountSubmit(e, this); }
    onChange(e) { handleQtyInput(e); }
  }
  customElements.define('cart-drawer', CartDrawer);

  class CartPage extends HTMLElement {
    connectedCallback() {
      this.addEventListener('click', (e) => handleCartActions(e, this));
      this.addEventListener('submit', (e) => handleDiscountSubmit(e, this));
      this.addEventListener('change', (e) => handleQtyInput(e));
    }
  }
  customElements.define('cart-page', CartPage);

  function setBusy(el, busy) {
    if (!el) return;
    el.classList.toggle('is-loading', busy);
    el.toggleAttribute('aria-busy', busy);
  }

  async function handleCartActions(e, scope) {
    const qtyBtn = e.target.closest('[data-qty-change]');
    if (qtyBtn) {
      e.preventDefault();
      setBusy(qtyBtn.closest('.line'), true);
      try { await cart.change(Number(qtyBtn.dataset.lineIndex), Number(qtyBtn.dataset.qtyChange)); }
      catch (err) { window.alert((err && err.description) || strings.cartError); }
      return;
    }
    const quick = e.target.closest('[data-quick-add]');
    if (quick) {
      e.preventDefault();
      setBusy(quick, true);
      try { await cart.add([{ id: Number(quick.dataset.quickAdd), quantity: 1 }]); }
      catch (err) { setBusy(quick, false); window.alert((err && err.description) || strings.cartError); }
      return;
    }
    const remove = e.target.closest('[data-remove-discount]');
    if (remove) {
      e.preventDefault();
      const code = remove.dataset.removeDiscount;
      const remaining = qsa('[data-applied-code]', scope)
        .map((el) => el.dataset.appliedCode)
        .filter((c) => c !== code);
      try { await cart.discount(remaining.join(',')); } catch (err) { /* keep current state */ }
    }
  }

  async function handleDiscountSubmit(e, scope) {
    const form = e.target.closest('[data-discount-form]');
    if (!form) return;
    e.preventDefault();
    const input = qs('input[name="discount"]', form);
    const code = (input.value || '').trim();
    if (!code) return;
    const existing = qsa('[data-applied-code]', scope).map((el) => el.dataset.appliedCode);
    const button = qs('button', form);
    setBusy(button, true);
    try {
      const data = await cart.discount([...existing, code].join(','));
      const applied = (data.discount_codes || []).find((d) => d.code.toLowerCase() === code.toLowerCase());
      if (applied && !applied.applicable) {
        const error = qs('[data-discount-error]', scope);
        if (error) error.hidden = false;
      }
    } catch (err) {
      const error = qs('[data-discount-error]', scope);
      if (error) error.hidden = false;
      setBusy(button, false);
    }
  }

  let qtyTimer;
  function handleQtyInput(e) {
    const input = e.target.closest('[data-qty-input-line]');
    if (!input) return;
    clearTimeout(qtyTimer);
    qtyTimer = setTimeout(() => {
      cart.change(Number(input.dataset.qtyInputLine), Math.max(0, Number(input.value) || 0)).catch(() => {});
    }, 350);
  }

  /* Header cart icon opens the drawer. */
  document.addEventListener('click', (e) => {
    const toggle = e.target.closest('[data-cart-toggle]');
    if (!toggle || theme.cartType !== 'drawer') return;
    const drawer = cart.drawer();
    if (!drawer) return;
    e.preventDefault();
    drawer.open();
  });

  /* ---------- buy box: variants, bundle tiers, add to cart ---------- */
  class BuyBox extends HTMLElement {
    connectedCallback() {
      const json = qs('[data-product-json]', this);
      this.product = json ? JSON.parse(json.textContent) : null;
      this.form = qs('[data-product-form]', this) || qs('form[action*="/cart/add"]', this);
      this.variantInput = qs('[data-variant-input]', this);
      this.qtyInput = qs('[data-qty-input]', this);
      this.slides = qs('[data-gallery-slides]', this);

      qsa('input[data-option-index]', this).forEach((input) => input.addEventListener('change', () => this.onOptionChange()));
      qsa('input[data-tier]', this).forEach((input) => input.addEventListener('change', () => this.updatePrices()));
      if (this.form) this.form.addEventListener('submit', (e) => this.onSubmit(e));

      qsa('[data-thumb]', this).forEach((thumb) => thumb.addEventListener('click', () => this.goTo(Number(thumb.dataset.thumb))));
      if (this.slides) {
        this.slides.addEventListener('scroll', () => {
          window.clearTimeout(this.scrollTimer);
          this.scrollTimer = window.setTimeout(() => this.syncThumbs(), 80);
        }, { passive: true });
      }
      this.currentVariant = this.findVariant() || (this.product && this.product.variants[0]);
      this.updatePrices();
    }

    selectedOptions() {
      const groups = {};
      qsa('input[data-option-index]:checked', this).forEach((input) => { groups[input.dataset.optionIndex] = input.value; });
      return groups;
    }

    findVariant() {
      if (!this.product) return null;
      const options = this.selectedOptions();
      return this.product.variants.find((variant) =>
        Object.keys(options).every((index) => variant.options[Number(index)] === options[index])
      );
    }

    onOptionChange() {
      const variant = this.findVariant();
      qsa('[data-option-selected]', this).forEach((label) => {
        const options = this.selectedOptions();
        label.textContent = options[label.dataset.optionSelected] || '';
      });
      if (!variant) {
        this.setButton(false, strings.unavailable);
        return;
      }
      this.currentVariant = variant;
      if (this.variantInput) {
        this.variantInput.value = variant.id;
        this.variantInput.dispatchEvent(new Event('change', { bubbles: true }));
      }
      if (variant.featured_media && this.product.media) {
        const match = this.product.media.find((m) => m.id === variant.featured_media.id);
        if (match) this.goTo(match.index);
      }
      if (this.hasAttribute('data-update-url')) {
        const url = new URL(window.location.href);
        url.searchParams.set('variant', variant.id);
        window.history.replaceState({}, '', url.toString());
      }
      this.updatePrices();
    }

    selectedTier() {
      const tier = qs('input[data-tier]:checked', this);
      return tier ? { qty: Number(tier.dataset.qty) || 1, pct: Number(tier.dataset.pct) || 0 } : { qty: 1, pct: 0 };
    }

    updatePrices() {
      const variant = this.currentVariant;
      if (!variant) return;
      const price = variant.price;
      const compare = variant.compare_at_price && variant.compare_at_price > price ? variant.compare_at_price : null;

      const priceEl = qs('[data-price]', this);
      const compareEl = qs('[data-compare]', this);
      const saveEl = qs('[data-save-badge]', this);
      if (priceEl) priceEl.textContent = formatMoney(price);
      if (compareEl) { compareEl.hidden = !compare; if (compare) compareEl.textContent = formatMoney(compare); }
      if (saveEl) {
        const pct = compare ? Math.floor(((compare - price) * 100) / compare) : 0;
        saveEl.hidden = pct <= 0;
        saveEl.textContent = saveEl.textContent.replace(/\d+%/, `${pct}%`);
      }

      qsa('.tier', this).forEach((tierEl) => {
        const input = qs('input[data-tier]', tierEl);
        const qty = Number(input.dataset.qty) || 1;
        const pct = Number(input.dataset.pct) || 0;
        const total = Math.floor((price * qty * (100 - pct)) / 100);
        const full = (compare || price) * qty;
        const totalEl = qs('[data-tier-total]', tierEl);
        const fullEl = qs('[data-tier-full]', tierEl);
        const eachEl = qs('[data-tier-each]', tierEl);
        if (totalEl) totalEl.textContent = formatMoney(total);
        if (fullEl) { fullEl.hidden = full <= total; fullEl.textContent = formatMoney(full); }
        if (eachEl) eachEl.textContent = formatMoney(Math.floor(total / qty));
      });

      const tier = this.selectedTier();
      if (this.qtyInput) this.qtyInput.value = tier.qty;
      const buttonPrice = qs('[data-button-price]', this);
      if (buttonPrice) buttonPrice.textContent = formatMoney(Math.floor((price * tier.qty * (100 - tier.pct)) / 100));

      const sticky = document.querySelector(`sticky-buy[data-target="${this.closest('section') ? this.closest('section').id : ''}"] [data-sticky-price]`);
      if (sticky) sticky.textContent = formatMoney(price);

      this.setButton(variant.available, variant.available ? null : strings.soldOut);
    }

    setButton(available, label) {
      const button = qs('[data-add-button]', this);
      if (!button) return;
      button.disabled = !available;
      const labelEl = qs('[data-add-label]', button);
      if (!labelEl) return;
      if (!available) {
        if (!this.originalLabel) this.originalLabel = labelEl.innerHTML;
        labelEl.textContent = label || strings.soldOut;
      } else if (this.originalLabel) {
        labelEl.innerHTML = this.originalLabel;
        this.originalLabel = null;
        this.updatePrices();
      }
    }

    goTo(index) {
      if (!this.slides) return;
      const slide = this.slides.children[index];
      if (slide) this.slides.scrollTo({ left: slide.offsetLeft - this.slides.offsetLeft, behavior: 'smooth' });
      this.setActiveThumb(index);
    }

    syncThumbs() {
      if (!this.slides) return;
      const index = Math.round(this.slides.scrollLeft / this.slides.clientWidth);
      this.setActiveThumb(index);
    }

    setActiveThumb(index) {
      qsa('[data-thumb]', this).forEach((thumb) => thumb.setAttribute('aria-current', String(Number(thumb.dataset.thumb) === index)));
      qsa('[data-gallery-dots] span', this).forEach((dot, i) => dot.classList.toggle('is-active', i === index));
    }

    async onSubmit(e) {
      if (theme.cartType !== 'drawer' || !cart.drawer()) return; // fall back to normal form post
      e.preventDefault();
      const button = qs('[data-add-button]', this);
      const error = qs('[data-form-error]', this);
      if (error) error.hidden = true;
      setBusy(button, true);
      try {
        const id = Number(this.variantInput.value);
        const quantity = Number(this.qtyInput ? this.qtyInput.value : 1) || 1;
        await cart.add([{ id, quantity }]);
        cart.drawer().open();
      } catch (err) {
        if (error) {
          error.textContent = (err && (err.description || err.message)) || strings.cartError;
          error.hidden = false;
        }
      } finally {
        setBusy(button, false);
      }
    }
  }
  customElements.define('buy-box', BuyBox);

  /* ---------- sticky buy bar ---------- */
  class StickyBuy extends HTMLElement {
    connectedCallback() {
      const target = document.getElementById(this.dataset.target);
      if (!target || !('IntersectionObserver' in window)) return;
      // Hide the bar whenever any part of the buy section is on screen.
      const actions = target;
      let actionsVisible = true;
      const update = () => {
        const show = !actionsVisible && window.scrollY > window.innerHeight * 0.9;
        this.classList.toggle('is-visible', show);
        document.body.classList.toggle('has-sticky-buy', show);
        document.body.classList.toggle('buy-in-view', actionsVisible);
      };
      this.observer = new IntersectionObserver(([entry]) => { actionsVisible = entry.isIntersecting; update(); });
      this.observer.observe(actions);
      this.onScroll = () => update();
      window.addEventListener('scroll', this.onScroll, { passive: true });
      const link = qs('a', this);
      if (link) link.addEventListener('click', (e) => {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    }
    disconnectedCallback() {
      if (this.observer) this.observer.disconnect();
      window.removeEventListener('scroll', this.onScroll);
      document.body.classList.remove('has-sticky-buy', 'buy-in-view');
    }
  }
  customElements.define('sticky-buy', StickyBuy);

  /* ---------- discount popup ---------- */
  class DiscountPopup extends HTMLElement {
    connectedCallback() {
      this.panel = qs('.popup__panel', this);
      this.teaser = document.querySelector('[data-popup-open]');
      this.key = 'alumnus-popup';
      this.days = Number(this.dataset.days) || 7;

      qsa('[data-popup-close]', this).forEach((el) => el.addEventListener('click', () => this.close(true)));
      if (this.teaser) this.teaser.addEventListener('click', () => this.open());

      const form = qs('[data-popup-form]', this) || qs('form', this);
      if (form) form.addEventListener('submit', () => {
        try { window.sessionStorage.setItem('alumnus-popup-submitted', '1'); } catch (e) { /* ignore */ }
      });

      this.addEventListener('click', (e) => {
        const copy = e.target.closest('[data-copy-code]');
        if (!copy) return;
        const code = copy.dataset.copyCode;
        if (navigator.clipboard) navigator.clipboard.writeText(code).catch(() => {});
        copy.textContent = strings.copied || 'Copied';
      });

      this.onKey = (e) => {
        if (!this.classList.contains('is-open')) return;
        if (e.key === 'Escape') this.close(true);
        trapFocus(this.panel, e);
      };
      document.addEventListener('keydown', this.onKey);

      if (this.hasAttribute('data-design-mode')) return; // opened from the editor instead

      // Back from a successful signup: show the code.
      let submitted = false;
      try { submitted = window.sessionStorage.getItem('alumnus-popup-submitted') === '1'; } catch (e) { /* ignore */ }
      const posted = /customer_posted=true/.test(window.location.search);
      if (posted) storage.set(`${this.key}-subscribed`, '1');
      if (posted && submitted && qs('[data-popup-success]', this)) {
        try { window.sessionStorage.removeItem('alumnus-popup-submitted'); } catch (e) { /* ignore */ }
        this.open();
        return;
      }

      if (storage.get(`${this.key}-subscribed`)) return;
      const last = Number(storage.get(`${this.key}-dismissed`)) || 0;
      if (Date.now() - last < this.days * 86400000) {
        if (this.teaser) this.teaser.hidden = false;
        return;
      }
      this.arm();
    }

    disconnectedCallback() {
      document.removeEventListener('keydown', this.onKey);
      this.disarm();
    }

    arm() {
      const delay = Number(this.dataset.delay) || 0;
      const scroll = Number(this.dataset.scroll) || 0;
      if (delay > 0) this.timer = setTimeout(() => this.open(), delay * 1000);
      if (scroll > 0) {
        this.onScroll = () => {
          const height = document.documentElement.scrollHeight - window.innerHeight;
          if (height > 0 && (window.scrollY / height) * 100 >= scroll) this.open();
        };
        window.addEventListener('scroll', this.onScroll, { passive: true });
      }
      if (this.dataset.exit === 'true' && window.matchMedia('(pointer: fine)').matches) {
        this.onLeave = (e) => { if (e.clientY <= 0) this.open(); };
        document.addEventListener('mouseout', this.onLeave);
      }
    }

    disarm() {
      clearTimeout(this.timer);
      if (this.onScroll) window.removeEventListener('scroll', this.onScroll);
      if (this.onLeave) document.removeEventListener('mouseout', this.onLeave);
    }

    open() {
      if (this.classList.contains('is-open')) return;
      // Never cover the cart drawer or mobile menu.
      const drawerOpen = document.querySelector('cart-drawer.is-open, .menu-drawer[open]');
      if (drawerOpen && !this.hasAttribute('data-design-mode')) return;
      this.disarm();
      this.previousFocus = document.activeElement;
      this.classList.add('is-open');
      if (this.teaser) this.teaser.hidden = true;
      lockScroll(true);
      setTimeout(() => {
        const input = qs('input[type="email"]', this);
        (input || this.panel).focus();
      }, 60);
    }

    close(remember) {
      this.classList.remove('is-open');
      lockScroll(false);
      if (remember) storage.set(`${this.key}-dismissed`, String(Date.now()));
      if (this.teaser && !storage.get(`${this.key}-subscribed`)) this.teaser.hidden = false;
      if (this.previousFocus && this.previousFocus.focus) this.previousFocus.focus();
    }
  }
  customElements.define('discount-popup', DiscountPopup);

  /* ---------- theme editor support ---------- */
  document.addEventListener('shopify:section:load', (e) => {
    initReveal(e.target);
    initAutoplayVideos(e.target);
  });
  document.addEventListener('shopify:section:select', (e) => {
    const popup = e.target.querySelector('discount-popup');
    if (popup) popup.open();
  });
  document.addEventListener('shopify:section:deselect', (e) => {
    const popup = e.target.querySelector('discount-popup');
    if (popup) popup.close(false);
  });
  document.addEventListener('shopify:block:select', (e) => {
    const block = e.target;
    const carousel = block.closest('carousel-slider');
    if (carousel && carousel.scrollToItem) carousel.scrollToItem(block);
    const details = block.closest('details') || (block.tagName === 'DETAILS' ? block : null);
    const faq = block.closest('faq-tabs');
    if (faq && block.dataset.category) faq.select(block.dataset.category);
    if (details) details.open = true;
  });

  /* ---------- boot ---------- */
  initReveal();
  initAutoplayVideos();
  // Safety net: never leave content hidden if the observer misses something.
  window.setTimeout(() => qsa('.reveal:not(.is-in)').forEach((el) => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight) el.classList.add('is-in');
  }), 1500);
})();
