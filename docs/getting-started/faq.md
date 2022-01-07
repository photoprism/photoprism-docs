# Frequently Asked Questions

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

If not disabled via `PHOTOPRISM_DISABLE_BACKUPS` or `--disable-backups`, PhotoPrism will automatically create / update
[YAML](../developer-guide/technologies/yaml.md) sidecar files while indexing and after manually editing fields like 
title, date, or location. They **serve as a backup** in case the database (index) gets lost, or when folders are synced 
with a remote PhotoPrism instance.

Like JSON, [YAML](../developer-guide/technologies/yaml.md) files can be opened using common development tools and text editors.
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

This depends on your [runtime environment](docker-compose.md) and [configuration](config-options.md).
While sub-folders can be selected for indexing in the UI, changing the *originals* base folder 
requires a restart for security reasons.

If you skip configuration and don't use one of our Docker images, PhotoPrism will try to find 
a photo library by going through a list of common 
[folder names](https://github.com/photoprism/photoprism/blob/develop/pkg/fs/dirs.go) 
like `/photoprism/originals`, `Pictures`, and `~/Photos`. It will also search for other resources
like external applications, classification models, and frontend assets.

Your library will be mounted from `~/Pictures` by default when using our 
example [docker-compose.yml](docker-compose.md) file, where `~` is a placeholder for your home directory. 

You may mount any folder accessible from your computer, including network drives.
Note that PhotoPrism won't be able to see folders that have not been mounted unless you install it locally
without Docker (developers only).

Multiple folders can be indexed by mounting them as sub-folders of `/photoprism/originals`:

```
volumes:
  - "~/Family:/photoprism/originals/Family"
  - "~/Friends:/photoprism/originals/Friends"
``` 

### Which file types are supported? ###

The primary image format is JPEG. Support for JPEG XL is planned but not available yet. 
When indexing, a JPEG sidecar file may be created automatically for RAW, HEIF, TIFF, PNG, BMP, GIF, and video files. 
It is needed for generating thumbnails, image classification, and facial recognition.

Due to the patent situation and its complexity, [TIFF is only partially supported](https://github.com/golang/go/issues?q=is%3Aissue+image%2Ftiff+) at the moment.

The following RAW converters can be used to generate JPEGs (included in our Docker image,
otherwise you may need to install them on your system):

- [Darktable](https://www.darktable.org/) ([supported cameras](https://www.darktable.org/resources/camera-support/))
- [RawTherapee](https://rawtherapee.com/) ([supported cameras](https://www.libraw.org/supported-cameras))
 
If you're running PhotoPrism directly on a Mac, RAW files will be converted with [Sips](https://ss64.com/osx/sips.html) ([supported cameras](https://support.apple.com/en-us/HT211241)) by default.
Our goal is to provide top-notch support for all RAW formats, regardless of camera make and model.
Please let us know when there are any issues with a particular camera or file format.

Video formats supported by [FFmpeg](https://en.wikipedia.org/wiki/FFmpeg#Supported_codecs_and_formats) can be transcoded to
[MPEG-4 AVC](https://en.wikipedia.org/wiki/Advanced_Video_Coding). Still images for generating thumbnails can be extracted from 
most videos as well. 

If you have videos, always enable JSON sidecar files so that video metadata such as date, location, codec, 
and duration can be indexed and searched.

### Why don't you display animated GIFs natively? ###

PhotoPrism focuses on photographic images and short videos. You may
[convert your GIF files to  H.264 / MPEG-4 AVC](https://unix.stackexchange.com/questions/40638/how-to-do-i-convert-an-animated-gif-to-an-mp4-or-mv4-on-the-command-line) 
using `ffmpeg`. That's also what Twitter does when you post a GIF. They will then be shown as 
"live photos" and start playing on mouse over while also consuming less storage and bandwidth 
compared to your original GIF files.

### Why is my storage folder so large? What is in it? ###

The storage folder contains sidecar, thumbnail, and configuration files.
It may also contain index database files if you're using SQLite.
Most space is consumed by thumbnails: These are high-quality resampled, smaller 
versions of your originals.

Thumbnails are required because Web browsers do a pretty bad job at resampling large images 
so that they fit your screen. Using originals for slideshows and search result previews 
would consume much more browser memory, and reduce overall performance, as well.

If you're happy with lower quality thumbnails, you can reduce their JPEG quality 
and/or set a size limit. Note that existing thumbnail files won't be replaced automatically 
after changing [config values](config-options.md).

You may also choose to render thumbnails on-demand if you have a fast CPU and enough memory. 
However, storage is typically affordable enough for most users to go for better quality and 
performance instead.

### Can I skip creating thumbnails completely? ###

The smallest [configurable](../user-guide/settings/advanced.md) size is 720px for consumption by 
the indexer to perform color detection, face detection, and image classification. Recreating them 
every time they are needed is too demanding for even the most powerful servers. Unless you only 
have a few small images, it would render the app unusable.

!!! danger ""
    Reducing the *Static Size Limit* of thumbnails has a **significant impact on  [facial recognition](../user-guide/organize/people.md)
    and image classification** results. Simply put, it means that the indexer can no longer see properly.

### I'm having issues understanding the difference between the import and originals folders? ###

You may optionally mount an *import* folder from which files can be transferred to the *originals* folder
in a structured way that avoids duplicates. Imported files receive a canonical filename and will be
organized by year and month.

Most users with existing photo libraries will want to index their *originals* folder directly
without importing files, leaving the existing file and folder names unchanged. On the other hand
importing is an efficient way to add files, since PhotoPrism doesn't have to search your *originals*
folder to find new files.

### Can I use PhotoPrism to sort files into a configurable folder structure? ###

You have complete freedom in how you organize your originals. If you don't like the unique names and 
folders used by the import function, you can resort to external batch renaming tools, for example
[ExifTool](https://ninedegreesbelow.com/photography/exiftool-commands.html#rename),
[PhockUp](https://github.com/ivandokov/phockup),
or [Photo Organizer](https://www.systweak.com/photo-organizer).

Configurable import folders may be available in a later version. This is because - depending on the specific 
pattern - appropriate conflict resolution is required and the patterns must be well understood and validated 
to avoid typos or other misconfigurations that lead to undesired results for which we do not want to be responsible.

### Should I use an SD card or a USB stick? ###

Conventional USB sticks and SD cards are not suitable for long-term storage. Not only because of the 
performance, but also because they can lose data over time. Local [Solid-State Drives](performance.md#storage) 
(SSDs) are best, even when connected externally via USB 3. USB 1 and 2 devices will be slow either way.

### Is a Raspberry Pi fast enough? ###

This largely depends on your expectations and the number of files you have. Most users report that
PhotoPrism runs smoothly on their Raspberry Pi 4. However, initial indexing typically takes much longer
than on standard desktop computers.

Also keep in mind that the hardware has limited video transcoding capabilities, so the conversion of video
file formats is not well-supported and software transcoding is generally slow.

### Should I use SQLite, MariaDB, or MySQL? ###

PhotoPrism is compatible with [SQLite 3](https://www.sqlite.org/) and [MariaDB 10.5.12+](https://mariadb.org/).
Older databases using the same dialect, such as MySQL 8, may work but are not officially supported.

If you have few pictures, concurrent users, and CPU cores, [SQLite](https://www.sqlite.org/)
may seem faster compared to full-featured database servers like [MariaDB](https://mariadb.com/).

This changes as the index grows and the number of concurrent accesses increases.
The way MariaDB and MySQL handle multiple queries is completely different and optimized
for high concurrency. SQLite, for example, locks the index on updates so that other
operations have to wait. In the worst case, this can lead to timeout errors.
Its main advantage is that you don't need to run a separate database server.
This can be very useful for testing and also works great if you only have a few
thousand files to index.

MariaDB lacks some features that [MySQL Enterprise Edition](https://www.mysql.com/products/enterprise/) offers.
On the other hand, MariaDB has many optimizations. It is also completely open-source.

### Why is only the logo displayed when I open the app? ###

This may happen when the server cannot be reached, for example, because a proxy is misconfigured,
JavaScript is disabled in your browser, an ad blocker is blocking requests, or you are using an incompatible browser.

We recommend going through the [checklist provided](troubleshooting.md#app-not-loading) and to verify that
your browser meets the [system requirements](index.md#system-requirements).

### Why is PhotoPrism getting stuck in a restart loop? ###

This happens when Docker was configured to automatically restart services after failures.

We recommend going through the [checklist for fatal server errors](troubleshooting.md#fatal-server-errors) and to verify that
your computer meets the [system requirements](index.md#system-requirements).

### Can I install PhotoPrism in a sub-directory on a shared domain?

This is possible with our latest release if you run it behind a proxy.
Note that for a Progressive Web App (PWA) to work as designed, the service worker should
be located in the root directory. Also keep in mind sharing a domain with
other apps may negatively impact the performance and
[security](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)
of all apps installed. The length of share links increases as well.

### I could not find a documentation of config parameters? ###

We maintain a complete list of [config options](config-options.md) in *Getting Started*.
When you run `photoprism help` in a [terminal](docker-compose.md#command-line-interface), 
all commands and parameters available in your currently installed [version](https://docs.photoprism.app/release-notes/) 
are listed:

```
docker-compose exec photoprism photoprism help
```

Our [Docker Compose](docker-compose.md) [examples](https://dl.photoprism.app/docker/) are continuously 
updated and inline documentation has been added to simplify installation.

### What exactly does the read-only mode? ###

When you enable *read-only mode*, all features that require write permission to the *originals* folder
are disabled, in particular import, upload, and delete. Set `PHOTOPRISM_READONLY` to `"true"`
in `docker-compose.yml` for this. You can mount a folder with the `:ro` flag to make Docker block
write operations as well.

### How can I uninstall PhotoPrism? ###

This depends on how you installed it. If you're running PhotoPrism with [Docker Compose](docker-compose.md), 
this command will stop and remove the Docker container:

```
docker-compose rm -s -v
```

Please refer to the official Docker [documentation](https://docs.docker.com/compose/reference/rm/) 
for further details.

### How can I mount network shares with Docker? ###

There are multiple ways of using network storage. One of the easiest might be to directly mount NFS shares with Docker.

You can mount any number of NFS shares as folders. Follow this `docker-compose.yml` example 
if you want to mount the *originals* folder as a share:

```yaml
services:
  photoprism:
    # ...
    volumes:
      # Map originals folder to NFS:
      - "photoprism-originals:/photoprism/originals"     

volumes:
  photoprism-originals:
    driver: local
    driver_opts:
      type: nfs
      # The IP of your NAS:
      o: "username=user,password=secret,addr=1.2.3.4,soft,rw"
      # Share path on your NAS:
      device: ":/mnt/photos" 
```

For Windows / CIFS shares:

```yaml
volumes:
  photoprism-originals:
    driver: local
    driver_opts:
      type: cifs
      o: "username=user,password=secret,rw"
      device: "//host/folder"
```

!!! info 
    This was tested with TrueNAS and NFS, but other (network) file systems may be mounted with Docker as well.

!!! tip 
    Mounting the *import* folder to a share which is also accessible via other ways (e.g. CIFS)
    is especially handy, as you can dump all data from a SD card / camera directly into that folder 
    and trigger the index in the GUI afterwards. So you can skip the upload dialog in the 
    GUI and it's a little faster.

### Why are you using Docker, isn't it pretty new and complicated? ###

Containers are nothing new; [Solaris Zones](https://en.wikipedia.org/wiki/Solaris_Containers) have been around for
about 15 years, first released publicly in 2004. The chroot system call was introduced during
[development of Version 7 Unix in 1979](https://en.wikipedia.org/wiki/Chroot). It is used ever since for hosting
applications exposed to the public Internet.

Modern Linux containers are an incremental improvement. A main advantage of Docker is that application images
can be easily made available to users via Internet. It provides a common standard across most operating
systems and devices, which saves our team a lot of time that we can then spend more effectively, for example,
providing support and developing one of the many features that users are waiting for.

Human-readable and versioned Dockerfiles as part of our public source code also help avoid surprises and
"works for me" moments by enabling us to have the exact same environment everywhere in development and production.

Last but not least, virtually all file format parsers have vulnerabilities that just haven't been discovered yet.
This is a known risk that can affect you even if your computer is not directly connected to the Internet.
Running apps in a container with limited host access is an easy way to improve security without
compromising performance and usability.

!!! tldr ""
    A virtual machine running its own operating system provides more security, but typically has side effects 
    such as lower performance and more difficult handling. Note that you can also run Docker in a VM to get the 
    best of both worlds.

### I'm using an operating system without Docker support. How to install and use PhotoPrism without Docker? ###

You can build and install PhotoPrism from the publicly available [source code](../developer-guide/setup.md):

```bash
git clone https://github.com/photoprism/photoprism.git
cd photoprism
make all install
```

If build dependencies are missing, you must install them manually as shown in our development 
[Dockerfile](https://github.com/photoprism/photoprism/blob/develop/docker/development/Dockerfile).
You often don't need to use the exact same versions, so it's possible replace packages with what is available 
in your environment.

Note we don't have the resources to provide private users with dependencies and TensorFlow libraries for their personal environments.
We therefore recommend learning Docker if your operating system supports it. Docker vastly simplifies installation and 
upgrades. It saves our team a lot of time that we can then spend more effectively, see previous question.

!!! tldr ""
    Everyone is invited to contribute by building & testing native packages for Linux distributions and other 
    operating systems! 💐

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

There is no single sign-on support yet as we didn't consider it essential for our initial release.
Our team is currently working on [OpenID Connect](https://github.com/photoprism/photoprism/issues/782),
which will be available in a future release.

### PhotoPrism is really terrible, can I tell you how bad it is? ###

If you are [having a bad day](https://photoprism.app/code-of-conduct) and want to offend someone,
please go somewhere else.

!!! info
    Our development and testing efforts are focused on small servers and home users. Adding functionality
    that is primarily useful for business environments, or that only benefits few private 
    users with special needs, diverts resources away from features that benefit everyone.
    Professional users are welcome to [reach out](../contact.md) to us for a custom solution.
