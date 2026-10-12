# Using PostgreSQL (Experimental)

!!! warning "Development Preview"
    PostgreSQL support is **experimental** and only available in our [development preview](../../updates.md#development-preview) builds, so it does not work with the current stable release yet. The database schema may still change without migrations, so you should not use it for a library you depend on, and you should keep [backups](../../../user-guide/backups/index.md) of your originals and sidecar files.

In addition to [MariaDB and SQLite](../../index.md#databases), our preview builds can use [PostgreSQL](https://www.postgresql.org/) 16 or later as index database. We test with PostgreSQL 18.

## Setting Up a New Instance

PhotoPrism creates the tables when it starts with an empty database. To use PostgreSQL with Docker Compose, add a `postgres` service to your `compose.yaml` and configure the `photoprism` service to use it, for example:

```yaml
services:
  photoprism:
    image: photoprism/photoprism:preview
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
```

Please change the password before you start the services for the first time, and use the same value in both places.

`POSTGRES_INITDB_ARGS` only takes effect when the database server is initialized, i.e. when its storage folder is still empty. The ICU locale `und` makes PostgreSQL sort names and titles in the same order as MariaDB. Without it, the sort order depends on the default locale of the server, which differs between images based on Alpine Linux and Debian.

## Differences From MariaDB

- File and folder names must be valid UTF-8. Files whose names contain invalid characters cannot be indexed, while MariaDB and SQLite accept them.
- Lists sorted by name or title follow the collation of the database, see above.
- We have not yet compared the performance with MariaDB.

## Backups

The [`photoprism backup`](../../../user-guide/backups/index.md#backup-command) and [`photoprism restore`](../../../user-guide/backups/restore.md#restore-command) commands work with PostgreSQL as well, using the `pg_dump` and `psql` clients included in our Docker images. An index backup created from PostgreSQL can only be restored into a PostgreSQL database. A restore is applied as a whole: if one statement fails, the database remains unchanged and the command reports the error.

## Moving an Existing Library

There is currently no command to move an existing MariaDB or SQLite index to PostgreSQL. To try PostgreSQL with your pictures, set up a new instance as shown above and index your originals. Photo edits that PhotoPrism has saved to [YAML sidecar files](../../../user-guide/backups/export.md#photo-backups) are restored automatically, and [album backups](../../../user-guide/backups/export.md#album-backups) can be restored with `photoprism restore -a`.

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
