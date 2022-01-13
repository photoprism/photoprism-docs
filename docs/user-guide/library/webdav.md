# WebDAV File Upload #

!!! tldr ""
    You can disable WebDAV in [Advanced Settings](../settings/advanced.md). For security reasons, the built-in WebDAV
    server is automatically disabled when running in [public mode](../../getting-started/config-options.md) without
    authentication.

WebDAV-compatible apps and clients such as Microsoft's Windows Explorer and Apple's Finder can connect directly
to PhotoPrism, allowing you to open, edit, and delete files from your computer as if they were local.

You can use WebDAV-compatible apps, including Microsoft's Windows Explorer and Apple's Finder, 
to add files to your *originals* and *import* folders from a remote computer or mobile device.
Follow the [instructions to learn how to connect](../sync/webdav.md).

You can [start to index or import](index.md) as usual after files have been transferred
to your library.

!!! tip ""
    You can use also WebDAV to download files from your library. Simply connect to 
    `http://server-ip:2342/originals/` (local server without HTTPS) or 
    `https://yourdomain/originals/` (public server with HTTPS enabled), and copy the files to 
    a folder on your local device.
