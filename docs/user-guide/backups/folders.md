The following overview describes the most important files and folders used by PhotoPrism:

## Originals

Your original photo and video media files are [stored in the *originals* folder](../../getting-started/docker-compose.md#photoprismoriginals). If [read-only mode](../settings/advanced.md#read-only-mode) is disabled, new files can be added using the [web upload dialog](../library/upload.md), the [import functionality](../library/import.md), or by [mounting the folder via WebDAV](../sync/webdav.md). PhotoPrism will generally [not move, rename, or otherwise modify the files in this folder](../../getting-started/faq.md#in-which-cases-could-files-in-the-originals-folder-get-modified) unless a user requests it.

The path can be changed using the environment variable [`PHOTOPRISM_ORIGINALS_PATH`](../../getting-started/config-options.md#storage), the [corresponding CLI flag](../../getting-started/config-options.md#storage), or a [YAML configuration file](../../getting-started/config-files/index.md#storage).

[Learn more ›](../../getting-started/docker-compose.md#photoprismoriginals)

## Storage

Unless you have a [custom configuration](../settings/advanced.md), the [*storage* folder](../../getting-started/docker-compose.md#photoprismstorage) is used to read and write [config](#config), [cache](#cache), [backup](#backup), [thumbnail](#thumbnails), and [sidecar](#sidecar) files. [Never configure the *storage* folder to be inside the *originals* folder](../../known-issues.md#nested-storage-folder), even under a hidden name that starts with `.`.

The path can be changed using the environment variable [`PHOTOPRISM_STORAGE_PATH`](../../getting-started/config-options.md#storage), the [corresponding CLI flag](../../getting-started/config-options.md#storage), or a [YAML configuration file](../../getting-started/config-files/index.md#storage).

[Learn more ›](../../getting-started/docker-compose.md#photoprismstorage)

### Cache

This folder contains the subdirectories `json` and `thumbnails` for storing ExifTool JSON files and thumbnail images. You can customize its storage path by setting [`PHOTOPRISM_CACHE_PATH`](../../getting-started/config-options.md#storage), using the [corresponding CLI flag](../../getting-started/config-options.md#storage), or editing the [`options.yml`](../../getting-started/config-files/index.md#storage) config file.

[Learn more ›](../../getting-started/faq.md#why-is-my-storage-folder-so-large-what-is-in-it)

#### JSON

Unless you have disabled [ExifTool](https://exiftool.org/) in [Settings > Advanced](../settings/advanced.md), it may create JSON files with file metadata in this directory, for example when indexing or importing new files.

[Learn more ›](../settings/advanced.md#disable-exiftool)

#### Thumbnails

PhotoPrism creates thumbnails in different sizes for each photo. They are stored in the `thumbnails` directory. More information can be found in [Preview Images](../settings/advanced.md#preview-images).

[Learn more ›](../settings/advanced.md#preview-images)

### Sidecar

The *sidecar* folder contains [YAML backup files](export.md#photo-backups) for your photo metadata as well as, for example, automatically generated JPEG versions of RAW images. Both can be configured in [Settings > Advanced](../settings/advanced.md). You can customize its storage path by setting [`PHOTOPRISM_SIDECAR_PATH`](../../getting-started/config-options.md#sidecar-files), using the [corresponding CLI flag](../../getting-started/config-options.md#sidecar-files), or editing the [`options.yml`](../../getting-started/config-files/index.md#sidecar-files) config file.

[Learn more ›](../settings/advanced.md#backups)

### Config

The *config* folder contains configuration files and certificates. You can customize its storage path by setting [`PHOTOPRISM_CONFIG_PATH`](../../getting-started/config-options.md#storage), using the [corresponding CLI flag](../../getting-started/config-options.md#storage), or editing the [`defaults.yml`](../../getting-started/config-files/defaults.md) config file.

[Learn more ›](../../getting-started/config-files/index.md)

### Backup

The *backup* folder contains database dumps as well as album [backup files](../../getting-started/advanced/backups.md). By default, it is located in the *storage* folder. You can customize its storage path by setting [`PHOTOPRISM_BACKUP_PATH`](../../getting-started/config-options.md#backup), using the [corresponding CLI flag](../../getting-started/config-options.md#backup), or editing the [`options.yml`](../../getting-started/config-files/index.md#backup) config file.

[Learn more ›](../../getting-started/config-options.md#backup)

## Import

The [import feature](../library/import.md) lets you transfer files from the *import* folder to the [*originals* folder](#originals). Duplicates are automatically skipped, and the imported files are given unique file paths based on their content and metadata. The base path of the *import* directory can be changed by setting [`PHOTOPRISM_IMPORT_PATH`](../../getting-started/config-options.md#storage), using the [corresponding CLI flag](../../getting-started/config-options.md#storage), or editing the [`options.yml`](../../getting-started/config-files/index.md#storage) config file.

[Learn more ›](../../getting-started/docker-compose.md#photoprismimport)

## Database

If you are [using MariaDB](../../getting-started/troubleshooting/mariadb.md) or [another dedicated database server](../../getting-started/faq.md#should-i-use-sqlite-mariadb-or-mysql) instead of [SQLite](../../getting-started/troubleshooting/sqlite.md), it stores its data in a separate *database* folder whose location depends on your configuration, for example in the `mariadb` service section of [your `compose.yaml` file](../../getting-started/docker-compose.md#database).

[Learn more ›](../../getting-started/troubleshooting/mariadb.md#server-migration)

## Temp

Uploads, downloads, and other *temporary* files may be created in the *temp* folder. The path can be changed by setting [`PHOTOPRISM_TEMP_PATH`](../../getting-started/config-options.md#storage), using the [corresponding CLI flag](../../getting-started/config-options.md#storage), or editing the [`options.yml`](../../getting-started/config-files/index.md#storage) config file.

[Learn more ›](../../getting-started/config-options.md#storage)

## Assets

The *assets* folder contains static resources such as machine learning models, icons, and templates. Its path can be changed by setting [`PHOTOPRISM_ASSETS_PATH`](../../getting-started/config-options.md#storage), using the [corresponding CLI flag](../../getting-started/config-options.md#storage), or editing the [`options.yml`](../../getting-started/config-files/index.md#storage) config file.

[Learn more ›](../../getting-started/config-options.md#storage)
