# Troubleshooting PostgreSQL Problems

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://www.photoprism.app/membership) receive direct [technical support](https://www.photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to [determine the cause of your problem](index.md).

## Compatibility

PhotoPrism is compatible with [SQLite 3](https://www.sqlite.org/), [MariaDB 10.5.12+](https://mariadb.org/) and [PostgreSQL 17.4+](https://www.postgresql.org/).
Official support for MySQL 8 is discontinued as Oracle seems to have stopped shipping [new features and enhancements](https://github.com/photoprism/photoprism/issues/1764).
As a result, the testing effort required before each release is no longer feasible.

Our [configuration examples](https://dl.photoprism.app/docker/) are generally based on the [current stable version](https://www.postgresql.org/about/newsarchive/pgsql/) to take advantage of performance improvements. This does not mean that [older versions](../index.md#databases) are no longer supported and you must upgrade immediately. We recommend not using the `:latest` tag for the PostgreSQL Docker image and to upgrade manually by changing the tag once we had a chance to test a new major version, e.g.:

```yaml
services:
  postgres:
    image: postgres:17-alpine
    ...
```

## Cannot Connect

First, verify that you are using the correct port (default is `5432`) and host:

- in the internal Docker network, the default hostname is `postgresql` (same as the [service](https://dl.photoprism.app/docker/compose.yaml))
- avoid changing the default network configuration, unless you are experienced with this
- avoid using IP addresses other than `127.0.0.1` (localhost) directly, as [they can change](https://github.com/photoprism/photoprism/discussions/2791#discussioncomment-3985376)
- only use `localhost` or `127.0.0.1` if the database port [has been exposed](https://docs.docker.com/compose/compose-file/compose-file-v3/#ports) as described below and you are on the same computer (host)
- we recommend [configuring a local hostname](https://dl.photoprism.app/img/docs/pihole-local-dns.png) to access other hosts on your network

To connect to PostgreSQL from your host or home network, you need to expose port `5432` in your `compose.yaml` or `docker-compose.yml`
and [restart the service for changes to take effect](../docker-compose.md#step-2-start-the-server):

```yaml
services:
  postgres:
    ports:
      - "5432:5432"
```

!!! danger ""
    Set strong passwords if the database is exposed to an external network. Never expose your database to the public
    Internet in this way, for example, if it is running on a cloud server.

If this doesn't help, check the [Docker Logs](docker.md#viewing-logs) for messages like *disk full*, *disk quota exceeded*, *no space left on device*, *read-only file system*, *error creating path*, *wrong permissions*, *no route to host*, *connection failed*, *exec format error*, *no matching manifest*, and *killed*:

- [ ] Make sure that the database *storage* folder is readable and writable: Errors such as "read-only file system", "error creating path", "failed to create folder", "permission denied", or "wrong permissions" indicate a [filesystem permission problem](docker.md#file-permissions)
- [ ] If [symbolic links](https://en.wikipedia.org/wiki/Symbolic_link) are mounted or used within the *storage* folder, replace them with the actual paths and verify that they are accessible
- [ ] If the PostgreSQL service has been "killed" or otherwise automatically terminated, this can point to a [memory problem](docker.md#adding-swap) (add swap and/or memory; remove or increase usage limits)
- [ ] In case the logs also show "disk full", "quota exceeded", or "no space left" errors, either [the disk containing the *storage* folder is full](docker.md#disk-space) (add storage) or a disk usage limit is configured (remove or increase it)
- [ ] Log messages that contain "no route to host" may also indicate a general network configuration problem (follow our [examples](https://dl.photoprism.app/docker/))
- [ ] You have to resort to [alternative Docker images](../raspberry-pi.md#older-armv7-based-devices) to run PostgreSQL on ARMv7-based devices and those with a 32-bit operating system
- [ ] You may find a solution in the official [PostgreSQL Docker Hub page](https://hub.docker.com/_/postgres/)

## Wrong Password

If the password you are using was specified in a `compose.yaml` or `docker-compose.yml` file and contains one or more `$` characters, these [must be escaped with `$$`](../../developer-guide/technologies/yaml.md#dollar-signs) (a double dollar sign) so that, for example, `"compo$e"` becomes `"compo$$e"`:


```yaml
services:
  postgres:
    environment:
      # sets password to "compo$e"
      POSTGRES_PASSWORD: "compo$$e"
```

Also note that you **cannot change the database password** with `POSTGRES_PASSWORD` after PostgreSQL has been started for the first time.

In this case, you can either delete the database storage folder and restart the database service or follow the instructions under [Lost Root Password](#lost-root-password).

## Incompatible Schema

If your database does not seem to be compatible with the currently installed version of PhotoPrism, for example because search results are missing or incorrect, first make sure you are using a [supported database](../index.md#databases).

Once you have verified that is not a problem, you can run the following command [in a terminal](../docker-compose.md#command-line-interface) to check the status of previous database schema migrations:

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

If you want to move your PostgreSQL database to another server or virtual machine:

- Read the [Creating Backups](../../user-guide/backups/index.md) chapter in our [User Guide](../../user-guide/index.md) for general information on [how to back up](../../user-guide/backups/index.md) and [restore your data](../../user-guide/backups/restore.md)
- We recommend that you [create a full backup](../../user-guide/backups/index.md) of all files before starting the server migration or making any other major changes
- Ideally, the PostgreSQL versions of both servers [should match](#version-upgrade) and the existing database files should [not be corrupted](#corrupted-files), e.g. due to an [unclean shutdown](#server-crashes)
- If your servers are not running on the [latest stable release](https://www.postgresql.org/about/newsarchive/pgsql/), we recommend that you [update both](#version-upgrade) for the migration so that they are feature and binary compatible

To create a database backup:

- [ ] In case the PostgreSQL version and system architecture match, you can shut down your existing PhotoPrism instance and the database server, and then copy the [entire *database* storage folder](../../user-guide/backups/folders.md#database) without changing any file or folder permissions
- [ ] Alternatively, you can use the built-in [`photoprism backup -i -f`](../../user-guide/backups/index.md#backup-command) [CLI command](../docker-compose.md#opening-a-terminal), or backup the database with a [manually created SQL dump](https://www.postgresql.org/docs/current/backup-dump.html) (backup file)
 
On the new server:
 
- [ ] If you copied the entire *database* storage folder, start the PostgreSQL server and make sure PhotoPrism can [access the new database](#cannot-connect) by updating its configuration or your network settings if necessary
- [ ] To restore the database from a backup dump ([either manually](https://www.postgresql.org/docs/current/backup-dump.html#BACKUP-DUMP-RESTORE) or [using the `photoprism restore -i -f`](../../user-guide/backups/restore.md#restore-command) [CLI command](../docker-compose.md#opening-a-terminal)), the PostgreSQL server must be running and PhotoPrism must be restarted after the backup has been restored
- [ ] Be sure to [never expose your database](#cannot-connect) to the public Internet, and [use strong passwords](#wrong-password) if the database is exposed to an external network

## Server Crashes

If the server crashes unexpectedly or your database files get corrupted frequently, it is usually because they are stored on an unreliable device such as a USB flash drive, an SD card, or a shared network folder mounted via NFS or CIFS. These may also have [unexpected file size limitations](https://thegeekpage.com/fix-the-file-size-exceeds-the-limit-allowed-and-cannot-be-saved/), which is especially problematic for databases that do not split data into smaller files.

- [ ] Never use the same database files with more than one server instance
- [ ] To share a database over a network, run the database server directly on the remote server instead of sharing database files
- [ ] Make sure you are using the latest Docker version and read the release notes for the database server version you are using

## Corrupted Files

Most database table and/or index corruptions are hardware-related. Corrupted page writes can be caused by power failures or bad memory. The problem can also be caused by using network attached storage (NAS) and placing PostgreSQL databases on it.

↪ [Server Crashes](#server-crashes)

## Lost photoprism user Password

In case you forgot the PostgreSQL "photoprism" password and the one specified in your configuration does not work,
you can reset the password via the `psql` and docker commands.

The following assumes that your config has not changed the compose setting below.

```yaml
services:
  postgres:
    environment:
      POSTGRES_USER: photoprism
```

Open a database console:

```bash
docker compose exec postgres psql -U photoprism
```

Enter the following commands to change the password for "photoprism":

```sql
ALTER USER photoprism WITH PASSWORD 'new_password';
exit
```
