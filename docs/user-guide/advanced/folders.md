This page gives you an overview about the directories used by PhotoPrism.

## Originals
This path can be configured by `PHOTOPRISM_ORIGINALS_PATH`.
The `originals` directory contains your photo library. PhotoPrism will never move or rename files in this folder. It may add files from uploads or imports, unless read-only mode is enabled.

## Import
This path can be configured by `PHOTOPRISM_IMPORT_PATH`.
If you decide to use our [import](../library/import-vs-index.md) functionality,
you add your photos to the `import` directory, so that they can be imported into `originals`.

## Storage
The storage path can be configured using `PHOTOPRISM_STORAGE_PATH`.

In case cache, sidecar and config path are not defined separately, those are located in the storage directory.
In addition the storage directory contains [album backups](./backups.md#album-backups) in `/albums` as well as database files.

!!! attention
    You storage path must NOT be located in your originals path. Otherwise your thumbnails will be indexed as well!

### Cache
The `cache` directory contains `json` and `thumbnails` directories. 
The path can be set using `PHOTOPRISM_CACHE_PATH`.

#### JSON
PhotoPrism creates JSON files containing a file's metadata, read by exiftool, in this directory.
You can prevent PhotoPrism from creating those JSON files by disabling exiftool in [Settings](../settings/advanced.md).

#### Thumbnails
PhotoPrism creates thumbnails in different sizes for each photo. Those are stored in the `thumbnails` directory.
More information on thumbnails can be found [here](../settings/advanced.md#images).

### Sidecar
In the `sidecar` directory PhotoPrism stores [YAML backup files](./backups.md) for each photo as well as JPEG's it converted e.g. from RAWs.
Both backup and converting functionalities can be disabled in [Settings](../settings/advanced.md).
The sidecar path can be configured using `PHOTOPRISM_SIDECAR_PATH`.

### Config
In the config path, setting files might be stored. It can be set with `PHOTOPRISM_CONFIG_PATH`.

## Backup
[Database backup files](./backups.md#backup-command) are stored in the backup directory.
It can be configured using `PHOTOPRISM_BACKUP_PATH`.

## Temp
In the `temp` directory, uploads and downloads are temporarily stored. You can configure the path using `PHOTOPRISM_TEMP_PATH`.

## Asset
The asset path is used to store static resources like models and templates. It can be set using `PHOTOPRISM_ASSETS_PATH`.


