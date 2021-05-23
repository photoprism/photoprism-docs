# Advanced Settings #

This page enables advanced control of PhotoPrism,
and configuring image and thumbnail handling.

![](img/advanced-settings.jpg)

The same options can all be set using their corresponding
[config options](/getting-started/config-options/) instead.
Settings are saved in the `storage/config` directory.

!!! note
    The Advanced Settings page is not available if public mode is [enabled](/getting-started/config-options/).

## Options

### Debug Logs
When enabled, debug logs are shown in *Library>Logs*.
Requires restart.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_DEBUG`.

### Read-only Mode
When enabled, importing, uploading and deleting files is not possible.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_READONLY`.

### Experimental Features
When enabled, your instance will be updated with experimental features.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_EXPERIMENTAL`.

### Disable Backups
This option prevents creating the following `yml` backups:

- For photos in `storage/sidecar`
- For albums, months, states and folders in `storage/albums`

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_DISABLE_BACKUPS`.

### Disable WebDAV
This option prevents building WebDav connections.
Requires restart for changes to be applied.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_DISABLE_WEBDAV`.

### Disable Places
When selected, geo-information (latitude, longitude) will still be read (and indexed)
from your files metadata, however PhotoPrism will not use reverse lookup to
determine place names using those coordinates as it normally would.

The Places section will not be visible.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_DISABLE_PLACES`.

### Disable ExifTool
This option prevents the creation of `json` files with Exif data in `storage/sidecar`.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_DISABLE_EXIFTOOL`.

### Disable TensorFlow
When selected, image classification / object detection
(using [TensorFlow](https://www.tensorflow.org/)) is disabled,
so no labels are created for your files.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_DISABLE_TENSORFLOW`.

## Images

This section controls how original files are converted to
JPEG for use as thumbnails and image previews.

### Downscaling Filter

This selects the algorithm used to generate downsampled JPEG preview
images ('thumbnails') from original files.

For best quality thumbnails, choose the *lanczos* downscaling filter,
which is slow to process (during thumbnail generation)
but generates higher quality thumbnails.
By comparison, the *cubic* filter may be 30% faster.
See [section below](/user-guide/settings/advanced/#downscaling-filters) for detailed description of available filters.

The equivalent [config option](/getting-started/config-options/) is `PHOTOPRISM_THUMB_FILTER`.

### Dynamic Previews

Enable generating thumbnails on-the-fly as they're required
(either for viewing or analysing with TensorFlow).
This saves disk space, but is more processor-intensive and so not recommended
when hosting on less powerful devices (such as Raspberry Pi).

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_THUMB_UNCACHED`.

### JPEG Quality

For best quality thumbnails, choose a value above 90.
Higher quality values require more storage (larger thumbnails),
and the thumbnails take more time to generate.

Quality levels of 90% or higher are generally considered "high quality",
80%-90% is "medium quality", and 70%-80% is low quality (as you may see
in heavily compressed social media content).
Anything below 70% is typically a very low quality image.
Read more [here](https://fotoforensics.com/tutorial-estq.php).

As an example of file size, if a quality of 95 results in a preview file size of 500kB,
reducing quality to 80 reduces that file size down to about 100kB.

Image classification (which passes the thumbnails through TensorFlow)
also works better with sharp images,
so it's likely a lower quality will result in less accurate labels.

The equivalent [config option](/getting-started/config-options/) is `PHOTOPRISM_JPEG_QUALITY`.

### Dynamic and Static Size Limits

**Dynamic Size Limit**: During dynamic (on-demand) thumbnail generation,
no thumbnails will be created above this size.
The equivalent [config option](/getting-started/config-options/) is `PHOTOPRISM_THUMB_SIZE_UNCACHED`.

**Static Size Limit**: During initial indexing or import (as thumbnails are generated),
no thumbnails will be created above this size.
The equivalent [config option](/getting-started/config-options/) is `PHOTOPRISM_THUMB_SIZE`.

!!! warning
    When the configured size limits are exceeded (for example if users have a larger screen),
    no sufficiently large thumbnail will be generated,
    so the photo viewer may be forced to use original image files instead.
    Browsers can struggle to accurately resample the original file,
    or can display images with the wrong orientation.

The smallest configurable limit is 720px, to enable reasonable preview sizes and for consumption by TensorFlow during image classification.

It's recommended to set these limits high, for the smoothest experience while browsing PhotoPrism.
However, if disk space used by thumbnails is a serious concern,
and you're willing to compromise heavily by increasing processing load on the server,
it's possible to set the Static Size Limit as the minimum possible (720px),
but set a high Dynamic Size Limit.
This will allow the server to generate downsampled preview images on-demand,
causing a delay when previewing a photo in full screen mode.

!!! tip
    To view original images, enable *Dynamic Previews*,
    and configure *Dynamic Size Limit* and *Static Size Limit*
    to a small value like `720`. When viewing images exceeding that limit,
    the original files will be displayed.

#### What files will be created by PhotoPrism?

The minimum size for static previews is 720px, so all images up to `720x720` will be rendered.
Higher static limits will additionally generate previews only up to the defined limit.

The files are generated in the `storage/cache/thumbnails` folder,
with file paths dependent on the size and original file's hash, such as:

`storage/cache/thumbnails/1/a/3/1a30c1f...9_100x100_center.jpg`

The table below shows each generated size, with the PhotoPrism features using each.

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

## Downscaling Filters

### Linear

Bilinear interpolation takes a weighted average of the four
neighborhood pixels to calculate its final interpolated
value. The result is a much smoother image than the original
image. When all known pixel distances are equal, then the
interpolated value is simply their sum divided by four.
This technique performs interpolation in both directions,
horizontal and vertical. This technique gives better result
than nearest neighbor interpolation and take less
computation time compared to bicubic interpolation.

### Cubic

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

### Lanczos

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

### Blackman

Blackman is a modification of Lanczos that has better control of ringing artifacts.

### Examples

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

## RAW Conversion

Many photographers keep their originals in some sort of lossless RAW format instead of compressed JPEG, especially when shooting with a Digital SLR. Some [mobile phones](https://www.fredericpaulussen.be/how-to-raw-photos-huawei-p30-pro/) also support RAW or use HEIC/HEIF for a similar purpose. PhotoPrism aims at providing excellent support for all [RAW](https://en.wikipedia.org/wiki/Raw_image_format) formats, independent of camera brand and model. Please let us know when there is an issue with your specific device.

Web browsers in general cannot display RAW image files. They need to be converted, which is what our *import* and *convert* commands do. You'll also find a checkbox for this step in our [Web UI](general.md).

In addition, PhotoPrism also supports TIFF, PNG, BMP and GIF files. Be aware that files in those formats often don't contain useful metadata and are typically used for screenshots, charts, graphs and icons only.

![](img/editPhoto.png)

!!! info
    Generated sidecar files will be stored outside your originals folder by default, so that
    RAW to JPEG conversion also works in read-only mode.

### JPEG Size Limit

This controls the maximum size of downsampled JPEG preview files to create
when converting original RAW images.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_JPEG_SIZE`.

### Use Presets

Disables simultaneous conversion of RAW files to apply Darktable presets.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_RAW_PRESETS`.

### Disable Darktable

When disabled Darktable won't be used for RAW conversion.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_DISABLE_DARKTABLE`.

### Disable RawTherapee

When disabled RawTherapee won't be used for RAW conversion.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_DISABLE_RAWTHERAPEE`.

### Disable FFmpeg

When disabled FFmpeg won't be used for video transcoding.

The equivalent [config toggle](/getting-started/config-options/) is `PHOTOPRISM_DISABLE_FFMPEG`.
