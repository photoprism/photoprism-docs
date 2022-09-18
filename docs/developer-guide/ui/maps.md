# Rendering Interactive Maps in the UI

PhotoPrism includes four [high-resolution world maps](https://try.photoprism.app/places) that allow you to browse photos by location, see [rendering maps](../ui/maps.md).

The API keys required to use these maps are unfortunately not free for us due to the number of users we have. Those costs are one of the reasons why we encourage all users to support our mission by [signing up as a sponsor](https://photoprism.app/membership) or purchasing a [commercial license](https://photoprism.app/teams).

![Places UI Example](https://dl.photoprism.app/img/ui/desktop-places-chicago-1000px.jpg)

Visit [try.photoprism.app/places](https://try.photoprism.app/places) to try our demo.

## Mapbox/MapLibre GL JS ##

Because Mapbox GL JS is [no longer open-source](https://wptavern.com/mapbox-gl-js-is-no-longer-open-source),
we now [sponsor](https://github.com/orgs/photoprism/sponsoring) and use [MapLibre GL JS](https://github.com/maplibre/maplibre-gl-js)
for rendering maps in the UI. MapLibre GL is a fork from the last Mapbox GL version available under a permissive
[BSD license](https://github.com/mapbox/mapbox-gl-js/tree/v1.13.2).

Statement by former Mapbox engineer Tom MacWright:

> OSS, we hoped, was about enabling people and unlocking people’s ability to collaborate. It turns out that in 2020, it’s mostly helping companies and getting nothing in return. That’s not a dynamic you can build a sustainable business on.
