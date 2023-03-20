# Using a Content Delivery Network (CDN)

If you connect your instance to the public Internet and expect the number of users to fluctuate greatly or some users to access it from remote locations with high latency, we recommend configuring a *Content Delivery Network* as this can effectively reduce server load and improve the user experience:

![Network Diagram](https://dl.photoprism.app/img/diagrams/proxy-cdn.svg?classes=w100)

## Config Options

You can use the following config options to specify the URL of an external CDN and change the expiration time for caching thumbnails and other static content:

| Environment                  | CLI Flag            | Default | Description                                                 |
|------------------------------|---------------------|---------|-------------------------------------------------------------|
| PHOTOPRISM_CDN_URL           | --cdn-url           |         | content delivery network `URL` *sponsors only*              |
| PHOTOPRISM_HTTP_CACHE_MAXAGE | --http-cache-maxage | 2592000 | time in `SECONDS` until cached content expires              |
| PHOTOPRISM_HTTP_CACHE_PUBLIC | --http-cache-public |         | allow static content to be cached by a CDN or caching proxy |

!!! note ""
    `PHOTOPRISM_HTTP_CACHE_MAXAGE` and `PHOTOPRISM_HTTP_CACHE_PUBLIC` will be available with our upcoming release.

## CDN Providers

### bunny.net

![Bunny CDN](https://dl.photoprism.app/img/website/bunny-cdn.svg){ class='md right' }
If you don't have a CDN provider yet, we can recommend [bunny.net](https://bunny.net?ref=8wx1e6qu14). This EU-based company has a funny name, but is a reputable provider with a good feature set, an own Tier 1 network, and more than 10,000 customers including big names like Hyundai. We also chose [bunny.net](https://bunny.net?ref=8wx1e6qu14) for our website and public demo as they are fully compliant with the GDPR.[^1]

Pricing is very affordable compared to other providers and there is no minimum usage or monthly fee, so you only pay for what you actually need.

[Learn more ›](https://bunny.net?ref=8wx1e6qu14)

[^1]: If you use our link to sign up, we will receive a $20 credit that helps us operate [our demo](https://demo.photoprism.app/).
