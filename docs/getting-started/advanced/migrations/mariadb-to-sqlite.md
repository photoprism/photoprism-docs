# Migrating from MariaDB to SQLite

*Note: This is contributed content intended for advanced users. You can contribute by clicking :material-pencil: to send a pull request with your changes.*

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

## Solving Performance Issues

After migrating from MariaDB, it is possible that columns do not have exactly the data type they should have or that indexes are missing. This can lead to poor performance.

If this is the case, please make sure that your migrated database schema matches that of a fresh, non-migrated installation, e.g. by [re-running the migrations manually](index.md) in a terminal with the `photoprism migrations ls` and `photoprism migrations run [id]` subcommands.
