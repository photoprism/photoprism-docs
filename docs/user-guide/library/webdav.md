# WebDAV File Upload #

WebDAV-compatible apps and clients such as [PhotoSync](../sync/mobile-devices.md), Microsoft's Windows Explorer,
and Apple's Finder can connect directly to PhotoPrism:

↪ [Connecting via WebDAV](../sync/webdav.md)

After files have been transferred, you can [index](../library/originals.md) or [import](../library/import.md) them as usual.
By default, indexing and importing start automatically after a safety delay when files have been uploaded using WebDAV.

!!! tldr ""
    You can disable WebDAV in [Advanced Settings](../settings/advanced.md). For security reasons, the built-in WebDAV
    server is automatically disabled when running in [public mode](../../getting-started/config-options.md) without
    authentication.

!!! note ""
    You can also use WebDAV to download files from your library: Simply connect to 
    `http://server-ip:2342/originals/` (local server without HTTPS) or 
    `https://yourdomain/originals/` (public server with HTTPS enabled), and then copy the files to 
    a folder on your local device.
