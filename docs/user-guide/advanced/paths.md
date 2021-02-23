This page gives you an overview about the paths used by PhotoPrism.

## Originals Path
This path can be configured by `PHOTOPRISM_ORIGINALS_PATH`.
The `originals` directory contains your photo library.

## Import Path
This path can be configured by `PHOTOPRISM_IMPORT_PATH`.
If you decide to use our [import](../library/import-vs-index.md) functionality,
you add your photos to the `import` directory, so that they can be imported into `originals`.

## Storage Path
The storage path can be configured using `PHOTOPRISM_STORAGE_PATH`.
Using the default settings the storage path contains cache, sidecar and backup paths as well as database files.

//Always? Welche sind immer in storage?

### Cache Path
The `cache` directory contains `json` and `thumbnails` directories. 
The path can be set using `PHOTOPRISM_CACHE_PATH`.

#### JSON
PhotoPrism creates json files containing a file's exifdata in this directory.
You can prevent PhotoPrism from creating those json files by disabling exiftool in [Settings](../settings/advanced.md).

//Is this json updated when I update the exif data of my file in originals?
// Do we create those for all file types?

#### Thumbnails
PhotoPrism creates thumbnails in different sizes for each photo. Those are stored in the `thumbnails` directory.
More information on thumbnails can be found [here](../settings/advanced.md#images).

### Sidecar Path
In the `sidecar` directory PhotoPrism stores [yml backup files](./backups.md) for each photo as well as jpgs it converted e.g. from RAWs.
Both backup and converting functionalities can be disabled in [Settings](../settings/advanced.md).
The sidecar path can be configured using `PHOTOPRISM_SIDECAR_PATH`.

### Backup Path
Ist das /albums???
Switch off with what?

## Temp Path
In the `temp` directory, uploads and downloads are temporarily stored. You can configure the path using `PHOTOPRISM_TEMP_PATH`.

## Asset Path
The asset path is used to store static resources like models and templates. It can be set using `PHOTOPRISM_ASSETS_PATH`.

## Config Path
In the config path, setting files might be stored. It can be set with `PHOTOPRISM_CONFIG_PATH`.

