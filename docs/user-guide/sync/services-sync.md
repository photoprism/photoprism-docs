# Syncing with other WebDAV-compatible Apps and Services

Under [Settings > Services](../settings/sync.md) you can connect your PhotoPrism instance to other apps and services that can be accessed via WebDAV, e.g. other PhotoPrism instances, Nextcloud or ownCloud.

!!! danger "" 
    When syncing, your files will be uploaded or downloaded to/from another service, which requires additional storage space. If you want PhotoPrism to index files from another local application, e.g. Nextcloud, we recommend mounting its file storage directory as [*originals* folder](../../getting-started/docker-compose.md#photoprismoriginals) instead of synchronizing the files via WebDAV. This prevents unnecessary copies of your files from being created.

## Automatically Upload/Download Files to/from another App

1. Go to *Settings*
2. Open *Services* tab
3. Click into the sync cell of your service
   ![Screenshot](../settings/img/services-sync-1-light.jpg){ class="shadow" }
4. Enable synchronization in the upper right corner
5. Choose a folder from your service
6. Choose a sync interval
7. Select the options that are suitable for you and click *Save*

![Screenshot](../settings/img/services-sync-2-light.jpg){ class="shadow" }

### Remote Sync Options

* *Download remote files* will download all files from the selected folder of the other service that do not yet exist in PhotoPrism
* *Upload local files* will upload all files (including private or archived ones) from PhotoPrism to your service that do not yet exist there
* *Preserve filenames* will keep filenames without renaming them
* *Sync raw and video files* will upload/download raw and video files alongside with JPEGS