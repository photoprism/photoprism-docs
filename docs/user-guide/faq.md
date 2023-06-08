# Frequently Asked Questions

## General ##

??? question "Does your software depend on any external services?"

    As explained in our [Privacy Policy](https://www.photoprism.app/privacy#section-7), reverse geocoding and interactive world maps depend on retrieving the necessary information [from us](https://www.photoprism.app/contact) and [MapTiler AG](https://www.maptiler.com/contacts/), headquartered in Switzerland. Both services are provided with a very high level of privacy and confidentiality.
    
    Your use of these services is [fully covered by us](../getting-started/faq.md#are-the-keys-for-using-interactive-world-maps-provided-free-of-charge). Depending on your usage, this can save you much more than the cost of a [PhotoPrism+ Membership](https://www.photoprism.app/membership), since other providers generally charge usage-based fees and may also not allow you to cache the data they provide, compromising your privacy with unnecessary requests.

    [View Privacy Policy ›](https://www.photoprism.app/privacy#section-7){ class="pr-3" } [View Compliance FAQ ›](https://www.photoprism.app/kb/compliance-faq#privacy)

    In order to successfully set up your installation and view location details in PhotoPrism, you must [allow incoming requests as well as those to our Geocoding API and Docker](../getting-started/troubleshooting/firewall.md) if you have a firewall installed, and make sure that your Internet connection is working:

    [![](https://dl.photoprism.app/img/diagrams/proxy-cdn.svg){ class="w100" }](../getting-started/troubleshooting/firewall.md)

??? question "Why are some features only available to members?"

    PhotoPrism is **100% self-funded and independent**. Voluntary donations do not cover the cost of a team working full time to provide you with updates, documentation, and support. It is your decision whether you want to sign up to enjoy additional benefits.

    [View Membership FAQ ›](https://www.photoprism.app/membership/faq)

??? question "What are the advantages of purchasing a commercial license?"

    A key difference between the [public license](https://docs.photoprism.app/license/agpl/) and a [commercial license agreement](https://www.photoprism.app/teams) is that you get access to additional support and configuration options, as well as the right to customize functionality to your needs without having to publicly disclose your changes. Our [Compliance FAQ](https://www.photoprism.app/kb/compliance-faq) gives answers to the most frequently asked questions about product compliance and scalability.

    [Compare Team Editions ›](https://www.photoprism.app/teams#compare)

??? question "When exactly will new features be released?"
    
    Our [Project Roadmap](https://link.photoprism.app/roadmap) shows what tasks are in progress and what features will be implemented next. You may give ideas you like a thumbs-up, so we know what's most popular.

    Be aware that we have a zero-bug policy and do our best to help users when they need support or have other questions. This comes at a price though, as we can't give exact release dates for new features. Our team receives many more requests than can be implemented, so we want to emphasize that we are in no way obligated to implement the features, enhancements, or other changes you request. We do, however, appreciate your feedback and carefully consider all requests.

    **Since [sustained funding](https://www.photoprism.app/oss/faq) is key to quickly releasing new features, we encourage all users to support our mission by [signing up as a member](https://www.photoprism.app/membership) or purchasing a [commercial license](https://www.photoprism.app/teams).**

## Membership ##

??? question "How can I activate my membership?"

    To connect a new instance to your membership account, you will need to log in with the admin user that is automatically created during setup (see your `docker-compose.yml` file or the app store documentation), and then follow the steps described in our activation guide.
    
    [View Activation Guide ›](https://www.photoprism.app/kb/activation)

??? question "Are there alternatives to a recurring subscription?"

    Yes, our Plus members automatically receive a free lifetime Essentials membership after 24 months. Likewise, Silver members receive a lifetime Plus membership after 24 months, Gold members after 12 months, and Platinum members after only 6 months.

    If you would like to sign up for a Silver, Gold or Platinum membership, you can do so either [directly on our website](https://my.photoprism.app/register) or [on Patreon](https://link.photoprism.app/patreon). In addition, we are working on a Plus Feature Pack that includes just the features without support, so we can offer it to you at a lower price.

    Note that as a lifetime member you will always receive updates and support for your personal use from us, unlike with so-called "lifetime" licenses, which may only be good until the next major version is released.
 
    [View Membership FAQ ›](https://www.photoprism.app/membership/faq) [Sign Up ›](https://link.photoprism.app/membership)

??? question "What happens if I cancel my membership?"

    If you are eligible for a lifetime Essentials or Plus membership, you can continue to use these features even if you decide to stop supporting us. Otherwise, you can continue to use all the freely available features. In no case will you lose access to your pictures.

    [Compare Features ›](https://www.photoprism.app/editions#compare)

## User Interface ##

??? question "Can I select multiple pictures at once?"

    Yes, this is possible. How it works depends on what kind of device you use.

    **Desktop Browser**
    
    Select the first picture by clicking :material-checkbox-blank-circle-outline: in the lower right corner.
    
    The user interface is now in selection mode:

    - to additionally select individual pictures, click them anywhere except on the play/view icons in the corner
    - to select multiple pictures at once, use a shift+click to select all pictures between the last selected picture and the one you shift+click

    **Mobile Devices**

    Select the first picture with a long touch.
    
    The user interface is now in selection mode:

    - to additionally select individual pictures, touch them anywhere except on the play/view icons in the corner
    - to select multiple pictures at once, use a long touch to select all pictures between the last selected picture and the one you long touch

??? question "Can I use trees for organizing my pictures and albums?"

    Except in *Library > Originals* and for object classification in *Labels*, PhotoPrism does not
    support hierarchically organized content for a number of reasons:
    
    First, there are many tools (including Windows Explorer and Mac OS Finder) that already browse folders in such a way.
    
    A common UX challenge is dealing with namespaces.
    For example, the album "Berlin" may exist 5 times in different parts of a tree.
    To avoid ambiguities, simple input fields need to be replaced with a tree browser that
    shows the complete context.
    This is especially difficult on mobile screens.
    
    Personal albums can typically be browsed by time, with optional filters for more specific results.
    This is different in Enterprise asset management, where trees are required to manage
    responsibilities & [permissions](https://github.com/photoprism/photoprism/issues/455#issuecomment-675859270).
    We might do a special release for professional users later.
    
    While you have complete freedom with organizing your original files and folders,
    we don't think trees should be an integral part of our user interface.
    Most users won't be able to sort their memories in a strictly hierarchical way
    and prefer to explore them in multiple dimensions instead.

## Maps & Places ##

??? question "Why are the streets on the Places map no longer loading?"

    The high-quality maps have been a paid feature for a long time, but were still available for testing. Since many users didn't realize this and simply used the commercial maps for free, this was [recently changed](https://github.com/photoprism/photoprism/issues/2998). Please see the [feature comparison on our website](https://www.photoprism.app/editions#compare) for reference. 

    [Compare Memberships ›](https://www.photoprism.app/editions#compare)

??? question "Why are some pictures positioned at unvisited locations on the map?"

    PhotoPrism can estimate the location of pictures taken without GPS information by extrapolating it from the location of other pictures taken on the same day. These estimates can be [disabled in the settings](./settings/library.md) if you don't want them.

## Media Library ##

??? question "What media file types are supported?"

    PhotoPrism supports indexing, viewing, and [converting](settings/library.md) most popular image, video and RAW formats, including JPEG, PNG, GIF, BMP, HEIF, HEIC, MP4, MOV, WebP, and WebM. 
    [TIFF is partially supported](https://github.com/golang/go/issues?q=is%3Aissue+image%2Ftiff+)
    without extensions like GeoTIFF.

    When indexing, a JPEG or PNG sidecar file is automatically created for videos and images in other formats, such as RAW or vector graphics. It is needed for thumbnail generation, image classification, and face detection. JPEG XL support is planned as soon as it is generally available and enough compatible tools exist.
    
    If installed, converting RAW files is possible with the following converters (our Docker image includes both):

    - [Darktable](https://www.darktable.org/) ([supported cameras](https://www.darktable.org/resources/camera-support/))
    - [RawTherapee](https://rawtherapee.com/) ([supported cameras](https://www.libraw.org/supported-cameras))

    On a Mac, RAW files can also be converted with [Sips](https://ss64.com/osx/sips.html) ([supported cameras](https://support.apple.com/en-us/HT211241)).
    Our goal is to provide top-notch support for all RAW formats, regardless of camera make and model.
    Please let us know about any issues with a particular camera or file format.

    For maximum browser compatibility, [video codecs and containers](../developer-guide/media/index.md) supported by [FFmpeg](https://en.wikipedia.org/wiki/FFmpeg#Supported_codecs_and_formats) can be transcoded to [MPEG-4 AVC](https://en.wikipedia.org/wiki/Advanced_Video_Coding) on demand, just as still images can be extracted for thumbnail creation.
    
    Make sure you have JSON sidecar files enabled if you have videos, live photos, and/or [animated GIFs](https://github.com/photoprism/photoprism/issues/590) so that video-specific metadata such as codec, frames, and duration can be extracted, indexed, and searched.

    For a complete list of file formats and extensions, see our downloadable [Feature Overview](https://link.photoprism.app/overview).

??? question "What metadata sidecar file types are supported?"

    Currently, three types of [file formats](../developer-guide/media/index.md) are supported:
    
    #### JSON ####
    
    If not disabled via `PHOTOPRISM_DISABLE_EXIFTOOL` or `--disable-exiftool`, [Exiftool](https://exiftool.org/) is used
    to automatically create a JSON sidecar for each media file. **In this way, embedded XMP and video metadata can also be indexed.**
    Native metadata extraction is limited to common Exif headers. Note that this causes small amount of overhead when
    indexing for the first time.
    
    JSON files can also be useful for debugging, as they contain the full metadata and can be processed with common
    development tools and text editors.
    
    *Metadata JSON files exported from Google Photos can be read as well. Support for more schemas may be added over time.*
    
    #### YAML ####
    
    Unless disabled via `PHOTOPRISM_DISABLE_BACKUPS` or `--disable-backups`, PhotoPrism automatically creates/updates
    [human-friendly YAML sidecar files](../developer-guide/technologies/yaml.md) during indexing and after manual
    editing of fields such as title, date, or location. They serve as a backup in case the database (index) is lost,
    or when folders are synchronized with a remote instance.
    
    Like JSON, [YAML](../developer-guide/technologies/yaml.md) files can be opened with common development tools and
    text editors. However, changes are not synchronized with the original index, as this could overwrite existing data.
    
    #### XMP ####
    
    XMP (Extensible Metadata Platform) is an XML-based metadata container format [developed by Adobe](https://www.adobe.com/products/xmp.html).
    It provides many more fields (as part of embedded models like Dublin Core) than Exif. This also makes it difficult - if not
    impossible - to provide full support. Reading title, copyright, artist, and description from XMP sidecar files is
    implemented as a proof-of-concept, [contributions are welcome](../developer-guide/metadata/xmp.md). Indexing of
    embedded XMP is only possible via Exiftool, see above.

??? question "Why are my video files not indexed?"

    In case [FFmpeg is disabled](settings/advanced.md#disable-ffmpeg) or not installed, videos cannot be indexed because still images cannot be created.
    You should also have [Exiftool enabled](../getting-started/config-options.md#feature-flags) to extract metadata such as duration, resolution, and codec.

??? question "Are JPEGs updated when RAW or XMP files change?"

    JPEGs are currently not regenerated when related RAW or XMP files change. RAW files are digital negatives by design. PhotoPrism therefore assumes that their image information is immutable.

    XMP files can affect the appearance, but most of the metadata they contain, such as title and description, does not. Creating JPEGs from RAW files is a time-consuming task, and in most cases would cause a huge, unjustified amount of overhead. In addition, the rendering information in XMP files is not well standardized. For example, changes you make in Photoshop may not be compatible with Darktable.

    We recommend manually updating existing JPEG sidecar files as needed or creating additional JPEGs, so you can choose between different versions. New files and other metadata changes are detected and reflected in the index as usual when your library is scanned.

??? question "Some files seem hidden, where are they?"

    If the [quality filter](organize/review.md) is enabled, you might find them in *Photos > Review*. Otherwise, their
    format may not be supported, they may be corrupted, or they may be stacked with other files if their name,
    exact date & location, or unique image ID indicate they belong to the same photo. You may then unstack
    them if this happened by mistake e.g. because of bad metadata.

    [View Troubleshooting Checklist ›](../getting-started/troubleshooting/index.md#missing-pictures)

??? question "For what reasons can files be stacked?"

    1. Files sharing exactly the same file and folder name will always be stacked, for example `/2018/IMG_1234.jpg` and `/2018/IMG_1234.avi`
    2. Files with related, sequential names like `/2018/IMG_1234 (2).jpg` and `/2018/IMG_1234 (3).jpg` may be stacked as well (optional)
    3. Pictures were taken at the same GPS position and second (optional)
    4. Image metadata contains the same *Unique Image ID* or *XMP Instance ID* (optional)

    You can change the behaviour for 2 - 4 in [*Settings*](settings/library.md).
    
    Note that already stacked files are not automatically unstacked when you change the stacking settings.

??? question "I already indexed some files. Why are Folders, Calendar and Moments still empty?"

    Folders, Calendar and Moments are populated at the end of the indexing process.

??? question "Why does the count in *Search* not match the count of files in *Originals*?"

    *Library > Originals* shows actual files, whereas *Search* counts unique photos and videos.

    Photos and videos may have more than one file, for example:

    * A raw file + related jpg file + related xmp file = 3 files, 1 photo
    * A mp4 file + related jpg file = 2 files, 1 video

    It is also possible that multiple .jpg files are stacked because they are related to each other.

??? question "When should I perform a complete rescan?"

    We recommend performing a [complete rescan](library/originals.md#when-should-complete-rescan-be-selected) after major updates to take advantage of new search filters and sorting options. Be sure to [read the notes for each release](../release-notes.md) to see what changes have been made and if they might affect your library, for example, because of the file types you have or because new search features have been added. If you encounter problems that you cannot solve otherwise (i.e. before reporting a bug), please also try a rescan and see if it solves the problem.
    
    You can start a [rescan from the user interface](library/originals.md) by navigating to *Library* > *Index*, selecting "Complete Rescan", and then clicking "Start". Manually entered information such as labels, people, titles or descriptions will not be modified when indexing, even if you perform a "complete rescan". Be careful not to start multiple indexing processes at the same time, as this will lead to a high server load.

??? question "Can I use the web interface to permanently delete files?"

    Yes, you can [permanently delete](./organize/delete.md) files.

??? question "In which cases could files in the originals folder get modified?"

    PhotoPrism generally does not write to the *originals* folder, with the following exceptions: (1) You rotate an image in the user interface, so its Exif header must be updated. (2) You unstack files that were stacked based on their name, so they must be renamed. (3) You add files using the import functionality or the web upload. (4) You manually delete files in the user interface. (5) You have configured the *originals* folder as your sidecar folder. (6) You access the *originals* folder with a WebDAV client to manage your files without having *read-only mode* enabled.

## Metadata ##

??? question "Windows shows different metadata values. Could this be a bug in PhotoPrism?"

    We recommend that you use [Exiftool](https://exiftool.org/install.html) to see all metadata fields and values, as Windows has limited functionality.
    
    It might then become clear why there are differences. For example, it could be that Windows does not support some fields and therefore ignores them, or that the data shown is actually from the file system and not from the files. Should you still believe to have found a bug, please [provide us with sample files](https://www.photoprism.app/contact#file-samples) so that we can reproduce the issue.

??? question "Why do some pictures have 08/12/2002 as date if they were not taken on that day?"
    
    This is usually caused by a [bug in Android](https://issuetracker.google.com/issues/36963276) that caused photos to be created with an incorrect CreateDate. While the date can easily be changed in the edit dialog, this only updates the index without modifying your originals.
    To fix the date directly in your image or video files, please use other applications like Photoshop, or Exiftool, and re-index your library.

??? question "Why do some pictures have an odd date like 01/01/1980?"

    This may happen in case there was an issue with your camera's settings when the photo was taken.
    While the date can easily be changed in the [edit dialog](organize/edit.md), this only updates the index
    without modifying your originals.
    
    To fix the date directly in your image or video files, please use other applications
    like Photoshop, or Exiftool, and re-index your library.

??? question "What's the difference between keywords and labels?"

    Keywords contain a list of search terms extracted from metadata, file names, and other sources
    like geodata. Pictures with matching keywords automatically show up in related *Labels*.

    Although related, keywords and labels serve different purposes:

    * **Labels** may have parent categories and are primarily used for classification, like "animal", "cat", or "boat". Duplicates and ambiguities should be avoided.

    * **Keywords** are primarily used for searching. They may include similar terms and translations, like "kitten", "kitty", and "cat".

## Live Photos ##

??? question "Why can't I play Live Photos or find stacks when I search for specific images?"

    Our search API and user interface perform a file search. This is intentional since "stacks" can contain files of different types and properties, such as color.
    
    For example, there may be color and monochrome versions. Now, when you search for them or sort them by color, the user interface must display individual files. Otherwise, the results showing a color image/video when you filter by monochrome would make no sense.
    
    Likewise, if you search for `filename.mp4.*`, you will find only JPEGs without video, because the video file extension is `.mp4` without an extra dot at the end.

    We recommend using the `path:` and/or `name:` filters with wildcards if searching for individual files limits the search results too much. Most users will want to find all related files so that they can be displayed together, e.g. as live photos consisting of a video and an image.
    
    You can combine these filters with other filters such as `live` to ensure that the results include only pictures with a specific media type. Alternatively, you can use the `filename:` filter with a more permissive wildcard that excludes the file extension.

## Thumbnails ##

??? question "Isn't it insecure that thumbnail image URLs work even if you are not logged in?"

    Like most commercial image hosting services, we've chosen to use a **cookie-free thumbnail API** to minimize request latency and avoid unnecessary network traffic. If you were to copy private session cookies and use them in a different browser window, you would have a similar problem, except that they also work for other API endpoints, not just a single image.

    Even if URLs were to become invalid every minute: Digital copies are as good as originals. Once shared and downloaded, such images should be considered "leaked" because they are cached and can be re-shared by the recipient at any time, with no sure way to get all copies back. Any form of protection we could provide would essentially be "snake oil", could be circumvented, and would have a negative impact on the user experience, such as disabling the browser cache or context menu.

    For the highest level of protection, it is recommended to shield your private server from the public Internet. Always use **HTTPS, a VPN and/or ideally TLS client certificates** and make sure that only people you trust have access to your instance.

    Visit [docs.photoprism.app/developer-guide/media/thumbnails/](https://docs.photoprism.app/developer-guide/media/thumbnails/) to learn more.

## WebDAV ##

??? question "Why do I get an error when trying to add a remote server for syncing?"

    When adding a new remote server, PhotoPrism tests a number of
    [common endpoints](https://raw.githubusercontent.com/photoprism/photoprism/develop/internal/remote/heuristic.go).
    Only when that fails, you'll see an error. There may be different reasons for this:

    - you are using HTTPS with an invalid certificate (not signed, outdated, domain doesn't match,...)
    - your server has permission issues, or an otherwise bad configuration. For example, Nextcloud blocks requests
    if the host doesn't match `trusted_domains` in its `config.php`
    - the IP is not reachable from your PhotoPrism instance due to network settings, or a firewall
    - the internal hostname can not be resolved to an IP address
    - it's the wrong host or port
    - username or password are wrong

    [Curl](https://curl.se/) is an excellent tool for
    [testing HTTP connections](https://code.blogs.iiidefix.net/posts/webdav-with-curl/) if you don't mind using a terminal:
    
    ```
    curl -X PROPFIND -H "Depth: 1" -u user:pass https://example.org/webdav/
    ```
    
    To avoid overlooking issues, it's best to run it from the same Docker container, virtual machine,
    or server environment where PhotoPrism is installed.

??? question "My file sync app fails with "unable to parse TLS packet headers" when trying to connect via WebDAV?"

    Because of security considerations, some backup tools and file sync apps like
    [FolderSync removed support for non-SSL HTTP communication](https://foldersync.io/docs/faq/#https-connection-errors).
    
    If you install PhotoPrism on a public server outside your home network, **always run it behind a secure
    HTTPS reverse proxy**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted 
    by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to 
    connect as well.

*[sidecar files]: additional files that sit next to a main file
