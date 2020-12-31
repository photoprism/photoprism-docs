# Sync files from Dropbox #

It's possible to use [Dropbox](https://www.dropbox.com/) to store your photos, while viewing and managing them through PhotoPrism.

A useful (although paid) feature is [Dropbox Smart Sync](https://www.dropbox.com/smart-sync) (with optional auto-evict) which will download the files from Dropbox's servers only when you (or PhotoPrism) accesses them (such as during initial indexing, or when downloading an original file via the PhotoPrism interface).

1. Set up a Dropbox account.
2. Install the Dropbox desktop client.
3. Sync your Dropbox to a local directory.
4. If using Docker, configure the Dropbox folder as the `photoprism/originals` directory (or a subdirectory of that).
5. Follow the PhotoPrism [getting started](/getting-started/) guide as normal.
