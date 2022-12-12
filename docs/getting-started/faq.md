# Frequently Asked Questions

### What media file types are supported?

PhotoPrism supports indexing, viewing, and [converting](../user-guide/settings/library.md) most popular image, video and RAW formats, including JPEG, PNG, GIF, BMP, HEIF, HEIC, MP4, MOV, WebP, and WebM. [TIFF is partially supported](https://github.com/golang/go/issues?q=is%3Aissue+image%2Ftiff+) without extensions such as GeoTIFF.

The internally used image format is JPEG. When indexing, a JPEG sidecar file can be created automatically for videos and images in other formats. It is needed for thumbnail generation, image classification, and face detection. JPEG XL support is planned as soon as it is generally available and enough compatible tools exist.

If installed, converting RAW files is possible with the following converters (our Docker image includes both):

- [Darktable](https://www.darktable.org/) ([supported cameras](https://www.darktable.org/resources/camera-support/))
- [RawTherapee](https://rawtherapee.com/) ([supported cameras](https://www.libraw.org/supported-cameras))

On a Mac, RAW files can also be converted with [Sips](https://ss64.com/osx/sips.html) ([supported cameras](https://support.apple.com/en-us/HT211241)).
Our goal is to provide top-notch support for all RAW formats, regardless of camera make and model.
Please let us know about any issues with a particular camera or file format.

For maximum browser compatibility, [video codecs and containers](../developer-guide/media/index.md) supported by [FFmpeg](https://en.wikipedia.org/wiki/FFmpeg#Supported_codecs_and_formats) can be transcoded to [MPEG-4 AVC](https://en.wikipedia.org/wiki/Advanced_Video_Coding) on demand, just as still images can be extracted for thumbnail creation.

Make sure you have JSON sidecar files enabled if you have videos, live photos, and/or [animated GIFs](https://github.com/photoprism/photoprism/issues/590) so that video-specific metadata such as codec, frames, and duration can be extracted, indexed, and searched.

For a complete list of file formats and extensions, see our downloadable [Feature Overview](https://link.photoprism.app/overview).

!!! tldr ""
    In case [FFmpeg is disabled](config-options.md#feature-flags) or not installed, videos cannot be indexed because still images cannot be created.
    You should also have [Exiftool enabled](config-options.md#feature-flags) to extract metadata such as duration, resolution, and codec.

### What are sidecar files and where do I find them?

A sidecar is a file that sits next to your main photo or video files and usually has the same name
but a different extension:

 * `IMG_0123.mov`
 * `IMG_0123.mov.jpg`
 * `IMG_0123.json`

New sidecar files are created in the *storage* folder by default, so the *originals* folder can be mounted read-only.

!!! tldr ""
    Even if `PHOTOPRISM_DISABLE_EXIFTOOL` and `PHOTOPRISM_DISABLE_BACKUPS` are set to `"true"`,
    the indexer looks for existing sidecar files and uses them.

### What metadata sidecar file types are supported?

Currently, three types of [file formats](../developer-guide/media/index.md) are supported:

#### JSON ####

If not disabled via `PHOTOPRISM_DISABLE_EXIFTOOL` or `--disable-exiftool`, [Exiftool](https://exiftool.org/) is used
to automatically create a JSON sidecar for each media file. **In this way, embedded XMP and video metadata can also be indexed.**
Native metadata extraction is limited to common Exif headers. Note that this causes small amount of overhead when
indexing for the first time.

JSON files can also be useful for debugging, as they contain the full metadata and can be processed with common 
development tools and text editors.

!!! info ""
    JSON files exported from Google Photos can be read as well. Support for more schemas may be added over time.

#### YAML ####

Unless disabled via `PHOTOPRISM_DISABLE_BACKUPS` or `--disable-backups`, PhotoPrism automatically creates/updates
[human-friendly YAML sidecar files](../developer-guide/technologies/yaml.md) during indexing and after manual editing
of fields such as title, date, or location. They serve as a backup in case the database (index) is lost, or when
folders are synchronized with a remote instance.

Like JSON, [YAML](../developer-guide/technologies/yaml.md) files can be opened with common development tools and 
text editors. However, changes are not synchronized with the original index, as this could overwrite existing data.

#### XMP ####

XMP (Extensible Metadata Platform) is an XML-based metadata container format [developed by Adobe](https://www.adobe.com/products/xmp.html).
It provides many more fields (as part of embedded models like Dublin Core) than Exif. This also makes it difficult - if not 
impossible - to provide full support. Reading title, copyright, artist, and description from XMP sidecar files is 
implemented as a proof-of-concept, [contributions are welcome](../developer-guide/metadata/xmp.md). Indexing of 
embedded XMP is only possible via Exiftool, see above.

### Does your software depend on any external services?

As explained in our [Privacy Policy](https://photoprism.app/privacy#section-7), reverse geocoding and interactive world maps depend on retrieving the necessary information [from us](https://photoprism.app/contact) and [MapTiler AG](https://www.maptiler.com/contacts/), headquartered in Switzerland. Both services are provided with a very high level of privacy and confidentiality.

Your use of these services is [fully covered by us](#are-the-keys-for-using-interactive-world-maps-provided-free-of-charge). Depending on your usage, this can save you much more than the cost of a [PhotoPrism+ Membership](https://photoprism.app/membership), since other providers generally charge usage-based fees and may also not allow you to cache the data they provide, compromising your privacy with unnecessary requests.

In order to use the maps and view location details in PhotoPrism, as well as successfully run our test suite as a developer, you must **allow requests to these API endpoints** if you have a firewall installed and make sure your Internet connection is working.

Should you wish to operate one or both of these services on your own premises, we can set up such a [fully autonomous solution](https://photoprism.app/kb/compliance-faq#fully-autonomous-solution) for you, provided you are prepared to cover the initial setup costs as well as ongoing maintenance fees for content licenses and updates.

[View Privacy Policy ›](https://photoprism.app/privacy#section-7){ class="pr-3" } [View Compliance FAQ ›](https://photoprism.app/kb/compliance-faq#privacy)

### Why do I see connection errors when requesting API keys at startup?

As explained above, reverse geocoding and interactive world maps depend on retrieving the necessary information from external services. Please make sure that you allow requests to these API endpoints if you have a firewall installed, and verify that your Internet connection is working.

### Are the keys for using interactive world maps provided free of charge?

The API keys required to use the maps are unfortunately not free for us due to the number of users we have. Those costs are one of the reasons why we encourage all users to support our mission by [signing up as a sponsor](https://photoprism.app/membership) or purchasing a [commercial license](https://photoprism.app/teams).

While we could register several "non-commercial test accounts" instead, we don't think that would be fair and [Maptiler](https://www.maptiler.com/) might then stop offering them to those in need.

[Compare Personal Editions ›](https://photoprism.app/editions#compare)

### What are the advantages of purchasing a commercial license?

A key difference between the [public license](https://docs.photoprism.app/license/agpl/) and a [commercial license agreement](https://photoprism.app/teams) is that you get access to additional support and configuration options, as well as the right to customize functionality to your needs without having to publicly disclose your changes. Our [Compliance FAQ](https://photoprism.app/kb/compliance-faq) gives answers to the most frequently asked questions about product compliance and scalability.

[Compare Team Editions ›](https://photoprism.app/teams#compare)

### Will the self-hosted version continue to be supported?

Absolutely! We are on a mission to protect your freedom and privacy. Self-hosting is the easiest way to stay in control and protect [your privacy](https://photoprism.app/privacy). It also provides the best experience for advanced users who often rely on a local toolchain to select, edit, and publish their pictures.

At the same time, we know there's a huge demand and many practical uses for a cloud-hosted app that is easy to set up. We like to give our users the choice and therefore offer a fully managed service as a deployment option. Selected hosting partners ensure that your privacy is protected as much as technically possible, even in the cloud.

### Are JPEGs updated when RAW or XMP files change?

JPEGs are currently not regenerated when related RAW or XMP files change. RAW files are digital negatives by design.
PhotoPrism therefore assumes that their image information is immutable.

XMP files can affect the appearance, but most of the metadata they contain, such as title and description, does not.
Creating JPEGs from RAW files is a time-consuming task, and in most cases would cause a huge, unjustified amount of
overhead. In addition, the rendering information in XMP files is not well standardized. For example, changes you make
in Photoshop may not be compatible with Darktable.

We recommend manually updating existing JPEG sidecar files as needed or creating additional JPEGs, so you can choose
between different versions. New files and other metadata changes are detected and reflected in the index as usual when
your library is scanned.

### Which folder will be indexed?

This depends on your environment and [configuration](config-options.md). While subfolders can be selected for indexing
in the UI, changing the *originals* base folder requires a restart for security reasons.

If you skip configuration and don't use one of our Docker images, PhotoPrism will attempt to find a photo library
by searching a [list of common folder names](https://github.com/photoprism/photoprism/blob/develop/pkg/fs/dirs.go)
such as `/photoprism/originals` and `~/Pictures`. It also searches for other resources such as external applications,
classification models, and frontend assets.

If you use our [Docker Compose](docker-compose.md) example without modifications, pictures will be
mounted from `~/Pictures` where `~` is a shortcut for your home directory:

- `\user\username` on Windows
- `/Users/username` on macOS
- and `/root` or `/home/username` on Linux

Since the app is running inside a container, you have to explicitly mount the host folders you want to use.
PhotoPrism won't be able to see folders that have not been mounted. Multiple folders can be made accessible
by mounting them as subfolders of `/photoprism/originals`, for example:

```yaml
volumes:
  - "/home/username/Pictures:/photoprism/originals"
  - "/example/friends:/photoprism/originals/friends"
  - "/mnt/photos:/photoprism/originals/media"
```

### How can I install PhotoPrism without Docker?

#### Building From Source ####

You can build and install PhotoPrism from the publicly available [source code](https://docs.photoprism.app/developer-guide/setup/):

```bash
git clone https://github.com/photoprism/photoprism.git
cd photoprism
make all install DESTDIR=/opt/photoprism
```

Missing build dependencies must be installed manually as shown in our human-readable and versioned
[Dockerfile](https://github.com/photoprism/photoprism/blob/develop/docker/develop/bookworm/Dockerfile). You often don't
need to use the exact same versions, so it's possible to replace packages with what is available in your environment.

Please note that we do not have the resources to provide private users with dependencies and
[TensorFlow libraries](https://dl.photoprism.app/tensorflow/) for their personal environments.
We recommend giving Docker a try if you use Linux as it saves developers a lot of time when building,
testing, and deploying complex applications like PhotoPrism. It also effectively helps avoid
"works for me" moments and missing dependencies, see [next question](#why-are-you-using-docker).

#### Installation Packages ####

An [unofficial port](https://docs.photoprism.app/getting-started/freebsd/) is available for FreeBSD / FreeNAS users.
Developers are invited to contribute by [building and testing standalone packages](https://docs.photoprism.app/developer-guide/)
for Linux distributions and other operating systems. 

Updates are [released several times a month](https://docs.photoprism.app/release-notes/), so maintaining the long list of dependencies for additional environments would currently consume too many of [our resources](https://docs.photoprism.app/funding/).

#### LXC Images ####

There is no official [LXC image](https://linuxcontainers.org/) available yet, see [related GitHub issue](https://github.com/photoprism/photoprism/issues/147) for details.

### Why are you using Docker?

Containers are nothing new; [Solaris Zones](https://en.wikipedia.org/wiki/Solaris_Containers) have been around for
about 15 years, first released publicly in 2004. The chroot system call was introduced during
[development of Version 7 Unix in 1979](https://en.wikipedia.org/wiki/Chroot). It is used ever since for hosting
applications exposed to the public Internet.

Modern Linux containers are an incremental enhancement. A main advantage of Docker is that application images
can be easily made available to users via Internet. It provides a common standard across most operating
systems and devices, which saves our team a lot of time that we can then spend [more effectively](../developer-guide/code-quality.md#effectiveness-efficiency), for example,
providing support and developing one of the many features that users are waiting for.

Human-readable and [versioned Dockerfiles as part of our public source code](https://github.com/photoprism/photoprism/tree/develop/docker)
also help avoid "works for me" moments and other unwelcome surprises by enabling teams to have the exact same environment everywhere in [development](https://github.com/photoprism/photoprism/blob/develop/docker/develop/bookworm/Dockerfile), staging,
and [production](https://github.com/photoprism/photoprism/blob/develop/docker/photoprism/bookworm/Dockerfile).

Last but not least, virtually all file format parsers have vulnerabilities that just haven't been discovered yet.
This is a known risk that can affect you even if your computer is not directly connected to the Internet.
Running apps in a container with limited host access is an easy way to improve security without
compromising performance and usability.

!!! tldr ""
    A virtual machine running its own operating system provides more security, but typically has side effects
    such as lower performance and more difficult handling. You can also run Docker in a VM to get the best of
    both worlds. It's essentially what happens when you run dockerized applications on [virtual cloud servers](cloud/digitalocean.md)
    and operating systems other than Linux.

### Should I use SQLite, MariaDB, or MySQL?

PhotoPrism is compatible with [SQLite 3](https://www.sqlite.org/) and [MariaDB 10.5.12+](https://mariadb.org/).
Official support for MySQL 8 is discontinued as Oracle seems to have stopped shipping [new features and enhancements](https://github.com/photoprism/photoprism/issues/1764).
As a result, the testing effort required before each release is no longer feasible.

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

### I've configured an external database, but can't connect?

Most often this happens when new users configure `localhost` or `127.0.0.1` as database server host, since these always point back to the current container or computer. So it is not possible to access an external service with such a hostname or an IP address starting with 127. It works only if it is used directly in the container or on the computer where the database server is running. Instead, you must use a hostname or IP address that is accessible from other machines and containers.

### Why does PhotoPrism always consume 100% of CPU when the background worker is running?

Many users reporting poor performance and high CPU load have migrated from SQLite to MariaDB so that [their database schema is not optimized for performance](advanced/databases.md), for example, because indexes are missing or columns have the wrong data type. The [instructions for these migrations](advanced/migrations/sqlite-to-mariadb.md) were provided by a contributor and are not part of the original software distribution. As such, they have not been officially released, recommended, or extensively tested by us.

In some instances, users have manually changed the contents of the database. It is also possible that the database is in an inconsistent state for other reasons, e.g. due to bugs in previous versions that have been fixed in the meantime. However, we are not currently aware of any such cases.

Due to the amount of time required to review each report, we can only offer this to [eligible sponsors](https://photoprism.app/membership) and [business customers](https://photoprism.app/teams), and not to users who have chosen our free community edition.

[Get Performance Tips ›](troubleshooting/performance.md#mariadb){ class="pr-3" } [View Database Schema ›](../developer-guide/database/index.md)

### Can you improve performance when using older or otherwise slow hardware?

It is a known issue that the user interface and backend operations, especially face recognition, can be slow or even crash on older hardware due to a lack of resources. Like most applications, PhotoPrism has certain requirements and our development process does not include testing on unsupported or unusual hardware.

In many cases, performance can be improved through optimizations. Since these can prove to be very time-consuming and cost-intensive in practice, users and developers must decide on a case-by-case basis whether this provides sufficient benefit in relation to the costs or whether the use of more powerful hardware is faster and cheaper overall.

We kindly ask you not to open a problem report on GitHub Issues for poor performance on older hardware until a full cause and feasibility analysis has been performed. [GitHub Discussions](https://github.com/photoprism/photoprism/discussions) or any of our other public forums and communities are great places to start a discussion.

That being said, one of the advantages of [open-source software](https://docs.photoprism.app/developer-guide/) is that users can submit [pull requests](https://docs.photoprism.app/developer-guide/pull-requests/) with performance and other enhancements they would like to see implemented. This will result in a much faster solution than waiting for a core team member to remotely analyze your problem and then provide a fix.

### Is a Raspberry Pi fast enough?

This largely depends on your expectations and the number of files you have. Most users report that
PhotoPrism runs smoothly on their Raspberry Pi 4. However, initial indexing typically takes much longer
than on standard desktop computers.

Also keep in mind that the hardware has limited video transcoding capabilities, so the conversion of video
[file formats](../developer-guide/media/index.md) is not well-supported and software transcoding is generally slow.

### Should I use an SD card or a USB stick?

Conventional USB sticks and SD cards are not suitable for long-term storage. Not only because of the
performance, but also because they can lose data over time. Local [Solid-State Drives](troubleshooting/performance.md#storage)
(SSDs) are best, even when connected externally via USB 3. USB 1 and 2 devices will be slow either way.

### Why don't you display animated GIFs natively?

Support for animated GIFs was [added in April 2022](https://github.com/photoprism/photoprism/issues/590).

### Why is my storage folder so large? What is in it?

The *storage* folder contains sidecar, cache, and configuration files. It may also contain index database files if you are [using SQLite](#should-i-use-sqlite-mariadb-or-mysql).

Most of the space is taken up by the thumbnails: These are high-quality, scaled-down versions of your originals. Thumbnails are necessary because web browsers are bad at [resizing large images to fit the screen](../user-guide/settings/advanced.md#downscaling-filter). Using full-resolution originals for slideshows and in search results would also consume a lot of browser memory and significantly reduce indexing performance.

We are working to implement storage optimizations whenever there is an opportunity. It is also possible to [increase the JPEG compression and/or limit the resolution](../user-guide/settings/advanced.md#images) if you are happy with lower quality thumbnails.

To free up as much space as possible, the most effective way is to delete all files in the `/cache/thumbnails` *storage* folder. It is located outside the *originals* folder by default, depending on [your configuration](config-options.md#storage). Then [perform a full rescan of your library](../user-guide/library/originals.md) or run the command `photoprism thumbs -f` [in a terminal](docker-compose.md#command-line-interface) if you have direct server access. This command can also be used to replace existing thumbnails, for example after changing the quality settings. Higher resolution thumbnails cannot be automatically removed at this time.

If you have a fast CPU and enough memory, you can [choose to render certain thumbnails only on demand](../user-guide/settings/advanced.md#images). However, storage is usually so cheap that most users opt for better quality and performance instead.

Actual storage requirements vary and depend, among other things, on file resolutions and formats (RAW, JPEG, video,...). For highly compressed, high-resolution videos in modern formats that cannot be displayed natively by browsers, the storage folder may even be larger than the originals, since [videos transcoded to AVC](../user-guide/organize/video.md#transcoding) are not as heavily compressed.

### Can I skip creating thumbnails completely?

The [smallest configurable size](../user-guide/settings/advanced.md#dynamic-and-static-size-limits) is 720px for [use by the indexer to perform color detection, image classification, as well as face detection and recognition](../user-guide/settings/advanced.md#what-files-will-be-created-by-photoprism). Recreating them every time they are needed is too demanding even for the most powerful servers. Unless you have just a few small pictures, this would make the app unusable.

!!! danger ""
    Reducing the *Static Size Limit* of thumbnails has a **significant impact on [face recognition](../user-guide/organize/people.md)
    and image classification** results. Simply put, it means that the indexer can no longer see properly.

### When should I perform a complete rescan?

We recommend performing a [complete rescan](../user-guide/library/originals.md#when-should-complete-rescan-be-selected) after major updates to take advantage of new search filters and sorting options. Be sure to [read the notes for each release](../release-notes.md) to see what changes have been made and if they might affect your library, for example, because of the file types you have or because new search features have been added. If you encounter problems that you cannot solve otherwise (i.e. before reporting a bug), please also try a rescan and see if it solves the problem.

You can start a [rescan from the user interface](../user-guide/library/originals.md) by navigating to *Library* > *Index*, selecting "Complete Rescan", and then clicking "Start". Manually entered information such as labels, people, titles or descriptions will not be modified when indexing, even if you perform a "complete rescan". Be careful not to start multiple indexing processes at the same time, as this will lead to a high server load.

### I'm having issues understanding the difference between the import and originals folders?

You may optionally mount an *import* folder from which files can be transferred to the *originals* folder
in a structured way that avoids duplicates. Imported files receive a canonical filename and will be
organized by year and month.

Most users with existing photo libraries will want to index their *originals* folder directly
without importing files, leaving the existing file and folder names unchanged. On the other hand
importing is an efficient way to add files, since PhotoPrism doesn't have to search your *originals*
folder to find new files.

### Can I use PhotoPrism to sort files into a configurable folder structure?

You have complete freedom in how you organize your originals. If you don't like the unique names and 
folders used by the import function, you can resort to external batch renaming tools, for example
[ExifTool](https://ninedegreesbelow.com/photography/exiftool-commands.html#rename),
[PhockUp](https://github.com/ivandokov/phockup),
or [Photo Organizer](https://www.systweak.com/photo-organizer).

Configurable import folders may be available in a later version. This is because - depending on the specific 
pattern - appropriate conflict resolution is required and the patterns must be well understood and validated 
to avoid typos or other misconfigurations that lead to undesired results for which we do not want to be responsible.

### Why is only the logo displayed when I open the app?

This may happen when the server cannot be reached, for example, because a proxy is misconfigured,
JavaScript is disabled in your browser, an ad blocker is blocking requests, or you are using an incompatible browser.

We recommend going through the [checklist provided](troubleshooting/index.md#app-not-loading) and to verify that
your browser meets the [system requirements](index.md#system-requirements).

### Why is PhotoPrism getting stuck in a restart loop?

This happens when Docker was configured to automatically restart services after failures.

We recommend going through the [checklist for fatal server errors](troubleshooting/index.md#fatal-server-errors) and to verify that
your computer meets the [system requirements](index.md#system-requirements).

### Can I install PhotoPrism in a sub-directory on a shared domain?

Setting up PhotoPrism behind a [reverse proxy](proxies/traefik.md) in a sub-directory on a shared domain is possible in principle. This method is experimental, however, and not generally recommended because a number of [detailed issues remain to be addressed](https://github.com/photoprism/photoprism/issues/2391) and technical expertise is required.

### I could not find a documentation of config parameters?

We maintain a complete list of [config options](config-options.md) in *Getting Started*.
When you run `photoprism help` in a [terminal](docker-compose.md#command-line-interface), 
all commands and parameters available in your currently installed [version](https://docs.photoprism.app/release-notes/) 
are listed:

```bash
docker compose exec photoprism photoprism help
```

Our [Docker Compose](docker-compose.md) [examples](https://dl.photoprism.app/docker/) are continuously 
updated and inline documentation has been added to simplify installation.

### What exactly does the read-only mode?

When you enable *read-only mode*, all features that require write permission to the *originals* folder
are disabled, for example import, upload, and delete. Set `PHOTOPRISM_READONLY` to `"true"`
in `docker-compose.yml` for this. You can [mount a folder with the `:ro` flag](https://docs.docker.com/compose/compose-file/compose-file-v3/#short-syntax-3) to make Docker block
write operations as well.

### How can I uninstall PhotoPrism?

This depends on how you installed it. If you're running PhotoPrism with [Docker Compose](docker-compose.md), 
this command will stop and remove the Docker container:

```bash
docker compose rm -s -v
```

Please refer to the official Docker [documentation](https://docs.docker.com/compose/reference/rm/) 
for further details.

### How can I mount network shares with Docker?

Shared folders that have already been mounted on your host can be mounted like any local drive or directory.
Alternatively, you can mount network storage with [Docker Compose](https://docs.docker.com/compose/compose-file/compose-file-v3/#driver_opts).
Please never store database files on an unreliable device such as a USB stick, SD card, or network drive.

**Unix / NFS**

Follow this `docker-compose.yml` example to mount Network File System (NFS) shares e.g. from Unix servers or NAS devices:

```yaml
services:
  photoprism:
    # ...
    volumes:
      # Map named volume "originals"
      # to "/photoprism/originals":
      - "originals:/photoprism/originals"     
  mariadb:
    # ...

# Specify named volumes:
volumes:
  originals:
    driver_opts:
      type: nfs
      # Authentication and other mounting options:
      o: "addr=1.2.3.4,username=user,password=secret,soft,rw,nfsvers=4"
      # Mount this path:
      device: ":/mnt/example"
```

`device` should contain the path to the share on the NFS server, note the `:` at the beginning. In the above example, the share can be mounted as the named volume `originals` in your `docker-compose.yml`.

Driver-specific options can be set after the server address in `o`, see the [nfs manual page](https://man7.org/linux/man-pages/man5/nfs.5.html). Here are some examples of commonly used options:

- `nfsvers=3` or `nfsvers=4` to specify the NFS version
- `nolock` (optional): Remote applications on the NFS server are not affected by lock files inside the Docker container (only other processes inside the container are affected by locks)
- `timeo=n` (optional, default 600): The NFS client waits `n` tenths of a second before retrying an NFS request
- `soft` (optional): The NFS client aborts an NFS request after `retrans=n` unsuccessful retries, otherwise it retries indefinitely
- `retrans=n` (optional, default 2): Sets the number of retries for NFS requests, only relevant when using `soft`

**SMB / CIFS**

Follow this `docker-compose.yml` example to mount [CIFS network shares](https://en.wikipedia.org/wiki/Server_Message_Block), e.g. **from Windows**, NAS devices or Linux servers with Samba:

```yaml
services:
  photoprism:
    # ...
    volumes:
      # Map named volume "originals"
      # to "/photoprism/originals":
      - "originals:/photoprism/originals"     
  mariadb:
    # ...

# Specify named volumes:
volumes:
  originals:
    driver_opts:
      type: cifs
      o: "username=user,password=secret,rw"
      device: "//host/folder"
```

Note that related values must start at the same indentation level in [YAML](../developer-guide/technologies/yaml.md) and that **tabs are not allowed for indentation**. We recommend using 2 spaces, but any number will do as long as it is consistent.

!!! tip ""
    Mounting the import folder from a network drive that can also be accessed via other ways (e.g. CIFS) is handy 
    because you can dump all data from an SD card/camera directly to this folder and then start the import process
    under [*Library* > *Import*](../user-guide/library/import.md). PhotoPrism also [has WebDAV support](../user-guide/sync/webdav.md)
    for remote file management and uploading, for example, through [PhotoSync](https://link.photoprism.app/photosync).

### Why does changing permissions using chmod does not work for my  network shares?
This is a common phenomenon with NFS shares. For security reasons, permissions must be changed on the server to take effect; unless the server allows them to be changed remotely, which depends on the settings. 
Even then, the actual permissions on the server and those effective on the clients may be different in the worst case.

### Do you support Podman?

Podman works just fine both in rootless and under root. Mind the SELinux which is enabled on 
Red Hat compatible systems, you may hit permission error problems. 

More details on how to run PhotoPrism with [Podman](https://podman.io/) on CentOS in 
[this blog post](https://lukas.zapletalovi.com/2020/01/deploy-photoprism-in-centos-80.html), 
it includes all the details including root and rootless modes, user mapping and SELinux.

### Any plans to add support for Active Directory, LDAP or other centralized account management options?

There is no single sign-on support yet as we didn't consider it essential for our initial release.
Our team is currently working on [OpenID Connect](https://github.com/photoprism/photoprism/issues/782),
which will be available in a future release.

### Your app is really terrible, can I tell you how bad it is?

Please take the time to read this documentation and [determine the cause of your problem](https://docs.photoprism.app/getting-started/troubleshooting/) before opening invalid bug reports, starting a public "shitstorm" or insulting other community members in our chat rooms. Aside from being annoying for everyone, it also keeps our team from working on features and enhancements that users like you are waiting for. Visit [photoprism.app/code-of-conduct](https://photoprism.app/code-of-conduct) to learn more.

!!! info "Professional Users"
    Our Community Edition is designed primarily for small servers and home users. Professional users are welcome
    to [contact us for a commercial solution](https://photoprism.app/contact).
