# Color Profiles

## Standard RGB

[sRGB](https://en.wikipedia.org/wiki/SRGB) is the default color space used when [generating thumbnails](thumbnails.md). PhotoPrism and web browsers assume this color space for all pictures that do not have an embedded ICC color profile.

## ICC Profiles

An [ICC color profile](https://en.wikipedia.org/wiki/ICC_profile) for [wide-gamut displays](https://en.wikipedia.org/wiki/Gamut) can optionally be embedded in image and video files. For color profiles other than [sRGB](https://en.wikipedia.org/wiki/SRGB) and [Display P3](https://en.wikipedia.org/wiki/DCI-P3#P3_colorimetry), the thumbnails must be generated with `libvips` by setting the `PHOTOPRISM_THUMB_LIBRARY` config option to `vips` or `auto` so that the [ICC profiles are preserved](https://github.com/photoprism/photoprism/issues/1474): 

|          Environment           |       CLI Flag        | Default |                                         Description                                          |
|--------------------------------|-----------------------|---------|----------------------------------------------------------------------------------------------|
| PHOTOPRISM_THUMB_LIBRARY       | --thumb-library       | auto    | image processing `LIBRARY` to be used for generating thumbnails (auto, imaging, vips)        |
| PHOTOPRISM_THUMB_COLOR         | --thumb-color         | auto    | standard color `PROFILE` for thumbnails (auto, preserve, srgb, none)                         |

Image colors may otherwise not be displayed correctly, which is particularly noticeable with ProPhoto RGB and Adobe RGB, as these cover a wide range of colors:

![ICC Profiles](img/icc-profiles.svg)

## Color Detection

Color detection is performed during indexing using a 3x3 thumbnail that covers the top, bottom, and center of an image e.g. <https://demo.photoprism.app/library/browse?color=green>.

[Learn more ›](../metadata/colors.md)
