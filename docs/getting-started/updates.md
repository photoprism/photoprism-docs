# Getting Updates

!!! example ""
    **Back us on [Patreon](https://www.patreon.com/photoprism) or [GitHub Sponsors](https://github.com/sponsors/photoprism).**
    Your continued support [helps us](../funding.md) provide services like world maps and develop new features. Thank you! 💜

### Docker Compose ###

Open a terminal and change to the folder where the `docker-compose.yml` file was saved.
Now run the following commands to download the most recent image from Docker Hub and
restart your instance in the background:

```
docker-compose pull photoprism
docker-compose stop photoprism
docker-compose up -d photoprism
```

Pulling a new version can take several minutes, depending on your internet connection speed.

Advanced users can add these commands to a `Makefile` so that they only have to type a single 
command like `make update`. See [command reference](docker-compose.md#command-line-interface)
to learn more about terminal commands.

!!! info ""
    Running an image with `:latest` tag does not cause Docker to automatically download new images.

!!! tldr ""
    You can test upcoming features and improvements by changing the image from `photoprism/photoprism:latest`
    to `photoprism/photoprism:preview` in your [`docker-compose.yml`](https://dl.photoprism.app/docker/).
    Then pull the most recent image and restart your instance as shown above.
    There is no preview available for 32-bit operating systems.

### Raspberry Pi ###

Our [stable version](https://docs.photoprism.app/release-notes/) and development preview have been built into a
single [multi-arch image](https://hub.docker.com/r/photoprism/photoprism) for common 64-bit AMD, Intel,
and ARM processors.

That means, [Raspberry Pi](raspberry-pi.md) 3 / 4 owners can now pull from the same repository,
enjoy the exact same functionality, and can follow the regular [installation instructions](docker-compose.md)
after going through a short list of [requirements](raspberry-pi.md#system-requirements).

Alternative Docker images are provided for [ARMv7-based devices](raspberry-pi.md#older-armv7-based-devices)
and those with a 32-bit operating system.

### Facial Recognition ###

Existing users may index faces without performing a complete rescan:

```
docker-compose exec photoprism photoprism faces index
```

Remove existing people and faces for a clean start e.g. after upgrading from our 
[development preview](https://docs.photoprism.app/release-notes/#development-preview):

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

Users of our [DigitalOcean 1-Click App](cloud/digitalocean.md) have Watchtower pre-installed.

!!! caution
    Automatic updates may interrupt indexing and import operations.
    Only enable Watchtower if you are comfortable with this.

### Pure Docker ###

Open a terminal on your server, and run the following command to pull the most recent container image:

```
docker pull photoprism/photoprism:latest
```

See [Running PhotoPrism with Docker](docker.md) for a command reference.
