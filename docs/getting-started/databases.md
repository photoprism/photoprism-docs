# Advanced Database Setup

PhotoPrism is compatible with [MariaDB 10](https://mariadb.org/),
[MySQL 8](https://www.mysql.com/), and [SQLite 3](https://www.sqlite.org/).

!!! info
    Our [docker-compose.yml](https://dl.photoprism.org/docker/) examples include
    tested and working database configurations. These docs are for advanced users only.

## MariaDB ##

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
```

Set the database environment variables for PhotoPrism as follows:

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_DATABASE_DRIVER: "mysql"
      PHOTOPRISM_DATABASE_SERVER: "mariadb:3306"
      PHOTOPRISM_DATABASE_NAME: "photoprism"
      PHOTOPRISM_DATABASE_USER: "photoprism"
      PHOTOPRISM_DATABASE_PASSWORD: "insecure"
```

!!! note
    `mariadb:3306` needs to be replaced with the actual database server host and port, 
    unless you're using our [docker-compose.yml](https://dl.photoprism.org/docker/docker-compose.yml)
    example without modifications.