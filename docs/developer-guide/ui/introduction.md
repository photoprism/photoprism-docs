# Web UI Overview

Open a terminal and run `photoprism start` (or `make start` inside the main repository) to bring up the built-in web server on [http://localhost:2342](http://localhost:2342). The development compose file (`compose.yaml`) exposes the same port, so once the backend is reachable you can iterate on the frontend without rebuilding the entire container stack.

## Frameworks and Bundling

- The UI is a Vue 3 + Vuetify 3 single-page application. Bootstrap and other legacy frameworks are no longer used.
- The entry points live in [`frontend/src/app.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/app.js) (bootstrap logic, router, plugins) and [`frontend/src/app.vue`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/app.vue) (layout shell). The route definitions are stored in [`frontend/src/app/routes.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/app/routes.js).
- Webpack (configured in [`frontend/webpack.config.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/webpack.config.js)) bundles the Vue code, registers the service worker, and emits the optimized JS/CSS that gets injected into the Go HTML template at [`assets/templates/index.gohtml`](https://github.com/photoprism/photoprism/blob/develop/assets/templates/index.gohtml).
- Startup logic such as the browser capability check and splash screen is implemented in [`assets/static/js/browser-check.js`](https://github.com/photoprism/photoprism/blob/develop/assets/static/js/browser-check.js) and [`frontend/src/css/splash.css`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/css/splash.css), so update both files together when changing the loader.
- Documentation and landing pages may use lightweight static tooling (for example MkDocs Material or Hugo), but the actual app always goes through the Vue stack described above.

For a detailed tour of every directory see [`frontend/CODEMAP.md`](https://github.com/photoprism/photoprism/blob/develop/frontend/CODEMAP.md) in the main repository.

## Components

Reusable Vue components live under [`frontend/src/component/`](https://github.com/photoprism/photoprism/tree/develop/frontend/src/component), while top-level pages that map to Vue Router routes are stored in [`frontend/src/page/`](https://github.com/photoprism/photoprism/tree/develop/frontend/src/page). Global component registration happens in [`frontend/src/component/components.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/component/components.js). The [UI Components](components.md) page explains how we group and reference shared widgets, while Vuetify’s own component catalog covers the standard building blocks that ship with the framework.

## Dependencies

- The authoritative dependency list is [`frontend/package.json`](https://github.com/photoprism/photoprism/blob/develop/frontend/package.json).
- Install or refresh dependencies by running `npm install` inside the `frontend` directory. The root Makefile wraps this via `make deps` / `make install`, which creates `frontend/node_modules/` and the shared `venv/` in one step.
- Add a dependency with `npm install <package> --save` so it is recorded in `package.json` + `package-lock.json`. Always check [`frontend/CODEMAP.md`](https://github.com/photoprism/photoprism/blob/develop/frontend/CODEMAP.md) before adding new runtime libraries.

## Build, Watch, and Test

- Development server / watcher: `make watch-js` from the repo root, or `cd frontend && npm run watch`. This rebuilds the bundle whenever you change files under [`frontend/src/`](https://github.com/photoprism/photoprism/tree/develop/frontend/src).
- Production build: `make build-js` (root) or `cd frontend && npm run build`.
- Dev build without watcher: `npm run build-dev`.
- Unit tests (Vitest): `make vitest-watch` / `make vitest-coverage` or `cd frontend && npm run test`.
- Linting & formatting: `npm run lint` and `npm run fmt` keep ESLint + Prettier aligned with CI.

## External Resources

- https://vuejs.org/guide/quick-start.html — official Vue 3 guide
- https://vuetifyjs.com/en/getting-started/installation/ — Vuetify 3 docs and Material Design guidance
- https://web.dev/explore/progressive-web-apps/ — Google’s canonical PWA reference
- https://webpack.js.org/concepts/ — bundler fundamentals used in [`frontend/webpack.config.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/webpack.config.js)
- https://web.dev/articles/fullscreen/ — background reading for fullscreen helpers in [`frontend/src/common/fullscreen.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/common/fullscreen.js)
- https://maplibre.org/ — base engine for Places maps (see [maps.md](maps.md))
- https://floating-ui.com/ / https://floating-vue.starpad.dev/ — tooltip stack we rely on for hover/focus hints

Older Vue 2 tutorials can still provide inspiration, but always cross-check APIs with the current Vue 3 / Vuetify 3 documentation before copying snippets into the codebase.
