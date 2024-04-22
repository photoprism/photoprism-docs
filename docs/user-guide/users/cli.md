# User Management Commands

## Changing a Password

Running the following in a terminal changes the password of an existing user without affecting other account settings, e.g. if you cannot remember the currently set password or if there was a problem [configuring the initial admin account](../../getting-started/config-options.md#authentication) (replace `[username]` with the username of the account you want to update):

```bash
photoprism passwd [username]
```

Note that when you use [Docker Compose](../../getting-started/docker-compose.md#command-line-interface) and do not [already have a terminal session open](../../getting-started/docker-compose.md#opening-a-terminal), you must prepend `docker compose exec photoprism` so that the command is executed within the `photoprism` container, for example:

```bash
docker compose exec photoprism photoprism passwd admin
```

This also [applies to other terminal commands](../../getting-started/docker-compose.md#examples), including those listed below.

!!! tldr ""
    The examples in our documentation use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible Linux distributions.

## Managing User Accounts

As an alternative to the [web user interface](index.md), you can [run the following commands in a terminal](../../getting-started/docker-compose.md#command-line-interface) to perform tasks such as adding, viewing, editing and deleting user accounts:

| CLI Command                                 | Description                                  |
|---------------------------------------------|----------------------------------------------|
| `photoprism users ls [search]`              | Searches existing user accounts              |
| `photoprism users legacy [search]`          | Searches legacy user accounts                |
| `photoprism users add [options] [username]` | Adds a new user account                      |
| `photoprism users show [username]`          | Displays user account information            |
| `photoprism users mod [options] [username]` | Modifies an existing user account            |
| `photoprism users rm [username]`            | Removes a user account                       |
| `photoprism users reset --yes`              | Removes all accounts and resets the database |

### Command Options

The `add` and `mod` commands support these flags to set or change account properties:

| Command Flag                         | Description                                                      |
|--------------------------------------|------------------------------------------------------------------|
| `--name NAME`, `-n NAME`             | full NAME for display in the interface                           |
| `--email EMAIL`, `-m EMAIL`          | unique EMAIL address of the user                                 |
| `--password PASSWORD`, `-p PASSWORD` | PASSWORD for local authentication                                |
| `--role value`, `-r value`           | user role NAME (admin, user, viewer or guest) (default: "admin") |
| `--superadmin`, `-s`                 | make user super admin with full access                           |
| `--no-login`, `-l`                   | disable login on the web interface                               |
| `--webdav`, `-w`                     | allow to sync files via WebDAV                                   |
| `--upload-path value`, `-u value`    | upload files to this sub-folder                                  |
| `--disable-2fa`                      | deactivate two-factor authentication                             |

### Creating a New Account

The command `photoprism users add` creates a new user account. For example, you could run the following to add a new admin with the username "bob" and the password "mysecret":

```bash
docker compose exec photoprism photoprism users add -p mysecret -n "Bob" bob
```

If you do not specify an initial password with the `-p` flag, you will be prompted to enter a password for the new account. Further account properties can be set with the flags listed above.

!!! example ""
    Please note that [additional account roles](roles.md) such as *user*, *viewer*, and *guest* are [currently only available with a membership](https://www.photoprism.app/editions#compare) to support development and maintenance.

### Viewing Account Details

To view the account properties of a specific user, use the `show` subcommand:

```bash
docker compose exec photoprism photoprism users show bob
```

### Searching User Accounts

To list all existing accounts, you can run the following:

```bash
docker compose exec photoprism photoprism users ls
```

With the `photoprism users ls` command, you can also find specific accounts based on a search term you provide:

```bash
docker compose exec photoprism photoprism users ls bob
```

To display a description and the available options for a command, use the `--help` flag:

```bash
docker compose exec photoprism photoprism users ls --help
```

## Viewing Login Attempts

For security reasons, authentication logs are not visible on the regular web user interface and can only be viewed in the application service logs or searched in a terminal using the the following CLI command:

```bash
docker compose exec photoprism photoprism logins ls [search]
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

## Session Management

You can use the following terminal commands to create, inspect and, if necessary, delete access tokens for the authentication of browsers and other clients (including [app passwords](2fa.md#step-3-app-passwords)):

| CLI Command                         | Description                                              |
|-------------------------------------|----------------------------------------------------------|
| `photoprism auth ls [search]`       | Lists currently authenticated users and clients          |
| `photoprism auth add [username]`    | Adds a new authentication secret for client applications |
| `photoprism auth show [identifier]` | Shows detailed information about a session               |
| `photoprism auth rm [identifier]`   | Deletes a session by id or access token                  |
| `photoprism auth reset --yes`       | Resets the authentication of all users and clients       |

!!! tldr ""
    Should you experience problems, for example after upgrading from a [previous release](../../release-notes.md) or [development preview](../../getting-started/updates.md#development-preview), we recommend running the `photoprism auth reset --yes` command [in a terminal](../../getting-started/docker-compose.md#command-line-interface) to reset the `auth_sessions` table to a clean state and force a re-login of all users. Please note that this will also delete all client access tokens and any [app passwords](2fa.md#step-3-app-passwords) that users may have created.