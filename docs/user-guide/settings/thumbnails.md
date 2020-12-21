# Thumbnail Settings #

For best results, you should (at least) set jpeg quality to 95 and use the "lanczos" filter. Obviously this will require significantly more storage and CPU time. From our experience, "cubic" might be 30% faster than "lanczos" on modern desktop and server CPUs. Keep in mind that you only need to create thumbnails once and then can enjoy them for the rest of your life.

## Config Options ##

`--thumb-filter NAME, -f NAME`

downscaling filter NAME (best to worst: blackman, lanczos, cubic, linear) (default: "lanczos") [$PHOTOPRISM_THUMB_FILTER]

`--thumb-size PIXELS, -s PIXELS`

static thumbnail size limit in PIXELS (720-7680) (default: 2048) [$PHOTOPRISM_THUMB_SIZE]

`--thumb-uncached, -u`

enable dynamic thumbnail rendering (high memory and cpu usage) [$PHOTOPRISM_THUMB_UNCACHED]

`--thumb-size-uncached PIXELS, -x PIXELS`

dynamic rendering size limit in PIXELS (720-7680) (default: 7680) [PHOTOPRISM_THUMB_SIZE_UNCACHED]

`--jpeg-quality value, -q value`

set to 95 for high-quality thumbnails (25-100) (default: 90) [$PHOTOPRISM_JPEG_QUALITY]

## Example ##

You can limit the size of JPEG thumbnails using the `-s` parameter when you run commands:

```
photoprism -s 720 start
```

The minimum size is 720px. This will render the following images:

![Screenshot 2020-01-08 at 22 10 30](https://user-images.githubusercontent.com/301686/72016344-e5fdfb80-3263-11ea-95b3-00564156140f.png)

500px is used for tiles in search results, the others are mostly needed for classification.

Size is still ~550kb with high quality (95). With lower JPEG quality (80), you'll get it down to ~100kb:

```
photoprism -s 720 -q 80 start
```

This page demonstrates and discusses the effects of JPEG compression: http://fotoforensics.com/tutorial-estq.php

Image classification obviously works better with sharp images, so it's possible you'll get less accurate labels with higher compression. Please share your experience.

If size limit is exceeded, for example because you use a large screen, originals will be used for displaying images in the frontend. This might result in the image displayed with wrong rotation if the browser doesn't rotate it automatically.

## Sizes ##


Name      | Source    | Width  | Height  | Use               |
:---------|:----------|:------:|:-------:|:------------------|
colors    | fit_720   | 3      | 3       | colors            |
tile_50   | tile_500  | 50     | 50      | maps              |
tile_100  | tile_500  | 100    | 100     | maps              |
tile_224  | tile_500  | 224    | 224     | tensorflow        |
left_224  | fit_720   | 224    | 224     | tensorflow        |
right_224 | fit_720   | 224    | 224     | tensorflow        |
tile_500  |           | 500    | 500     | preview           |
fit_720   |           | 720    | 720     | lightbox          |
fit_1280  | fit_2048  | 1280   | 1024    | lightbox          |
fit_1920  | fit_2048  | 1920   | 1200    | lightbox          |
fit_2048  |           | 2048   | 2048    | lightbox          |
fit_2560  |           | 2560   | 1600    | lightbox / retina |
fit_3840  |           | 3840   | 2400    | lightbox / retina |

## Filters ##

Source: https://ijarcce.com/wp-content/uploads/2016/02/IJARCCE-7.pdf

### Linear ###

Bilinear interpolation takes a weighted average of the four
neighborhood pixels to calculate its final interpolated
value. The result is much smoother image than the original
image. When all known pixel distances are equal, then the
interpolated value is simply their sum divided by four.
This technique performs interpolation in both directions,
horizontal and vertical. This technique gives better result
than nearest neighbor interpolation and take less
computation time compared to bicubic interpolation.

### Cubic ###

Catmull-Rom is a local interpolating spline developed for
computer graphics purposes. Its initial use was in design
of curves and surfaces, and has recently been used in
several applications. Catmull-Rom splines are a family of
cubic interpolating splines formulated such that the
tangent at each point is calculated using the previous and
next point on the spline. The results are similar to ones
produced by bicubic interpolation with regards to
sharpness, but the Catmull-Rom reconstruction is clearly
superior in smooth signal region.

### Lanczos ###

The Lanczos interpolation function is a mathematical formula
used to smoothly interpolate the value of a digital
image between its samples. It maps each sample of the
given image to a translated and scaled copy of the Lanczos
kernel, which is a sinc function windowed by the central
hump of a dilated sinc function. The sum of these
translated and scaled kernels is then evaluated at the
desired pixel. Lanczos interpolation has the **best
properties in terms of detail preservation and minimal
generation of aliasing artifacts** for geometric
transformations not involving strong down sampling. 
However higher order Lanczos interpolation requires high
computational time, which makes it unsuitable for
most commercial software.

### Blackman ###

Blackman is a modification of Lanczos that has better control of ringing artifacts.

### Examples ###

Original image:

![](img/branches.png)

The same image resized from 600x400px to 150x100px using different resampling filters.
From faster (lower quality) to slower (higher quality):

Filter                    | Resize result
--------------------------|---------------------------------------------
Nearest Neighbor          | ![](img/out_resize_nearest.png) 
Bilinear                  | ![](img/out_resize_linear.png)
Sharp Bicubic             | ![](img/out_resize_catrom.png)
Lanczos                   | ![](img/out_resize_lanczos.png)
