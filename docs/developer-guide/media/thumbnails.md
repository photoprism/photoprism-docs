# Thumbnail Images

PhotoPrism uses the [disintegration/imaging](https://github.com/disintegration/imaging) package to generate thumbnail
images that are displayed in search results and in the full-screen viewer.

The smallest configurable size is 720 pixels for use by the indexer to perform color detection, face detection,
and image classification. For more details, see [Advanced Settings](../../user-guide/settings/advanced.md)
in the [User Guide](../../user-guide/index.md).

## API Design ##

### Why use a cookie-free domain? ###

Avoiding cookies helps minimize request latency by eliminating network traffic:

- when a browser requests static files such as images from a server via HTTPS, it is generally unnecessary to send a
cookie along with each request if the URLs cannot be guessed realistically - that is, for most practical use cases
- one potential use of cookies might be to prevent the user from intentionally or accidentally sharing cryptic thumbnail URLs with others
- however, this is possible with most real-world image hosting services and could also be considered a feature if you only want to share specific thumbnails without overhead

An additional advantage of this approach is that users can easily integrate a content delivery network (CDN),
as there are no secrets to share and no cookies to check.

Because most users have only one domain/host name and modern Web apps can store authentication tokens in *localStorage*
instead, we have decided not use any cookies by default.

**See also:**

- https://www.keycdn.com/support/how-to-use-cookie-free-domains
- https://ourcodeworld.com/articles/read/1341/why-you-should-use-a-cookie-less-domain-for-serving-your-static-content-cdn
- https://pragmaticwebsecurity.com/articles/oauthoidc/localstorage-xss.html

### Image URIs ####

Authenticated with SHA1 hash and additional security token:

```
/api/v1/t/a2195b6840f46b555719d8e22e9b080e61a7317c/10d68214/tile_500
```

In public mode without security token:

```
/api/v1/t/a2195b6840f46b555719d8e22e9b080e61a7317c/public/tile_500
```

The thumbnail size and aspect ratio are specified at the end, in this case `tile_500`, which means 500x500 pixels.

### Video URIs ####

Authenticated with SHA1 hash and additional security token:

```
/api/v1/videos/51843134d75f4cbde534270cdd5954067f887ee6/10d68214/avc
```

In public mode without security token:

```
/api/v1/videos/51843134d75f4cbde534270cdd5954067f887ee6/public/avc
```

Videos can be streamed if the browser supports it. The format is specified at the end, in this case MPEG-4 AVC.

## Preview Sizes ##

These are configured in [`internal/thumb/types.go`](https://github.com/photoprism/photoprism/blob/master/internal/thumb/types.go). A `TypeMap` defines;

- the different dimensions of preview image ('thumbnail') generated
- the corresponding purposes/usages of each
- the source file used to generate each.

## Links ##

- https://en.wikipedia.org/wiki/Comparison_gallery_of_image_scaling_algorithms
- https://en.wikipedia.org/wiki/Lanczos_resampling
- https://en.wikipedia.org/wiki/Image_scaling
