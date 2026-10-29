# Managing User Accounts

!!! example ""
    [PhotoPrism® Plus](https://www.photoprism.app/editions/#compare) includes a web user interface for account and session management, in addition to the [command-line interface](cli.md) available in all editions.
    If you are running [PhotoPrism® Pro](https://www.photoprism.app/teams/#compare), see [Managing User Accounts](https://www.photoprism.app/pro/kb/roles/) in the Pro Knowledge Base.

You can add, edit, and delete user accounts by navigating to *Settings > Users* as an [Admin](roles.md#admin):

![Screenshot](img/users-2502.jpg){ class="shadow" }

## Adding a New User

![Screenshot](img/users-add-2502.jpg){ class="shadow" }

Usernames of new accounts may only contain standard ASCII characters, so accented letters and non-Latin scripts are not accepted. Existing accounts keep their names.

## Editing User Details

![Screenshot](img/users-edit-2502.jpg){ class="shadow" }

The *MCP* switch next to *WebDAV* controls whether an account can use [MCP](../../developer-guide/api/mcp.md#authorization) to let AI assistants search and browse the library. It is on by default for roles that may use MCP, and has no effect if MCP is [disabled for all users](../../getting-started/config-options.md#feature-flags).

Only [super admins](roles.md#admin) can change the [authentication provider](cli.md#command-options) of another account through the web interface. Their own account is excluded so that they do not accidentally lock themselves out, for example by setting the provider to `none`.

## Changing Passwords

Super admins can reset another user's password without knowing the current one. Regular admins can change another user's password only if they know the current password.

![Screenshot](img/users-change-pw-2502.jpg){ class="shadow" }

## Deleting a User

![Screenshot](img/users-delete-2502.jpg){ class="shadow" }

Deleting a user signs the account out on all devices, including its app passwords, and disables it. The account record is kept, and pictures the user has uploaded are not deleted.

## Managing Sessions

You can view and delete active sessions by navigating to *Settings > Users > Sessions* as an [Admin](roles.md#admin):

![Screenshot](img/sessions-2502.jpg){ class="shadow" }

To view session details, click :material-magnify:.
To delete a session, click :material-delete:.

!!! info ""
    When a password or privilege level changes, PhotoPrism invalidates that user's other active sessions to protect the account.
