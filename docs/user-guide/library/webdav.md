# WebDAV File Upload #

WebDAV-compatible apps and clients such as Microsoft's Windows Explorer and Apple's Finder can connect directly
to PhotoPrism, allowing you to open, edit, and delete files from a remote device as if they were local:

↪ [Connecting via WebDAV](../sync/webdav.md)

After files have been transferred, you can [index](../library/index.md) or [import](../library/import.md) them as usual.
By default, indexing and importing start automatically after a safety delay when files have been uploaded using WebDAV.

!!! tldr ""
    You can disable WebDAV in [Advanced Settings](../settings/advanced.md). For security reasons, the built-in WebDAV
    server is automatically disabled when running in [public mode](../../getting-started/config-options.md) without
    authentication.

!!! tip ""
    You can use also WebDAV to download files from your library. Simply connect to 
    `http://server-ip:2342/originals/` (local server without HTTPS) or 
    `https://yourdomain/originals/` (public server with HTTPS enabled), and copy the files to 
    a folder on your local device.
