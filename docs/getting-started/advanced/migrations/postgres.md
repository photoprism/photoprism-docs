# Using PostgreSQL (Experimental)

!!! warning "Experimental"
    PostgreSQL support is **experimental**. The database schema may still change without migrations, so you should not use it for a library you depend on, and you should keep [backups](../../../user-guide/backups/index.md) of your originals and sidecar files.

In addition to [MariaDB and SQLite](../../index.md#databases), PhotoPrism can use [PostgreSQL](https://www.postgresql.org/) 16 or later as index database. We test with PostgreSQL 18.

## Setting Up a New Instance

PhotoPrism creates the tables when it starts with an empty database. To use PostgreSQL with Docker Compose, add a `postgres` service to your `compose.yaml` and configure the `photoprism` service to use it, for example:

```yaml
services:
  photoprism:
    image: photoprism/photoprism:latest
    depends_on:
      - postgres
    environment:
      PHOTOPRISM_DATABASE_DRIVER: "postgres"
      PHOTOPRISM_DATABASE_SERVER: "postgres:5432"
      PHOTOPRISM_DATABASE_NAME: "photoprism"
      PHOTOPRISM_DATABASE_USER: "photoprism"
      PHOTOPRISM_DATABASE_PASSWORD: "insecure"
      ...

  postgres:
    image: postgres:18-alpine
    restart: unless-stopped
    stop_grace_period: 15s
    volumes:
      - "./database:/var/lib/postgresql"
    environment:
      POSTGRES_DB: "photoprism"
      POSTGRES_USER: "photoprism"
      POSTGRES_PASSWORD: "insecure"
      POSTGRES_INITDB_ARGS: "--locale-provider=icu --icu-locale=und"
      PGDATA: "/var/lib/postgresql/18/docker"
```

Please change the password before you start the services for the first time, and use the same value in both places.

Store the database files in a folder on a local SSD, as shown above, rather than in a named or anonymous Docker volume, which can lead to data loss when the container is recreated. The mount path depends on the PostgreSQL version, see [Server Does Not Start](#server-does-not-start).

`POSTGRES_INITDB_ARGS` only takes effect when the database server is initialized, i.e. when its storage folder is still empty. The ICU locale `und` makes PostgreSQL sort names and titles in the same order as MariaDB. Without it, the sort order depends on the default locale of the server, which differs between images based on Alpine Linux and Debian.

## Differences From MariaDB

- File and folder names must be valid UTF-8. Files whose names contain invalid characters cannot be indexed, while MariaDB and SQLite accept them.
- Lists sorted by name or title follow the collation of the database, see above.
- We have not yet compared the performance with MariaDB.

## Backups

The [`photoprism backup`](../../../user-guide/backups/index.md#backup-command) and [`photoprism restore`](../../../user-guide/backups/restore.md#restore-command) commands work with PostgreSQL as well, using the `pg_dump` and `psql` clients included in our Docker images. An index backup created from PostgreSQL can only be restored into a PostgreSQL database. A restore is applied as a whole: if one statement fails, the database remains unchanged and the command reports the error.

## Troubleshooting

### Cannot Connect

In the internal Docker network, the database server's hostname is the name of its service, e.g. `postgres`, and the default port is `5432`. `localhost` and `127.0.0.1` point to the PhotoPrism container itself, so use the service name instead. Check the [logs](../../troubleshooting/docker.md#viewing-logs) of both services for errors such as *permission denied* or *no space left on device*.

To connect from your host, e.g. with a database client, you can publish the port in the `postgres` service and restart it:

```yaml
services:
  postgres:
    ports:
      - "127.0.0.1:5432:5432"
```

!!! danger ""
    Never expose your database to the public Internet, and set strong passwords if it is reachable from other computers on your network.

### Server Does Not Start

The official `postgres` Docker images changed their data folder with PostgreSQL 18:

| Version        | Mount Path                 | Data Folder                     |
|----------------|----------------------------|---------------------------------|
| 18+            | `/var/lib/postgresql`      | `/var/lib/postgresql/18/docker` |
| 17 and earlier | `/var/lib/postgresql/data` | `/var/lib/postgresql/data`      |

If a PostgreSQL 18 container finds a volume mounted at `/var/lib/postgresql/data`, e.g. because you only changed the image tag of an existing service, it exits and logs an error that starts with:

```
Error: in 18+, these Docker images are configured to store database data in a
       format which is compatible with "pg_ctlcluster" (specifically, using
       major-version-specific directory names).
```

This also happens if the mounted folder is empty. Change the mount path to `/var/lib/postgresql`. Setting `PGDATA` as in the [example above](#setting-up-a-new-instance) keeps the data folder at a fixed location; it contains the major version, so change it together with the image tag when you [upgrade](#version-upgrade). If the folder contains the database of an older version, you also need to [upgrade it](#version-upgrade), since PostgreSQL 18 cannot use those files.

### Wrong Password

If a password in your `compose.yaml` contains `$` characters, these [must be escaped with `$$`](../../../developer-guide/technologies/yaml.md#dollar-signs), so that, for example, `"compo$e"` becomes `"compo$$e"`.

`POSTGRES_PASSWORD` only sets the password when the database server is started with an empty storage folder for the first time. To change it later, open a database console and set a new password, then update `PHOTOPRISM_DATABASE_PASSWORD` accordingly:

```bash
docker compose exec postgres psql -U photoprism -c "ALTER USER photoprism WITH PASSWORD 'new_password';"
```

### Version Upgrade

A new major version of PostgreSQL cannot use the database files of an older one. To upgrade, e.g. from PostgreSQL 17 to 18, create an index backup with [`photoprism backup -i`](../../../user-guide/backups/index.md#backup-command), start the new version with an empty storage folder, and then restore the backup with [`photoprism restore -i -f`](../../../user-guide/backups/restore.md#restore-command). The same steps move your database to another server. Restart PhotoPrism after the backup has been restored.

## Moving an Existing Library

The `photoprism database transfer` command copies an existing MariaDB or SQLite index to PostgreSQL, including users, sessions, and settings. It works between all three kinds of database, so you can also use it to move back later. An [index backup](../../../user-guide/backups/index.md#backup-command) can only be restored into the same kind of database, so it is not an alternative for this.

1. Create an [index backup](../../../user-guide/backups/index.md#backup-command) with `photoprism backup -i`, so you can return to your current database if needed.
2. Add a `postgres` service to your `compose.yaml` as shown [above](#setting-up-a-new-instance), but leave the database settings of the `photoprism` service unchanged for now. Then start the new service with `docker compose up -d postgres`.
3. Stop PhotoPrism with `docker compose stop photoprism`, since changes made during the transfer would be missing in the new database.
4. Run the transfer in a new container, using the values of your `postgres` service:

    ```bash
    docker compose run --rm photoprism photoprism database transfer --target-driver postgres --target-server postgres:5432 --target-name photoprism --target-user photoprism --target-password insecure
    ```

5. Change the `PHOTOPRISM_DATABASE_*` settings of the `photoprism` service to the PostgreSQL values shown [above](#setting-up-a-new-instance), and start it again with `docker compose up -d`.

The target database must be empty. If PhotoPrism has already been started with it, the command refuses to run unless you pass `--force`, which replaces its data. If the transfer fails, the target is emptied again, so you can fix the cause and run the command once more. If the target server rejects large statements, lower the number of rows copied per statement with `--batch`, e.g. `--batch 100`.

Instead of moving your index, you can also set up a new instance as shown above and index your originals. Photo edits that PhotoPrism has saved to [YAML sidecar files](../../../user-guide/backups/export.md#photo-backups) are restored automatically, and [album backups](../../../user-guide/backups/export.md#album-backups) can be restored with `photoprism restore -a`.

## Databases From Development Versions

Databases that were created with development versions of the PostgreSQL support, e.g. from [pull request #4831](https://github.com/photoprism/photoprism/pull/4831), use a different schema and cannot be upgraded. PhotoPrism does not use such a database and logs this error instead:

```
database was created by an unsupported development version of PostgreSQL support, please create a new database and index your originals again
```

To continue, create a new, empty database, e.g. with `CREATE DATABASE` or a new `postgres` service, and configure PhotoPrism to use it. Keep the *storage* folder, which contains your [YAML sidecar files](../../../user-guide/backups/export.md#photo-backups) and [album backups](../../../user-guide/backups/export.md#album-backups). To make sure the album backups are up to date, you can run this command with the development version before you switch:

```bash
photoprism backup -a
```

When the new version starts with the empty database, it restores your albums from the album backups, and when you then index your originals, your photo edits are restored from the YAML sidecar files, provided backups were not disabled. If albums are missing afterwards, e.g. because the backups are in another folder, you can restore them with:

```bash
photoprism restore -a
```
