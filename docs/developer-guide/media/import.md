# Importing, Indexing, and Uploading

PhotoPrism is meant to be a complete photo management solution that not only lets you [index your existing pictures](../../user-guide/library/originals.md), but also add or [upload new files](../../user-guide/library/upload.md) to your photo collection or [delete existing files](../../user-guide/organize/delete.md) to free up space.

You can therefore choose to [index your originals directly](../../user-guide/library/originals.md), leaving all file and folder names unchanged, or [use the optional import feature](../../user-guide/library/import.md) that automatically removes duplicates, gives files a unique name and sorts them by year and month.

To learn more, follow our [First Steps 👣](../../user-guide/first-steps.md) tutorial which will guide you through the interface and settings.

## Read-Only Mode ##

Early in development there was some debate about whether PhotoPrism should be responsible for naming files, see [Support Photos In Place on Hard Drive #41](https://github.com/photoprism/photoprism/issues/41). Once you want the software to automatically create new files or merge photo libraries from different devices, this is often the only viable option.

Besides the index-only functionality for users who want to name their files manually, we have also introduced a read-only mode for those who want to use the software as a gallery with limited features, see [Read-Only Mode #56](https://github.com/photoprism/photoprism/issues/56).

## Post Processing ##

After importing new pictures, it would be great if users could quickly sort and review them. This way, the library stays clean and organized, even without applying filters to hide bad shots.

This is common workflow among users of [Adobe Bridge](https://www.adobe.com/products/bridge.html), a tool used by many professionals. They go through complete asset collections and sort photos using keyboard shortcuts, where keys toggle pre-defined tags or flags like "favorite".

## Upload Options ##

Users can either [use WebDAV to upload files](../../user-guide/sync/webdav.md) and add them to their *originals* or *import* folder, or [use the Web Upload](../../user-guide/library/upload.md) to add them to a temporary directory on the server, from which they will be imported to the *originals* folder.

!!! example ""
    We might later use [WebAssembly](https://webassembly.org/) or the [File API](https://developer.mozilla.org/en-US/docs/Web/API/File_API/Using_files_from_web_applications) to improve the performance and capabilities of the [Web Upload](../../user-guide/library/upload.md).
