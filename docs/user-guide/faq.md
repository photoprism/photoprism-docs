# Frequently Asked Questions

### Can I use trees for organizing my pictures and albums? ###

Except in *Library > Originals* and for object classification in *Labels*, PhotoPrism does not
support hierarchically organized content for a number of reasons:

First, there are many tools (including Windows Explorer and Mac OS Finder) that already browse folders in such a way.

A common UX challenge is dealing with namespaces.
For example, the album "Berlin" may exist 5 times in different parts of a tree.
Simple input fields or dropdowns become useless in this case and must be replaced 
with a complex tree browser that shows the complete context to avoid ambiguities.
This is especially difficult on mobile screens.

Personal albums can typically be browsed by time, with optional filters for more specific results.
This is different in Enterprise asset management, where trees are required to manage 
responsibilities & [permissions](https://github.com/photoprism/photoprism/issues/455#issuecomment-675859270). 
We might do a special release for professional users later. 

While even deeply nested folders can be indexed without issues,
we don't think trees should be an integral part of our user interface.
Most users won't be able to sort their memories in a strictly hierarchical way 
and prefer to explore them in multiple dimensions instead.

### Which file types are supported? ###

PhotoPrism's primary image file format is JPEG.
While indexing, a JPEG sidecar file may automatically be created for RAW, HEIF, TIFF, PNG, BMP, 
and GIF files. It is required for classification and resampling.

Support for specific RAW formats depends on the runtime environment and configuration. We may use 
Darktable, RawTherapee, and sips (on OS X) for RAW to JPEG conversion.

Only MPEG-4 AVC video files are fully supported for now. Transcoding of other codecs is planned for a later release.
In addition, `PHOTOPRISM_SIDECAR_JSON` must be `"true"` in order to
extract and index metadata like location and duration from video files.

You're welcome to open an issue if you experience issues with a specific file format.

### Why do some pictures have an odd date like 01/01/1980? ###

This may happen in case there was an issue with your camera's settings when the photo was taken.
While the date can easily be changed in the [edit dialog](organize/edit.md), this only updates the index 
without modifying your originals.

To fix the date directly in your image or video files, please use other applications
like Photoshop, or Exiftool, and re-index your library.

### Some files seem hidden, where are they? ###

If the [quality filter](organize/review.md) is enabled, you might find them in *Photos > Review*. Otherwise, their
format may not be supported, they may be corrupted, or they may be stacked with other files if their name, 
exact date & location, or unique image ID indicate they belong to the same photo. You may then unstack 
them if this happened by mistake e.g. because of bad metadata.

### How can I permanently delete files? ###

As we currently don't modify originals to avoid accidental data loss and conflicts with other applications, 
you may only "soft delete" pictures by moving them to *Photos > Archive* using the context menu (if enabled in Settings).

Permanently deleting files for freeing up storage will be implemented in a later release,
see [Use trashcan to physically delete files after confirmation #167](https://github.com/photoprism/photoprism/issues/167).

When deleting files manually, or using other applications, make sure to re-index your library 
(or run `photoprism purge` in a terminal).

### Which folder will be indexed? ###

This depends on your [configuration](../getting-started/config-options.md). While sub-folders can be selected for
indexing in the UI, changing the base folder requires a restart.

Your photo and video collection will be mounted from `~/Pictures` by default when 
using our example [docker-compose.yml](../getting-started/docker-compose.md) file, 
where `~` is a placeholder for your home directory.

You may change this to any folder accessible from your computer, including network drives.
Note that PhotoPrism won't be able to see folders that have not been mounted unless you compile & install it locally
without Docker (developers only).

Multiple folders can be indexed by mounting them as sub-folders of `/photoprism/originals`:

```
volumes:
  - "~/Family:/photoprism/originals/Family"
  - "~/Friends:/photoprism/originals/Friends"
``` 

### What's the difference between keywords and labels? ###

Keywords contain a list of search terms extracted from metadata, file names, and other sources 
like geodata. Pictures with matching keywords automatically show up in related *Labels*. 

Although related, keywords and labels serve different purposes:

* **Labels** may be nested and are primarily used for classification, like "animal", "cat", or "boat". 
  Duplicates and ambiguities should be avoided.
* **Keywords** are primarily used for searching. They may include similar terms and translations,
  like "kitten", "kitty", and "cat".

### What are sidecar files and where do I find them? ###

A sidecar is a file which sits **alongside** your main photo or video files, 
typically using the same name and a different extension like 

 * `IMG_0101.jpg`
 * `IMG_0101.json`
 * `IMG_0101.yaml`

New sidecar files will be created in the *storage* folder by default so that the *originals* folder 
can be mounted read-only.

!!! info
    PhotoPrism will always look out for existing sidecar files and use them for indexing, 
    even if `PHOTOPRISM_SIDECAR_JSON` and `PHOTOPRISM_SIDECAR_YAML` are set to `"false"`.

Three types of metadata sidecar files are supported currently:

#### JSON ####

If enabled via `PHOTOPRISM_SIDECAR_JSON` or `--sidecar-json`, [Exiftool](https://exiftool.org/) is used to 
automatically create a JSON sidecar for each media file. 
**This way, embedded XMP and video metadata can be indexed as well.**
Native metadata extraction is limited to common Exif headers.
Note that this causes moderate overhead when indexing for the first time.

JSON files may also be useful for debugging as they contain the complete metadata, 
and can be processed using common development tools and text editors.

!!! tip
    PhotoPrism can also read JSON files exported by Google Photos. Support for additional
    schemas may be added over time.

#### YAML ####

If enabled via `PHOTOPRISM_SIDECAR_YAML` or `--sidecar-yaml`, PhotoPrism will automatically create / update 
YAML sidecar files while indexing and after manually editing fields like title, date, or location. 
They **serve as a backup** in case the database (index) gets lost, or when folders are synced with a remote 
PhotoPrism instance.

Like JSON, YAML files can be viewed and updated using a text editor.
Manual changes won't be synced back to the original index though as this might overwrite existing data.

#### XMP ####

XMP (Extensible Metadata Platform) is an XML-based metadata container format 
[invented by Adobe](https://www.adobe.com/products/xmp.html). 
It offers much more fields (as part of embedded models like Dublin Core) than Exif. 
That also makes it difficult - if not impossible - to provide complete support.
Reading Title, Copyright, Artist, and Description from XMP sidecar files is implemented as a proof-of-concept, 
[contributions welcome](https://docs.photoprism.orig/developer-guide/metadata/xmp/).
Indexing embedded XMP is only possible via Exiftool, see above.
