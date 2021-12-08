# Frequently Asked Questions

## User Interface ##

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

??? question "What's the difference between keywords and labels?"
      Keywords contain a list of search terms extracted from metadata, file names, and other sources
      like geodata. Pictures with matching keywords automatically show up in related *Labels*.

      Although related, keywords and labels serve different purposes:

      * **Labels** may have parent categories and are primarily used for classification, like "animal", "cat", or "boat".
      Duplicates and ambiguities should be avoided.

      * **Keywords** are primarily used for searching. They may include similar terms and translations,
      like "kitten", "kitty", and "cat".

??? question "Can I use the web interface to permanently delete files?"

    Yes, you can [permanently delete](./organize/delete.md) files.

## Library, Counts & Files ##

??? question "Which file types are supported?"

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

??? question "Some files seem hidden, where are they?"

    If the [quality filter](organize/review.md) is enabled, you might find them in *Photos > Review*. Otherwise, their
    format may not be supported, they may be corrupted, or they may be stacked with other files if their name,
    exact date & location, or unique image ID indicate they belong to the same photo. You may then unstack
    them if this happened by mistake e.g. because of bad metadata.

??? question "For what reasons can files be stacked?"

    1. Files sharing exactly the same file and folder name will always be stacked, for example `/2018/IMG_1234.jpg` and `/2018/IMG_1234.avi`
    2. Files with related, sequential names like `/2018/IMG_1234 (2).jpg` and `/2018/IMG_1234 (3).jpg` may be stacked as well (optional)
    3. Metadata suggests files have been taken at the same location and second (optional)
    4. File metadata contains the same *Unique Image ID* or *XMP Instance ID* (optional)

    You can change the behaviour for 2 - 4 in [*Settings*](settings/library.md).

??? question "I already indexed some files. Why are Folders, Calendar and Moments still empty?"

    Folders, Calendar and Moments are populated at the end of the indexing process.

??? question "Why does the count in *Search* not match the count of files in *Originals*?" 

    *Library > Originals* shows actual files, whereas *Search* counts unique photos and videos.

    Photos and videos may have more than one file, for example:

    * A raw file + related jpg file + related xmp file = 3 files, 1 photo
    * A mp4 file + related jpg file = 2 files, 1 video

    It is also possible that multiple .jpg files are stacked because they are related to each other.

??? question "Why is the count for *Originals* higher than the number of files physically existing in my originals directory?" 

    When indexing, an additional JPEG sidecar file may be created automatically for RAW, HEIF, TIFF, PNG, BMP, GIF, and video files.
    It is needed for generating thumbnails, image classification, and facial recognition.
    You can find it in `/storage/sidecar` by default, so your originals folder remains untouched. The file browser 
    in *Library > Originals* always displays it next to the original, independent of the physical storage location.

## Metadata ##

??? question "Why do some of my photos without geolocation information show a random location?"

    PhotoPrism estimates the location of photos without geolocation from photos that have been taken on the same day.
    You can disable estimations in [Settings](./settings/general.md).

??? question "Why do some pictures have an odd date like 01/01/1980?"

    This may happen in case there was an issue with your camera's settings when the photo was taken.
    While the date can easily be changed in the [edit dialog](organize/edit.md), this only updates the index
    without modifying your originals.
    
    To fix the date directly in your image or video files, please use other applications
    like Photoshop, or Exiftool, and re-index your library.

## WebDAV, Sync & Upload ##

??? question "Why do I get an error when trying to add a remote server for syncing?" 

    When adding a new remote server, PhotoPrism tests a number of
    [common endpoints](https://raw.githubusercontent.com/photoprism/photoprism/develop/internal/remote/heuristic.go).
    Only when that fails, you'll see an error. There may be different reasons for this:

    - You're using HTTPS with an invalid certificate (not signed, outdated, domain doesn't match,...).
    - Your server has permission issues, or an otherwise bad configuration. For example, Nextcloud blocks requests
    if the host doesn't match `trusted_domains` in its `config.php`.
    - The IP is not reachable from your PhotoPrism instance due to network settings, or a firewall.
    - The internal hostname can not be resolved to an IP address.
    - It's the wrong host or port.
    - Username or password are wrong.

    [Curl](https://curl.se/) is an excellent tool for
    [testing HTTP connections](https://code.blogs.iiidefix.net/posts/webdav-with-curl/) if you don't mind using a terminal:
    
    ```
    curl -X PROPFIND -H "Depth: 1" -u user:pass https://example.org/webdav/
    ```
    
    To avoid overlooking issues, it's best to run it from the same Docker container, virtual machine,
    or server environment where PhotoPrism is installed.

??? question "My file sync app fails with "unable to parse TLS packet headers" when trying to connect via WebDAV?"

    Because of security considerations, some backup tools and file sync apps like
    [FolderSync removed support for non-SSL HTTP communication](https://www.tacit.dk/foldersync/faq/#i-can-not-connect-to-a-non-https-webdav-server-why).
    
    If you install PhotoPrism on a public server outside your home network, please always run it behind a secure
    HTTPS reverse proxy. Your files and passwords will otherwise be transmitted in clear text and can be intercepted 
    by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to 
    connect as well.
