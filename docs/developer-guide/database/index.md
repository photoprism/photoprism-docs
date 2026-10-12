# Database Schema

!!! example ""
    This schema description is **for illustrative purposes only** and should not be used to update or replace an existing production database.

## Entity-Relationship Diagram

↪ [docs.photoprism.app/developer-guide/database/schema/](schema.md)

## Mermaid Markup

With [Mermaid.js](https://mermaid-js.github.io/) you can generate visual diagrams from this markup file:

↪ [mariadb.mmd](https://github.com/photoprism/photoprism/blob/develop/internal/entity/schema/mariadb.mmd)

## MariaDB SQL Dump

An SQL schema dump can be created using the command shown below, for example:

↪ [mariadb.sql](https://raw.githubusercontent.com/photoprism/photoprism/develop/internal/entity/schema/mariadb.sql)

If you need an updated dump, you can run this command in your [development environment](../setup.md):

```bash
mariadb-dump --no-data --skip-add-locks --skip-comments \
 --skip-opt --skip-set-charset photoprism > mariadb.sql
```

Please note that the dump we provide is only updated at irregular intervals and should therefore not be used to update or replace an existing production database.

## PostgreSQL (Experimental)

Development builds can also use PostgreSQL 16 or later as database; we test with PostgreSQL 18. To try it in the [development environment](../setup.md), start the optional `postgres` service with `docker compose --profile postgres up -d`. Then run this command in a [terminal](../setup.md) to start PhotoPrism with it, since `compose.yaml` configures MariaDB by default:

```bash
./photoprism --database-driver=postgres --database-server=postgres:4002 \
 --database-user=photoprism start
```

The schema is created by [GORM](https://gorm.io/) from the models in [`internal/entity`](https://github.com/photoprism/photoprism/tree/develop/internal/entity) and differs from MariaDB in a few ways:

- Columns that are `VARBINARY` on MariaDB, such as UIDs, paths, and hashes, are `varchar` with the `"C"` collation, so they compare and sort byte by byte. They cannot hold invalid UTF-8, so a file name that is not valid UTF-8 cannot be indexed.
- Other text columns use the database collation, and `=` compares them case-sensitively. For a sort order similar to MariaDB's, create the database with an ICU locale, e.g. `POSTGRES_INITDB_ARGS="--locale-provider=icu --icu-locale=und"` for a new server.
- Timestamps are `timestamptz` and are read in UTC.

Since the schema may still change without migrations, databases created with earlier development versions are not upgraded. If PhotoPrism refuses to start because of an unsupported schema, create a new database and index your originals again.

## Schema Migrations

↪ [docs.photoprism.app/developer-guide/database/migrations/](migrations.md)

↪ [github.com/photoprism/photoprism/tree/develop/internal/entity/migrate](https://github.com/photoprism/photoprism/tree/develop/internal/entity/migrate)
