# Migrating between supported databases

With a PhotoPrism build greater than 20250820 comes a new command to copy the index database between supported DBMS systems.  
This set of instructions assumes that the target DBMS has not been used before, and it is being started for the 1st time as part of these instructions.
If that is not the case, then you will have to create the photoprism database and user in the target DBMS before executing the migration commands.

## Instructions

- Open a shell command on your host
- Backup your existing PhotoPrism database.    Consider if you want to include album metadata as well which isn't included in the example
    - ```docker compose exec photoprism photoprism backup -i -f```
- Stop your PhotoPrism stack
    - ```docker compose down```
- Backup your existing compose.yaml file
- Add your target dbms configuration to the compose.yaml file.  Adjust the following as appropriate for your configuration.  Don't forget to adjust the passwords.

=== MariaDB config

    ```yaml
    mariadb:
        ## If MariaDB gets stuck in a restart loop, this points to a memory or filesystem issue:
        ## https://docs.photoprism.app/getting-started/troubleshooting/#fatal-server-errors
        restart: unless-stopped
        image: mariadb:11
        container_name: mariadb
        ## "security_opt" specifies options for kernel security modules, it can be omitted if it is not needed or supported:
        security_opt:
        - seccomp:unconfined
        - apparmor:unconfined
        ## "user" starts the service with a specific non-root user and group ID (optional):
        # user: 1000:1000
        ## MariaDB config flags, see https://mariadb.com/kb/en/server-system-variables/
        command: --innodb-buffer-pool-size=2G --transaction-isolation=READ-COMMITTED --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --max-connections=512 --innodb-rollback-on-timeout=OFF --innodb-lock-wait-timeout=120
        volumes:
        - "./database:/var/lib/mysql"
        environment:
        MARIADB_AUTO_UPGRADE: "1"
        MARIADB_INITDB_SKIP_TZINFO: "1"
        MARIADB_DATABASE: "photoprism"
        MARIADB_USER: "photoprism"
        MARIADB_PASSWORD: "insecure"
        MARIADB_ROOT_PASSWORD: "insecure"
    ```

=== PostgreSQL config

    ```yaml
    postgres:
        image: postgres:17-alpine
        expose:
        - "5432"
        ports:
        - "5432:5432" # database port (host:container)
        volumes:
        - "postgresql:/var/lib/postgresql/data"
        environment:
        POSTGRES_DB: photoprism
        POSTGRES_USER: photoprism
        POSTGRES_PASSWORD: insecure
    ```

- Add an entrypoint to your compose.yaml so that PhotoPrism does not start when the containers are started
    - locate the ```container_name: photoprism``` line and add the comment, entrypoint and command shown below, with the same indent as the container_name:
```yaml
    container_name: photoprism
    # the following overides the default commands and prevents PhotoPrism from starting as a service
    entrypoint: ["/scripts/cmd.sh"]
    command: ["/scripts/cmd.sh", "tail", "-f", "/dev/null"]
```
- Start your PhotoPrism stack
    - ```docker compose up```
- Execute the command to transfer (copy) your database between DBMS'
    - This assumes that your target database name is photoprism in MariaDB or PostgreSQL

=== Transfer to MariaDB

    ```bash
    docker compose exec photoprism photoprism --tfr-db mysql --tfr-db-name photoprism --tfr-db-server "mariadb:4001" --tfr-db-pass insecure migrations transfer
    ```

=== Transfer to PostgreSQL

    ```bash
    docker compose exec photoprism photoprism --tfr-db postgres --tfr-db-name photoprism --tfr-db-server "postgresql:5432" --tfr-db-pass insecure migrations transfer
    ```

=== Transfer to SQLite

    ```bash
    docker compose exec photoprism photoprism --tfr-db sqlite --transfer-dsn "./storage/index.db" migrations transfer
    ```

You should see output similar to the following after the command execution:

```
time="2025-08-22T10:21:41Z" level=info msg="migrate: transfer batch size set to 100"
time="2025-08-22T10:21:41Z" level=info msg="migrate: ensure target is empty..."
time="2025-08-22T10:21:41Z" level=info msg="migrate: migrating database schema..."
time="2025-08-22T10:21:42Z" level=info msg="migrate: migrating against target"
time="2025-08-22T10:21:42Z" level=info msg="migrate: 20250117-000001 bypassed [61.199962ms] due new database"
time="2025-08-22T10:21:42Z" level=info msg="migrate: 20241202-000001 bypassed [94.484441ms] due new database"
time="2025-08-22T10:21:42Z" level=info msg="migrate: 20250416-000001 bypassed [101.589216ms] due new database"
time="2025-08-22T10:21:42Z" level=info msg="migrate: 20250819-000001 successful [98.948776ms]"
time="2025-08-22T10:21:42Z" level=info msg="migrate: migrating against source"
time="2025-08-22T10:22:39Z" level=info msg="migrate: number of users transfered 2"
time="2025-08-22T10:22:40Z" level=info msg="migrate: number of albums transfered 643"
time="2025-08-22T10:22:40Z" level=info msg="migrate: number of cameras transfered 35"
time="2025-08-22T10:22:40Z" level=info msg="migrate: number of lenses transfered 40"
time="2025-08-22T10:22:41Z" level=info msg="migrate: number of places transfered 768"
time="2025-08-22T10:22:47Z" level=info msg="migrate: number of cells transfered 7622"
time="2025-08-22T10:22:47Z" level=info msg="migrate: number of countries transfered 23"
time="2025-08-22T10:22:51Z" level=info msg="migrate: number of keywords transfered 4695"
time="2025-08-22T10:22:51Z" level=info msg="migrate: number of labels transfered 198"
time="2025-08-22T10:24:28Z" level=info msg="migrate: number of photos transfered 23173"
time="2025-08-22T10:24:49Z" level=info msg="migrate: number of files transfered 24934"
time="2025-08-22T10:24:49Z" level=info msg="migrate: number of albumusers transfered 0"
time="2025-08-22T10:24:49Z" level=info msg="migrate: number of clients transfered 0"
time="2025-08-22T10:24:49Z" level=info msg="migrate: number of sessions transfered 4"
time="2025-08-22T10:24:49Z" level=info msg="migrate: number of userdetails transfered 5"
time="2025-08-22T10:24:49Z" level=info msg="migrate: number of usersettings transfered 5"
time="2025-08-22T10:24:49Z" level=info msg="migrate: number of usershares transfered 0"
time="2025-08-22T10:24:49Z" level=info msg="migrate: number of categories transfered 163"
time="2025-08-22T10:24:49Z" level=info msg="migrate: number of duplicates transfered 0"
time="2025-08-22T10:24:49Z" level=info msg="migrate: number of errors transfered 0"
time="2025-08-22T10:24:50Z" level=info msg="migrate: number of faces transfered 297"
time="2025-08-22T10:24:50Z" level=info msg="migrate: number of services transfered 0"
time="2025-08-22T10:24:50Z" level=info msg="migrate: number of fileshares transfered 0"
time="2025-08-22T10:24:50Z" level=info msg="migrate: number of filesyncs transfered 0"
time="2025-08-22T10:24:50Z" level=info msg="migrate: number of folders transfered 349"
time="2025-08-22T10:24:50Z" level=info msg="migrate: number of links transfered 0"
time="2025-08-22T10:25:00Z" level=info msg="migrate: number of markers transfered 4018"
time="2025-08-22T10:25:00Z" level=info msg="migrate: number of passcodes transfered 1"
time="2025-08-22T10:25:01Z" level=info msg="migrate: number of passwords transfered 3"
time="2025-08-22T10:25:01Z" level=info msg="migrate: number of photousers transfered 0"
time="2025-08-22T10:25:01Z" level=info msg="migrate: number of reactions transfered 0"
time="2025-08-22T10:25:01Z" level=info msg="migrate: number of subjects transfered 46"
time="2025-08-22T10:25:01Z" level=info msg="completed in 3m19.461785631s"
```
- Stop the photoprism container
    - ```docker compose stop photoprism```
- Stop the old DBMS container with one of the following commands (assuming that you had one)
    - ```docker compose stop mariadb```
    - ```docker compose stop postgres```
- Update the compose.yaml DBMS configuration to use your target DBMS

=== MariaDB

    - Update your photoprism settings to match your new DBMS
    ```yaml
          # PHOTOPRISM_DATABASE_DRIVER: "sqlite"         # SQLite is an embedded database that does not require a separate database server
          PHOTOPRISM_DATABASE_DRIVER: "mysql"            # MariaDB 10.5.12+ (MySQL successor) offers significantly better performance compared to SQLite
          PHOTOPRISM_DATABASE_SERVER: "mariadb:3306"     # MariaDB database server (hostname:port)
          PHOTOPRISM_DATABASE_NAME: "photoprism"         # MariaDB database, see MARIADB_DATABASE in the mariadb service
          PHOTOPRISM_DATABASE_USER: "photoprism"         # MariaDB database username, must be the same as MARIADB_USER
          PHOTOPRISM_DATABASE_PASSWORD: "insecure"       # MariaDB database password, must be the same as MARIADB_PASSWORD
    ```
    - Remove the PostgreSQL DBMS service, if you came from PostgreSQL, and change the photoprism service dependancies
    ```yaml
            depends_on:
          - mariadb
    ```

=== PostgreSQL

    - Update your photoprism settings to match your new DBMS
    ```yaml
          # PHOTOPRISM_DATABASE_DRIVER: "sqlite"         # SQLite is an embedded database that does not require a separate database server
          PHOTOPRISM_DATABASE_DRIVER: "postgres"         # PostgreSQL 17
          PHOTOPRISM_DATABASE_SERVER: "postgres:5432"    # PostgreSQL database server (hostname:port)
          PHOTOPRISM_DATABASE_NAME: "photoprism"         # PostgreSQL database, see POSTGRES_DB in the postgres service
          PHOTOPRISM_DATABASE_USER: "photoprism"         # PostgreSQL database username, must be the same as POSTGRES_USER
          PHOTOPRISM_DATABASE_PASSWORD: "insecure"       # PostgreSQL database password, must be the same as POSTGRES_PASSWORD
    ```
    - Remove the MariaDB DBMS service, if you came from MariaDB, and change the photoprism service dependancies
    ```yaml
            depends_on:
          - postgres
    ```

=== SQLite

    - Update your photoprism settings to match your new DBMS
    ```yaml
          PHOTOPRISM_DATABASE_DRIVER: "sqlite"             # SQLite is an embedded database that does not require a separate database server
          # PHOTOPRISM_DATABASE_DRIVER: "mysql"            # MariaDB 10.5.12+ (MySQL successor) offers significantly better performance compared to SQLite
          # PHOTOPRISM_DATABASE_SERVER: "mariadb:3306"     # MariaDB database server (hostname:port)
          # PHOTOPRISM_DATABASE_NAME: "photoprism"         # MariaDB database, see MARIADB_DATABASE in the mariadb service
          # PHOTOPRISM_DATABASE_USER: "photoprism"         # MariaDB database username, must be the same as MARIADB_USER
          # PHOTOPRISM_DATABASE_PASSWORD: "insecure"       # MariaDB database password, must be the same as MARIADB_PASSWORD
    ```
    - Remove the MariaDB or PostgreSQL DBMS service, if you came from MariaDB or PostgreSQL, and change the photoprism service dependancies
    ```yaml
          #  depends_on:
          #- postgres
    ```

- Remove the command to stop PhotoPrism from starting by commenting out the entrypoint and command as shown
```yaml
    container_name: photoprism
    # the following overides the default commands and prevents PhotoPrism from starting as a service
    # entrypoint: ["/scripts/cmd.sh"]
    # command: ["/scripts/cmd.sh", "tail", "-f", "/dev/null"]
```
- Save the compose.yaml file
- Start the PhotoPrism container
    - ```docker compose photoprism start```


PhotoPrism should start, using the new DBMS, with all of your data.
