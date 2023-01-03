# Creating Backups

A full backup of PhotoPrism should include, at a minimum, the files in your *originals* folder and a SQL dump of the database. We also recommend backing up the *storage* folder so you don't have to recreate thumbnails and have a complete backup of your configuration.

The easiest way to create an index SQL backup is to run this command in a terminal:

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

Creating SQL dumps from SQLite is currently not fully supported by the `photoprism backup` command. However, you can run this command to create a backup file if you use [docker-compose:](../docker-compose.md#command-line-interface):

```bash
docker compose exec -T photoprism sqlite3 /photoprism/storage/index.db .dump > photoprism-db.sql
```

If you only use `docker`, you can run the following:

```bash
docker exec -t PhotoPrism sqlite3 /photoprism/storage/index.db .dump > photoprism-db.sql
```

## Restore Backups

Follow [this guide to restore](../../user-guide/advanced/restore.md) PhotoPrism from backups.

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-pencil: to send a pull request with your changes.
