PhotoPrism’s library pages create the illusion of “infinite” content by combining progressive loading with lightweight virtualization. The goal is to keep network usage and DOM size under control while allowing users to scroll thousands of photos without jank.

## Progressive Loading

Route components such as [`frontend/src/page/photos.vue`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/page/photos.vue), [`frontend/src/page/albums.vue`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/page/albums.vue), or [`frontend/src/page/labels.vue`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/page/labels.vue) fetch content through the REST models in [`frontend/src/model/`](https://github.com/photoprism/photoprism/tree/develop/frontend/src/model) (`Photo`, `Label`, `Album`, …). Each model inherits batching helpers from [`frontend/src/model/rest.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/model/rest.js), so `Model.batchSize()` defines how many entities we request per round trip.

Pages pass a `loadMore` callback into `<p-scroll>` ([`frontend/src/component/scroll.vue`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/component/scroll.vue)). That component listens to global scroll events and triggers `loadMore()` when the remaining scroll distance is smaller than `loadDistance` (defaults to roughly four viewports). The page component then:

1. Checks `scrollDisabled` / `complete` flags to avoid duplicate fetches.
2. Calls the model’s `search`/`list` method with the current `offset` and `batchSize`.
3. Appends the new results and advances `offset` for the next batch.
4. Updates `$view.saveWindowScrollPos()` so history navigation restores the same position after returning from the lightbox or detail pages.

Tuning tips:

- Use larger batches for cards and mosaic views (hundreds of photos) to amortize request overhead; list view can use smaller batches.
- Adjust `loadDistance` and `batchSize` together. If one grows and the other stays tiny, the UI either loads too much data early or stalls because `loadMore` fires too late.
- The `PScroll` component throttles calls via a `wait` flag. Keep the logic there instead of sprinkling additional throttles in every page component.

## Virtualized Rendering

Even with progressive loading, rendering thousands of fully-populated cards is expensive. Instead of removing DOM nodes entirely (classic virtualization), we swap off-screen cards with lightweight placeholders that preserve layout measurements. The approach lives in:

- [`frontend/src/common/virtualization-tools.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/common/virtualization-tools.js) — helper that tracks visible indices via an `IntersectionObserver`
- [`frontend/src/component/photo/view/cards.vue`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/component/photo/view/cards.vue)
- [`frontend/src/component/photo/view/mosaic.vue`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/component/photo/view/mosaic.vue)
- [`frontend/src/component/photo/view/list.vue`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/component/photo/view/list.vue)

Each view component:

1. Adds `ref="items"` to every rendered card/tile and stores its zero-based index in `data-index`.
2. Creates a single `IntersectionObserver` (see `beforeCreate` hooks) with a generous `rootMargin` so upcoming rows start rendering before they enter the viewport.
3. Observes every second (or fifth) element to reduce callback churn.
4. Persists the visible indices in a `Set` and feeds them into `virtualizationTools.updateVisibleElementIndices()` to derive `[firstVisible, lastVisible]`.
5. Renders the real card markup only when `index` falls within that range; otherwise it renders a simple placeholder `<div>` with matching height/width.

This technique keeps DOM size relatively flat without forcing us to rearchitect the layout around absolute positioning.

### Implementation Details

- Because Vue doesn’t track mutations inside a `Set`, also store `firstVisibleElementIndex` and `lastVisibleElementIndex` in `data()` so reactivity kicks in when the observer reports a change.
- Expand the rendered range by a few items (`±4` in cards view) to hide the swap as a user scrolls quickly.
- Replace removed entries carefully: when a grid item unmounts (for example a photo is deleted), its observer entry may report `isIntersecting=false` even though the page layout has not moved. Ignore entries whose targets are no longer attached to the DOM (see `virtualizationTools.updateVisibleElementIndices`).
- Intersection observers only work when the component is still mounted. Always `disconnect()` inside `beforeUnmount` to avoid leaking references when navigating between routes.

## Rendering Performance

- Prefer raw HTML elements for repeated nodes. For instance, cards view uses `<button>` with utility classes instead of `<v-btn>` to avoid Vuetify reactivity overhead.
- Use Vue conditionals (`v-if` / `v-else`) to strip unused DOM rather than toggling `display: none`.
- Memoize expensive getters in the models. Photo methods such as `getDateString()` use [`memoize-one`](https://www.npmjs.com/package/memoize-one) so scrolling through thousands of cards doesn’t recalculate unchanged metadata on every frame. Keep memoized helpers pure.
- Avoid inline arrow functions in templates for frequently rendered props; compute derived state in `computed` properties once per render.

### Memoization in Practice

The `Photo` model in [`frontend/src/model/photo.js`](https://github.com/photoprism/photoprism/blob/develop/frontend/src/model/photo.js) memoizes multiple helpers so repeated renders reuse cached strings. The example below shows how `generateClasses` caches the computed CSS class list based on a handful of stable inputs:

```js
// frontend/src/model/photo.js
import memoizeOne from "memoize-one";

export class Photo extends RestModel {
  classes() {
    return this.generateClasses(
      this.isPlayable(),
      PhotoClipboard.has(this),
      this.Portrait,
      this.Favorite,
      this.Private,
      this.isStack()
    );
  }

  generateClasses = memoizeOne((isPlayable, isInClipboard,
                                portrait, favorite, isPrivate, isStack) => {
    let classes = ["is-photo", "uid-" + this.UID, "type-" + this.Type];
    if (isPlayable) classes.push("is-playable");
    if (isInClipboard) classes.push("is-selected");
    if (portrait) classes.push("is-portrait");
    if (favorite) classes.push("is-favorite");
    if (isPrivate) classes.push("is-private");
    if (isStack) classes.push("is-stack");
    return classes;
  });
}
```

Because `memoizeOne` returns the previous array when the inputs have not changed, Vue avoids diffing long class lists on every scroll frame. Apply the same pattern to other frequently-called getters (for example, `photo.locationInfo()` or `photo.getVideoInfo()`) to keep render times low.

## Putting It All Together

When implementing a new infinite-scrolling view:

1. Define a batch-friendly model in [`frontend/src/model/`](https://github.com/photoprism/photoprism/tree/develop/frontend/src/model) (if one does not exist yet).
2. Build the route/page that owns the filters, fetch state, and `loadMore` callback.
3. Create a child view component that renders the list and wires in the virtualization helper.
4. Use `$view.saveWindowScrollPos()` / `restoreWindowScrollPos()` so scroll position is preserved when navigating back.
5. Test on low-powered hardware or throttled browsers to confirm placeholders stay ahead of the user while scrolling quickly.

Following these patterns keeps the UI responsive even with very large libraries.
