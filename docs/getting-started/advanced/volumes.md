# Docker Volume Mounts

When using Docker, all application services run in isolated containers, so you must explicitly [mount the host folders](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes) you want to use. Be aware that PhotoPrism and MariaDB cannot see folders that have not been mounted. This is an important security feature.

## Originals Folder

The *originals* folder contains your original photo and video files.

`~/Pictures` will be mounted by default, where `~` is a shortcut for your home directory:

```yaml
volumes:
  # "/host/folder:/photoprism/folder"  # example
  - "~/Pictures:/photoprism/originals"
```

You can mount [any folder accessible from the host](https://docs.docker.com/compose/compose-file/compose-file-v3/#short-syntax-3), including [network shares](../troubleshooting/docker.md#network-storage). Additional directories can also be mounted as subfolders of `/photoprism/originals` (depending on overlay file system support):

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

!!! tldr ""
    Never [store database files](https://docs.photoprism.app/getting-started/troubleshooting/mariadb/#corrupted-files) on an unreliable device such as a USB flash drive, SD card, or shared network folder. These may also have [unexpected file size limitations](https://thegeekpage.com/fix-the-file-size-exceeds-the-limit-allowed-and-cannot-be-saved/), which is especially problematic for databases that do not split data into smaller files. We strongly recommend [using SSD storage for databases only](../troubleshooting/performance.md#storage).

## Network Storage

Shared folders that have already been mounted on your host can be mounted like any local drive or directory.
Alternatively, you can mount network storage with [Docker Compose](https://docs.docker.com/compose/compose-file/compose-file-v3/#driver_opts).
Please never store database files on an unreliable device such as a USB stick, SD card, or network drive.

### Unix / NFS

Follow this `docker-compose.yml` example to mount Network File System (NFS) shares e.g. from Unix servers or NAS devices:

```yaml
services:
  photoprism:
    # ...
    volumes:
      # Map named volume "originals"
      # to "/photoprism/originals":
      - "originals:/photoprism/originals"     
  mariadb:
    # ...

# Specify named volumes:
volumes:
  originals:
    driver_opts:
      type: nfs
      # Authentication and other mounting options:
      o: "addr=1.2.3.4,username=user,password=secret,soft,rw,nfsvers=4"
      # Mount this path:
      device: ":/mnt/example"
```

`device` should contain the path to the share on the NFS server, note the `:` at the beginning. In the above example, the share can be mounted as the named volume `originals`. You can also choose another name as long as it is consistent.

Driver-specific options can be set after the server address in `o`, see the [nfs manual page](https://man7.org/linux/man-pages/man5/nfs.5.html). Here are some examples of commonly used options:

- `nfsvers=3` or `nfsvers=4` to specify the NFS version
- `nolock` (optional): Remote applications on the NFS server are not affected by lock files inside the Docker container (only other processes inside the container are affected by locks)
- `timeo=n` (optional, default 600): The NFS client waits `n` tenths of a second before retrying an NFS request
- `soft` (optional): The NFS client aborts an NFS request after `retrans=n` unsuccessful retries, otherwise it retries indefinitely
- `retrans=n` (optional, default 2): Sets the number of retries for NFS requests, only relevant when using `soft`

### SMB / CIFS

Follow this `docker-compose.yml` example to mount [CIFS network shares](https://en.wikipedia.org/wiki/Server_Message_Block), e.g. **from Windows**, NAS devices or Linux servers with [Samba](https://www.samba.org/):

```yaml
services:
  photoprism:
    # ...
    volumes:
      # Map named volume "originals"
      # to "/photoprism/originals":
      - "originals:/photoprism/originals"     
  mariadb:
    # ...

# Specify named volumes:
volumes:
  originals:
    driver_opts:
      type: cifs
      o: "username=user,password=secret,rw"
      device: "//host/folder"
```

Then restart all services for the changes to take effect. Note that related values must start at the same indentation level [in YAML](../../developer-guide/technologies/yaml.md) and that **tabs are not allowed for indentation**. We recommend using 2 spaces, but any number will do as long as it is consistent.
