# Thumbnail Image API

## Introduction

Like most commercial image hosting services, we have chosen to implement a **cookie-free** thumbnail API to minimize request latency by avoiding unnecessary network traffic:

- When a browser requests static files such as images over HTTPS, it is usually unnecessary to send a cookie with every request if the URLs cannot be guessed
- One possible use of cookies may be to prevent the user from intentionally or accidentally sharing confidential thumbnail URLs with others
- This is possible with most image hosting services/social media sites, and could also be considered a feature if you just want to share a few thumbnails without a lot of bells and whistles
- Once an image has been downloaded by someone else, blocking the original URL provides little additional security, as digital copies are just as good as the original, see info box below
- Keeping that in mind, previously shared URLs can be invalidated by rotating the token they contain: for an account's own token by changing that account's password, or by [changing the configured token](../../getting-started/config-options.md#authentication) for URLs that carry it, see [Preview Tokens](#preview-tokens) below
- This will invalidate the browser cache on all connected devices, requiring previously cached thumbnails to be downloaded again
- Be aware that frequent token changes result in performance degradation and a poor user experience.

In addition to better performance, a major advantage of cookie-free thumbnails is that they can be easily integrated into a content delivery network (CDN), since there is no need to check cookies or add other complex logic on edge servers.

!!! example ""
    Since most users only have one domain/host name and modern web applications can store [authentication tokens](auth.md) in *localStorage*, our Thumbnail Image API does not currently require or use cookies.

### Preview Tokens

Preview tokens are one of two media tokens; see [Preview & Download Tokens](tokens.md) for how they compare. How they are issued depends on whether the instance requires authentication:

- **In public mode**, no token is validated and the literal string `public` is used for everyone, so every visitor sees identical preview URLs.
- **Otherwise, one token per user account**, copied to the sessions that account opens. Visitors who follow a share link instead receive a token belonging to their session alone, which expires with it.

Outside public mode, a token is accepted only while at least one session holding it is still active, so it is released when the account's last session ends, and rotating an account's token invalidates the URLs that carry the previous one. Because the token is part of the URL, the same picture then has a different preview URL for each account.

#### Shared Tokens & CDNs

In public mode there is a single token, so a cache or CDN stores one copy of each thumbnail and nothing fragments. Where accounts have their own tokens, an upstream cache instead stores a separate copy per account, which lowers the hit rate.

`PHOTOPRISM_PREVIEW_TOKEN` pins the instance-wide token value that the server accepts, so preview URLs you construct yourself stay valid across restarts. Signed-in accounts are still served their own token, so setting this option does not by itself make their URLs identical. Leave it unset to have a stable value derived automatically.

Changing the configured value invalidates URLs that carry it, and frequent changes degrade cache performance as described above. An account's own token is rotated when that account's password changes.

### Security Considerations

Digital copies are as good as originals: Once shared and downloaded, such images should be considered "leaked" because they are cached and can be re-shared by the recipient at any time, with no sure way to get all copies back, even if the download URL becomes invalid or the service is shut down completely.

Any form of protection we could provide would essentially be "snake oil", could be circumvented, and would have a negative impact on the user experience, such as disabling the browser cache or context menu.

Thumbnail and video URLs are capability URLs: they are authorized by the SHA1 hash together with the token they contain, not by an app session or a cookie. The [user roles](../../user-guide/users/roles.md) that govern access to the app and its other API endpoints therefore do not apply to these paths, which is what makes them cacheable and CDN-friendly in the first place. Treat a preview URL as usable by anyone who has it, for as long as its token is valid.

For the highest level of protection, it is recommended to shield your private server from the public Internet. Always use **HTTPS, a VPN and/or ideally TLS client certificates** and make sure that only people you trust have access to your instance.

### Further Reading

- https://ourcodeworld.com/articles/read/1341/why-you-should-use-a-cookie-less-domain-for-serving-your-static-content-cdn
- https://pragmaticwebsecurity.com/articles/oauthoidc/localstorage-xss.html

## Image Endpoint URI

A GET request to the following URI returns a thumbnail image of the [specified size](#thumbnail-sizes) for the picture referenced by the SHA1 hash:

```
/api/v1/t/:hash/:token/:size
```

If the instance requires authentication, you must also specify a valid [security token](search.md#response-headers), e.g.:

```
/api/v1/t/a2195b6840f46b555719d8e22e9b080e61a7317c/10d68214/tile_500
```

With public mode enabled, you can instead use "public" as [security token](search.md#response-headers) placeholder:

```
/api/v1/t/a2195b6840f46b555719d8e22e9b080e61a7317c/public/tile_500
```

## Video Endpoint URI

A GET request to the following URI returns the video referenced by the SHA1 hash (transcoding and range requests are supported for streaming):

```
/api/v1/videos/:hash/:token/:format
```

If the instance requires authentication, you must also specify a valid [security token](search.md#response-headers), e.g.:

```
/api/v1/videos/51843134d75f4cbde534270cdd5954067f887ee6/10d68214/avc
```

With public mode enabled, you can instead use `public` as the [security token](search.md#response-headers) placeholder:

```
/api/v1/videos/51843134d75f4cbde534270cdd5954067f887ee6/public/avc
```

!!! example ""
    The only target format currently available for transcoding is `avc` (MPEG-4 AVC / H.264).

## Thumbnail Sizes

The smallest configurable static and dynamic size limit is 720px, so most sizes up to `fit_720` are **always** generated by default.
[Higher size limits](../../user-guide/settings/advanced.md#preview-images) generate thumbnails with more detail at higher resolutions - either statically (pre-generated while indexing) or **on demand** if the [configuration permits](../../getting-started/config-options.md#preview-images).

**Optional** thumbnail sizes cannot be pre-generated and are only rendered on request, for example when sharing an image on Instagram.

The following overview shows the name, dimensions, and aspect ratio for each thumbnail size as well as a description of how it is used:

| Name      | Width | Height | Aspect Ratio | Available | Usage             |
|-----------|-------|--------|--------------|-----------|-------------------|
| colors    | 3     | 3      | 1:1          | Always    | Color Detection   |
| tile_50   | 50    | 50     | 1:1          | Always    | List View         |
| tile_100  | 100   | 100    | 1:1          | Always    | Places View       |
| left_224  | 224   | 224    | 1:1          | On-Demand | AI                |
| right_224 | 224   | 224    | 1:1          | On-Demand | AI                |
| tile_224  | 224   | 224    | 1:1          | Always    | AI, Mosaic View   |
| left_384  | 384   | 384    | 1:1          | Optional  | AI                |
| right_384 | 384   | 384    | 1:1          | Optional  | AI                |
| tile_384  | 384   | 384    | 1:1          | Optional  | AI                |
| left_480  | 480   | 480    | 1:1          | Optional  | AI                |
| right_480 | 480   | 480    | 1:1          | Optional  | AI                |
| tile_480  | 480   | 480    | 1:1          | Optional  | AI                |
| tile_500  | 500   | 500    | 1:1          | Always    | Cards View        |
| fit_720   | 720   | 720    | Preserved    | Always    | SD TV, Mobile     |
| tile_1080 | 1080  | 1080   | 1:1          | Optional  | Instagram         |
| fit_1280  | 1280  | 1024   | Preserved    | On-Demand | HD TV, SXGA       |
| fit_1600  | 1600  | 900    | Preserved    | Optional  | Social Media      |
| fit_1920  | 1920  | 1200   | Preserved    | On-Demand | Full HD           |
| fit_2048  | 2048  | 2048   | Preserved    | Optional  | DCI 2K, Tablets   |
| fit_2560  | 2560  | 1600   | Preserved    | On-Demand | Quad HD           |
| fit_3840  | 3840  | 2400   | Preserved    | Optional  | 4K Ultra HD       |
| fit_4096  | 4096  | 4096   | Preserved    | On-Demand | DCI 4K, Retina 4K |
| fit_5120  | 5120  | 5120   | Preserved    | On-Demand | Retina 5K         |
| fit_7680  | 7680  | 4320   | Preserved    | On-Demand | 8K Ultra HD 2     |
| fit_15360 | 15360 | 8640   | Preserved    | On-Demand | 16K UHD           |

↪ [`internal/thumb/sizes.go`](https://github.com/photoprism/photoprism/blob/develop/internal/thumb/sizes.go)

!!! example ""
    Generated thumbnail files are stored in the `storage/cache/thumbnails` folder, where the path and file name depend on the [thumbnail size](../media/thumbnails.md#standard-sizes) and original file hash. [Learn more ›](../media/thumbnails.md)

## Size Limits

Two [configuration options](../../getting-started/config-options.md#preview-images) bound the sizes an instance produces, both in pixels:

| Option                         | Default | Effect                                      |
|--------------------------------|---------|---------------------------------------------|
| PHOTOPRISM_THUMB_SIZE          | 1920    | Largest size pre-generated while indexing   |
| PHOTOPRISM_THUMB_SIZE_UNCACHED | 7680    | Largest size that may be rendered on demand |
| PHOTOPRISM_THUMB_UNCACHED      | false   | Renders sizes above the pre-generated limit |

A request for a size larger than the instance can render is **reduced to the largest size available**, on the image endpoint as well as on the [cover endpoints](#cover-images). The reduction resolves to a `fit_*` size, so the complete picture is preserved rather than cropped.

The `thumbs` list in the client configuration advertises only the sizes within these limits, so clients that build their URLs from it never request a size that would be reduced.

To serve 16K previews, raise the on-demand limit to the full size and enable on-demand rendering:

```yaml
PHOTOPRISM_THUMB_SIZE_UNCACHED: "15360"
PHOTOPRISM_THUMB_UNCACHED: "true"
```

## Cover Images

Albums, labels, and folders have cover endpoints of their own. Note that the folder endpoint takes the UID *after* `/t/`, while the album and label endpoints take it before:

```
/api/v1/albums/:uid/t/:token/:size
/api/v1/labels/:uid/t/:token/:size
/api/v1/folders/t/:uid/:token/:size
```

Albums and labels include a `Thumb` field that holds the file hash of their cover picture. **When it is set, request the picture from the [image endpoint](#image-endpoint-uri) with that hash**, so covers are served from the same cache as all other thumbnails:

```
/api/v1/t/:thumb/:token/:size
```

The album and label cover endpoints return a generic placeholder icon when a cover file is assigned, and resolve a cover by search only for albums and labels that have none. Folders have no `Thumb` field, so their covers are always requested from the folder endpoint.

Since covers are displayed as tiles, they are limited to `fit_720`, and cropped sizes to `tile_500`, with larger requests reduced accordingly. Cover images are always served inline.
