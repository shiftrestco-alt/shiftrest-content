# Theme dev tools

Checks and a local preview for `../alumnus-theme`. You don't need these to use the theme.

```bash
npm install                     # liquidjs, Shopify Theme Check, Playwright
npm run check                   # Shopify Theme Check + JSON template/settings validator
node preview.js ../alumnus-theme ./preview index --product          # render the homepage with a sample product
node preview.js ../alumnus-theme ./preview index --product --cart --out=index-cart.html
cp ../alumnus-theme/assets/* ./preview/assets/ 2>/dev/null || (mkdir -p preview/assets && cp ../alumnus-theme/assets/* preview/assets/)
(cd preview && python3 -m http.server 8765)                         # serve it
node shot.js http://127.0.0.1:8765/index.html shot.png 1440 900 full  # screenshot
npm test                        # browser tests (bundles, variants, popup, cart drawer, sticky bar, mobile)
```

`preview.js` emulates the Shopify Liquid objects, tags and filters the theme uses (LiquidJS plus mocks).
It is a smoke test, not a Shopify replacement: always check the real store preview before publishing.
`interact.js` expects these rendered files in `preview/`: index, index-fresh, index-cart, product,
landing, cart, collection, search, page.contact, 404, password. Set `CHROMIUM_PATH` if Playwright
should use a specific Chromium build.
