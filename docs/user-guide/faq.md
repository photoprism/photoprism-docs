# Frequently Asked Questions

### Can I use trees for organizing my pictures and albums? ###

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

### What's the difference between keywords and labels? ###

Keywords contain a list of search terms extracted from metadata, file names, and other sources 
like geodata. Pictures with matching keywords automatically show up in related *Labels*. 

Although related, keywords and labels serve different purposes:

* **Labels** may have parent categories and are primarily used for classification, like "animal", "cat", or "boat". 
  Duplicates and ambiguities should be avoided.
* **Keywords** are primarily used for searching. They may include similar terms and translations,
  like "kitten", "kitty", and "cat".

### Which file types are supported? ###

PhotoPrism's primary image file format is JPEG.
While indexing, a JPEG sidecar file may automatically be created for RAW, HEIF, TIFF, PNG, BMP, 
and GIF files. It is required for classification and resampling.

Support for specific RAW formats depends on the runtime environment and configuration. PhotoPrism may use 
[Darktable](https://www.darktable.org/) and [RawTherapee](https://rawtherapee.com/) for RAW to JPEG conversion. 
On Mac OS, [Sips](https://ss64.com/osx/sips.html) can be used as well.

We support all common video types.
You should configure PhotoPrism to automatically create JSON sidecar files so that
video metadata like location and duration can be indexed.

You're welcome to open an issue if you experience issues with a specific file format.

### Some files seem hidden, where are they? ###

If the [quality filter](organize/review.md) is enabled, you might find them in *Photos > Review*. Otherwise, their
format may not be supported, they may be corrupted, or they may be stacked with other files if their name, 
exact date & location, or unique image ID indicate they belong to the same photo. You may then unstack 
them if this happened by mistake e.g. because of bad metadata.

### Why are some files stacked? ###

Files with the same *XMP Instance ID* or *Unique Image ID* as well 
as images with the exact same time and location are stacked by default. These are considered identical, not sequences 
of related files based on their file names. You may disable this in [Settings](settings/library.md). Sidecar files are always going to be stacked as that's their purpose.

### Why do some pictures have an odd date like 01/01/1980? ###

This may happen in case there was an issue with your camera's settings when the photo was taken.
While the date can easily be changed in the [edit dialog](organize/edit.md), this only updates the index 
without modifying your originals.

To fix the date directly in your image or video files, please use other applications
like Photoshop, or Exiftool, and re-index your library.

### Can I use the web interface to permanently delete files? ###

Yes, [permanent deletion](./organize/delete.md) is available as early access feature for our sponsors.

### I already indexed some files. Why are Folders, Calendar and Moments still empty? ###

Folders, Calendar and Moments are populated at the end of the indexing process.

### Why does the count in *Search* not match the count of files in *Originals*? ###

The *Originals* section shows files, whereas the *Search* shows photos and videos. 

Photos and video can consist of multiple files:

* A raw file + related jpg file + related xmp file = 3 files but 1 photo
* A mp4 file + related jpg file = 2 files but 1 video

It is also possible that multiple .jpg files are stacked because they are related to each other.
  
### Why is the count for *Originals* higher than the number of files physically existing in my originals directory? ###

During indexing your files, PhotoPrism creates a .jpg Version for all other file types than .jpg (e.g. RAWS, Videos, PNGs etc). 
These files are stored in /storage/sidecar (unless configured otherwise). 
In the UI they are shown in the *Originals* section and added to its count.

### Why do some of my photos without geolocation information show a random location? ###

PhotoPrism estimates the location of photos without geolocation from photos that have been taken on the same day.
You can disable estimations in [Settings](./settings/general.md).

### Why do I get an error when trying to add a remote server for syncing? ###

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

### My file sync app fails with "unable to parse TLS packet headers" when trying to connect via WebDAV? ###

Because of security considerations, some backup tools and file sync apps like
[FolderSync removed support for non-SSL HTTP communication](https://www.tacit.dk/foldersync/faq/#i-can-not-connect-to-a-non-https-webdav-server-why).

When installing PhotoPrism on a public server outside your home network, please **always run it
behind a secure HTTPS reverse proxy** like [Traefik](../getting-started/proxies/traefik.md),
[Caddy](../getting-started/proxies/caddy-2.md), or [NGINX](../getting-started/proxies/nginx.md).
Your files and passwords will be transmitted in clear text otherwise, and can be intercepted
by anyone in between including your provider, hackers, and governments.