# Sync files with Dropbox

*Note: This is contributed content.*

It's possible to use [Dropbox](https://www.dropbox.com/) to store your photos, while viewing and managing them through PhotoPrism.

1. Set up a Dropbox account.
2. Install the Dropbox desktop client.
3. Sync your Dropbox to a local directory.
4. If using Docker, configure your `docker-compose.yml` with;
    ```
    volumes:
      - "~/Dropbox/Photos:/photoprism/originals"
    ```
5. Follow the PhotoPrism [getting started](/getting-started/) guide as normal.

## Auto-upload from Mobile

The Dropbox mobile apps also have a 'Camera Upload' feature which syncs photos to Dropbox, and then to any machine with Dropbox installed.

To auto-import uploaded files into PhotoPrism;

1. Install the Dropbox [iOS](https://itunes.apple.com/gb/app/dropbox/id327630330?mt=8) or [Android](https://play.google.com/store/apps/details?hl=en_GB&id=com.dropbox.android) app.
2. Enable 'Camera Uploads' in the Dropbox app's settings.
3. Install the Dropbox [desktop client](https://www.dropbox.com/install) on your server or a network-accessible machine
4. Configure the `Camera Uploads` folder as your `import` directory for PhotoPrism.
    In your `docker-compose.yml` file, this is;
    ```
    volumes:
      - "~/Dropbox/Camera Uploads:/photoprism/import"
    ```
5. Optional: Enable 'delete on import' in PhotoPrism's settings to delete imported files from Dropbox. This saves Dropbox space, allowing you to remain within the 2GB free tier.

!!! note
    The Dropbox mobile app needs to be opened periodically or it tends to fail to identify and sync new photos.

    The [PhotoPrism mobile app](https://github.com/photoprism/photoprism-mobile) is also under development and provides a sync feature.

## Smart / Selective Sync

A useful (although paid) feature is [Dropbox Smart Sync](https://www.dropbox.com/smart-sync) (with optional auto-evict) which will download the files from Dropbox's servers only when you (or PhotoPrism) accesses them (such as during initial indexing, or when downloading an original file via the PhotoPrism interface).

This can save space on your server by automically offloading the originals unless/until they're viewed.
