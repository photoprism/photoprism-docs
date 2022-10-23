# Troubleshooting SQLite Problems

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://photoprism.app/membership) receive direct [technical support](https://photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to [determine the cause of your problem](index.md).

#### Bad Performance ####

If you have only a few images, concurrent users, and CPU cores, [SQLite](https://www.sqlite.org/) may seem faster compared to full-fledged database servers like [MariaDB](https://mariadb.com/).

This changes as the index grows and the number of concurrent requests increases. The way MariaDB handles multiple queries is completely different and optimized for high concurrency, while SQLite, for example, locks the index on updates so that other operations have to wait. In the worst case, this can lead to locking errors and timeouts during indexing - especially when combined with a slow disk or network storage.

The biggest advantage of SQLite is that you don't need to run a separate database server. This can be very useful for testing and works well if you only have a few thousand files to index. If you are looking for scalability and high performance, it is not a good choice.

[Get MariaDB Performance Tips ›](performance.md#mariadb){ class="pr-3" }

#### Locking Errors ####

If you use [traditional hard drives instead of SSDs](performance.md#storage), you will find that PhotoPrism frequently runs into locking issues with SQLite because your CPU is many times faster than the mechanical heads of your disks. To some extent, this may also happen with solid-state drives, but it is much more likely with slow storage.

You may be able to optimize the behavior and reduce locking [with SQLite parameters](https://github.com/photoprism/photoprism/issues/2707) that you can set with the [database DSN config option](../config-options.md#database-connection), but ultimately you should use an SSD if you want to keep SQLite or switch to MariaDB. Please note that our team cannot provide support otherwise.

#### Migrating to MariaDB ####

When [migrating from SQLite to MariaDB](../advanced/migrations/sqlite-to-mariadb.md), e.g. using scripts and instructions from the community, you should note that your database schema may no longer be optimized for performance and indexes may be missing. Also, MariaDB cannot handle rows with "text" columns in memory and always uses temporary tables on disk if there are any.

If this is the case, please make sure that your migrated database schema matches that of a [fresh, non-migrated installation](../../developer-guide/database/index.md) . It may help to [run the migrations manually](../advanced/migrations/index.md) in a terminal using the *migrations* subcommands. However, this does not guarantee that all issues such as missing indexes are resolved.

[Troubleshoot MariaDB Problems ›](mariadb.md){ class="pr-3" }
