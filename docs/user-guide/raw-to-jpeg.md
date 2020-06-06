# RAW to JPEG Conversion #

Many photographers keep their originals in some sort of lossless RAW format instead of compressed JPEG, especially when shooting with a Digital SLR. Some [mobile phones](https://www.fredericpaulussen.be/how-to-raw-photos-huawei-p30-pro/) also support RAW or use HEIC/HEIF for a similar purpose. PhotoPrism aims at providing excellent support for all [RAW](https://en.wikipedia.org/wiki/Raw_image_format) formats, independent of camera brand and model. Please let us know when there is an issue with your specific device.

Web browsers in general can not display RAW image files. They need to be converted, which is what our import and convert commands do. You'll also find a checkbox for this step in our Web UI.

In addition, PhotoPrism now also supports TIFF, PNG, BMP and GIF files. Be aware that files in those formats often don't contain useful metadata and are typically used for screenshots, charts, graphs and icons only.

![](https://pbs.twimg.com/media/EPd-Lp1WAAYYBzs?format=png&name=large)

### Read-only mode ###

Conversion is currently disabled in read-only mode because creating JPEGs from RAWs is a pretty expensive operation and it makes sense to store JPEGs right next to their RAW files so that they can be found and used again in the future. Otherwise it might not be possible to match the files again and you don't want to put the expensively created JPEG file in a temporary directory or do all this on the fly in memory, unless you have a really fast computer. Most users want to make a backup of their files, so files that belong together should not be randomly distributed across the file system. 20 years from now, it's probably easier to open a JPEG than render a proprietary RAW file again in good quality.

However, we see the point of [users who want to use PhotoPrism as a read-only photo viewer](https://github.com/photoprism/photoprism/issues/189) that should not create any files in their originals directory. The easiest solution is to create JPEGs manually or use another tool you trust to do this automatically.

With some effort, it might be possible to extract embedded JPEGs in acceptable quality from many RAW formats and use those in read-only mode. Alternatively, JPEGs could be created in the cache directory with all the disadvantages mentioned above, the storage will be gone one way or the other. Note that JPEGs in full-resolution are relatively large and you won't be able to find or reuse them as files there have a different naming scheme based on the hash of the original file.

Idea: Put converted images in `cache/converted` by default with an option to automatically move / copy them to the `originals` directory. Feedback welcome.
