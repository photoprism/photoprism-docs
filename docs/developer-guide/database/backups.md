# Database Backups & Restores

This page explains how the [`photoprism backup`](../../user-guide/backups/index.md#backup-command) and [`photoprism restore`](../../user-guide/backups/restore.md#restore-command) commands create and read MariaDB dumps, and why they work this way. The same applies to the scheduled backups. SQLite dumps are created and restored with the `sqlite3` client and are not affected by what follows.

The code lives in [`internal/photoprism/backup`](https://github.com/photoprism/photoprism/tree/develop/internal/photoprism/backup).

## Creating a Dump

PhotoPrism runs `mariadb-dump` with these flags, in addition to the connection settings:

| Flag                   | Effect                                                                                               |
|------------------------|------------------------------------------------------------------------------------------------------|
| `--single-transaction` | Reads all InnoDB tables from one consistent snapshot, without locking them.                          |
| `--skip-add-locks`     | The dump does not lock each table while it is restored.                                              |
| `--skip-no-autocommit` | Each `INSERT` statement is committed on its own when the dump is restored.                           |

As a result:

- **Backups don't block your instance.** Tables are not locked while a dump is created, so the application can keep writing, and the dump still reflects a single point in time.
- **No `LOCK TABLES` privilege is required.** A database user without it can create and restore backups.
- **Tables should use InnoDB.** The snapshot only covers InnoDB tables. If others exist, such as Aria or MyISAM tables, the backup logs a warning that names them. They are still included in the dump, but not as part of the snapshot.
- **Schema changes interrupt a backup.** If another process recreates or rebuilds a table while a dump is being created, for example with `photoprism users reset` or while a second instance migrates the same database, the dump fails with error 1412 and no file is written. Run the backup again once the other command has finished.

## Restoring a Dump

The dump is streamed to the `mariadb` client, which continues after a failed statement and reports it. When statements fail, the restore command logs a warning with their number and line numbers, for example:

```
restore: index database restored, but 1 statement failed, so some rows may be missing (error 1062 at line 9)
```

A failed statement only costs its own rows. To ensure this, PhotoPrism turns unique checks back on while restoring by rewriting one line in the dump header:

```sql
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
```

With both unique and foreign key checks turned off, MariaDB 10.6 and later load an empty table in a mode that can only be rolled back as a whole. In dumps that insert all rows of a table in one transaction, which `mariadb-dump` 11.8 and later do by default, one failed statement would otherwise remove all rows of that table, including those that were restored successfully. The rest of the dump is passed through unchanged. This also applies to backups created with earlier versions.

Dumps created with earlier versions lock each table while it is restored. If the database user does not have the `LOCK TABLES` privilege, each of these statements fails and is included in the warning, even though all rows are restored.

## Why Restores Don't Lock Tables

We decided not to lock tables while restoring, since doing so is not needed to restore the data correctly:

- Each table in a dump is created with its next ID already set, so rows the application adds during a restore receive new IDs and don't conflict with the restored rows. In our tests, a restore of 400,000 rows kept every row while the application was adding rows at the same time, with and without table locks.
- Locking a table blocks all access to it until its data has been loaded, which can take minutes for large tables.
- Users without the `LOCK TABLES` privilege would not be protected by locks anyway, and would get an additional warning for each table.

Locks would only make a difference if the application created a row with the same unique name as a row in the dump while it is being restored, for example a new label during indexing. A restore while indexing or importing gives inconsistent results either way, since the application writes to a partly restored database. For this reason, you should always restore a backup when your instance is not indexing or importing files, and then restart it.
