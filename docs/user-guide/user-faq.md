# Frequently Asked Questions

### What is the easiest way to install PhotoPrism on Mac/Windows? ###

### Should I install PhotoPrism on my laptop or on a server? ###

### Is there a mobile app available? ###
We do not offer a native app via the app stores. 
But our app is fully responsive and you can add it to the homescreen of your phone or tablet. 
This way you can use it like any other app.

**iOS:**

1. Open photoprism in the Safari browser on your phone or tablet
2. Click :material-export-variant:
3. Click add to home screen :material-plus-box-outline:

**Android:**


### How can I find/change my import/originals directories? ###


### Why do some of my photos get the import date as date instead of the date of the image creation? ###
?????

### Where are my files saved? ###
Your original files stay in the directory you defined as Originals during the set up.

### Can PhotoPrism do backups of my files? ###

### Can I backup images from my phone directly to PhotoPrism? ###

### I removed a label but the related keyword is still existing, why? ##
Keywords come from various sources: labels, file names, folder names, locations etc. 
If a label is removed the keyword is not automatically removed because it might originated from another source.
You can delete the keyword manually on the [edit dialogue](organize/edit.md).

### What are sidecar files and where do I find them? ###

A sidecar is a file which sits **alongside** your main photo or video files,
typically using the same name, and a different extension like

* `IMG_0101.jpg`
* `IMG_0101.json`
* `IMG_0101.yaml`

New sidecar files will be created in the *storage* folder by default so that the *originals* folder
can be mounted read-only.

!!! info
PhotoPrism will always look out for existing sidecar files and use them for indexing,
even if `PHOTOPRISM_DISABLE_EXIFTOOL` and `PHOTOPRISM_DISABLE_BACKUPS` are set to `"true"`.

Three types of metadata sidecar files are supported currently:

#### JSON ####

If not disabled via `PHOTOPRISM_DISABLE_EXIFTOOL` or `--disable-exiftool`, [Exiftool](https://exiftool.org/) is used to
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

If disabled via `PHOTOPRISM_DISABLE_BACKUPS` or `--disable-backups`, PhotoPrism will automatically create / update
YAML sidecar files while indexing and after manually editing fields like title, date, or location.
They **serve as a backup** in case the database (index) gets lost, or when folders are synced with a remote
PhotoPrism instance.

Like JSON, YAML files can be opened using common development tools and text editors.
Changes won't be synced back to the original index though as this might overwrite existing data.

#### XMP ####

XMP (Extensible Metadata Platform) is an XML-based metadata container format
[invented by Adobe](https://www.adobe.com/products/xmp.html).
It offers much more fields (as part of embedded models like Dublin Core) than Exif.
That also makes it difficult - if not impossible - to provide complete support.
Reading Title, Copyright, Artist, and Description from XMP sidecar files is implemented as a proof-of-concept,
[contributions welcome](../developer-guide/metadata/xmp.md).
Indexing embedded XMP is only possible via Exiftool, see above.

### What is the advantage of PhotoPrism being OpenSource for me as a user? ###
