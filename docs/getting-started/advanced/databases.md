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
FLUSH PRIVILEGES;
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
    unless you're using our [docker-compose.yml](https://dl.photoprism.app/docker/docker-compose.yml)
    example without modifications.

## Database Migrations ##

*Note: This is contributed content intended for advanced users. If you find any errors or want to improve something, click :material-pencil: to make changes and send a pull request.*

### MariaDB to Sqlite ###

- Install <https://github.com/techouse/mysql-to-sqlite3> on your host.
- Stop Photoprism: `docker-compose stop photoprism`
- Add the port to the MariaDB service
- On the **host** now run `sudo mysql2sqlite -f <PATH_TO_STORAGE_MOUNT>/storage/index.db -d photoprism -u root --mysql-password 'insecure'`
- Shutdown your current stack fully: `docker-compose down`
- Edit your `docker-compose.yml`:
  - Remove the MariaDB service.
  - Change in the Photoprism settings to use the sqlite driver and remove the other database settings
- Start your stack again with `docker-compose up -d`
- If this worked you may want to delete the old mountpoint for the MariaDB database.

### Sqlite to MariaDB ###

- Install <https://github.com/techouse/sqlite3-to-mysql> on your host. (openSUSE: `zypper in python-sqlite3-to-mysql`)
- Shutdown your current stack: `docker-compose down`
- Add the current snippet of the MariaDB to your Sqlite Photoprism Docker-Compose with the addition of the extra `ports`
  section where you expose port 3306 to the Host. In my case this looked like attachment 1.
- Start the stack again: `docker-compose up -d`
- Stop Photoprism: `docker-compose stop photoprism`
- On the **host** now run `sudo sqlite3mysql -f <PATH_TO_STORAGE_MOUNT>/storage/index.db -d photoprism -u root --mysql-password 'insecure'`
- Shutdown your current stack again: `docker-compose down`
- Edit your `docker-compose.yml` so it uses the MariaDB database you added before. Don't forget to remove the `ports`
  section of the MariaDB Container.
- Start your stack again with `docker-compose up -d`
- If this worked you may want to delete the file `index.db` in the `storage` mount since it contains out of date
  information.

Attachment 1:

```yaml
services:
  mariadb:
    restart: unless-stopped
    image: mariadb:10.8
    ports:
      - 3306:3306 # Expose Port 3306 
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
    command: mysqld --innodb-buffer-pool-size=1G --transaction-isolation=READ-COMMITTED --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --max-connections=512 --innodb-rollback-on-timeout=OFF --innodb-lock-wait-timeout=120
    volumes:
      - "./database:/var/lib/mysql" # DO NOT REMOVE
    environment:
      MARIADB_AUTO_UPGRADE: "1"
      MARIADB_INITDB_SKIP_TZINFO: "1"
      MARIADB_DATABASE: "photoprism"
      MARIADB_USER: "photoprism"
      MARIADB_PASSWORD: "insecure"
      MARIADB_ROOT_PASSWORD: "insecure"
```

!!! danger ""
    Set strong passwords if the database is exposed to an external network. Never expose your database to the public
    Internet in this way, for example, if it is running on a cloud server.
