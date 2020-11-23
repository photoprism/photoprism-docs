We've recently launched **PhotoPrism Places**, a Geocoding API that replaces OpenStreetMap development infrastructure. Our users now enjoy much better performance, higher availability and more privacy. In addition, we're going to add information about public events that have taken place at a location. This can be used to automatically create albums of popular music festivals or sports events.

We are happy to assist other OSS projects that don't have the time or expertise to run their own infrastructure.

## Example Request ## 

https://places.photoprism.org/v1/location/149ce78563

```json
{
  "id":"149ce78563",
  "name":"Pink Beach",
  "category":"nature",
  "timezone":"Europe/Athens",
  "lat":35.26963621850717,
  "lng":23.53695076231683,
  "place": {
    "id":"149ce78563",
    "label":"Chrisoskalitissa, Crete, Greece",
    "city":"Chrisoskalitissa",
    "state":"Crete",
    "country":"gr"
  },
  "events":[],
  "licence":"Data © OpenStreetMap contributors"
}
```

## Privacy ##

Geocoding requests are NOT logged, but developers can of course see cached items in MariaDB without personal information. That's the point of a cache. Those will be randomly distributed with hot spots around tourist attractions and big cities.

Because of HTTPS, your internet provider can't see the exact request, just that you contacted a server.

The API approximates coordinates, encodes them with [S2](https://s2geometry.io/resources/s2cell_statistics.html) and doesn't care about street or house number:

![](img/placesPrivacy.jpeg)

## Performance ##

First [benchmarks](https://github.com/tsliwowicz/go-wrk) show that up to 2500 req/s can be handled. Compare this with the pricing of commercial providers and you'll see the value. Response times range from 10ms to 7μs, depending on the query and cache.

If you prefer running this on-site: We use a 6-core Intel Xeon processor, 320 GB of SSD and 16 GB of memory. 
In addition you'll have to download ~100 GB of data.
Due to the properties of S2 cell IDs, scaling and sharding should be easy if needed.

## Event Discovery ##
- https://schedjoules.github.io/event-discovery-api/#introduction
- https://www.gdeltproject.org/data.html#rawdatafiles

## Open Source Libraries ##
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

## OpenStreetMap ##
At the moment, we use the [reverse lookup API](https://wiki.openstreetmap.org/wiki/Nominatim#Reverse_Geocoding) of OpenStreetMap as well as the their tiles for our Leaflet-based Places page.

Code: https://github.com/photoprism/photoprism/blob/develop/internal/photoprism/openstreetmap.go

## Commercial Maps ##
- https://developers.google.com/maps/documentation/
- https://www.mapbox.com/maps/

## Tutorials ##
- https://developers.google.com/maps/solutions/store-locator/clothing-store-locator#findnearsql
- https://blog.mastermaps.com/2014/08/showing-geotagged-photos-on-leaflet-map.html - Showing geotagged photos on a Leaflet map
- https://rubenspgcavalcante.github.io/leaflet-ant-path/ - Animate polylines as ants walking in a path
