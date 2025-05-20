# Troubleshooting MariaDB Problems

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://www.photoprism.app/membership) receive direct [technical support](https://www.photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to [determine the cause of your problem](index.md).

## Compatibility

PhotoPrism is compatible with [SQLite 3](sqlite.md) and [MariaDB 10.5.12+](https://mariadb.org/).
Official support for MySQL 8 is discontinued as Oracle seems to have stopped shipping [new features and enhancements](https://github.com/photoprism/photoprism/issues/1764).
As a result, the testing effort required before each release is no longer feasible.

Our [configuration examples](https://dl.photoprism.app/docker/) are generally based on the [current stable version](https://mariadb.com/kb/en/mariadb-server-release-dates/) to take advantage of performance improvements. This does not mean that [older versions](../index.md#databases) are no longer supported and you must upgrade immediately. We recommend not using the `:latest` tag for the MariaDB Docker image and to upgrade manually by changing the tag once we had a chance to test a new major version, e.g.:

```yaml
services:
  mariadb:
    image: mariadb:11
    ...
```

## Cannot Connect

First, verify that you are using the correct port (default is `3306`) and host:

- in the internal Docker network, the default hostname is `mariadb` (same as the [service](https://dl.photoprism.app/docker/compose.yaml))
- avoid changing the default network configuration, unless you are experienced with this
- avoid using IP addresses other than `127.0.0.1` (localhost) directly, as [they can change](https://github.com/photoprism/photoprism/discussions/2791#discussioncomment-3985376)
- only use `localhost` or `127.0.0.1` if the database port [has been exposed](https://docs.docker.com/compose/compose-file/compose-file-v3/#ports) as described below and you are on the same computer (host)
- we recommend [configuring a local hostname](https://dl.photoprism.app/img/docs/pihole-local-dns.png) to access other hosts on your network

To connect to MariaDB from your host or home network, you need to expose port `3306` in your `compose.yaml` or `docker-compose.yml`
and [restart the service for changes to take effect](../docker-compose.md#step-2-start-the-server):

```yaml
services:
  mariadb:
    ports:
      - "3306:3306"
```

!!! danger ""
    Set strong passwords if the database is exposed to an external network. Never expose your database to the public
    Internet in this way, for example, if it is running on a cloud server.

If this doesn't help, check the [Docker Logs](docker.md#viewing-logs) for messages like *disk full*, *disk quota exceeded*, *no space left on device*, *read-only file system*, *error creating path*, *wrong permissions*, *no route to host*, *connection failed*, *exec format error*, *no matching manifest*, and *killed*:

- [ ] Make sure that the database *storage* folder is readable and writable: Errors such as "read-only file system", "error creating path", "failed to create folder", "permission denied", or "wrong permissions" indicate a [filesystem permission problem](docker.md#file-permissions)
- [ ] If [symbolic links](https://en.wikipedia.org/wiki/Symbolic_link) are mounted or used within the *storage* folder, replace them with the actual paths and verify that they are accessible
- [ ] If the MariaDB service has been "killed" or otherwise automatically terminated, this can point to a [memory problem](docker.md#adding-swap) (add swap and/or memory; remove or increase usage limits)
- [ ] In case the logs also show "disk full", "quota exceeded", or "no space left" errors, either [the disk containing the *storage* folder is full](docker.md#disk-space) (add storage) or a disk usage limit is configured (remove or increase it)
- [ ] Log messages that contain "no route to host" may also indicate a general network configuration problem (follow our [examples](https://dl.photoprism.app/docker/))
- [ ] You have to resort to [alternative Docker images](../raspberry-pi.md#older-armv7-based-devices) to run MariaDB on ARMv7-based devices and those with a 32-bit operating system
- [ ] You may find a solution in the official [MariaDB Docker Image FAQ](https://mariadb.com/kb/en/docker-official-image-frequently-asked-questions/)

## Wrong Password

If the password you are using was specified in a `compose.yaml` or `docker-compose.yml` file and contains one or more `$` characters, these [must be escaped with `$$`](../../developer-guide/technologies/yaml.md#dollar-signs) (a double dollar sign) so that, for example, `"compo$e"` becomes `"compo$$e"`:


```yaml
services:
  mariadb:
    environment:
      # sets password to "compo$e"
      MARIADB_PASSWORD: "compo$$e"
```

Also note that you **cannot change the database password** with `MARIADB_PASSWORD` after MariaDB has been started for the first time.

In this case, you can either delete the database storage folder and restart the database service or follow the instructions under [Lost Root Password](#lost-root-password).

## Unsupported Scan

You may encounter errors similar to this when starting your instance or restoring a backup if you have manually configured the MariaDB database connection DSN, without [adding the necessary parameters](https://github.com/go-sql-driver/mysql?tab=readme-ov-file#parameters) such as `parseTime=true` to the `PHOTOPRISM_DATABASE_DSN` environment variable or the `--database-dsn` command flag:

```
sql: Scan error on column index 5 unsupported Scan,
storing driver.Value type []uint8 into type *time.Time
```

To avoid this issue, please use the [following configuration options](https://docs.photoprism.app/getting-started/config-options/#database-connection) to specify the MariaDB database name, server, user, and password:

- `PHOTOPRISM_DATABASE_NAME`
- `PHOTOPRISM_DATABASE_SERVER`
- `PHOTOPRISM_DATABASE_USER`
- `PHOTOPRISM_DATABASE_PASSWORD`

This will automatically generate a compatible Data Source Name (DSN) for connecting to your MariaDB database server. Since the required parameters may change in future versions, we recommend against setting the DSN manually unless it is for testing or development purposes. If you do need to set it manually, it should include the parameters `charset=utf8mb4,utf8&collation=utf8mb4_unicode_ci&parseTime=true`.

Users of [SQLite](sqlite.md) can specify the filename directly with the DSN config option, if necessary.

## Bad Performance

Many users reporting poor performance and high CPU usage have migrated from SQLite to MariaDB, so their database schema is no longer optimized for performance. For example, MariaDB cannot handle rows with `text` columns in memory and always uses temporary tables on disk if there are any.

The instructions for these migrations were provided by a contributor and are not part of the original software distribution. As such, they have not been officially released, recommended, or extensively tested by us.

If this is the case, please make sure that your migrated database schema matches that of a [fresh, non-migrated installation](../../developer-guide/database/index.md). It may help to [run the migrations manually](../advanced/migrations/index.md) in a terminal using the *migrations* subcommands. However, this does not guarantee that all issues such as missing indexes are resolved.

[Get Performance Tips ›](performance.md#mariadb){ class="pr-3 block-xs" } [View Database Schema ›](../../developer-guide/database/index.md)

## Version Upgrade

Should MariaDB fail to start after upgrading from an earlier version (or migrating from MySQL), the [internal management schema](https://mariadb.com/kb/en/understanding-mariadb-architecture/#system-databases) may be outdated. With older versions, it could only be updated manually.
However, newer MariaDB Docker images **support automatic upgrades** on startup, so you don't have to worry about that anymore.

!!! danger ""
    When upgrading from MariaDB 10.x to [11.0](https://mariadb.com/kb/en/release-notes-mariadb-11-0-series/), you [must replace](https://github.com/photoprism/photoprism/commit/bff649469d084498a1e75492c0bd99bda3f5a340#diff-03a31d6e73f48b7bba98b65352ce67a7d153fe2461f9c7b5e76be49a97ebf0cb) `command: mysqld` with `command: ` (followed by the command flags) in your `compose.yaml` or `docker-compose.yml` file, otherwise the database server may fail to start. 

### Manual Update

To manually upgrade the internal database schema, run this command in a terminal:

```bash
docker compose exec mariadb mariadb-upgrade -uroot -p
```

Enter the MariaDB "root" password specified in your `compose.yaml` or `docker-compose.yml` when prompted.

Alternatively, you can downgrade to the previous version, create a database backup using the `photoprism backup`
command, start a new database instance based on the latest version, and then restore your index with
the `photoprism restore` command.

### Auto Upgrade

To enable automatic schema updates, set `MARIADB_AUTO_UPGRADE` to a non-empty value in your `compose.yaml` or `docker-compose.yml` as shown in our [config example](https://dl.photoprism.app/docker/compose.yaml):

```yaml
services:
  mariadb:
    image: mariadb:11
    ...
    environment:
      MARIADB_AUTO_UPGRADE: "1"
      MARIADB_INITDB_SKIP_TZINFO: "1"
      ...
```

Before starting MariaDB in production mode, the database image entrypoint script now runs `mariadb-upgrade` to update the internal management schema as needed. For example, when you pull a new major release and restart the service.

!!! tldr ""
    Since PhotoPrism does not require time zone support, you can also add `MARIADB_INITDB_SKIP_TZINFO` to your config as shown above. However, this is only a recommendation and optional.

## Incompatible Schema

If your database does not seem to be compatible with the currently installed version of PhotoPrism, for example because search results are missing or incorrect, first make sure you are using a [supported database](../index.md#databases) and that its internal management schema is up-to-date. How to do that is explained in the [previous section](#version-upgrade).

Once you have verified that neither is a problem, you can run the following command [in a terminal](../docker-compose.md#command-line-interface) to check the status of previous database schema migrations:

```bash
docker compose exec photoprism photoprism migrations ls
```

!!! note ""
    Omit the `docker compose exec photoprism` prefix if you are using an interactive terminal session or are running PhotoPrism directly on your computer without Docker.

### Re-Run Migrations

Should the status of any migration not be OK, you can re-run failed migrations using this command in a terminal:

```bash
docker compose exec photoprism photoprism migrations run -f
```

The `-f` flag instructs the `photoprism migrations run` subcommand to re-run previously failed migrations. Use `--help` to see the command help.

Additional migration command examples can be found in the [Developer Guide](../../developer-guide/database/migrations.md).

### Complete Rescan

We recommend that you **re-index your pictures after a schema migration**, especially if problems persist. You can either start a [rescan from the user interface](../../user-guide/library/originals.md) by navigating to *Library* > *Index*, checking "Complete Rescan", and then clicking "Start", or by running this command in a terminal:

```bash
docker compose exec photoprism photoprism index -f
```

!!! tldr ""
    Be careful not to start multiple indexing processes at the same time, as this will lead to a high server load.

## Server Migration<a id="server-relocation"></a>

If you want to move your MariaDB database to another server or virtual machine:

- Read the [Creating Backups](../../user-guide/backups/index.md) chapter in our [User Guide](../../user-guide/index.md) for general information on [how to back up](../../user-guide/backups/index.md) and [restore your data](../../user-guide/backups/restore.md)
- We recommend that you [create a full backup](../../user-guide/backups/index.md) of all files before starting the server migration or making any other major changes
- Ideally, the MariaDB versions of both servers [should match](#version-upgrade) and the existing database files should [not be corrupted](#corrupted-files), e.g. due to an [unclean shutdown](#server-crashes)
- If your servers are not running on the [latest stable release](https://mariadb.org/mariadb/all-releases/), we recommend that you [update both](#version-upgrade) for the migration so that they are feature and binary compatible

To create a database backup:

- [ ] In case the MariaDB version and system architecture match, you can shut down your existing PhotoPrism instance and the database server, and then copy the [entire *database* storage folder](../../user-guide/backups/folders.md#database) without changing any file or folder permissions
- [ ] Alternatively, you can use the built-in [`photoprism backup -i -f`](../../user-guide/backups/index.md#backup-command) [CLI command](../docker-compose.md#opening-a-terminal), or backup the database with a [manually created SQL dump](https://mariadb.com/kb/en/mariadb-dump/) (backup file)
 
On the new server:
 
- [ ] If you copied the entire *database* storage folder, start the MariaDB server and make sure PhotoPrism can [access the new database](#cannot-connect) by updating its configuration or your network settings if necessary
- [ ] To restore the database from a backup dump ([either manually](https://mariadb.com/kb/en/restoring-data-from-dump-files/) or [using the `photoprism restore -i -f`](../../user-guide/backups/restore.md#restore-command) [CLI command](../docker-compose.md#opening-a-terminal)), the MariaDB server must be running and PhotoPrism must be restarted after the backup has been restored
- [ ] Be sure to [never expose your database](#cannot-connect) to the public Internet, and [use strong passwords](#wrong-password) if the database is exposed to an external network

## Server Crashes

If the server crashes unexpectedly or your database files get corrupted frequently, it is usually because they are stored on an unreliable device such as a USB flash drive, an SD card, or a shared network folder mounted via NFS or CIFS. These may also have [unexpected file size limitations](https://thegeekpage.com/fix-the-file-size-exceeds-the-limit-allowed-and-cannot-be-saved/), which is especially problematic for databases that do not split data into smaller files.

- [ ] Never use the same database files with more than one server instance
- [ ] To share a database over a network, run the database server directly on the remote server instead of sharing database files
- [ ] To repair your tables after you have moved the files to a local disk, you can [start MariaDB with `--innodb-force-recovery=1`](https://mariadb.com/kb/en/innodb-recovery-modes/) (otherwise the same procedure as for recovering a lost password, see above)
- [ ] Make sure you are using the latest Docker version and read the release notes for the database server version you are using

## Invalid Table Errors

If you are using macOS and see errors like `Invalid (old?) table or database name '._column_stats'`, it may be because you are running MariaDB on a file system like ExFAT that does not support extended attributes. In this case, macOS automatically creates these files and MariaDB then reports them as invalid tables (which is technically correct). To remove extended attribute files, you can run the following in a terminal:

```
find . -type f -name '._*' -delete
```

Unless you open the storage folder again in macOS Finder, the errors should then be gone after restarting the database.

## Corrupted Files

Most database table and/or index corruptions are hardware-related. Corrupted page writes can be caused by power failures or bad memory. The problem can also be caused by using network attached storage (NAS) and placing InnoDB databases on it.

↪ [Server Crashes](#server-crashes)

## Lost Root Password

In case you forgot the MariaDB "root" password and the one specified in your configuration does not work,
you can [start the server with the `--skip-grant-tables` flag](https://mariadb.com/docs/reference/mdb/cli/mariadbd/skip-grant-tables/)
added to the `mysqld` command in your `compose.yaml` or `docker-compose.yml`. This will temporarily give full access
to all users after a restart:

```yaml
services:
  mariadb:
    command: --skip-grant-tables
```

Restart the `mariadb` service for changes to take effect:

```bash
docker compose stop mariadb
docker compose up -d mariadb
```

Now open a database console:

```bash
docker compose exec mariadb mysql -uroot
```

Enter the following commands to change the password for "root":

```sql
FLUSH PRIVILEGES;
ALTER USER 'root'@'%' IDENTIFIED BY 'new_password';
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
exit
```

When you are done, remove the `--skip-grant-tables` flag again to restore the original
command and restart the `mariadb` service as described above.

## Unicode Support

If the logs show "incorrect string value" database errors and you are running a custom MariaDB or MySQL
server that is not based on our [default configuration](https://dl.photoprism.app/docker/compose.yaml):

- [ ] Full [Unicode](https://home.unicode.org/basic-info/faq/) support [must be enabled](https://mariadb.com/kb/en/setting-character-sets-and-collations/#example-changing-the-default-character-set-to-utf-8), e.g. using the `mysqld` command parameters `--character-set-server=utf8mb4` and `--collation-server=utf8mb4_unicode_ci`
- [ ] Note that an existing database may use a different character set if you imported it from another server
- [ ] Before submitting a support request, verify the problem still occurs with a newly created database based on our example

Run this command in a terminal to see the current values of the collation and character set variables (change the root
password `insecure` and database name `photoprism` as specified in your `compose.yaml` or `docker-compose.yml`):

```bash
echo "SHOW VARIABLES WHERE Variable_name LIKE 'character\_set\_%' OR Variable_name LIKE 'collation%';" | \
docker compose exec -T mariadb mysql -uroot -pinsecure photoprism
```

## MySQL Errors

Official [support for MySQL 8 is discontinued](../index.md#databases) as Oracle seems to have stopped shipping [new features and enhancements](https://github.com/photoprism/photoprism/issues/1764).
As a result, the testing effort required before each release is no longer feasible.

*[SQLite]: self-contained, serverless SQL database
