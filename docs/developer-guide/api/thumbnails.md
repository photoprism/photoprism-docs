# Thumbnail Image API

## Introduction

Like most commercial image hosting services, we have chosen to implement a **cookie-free** thumbnail API to minimize request latency by avoiding unnecessary network traffic:

- When a browser requests static files such as images from a server over HTTPS, it is generally unnecessary to send a cookie with each request if the URLs cannot be guessed, so for most practical use cases
- One possible use of cookies may be to prevent the user from intentionally or accidentally sharing confidential thumbnail URLs with others
- This is possible with most image hosting services/social media sites, and could also be considered a feature if you just want to share a few thumbnails without a lot of bells and whistles
- Once an image has been downloaded by someone else, blocking the original URL provides little additional security, as digital copies are just as good as the original, see info box below
- Keeping that in mind, previously shared URLs can be invalidated by [changing the security token in your config](../../getting-started/config-options.md#security-tokens)
- This will invalidate the browser cache on all connected devices, requiring previously cached thumbnails to be downloaded again
- Be aware that frequent token changes result in performance degradation and a poor user experience.

In addition to better performance, a major advantage of cookie-free thumbnails is that they can be easily integrated into a content delivery network (CDN), since there is no need to check cookies or add other complex logic on edge servers.

!!! tldr ""
    Since most users only have one domain/host name and modern web applications can store [authentication tokens](auth.md) in *localStorage*, our Thumbnail Image API does not currently require or use cookies.

### Security Considerations

Digital copies are as good as originals: Once shared and downloaded, such images should be considered "leaked" because they are cached and can be re-shared by the recipient at any time, with no sure way to get all copies back, even if the download URL becomes invalid or the service is shut down completely.

Any form of protection we could provide would essentially be "snake oil", could be circumvented, and would have a negative impact on the user experience, such as disabling the browser cache or context menu.

For the highest level of protection, it is recommended to shield your private server from the public Internet. Always use **HTTPS, a VPN and/or ideally TLS client certificates** and make sure that only people you trust have access to your instance.

### Further Reading ###

- https://ourcodeworld.com/articles/read/1341/why-you-should-use-a-cookie-less-domain-for-serving-your-static-content-cdn
- https://pragmaticwebsecurity.com/articles/oauthoidc/localstorage-xss.html

## Image Endpoint URI

Authenticated with SHA1 hash and additional [security token](search.md#response-headers):

```
/api/v1/t/a2195b6840f46b555719d8e22e9b080e61a7317c/10d68214/tile_500
```

In public mode without [security token](search.md#response-headers):

```
/api/v1/t/a2195b6840f46b555719d8e22e9b080e61a7317c/public/tile_500
```

The thumbnail [size and aspect ratio](#thumbnail-types) are specified at the end, in this case `tile_500`, which means 500x500 pixels.

## Video Endpoint URI

Authenticated with SHA1 hash and additional [security token](search.md#response-headers):

```
/api/v1/videos/51843134d75f4cbde534270cdd5954067f887ee6/10d68214/avc
```

In public mode without [security token](search.md#response-headers):

```
/api/v1/videos/51843134d75f4cbde534270cdd5954067f887ee6/public/avc
```

Videos can be streamed if the browser supports it. The format is specified at the end, in this case MPEG-4 AVC.

## Thumbnail Types ####

The smallest configurable static and dynamic size limit is 720px, so all formats up to `fit_720` should be generated
by default while indexing.

Higher settings allow PhotoPrism to generate thumbnails with more detail in higher resolutions - either 
*statically* (while indexing) or *dynamically* (on-demand).

|   Name    | Width | Height | Aspect Ratio |          Usage          |
|-----------|-------|--------|--------------|-------------------------|
| colors    |     3 |      3 | 1:1          | Color Detection         |
| tile_50   |    50 |     50 | 1:1          | List View               |
| tile_100  |   100 |    100 | 1:1          | Places View             |
| left_224  |   224 |    224 | 1:1          | TensorFlow              |
| right_224 |   224 |    224 | 1:1          | TensorFlow              |
| tile_224  |   224 |    224 | 1:1          | TensorFlow, Mosaic View |
| tile_500  |   500 |    500 | 1:1          | Cards View              |
| fit_720   |   720 |    720 | Preserved    | SD TV, Mobile           |
| tile_1080 |  1080 |   1080 | 1:1          | Instagram               |
| fit_1280  |  1280 |   1024 | Preserved    | HD TV, SXGA             |
| fit_1600  |  1600 |    900 | Preserved    | Social Media            |
| fit_1920  |  1920 |   1200 | Preserved    | Full HD                 |
| fit_2048  |  2048 |   2048 | Preserved    | DCI 2K, Tablets         |
| fit_2560  |  2560 |   1600 | Preserved    | Quad HD, Notebooks      |
| fit_3840  |  3840 |   2400 | Preserved    | 4K Ultra HD             |
| fit_4096  |  4096 |   4096 | Preserved    | DCI 4K, Retina 4K       |
| fit_7680  |  7680 |   4320 | Preserved    | 8K Ultra HD 2           |

↪ [`internal/thumb/sizes.go`](https://github.com/photoprism/photoprism/blob/develop/internal/thumb/sizes.go)

## Storage Folders ##

Generated thumbnails are cached in sub-folders of `/storage/cache/thumbnails` based on the SHA1 hash of the original file.

[Learn more ›](../media/thumbnails.md#storage-folders)
