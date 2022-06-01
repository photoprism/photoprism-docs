# Running PhotoPrism on a Raspberry Pi

Our [stable version and development preview](../release-notes.md) have been built into a single
[multi-arch Docker image](https://hub.docker.com/r/photoprism/photoprism) for 64-bit AMD, Intel, and ARM processors.

That means, Raspberry Pi 3 / 4, Apple Silicon, and other ARM64-based devices can pull from the same repository,
enjoy the exact same functionality, and can follow the regular [Installation Instructions](docker-compose.md) 
after going through a short list of [System Requirements](#system-requirements).

Note that Raspberry Pi OS (Raspbian) is a 32-bit user-space Linux with a 64-bit kernel to remain compatible with older
Raspberry software. This requires [special configuration](#raspberry-pi-os) to run modern 64-bit applications and Docker
images, see [Architecture Specific Notes](#architecture-specific-notes).

### System Requirements ###

- Your device should have at least 3 GB of physical memory and a 64-bit operating system
- While PhotoPrism has been reported to work on devices with less memory, we take no responsibility for instability or performance problems
- RAW image conversion and TensorFlow are disabled on systems with 1 GB or less memory
- Indexing large photo and video collections significantly benefits from [local SSD storage](troubleshooting/performance.md#storage) and plenty of memory for caching, especially the conversion of RAW images and the transcoding of videos are very demanding
- If less than [4 GB of swap space](troubleshooting/docker.md#adding-swap) is configured or a manual memory/swap limit is set, this can cause unexpected restarts, for example, when the indexer temporarily needs more memory to process large files
- High-resolution panoramic images may require additional swap space and/or physical memory above the recommended minimum
- We recommend disabling [kernel security](troubleshooting/docker.md#kernel-security) in your 
  [docker-compose.yml](https://dl.photoprism.app/docker/arm64/docker-compose.yml), especially if you do 
  not have experience with the configuration:
  ```yaml
  photoprism:
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
  ```
- If you install PhotoPrism on a public server outside your home network, **always run it behind a secure HTTPS reverse proxy** such as [Traefik](proxies/traefik.md) or [Caddy](proxies/caddy-2.md)

### Architecture Specific Notes ###

#### Modern ARM64-based Devices ####

| Image               | Name                            |
|---------------------|---------------------------------|
| Stable Release      | `photoprism/photoprism:latest`  | 
| Development Preview | `photoprism/photoprism:preview` | 
| MariaDB             | `arm64v8/mariadb:10.7`          | 

Raspberry Pi OS (Raspbian) requires [special configuration](#raspberry-pi-os) to run modern 64-bit applications and
Docker images. If you do not have legacy software, we recommend choosing a standard 64-bit Linux distribution as this
requires less experience:

- [Raspberry Pi Debian](https://raspi.debian.net/)
- [Ubuntu for Raspberry Pi](https://ubuntu.com/raspberry-pi)
- [UbuntuDockerPi](https://github.com/guysoft/UbuntuDockerPi) is a 64-bit Ubuntu Server with Docker pre-configured

Other distributions that target the same use case as Raspbian, such as CoreELEC, may have the same problems and
should also not be used to run modern server applications.

##### Raspberry Pi OS #####

To ensure compatibility with 64-bit Docker images, your Raspberry Pi 3 / 4 must boot with
the `arm_64bit=1` flag in its [config.txt file](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).
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
| MariaDB             | `linuxserver/mariadb:latest`          |

If your device meets the [requirements](#system-requirements), mostly the same installation instructions as 
for regular Linux servers apply. Please pay close attention to changed directory and environment variable names.

!!! note ""
    Darktable is not included in the ARMv7 image because it is not 32-bit compatible. Always choose the regular
    64-bit version if your device supports it.

### Is a Raspberry Pi fast enough? ###

This largely depends on your expectations and the number of files you have. Most users report that
PhotoPrism runs smoothly on their Raspberry Pi 4. However, initial indexing typically takes much longer
than on standard desktop computers.

Also keep in mind that the hardware has limited video transcoding capabilities, so the conversion of video
[file formats](../developer-guide/media/index.md) is not well-supported and software transcoding is generally slow.

### Getting Updates ###

Open a terminal and change to the folder where the `docker-compose.yml` file is located.[^1]
Now run the following commands to download the most recent image from Docker Hub and
restart your instance in the background:

```bash
docker-compose pull
docker-compose stop
docker-compose up -d
```

Pulling a new version can take several minutes, depending on your internet connection speed.

Advanced users can add this to a `Makefile` so that they only have to type a single
command like `make update`. See [Command-Line Interface](docker-compose.md#command-line-interface) 
to learn more about terminal commands.

!!! tldr ""
    Running an image with `:latest` tag does not cause Docker to automatically download new images.
    We recommend that you compare your `docker-compose.yml` with our examples at [dl.photoprism.app/docker](https://dl.photoprism.app/docker/) from time to time in case there are new configuration options or other improvements.

### Troubleshooting ###

If your device runs out of memory, the index is frequently locked, or other system resources are running low:

- [ ] Try [reducing the number of workers](config-options.md#index-workers) by setting `PHOTOPRISM_WORKERS` to a reasonably small value in `docker-compose.yml`, depending on the performance of your device
- [ ] Make sure [your device has at least 4 GB of swap space](troubleshooting/docker.md#adding-swap) so that indexing doesn't cause restarts when memory usage spikes; RAW image conversion and video transcoding are especially demanding
- [ ] If you are using SQLite, switch to MariaDB, which is [better optimized for high concurrency](faq.md#should-i-use-sqlite-mariadb-or-mysql)
- [ ] As a last measure, you can [disable the use of TensorFlow](config-options.md#feature-flags) for image classification and facial recognition

Other issues? Our [troubleshooting checklists](troubleshooting/index.md) help you quickly diagnose and solve them.

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://photoprism.app/membership) receive direct [technical support](https://photoprism.app/contact) via email.
    Before submitting a support request, try to [determine the cause of your problem](troubleshooting/index.md).

### Credits ###

A big thank you to [Guy Sheffer](https://github.com/guysoft) for helping us [build](https://github.com/photoprism/photoprism/issues/109)
a Raspberry Pi version!

[^1]: The default [Docker Compose](https://docs.docker.com/compose/) config filename is `docker-compose.yml`. For simplicity, it doesn't need to be specified when running the `docker-compose` command in the same directory. Config files for other apps or instances should be placed in separate folders.
