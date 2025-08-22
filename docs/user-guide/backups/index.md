# Creating Backups

At a minimum, a backup of PhotoPrism should include the files in [your *originals* folder](../../getting-started/docker-compose.md#photoprismoriginals) and a copy of the index database. We also recommend backing up [the *storage* folder](../../getting-started/docker-compose.md#photoprismstorage) so that you don't need to recreate any thumbnail or sidecar files, and your backup includes the complete configuration.

!!! tldr ""
    The easiest way to create a full backup is to first run the backup command to generate a database dump as shown below.
    Then back up your *originals* and *storage* folders using any standard file backup utility.

## Scheduled Backups

By default, [PhotoPrism 240523-923ee0cf7](../../release-notes.md#may-23-2024) and newer versions automatically create daily database backups for you, with up to 3 copies being retained. The schedule, the type of backups, and the number of backups to be retained can be [changed in the configuration](../../getting-started/config-options.md#backup).

We recommend that you manually create a full backup of all files, including your configuration and index database, before starting a [server migration](#mariadb-server-migration) or making any other major changes.

## Backup Command

If you are using Docker Compose, you can run the following command [in a terminal](../../getting-started/docker-compose.md#command-line-interface) to manually create a new MariaDB or SQLite database backup:

```
docker compose exec photoprism photoprism backup -i -f
```

By default, a backup is created in `storage/backup/mysql/[YYYY-MM-DD].sql`. Omit the `-f` flag if you do not want to overwrite existing files. A custom backup base folder can be configured with [`PHOTOPRISM_BACKUP_PATH`](../../getting-started/config-options.md#storage)

If you are using Podman on a Red Hat-compatible Linux distribution, exchange `docker compose` for `podman-compose`.

Alternative ways to create SQL dumps from SQLite are shown in our [advanced backup guide](../../getting-started/advanced/backups.md#sqlite-backups).

### Custom file names

You can specify a custom filename as an argument to dump the database to a file of your choice (using the `-f` flag to overwrite existing files):

```
docker compose exec photoprism photoprism backup -i my_custom_dump.sql
```

The file name argument is interpreted as an absolute path, so the example above will create a file `/photoprism/my_custom_dump.sql` inside the container volume. For example, to store the file in the default backup directory:

```
docker compose exec photoprism photoprism backup -i /photoprism/storage/backup/mysql/my_custom_dump.sql
```

You can also use `-` as file name to write the SQL dump to [stdout](../../getting-started/advanced/backups.md). 

!!! tldr ""
    Note that our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible distributions.

## Important Directories

### Originals

The [*originals* folder](../../getting-started/docker-compose.md#photoprismoriginals) contains your original photo and video files. You can back it up and restore it using any standard file backup program if you have not already set this up.

[Learn more ›](folders.md#originals)

### Storage

SQLite, config, cache, backup, thumbnail and sidecar files are saved in [the *storage* folder](../../getting-started/docker-compose.md#photoprismstorage). As with the *originals* folder, the exact path on your computer [depends on your configuration](../../getting-started/config-options.md#storage).

We recommend that you back up this folder as well so that you don't need to recreate the thumbnails and have a complete backup of your configuration. As for the *originals* folder, you can use any standard file backup utility to do this.

[Learn more ›](folders.md#storage)

### Database

If you are [using MariaDB](../../getting-started/troubleshooting/mariadb.md) or [another dedicated database server](../../getting-started/faq.md#should-i-use-sqlite-mariadb-or-mysql) instead of [SQLite](../../getting-started/troubleshooting/sqlite.md), they will store their data in a separate *database* folder whose location depends on your configuration, e.g. in the `mariadb` service section of [your `compose.yaml` file](../../getting-started/docker-compose.md#database).

## MariaDB Server Migration

For detailed information on how to move your [MariaDB database](#database) to another server or virtual machine, please see the [Server Migration](../../getting-started/troubleshooting/mariadb.md#server-migration) section of our [MariaDB Troubleshooting Guide](../../getting-started/troubleshooting/mariadb.md).

[Learn more ›](../../getting-started/troubleshooting/mariadb.md#server-migration)
