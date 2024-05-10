# Database Schema

!!! example ""
    This schema description is **for illustrative purposes only** and should not be used to update or replace an existing production database.

## Entity Relationships

↪ [Entity-Relationship Diagram](schema.md)

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

Note that the dump we provide is only updated at irregular intervals and should therefore not be used to update or replace an existing production database.
