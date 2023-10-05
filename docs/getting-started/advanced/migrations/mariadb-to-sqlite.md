# Migrating from MariaDB to SQLite

*While we believe this contributed content may be helpful to advanced users, we have not yet thoroughly reviewed it. If you have suggestions for improvement, please let us know by clicking :material-file-edit-outline: to submit a change request.*

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
