# Advanced Backup Guide

**A backup of PhotoPrism should include, at a minimum, the files in [your *originals* folder](../docker-compose.md#photoprismoriginals) and a copy of the index database. We also recommend backing up [the *storage* folder](../docker-compose.md#photoprismstorage) so that you don't need to recreate the thumbnails and your backup includes all config files.**

You can create an index SQL backup by running this command in a terminal:

```bash
photoprism backup -i [filename]
```

Or the following for [docker-compose](../docker-compose.md):

```bash
docker compose exec -T photoprism photoprism backup -i - > photoprism-db.sql
```

As seen above, you can use `-` as filename to write the backup to stdout.
This is done to ensure the backup resides outside of the container environment.

If you leave the filename empty, the backup will be written to the default backup folder configured via [`PHOTOPRISM_BACKUP_PATH`](../../config-options/#storage-folders).

If you want, you can also export your cache and thumbnails, but it can also be re-generated after restore.
It will save you from re-generating thumbnails from scratch however.

Helpful information can be found on [GitHub](https://github.com/photoprism/photoprism/discussions/772) as well.

## SQLite Backups

Creating SQL dumps from SQLite is currently not supported by the `photoprism backup` command, since SQLite files are located in the *storage* folder and thus should automatically be part of any backup.

However, if you prefer to have a dump, you can [run this command](../docker-compose.md#command-line-interface) to create one:

```bash
docker compose exec -T photoprism sqlite3 /photoprism/storage/index.db .dump > photoprism-db.sql
```

If you use pure `docker`, you can run the following (or replace `docker` with `podman` on Red Hat-based Linux distributions):

```bash
docker exec -t PhotoPrism sqlite3 /photoprism/storage/index.db .dump > photoprism-db.sql
```

## Restore Backups

See our user guide to learn how to [restore backups](../../user-guide/backups/restore.md).

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-pencil: to send a pull request with your changes.
