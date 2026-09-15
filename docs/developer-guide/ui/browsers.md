# Browser Compatibility

PhotoPrism ships a single-page app that targets evergreen browsers. The loader script at `assets/static/js/browser-check.js` (rendered through `assets/templates/index.gohtml`) blocks unsupported clients before Vue boots, so keep this page aligned with the logic in that script.

## Supported Platforms

- Chrome, Edge, and Firefox: latest stable versions on Windows, macOS, and Linux
- Safari 13+ on macOS and iOS 13+ (the splash screen warns older iOS devices)
- Chromium-based mobile browsers that ship with modern ES2019 features

Internet Explorer is **not** supported. Legacy Android WebView builds without ES modules or Fetch support will hit the browser-check warning.

When introducing APIs that may not exist on the minimum baseline (for example `AbortController` on Safari 13), add a capability check or a lightweight polyfill under `assets/static/js/browser-check.js`.

## Features With a Higher Baseline

Interactive maps need a **WebGL 2** context, which is above the baseline the loader script enforces. That check therefore does not belong in `browser-check.js`: blocking the whole app would deny photo browsing to a client that can do everything except render a map. It is made at render time by `supportsWebGL2()` in [`frontend/src/common/map.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/common/map.js), and the map views show a map-unavailable message when it fails, leaving browsing, location information, and non-map location editing usable. See [Rendering Interactive Maps](maps.md) for the rendering stack.

Follow the same pattern for any other feature whose requirement exceeds the baseline: check the capability where the feature is used and degrade that feature, rather than raising the bar for the whole app.

## Testing

- Run the Vitest unit suite (`make vitest-watch`) on every UI change.
- Use the “Devices” tab in Chrome DevTools or Safari’s Responsive Design Mode to spot layout regressions on phones and tablets.
- [BrowserStack](https://www.browserstack.com/) remains free for open-source projects and is the easiest way to test on edge versions of Safari, iOS, and legacy Android without owning physical devices.
- Capture baseline screenshots for new layouts via the Playwright workflows documented in `AGENTS.md` so we can diff rendering changes over time.
