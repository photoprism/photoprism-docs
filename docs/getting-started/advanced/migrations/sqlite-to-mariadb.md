# Migrating from SQLite to MariaDB

*Note: This is contributed content intended for advanced users. You can contribute by clicking :material-pencil: to send a pull request with your changes.*

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
    command: mysqld --innodb-buffer-pool-size=1G >
      --transaction-isolation=READ-COMMITTED --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci --max-connections=512
      --innodb-rollback-on-timeout=OFF --innodb-lock-wait-timeout=120
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

## Solving Performance Issues

After migrating from SQLite, it is possible that columns do not have exactly the data type they should have or that indexes are missing. This can lead to poor performance. For example, MariaDB cannot process rows with `text` columns in memory and always uses temporary tables on disk if there are any.

If this is the case, please make sure that your migrated database schema matches that of a fresh, non-migrated installation, e.g. by [re-running the migrations manually](index.md) in a terminal with the `photoprism migrations ls` and `photoprism migrations run [id]` subcommands.