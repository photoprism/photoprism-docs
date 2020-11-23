# Library Settings #

## RAW to JPEG Conversion ##

Many photographers keep their originals in some sort of lossless RAW format instead of compressed JPEG, especially when shooting with a Digital SLR. Some [mobile phones](https://www.fredericpaulussen.be/how-to-raw-photos-huawei-p30-pro/) also support RAW or use HEIC/HEIF for a similar purpose. PhotoPrism aims at providing excellent support for all [RAW](https://en.wikipedia.org/wiki/Raw_image_format) formats, independent of camera brand and model. Please let us know when there is an issue with your specific device.

Web browsers in general cannot display RAW image files. They need to be converted, which is what our *import* and *convert* commands do. You'll also find a checkbox for this step in our [Web UI](ui.md).

In addition, PhotoPrism also supports TIFF, PNG, BMP and GIF files. Be aware that files in those formats often don't contain useful metadata and are typically used for screenshots, charts, graphs and icons only.

![](img/editPhoto.png)

!!! info
    Generated sidecar files are stored outside your originals folder by default, so that
    RAW to JPEG conversion also works in read-only mode.