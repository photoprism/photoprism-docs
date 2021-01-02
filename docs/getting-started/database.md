# Database

Photoprism supports the following database types:

- SQLite 3
- MariaDB 10
- MySQL 8

## MySQL / MariaDB Setup

> Note: These instructions were only tested on MariaDB 10.

When creating a new database on your database server, be sure to set
the charset and collation as follows:

```sql
CREATE DATABASE photoprism
CHARACTER SET = 'utf8mb4'
COLLATE = 'utf8mb4_unicode_ci';
```

Now create a user and grant privileges for this new database:

```sql
CREATE USER 'photoprism'@'%' IDENTIFIED BY 'db-password-here';
GRANT ALL PRIVILEGES ON photoprism.* to 'photoprism'@'%';
```

Set your database DSN in Photoprism as follows:

`photoprism:db-password-here@tcp(my-db-server:3307)/photoprism?charset=utf8mb4,utf8&parseTime=true`
