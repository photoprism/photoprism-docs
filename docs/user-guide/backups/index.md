# Creating Backups

At a minimum, a backup of PhotoPrism should include the files in [your *originals* folder](../../getting-started/docker-compose.md#photoprismoriginals) and a copy of the index database. We also recommend backing up [the *storage* folder](../../getting-started/docker-compose.md#photoprismstorage) so that you don't need to recreate any thumbnail or sidecar files, and your backup includes the complete configuration.

=== "MariaDB"

    1. The easiest way to create a full backup is to first run the backup command to generate a MariaDB database dump as shown below.
    2. Then back up your *originals* and *storage* folders using any standard file backup utility.

=== "SQLite"

    A full backup of both folders is mandatory, but it is not necessary to [create a dump](../../getting-started/advanced/backups.md#sqlite-backups) first, as there already is a copy of the index database in the *storage* folder.

## Backup Command

The easiest way to create an index SQL dump of MariaDB is to run the backup command in a terminal:

```
docker compose exec photoprism photoprism backup -i -f
```

If you are using Podman on a Red Hat-compatible Linux distribution:

```
podman-compose exec photoprism photoprism backup -i -f
```

By default, this will create a backup in `storage/backup/mysql/YYYY-MM-DD.sql`.

Omit the `-f` flag if you do not want to overwrite existing files. A custom backup folder can be configured with [`PHOTOPRISM_BACKUP_PATH`](../../getting-started/config-options.md#storage).

Alternatively, you can pass a specific filename as argument or `-` to write the SQL dump to stdout. This and how to create SQL dumps from SQLite is shown in the [advanced backup guide](../../getting-started/advanced/backups.md).

!!! tldr ""
    Note that our guides now use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose`.

## Important Folders

### Originals

The [*originals* folder](../../getting-started/docker-compose.md#photoprismoriginals) contains your original photo and video files. You can back it up and restore it using any standard file backup program if you have not already set this up.

### Storage

SQLite, config, cache, thumbnail and sidecar files are saved in [the *storage* folder](../../getting-started/docker-compose.md#photoprismstorage). As with the *originals* folder, the exact path on your computer [depends on your configuration](../../getting-started/config-options.md#storage).

We recommend that you back up this folder as well so that you don't need to recreate the thumbnails and have a complete backup of your configuration. As for the *originals* folder, you can use any standard file backup utility to do this.

!!! example ""
    Depending on the [resources available to us](https://photoprism.app/kb/oss), a future version may include additional features so that you do not have to rely on external tools to perform file backups and can use a web interface.
