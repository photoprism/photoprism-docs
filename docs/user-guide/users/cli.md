# User Management Commands

## Managing User Accounts

As an alternative to the [web user interface](index.md), you can also add, view, modify, and delete user accounts by running the following commands [in a terminal](../../getting-started/docker-compose.md#command-line-interface):

| CLI Command                                 | Description                                  |
|---------------------------------------------|----------------------------------------------|
| `photoprism users ls [search]`              | Searches existing user accounts              |
| `photoprism users legacy [search]`          | Searches legacy user accounts                |
| `photoprism users add [options] [username]` | Adds a new user account                      |
| `photoprism users show [username]`          | Displays user account information            |
| `photoprism users mod [options] [username]` | Modifies an existing user account            |
| `photoprism users rm [username]`            | Removes a user account                       |
| `photoprism users reset`                    | Removes all accounts and resets the database |

### Command Options

The `add` and `mod` commands support these flags to set or change account properties:

| Command Flag                         | Description                                     |
|--------------------------------------|-------------------------------------------------|
| `--name NAME`, `-n NAME`             | full NAME for display in the interface          |
| `--email EMAIL`, `-m EMAIL`          | unique EMAIL address of the user                |
| `--password PASSWORD`, `-p PASSWORD` | PASSWORD for authentication                     |
| `--role value`, `-r value`           | admin, user, viewer or guest (default: "admin") |
| `--superadmin`, `-s`                 | make user super admin with full access          |
| `--no-login`, `-l`                   | disable login on the web interface              |
| `--webdav`, `-w`                     | allow to sync files via WebDAV                  |
| `--upload-path value`, `-u value`    | upload files to this sub-folder                 |

For example, you could do the following to add a new admin with the username "bob" and the password "mysecret":

```
docker compose exec photoprism photoprism users add -p mysecret -n "Bob" bob
```

!!! example ""
    Additional [account roles](roles.md) like user, viewer, and guest are currently [only available with a membership](https://www.photoprism.app/editions#compare) to support development and maintenance.

!!! tldr ""
    Note that our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible Linux distributions.

### Viewing Account Details

To see all account properties of a particular user, use the `show` subcommand:

```
docker compose exec photoprism photoprism users show bob
```

### Searching User Accounts

To list all existing accounts, you can run the following:

```
docker compose exec photoprism photoprism users ls
```

This command can also filter the result if you provide a search term as argument:

```
docker compose exec photoprism photoprism users ls bob
```

To display a description and the available options for a command, use the `--help` flag:

```
docker compose exec photoprism photoprism users ls --help
```

## Viewing Login Attempts

For security reasons, authentication logs are not visible on the regular web user interface and can only be viewed in the application service logs or searched in a terminal using the the following CLI command:

```
photoprism logins ls [search]
```

### Command Options

You can combine it with these flags to change the output format and the maximum number of search results:

| Command Flag | Description                            |
|--------------|----------------------------------------|
| `--md, -m `  | format as machine-readable Markdown    |
| `--csv, -c`  | export as semicolon separated values   |
| `--tsv, -t`  | export as tab separated values         |
| `-n LIMIT`   | LIMIT number of results (default: 100) |

### Example Report

| Client IP  | User Name | Realm | Status |     Last Login      | Failed At |
|------------|-----------|-------|--------|---------------------|-----------|
| 172.19.0.1 | user      | api   | OK     | 2023-02-03 07:17:46 |           |
| 172.19.0.1 | viewer    | api   | OK     | 2023-02-03 07:16:55 |           |
| 172.19.0.1 | admin     | api   | OK     | 2023-02-03 06:55:06 |           |

!!! tldr ""
    Run `photoprism logins clear` to clear all recorded incidents and reset the database to a clean state.

## Session Monitoring

You can use the following terminal commands to find, examine and, if necessary, delete browser sessions:

| CLI Command                   | Description                        |
|-------------------------------|------------------------------------|
| `photoprism sess ls [search]` | Finds and displays sessions        |
| `photoprism sess show [id]`   | Shows detailed session information |
| `photoprism sess rm [id]`     | Deletes the specified session      |
| `photoprism sess clear`       | Removes all sessions               |
