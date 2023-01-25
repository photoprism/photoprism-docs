# Migrating from MariaDB to SQLite

*For advanced users only: The instructions for these migrations were provided by a contributor and are not part of the original software distribution. As such, they have not been officially released, recommended, or extensively tested by us. You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.*

- Install <https://github.com/techouse/mysql-to-sqlite3> on your host.
- Stop Photoprism: `docker compose stop photoprism`
- Add the port to the MariaDB service
- On the **host** now run `sudo mysql2sqlite -f <PATH_TO_STORAGE_MOUNT>/storage/index.db -d photoprism -u root --mysql-password 'insecure'`
- Shutdown your current stack fully: `docker compose down`
- Edit your `docker-compose.yml`:
  - Remove the MariaDB service.
  - Change in the Photoprism settings to use the sqlite driver and remove the other database settings
- Start your stack again with `docker compose up -d`
- If this worked you may want to delete the old mountpoint for the MariaDB database.

!!! warning "Bad Performance"
    Many users reporting poor performance and high CPU usage have migrated, so their database schema is no longer optimized for performance, for example, because indexes are missing or columns have the wrong data type.

    If this is the case, please make sure that your migrated database schema matches that of a fresh, non-migrated installation. It may help to [run the migrations manually](../../advanced/migrations/index.md) in a terminal using the *migrations* subcommands. However, this does not guarantee that all issues such as missing indexes are resolved.
