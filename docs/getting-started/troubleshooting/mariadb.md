# Troubleshooting MariaDB Problems

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://photoprism.app/membership) receive direct [technical support](https://photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to [determine the cause of your problem](index.md).

#### Cannot Connect ####

First, verify that you are using the correct port (default is `3306`) and hostname or IP address:

- in the Docker environment, the default hostname is `mariadb` (same as the service name) 
- use `localhost` on your host if the port has been exposed as described below
- use your private host IP from inside your home network (see network settings)

To connect to MariaDB from your host or home network, you need to expose port `3306` in your `docker-compose.yml`
and [restart the service for changes to take effect](../docker-compose.md#step-2-start-the-server):

```yaml
services:
  mariadb:
    ports:
      - "3306:3306"
```

!!! danger ""
    Set strong passwords if the database is exposed to an external network. Never expose your database to the public
    Internet in this way, for example, if it is running on a cloud server.

If this doesn't help, check the [Docker Logs](docker.md#viewing-logs) for messages like *disk full*, *disk quota exceeded*,
*no space left on device*, *read-only file system*, *error creating path*, *wrong permissions*, *no route to host*, *connection failed*, *exec format error*,
*no matching manifest*, and *killed*:

- [ ] Make sure that the database *storage* folder is readable and writable: Errors such as "read-only file system", "error creating path", or "wrong permissions" indicate a [filesystem permission problem](docker.md#file-permissions)
- [ ] If [symbolic links](https://en.wikipedia.org/wiki/Symbolic_link) are mounted or used within the *storage* folder, replace them with the actual paths and verify that they are accessible
- [ ] If the MariaDB service has been "killed" or otherwise automatically terminated, this can point to a [memory problem](docker.md#adding-swap) (add swap and/or memory; remove or increase usage limits)
- [ ] In case the logs also show "disk full", "quota exceeded", or "no space left" errors, either [the disk containing the *storage* folder is full](docker.md#disk-space) (add storage) or a disk usage limit is configured (remove or increase it)
- [ ] Log messages that contain "no route to host" may also indicate a general network configuration problem (follow our [examples](https://dl.photoprism.app/docker/))
- [ ] You have to resort to [alternative Docker images](../raspberry-pi.md#older-armv7-based-devices) to run MariaDB on ARMv7-based devices and those with a 32-bit operating system

#### Bad Performance ####

↪ [Performance Tips](performance.md#mariadb)

#### Version Upgrade ####

If MariaDB fails to start after upgrading from an earlier version (or migrating from MySQL), the [internal management schema](https://mariadb.com/kb/en/understanding-mariadb-architecture/#system-databases) may be outdated. With older versions, it could only be updated manually.
However, newer MariaDB Docker images **support automatic upgrades** on startup, so you don't have to worry about that anymore.

##### Manual Update #####

To manually upgrade the internal database schema, run this command in a terminal:

```bash
docker-compose exec mariadb mariadb-upgrade -uroot -p
```

Enter the MariaDB "root" password specified in your `docker-compose.yml` when prompted.

Alternatively, you can downgrade to the previous version, create a database backup using the `photoprism backup`
command, start a new database instance based on the latest version, and then restore your index with
the `photoprism restore` command.

##### Auto Upgrade #####

To enable automatic schema updates, set `MARIADB_AUTO_UPGRADE` to a non-empty value in your `docker-compose.yml` as shown in our [config example](https://dl.photoprism.app/docker/docker-compose.yml):

```yaml
services:
  ...

  mariadb:
    image: mariadb:10.7
    ...
    environment:
      MARIADB_AUTO_UPGRADE: "1"
      MARIADB_INITDB_SKIP_TZINFO: "1"
      ...
```

Before starting MariaDB in production mode, the database image entrypoint script now runs `mariadb-upgrade` to update the internal management schema as needed. For example, when you pull a new major release and restart the service.

!!! tldr ""
    Since PhotoPrism does not require time zone support, you can also add `MARIADB_INITDB_SKIP_TZINFO` to your config as shown above. However, this is only a recommendation and optional.

#### Incompatible Schema ####

If your database does not seem to be compatible with the currently installed version of PhotoPrism, for example because search results are missing or incorrect, first make sure you are using a [supported database](../index.md#databases) and that its internal management schema is up-to-date. How to do that is explained in the [previous section](#version-upgrade).

Once you have verified that neither is a problem, you can run the following command [in a terminal](../docker-compose.md#command-line-interface) to check the status of previous database schema migrations:

```bash
docker-compose exec photoprism photoprism migrations ls
```

!!! note ""
    Omit the `docker-compose exec photoprism` prefix if you are using an interactive terminal session or are running PhotoPrism directly on your computer without Docker.

##### Re-Run Migrations #####

Should the status of any migration not be OK, you can re-run failed migrations using this command in a terminal:

```bash
docker-compose exec photoprism photoprism migrations run -f
```

The `-f` flag instructs the `photoprism migrations run` subcommand to re-run previously failed migrations. Use `--help` to see the command help.

##### Complete Rescan #####

We recommend that you always **perform a rescan after a schema migration**, especially if problems persist. You can either start a [rescan from the user interface](../../user-guide/library/originals.md) by navigating to *Library* > *Index*, checking "Complete Rescan", and then clicking "Start", or by running this command in a terminal:

```bash
docker-compose exec photoprism photoprism index -f
```

!!! tldr ""
    Be careful not to start multiple indexing processes at the same time, as this will lead to a high server load.

#### Lost Root Password ####

In case you forgot the MariaDB "root" password and the one specified in your configuration does not work,
you can [start the server with the `--skip-grant-tables` flag](https://mariadb.com/docs/reference/mdb/cli/mariadbd/skip-grant-tables/)
added to the `mysqld` command in your `docker-compose.yml`. This will temporarily give full access
to all users after a restart:

```yaml
services:
  mariadb:
    command: mysqld --skip-grant-tables
```

Restart the `mariadb` service for changes to take effect:

```bash
docker-compose stop mariadb
docker-compose up -d mariadb
```

Now open a database console:

```bash
docker-compose exec mariadb mysql -uroot
```

Enter the following commands to change the password for "root":

```sql
FLUSH PRIVILEGES;
ALTER USER 'root'@'%' IDENTIFIED BY 'new_password';
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
UPDATE mysql.user SET authentication_string = '' WHERE user = 'root';
UPDATE mysql.user SET plugin = '' WHERE user = 'root';
exit
```

When you are done, remove the `--skip-grant-tables` flag again to restore the original
command and restart the `mariadb` service as described above.

#### Corrupted Files ####

If your database files get corrupted frequently, it is usually because they are stored on an unreliable device such
as a USB flash drive, an SD card, or a shared network folder.

- [ ] Never use the same database files with more than one server instance
- [ ] To share a database over a network, run the database server directly on the remote server instead of sharing database files
- [ ] To repair your tables after you have moved the files to a local disk, you can [start MariaDB with `--innodb-force-recovery=1`](https://mariadb.com/kb/en/innodb-recovery-modes/) (otherwise the same procedure as for recovering a lost password, see above)

#### Server Relocation ####

When moving MariaDB to another computer, cloud server, or virtual machine:

- [ ] Move the complete *storage* folder along with it and preserve the [file permissions](docker.md#file-permissions)
- [ ] **or** restore your index [from an SQL dump](https://mariadb.com/kb/en/mysqldump/) (backup file)
- [ ] Perform a [version upgrade](#version-upgrade) if necessary
- [ ] Make sure that PhotoPrism can access the database on the new host
- [ ] Set strong passwords if the database is exposed to an external network
- [ ] Never expose your database to the public Internet

#### Unicode Support ####

If the logs show "incorrect string value" database errors and you are running a custom MariaDB or MySQL
server that is not based on our [default configuration](https://dl.photoprism.app/docker/docker-compose.yml):

- [ ] Full [Unicode](https://home.unicode.org/basic-info/faq/) support [must be enabled](https://mariadb.com/kb/en/setting-character-sets-and-collations/#example-changing-the-default-character-set-to-utf-8), e.g. using the `mysqld` command parameters `--character-set-server=utf8mb4` and `--collation-server=utf8mb4_unicode_ci`
- [ ] Note that an existing database may use a different character set if you imported it from another server
- [ ] Before submitting a support request, verify the problem still occurs with a newly created database based on our example

Run this command in a terminal to see the current values of the collation and character set variables (change the root
password `insecure` and database name `photoprism` as specified in your `docker-compose.yml`):

```bash
echo "SHOW VARIABLES WHERE Variable_name LIKE 'character\_set\_%' OR Variable_name LIKE 'collation%';" | \
docker-compose exec -T mariadb mysql -uroot -pinsecure photoprism
```

#### MySQL Errors ####

Official [support for MySQL 8 is discontinued](../index.md#databases) as Oracle seems to have stopped shipping [new features and improvements](https://github.com/photoprism/photoprism/issues/1764).
As a result, the testing effort required before each release is no longer feasible.

*[SQLite]: self-contained, serverless SQL database