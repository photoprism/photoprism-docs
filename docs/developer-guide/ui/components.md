PhotoPrism’s frontend is entirely component driven. Vue 3 single-file components live in [`frontend/src/component/`](https://github.com/photoprism/photoprism/tree/develop/frontend/src/component), while full-page views (albums, search, settings, etc.) live under [`frontend/src/page/`](https://github.com/photoprism/photoprism/tree/develop/frontend/src/page). Router entries in [`frontend/src/app/routes.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/app/routes.js) import those page components on demand.

## Global Registration

Shared widgets (toolbars, dialogs, grids, buttons) are registered globally in [`frontend/src/component/components.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/component/components.js) so pages can reference them without a local import. When you add a frequently reused component, export it there and document any required props/slots in the file header.

## Structure and Naming

- Keep component names prefixed with `P` (for PhotoPrism) to avoid clashes with Vuetify components, e.g. `PPhotoViewCards` in [`frontend/src/component/photo/view/cards.vue`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/component/photo/view/cards.vue).
- Organize files by domain: `component/photo/view`, `component/places`, `component/dialog`, etc. Each folder typically holds Vue templates plus small helpers (for example [`frontend/src/component/places/style-control.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/component/places/style-control.js)).
- Vue Router pages belong under [`frontend/src/page/`](https://github.com/photoprism/photoprism/tree/develop/frontend/src/page) (for example `frontend/src/page/labels.vue`). These files orchestrate models ([`frontend/src/model/`](https://github.com/photoprism/photoprism/tree/develop/frontend/src/model)), the `$api` client, and shared components to render full routes.

## Styling and Assets

Component-scoped styles are rare; most UI rules live in the CSS bundles under [`frontend/src/css/`](https://github.com/photoprism/photoprism/tree/develop/frontend/src/css) (for example [`views.css`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/css/views.css), [`navigation.css`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/css/navigation.css), [`places.css`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/css/places.css)). When a component needs custom selectors, co-locate them in the relevant CSS file instead of embedding large `<style>` blocks in the component.

## Authoritative References

- [`frontend/CODEMAP.md`](https://github.com/photoprism/photoprism/blob/develop/frontend/CODEMAP.md) — up-to-date entry points and tooling
- [Focus Management](focus-management.md) — how `$view` wires focus into dialogs and pages
- [Infinite Scrolling](infinite-scrolling.md) — virtualization helpers used by photo views

Let the frontend maintainers know via chat or pull request if a component pattern is unclear. We prefer improving these docs over explaining the same details repeatedly in code reviews.
