# Library Settings

## Index ##

#### Hide Private :material-lock: ####
Photos/videos marked as *private* do NOT appear in *Photos*, *Videos*, *Favorites*, *Labels*, *Places* and shared albums in case this option is selected.

#### Quality Filter :material-eye: ####
When selected, non-photographic photos/videos like screenshots and low-quality photos need to be [*reviewed*](../organize/review.md) before they appear in *Photos* or *Videos*.

#### Convert to JPEG :material-camera: ####
*JPEGs* are created for *RAW files* during [*indexing*](../library/indexing.md) in case they do not yet exist. JPEGs will be stored in the same folder next to the original.

!!! attention
In case this is disabled and there is a RAW file without a JPEG there will be no preview.

## Stacks :material-image-multiple: ##

Related files will be grouped when selected.
Grouped files will have one primary file that is shown in our views. You find your grouped files in [*Stacks*](../organize/stacks.md).

PhotoPrism provides three options to group files:

* Place & Time
* Sequential Name
* Unique ID

## RAW to JPEG Conversion ##

Many photographers keep their originals in some sort of lossless RAW format instead of compressed JPEG, especially when shooting with a Digital SLR. Some [mobile phones](https://www.fredericpaulussen.be/how-to-raw-photos-huawei-p30-pro/) also support RAW or use HEIC/HEIF for a similar purpose. PhotoPrism aims at providing excellent support for all [RAW](https://en.wikipedia.org/wiki/Raw_image_format) formats, independent of camera brand and model. Please let us know when there is an issue with your specific device.

Web browsers in general cannot display RAW image files. They need to be converted, which is what our *import* and *convert* commands do. You'll also find a checkbox for this step in our [Web UI](ui.md).

In addition, PhotoPrism also supports TIFF, PNG, BMP and GIF files. Be aware that files in those formats often don't contain useful metadata and are typically used for screenshots, charts, graphs and icons only.

![](img/editPhoto.png)

!!! info
    Generated sidecar files are stored outside your originals folder by default, so that
    RAW to JPEG conversion also works in read-only mode.