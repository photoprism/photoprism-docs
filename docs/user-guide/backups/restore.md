# Restoring Backups

To restore your instance, you must have the files in [your *originals* folder](../../getting-started/docker-compose.md#photoprismoriginals) and a copy of the index database. We also recommend [having a backup](index.md) of [the *storage* folder](../../getting-started/docker-compose.md#photoprismstorage) so that you don't need to recreate any thumbnail or sidecar files, and your backup includes the complete configuration:

- if you have a backup copy of your *storage* and *originals* folders, the easiest way is to restore those folders first and then run the restore command as shown below
- otherwise, you additionally need to perform a [complete rescan of your library](../../user-guide/library/originals.md) to recreate missing sidecar and thumbnail files

## Restore Command

To restore the index from an existing MariaDB dump, you can run the following command:

```
docker compose exec photoprism photoprism restore -i -f
```

*Note that our guides now use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose`.*

If you are using Podman on a Red Hat-compatible Linux distribution:

```
podman-compose exec photoprism photoprism restore -i -f
```

This will automatically search the backup folder for the most recent index dump and restore it. A custom backup folder can be configured with [`PHOTOPRISM_BACKUP_PATH`](../../getting-started/config-options.md#storage).

Omit the `-f` flag to prevent overwriting an existing index. As with the backup command, you can also specify a specific dump filename as an argument:

```
docker compose exec photoprism photoprism restore -i [filename]
```

!!! tldr ""
    When the database is restored, all user accounts and passwords will be restored as well.
