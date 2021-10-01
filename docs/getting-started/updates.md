# Getting Updates

### Docker Compose ###

Open a terminal on your server, and run the following commands to pull the latest container image and restart PhotoPrism:

```
docker-compose pull photoprism
docker-compose stop photoprism
docker-compose up -d photoprism
```

Pulling a new version can take several minutes, depending on your internet connection.

Advanced users may put this into a `Makefile` so that they only need to type a single command.

See [Setup Using Docker Compose](docker-compose.md) for a full command reference.


!!! important "New Release"
    Our [latest release](../release-notes.md) comes as a single [multi-arch image](https://hub.docker.com/r/photoprism/photoprism)
    for AMD64, ARM64, and ARMv7. That means you don't need to pull from different Docker repositories anymore.
    We recommend updating your existing `docker-compose.yml` config based on [our examples](https://dl.photoprism.org/docker/).

!!! info "Preview Builds"
    Update your `docker-compose.yml` to use `photoprism/photoprism:preview` instead of 
    `photoprism/photoprism:latest` for testing our latest development preview.

### Watchtower ###

Adding [Watchtower](https://github.com/containrrr/watchtower) as a service to your `docker-compose.yml` will
automatically keep images up-to-date:

```yml
services:
  watchtower:
    image: containrrr/watchtower
    restart: unless-stopped
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
```

!!! info
    Automatic updates may interrupt indexing and importing operations. 
    Only enable Watchtower if you are comfortable with this.

### Pure Docker ###

Open a terminal on your server, and run the following command to pull the latest container image:

```
docker pull photoprism/photoprism:latest
```

See [Running PhotoPrism with Docker](docker.md) for a full command reference.

!!! info "Preview Builds"
    Use `photoprism/photoprism:preview` instead of `photoprism/photoprism:latest` for testing 
    our latest development preview.
