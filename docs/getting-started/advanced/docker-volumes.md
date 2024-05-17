# Docker Volume Mounts

When using Docker, all application services run in isolated containers, so you must explicitly [mount the host folders](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes) you want to use. Be aware that PhotoPrism and MariaDB cannot see folders that have not been mounted. This is an important security feature.

!!! note ""
    It is important that the *originals*, *storage*, and *database* folders are located on persistent volumes. We recommend changing the relative paths used in our examples to absolute paths and to avoid using named or anonymous [Docker volumes](https://docs.docker.com/compose/compose-file/07-volumes/#example) to prevent potential data loss when the container is recreated, e.g. [after an update](../updates.md#docker-compose) of the Docker image.

## Originals Folder

The *originals* folder contains your original photo and video files.

`~/Pictures` will be mounted by default, where `~` is a shortcut for your home directory:

```yaml
volumes:
  # "/host/folder:/photoprism/folder"  # example
  - "~/Pictures:/photoprism/originals"
```

You can mount [any folder accessible from the host](https://docs.docker.com/compose/compose-file/compose-file-v3/#short-syntax-3), including [network shares](../troubleshooting/docker.md#network-storage). Additional directories can also be mounted as sub folders of `/photoprism/originals` (depending on [overlay file system support](../troubleshooting/docker.md#overlay-volumes)):

```yaml
volumes:
  - "/home/username/Pictures:/photoprism/originals"
  - "/example/friends:/photoprism/originals/friends"
  - "/mnt/photos:/photoprism/originals/media"
```

On Windows, prefix the host path with the drive letter and use `/` instead of `\` as separator:

```yaml
volumes:
  - "D:/Example/Pictures:/photoprism/originals"
```

!!! tldr ""
    If *read-only mode* is enabled, all features that require write permission to the *originals* folder are disabled, e.g. [WebDAV](https://docs.photoprism.app/user-guide/sync/webdav/), uploading and deleting files. Set `PHOTOPRISM_READONLY` to `"true"` in `docker-compose.yml` for this. You can [mount a folder with the `:ro` flag](https://docs.docker.com/compose/compose-file/compose-file-v3/#short-syntax-3) to make Docker block write operations as well.

## Storage Folder

SQLite, config, cache, thumbnail and sidecar files are saved in the *storage* folder:

- a *storage* folder mount must always be configured in your `docker-compose.yml` file so that you do not lose these files after a restart or upgrade
- never configure the *storage* folder to be inside the *originals* folder unless the name starts with a `.` to indicate that it is hidden
- we recommend placing the *storage* folder on a [local SSD drive](../troubleshooting/performance.md#storage) for best performance
- mounting [symbolic links](https://en.wikipedia.org/wiki/Symbolic_link) or using them inside the *storage* folder is currently not supported
- avoid using a named or anonymous [Docker volume](https://docs.docker.com/compose/compose-file/07-volumes/#example) for permanently storing files, as this can lead to data loss when the container is recreated, e.g. [after an update](../updates.md#docker-compose) of the Docker image

!!! tldr ""
    Should you later want to move your instance to another host, the easiest and most time-saving way is to copy the entire *storage* folder along with your originals and database.

## Import Folder

You can optionally mount an *import* folder from which files can be transferred to the *originals* folder in a structured way that avoids duplicates:

- [imported files](https://docs.photoprism.app/user-guide/library/import/) receive a canonical filename and will be organized by year and month
- never configure the *import* folder to be inside the *originals* folder, as this will cause a loop by importing already indexed files

!!! tldr ""
    You can safely skip this. Adding files via [Web Upload](https://docs.photoprism.app/user-guide/library/upload/) and [WebDAV](https://docs.photoprism.app/user-guide/sync/webdav/) remains possible, unless [read-only mode](../config-options.md) is enabled or the [features have been disabled](https://docs.photoprism.app/user-guide/settings/general/).

## MariaDB Database

Our example includes a pre-configured [MariaDB](https://mariadb.com/) database server that stores it files in the `database` folder by default. If you remove it and provide no other database server credentials, SQLite database files will be created in the *storage* folder.

Please do not use a named or anonymous [Docker volume](https://docs.docker.com/compose/compose-file/07-volumes/#example) for storing MariaDB database files and check the mount path of the volume if you use a custom database image (it may not always be `/var/lib/mysql`), as both can lead to data loss when the database container is recreated, e.g. [after an update](../updates.md#docker-compose) of the Docker image.

!!! tldr ""
    Never [store database files](https://docs.photoprism.app/getting-started/troubleshooting/mariadb/#corrupted-files) on an unreliable device such as a USB flash drive, SD card, or shared network folder. These may also have [unexpected file size limitations](https://thegeekpage.com/fix-the-file-size-exceeds-the-limit-allowed-and-cannot-be-saved/), which is especially problematic for databases that do not split data into smaller files. We strongly recommend [using SSD storage for databases only](../troubleshooting/performance.md#storage).

## Network Storage

Shared folders that have already been mounted on your host under a drive letter or path can be used with Docker containers like [any other directory](../docker-compose.md#volumes).
In addition, certain types of network storage like NFS (Unix/Linux) and CIFS (Windows/Mac) can also be *mounted directly* with [Docker Compose](https://docs.docker.com/compose/compose-file/compose-file-v3/#driver_opts).

For more information, see the [Network Storage](../troubleshooting/docker.md#network-storage) section of our [Docker Troubleshooting Guide](../troubleshooting/docker.md).

[Configure Network Storage ›](../troubleshooting/docker.md#network-storage)
