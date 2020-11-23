# PhotoPrism Places #

We've recently launched **PhotoPrism Places**, a Geocoding API that replaces OpenStreetMap development infrastructure. Our users now enjoy much better performance, higher availability and more privacy. In addition, we're going to add information about public events that have taken place at a location. This can be used to automatically create albums of popular music festivals or sports events.

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
