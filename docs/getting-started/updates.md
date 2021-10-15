# Getting Updates

!!! note ""
    Our [stable version](../release-notes.md) and development preview now come as a single
    [multi-arch image](https://hub.docker.com/r/photoprism/photoprism) for **AMD64, ARM64, and ARMv7**. 
    That means you don't need to pull from different Docker repositories anymore. We recommend updating your existing 
    `docker-compose.yml` config based on [our examples](https://dl.photoprism.org/docker/).

!!! example ""
    **Back us on [Patreon](https://www.patreon.com/photoprism) or [GitHub Sponsors](https://github.com/sponsors/photoprism).**
    Your continued support helps us provide services like satellite maps and develop new features. Thank you very much! 💜

### Docker Compose ###

Open a terminal and change to the folder in which the `docker-compose.yml` file has been saved.
Now run the following commands to pull the most recent Docker image and restart your instance in the background:

```
docker-compose pull photoprism
docker-compose stop photoprism
docker-compose up -d photoprism
```

Pulling a new version can take several minutes, depending on your internet connection speed.

Advanced users may put this into a `Makefile` so that they only need to type a single command.

See [Setup Using Docker Compose](docker-compose.md) for a command reference.

!!! tldr ""
    You can test our latest features and improvements by changing the image from `photoprism/photoprism:latest`
    to `photoprism/photoprism:preview` in your [`docker-compose.yml`](https://dl.photoprism.org/docker/).
    Then pull the most recent image and restart your instance.

### Facial Recognition ###

Existing users may index faces without performing a complete rescan:

```
docker-compose exec photoprism photoprism faces index
```

Remove existing people and faces for a clean start e.g. after upgrading from our 
[development preview](https://docs.photoprism.org/release-notes/#development-preview):

```
docker-compose exec photoprism photoprism faces reset -f
```

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

Users of our [DigitalOcean 1-Click App](digitalocean.md) have Watchtower pre-installed.

!!! caution
    Automatic updates may interrupt indexing and import operations.
    Only enable Watchtower if you are comfortable with this.

### Pure Docker ###

Open a terminal on your server, and run the following command to pull the most recent container image:

```
docker pull photoprism/photoprism:latest
```

See [Running PhotoPrism with Docker](docker.md) for a command reference.

!!! tldr ""
    You can test our latest features and improvements by using `photoprism/photoprism:preview` 
    instead of `photoprism/photoprism:latest`.
