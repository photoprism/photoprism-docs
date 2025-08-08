# Getting Updates

### Docker Compose

Open a terminal and change to the folder where your `compose.yaml` file is located.[^1]
Now run the following commands to download the newest image from [Docker Hub](https://hub.docker.com/r/photoprism/photoprism/tags) and restart your instance in the background:

```bash
docker compose pull
docker compose stop
docker compose up -d
```

*Note that our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible distributions.*

Pulling a new version can take several minutes, depending on your internet connection speed.

Advanced users can [add this to a `Makefile`](https://dl.photoprism.app/docker/Makefile) so that they only have to type a single command like `make update`. See [Command-Line Interface](docker-compose.md#command-line-interface) to learn more about terminal commands.

!!! tldr ""
    Even when you use an image with the `:latest` tag, Docker does not automatically download new images for you. You can either manually upgrade as shown above, or set up a service like [Watchtower](#watchtower) to get automatic updates.

#### Config Examples

We recommend that you compare your own `compose.yaml` with [our latest examples](https://dl.photoprism.app/docker/) from time to time, as they may include new [config options](config-options.md) or other enhancements relevant to you.

#### Development Preview

You can test [**upcoming features and enhancements**](https://link.photoprism.app/roadmap) by changing the `photoprism/photoprism` image tag from `:latest` to [`:preview`](https://hub.docker.com/r/photoprism/photoprism/tags?page=1&name=preview) and then running the following commands to download the newest image from [Docker Hub](https://hub.docker.com/r/photoprism/photoprism/tags) and restart your instance in the background:

```bash
docker compose pull
docker compose stop
docker compose up -d
```

*Note that our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible distributions.*

#### Watchtower

Adding [Watchtower](https://github.com/containrrr/watchtower) as a service to your `compose.yaml` or `docker-compose.yml` will automatically keep images up-to-date:

```yaml
services:
  watchtower:
    image: containrrr/watchtower
    restart: unless-stopped
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
```

Users of our [DigitalOcean 1-Click App](cloud/digitalocean.md) have Watchtower pre-installed.

!!! danger
    Keep in mind that automatic updates can interrupt indexing and import operations, and enable Watchtower only if this is acceptable to you.

### Portainer

You can [change or update the image you are using](portainer/index.md) by navigating to "Stacks", selecting your existing PhotoPrism stack, and clicking "Editor":

![Screenshot](portainer/preview.png){ class="shadow" }

When you have [changed the configuration](portainer/index.md) to your needs or just want to get the latest image from Docker Hub, scroll down, click on "Update the stack", enable the "re-pull and redeploy" option, and then click on "Update":

![Screenshot](portainer/update.png){ class="shadow" }

### Pure Docker

Open a terminal and run the following to download the newest image from [Docker Hub](https://hub.docker.com/r/photoprism/photoprism/tags):

```bash
docker pull photoprism/photoprism:latest
```

Then stop and [recreate the `photoprism` service](docker.md#step-1-start-the-server) based on the new image, for example:

```bash
docker stop photoprism
docker rm photoprism
docker run -d \
      --name photoprism \
      --security-opt seccomp=unconfined \
      --security-opt apparmor=unconfined \
      -p 2342:2342 \
      -e PHOTOPRISM_UPLOAD_NSFW="true" \
      -e PHOTOPRISM_ADMIN_PASSWORD="insecure" \
      -v /photoprism/storage \
      -v ~/Pictures:/photoprism/originals \
      photoprism/photoprism:latest
```

[Learn more ›](docker.md)

!!! tldr ""
    In order to simplify configuration and updates, we recommend using [Docker Compose](docker-compose.md) instead of [Docker](docker.md).

### OpenMediaVault

To upgrade your instance, first connect to the server running OpenMediaVault via SSH or open a terminal from the web interface, then download the newest image from [Docker Hub](https://hub.docker.com/r/photoprism/photoprism/tags) and restart the service:

```bash
sudo podman pull docker.io/photoprism/photoprism:latest
sudo systemctl restart pod-photoprism.service
```

[Learn more ›](nas/openmediavault.md)

### Complete Rescan

We recommend performing a [complete rescan](../user-guide/library/originals.md#when-should-complete-rescan-be-selected) after major updates to take advantage of new search filters and sorting options. Be sure to [read the notes for each release](../release-notes.md) to see what changes have been made and if they might affect your library, for example, because of the file types you have or because new search features have been added. If you encounter problems that you cannot solve otherwise (i.e. before reporting a bug), please also try a rescan and see if it solves the problem.

You can start a [rescan from the user interface](../user-guide/library/originals.md) by navigating to *Library* > *Index*, selecting "Complete Rescan", and then clicking "Start". Manually entered information such as labels, people, titles or captions will not be modified when indexing, even if you perform a "complete rescan".

!!! tldr ""
    Be careful not to start multiple indexing processes at the same time, as this will lead to a high server load.

### Face Recognition

Existing users may index faces without performing a complete rescan:

```bash
docker compose exec photoprism photoprism faces index
```

Remove existing people and faces for a clean start e.g. after upgrading from our 
[development preview](https://docs.photoprism.app/release-notes/#development-preview):

```bash
docker compose exec photoprism photoprism faces reset -f
```

### MariaDB Server

Our [configuration examples](https://dl.photoprism.app/docker/) are generally based on the [current stable version](https://mariadb.com/docs/release-notes/community-server) to take advantage of performance improvements. This does not mean that [older versions](index.md#databases) are no longer supported and you must upgrade immediately.

We recommend using a version or subversion tag, such as `:11` or [`:11.8`](https://mariadb.org/11-8-lts-released/), instead of `:latest`, to specify the MariaDB service image in your `compose.yaml` file, as shown in this example:

```yaml
services:
  mariadb:
    image: mariadb:11.8
    ...
```

You can then manually upgrade to [new major versions](https://mariadb.com/docs/release-notes/community-server) by changing the image tag, e.g. from `mariadb:11` to `mariadb:12`, once [they are stable](https://mariadb.org/about/#maintenance-policy) and we had time to test them. 

However, this requires periodically checking for [new MariaDB images](https://hub.docker.com/_/mariadb) and adjusting [your `compose.yaml` file](docker-compose.md#database) accordingly, so you don't get stuck with an [outdated](https://mariadb.org/about/#maintenance-policy) version.

[Learn more ›](troubleshooting/mariadb.md#auto-upgrade)

!!! note ""
    If MariaDB fails to start after upgrading from an earlier version (or migrating from MySQL), the internal management schema may be outdated. See [Troubleshooting MariaDB Problems](troubleshooting/mariadb.md#version-upgrade) for instructions on how to fix this.

### Raspberry Pi

Our [stable releases](../release-notes.md) and [preview builds](updates.md#development-preview) are available as [multi-arch Docker images](https://hub.docker.com/r/photoprism/photoprism/tags) for 64-bit AMD, Intel, and ARM processors.
You therefore get the exact same functionality and can follow the same [update instructions](#docker-compose) if your device [meets the system requirements](raspberry-pi.md#system-requirements).

Try explicitly pulling the ARM64 version if you've booted your device with the `arm_64bit=1` flag and you see the "no matching manifest" error on [Raspberry Pi OS](raspberry-pi.md#raspberry-pi-os) (Raspbian):

```bash
docker pull --platform=arm64 photoprism/photoprism:latest
```

If you don't use legacy software, we recommend choosing a [standard 64-bit Linux distribution](raspberry-pi.md#modern-arm64-based-devices) as it requires less experience. For [ARMv7-based devices](raspberry-pi.md#older-armv7-based-devices), 32-bit images are [provided separately](https://hub.docker.com/r/photoprism/photoprism/tags?page=1&name=armv7).

!!! tldr ""
    Darktable is not included in the ARMv7 version because it is not 32-bit compatible.

### PhotoPrism® Plus

Our members can activate [additional features](https://link.photoprism.app/membership) by logging in with the [admin user created during setup](config-options.md#authentication) and then following the steps [described in our activation guide](https://www.photoprism.app/kb/activation). Thank you for your support, which has been and continues to be essential to the success of the project! :octicons-heart-fill-24:{ .heart .purple }

[Compare Memberships ›](https://link.photoprism.app/membership){ class="pr-3 block-xs" } [View Membership FAQ ›](https://www.photoprism.app/membership/faq) 

!!! example ""
    We recommend that new users install our free [Community Edition](index.md) before [signing up for a membership](https://link.photoprism.app/membership).

### How can I shorten the startup time after a restart or update?

To reduce startup time, do not set `PHOTOPRISM_INIT` to avoid running additional setup scripts, and set `PHOTOPRISM_DISABLE_CHOWN` to `"true"` to [disable automatic permission updates](config-options.md#docker-image).

!!! tldr ""
    If your instance doesn't start even after waiting for some time, our [Troubleshooting Checklists](troubleshooting/index.md#connection-fails) help you quickly diagnose and solve the problem.

[^1]: With the latest version of [Docker Compose](https://docs.docker.com/compose/), the [default config file name](https://docs.docker.com/compose/intro/compose-application-model/#the-compose-file) is `compose.yaml`, although the [`docker compose` command](troubleshooting/docker.md#docker-compose) still supports legacy `docker-compose.yml` files for backward compatibility.