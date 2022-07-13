# Advanced Database Setup

PhotoPrism is compatible with [SQLite 3](https://www.sqlite.org/) and [MariaDB 10.5.12+](https://mariadb.org/).
Older databases using the same dialect, such as MySQL 8, may work but are not officially supported.

Never store database files on an unreliable device such as a USB flash drive, SD card, or shared network folder. These may also have [unexpected file size limitations](https://thegeekpage.com/fix-the-file-size-exceeds-the-limit-allowed-and-cannot-be-saved/), which is especially problematic for databases that do not split data into smaller files.

!!! info
    Our [docker-compose.yml](https://dl.photoprism.app/docker/) examples include
    tested and working database configurations. These docs are for advanced users only.

!!! note "MySQL"
    Official support for MySQL 8 is discontinued as Oracle seems to have stopped shipping [new features and improvements](https://github.com/photoprism/photoprism/issues/1764).
    As a result, the testing effort required before each release is no longer feasible.

## Configuring MariaDB ##

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

## Manual Schema Migrations

An index schema migration is performed automatically when PhotoPrism starts. The following instructions may be helpful in special cases, such as when a temporary issue has prevented a successful migration:

↪ [Performing Index Migrations](migrations/index.md)

## Migrating to a Different Database

↪ [from SQLite to MariaDB](migrations/sqlite-to-mariadb.md)

↪ [from MariaDB to SQLite](migrations/mariadb-to-sqlite.md)

!!! warning "Performance Issues"
    After migrating, it is possible that columns do not have exactly the data type they should have or that indexes are missing. This can lead to poor performance. For example, MariaDB cannot process rows with `text` columns in memory and always uses temporary tables on disk if there are any. If this is the case, please make sure that your migrated database schema matches that of a fresh, non-migrated installation, e.g. by re-running the migrations manually in a terminal with the `photoprism migrations ls` and `photoprism migrations run [id]` subcommands.
