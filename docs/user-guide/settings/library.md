# Library Settings

![](img/settings-library-light.jpg){ class="shadow" }

## Index

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
    To prevent inexperienced users from accidentally disabling the creation of thumbnails *Preview Images* can only be disabled when [Experimental Features](advanced.md#experimental-features) are enabled.

## Stacks

[Stacks](../organize/stacks.md) are groups of files that have the same origin but may differ in quality, format, size, or color. You can navigate to [*Search > Stacks*](../organize/stacks.md) to find pictures with stacked media files.

PhotoPrism offers you the following optional stacking methods, which you can choose to enable based on your personal preferences:

* :material-clock-outline: **Place & Time** stacks pictures taken at same GPS position and second
* :material-fingerprint: **Unique ID**, matches the *Unique Image ID* (Exif), *Document ID*, or *Instance ID* (XMP)
* :material-format-list-numbered-rtl: **Sequential Name**, for example `/2018/IMG_1234 (2).jpg` and `/2018/IMG_1234 (3).jpg`

Files that share the same file and folder name (except for the file extension) are always stacked, for example `/2018/IMG_1234.jpg` and `/2018/IMG_1234.avi`. Note that it is **not possible to disable stacking of files with the same name** as this would break important functionality, most notably support for Apple [Live Photos](../organize/video.md#live-photos) (which consist of a photo and a video file with the same name), any other multi-format/hybrid formats like RAW/JPEG, and metadata in XMP/JSON sidecar files.

### Are files automatically unstacked when I change the settings?

When you change these settings, files that are already stacked will **not be unstacked automatically**. This is because unstacking is a resource-intensive operation that requires each file to be re-indexed.

The result also depends on the exact order in which you unstack the files, as non-media sidecar files, for example, remain bound to the remaining media file in a stack. We consider providing a command for this in a future release and appreciate [any contributions](../../developer-guide/index.md) in this regard.
 
!!! tldr ""
    If you are new to PhotoPrism and want to re-index your library with different settings, you can run the `photoprism reset` [command in a terminal](../../getting-started/docker-compose.md#command-line-interface) to reset the index and start from scratch.

### Which sequential naming patterns are supported?

If stacking by *Sequential Name* has been enabled, files with e.g. the following names would be stacked with the file `/2018/IMG_1234.jpg`:

- `/2018/IMG_1234 (2).jpg` `/2018/IMG_1234 (3).jpg`
- `/2018/IMG_1234 copy.jpg` `/2018/IMG_1234 copy 1.jpg` `/2018/IMG_1234 copy 2.jpg`
- `/2018/IMG_1234 (-2.7)` `/2018/IMG_1234 (+3.3).jpg` `/2018/IMG_1234(-2.7).jpg`  `/2018/IMG_1234(+3.3).jpg`
