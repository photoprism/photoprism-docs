# Thumbnail Rendering Settings

The [advanced settings user guide](/user-guide/settings/advanced/) explains the
usage of downscaling filter options and examples of images generated with each.

We use the [disintegration/imaging](https://github.com/disintegration/imaging) package to create thumbnails.

## Preview Sizes ##

These are configured in [`internal/thumb/types.go`](https://github.com/photoprism/photoprism/blob/master/internal/thumb/types.go). A `TypeMap` defines;

- the different dimensions of preview image ('thumbnail') generated
- the corresponding purposes/usages of each
- the source file used to generate each.

## Links ##
- https://en.wikipedia.org/wiki/Comparison_gallery_of_image_scaling_algorithms
- https://en.wikipedia.org/wiki/Lanczos_resampling
- https://en.wikipedia.org/wiki/Image_scaling
