# Restoring Backups

To restore your instance, you need the files in [your *originals* folder](../../getting-started/docker-compose.md#photoprismoriginals) and a copy of the index database. We also recommend [having a backup](index.md) of [the *storage* folder](../../getting-started/docker-compose.md#photoprismstorage) so you do not need to recreate thumbnail or sidecar files and your backup includes the complete configuration:

- If you have backup copies of your *storage* and *originals* folders, the easiest way is to restore those folders first and then run the restore command if you use MariaDB or another external database.
- Otherwise, you need to perform a [complete rescan of your library](../library/originals.md) to recreate missing sidecar and thumbnail files.
- Some metadata and albums can also be [recovered from YAML backup files](export.md) even if you no longer have a copy of the index database, unless you have [disabled backups](../../getting-started/config-options.md#feature-flags).

## Restore Command

To restore the index from an existing MariaDB or SQLite dump, you can run the following command:

```
docker compose exec photoprism photoprism restore -i -f
```

If you are using Podman on a Red Hat-compatible Linux distribution:

```
podman-compose exec photoprism photoprism restore -i -f
```

This automatically searches the configured database backup directory for the most recent SQL dump and restores it. You can change the backup base folder with [`PHOTOPRISM_BACKUP_PATH`](../../getting-started/config-options.md#backup).

Omit `-f` to avoid replacing an existing index. As with the backup command, you can also specify a specific dump filename as an argument:

```
docker compose exec photoprism photoprism restore -i [filename]
```

Restoring the database also restores user accounts, passwords, sessions, and other settings stored in the index. If credentials have changed since the backup was created, sign in with the values from the restored backup.

Before replacing an existing index with `-f`, we recommend testing the backup file, for example by restoring it on a separate test instance.

!!! tldr ""
    Note that our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible distributions.

## MariaDB Server Migration

For detailed information on how to move your [MariaDB database](folders.md#database) to another server or virtual machine, please see the [Server Migration](../../getting-started/troubleshooting/mariadb.md#server-migration) section of our [MariaDB Troubleshooting Guide](../../getting-started/troubleshooting/mariadb.md).

[Learn more ›](../../getting-started/troubleshooting/mariadb.md#server-migration)
