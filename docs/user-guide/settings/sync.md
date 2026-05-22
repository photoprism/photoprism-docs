# Services

You can connect your PhotoPrism instance to other services with WebDAV support, such as other PhotoPrism instances, Nextcloud or ownCloud. This allows you to [share](../share/services-share.md) or [synchronize](../sync/services-sync.md) files between multiple services.

PhotoPrism can also expose its originals via WebDAV so that compatible clients on macOS, Windows, and mobile devices can connect directly. [Learn more ›](../sync/webdav.md)

!!! tldr ""
    These settings are not available when running in public mode because they are not safe to use without authentication.

## Add Service ##

1. Go to *Settings*.
2. Open the *Services* tab.
3. Click *Connect*.
   ![Screenshot](img/services-connect-1-2502.jpg){ class="shadow" }
4. Fill in the service URL, username, and password.
5. Click *Connect*.
   ![Screenshot](img/services-connect-2-2502.jpg){ class="shadow" }
6. The service is now connected to PhotoPrism.


## Edit Connection Details ##

1. Go to *Settings*.
2. Open the *Services* tab.
3. Click the pencil :material-pencil: icon.
4. Edit account details and click *Save*.
   ![Screenshot](img/services-edit-2502.jpg){ class="shadow" }


## Edit Upload Settings ##

1. Go to *Settings*.
2. Open the *Services* tab.
3. Click into the upload cell of your service.
   ![Screenshot](img/services-upload-1-2502.jpg){ class="shadow" }
4. Select the folder to which photos should be uploaded and click *Save*.
   ![Screenshot](img/services-upload-2-2502.jpg){ class="shadow" }

You can now [share albums or files with this service](../share/services-share.md).

!!! danger ""
    Some Nextcloud configurations can cause uploaded files to appear as 0-byte files. See the [known workaround](https://github.com/photoprism/photoprism/issues/443).


## Edit Sync Settings ##

1. Go to *Settings*.
2. Open *Services* tab.
3. Click into the sync cell of your service.
   ![Screenshot](img/services-sync-1-2502.jpg){ class="shadow" }
4. Enable synchronization in the upper right corner.
5. Choose a folder from your service.
6. Choose a sync interval.
7. Select the options that are suitable for you and click *Save*.


![Screenshot](img/services-sync-2-2502.jpg){ class="shadow" }

### Remote Sync Options ###

- *Download remote files* will download all files from the selected folder of the other service that do not yet exist in PhotoPrism.
- *Upload local files* will upload all files (including private or archived ones) from PhotoPrism to your service that do not yet exist there.
- *Preserve filenames* will keep filenames without renaming them.
- *Sync raw and video files* will upload and download RAW and video files together with JPEGs.

