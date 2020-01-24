# Configuration

## Help ##
`photoprism help` shows all available commands and config parameters.

## Show current settings ##
`photoprism config` shows all config parameters and their values.

## Change settings ##
You can either use environment variables like `PHOTOPRISM_CACHE_PATH`, a [config file](https://github.com/photoprism/photoprism/blob/develop/configs/photoprism.yml) or command line parameters like `--cache-path` to configure PhotoPrism. [Environment variables](https://docs.docker.com/compose/environment-variables/) are usually best for dockerized applications. You can easily set them in [docker-compose.yml](https://github.com/photoprism/photoprism/blob/develop/docker-compose.yml) without touching any other files.

There is no need to change any settings if you follow the steps described in [Setup](setup.md).
