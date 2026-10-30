# Migrating from SQLite to MariaDB

The `photoprism database transfer` command copies your existing SQLite index to a MariaDB database, including users, sessions, albums, and settings. PhotoPrism creates the tables in the new database itself, so they are the same as in a new installation. An [index backup](../../../user-guide/backups/index.md#backup-command) can only be restored into the same kind of database, so it is not an alternative for this.

!!! info ""
    The examples on this page assume that you are using [Docker Compose](../../docker-compose.md) and run the commands in the folder where your `compose.yaml` file is located.

## Moving Your Index

1. Create an [index backup](../../../user-guide/backups/index.md#backup-command) with `docker compose exec photoprism photoprism backup -i`, so you can return to your current database if needed.
2. Add a `mariadb` service to your `compose.yaml` as shown below, but leave the database settings of the `photoprism` service unchanged for now. Then start the new service with `docker compose up -d mariadb`.
3. Stop PhotoPrism with `docker compose stop photoprism`, since changes made during the transfer would be missing in the new database.
4. Run the transfer in a new container, using the values of your `mariadb` service. The `--entrypoint` option is required, as the command would otherwise not read the database settings of the `photoprism` service and transfer an empty index instead:

    ```bash
    docker compose run --rm --entrypoint /opt/photoprism/bin/photoprism photoprism database transfer --target-driver mariadb --target-server mariadb:3306 --target-name photoprism --target-user photoprism --target-password insecure
    ```

    If PhotoPrism runs as a non-root user that is set with `PHOTOPRISM_UID` and `PHOTOPRISM_GID` instead of the `user` property, also pass these IDs with `--user`, e.g. `--user 1000:1000`, so that files created in your storage folder keep the right owner.

5. Change the database settings of the `photoprism` service to the MariaDB values shown below, and start it again with `docker compose up -d`.

Once you have checked that your pictures, albums, and accounts are complete, you may delete the `index.db` file and other files starting with `index.db` from the `storage` folder, as they are no longer up to date.

The target database must be empty. If PhotoPrism has already been started with it, the command refuses to run unless you pass `--force`, which replaces its data. If the transfer fails, the target is emptied again, so you can fix the cause and run the command once more. If the database server rejects large statements, lower the number of rows copied per statement with `--batch`, e.g. `--batch 100`.

## Example Configuration

The `mariadb` service is the same as in our [default `compose.yaml`](../../docker-compose.md):

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_DATABASE_DRIVER: "mysql"
      PHOTOPRISM_DATABASE_SERVER: "mariadb:3306"
      PHOTOPRISM_DATABASE_NAME: "photoprism"
      PHOTOPRISM_DATABASE_USER: "photoprism"
      PHOTOPRISM_DATABASE_PASSWORD: "insecure"
      ...

  mariadb:
    image: mariadb:12.3
    restart: unless-stopped
    stop_grace_period: 15s
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
    command: --innodb-buffer-pool-size=512M --transaction-isolation=READ-COMMITTED --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --max-connections=512 --innodb-rollback-on-timeout=OFF --innodb-lock-wait-timeout=120
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

Please change the passwords before you start the `mariadb` service for the first time, and use the same value for `MARIADB_PASSWORD`, `PHOTOPRISM_DATABASE_PASSWORD`, and `--target-password`. Store the database files on a local SSD, as shown above, rather than on a network share or USB flash drive.

## Databases Migrated With Other Tools

If you have previously moved your index to MariaDB with third-party tools, columns may not have the data type they should have, and indexes may be missing. This can lead to [poor performance](../../troubleshooting/performance.md#migration-from-sqlite), for example because MariaDB cannot process rows with `text` columns in memory. Running the [schema migrations](index.md) again does not fix this.

To get the same tables as a new installation, transfer your index to a new, empty database on the same server:

1. Create an [index backup](../../../user-guide/backups/index.md#backup-command) and stop PhotoPrism as described above.
2. Create the new database and allow the `photoprism` user to access it, using the password set with `MARIADB_ROOT_PASSWORD`:

    ```bash
    docker compose exec mariadb mariadb -uroot -pinsecure -e "CREATE DATABASE photoprism_new; GRANT ALL PRIVILEGES ON photoprism_new.* TO 'photoprism'@'%';"
    ```

3. Run the transfer with `--target-name photoprism_new` instead of `--target-name photoprism`.
4. Set `PHOTOPRISM_DATABASE_NAME` to `photoprism_new` and start PhotoPrism again with `docker compose up -d`.

[Learn more ›](../databases.md)
