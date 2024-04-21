# Running PhotoPrism on a Raspberry Pi

Our [stable releases](../release-notes.md) and [preview builds](updates.md#development-preview) are available as [multi-arch Docker images](https://hub.docker.com/r/photoprism/photoprism/tags) for 64-bit AMD, Intel, and ARM processors.[^1]
As a Raspberry Pi owner, you therefore get the exact same functionality and can follow the same [installation steps](docker-compose.md) after going through a short list of [system requirements](#system-requirements) and [architecture specific notes](#architecture-specific-notes).

!!! verified "PhotoPrismPi"
    The easiest way to run PhotoPrism on a Raspberry Pi[^2] is with [PhotoPrismPi](raspberry-pi/microsd-image.md).
    Simply [flash the image](raspberry-pi/microsd-image.md) to an SD card, plug it into the Pi and boot it. After a few minutes, our latest release will be ready to use!

### System Requirements ###

- For a good user experience, we recommend running PhotoPrism on [a Raspberry Pi 4 or 5 with at least 4 GB RAM](#is-a-raspberry-pi-fast-enough) and a [64-bit operating system](#modern-arm64-based-devices)
- High-resolution panoramic images may require additional swap space and/or physical memory above the [recommended minimum](index.md#system-requirements)
- Indexing performance will benefit greatly from [using SSD storage](troubleshooting/performance.md#storage), e.g. connected via USB 3
- Ensure that your device has [at least 4 GB of swap](troubleshooting/docker.md#adding-swap) configured and avoid setting a [hard memory limit](faq.md#why-is-my-configured-memory-limit-exceeded-when-indexing-even-though-photoprism-doesnt-actually-seem-to-use-that-much-memory) as that can cause unexpected restarts when the indexer temporarily needs more memory to process large files
- Indexing RAW images and high-resolution panoramas may require additional [swap space](troubleshooting/docker.md#adding-swap) and/or physical memory beyond the recommended minimum; RAW image conversion and TensorFlow are disabled on systems with 1 GB or less memory
- You should [enable HTTPS](using-https.md#how-to-enable-https) or run your server behind a [secure HTTPS reverse proxy like Traefik](proxies/traefik.md) if it is connected to a shared network or the public Internet
- Depending on the Linux distribution, you may need to set the following [security options](troubleshooting/docker.md#kernel-security) in your [docker-compose.yml](https://dl.photoprism.app/docker/arm64/docker-compose.yml):
  ```yaml
  photoprism:
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
  ```

### Architecture Specific Notes ###

#### Modern ARM64-based Devices ####

| Image               | Name                            |
|---------------------|---------------------------------|
| Stable Release      | `photoprism/photoprism:latest`  | 
| Development Preview | `photoprism/photoprism:preview` | 
| MariaDB             | `arm64v8/mariadb:10.11`         | 

Running 64-bit Docker images under Raspbian Linux requires a minimum of technical experience to perform the necessary [configuration changes](#raspberry-pi-os). This is because it is a 32-bit operating system with merely a 64-bit kernel to ensure compatibility with legacy software.  If you don't need compatibility with 32-bit apps, we recommend choosing a standard 64-bit Linux distribution instead as it will save you time and requires less experience:

- [Raspberry Pi Debian](https://raspi.debian.net/)
- [Ubuntu for Raspberry Pi](https://ubuntu.com/raspberry-pi)
- [UbuntuDockerPi](https://github.com/guysoft/UbuntuDockerPi) is a 64-bit Ubuntu Server with Docker pre-configured


!!! info ""
    Other distributions that target the same use case as Raspbian, such as CoreELEC, will have similar issues and should therefore also be avoided to run modern server applications.

##### Raspberry Pi OS #####

To ensure compatibility with 64-bit Docker images, your Raspberry Pi must boot with the `arm_64bit=1` flag in its [config.txt file](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).
An "exec format" error will occur otherwise.

Try explicitly pulling the ARM64 version if you've booted your device with the `arm_64bit=1` flag 
and you see the "no matching manifest" error on Raspberry Pi OS (Raspbian):

```bash
docker pull --platform=arm64 photoprism/photoprism:latest
```

It may also help to set the `DOCKER_DEFAULT_PLATFORM` environment variable to `linux/arm64`.

In case you see Docker errors related to "cgroups", try adding the following parameters to 
`/boot/firmware/cmdline.txt` or `/boot/cmdline.txt` (file location depends on the OS in use):

```
cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1
```

#### Older ARMv7-based Devices ####

You may use the following [32-bit Docker images](https://hub.docker.com/r/photoprism/photoprism/tags?page=1&name=armv7)
to run PhotoPrism and MariaDB on ARMv7-based devices (always use our ARM64 image if possible):

| Image               | Name                                  |
|---------------------|---------------------------------------|
| Stable Release      | `photoprism/photoprism:armv7`         |
| Development Preview | `photoprism/photoprism:preview-armv7` |
| MariaDB             | `yobasystems/alpine-mariadb:latest`   |

If your device meets the [requirements](#system-requirements), mostly the same installation instructions as for regular Linux servers apply.
However, you should pay close attention to differences in path and environment variable names.

!!! note ""
    Darktable is not included in the ARMv7 image because it is not 32-bit compatible. Always choose the regular
    64-bit version if your device supports it.

### Is a Raspberry Pi fast enough? ###

This mainly depends on your expectations and the number of files you have. Most users report that PhotoPrism runs smoothly on a Raspberry Pi 4 with 4 GB of RAM.

Note, however, that [initial indexing usually takes much longer](../user-guide/first-steps.md) than on a regular desktop computer and that the hardware has [limited video transcoding capabilities](advanced/transcoding.md), so video file format conversion is not well supported and software transcoding is generally slow. We take no responsibility for instability or performance problems if your device does not [meet the requirements](#system-requirements).

### Getting Updates ###

Open a terminal and change to the folder where the `docker-compose.yml` file is located.[^3]
Now run the following commands to download the newest image from Docker Hub and
restart your instance in the background:

```bash
docker compose pull
docker compose stop
docker compose up -d
```

Pulling a new version can take several minutes, depending on your internet connection speed.

Advanced users can [add this to a `Makefile`](https://dl.photoprism.app/docker/Makefile) so that they only have to type a single
command like `make update`. See [Command-Line Interface](docker-compose.md#command-line-interface) 
to learn more about terminal commands.

!!! tldr ""
    Even when you use an image with the `:latest` tag, Docker does not automatically download new images for you. You can either manually upgrade as shown above, or set up a service like [Watchtower](updates.md#watchtower) to get automatic updates.

#### Config Examples ####

We recommend that you compare your own `docker-compose.yml` with [our latest examples](https://dl.photoprism.app/docker/) from time to time, as they may include new [config options](config-options.md) or other enhancements relevant to you.

#### MariaDB Server ####

Our [config examples](https://dl.photoprism.app/docker/) are generally based on the [latest stable release](https://mariadb.com/kb/en/mariadb-server-release-dates/) to take advantage of performance enhancements.
This does not mean [older versions](index.md#databases) are no longer supported and you have to upgrade immediately.

!!! note ""
    If MariaDB fails to start after upgrading from an earlier version (or migrating from MySQL), the internal management schema may be outdated. See [Troubleshooting MariaDB Problems](troubleshooting/mariadb.md#version-upgrade) for instructions on how to fix this.

### Troubleshooting ###

If your device runs out of memory, the index is frequently locked, or other system resources are running low:

- [ ] Try [reducing the number of workers](config-options.md#index-workers) by setting `PHOTOPRISM_WORKERS` to a reasonably small value in `docker-compose.yml`, depending on the performance of your device
- [ ] Ensure that your device has [at least 4 GB of swap](troubleshooting/docker.md#adding-swap) configured and avoid setting a [hard memory limit](faq.md#why-is-my-configured-memory-limit-exceeded-when-indexing-even-though-photoprism-doesnt-actually-seem-to-use-that-much-memory) as that can cause unexpected restarts when the indexer temporarily needs more memory to process large files
- [ ] If you are using SQLite, switch to MariaDB, which is [better optimized for high concurrency](faq.md#should-i-use-sqlite-mariadb-or-mysql)
- [ ] As a last measure, you can [disable the use of TensorFlow](config-options.md#feature-flags) for image classification and facial recognition

Other issues? Our [troubleshooting checklists](troubleshooting/index.md) help you quickly diagnose and solve them.

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://www.photoprism.app/membership) receive direct [technical support](https://www.photoprism.app/contact) via email.
    Before submitting a support request, try to [determine the cause of your problem](troubleshooting/index.md).

[^1]: Experienced users can [alternatively use the packages](faq.md#installation-packages) at [dl.photoprism.app/pkg/linux/](https://dl.photoprism.app/pkg/linux/README.html) to manually install PhotoPrism on compatible Linux distributions. For more installation methods, see our [Getting Started FAQ](faq.md#how-can-i-install-photoprism-without-docker).
[^2]: Since our current [MicroSD image](raspberry-pi/microsd-image.md) is based on Ubuntu 22.04 LTS, it is not yet compatible with the Raspberry Pi 5, which [requires Ubuntu 23.10+](https://ubuntu.com/download/raspberry-pi). An updated image will be provided as soon as possible.
[^3]: The default [Docker Compose](https://docs.docker.com/compose/) config filename is `docker-compose.yml`. For simplicity, it doesn't need to be specified when running `docker compose` or `docker-compose` in the same directory. Config files for other apps or instances should be placed in separate folders.

*[Raspbian]: Raspberry Pi OS
*[Apple Silicon]: Apple M1 and M2
