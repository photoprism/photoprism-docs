# Quick Start
After you have successfully [set up](./index.md) PhotoPrism, you are now ready to use it.

-  Configure [library](../user-guide/settings/library.md) and [advanced settings](../user-guide/settings/advanced.md) according to your needs.
-  [Choose](../user-guide/library/index.md) whether you want to [index your originals](../user-guide/library/originals.md) so that the existing file and folder names are preserved, or [import them](../user-guide/library/import.md) so that they are automatically organized by year and month.

!!! note ""
    In case you want to index/import folders already existing on your server make sure you have them configured as originals/import directory during the setup.

- To add new pictures, you can either copy them to the *import* or *originals* folder [e.g. using WebDAV](../user-guide/sync/webdav.md), or [upload them with a browser](../user-guide/library/upload.md), which will import them automatically after upload.
- Start [indexing](../user-guide/library/originals.md) or [importing](../user-guide/library/import.md)

!!! note ""
    Ensure [there is enough disk space available](troubleshooting/docker.md#disk-space) for creating thumbnails and [verify filesystem permissions](troubleshooting/docker.md#file-permissions)
    before starting to index: Files in the *originals* folder must be readable, while the *storage* folder
    including all subdirectories must be readable and writeable.

- Finally, set up [automatic syncing](../user-guide/sync/mobile-devices.md) from your mobile phone and install the [Progressive Web App (PWA)](../user-guide/pwa.md) on your desktop, tablet, and phone home screens as needed.

!!! note ""
    While indexing, JPEG sidecar files may be created for originals in other formats such as RAW and HEIF.
    This is required for image classification, facial recognition, and for displaying them in a Web browser.
    Sidecar and thumbnail files will be added to the *storage* folder, so that your *originals* folder won't be modified.

Your [photos](../user-guide/organize/browse.md) and [videos](../user-guide/organize/video.md) will
successively become visible in search results and other parts of the user interface.
Open the *Logs* tab in *Library* to watch the indexer working.
The counts in the navigation are constantly updated, so you can follow the progress.

In case some of your pictures are still missing after indexing has been completed,
they might be in [Review](../user-guide/organize/review.md) due to low quality or incomplete metadata.
You can turn this and other features off in [Settings](../user-guide/settings/general.md),
depending on your specific use case.

Of course, you can continue using your favorite tools for processing RAW files, editing metadata,
or importing new shots. Go to *Library* and click *Start* to update the index after files have been
changed, added, or removed. This can also be automated using CLI commands and a [scheduler](https://dl.photoprism.app/docker/scheduler/).