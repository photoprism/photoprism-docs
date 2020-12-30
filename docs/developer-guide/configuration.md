# Configuration

## Help ##
`photoprism help` shows available commands, config parameters and environment variable names.
These are also listed in [Getting Started](/getting-started/config-options/).

## Show current settings ##
`photoprism config` shows all config parameters and their values.

## Change settings ##
You can either use environment variables like `PHOTOPRISM_CACHE_PATH`, config files (in the `storage/config` directory) or command line parameters like `--cache-path` to configure PhotoPrism. [Environment variables](https://docs.docker.com/compose/environment-variables/) are usually best for dockerized applications. You can easily set them in [docker-compose.yml](https://github.com/photoprism/photoprism/blob/develop/docker-compose.yml) without touching any other files.

There is no need to change any settings if you follow the steps described in [Setup](setup.md).
