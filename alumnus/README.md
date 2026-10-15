# Alumnus: Shopify theme + website playbook

A Pocket-style (heypocket.com) one-product store theme for the Alumnus AI note-taker, plus a PDF with the
comparison, offer and conversion research, the Shopify integration plan, and a Higgsfield prompt for every
image and video slot.

```
alumnus/
├── alumnus-theme.zip                 ← upload this to Shopify
├── alumnus-theme/                    ← the same theme, unzipped (assets, config, layout, locales, sections, snippets, templates)
├── docs/
│   ├── Alumnus-Website-Playbook-and-Higgsfield-Prompts.pdf
│   ├── Higgsfield-Prompts-Copy-Ready.txt   ← every prompt with the device description filled in
│   └── source/                       ← HTML/Python source of the PDF
└── dev/                              ← optional: Theme Check, template validator, local preview, browser tests
```

## Install

1. Shopify admin › **Online Store › Themes › Add theme › Upload zip file** › choose `alumnus-theme.zip`.
2. Click **Customize** on the uploaded theme (don't publish yet).
3. **Theme settings › Product and offer**: pick **Your Alumnus product** (one setting feeds the hero, buy box,
   sticky bar, closing offer and reviews) and set the **Sale end date** (countdowns stay hidden until you do).
4. Create the discounts the buy box advertises (Discounts › Create › Amount off products, automatic):
   "Duo bundle 10% off" with minimum quantity 2, "Study group 15% off" with minimum quantity 3, and the
   popup code `WELCOME10`. Change the percentages in the Buy box tiers if you change them here.
5. Upload images and videos into the labelled slots (see below), fill every `[bracket]`, place a test order, publish.

## Images and videos

Every empty media slot shows a label such as **IMG-01** or **VID-02** with what it should show and the size.
Each label has a matching prompt in Part 4 of the PDF and in `docs/Higgsfield-Prompts-Copy-Ready.txt`.
Product gallery images (IMG-18 to IMG-24, VID-06) go in **Products › Alumnus › Media**, not in the theme.
Labels always show in the theme editor; on the live store you can hide them with
**Theme settings › Media placeholders › Show placeholder labels**.

## What's built in

| Feature | Where to change it |
| --- | --- |
| Announcement bar with rotating messages and real countdown | Header › Announcement bar |
| Hero with live price, compare-at, star rating, trust line | Home › Hero |
| Intro film, logo bar, video carousel, lifestyle gallery, feature grid, app showcase, export formats | Home page sections |
| "Why not just use your phone?" comparison table | Home › Comparison table |
| Buy box: colors, 1/2/3 bundle tiers with badges and per-unit price, countdown, Shop Pay express, Pay in 4, trust badges, low-stock (real inventory), sticky buy bar | Home › Buy box (also the product page) |
| Guarantee strip, specs (can use metafields), plans, privacy, reviews (live stars from Judge.me etc.), FAQ with tabs and Google FAQ schema, closing offer | Home page sections |
| Email popup: timer, scroll and exit-intent triggers, instant code, auto-apply link, teaser tab | Sections list › Discount popup |
| Slide-out cart: savings lines, discount code field, add-on product, Pay in 4, express checkout | Theme settings › Cart |
| Landing page template for ads and personas | Create a page and choose the **landing** template |

## Checks run on this theme

- Shopify Theme Check (`@shopify/theme-check-node` 3.30): **0 errors, 0 warnings**.
- Every JSON template and section group validated against the section schemas (setting names, block types,
  ranges, select values, richtext format).
- Rendered locally with mock store data and tested in Chromium: bundle pricing, variant switching, countdown,
  sticky bar, FAQ tabs, popup triggers and memory, cart drawer, mobile menu, no horizontal scroll on phones
  (33/33 passing). See `dev/`.

## Notes

- Uses Shopify's new customer accounts (the header includes Shopify's sign-in component); legacy account
  templates are not included because Shopify deprecated them.
- Text in `[brackets]` marks facts only you or your supplier can confirm. The PDF's launch checklist lists them all.
- Rebuild the PDF after editing `docs/source/build_playbook.py`:
  `cd docs/source && python3 build_playbook.py && node print_pdf.js` (needs Playwright).
