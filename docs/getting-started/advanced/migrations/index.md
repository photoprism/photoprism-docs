# Performing Index Migrations

!!! info ""
    When using [Docker Compose](../../docker-compose.md), you can prepend commands like `docker compose exec [service] [command]` to run them in a service container.
    Should this fail with *no container found*, make sure the service has been started, you have specified an existing service (usually `photoprism`) and you are in the folder where the `docker-compose.yml` file is located.

## Show Migration Status

Run the `photoprism migrations ls` command in a terminal to see a list of all migrations and their current status:

```
$ photoprism migrations ls

|-----------------|---------|---------------------|---------------------|--------|
|       ID        | Dialect |     Started At      |     Finished At     | Status |
|-----------------|---------|---------------------|---------------------|--------|
| 20211121-094727 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20211124-120008 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-030000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-040000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-050000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-060000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-061000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-070000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-071000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-080000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-081000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-083000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-090000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-091000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220329-093000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220421-200000 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220521-000001 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220521-000002 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
| 20220521-000003 | mysql   | 2022-07-12 08:07:35 | 2022-07-12 08:07:35 | OK     |
|-----------------|---------|---------------------|---------------------|--------|
```

## Run Specific Migrations

To explicitly re-run specific migrations, you can pass them as arguments to the `photoprism migrations run` command:

```
$ photoprism migrations run 20220521-000003

INFO[2022-07-12T11:45:29Z] migrate: 20220521-000003 successful [12.967654ms] 
INFO[2022-07-12T11:45:29Z] migration completed in 40.89123ms            
INFO[2022-07-12T11:45:29Z] closed database connection 
```

## Retry Failed Migrations

To automatically retry previously failed migrations, pass the `-f` flag to the `photoprism migrations run` command:

```
$ photoprism migrations run -f
```
