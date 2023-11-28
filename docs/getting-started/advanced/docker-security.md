# Docker Security Guide

*This documentation is intended for experienced users who want to enhance the security of their installation. If you have suggestions for improvement, please let us know by clicking :material-file-edit-outline: to submit a change request.*

## Get the Latest Security Updates

Even though [PhotoPrism](https://github.com/photoprism/photoprism) is [developed in Go](https://go.dev/) and therefore does not use many of the C libraries installed in our Docker image, external file converters like Darktable and FFmpeg as well as other tools installed as dependencies might use them. They may also be directly affected by [recently discovered vulnerabilities](https://ubuntu.com/security/cves) for which updates are available.

To automatically install these updates when the container starts for the first time, you can add `PHOTOPRISM_INIT: "update"` to the `environment` section of the `photoprism` service in your `docker-compose.yml`:

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_INIT: "update"
      ...
    volumes:
      - ...
```

This can be combined with [other init actions](../config-options.md#docker-image) such as `https`, `gpu` and `tensorflow`, e.g. `PHOTOPRISM_INIT: "update https gpu tensorflow"`. For the changes to take effect, run the following to restart the services (`--force-recreate` will always recreate the containers to apply available updates, even if their configuration has not been changed):

```bash
docker compose stop
docker compose up -d --force-recreate
```

We also recommend making sure that the latest Docker version and security updates are automatically installed on your host operating system.

!!! tldr ""
    Note that our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible Linux distributions.

## Run Services as Non-Root User

It is recommended that you run the `photoprism` service as a non-root user by setting either the `user` [service property](https://docs.docker.com/compose/compose-file/05-services/#user) or the `PHOTOPRISM_UID` and `PHOTOPRISM_GID` [environment variable](../config-options.md#docker-image) in your `docker-compose.yml` file:

| Environment              | Default | Description                                                                                                                                                                                  |
|--------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_UID           | 0       | run as a non-root user after initialization (supported: 0, 33, 50-99, 500-600, 900-1250, and 2000-2100)                                                                                      |
| PHOTOPRISM_GID           | 0       | run with a specific group id after initialization, can optionally be used together with `PHOTOPRISM_UID` (supported: 0, 33, 44, 50-99, 105, 109, 115, 116, 500-600, 900-1250, and 2000-2100) |

*If you are using [hardware video transcoding](transcoding.md#intel-quick-sync), it should depend on the owner of the video device which user and group you choose so that the service has permission to access it.*

Finally, remember to [update the file permissions and/or owner](../troubleshooting/docker.md#file-permissions) with the `chmod` and `chown` commands when you make changes to the UID or GID, and [restart the services](../docker-compose.md#step-2-start-the-server) for your changes to take effect:

```bash
docker compose stop
docker compose up -d
```

## Remove Passwords From the Environment

Passwords specified directly in a  `docker-compose.yml` file or otherwise passed to the container environment may pose a security risk. As an alternative, they can be set in an [options.yml](../config-files/index.md) file located in the _config_ [storage folder](../docker-compose.md#photoprismstorage):

```yaml
AdminPassword: "my super secret password"
DatabasePassword: "my super secret password"
```

Likewise, MariaDB can be configured to use Docker secret files. For details, see the [Docker Compose Documentation](https://docs.docker.com/compose/compose-file/05-services/#secrets).

The following is an example of the changes to the `docker-compose.yml` file. Note that this example includes only the additional lines required to pass secret files to the MariaDB container:

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