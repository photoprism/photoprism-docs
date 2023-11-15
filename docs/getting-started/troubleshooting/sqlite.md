# Troubleshooting SQLite Problems

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://www.photoprism.app/membership) receive direct [technical support](https://www.photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to [determine the cause of your problem](index.md).

## Bad Performance

If you have only a few images, concurrent users, and CPU cores, [SQLite](https://www.sqlite.org/) may seem faster compared to full-fledged database servers like [MariaDB](https://mariadb.com/).

This changes as the index grows and the number of concurrent requests increases. The way MariaDB handles multiple queries is completely different and optimized for high concurrency, while SQLite, for example, locks the index on updates so that other operations have to wait. In the worst case, this can lead to locking errors and timeouts during indexing - especially when combined with a slow disk or network storage.

The biggest advantage of SQLite is that you don't need to run a separate database server. This can be very useful for testing and works well if you only have a few thousand files to index. If you are looking for scalability and high performance, it is not a good choice.

[Get MariaDB Performance Tips ›](performance.md#mariadb){ class="pr-3 block-xs" }

## Locking Errors

If you use [traditional hard drives instead of SSDs](performance.md#storage), you will find that PhotoPrism frequently runs into locking issues with SQLite because your CPU is many times faster than the mechanical heads of your disks. To some extent, this may also happen with solid-state drives, but it is much more likely with slow storage.

You may be able to optimize the behavior and reduce locking errors [with SQLite parameters](https://github.com/photoprism/photoprism/issues/2707) that you can set with the [database DSN config option](../config-options.md#database-connection). In particular, enabling [Write-Ahead Logging](https://www.sqlite.org/wal.html) has been shown to resolve locking issues and improve performance:

    sqlite3 index.db
    sqlite> PRAGMA journal_mode=WAL;

Ultimately you should use an SSD if you want to keep SQLite or switch to MariaDB. Please note that our team cannot provide support otherwise.

## Server Crashes

If the server crashes unexpectedly or your database files get corrupted frequently, it is usually because they are stored on an unreliable device such as a USB flash drive, an SD card, or a shared network folder mounted via NFS or CIFS. These may also have [unexpected file size limitations](https://thegeekpage.com/fix-the-file-size-exceeds-the-limit-allowed-and-cannot-be-saved/), which is especially problematic for databases that do not split data into smaller files.

- [ ] Never use the same database files with more than one server instance
- [ ] Use SSDs instead of traditional hard drives, never use network storage
- [ ] Consider using MariaDB instead of SQLite

## Corrupted Files

↪ [Server Crashes](#server-crashes)

## Migrating to MariaDB

When [migrating from SQLite to MariaDB](../advanced/migrations/sqlite-to-mariadb.md), e.g. using scripts and instructions from the community, you should note that your database schema may no longer be optimized for performance and indexes may be missing. Also, MariaDB cannot handle rows with "text" columns in memory and always uses temporary tables on disk if there are any.

If this is the case, please make sure that your migrated database schema matches that of a [fresh, non-migrated installation](../../developer-guide/database/index.md) . It may help to [run the migrations manually](../advanced/migrations/index.md) in a terminal using the *migrations* subcommands. However, this does not guarantee that all issues such as missing indexes are resolved.

[Troubleshoot MariaDB Problems ›](mariadb.md){ class="pr-3 block-xs" }
