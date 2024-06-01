The following gives you an overview of the most important folders that PhotoPrism uses:

## Originals

The *originals* folder contains the original photo and video files of your library. PhotoPrism will not move or rename the files in this folder without a user requesting it. Unless read-only mode is enabled, new files can be added using the [web upload dialog](../library/upload.md), the [import functionality](../library/import.md), or by mounting the folder [via WebDAV](../sync/webdav.md).

Its location can be changed by setting the `PHOTOPRISM_ORIGINALS_PATH` environment variable.

## Import

When [importing](../library/import.md), files are copied or moved from the *import* folder to the *originals* folder. In the process, duplicates are automatically skipped, and the imported files are given a unique file name and are sorted by year and month.

The location of the *import* folder can be changed by setting the `PHOTOPRISM_IMPORT_PATH` environment variable.

## Storage

Unless you use a custom configuration, the *storage* folder is used to save config, cache, [backup](export.md#album-backups), thumbnail, and sidecar files.

Its location can be changed by setting the `PHOTOPRISM_STORAGE_PATH` environment variable.

[Learn more ›](../../getting-started/faq.md#why-is-my-storage-folder-so-large-what-is-in-it)

!!! attention ""
    We recommend [not to configure](../../known-issues.md#nested-storage-folder) the *storage* folder to be inside the *originals* folder unless the name starts with a `.` to indicate that it is hidden.

### Cache

The *cache* folder contains the subdirectories `json` and `thumbnails` for storing ExifTool JSON files and thumbnail images.

Its location can be changed by setting the `PHOTOPRISM_CACHE_PATH` environment variable.

#### JSON

Unless you have disabled [ExifTool](https://exiftool.org/) in [Settings > Advanced](../settings/advanced.md), it may used to create JSON files with the metadata of a file in this directory e.g. when indexing or importing new files.

#### Thumbnails

PhotoPrism creates thumbnails in different sizes for each photo. Those are stored in the `thumbnails` directory.
More information on thumbnails can be found [here](../settings/advanced.md#preview-images).

### Sidecar

The *sidecar* folder contains [YAML backup files](export.md#photo-backups) for each picture as well as e.g. automatically generated JPEG versions of RAW images.
Both can be configured in [Settings > Advanced](../settings/advanced.md).

Its location can be changed by setting the `PHOTOPRISM_SIDECAR_PATH` environment variable.

### Config

The *config* folder contains configuration files and certificates.

Its location can be changed by setting the `PHOTOPRISM_CONFIG_PATH` environment variable.

### Backup

The *backup* folder contains database as well as album [backup files](../../getting-started/advanced/backups.md) and is located in the *storage* folder by default.

Its location can be changed by setting the `PHOTOPRISM_BACKUP_PATH` environment variable.

## Temp

Uploads, downloads, and other temporary files may be temporarily stored in the *temp* folder.

Its location can be changed by setting the `PHOTOPRISM_TEMP_PATH` environment variable.

## Assets

The *asset* folder contains static resources such as machine learning models, icons, and templates.

Its location can be changed by setting the `PHOTOPRISM_ASSETS_PATH` environment variable.


