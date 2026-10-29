# Docker Security Guide

*This documentation is intended for experienced users who want to enhance the security of their installation. If you have suggestions for improvement, please let us know by clicking :material-file-edit-outline: to send a pull request.*

## Get the Latest Security Updates

Even though [PhotoPrism](https://github.com/photoprism/photoprism) is [developed in Go](https://go.dev/) and therefore does not use many of the C libraries installed in our Docker image, external file converters like Darktable and FFmpeg as well as other tools installed as dependencies might use them. They may also be directly affected by [recently discovered vulnerabilities](https://ubuntu.com/security/cves) for which updates are available.

To automatically install these updates when the container starts for the first time, you can add `PHOTOPRISM_INIT: "update"` to the `environment` section of the `photoprism` service in your `compose.yaml` or `docker-compose.yml`:

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_INIT: "update"
      ...
    volumes:
      - ...
```

This can be combined with [other init actions](../config-options.md#docker-image) such as `https` and/or `gpu`, e.g. `PHOTOPRISM_INIT: "update https gpu"`. For the changes to take effect, run the following to restart the services (`--force-recreate` will always recreate the containers to apply available updates, even if their configuration has not been changed):

```bash
docker compose stop
docker compose up -d --force-recreate
```

Init actions are not performed if you use the [hardened configuration](#hardened-configuration) described below. In this case, pull updated images regularly, e.g. with `docker compose pull`, to get the latest security updates.

We also recommend making sure that the latest Docker version and security updates are automatically installed on your host operating system.

!!! tldr ""
    Note that our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible distributions.

## Run Services as Non-Root User

We recommend running the `photoprism` service as a non-root user by setting the `user` [service property](https://docs.docker.com/reference/compose-file/services/#user) in your `compose.yaml` or `docker-compose.yml` file, so that the container starts with this user ID:

```yaml
services:
  photoprism:
    user: "1000"
```

Specify only the user ID, for example `user: "1000"`, so that the service keeps its `video` and `render` group memberships. Add a group ID, as in `"1000:1000"`, only if network storage such as NFS requires it to read and write files. With our default entrypoint, the supported user IDs are 0, 33, 50-99, 500-600, 900-1250, and 2000-2100.

*If you are using [hardware video transcoding](transcoding.md#intel-quick-sync), it should depend on the owner of the video device which user and group you choose so that the service has permission to access it.*

### Hardened Configuration

When a high level of security is required, you can bypass our init script and entrypoint entirely, so that the container runs the `photoprism` binary directly as a non-root user, without additional privileges and capabilities:

```yaml
services:
  photoprism:
    user: "1000"
    entrypoint: ["/opt/photoprism/bin/photoprism"]
    command: ["start"]
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
```

This trades some convenience and functionality for security:

- [Init actions](../config-options.md#docker-image) specified with `PHOTOPRISM_INIT`, such as `update`, `https`, `gpu`, or the installation of hardware drivers, are not performed. Pull updated images instead, e.g. with `docker compose pull`, and run a [reverse proxy](../proxies/index.md) if you need HTTPS, since no default certificate is created.
- File permissions are not updated automatically, so the storage and originals folders must already be readable and writable by the user ID you specify.
- `PHOTOPRISM_UID`, `PHOTOPRISM_GID`, and `PHOTOPRISM_UMASK` have no effect.

The `no-new-privileges` and `cap_drop` settings require the entrypoint override shown above. Our default entrypoint needs these privileges to start, so the container will exit with an error if you add them without bypassing it.

### Compatibility Option

If your platform does not allow you to set the `user` property, for example in the container interface of some NAS devices, you can set the `PHOTOPRISM_UID` and `PHOTOPRISM_GID` [environment variables](../config-options.md#docker-image) instead. In this case, the container starts as root, performs the initialization, and then runs the app under the specified user and group IDs. Use the `user` property instead whenever your environment supports it.

| Environment    | Default | Description                                                                                                                                                                                  |
|----------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_UID | 0       | run as a non-root user after initialization (supported: 0, 33, 50-99, 500-600, 900-1250, and 2000-2100)                                                                                      |
| PHOTOPRISM_GID | 0       | run with a specific group id after initialization, can optionally be used together with `PHOTOPRISM_UID` (supported: 0, 33, 44, 50-99, 105, 109, 115, 116, 500-600, 900-1250, and 2000-2100) |

Do not set both the `user` property and these environment variables.

### Apply Changes

Finally, remember to [update the file permissions and/or owner](../troubleshooting/docker.md#file-permissions) with the `chmod` and `chown` commands when you make changes to the UID or GID, and [restart the services](../docker-compose.md#step-2-start-the-server) for your changes to take effect:

```bash
docker compose stop
docker compose up -d
```

## Remove Passwords From the Environment

Passwords specified directly in a  `compose.yaml` file or otherwise passed to the container environment may pose a security risk. As an alternative, they can be set in an [options.yml](../config-files/index.md) file located in the _config_ [storage folder](../docker-compose.md#photoprismstorage):

```yaml
AdminPassword: "my super secret password"
DatabasePassword: "my super secret password"
```

Likewise, MariaDB can be configured to use Docker secret files. For details, see the [Docker Compose Documentation](https://docs.docker.com/reference/compose-file/services/#secrets).

The following is an example of the changes to your `compose.yaml` or `docker-compose.yml` file. Note that this example includes only the additional lines required to pass secret files to the MariaDB container:

```yaml
secrets:
  # Secrets are single-line text files where the sole
  # content is the secret. Paths in this example assume
  # that secrets are kept in local ".secrets" folder.
  DB_ROOT_PWD:
    file: .secrets/db_root_pwd.txt
  DB_PWD:
    file: .secrets/db_pwd.txt

services:
  mariadb:
    environment:
      # Change the env variables to _FILE and point them to
      # the file locations within the container.
      MARIADB_PASSWORD_FILE: /run/secrets/DB_PWD
      MARIADB_ROOT_PASSWORD_FILE: /run/secrets/DB_ROOT_PWD
    secrets:
      # Give the container access to the secrets to mount
      # the files within the container.
      - DB_ROOT_PWD
      - DB_PWD
```

## Rootless Docker

In addition, you can run the Docker daemon as a non-root user in rootless mode. Configuring this is beyond the scope of this guide. For more information and instructions, see the [Docker Security Documentation](https://docs.docker.com/engine/security/rootless/).
