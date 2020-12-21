# Image Quality Settings

You may change the settings for preview images in the *Advanced* settings tab (not available in public mode):

![](img/advanced-settings.jpg)

For best results, you should choose a high JPEG quality > 90, and the *lanczos* downscaling filter.
This will require additional storage and slows down indexing, but only once when indexing for the first time.

In comparison, the *cubic* filter may be 30% faster than *lanczos*.
A [JPEG quality](http://fotoforensics.com/tutorial-estq.php) setting of 95 results in a preview files size of about 500kb.
Reducing the JPEG quality to 80 gets storage size down to 100kb, and results in visible artifacts
as in heavily compressed social media content.

Image classification also works better with sharp images, 
so it's likely you'll get less accurate labels with higher compression.

## Preview Sizes ##

Name      | Width  | Height  | Use                      |
:---------|:------:|:-------:|:-------------------------|
colors    | 3      | 3       | Color Detection          |
tile_50   | 50     | 50      | List Preview             |
tile_100  | 100    | 100     | Maps Preview             |
tile_224  | 224    | 224     | Mosaic Preview           |
left_224  | 224    | 224     | TensorFlow               |
right_224 | 224    | 224     | TensorFlow               |
tile_500  | 500    | 500     | Cards Preview            |
fit_720   | 720    | 720     | Mobile, TV               |
fit_1280  | 1280   | 1024    | Mobile, HD Ready TV      |
fit_1920  | 1920   | 1200    | Mobile, Full HD TV       |
fit_2048  | 2048   | 2048    | Tablets, Cinema 2K       |
fit_2560  | 2560   | 1600    | Quad HD, Retina Display  |
fit_3840  | 3840   | 2400    | Ultra HD                 |
fit_4096  | 4096   | 4096    | Ultra HD, Retina 4K      |
fit_7680  | 7680   | 4320    | 8K Ultra HD 2, Retina 6K |

!!! note
    When the configured size limit is exceeded, for example if users have a larger screen,
    the photo viewer may be forced to use original image files instead.
    This may result in images displayed with the wrong orientation.

## Downscaling Filters ##

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

Source: [A Comparative Analysis of Image Interpolation Algorithms](https://ijarcce.com/wp-content/uploads/2016/02/IJARCCE-7.pdf)

## What files will be created by PhotoPrism? ##

The minimum size for static previews is 720px. This will render the following images in the cache folder:

```
cache/thumbnails/1/a/3/1a30c1f...9_100x100_center.jpg
cache/thumbnails/1/a/3/1a30c1f...9_224x224_center.jpg
cache/thumbnails/1/a/3/1a30c1f...9_224x224_left.jpg
cache/thumbnails/1/a/3/1a30c1f...9_224x224_right.jpg
cache/thumbnails/1/a/3/1a30c1f...9_3x3_resize.png
cache/thumbnails/1/a/3/1a30c1f...9_500x500_center.jpg
cache/thumbnails/1/a/3/1a30c1f...9_50x50_center.jpg
cache/thumbnails/1/a/3/1a30c1f...9_720x720_fit.jpg
```

A static limit of 2048px renders additional previews up to this size:

```
cache/thumbnails/1/a/3/1a30c1f...9_1280x1024_fit.jpg
cache/thumbnails/1/a/3/1a30c1f...9_1920x1200_fit.jpg
cache/thumbnails/1/a/3/1a30c1f...9_2048x2048_fit.jpg
```

## Config Options ##

When using PhotoPrism in public mode, image quality preferences may be set in the application config file, 
or via command line parameter (requires a restart):

`--thumb-filter NAME, -f NAME`

downscaling filter NAME (best to worst: blackman, lanczos, cubic, linear) (default: "lanczos") [$PHOTOPRISM_THUMB_FILTER]

`--thumb-size PIXELS, -s PIXELS`

static thumbnail size limit in PIXELS (720-7680) (default: 2048) [$PHOTOPRISM_THUMB_SIZE]

`--thumb-uncached, -u`

enable dynamic thumbnail rendering (high memory and cpu usage) [$PHOTOPRISM_THUMB_UNCACHED]

`--thumb-size-uncached PIXELS, -x PIXELS`

dynamic rendering size limit in PIXELS (720-7680) (default: 7680) [PHOTOPRISM_THUMB_SIZE_UNCACHED]

`--jpeg-quality value, -q value`

choose 95 for high-quality thumbnails (25-100) (default: 92) [$PHOTOPRISM_JPEG_QUALITY]
