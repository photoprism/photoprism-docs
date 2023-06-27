# Advanced Database Setup

*Note that this guide is intended for advanced users and that our [docker-compose.yml examples](https://dl.photoprism.app/docker/) already contain a tested and working database configuration. You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.*

## Compatibility

PhotoPrism is compatible with [SQLite 3](https://www.sqlite.org/) and [MariaDB 10.5.12+](https://mariadb.org/).
Official support for MySQL 8 is discontinued as Oracle seems to have stopped shipping [new features and enhancements](https://github.com/photoprism/photoprism/issues/1764).
As a result, the testing effort required before each release is no longer feasible.

Our [configuration examples](https://dl.photoprism.app/docker/) are generally based on the [current stable version](https://mariadb.com/kb/en/mariadb-server-release-dates/) to take advantage of performance improvements. This does not mean that [older versions](../index.md#databases) are no longer supported and you must upgrade immediately. We recommend not using the `:latest` tag for the MariaDB Docker image and to upgrade manually by changing the tag once we had a chance to test a new major version.

## Storage

Local Solid-State Drives (SSDs) are [best for databases](../troubleshooting/performance.md#storage) of any kind. Never store database files on an unreliable device such as a USB flash drive, SD card, or shared network folder. These may also have [unexpected file size limitations](https://thegeekpage.com/fix-the-file-size-exceeds-the-limit-allowed-and-cannot-be-saved/), which is especially problematic for databases that do not split data into smaller files.

## Configuration ##

When creating a new database, make sure to set the charset and collation as follows:

```sql
CREATE DATABASE photoprism
CHARACTER SET = 'utf8mb4'
COLLATE = 'utf8mb4_unicode_ci';
```

Now create a user and grant privileges for this new database:

```sql
CREATE USER 'photoprism'@'%' IDENTIFIED BY 'insecure';
GRANT ALL PRIVILEGES ON photoprism.* to 'photoprism'@'%';
FLUSH PRIVILEGES;
```

Set the database environment variables for PhotoPrism and MariaDB as follows:

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_DATABASE_DRIVER: "mysql"
      PHOTOPRISM_DATABASE_SERVER: "mariadb:3306"
      PHOTOPRISM_DATABASE_NAME: "photoprism"
      PHOTOPRISM_DATABASE_USER: "photoprism"
      PHOTOPRISM_DATABASE_PASSWORD: "insecure"

  mariadb:
    environment:
      MARIADB_AUTO_UPGRADE: "1"
      MARIADB_INITDB_SKIP_TZINFO: "1"
      MARIADB_DATABASE: "photoprism"
      MARIADB_USER: "photoprism"
      MARIADB_PASSWORD: "insecure"
      MARIADB_ROOT_PASSWORD: "insecure"
```

!!! danger ""
    Set strong passwords if the database is exposed to an external network. Never expose your database to the public Internet in this way, for example, if it is running on a cloud server.

## Schema Migrations

An index schema migration is performed automatically every time PhotoPrism is (re)started. The following instructions may be helpful in special cases, such as when a temporary problem has prevented a successful migration:

[Run Migrations ›](migrations/index.md)

## Change Database

[Migrate from SQLite to MariaDB ›](migrations/sqlite-to-mariadb.md)

[Migrate from MariaDB to SQLite ›](migrations/mariadb-to-sqlite.md)

!!! warning "Bad Performance"
    Many users reporting poor performance and high CPU usage have migrated from SQLite to MariaDB, so their database schema is no longer optimized for performance. For example, MariaDB cannot handle rows with `text` columns in memory and always uses temporary tables on disk if there are any.

    If this is the case, please make sure that your migrated database schema matches that of a fresh, non-migrated installation. It may help to [run the migrations manually](../advanced/migrations/index.md) in a terminal using the *migrations* subcommands. However, this does not guarantee that all issues such as missing indexes are resolved.

    Due to the amount of time required to review each report, we can only offer this to [eligible members](https://www.photoprism.app/membership) and [business customers](https://www.photoprism.app/teams), and not to users who have chosen our free community edition.

    [Get Performance Tips ›](../troubleshooting/performance.md#mariadb){ class="pr-3 block-xs" } [View Database Schema ›](../../developer-guide/database/index.md) 

