# Schema Migrations

PhotoPrism runs database schema migrations automatically during startup. [GORM](https://gorm.io/) first creates missing tables and columns based on the models in [`internal/entity`](https://github.com/photoprism/photoprism/tree/develop/internal/entity), and SQL migrations then make the changes it cannot, such as converting data or changing a column type. The migration definitions live in the main repository under [`internal/entity/migrate`](https://github.com/photoprism/photoprism/tree/develop/internal/entity/migrate) and cover MariaDB and SQLite. On PostgreSQL, which is supported experimentally, the schema is created by GORM alone, so there are no SQL migrations for it yet. The `photoprism migrations …` subcommands exposed by [`internal/commands/migrations.go`](https://github.com/photoprism/photoprism/blob/develop/internal/commands/migrations.go) let you inspect their status, re-run individual steps, or retry failures without restarting the app.

!!! example "Running commands in Docker"
    When using [Docker Compose](../../getting-started/docker-compose.md), prepend commands with `docker compose exec photoprism …` to run them inside the container. If Docker reports *no container found*, ensure the stack is running and execute the command from the directory that contains your `compose.yaml` file.

## Inspect Migration Status

List every migration and its latest state with:

```bash
photoprism migrations ls
```

Sample output:

```
|-----------------|---------|-------|---------------------|---------------------|--------|
|       ID        | Dialect | Stage |     Started At      |     Finished At     | Status |
|-----------------|---------|-------|---------------------|---------------------|--------|
| 20240112-120000 | mysql   | main  | 2025-01-06 06:41:08 | 2025-01-06 06:41:08 | OK     |
| 20240218-083000 | mysql   | pre   | -                   | -                   | -      |
| 20240218-090000 | mysql   | main  | -                   | -                   | -      |
| 20240502-070500 | sqlite3 | main  | 2025-02-14 10:18:42 | 2025-02-14 10:18:42 | OK     |
|-----------------|---------|-------|---------------------|---------------------|--------|
```

- **Stage** indicates whether a migration runs in the `pre` stage before GORM updates the schema, in the regular `main` stage after it, or in the `post` stage after all others. Most migrations belong to `main`.
- The status column shows `OK` for completed migrations, `-` for migrations that have never run, `Repeat` for migrations flagged to rerun, or the error message returned by the last attempt.
- Pass migration IDs to restrict the output: `photoprism migrations ls 20240502-070500 20240502-071000`.
- Use the standard report flags (`--json`, `--md`, `--csv`, `--tsv`) to change the output format. This is helpful for automation or when you need to paste the table into an issue.

## Run Pending or Specific Migrations

`photoprism migrations run` executes all pending migrations for the current database driver. The command accepts optional migration IDs so you can re-run a subset:

```bash
# Run everything that has not been executed yet
photoprism migrations run

# Re-run a selection in order
photoprism migrations run 20240218-083000 20240218-090000
```

Useful flags:

- `--failed` / `-f` replays only the migrations that previously failed. This is equivalent to `conf.MigrateDb(true, nil)` in the backend code.
- `--trace` enables verbose logging during the migration run.

When the command finishes you will see a summary such as:

```
INFO[2025-02-15T12:11:02Z] migrating database schema...
INFO[2025-02-15T12:11:02Z] migrate: 20240218-083000 successful [14.9ms]
INFO[2025-02-15T12:11:02Z] migrate: 20240218-090000 successful [32.4ms]
INFO[2025-02-15T12:11:02Z] completed in 64.8ms
```

## Troubleshooting Tips

1. **Back up first.** Always snapshot your MariaDB or SQLite database before retrying migrations manually.
2. **Match the dialect.** The CLI selects the migrations based on `PHOTOPRISM_DATABASE_DRIVER`: `mysql` or `mariadb` runs the files in `internal/entity/migrate/mysql`, and `sqlite3` runs those in `internal/entity/migrate/sqlite3`.
3. **Inspect logs.** When a migration fails repeatedly, re-run it with `--trace` and check the log output for the SQL statement that caused the error.
4. **Verify permissions.** Schema updates require `ALTER`, `CREATE`, and `DROP` privileges. Limited database users may fail to apply certain migrations.
