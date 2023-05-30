# Docker Security Guide

*For advanced users only: The following recommendations, which are intended to improve the security of your Docker environment, were provided by a contributor and are not part of the original software distribution.  As such, they have not been officially released, recommended, or extensively tested by us. You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.*

## Run Services as Non-Root User

It is recommended that you run the PhotoPrism service as a non-root user by setting either the `user` [service property](https://docs.docker.com/compose/compose-file/05-services/#user) or the `PHOTOPRISM_UID` [environment variable](../config-options.md#docker-image) in your `docker-compose.yml` file.

Remember to [update the file permissions and/or ownership](../troubleshooting/docker.md#file-permissions) with the `chmod` and `chown` commands when you make changes to these settings.

## Remove Passwords From the Environment

Passwords specified directly in a  `docker-compose.yml` file or otherwise passed to the container environment may pose a security risk. As an alternative, they can be set in an [options.yml](../config-files/index.md) file located in the _config_ [storage folder](../docker-compose.md#photoprismstorage):

```yaml
AdminPassword: "my super secret password"
DatabasePassword: "my super secret password"
```

Likewise, MariaDB can be configured to use Docker secret files. For details, see the [official Docker Compose documentation](https://docs.docker.com/compose/compose-file/05-services/#secrets).

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