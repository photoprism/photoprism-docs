# Syncing with other WebDAV-compatible Apps and Services

In [settings](../settings/sync.md) you can connect your PhotoPrism instance to other services with WebDAV support, such as other PhotoPrism instances, Nextcloud or ownCloud.

!!! attention "" 
      When syncing, your files are uploaded or downloaded to/from another service, so your files are duplicated.

      If you want PhotoPrism to read from the same folder as another service, without making copies, you can simply [mount this folder as PhotoPrism's originals directory](../../getting-started/docker-compose.md#photoprismoriginals).

## Automatically Upload/Download Files to/from another App ##

1. Go to *Settings*
2. Open *Services* tab
3. Click into the sync cell of your service
   ![Screenshot](../settings/img/services-sync-1-light.jpg){ class="shadow" }
4. Enable synchronization in the upper right corner
5. Choose a folder from your service
6. Choose a sync interval
7. Select the options that are suitable for you and click *Save*


![Screenshot](../settings/img/services-sync-2-light.jpg){ class="shadow" }

### Remote Sync Options ###

* *Download remote files* will download all files from the selected folder of the other service that do not yet exist in PhotoPrism
* *Upload local files* will upload all files (including private or archived ones) from PhotoPrism to your service that do not yet exist there
* *Preserve filenames* will keep filenames without renaming them
* *Sync raw and video files* will upload/download raw and video files alongside with JPEGS