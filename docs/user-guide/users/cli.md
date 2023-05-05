# User Management Command-Line Interface

As an alternative to the web user interface, you can also manage user accounts by running the following commands in a terminal:

| CLI Command                                 | Description                                  |
|---------------------------------------------|----------------------------------------------|
| `photoprism users ls [search]`              | Searches existing user accounts              |
| `photoprism users legacy [search]`          | Searches legacy user accounts                |
| `photoprism users add [options] [username]` | Adds a new user account                      |
| `photoprism users show [username]`          | Displays user account information            |
| `photoprism users mod [options] [username]` | Modifies an existing user account            |
| `photoprism users rm [username]`            | Removes a user account                       |
| `photoprism users reset`                    | Removes all accounts and resets the database |

#### Adding and Changing Accounts

You can combine the `add` and `mod` subcommands with these flags to set or change account properties:

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

!!! tldr ""
    User account roles and the admin web UI are features that are currently only available in [PhotoPrism+](https://www.photoprism.app/editions#compare).

!!! info ""
    Note that our guides now use the new `docker compose` command by default. If your server does not yet support it, the old `docker-compose` command will still work.

#### Viewing Account Details

To see all account properties of a particular user, use the `show` subcommand:

```
docker compose exec photoprism photoprism users show bob
```

#### Searching User Accounts

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
