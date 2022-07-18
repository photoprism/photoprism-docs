# Creating Backups

!!! quote ""
    Help improve this page! You can contribute by clicking :material-pencil: to send a pull request with your changes.

A full backup of your PhotoPrism instance includes:

1. All content from your `originals` folder
2. An index database SQL dump

The best way to create an index backup is to run this command in a terminal:

```
photoprism backup -i [filename]
```

Or the following for [docker-compose](../docker-compose.md):

```
docker-compose exec -T photoprism photoprism backup -i - > photoprism-db.sql
```

As seen above, you can use `-` as filename to write the backup to stdout.
This is done to ensure the backup resides outside of the container environment.

If you leave the filename empty, the backup will be written to the default backup folder configured via [`PHOTOPRISM_BACKUP_PATH`](../../config-options/#storage-folders).

If you want, you can also export your cache and thumbnails, but it can also be re-generated after restore.
It will save you from re-generating thumbnails from scratch however.

Helpful information can be found on [GitHub](https://github.com/photoprism/photoprism/discussions/772) as well.

## Restore from Backup
Follow [this guide to restore](../../user-guide/advanced/restore.md) PhotoPrism from backups.
