# Getting Updates

!!! example ""
    **Back us on [Patreon](https://link.photoprism.app/patreon) or [GitHub Sponsors](https://link.photoprism.app/sponsor).**
    Your continued support [helps us](https://photoprism.app/membership) provide [regular updates](https://docs.photoprism.app/release-notes/)
    and services like [world maps](https://try.photoprism.app/library/places). Thank you! :octicons-heart-fill-24:{ .heart .purple }

### Docker Compose

Open a terminal and change to the folder where the `docker-compose.yml` file is located.[^1]
Now run the following commands to download the most recent image from Docker Hub and
restart your instance in the background:

```
docker compose pull
docker compose stop
docker compose up -d
```

*Note that our guides now use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose`.*

Pulling a new version can take several minutes, depending on your internet connection speed.

Advanced users can add this to a `Makefile` so that they only have to type a single 
command like `make update`. See [Command-Line Interface](docker-compose.md#command-line-interface)
to learn more about terminal commands.

!!! tldr ""
    Even when you use an image with the `:latest` tag, Docker does not automatically download new images for you. You can either manually upgrade as shown above, or set up a service like [Watchtower](#watchtower) to get automatic updates.

#### Config Examples

We recommend that you compare your own `docker-compose.yml` with [our latest examples](https://dl.photoprism.app/docker/) from time to time, as they may include new [config options](config-options.md) or other enhancements relevant to you.

#### Development Preview

You can test upcoming features and enhancements by changing the image from `photoprism/photoprism:latest`
to `photoprism/photoprism:preview` in your [`docker-compose.yml`](https://dl.photoprism.app/docker/).
Then pull the most recent image and restart your instance as shown above.

#### Watchtower

Adding [Watchtower](https://github.com/containrrr/watchtower) as a service to your `docker-compose.yml` will
automatically keep images up-to-date:

```yaml
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

### Pure Docker

Open a terminal on your server, and run the following command to pull the most recent container image:

```
docker pull photoprism/photoprism:latest
```

See [Running PhotoPrism with Docker](docker.md) for a command reference.

### Complete Rescan

We recommend performing a complete rescan after major updates to take advantage of new search filters and sorting options. Be sure to [read the notes for each release](../release-notes.md) to find out what changes have been made and if they might affect your library, for example, because of the file types you have or because new search features have been added. If you encounter problems that you cannot solve otherwise (i.e. before reporting a bug), please also try a rescan and see if it solves the problem.

You can start a [rescan from the user interface](../user-guide/library/originals.md) by navigating to *Library* > *Index*, selecting "Complete Rescan", and then clicking "Start". Manually entered information such as labels, people, titles or descriptions will not be modified when indexing, even if you perform a "complete rescan".

### Face Recognition

Existing users may index faces without performing a complete rescan:

```
docker compose exec photoprism photoprism faces index
```

Remove existing people and faces for a clean start e.g. after upgrading from our 
[development preview](https://docs.photoprism.app/release-notes/#development-preview):

```
docker compose exec photoprism photoprism faces reset -f
```

### MariaDB Server

Our [config examples](https://dl.photoprism.app/docker/) are generally based on the [latest stable release](https://mariadb.com/kb/en/mariadb-server-release-dates/) to take advantage of performance enhancements.
This does not mean [older versions](index.md#databases) are no longer supported and you have to upgrade immediately.

!!! note ""
    If MariaDB fails to start after upgrading from an earlier version (or migrating from MySQL), the internal management schema may be outdated. See [Troubleshooting MariaDB Problems](troubleshooting/mariadb.md#version-upgrade) for instructions on how to fix this.

### Raspberry Pi

Our [stable version and development preview](../release-notes.md) have been built into a single
[multi-arch Docker image](https://hub.docker.com/r/photoprism/photoprism) for 64-bit AMD, Intel, and ARM processors.

That means, Raspberry Pi 3 / 4, Apple Silicon, and other ARM64-based devices can pull from the same repository,
enjoy the exact same functionality, and can follow the regular [Installation Instructions](docker-compose.md)
after going through a short list of [System Requirements](raspberry-pi.md#system-requirements) and
[Architecture Specific Notes](raspberry-pi.md#architecture-specific-notes).

Try explicitly pulling the ARM64 version if you've booted your device with the `arm_64bit=1` flag
and you see the "no matching manifest" error on [Raspberry Pi OS](raspberry-pi.md#raspberry-pi-os) (Raspbian):

```bash
docker pull --platform=arm64 photoprism/photoprism:latest
```

If you do not have legacy software, we recommend [choosing a standard 64-bit Linux distribution](raspberry-pi.md#modern-arm64-based-devices)
as this requires less experience. Alternative 32-bit Docker images are provided for [ARMv7-based devices](raspberry-pi.md#older-armv7-based-devices).

!!! tldr ""
    Darktable is not included in the ARMv7 version because it is not 32-bit compatible.

[^1]: The default [Docker Compose](https://docs.docker.com/compose/) config filename is `docker-compose.yml`. For simplicity, it doesn't need to be specified when running the `docker-compose` command in the same directory. Config files for other apps or instances should be placed in separate folders.
