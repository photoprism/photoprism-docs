# Using a Content Delivery Network (CDN)

If you connect your instance to the public Internet and expect the number of users to fluctuate greatly or some users to access it from remote locations with high latency, we recommend configuring a *Content Delivery Network* as this can effectively reduce server load and improve the user experience:

![Network Diagram](https://dl.photoprism.app/img/diagrams/proxy-cdn.svg?classes=w100)

## Config Options

You can use the following config options to specify the URL of an external CDN and change the expiration time for caching server responses:

| Environment                  | CLI Flag            | Default | Description                                                                      |
|------------------------------|---------------------|---------|----------------------------------------------------------------------------------|
| PHOTOPRISM_CDN_URL           | --cdn-url           |         | content delivery network `URL` *sponsors only*                                   |
| PHOTOPRISM_HTTP_CACHE_TTL    | --http-cache-ttl    | 2592000 | number of `SECONDS` that a browser or CDN is allowed to cache HTTP responses     |
| PHOTOPRISM_HTTP_CACHE_PUBLIC | --http-cache-public |         | allow HTTP responses to be stored in a public cache, e.g. a CDN or caching proxy |

!!! note ""
    `PHOTOPRISM_HTTP_CACHE_TTL` and `PHOTOPRISM_HTTP_CACHE_PUBLIC` will be available with our upcoming release.

## CDN Providers

### bunny.net

![Bunny CDN](https://dl.photoprism.app/img/website/bunny-cdn.svg){ class='md right' }
If you don't have a CDN provider yet, we can recommend [bunny.net](https://bunny.net?ref=8wx1e6qu14). This EU-based company may have a funny name, but it's a reputable provider with a good feature set, its own Tier 1 network, and more than 10,000 customers, including big names like Hyundai. We also chose [bunny.net](https://bunny.net?ref=8wx1e6qu14) for our website and public demo as they are fully compliant with the GDPR.[^1]

Prices vary by region and are very reasonable compared to other providers. There is no minimum usage or fixed price, so you only pay for what you actually need. 

[Learn more ›](https://bunny.net?ref=8wx1e6qu14)

[^1]: If you use the link below to sign up for their service, we will receive a $20 credit that helps us operate our [public demo](https://demo.photoprism.app/).
