# Frequently Asked Questions

### I could not find a documentation of config parameters? ###

You may run `photoprism help` in a terminal to see all options and commands. 
We also maintain a complete list of [config options](config-options.md) in these docs.

Our Docker Compose [examples](https://dl.photoprism.org/docker/docker-compose.yml) are continuously maintained and inline documentation 
has been added to simplify installation.

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

### Which folder will be indexed? ###

This depends on your [configuration](config-options.md). While sub-folders can be selected for
indexing in the UI, changing the base folder requires a restart.

Your photo and video collection will be mounted from `~/Pictures` by default when 
using our example [docker-compose.yml](docker-compose.md) file, 
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

### Which file types are supported? ###

PhotoPrism's primary image file format is JPEG.
While indexing, a JPEG sidecar file may automatically be created for RAW, HEIF, TIFF, PNG, BMP, 
and GIF files. It is required for classification and resampling.

Support for specific RAW formats depends on the runtime environment and configuration. PhotoPrism may use 
Darktable and RawTherapee for RAW to JPEG conversion. 
On Mac OS, [Sips](https://ss64.com/osx/sips.html) can be used as well.

Only MPEG-4 AVC video files are fully supported for now. Transcoding of other codecs is planned for a later release.
In addition, `PHOTOPRISM_SIDECAR_JSON` must be `"true"` in order to
extract and index metadata like location and duration from video files.

You're welcome to open an issue if you experience issues with a specific file format.

### I'm having issues understanding the difference between the import and originals folders? ###

Import is a temporary folder from which you can move or copy files to *originals* in a structured way that avoids duplicates.
Most users with existing collections will want to index their *originals* folder without import, 
so that existing file and directory names don't change. On the other hand, importing may be more efficient when
adding files as you don't need to re-index *originals*.

### What exactly does the read-only mode? ###

There are users who don't want us to modify their original files and folders in any way, so we've added
a configuration option for this use case. It will disable uploads, import and future features
that might rename, update or delete files in the *originals* folder.

### I'm using an operating system without Docker support. How to install and use PhotoPrism without Docker? ###

In general, you would build / install it like a [developer](../developer-guide/setup.md) since we don't have packages 
for specific operating systems yet.

Instead of using Docker, you can manually type the commands listed in our development 
[Dockerfile](https://github.com/photoprism/photoprism/blob/develop/docker/development/Dockerfile) and replace packages with 
what is available in your environment. You often don't need to use the exact same versions for dependencies.

If your operating system has Docker support, we recommend learning Docker as it vastly simplifies installing
and upgrading.

### Do you support Podman? ###

Podman works just fine both in rootless and under root. Mind the SELinux which is enabled on 
Red Hat compatible systems, you may hit permission error problems. 

More details on on how to run PhotoPrism with [Podman](https://podman.io/) on CentOS in 
[this blog post](https://lukas.zapletalovi.com/2020/01/deploy-photoprism-in-centos-80.html), 
it includes all the details including root and rootless modes, user mapping and SELinux.

### Do you provide LXC images? ###

There is currently no [LXC](https://linuxcontainers.org/) build for
PhotoPrism, see [issue #147](https://github.com/photoprism/photoprism/issues/147) for details.

### Any plans to add support for Active Directory, LDAP or other centralized account management options? ###

There is no Active Directory, LDAP, or Single Sign-On support yet as we didn't consider it essential for a first release. 
It might be added later, maybe as a premium feature for our sponsors and contributors.

!!! info
    Our development and testing efforts are focused on small servers and home users. Adding functionality
    that is primarily useful for business environments, or that only benefits few private 
    users with special needs, diverts resources away from features that benefit everyone.
    Professional users are welcome to [reach out](../contact.md) to us for a custom solution.
