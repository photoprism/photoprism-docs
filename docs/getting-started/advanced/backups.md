# Advanced Backup Guide

At a minimum, a backup of PhotoPrism should include the files in [your *originals* folder](../../getting-started/docker-compose.md#photoprismoriginals) and a copy of the index database. We also recommend backing up [the *storage* folder](../../getting-started/docker-compose.md#photoprismstorage) so that you don't need to recreate any thumbnail or sidecar files, and your backup includes the complete configuration.

!!! tldr ""
    The easiest way to create a full backup is to first run the backup command to generate a database dump as described in our [**Backup Guide**](../../user-guide/backups/index.md). Then back up your *originals* and *storage* folders using any standard file backup utility.

## Scheduled Backups

By default, [PhotoPrism 240523-923ee0cf7](../../release-notes.md#may-23-2024) and newer versions automatically create daily database backups for you, with up to 3 copies being retained. The schedule, the type of backups, and the number of backups to be retained can be [changed in the configuration](../config-options.md#backup).

## Backup Command

You can run the following command [in a terminal](../docker-compose.md#command-line-interface) to manually create a new MariaDB or SQLite database backup:

```bash
photoprism backup -i [filename]
```

Or the following if you are using [docker-compose](../docker-compose.md):

```bash
docker compose exec -T photoprism photoprism backup -i - > photoprism-db.sql
```

As seen above, you can use `-` as filename to write the backup to stdout.
This is done to ensure the backup resides outside of the container environment.

If you leave the filename empty, the backup will be written to the default backup folder configured via [`PHOTOPRISM_BACKUP_PATH`](../config-options.md#storage).

If you want, you can also export your cache and thumbnails, but it can also be re-generated after restore.
It will save you from re-generating thumbnails from scratch however.

Helpful information can be found on [GitHub](https://github.com/photoprism/photoprism/discussions/772) as well.

## Restore Command

See our regular [Backup Guide](../../user-guide/backups/restore.md) to learn how to [restore backups](../../user-guide/backups/restore.md).

## SQLite Backups

!!! tldr ""
    If you are using a [current version](../../release-notes.md), you can create SQL dumps of SQLite with the `photoprism backup` command. Since the binary SQLite database files are located in the *storage* folder, they should also be automatically included in any backup.

In order to create a dump directly with SQLite, you can alternatively run [this command](../docker-compose.md#command-line-interface):

```bash
docker compose exec -T photoprism sqlite3 /photoprism/storage/index.db .dump > photoprism-db.sql
```

With pure `docker`, you can run the following (or replace `docker` with `podman` on Red Hat-based Linux distributions):

```bash
docker exec -t PhotoPrism sqlite3 /photoprism/storage/index.db .dump > photoprism-db.sql
```

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
