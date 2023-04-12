# Docker Security Guide

The following recommendations are aimed at improving the security of your Docker container.

## Run Services as Non-Root User

We recommend running the PhotoPrism service as a non-root user by setting either the user [service property](https://docs.docker.com/compose/compose-file/05-services/#user) or the `PHOTOPRISM_UID` [environment variable](https://docs.photoprism.app/getting-started/config-options/#docker-image) in the `docker-compose.yml` file.

Don't forget to update file permissions and/or ownership with the `chown` command when you make changes.

## Remove Passwords from the Environment

Passwords specified in a Docker Compose file or otherwise passed into the container's environment represent a security risk. Instead, they can be configured in the [options.yml](https://docs.photoprism.app/getting-started/config-files/) file within the _config_ folder:

```yaml
AdminPassword: "my super secret password"
DatabasePassword: "my super secret password"
```

Likewise, MariaDB can be configured to use Docker secret files. See the [docker compose documentation](https://docs.docker.com/compose/compose-file/05-services/#secrets).

An example of the modifications to `docker-compose.yml` is provided below. Note that this example only contains the additional lines necessary to pass secret files to the MariaDB container.


```yaml
secrets:
  # Secrets are single-line text files where the sole content is the secret
  # Paths in this example assume that secrets are kept in local folder called ".secrets"
  DB_ROOT_PWD:
    file: .secrets/db_root_pwd.txt
  DB_PWD:
    file: .secrets/db_pwd.txt

services:
  mariadb:
    environment:
      # Change the env variables to _FILE and point them to the file locations within the container
      MARIADB_PASSWORD_FILE: /run/secrets/DB_PWD
      MARIADB_ROOT_PASSWORD_FILE: /run/secrets/DB_ROOT_PWD
    secrets:
      # Give the container access to the secrets to mount the files within the container
      - DB_ROOT_PWD
      - DB_PWD
```

## Rootless Docker

The Docker daemon can be run as a non-root user using Rootless Mode.

Configuring this is beyond the scope of these help documents. See the [Docker Security Documentation](https://docs.docker.com/engine/security/rootless/) for more information and instructions.
