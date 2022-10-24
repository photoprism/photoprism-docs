# Rendering Interactive Maps in the UI

PhotoPrism includes four [high-resolution world maps](https://try.photoprism.app/library/places) that allow you to browse photos by location.
Visit [try.photoprism.app/library/places](https://try.photoprism.app/library/places) to try them on our demo.

![Places UI Example](https://dl.photoprism.app/img/ui/desktop-places-chicago-1000px.jpg)

The API keys required to use these maps are unfortunately not free for us due to the number of users we have, see [FAQ](../faq.md).

## Mapbox/MapLibre GL JS ##

Because Mapbox GL JS is [no longer open-source](https://wptavern.com/mapbox-gl-js-is-no-longer-open-source),
we now [sponsor](https://github.com/orgs/photoprism/sponsoring) and use [MapLibre GL JS](https://github.com/maplibre/maplibre-gl-js)
for rendering maps in the UI. MapLibre GL is a fork from the last Mapbox GL version available under a permissive
[BSD license](https://github.com/mapbox/mapbox-gl-js/tree/v1.13.2).

Statement by former Mapbox engineer Tom MacWright:

> OSS, we hoped, was about enabling people and unlocking people’s ability to collaborate. It turns out that in 2020, it’s mostly helping companies and getting nothing in return. That’s not a dynamic you can build a sustainable business on.
