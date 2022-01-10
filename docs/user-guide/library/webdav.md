# WebDAV File Upload #

!!! tldr ""
    For security reasons, the built-in WebDAV server is disabled when running in [public mode](../../getting-started/config-options.md) without authentication.

You can use WebDAV-compatible apps, including Microsoft's Windows Explorer and Apple's Finder, 
to add files to your *originals* and *import* folders from a remote computer or mobile device.

Follow the [instructions](../sync/webdav.md) to learn how to connect.

You can start [importing or indexing](index.md) as usual after files have been transferred
to your library.

!!! tip ""
    You can use also WebDAV to download files from your library. Simply connect to 
    `http://server-ip:2342/originals/` (local server without HTTPS) or 
    `https://yourdomain/originals/` (public server with HTTPS enabled), and copy the files to 
    a folder on your local device.
