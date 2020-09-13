# Frequently Asked Questions

### Can I use trees to organize my pictures and albums? ###

Except in *Library > Originals*, we don't support nested content in our user interface for a number of reasons:

First, there are many tools (including Windows Explorer and Mac OS Finder) that already browse folders in such a way.

A UX problem with trees is that they create namespaces, so the album "Berlin" might exist 20 times. 
Existing album selectors, e.g. when uploading, would instantly become useless and must be replaced 
with a complex tree browser that shows the context. Also difficult to use on a mobile phone.

Personal photo albums can typically be browsed by time, with optional filters - like category - that hide irrelevant results.
That is different in Enterprise asset management, where you might need trees for different products or teams, 
so that responsibilities & [permissions](https://github.com/photoprism/photoprism/issues/455#issuecomment-675859270) can be managed. 
We might do a special release for professional users and Enterprise customers later. 

Note that you can store photos and videos in any folder structure that suits your needs.
We just don't think hierarchical trees should be at the heart of our application.
Most users probably don't have their files properly sorted yet and want to explore them in multiple dimensions.

### What file types are supported by PhotoPrism? ###

PhotoPrism aims to support most common photo file formats like JPEG, PNG, and TIFF.
Depending on your runtime environment and configuration, it can also convert RAW files 
supported by Darktable, RawTherapee, or SIPS.

Video playback is only possible with MPEG-4 AVC files currently. Transcoding of other formats will be added later.
Note that `PHOTOPRISM_SIDECAR_JSON` must the set to `"true"` to extract and index video metadata like location or duration.

Please let us know if you have issues with a specific format you think should be supported.

### Why do some of my pictures have a strange date like 01/01/1980? ###

This may happen in case there was an issue with your camera's settings when the photo was taken.
While the date can easily be changed in the [edit dialog](organize/edit.md), this will only update the index 
but not any original media files.

To change dates - or other fields - directly in your image or video files, please use external apps 
like Photoshop, or Exiftool, and re-index your library.

### Some photos seem hidden after indexing, where are they? ###

If the [quality filter](organize/review.md) is enabled, you might find them in Photos > Review. Otherwise, their
format may not be supported, they may be corrupted, or they may be stacked with other files if their file name, 
exact date & location, or unique image ID, indicate that they belong to the same photo.

### How can I permanently delete files? ###

As we don't modify any originals to avoid unintended data loss, you can currently only "soft delete" pictures
by moving them to Archive using the context menu (if enabled in Settings).

Permanently deleting files for saving storage will be implemented in a later release,
see [Use trashcan to physically delete files after confirmation #167](https://github.com/photoprism/photoprism/issues/167).

When deleting files manually, or using external applications, make sure to re-index your library 
(or run `photoprism purge` in a terminal).

### Which folders will be indexed by PhotoPrism? ###

This depends on your [configuration](../getting-started/config-options.md).

If you're using our example [docker-compose.yml](../getting-started/docker-compose.md) file, your personal photo and video collection 
will be mounted from `~/Pictures` by default, where ~ is a placeholder for your home directory.

You may change this to any folder accessible from your computer, including network drives.
Note that PhotoPrism won't be able to see folders that have not been mounted unless you compile & install it locally
without Docker (recommended only for developers). Multiple folders can be indexed by mounting them as subfolders:

```
volumes:
  - "~/Family:/photoprism/originals/Family"
  - "~/Friends:/photoprism/originals/Friends"
``` 

### What's the difference between keywords and labels? ###

Keywords is a sorted and unique list of search terms extracted from various sources like Exif headers, sidecar files, 
and geo data.
They will be matched with labels, so that pictures with related keywords will automatically be visible in Labels. 

Although related, keywords and labels serve different purposes:

* Labels are general categories, like "cat", "dog", or "boat". They should not include duplicates.
* Keywords are search terms and may include duplicates with the same, or very similar, 
  meaning like "kitten", "cat", "katze", and "cats".

Keywords and labels can both be deleted manually.

### What are sidecar files and where do I find them? ###

A sidecar is a file which sits **alongside** your main photo or video files, 
typically using the same name and a different extension like 

 * `IMG_0101.jpg`
 * `IMG_0101.json`
 * `IMG_0101.yaml`

New files will be created in the storage / sidecar folder by default so that the *originals* folder 
does not need to be modified, and can be mounted read-only.
PhotoPrism will also search the *originals* folder for existing files, and use them for indexing 
even if `PHOTOPRISM_SIDECAR_JSON` or `PHOTOPRISM_SIDECAR_YAML` are set to `"false"`.

Three types of metadata sidecar files are supported currently:

#### JSON ####

If enabled via `PHOTOPRISM_SIDECAR_JSON` or `--sidecar-json`, [Exiftool](https://exiftool.org/) is used to 
automatically create JSON sidecar files. 
Embedded XMP and video metadata can be indexed this way while there is no native support yet (common Exif 
headers in JPEG and PNG files can be indexed natively without [Exiftool](https://exiftool.org/)).
Note that this will cause some overhead when indexing for the first time. 
They may also be useful as original metadata backup, or for debugging as they can be viewed & modified 
with any text editor and many other applications.

#### YAML ####

If enabled via `PHOTOPRISM_SIDECAR_YAML` or `--sidecar-yaml`, PhotoPrism will automatically create YAML sidecar
files while indexing and when manually editing fields like title, date, or location. They serve as a backup
in case the database (index) gets lost, or when you copy files to a different PhotoPrism instance.
YAML files can also be viewed with a regular text editor. Manual changes won't be synced back 
to the original index though as this would create an event loop and might overwrite existing data.
You may only use JSON or XMP files for this.

#### XMP ####

XMP (Extensible Metadata Platform) is an XML-based metadata container format 
[invented by Adobe](https://www.adobe.com/products/xmp.html). 
It offers much more fields (as part of embedded models like Dublin Core) than Exif. 
That also makes it difficult, if not impossible, to provide complete support.
Reading Title, Copyright, Artist, and Description from XMP sidecar files is implemented as a proof-of-concept, 
[contributions welcome](https://docs.photoprism.orig/developer-guide/metadata/xmp/).
Indexing embedded XMP is only possible using JSON sidecar files and Exiftool.
