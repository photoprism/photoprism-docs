HEIC / HEIF is a new image file format employing HEVC (h.265) image coding for the best compression ratios currently possible. Newer iPhones use it for internal photo storage. It is supported on iOS 11 and macOS High Sierra and later.

## Testing Conversion and Orientation

Let's say you have Docker installed and want to test HEIF image conversion and orientation with Debian 12 "Bookworm", you can simply run this command to open a terminal:

```bash
docker run --rm -v ${PWD}:/test -w /test -ti debian:bookworm bash
```

This will mount the current working directory as `/test`. Of course, you can also specify a full path instead of `${PWD}`.

The available Ubuntu, Debian and PhotoPrism images can be found on Docker Hub:

- https://hub.docker.com/_/ubuntu
- https://hub.docker.com/_/debian
- https://hub.docker.com/r/photoprism/photoprism/tags

Now install `exiftool` and `libheif-examples` (includes the `heif-convert` command) via `apt`:

```bash
apt update
apt install -y libheif-examples exiftool
```

Finally, run the `heif-convert` command (`-q 92` is optional and determines the JPEG quality/compression):

```
root@1ad9fb887a4f:/test# heif-convert -q 92 IMG_8437.HEIC IMG_8437.HEIC.jpg
File contains 1 image
Written to IMG_8437.HEIC.jpg
```

To view the image metadata, run `exiftool -n <filename>` and optionally use grep to filter the output:

```
root@1ad9fb887a4f:/test# exiftool -n IMG_8437.HEIC.jpg | grep ation
File Modification Date/Time     : 2022:09:18 08:16:28+00:00
Orientation                     : 6
Exposure Compensation           : 0
root@1ad9fb887a4f:/test# exiftool -n IMG_8437.HEIC | grep ation
File Modification Date/Time     : 2022:09:17 16:57:40+00:00
Orientation                     : 6
Exposure Compensation           : 0
HEVC Configuration Version      : 1
Min Spatial Segmentation IDC    : 0
Rotation                        : 270
```

**Rotation** and **Orientation** are the important values you should pay attention to and compare. The rotation is in degrees.

## Exiftool Parameters

- `-n` displays the raw values without changes
- `-j` will format the output as JSON
- `-g` groups the output by metadata source

## Exif Orientation

The Exif orientation values are numbered from 1 to 8:

1. = 0 degrees: the correct orientation, no adjustment is required.
2. = 0 degrees, mirrored: image has been flipped back-to-front.
3. = 180 degrees: image is upside down.
4. = 180 degrees, mirrored: image has been flipped back-to-front and is upside down.
5. = 90 degrees: image has been flipped back-to-front and is on its side.
6. = 90 degrees, mirrored: image is on its side.
7. = 270 degrees: image has been flipped back-to-front and is on its far side.
8. = 270 degrees, mirrored: image is on its far side.

## External Resources ##

- https://www.idownloadblog.com/2017/10/18/how-to-convert-heif-to-jpeg-imazing-heic-converter/ - How to convert HEIF images to JPEGs with iMazing HEIC Converter
- https://github.com/strukturag/libheif - libheif is a ISO/IEC 23008-12:2017 HEIF file format decoder and encoder (C++)
- https://github.com/nokiatech/heif - Reader/Writer Engine is an implementation of the HEIF standard to demonstrate its powerful features and capabilities (C++)
- https://github.com/monostream/tifig - A fast HEIF image converter aimed at thumbnailing
- https://github.com/perkeep/perkeep/issues/969 - HEIC/HEVC support in Perkeep
- https://github.com/jdeng/goheif/ - A decoder/converter for HEIC based on libde265 (CGO)
