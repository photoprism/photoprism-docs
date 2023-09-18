# Docker Security Guide

*For advanced users only. This guide is maintained by the community and may contain inaccurate or incomplete advice. You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.*

## Run Services as Non-Root User

It is recommended that you run the `photoprism` service as a non-root user by setting either the `user` [service property](https://docs.docker.com/compose/compose-file/05-services/#user) or the `PHOTOPRISM_UID` and `PHOTOPRISM_GID` [environment variable](../config-options.md#docker-image) in your `docker-compose.yml` file:

| Environment              | Default | Description                                                                                                                                                                       |
|--------------------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_UID           | 0       | run as a non-root user after initialization (supported: 0, 33, 50-99, 500-600, and 900-1200)                                                                                      |
| PHOTOPRISM_GID           | 0       | run with a specific group id after initialization, can optionally be used together with `PHOTOPRISM_UID` (supported: 0, 33, 44, 50-99, 105, 109, 115, 116, 500-600, and 900-1200) |

*If you are using [hardware video transcoding](transcoding.md#intel-quick-sync), it should depend on the owner of the video device which user and group you choose so that the service has permission to access it.*

Finally, remember to [update the file permissions and/or owner](../troubleshooting/docker.md#file-permissions) with the `chmod` and `chown` commands when you make changes to the UID or GID, and [restart the services](../docker-compose.md#step-2-start-the-server) for your changes to take effect:

```bash
docker compose stop
docker compose up -d
```

!!! tldr ""
    Note that our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible Linux distributions.

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