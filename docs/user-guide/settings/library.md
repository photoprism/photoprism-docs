# Library Settings

![](img/settings-library-light.jpg){ class="shadow" }

## Index ##

#### :material-chart-timeline-variant: Estimates ####

Estimates the location of pictures taken without GPS information by extrapolating it from the location of other pictures taken on the same day. 

!!! danger ""
    Be aware that, if you have pictures from unrelated events at different locations, the GPS coordinates of pictures from one event will be applied/extrapolated to pictures of the other event that lack coordinates (even if these are in different folders).

#### :material-eye: Quality Filter ####

Requires a [review of non-photographic and low-quality images](../organize/review.md) before they appear in search results.

#### :material-camera: Preview Images ####

Automatically creates JPEG or PNG preview images for other file types so they can be displayed in search results and in the full-screen viewer. 

!!! danger ""
    *Preview Images* should be enabled, otherwise PhotoPrism cannot index file types other than JPEG or PNG unless a preview sidecar file with the same filename prefix already exists. See *Stacks* to learn more about naming conventions of sidecar files.

!!! info ""
    To prevent inexperienced users from accidentally disabling the creation of thumbnails *Preview Images* can only be disabled when experimental mode is enabled.

## Stacks ##

!!! warning ""
    When you change the stacking settings, already stacked files will not be unstacked automatically.

Stacks are groups of files that have the same origin but differ in quality, format, size, or color. Go to *[Photos > Stacks](../organize/stacks.md)* to see all the picture stacks in your library.

PhotoPrism offers three methods for stacking files:

* :material-clock-outline: **Place & Time** stacks pictures taken at same GPS position and second
* :material-fingerprint: **Unique ID**, matches the *Unique Image ID* (Exif), *Document ID*, or *Instance ID* (XMP)
* :material-format-list-numbered-rtl: **Sequential Name**, for example `/2018/IMG_1234 (2).jpg` and `/2018/IMG_1234 (3).jpg`

Files that have exactly the same file and folder name are **always** stacked, for example `/2018/IMG_1234.jpg` and `/2018/IMG_1234.avi`.

!!! info "Sequential Naming Examples"
    Files with the following name patterns will get stacked with `/2018/IMG_1234.jpg` in case stacking by **sequential name** is enabled

    - `/2018/IMG_1234 (2).jpg` `/2018/IMG_1234 (3).jpg`
     
    - `/2018/IMG_1234 copy.jpg` `/2018/IMG_1234 copy 1.jpg` `/2018/IMG_1234 copy 2.jpg`
    
    - `/2018/IMG_1234 (-2.7)` `/2018/IMG_1234 (+3.3).jpg` `/2018/IMG_1234(-2.7).jpg`  `/2018/IMG_1234(+3.3).jpg`
