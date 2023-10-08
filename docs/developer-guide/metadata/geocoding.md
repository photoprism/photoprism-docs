# Reverse Geocoding

If enabled, reverse geocoding enriches photo and video metadata with details such as country, state, city, and category.

## Privacy Policy ##

As explained in detail in our [Privacy Policy](https://www.photoprism.app/privacy), reverse geocoding depends on retrieving the necessary information from a backend that we provide for this purpose.

The costs are currently fully covered by us for all users, including non-sponsors, and we ensure a very high level of privacy and confidentiality:

- API requests are not logged permanently.
- Our API approximates the coordinates and encodes them with a [fuzzy S2 cell ID](https://s2geometry.io/resources/s2cell_statistics.html) that does not include the house number or any other data identifying a specific residential address, except possibly in very sparsely populated areas of the world. Even then, we cannot trace the request back to a person, picture or point in time.
- We may store your server's IP address and other HTTP request headers for a limited time to perform authorization checks, prevent abuse, and implement rate limits. Since the traffic is encrypted, no one intercepting the server-to-server communication can see the exact request and response; only the fact that you exchanged data with our backend.

*Other open source applications sometimes use the free developer APIs operated by [openstreetmap.org](https://operations.osmfoundation.org/policies/tiles/). In this case, [their usage](https://operations.osmfoundation.org/policies/tiles/) and [privacy policies](https://wiki.osmfoundation.org/wiki/Privacy_Policy) apply, which means that your request data is stored and used to [create publicly available reports](https://planet.openstreetmap.org/tile_logs/). This is different from our approach, which focuses on [our users' privacy](https://www.photoprism.app/privacy) and user experience.*

## Example Request ##

`GET https://places.photoprism.app/v1/location/149ce78563`

```json
{
  "id": "s2:149ce78563",
  "name": "Elafonisi Kite Club",
  "street": "Κεφαλή",
  "postcode": "",
  "category": "nature",
  "timezone": "Europe/Athens",
  "lat": 35.269638,
  "lng": 23.536951,
  "place": {
    "id": "gr:GCd9oey68OFr",
    "label": "Χρυσοσκαλίτισσα, Greece",
    "district": "",
    "city": "Χρυσοσκαλίτισσα",
    "state": "Αποκεντρωμένη Διοίκηση Κρήτης",
    "country": "gr",
    "keywords": "χρυσοσκαλίτσα"
  },
  "events": [],
  "licence": "Data © PhotoPrism"
}
```

## Location Data ##

See: [internal/maps/location.go](https://github.com/photoprism/photoprism/blob/develop/internal/maps/location.go)

## World Maps ##

PhotoPrism also includes four [high-resolution world maps](https://try.photoprism.app/library/places) that allow you to browse photos by location, see [Web User Interface > Interactice Maps](../ui/maps.md). Visit [try.photoprism.app/library/places](https://try.photoprism.app/library/places) to try them on our demo.

## Related Resources ##

### Event Discovery ###

- https://schedjoules.github.io/event-discovery-api/#introduction
- https://www.gdeltproject.org/data.html#rawdatafiles

### Libraries ###

- https://tegola.io/ - An open source vector tile server written in Go
- https://tegola.io/tutorials/tegola-with-open-layers/ - Using Tegola with OpenLayers
- https://github.com/go-spatial/tegola-osm - scripts for importing and running a mirror of OSM with tegola
- https://pelias.io/ - Pelias Geocoder ([GitHub](https://github.com/pelias/pelias))
- https://github.com/Leaflet/Leaflet - JavaScript library for mobile-friendly interactive maps
- https://github.com/tidwall/tile38 - a geospatial database and realtime geofencing server
- https://github.com/melihmucuk/geocache - an in-memory cache that is suitable for geolocation based applications
- https://github.com/aaronland/go-slippy-tiles - a proxy for map tiles
- https://github.com/paulmach/osm - a general purpose library for reading, writing and working with OpenStreetMap data
- https://github.com/maguro/pbf - a Go-based OpenStreetMap PBF encoder/ decoder
- https://github.com/golang/geo - S2 geometry library in Go
- https://gist.github.com/antoniomo/3371e44cbe2f0cc75a525aac0d188cfb - example for S2 geometry library
- https://github.com/tidwall/redcon - Redis compatible server framework (Go)
- https://github.com/siddontang/ledisdb - a high performance NoSQL DB powered by Go ([homepage](http://ledisdb.com/))
- https://github.com/blevesearch/bleve/tree/master/geo - geo support in bleve

### Commercial Services ###

- https://developers.google.com/maps/documentation/
- https://www.mapbox.com/maps/

### Tutorials ###

- https://developers.google.com/maps/solutions/store-locator/clothing-store-locator#findnearsql
- https://blog.mastermaps.com/2014/08/showing-geotagged-photos-on-leaflet-map.html - Showing geotagged photos on a Leaflet map
- https://rubenspgcavalcante.github.io/leaflet-ant-path/ - Animate polylines as ants walking in a path
