There are two problems to solve when allowing the user to scroll through an "infinite" number of elements/photos:

1. You can't load an infinite amount of data.
2. You can't render an infinite amount of elements.

The solution to both is to not provide an infinite amount of elements, but instead create the illusion
of an infinite amount of elements by only loading and displaying what the user would actually currently be able to see.

## Loading Data - Progressively ##

The problem of infinite data is solved by loading the actually required elements progressively, in fixed amounts (batches).

- Load a batch of elements. If they don't fill the screen, load the next batch. repeat until the screen is filled.
- When the user is getting close to the end of the currently loaded elements, load the next batch of data.

In an ideal world the "next batch" is always loaded fast and early enough so that the user doesn't even notice that it
wasn't there from the beginning. This creates the illusion of having an infinite amount of data available.
There are two parameters to consider:

1. When to start loading the next batch?
    -  loading to early results in to much unnecessary data getting laoded.
    -  loading to late results in the user bumping into the end of the list of elements, because the next batch hasn't finished loading yet.
2. How large are the batches?
    -  to small batches can slow down the overall loading time by resulting in overhad because of too many requests.
    -  to large batches need to long to load for a single batch, so that the data may not yet be ready when it is needed.

The best values for these parameters vary vastly depending on the current network speed, number of elements that fit on the screen and the speed the user is scrolling. Luckily these values don't need to be perfect, just good enough.

We currently use [vue-infinite-scroll](https://www.npmjs.com/package/vue-infinite-scroll) to detect when the user is about to reacht the end of the currently loaded list, so we can load the next batch.
The batchsize depends on the current view and is currently somewhere in the range of 50 - 300 elements.

## Rendering elements - Virtualized ##

The further a user scrolls, the more batches of elements get loaded and displayed.
The more elements get displayed, the slower the browser gets and the more memory it needs.  
This means, if we were to just render all loaded elements, the limit how far you can scroll
would be entirely determined by the available cpu and memory of the client.

### Regular virtualization 

This problem is usually solved by virtualization:

1. determine the scrollposition and screensize of the client.
2. calculate what elements would be on the screen.
3. render **only** those elements.

The problem with this regular virtualization is that it requires the elements to be positioned absolutely and may prescribe how they are structured.
Implementing it would therefore imply a potentialy larger rewrite and less freedom when designing the elements.

### Pseudo-Virtualization with placeholders

Using the [IntersectionObserver API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API) we can efficiently determine wether something is currently visible or not.
We can use this information to replace all elements that are currently not in the visible area with simple placeholders of the same size.
This drastically reduces the load on the browser, because these (often single-domnode) placeholder-elements require a LOT less ressources.

This has the huge benefit that it doesn't restrict how components are structured or positioned, while also being easier to implement.
There are however two caveats:

1. We are still rendering *something* for every single loaded elements
    - The load on the browser therefore technically still increases (slightly) the more elements are loaded
    - This however reduces the load so much, that this slight increase per element barely matters at all
2. The placeholders size should be as close to the originals size as possible.
    - If the sizes don't match, scrolling might become a little janky.

This type of virtualization more than fast enough, and because we think the benefits outweigh the downsides, we decided go this route.

### Implementation details

The setup for a component that uses the placeholder-virtualization is as follows:

1. Add a ref to all the elements whose visibilty needs to be tracked
2. create a single `IntersectionObserver` in the `beforeCreate` that calls a (yet to be defined) `this.visibilitiesChanged`
3. on `mounted` and `updated`, call [observe](https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserver/observe) on all refs from step 1
4. define a function that takes an [IntersectionObserverEntry](https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserverEntry) and returns the index of the corresponding target (for example by adding a `data-index`-attribute to the observed element)
5. add `firstVisibleElementIndex: 0`, `lastVisibleElementIndex: 0` and `visibleElementIndices: new Set()` to the components state
6. conditionally render elements whose index is between `firstVisibleElementIndex` and `lastVisibleElementIndex`. Render placeholders for all other elements
7. define `visibilitiesChanged`. Let it call `virtualizationTools.updateVisibleElementIndices`. Use the result as new `this.firstVisibleElementIndex` and `this.lastVisibileElementIndex`

We use the `visibleElementIndices`-Set to keep track of elements that became visible or invisible.  
We also use `firstVisibleElementIndex` and `lastVisibleElementIndex` for two reasons:

1. Vue doesn't react to Set-changes (because its identity never changes), so manipulating it doesn't cause a rerender
2. When scrolling very fast, the set may for a very brief moment contain holes (for example it has the indices `1, 2, 4, 5, 6`). By implying that everything between the smallest and largest index is visible, these short-lived holes don't have any negative effect (index 3 would be rendered anyway)

### Render Performance

When working with a huge amount of elements, render performance of these elements is critically important.
The better the render performance, the more it actually feels like scrolling through an infinite list. It allowes the user to scroll faster without having to see placeholders and makes the application feel way snappier, especially on lower-end devices.

Here are some tips on how to gain performance. They are ordered from most to least important and only apply to things that are rendered for every element:

- Prefer regular HTML-Elements over vue-components
    - Rendering vue components executes a lot of JavaScript, blocking everything else. Rendering regular HTML elements is way faster
    - Example: use `<button>` instead of `<v-btn>`
- Prefer conditional rendering over hiding/showing elements via css
    - showing/hiding via css may prevent rerenders, but it increases the amount of rendered elements
    - The less elements (and therefore domnodes) are rendered the better
    - **Exception:** 
- Use less elements
    - Why use a `<v-card><v-img></v-img></v-card>` when performance is important and a `<div></div>` with some css works too?

### Memoization

Memoization is a technique to speed up function calls by caching results.
This can have a noticable impact on render-performance, especially when function
results are used for placeholders

Example: The the texts on the cards in the cards-view. There are function-calls like `photo.locationInfo()` and `photo.getDateString()`.  
The resulting values rarely change, but are calculated again and again on every render, resulting in ~280k calls per function when scrolling through ~2k pictures.

We use [`memoize-one`](https://www.npmjs.com/package/memoize-one) for much called, non-trivial functions whose parameters rarely change.
The funtions in the Photo model are a prime example for that.

For this to work the memoized function must be pure, which means its result must not depend on outside factors, but only on its parameters. Calling the same function twice with the same parameters must always return the same result.

If you want to memoize a function that is not pure you can still do so by moving all its logic into a new, memoized, pure function and having the old funtion just call the memoized one, providing the required parameters. Example:
```JavaScript
// ------------------ before ------------------
isPlayable() {
  if (this.Type === MediaAnimated) {
    return true;
  } else if (!this.Files) {
    return false;
  }

  return this.Files.some((f) => f.Video);
}
```
```JavaScript
// ------------------ after ------------------
isPlayable() {
  return this.generateIsPlayable(this.Type, this.Files);
}

generateIsPlayable = memoizeOne((type, files) => {
  if (type === MediaAnimated) {
    return true;
  } else if (!files) {
    return false;
  }

  return files.some((f) => f.Video);
})
```
