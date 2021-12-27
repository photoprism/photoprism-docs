# Running PhotoPrism on a Raspberry Pi

Our [stable version](../release-notes.md) and development preview have been built into a single
[multi-arch image](https://hub.docker.com/r/photoprism/photoprism) for 64-bit AMD, Intel, and ARM processors.

That means, Raspberry Pi 3 / 4, Apple M1, and other ARM64 users can pull from the same repository, 
enjoy the exact same functionality, and can follow the regular [Installation Instructions](docker-compose.md) 
after going through a short list of [System Requirements](#system-requirements) and 
[Architecture Specific Notes](#architecture-specific-notes).

!!! tldr ""
    Existing users are advised to keep their `docker-compose.yml` config updated based on the examples
    available at [dl.photoprism.app/docker](https://dl.photoprism.app/docker/).

### System Requirements ###

- Your device should have at least 4 GB of memory. Running PhotoPrism on a server with [less than 4 GB of swap space](troubleshooting.md#adding-swap)
  or setting a memory/swap limit can cause unexpected restarts, especially when the indexer temporarily needs more
  memory to process large files.
- If you see Docker errors related to "cgroups", it may help to add the following to `/boot/firmware/cmdline.txt`:
  ```
  cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1
  ```
- We [recommend](troubleshooting.md#linux-kernel-security) disabling Linux kernel security in your 
  [docker-compose.yml](https://dl.photoprism.app/docker/arm64/docker-compose.yml), especially if you do 
  not have experience with the configuration:
  ```yaml
  photoprism:
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
  ```
- If you install PhotoPrism on a public server outside your home network, please always run it behind a secure
  HTTPS reverse proxy such as [Traefik](proxies/traefik.md), [Caddy](proxies/caddy-2.md), or [NGINX](proxies/nginx.md).
  Your files and passwords will otherwise be transmitted in clear text and can be intercepted by anyone, 
  including your provider, hackers, and governments.

!!! note ""
    Indexing large photo and video collections significantly benefits from [local SSD storage](performance.md#storage)
    and plenty of memory for caching. Especially the conversion of RAW images and the transcoding of
    videos are very demanding.

!!! info ""
    If you're running out of memory - or other system resources - while indexing, try reducing the
    [number of workers](https://docs.photoprism.app/getting-started/config-options/) by setting
    `PHOTOPRISM_WORKERS` to a reasonably small value in `docker-compose.yml` (depending on the performance of the server).
    As a measure of last resort, you may disable using TensorFlow for image classification and facial recognition.

### Architecture Specific Notes ###

#### Modern ARM64-based Devices ####

| Image               | Name                               |
|---------------------|------------------------------------|
| Stable Release      | `photoprism/photoprism:latest`     | 
| Development Preview | `photoprism/photoprism:preview`    | 
| MariaDB             | `arm64v8/mariadb:10.6`             | 

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

##### Raspbian Alternatives #####

Raspberry Pi OS is designed to be compatible with older 32-bit applications. We recommend choosing 
a standard 64-bit Linux distribution to run modern server applications, for example:

- [UbuntuDockerPi](https://github.com/guysoft/UbuntuDockerPi) is a 64-bit Ubuntu Server with Docker pre-configured
- [Ubuntu for Raspberry Pi](https://ubuntu.com/raspberry-pi)
- [Ubuntu MATE for Raspberry Pi](https://ubuntu-mate.org/raspberry-pi/)

#### Older ARMv7-based Devices ####

You have to resort to alternative Docker images to run PhotoPrism and MariaDB on ARMv7-based devices
and those with a 32-bit operating system:

| Image             | Name                                |
|-------------------|-------------------------------------|
| ARMv7 Release     | `photoprism/photoprism:armv7`       | 
| MariaDB           | `linuxserver/mariadb:latest`        | 

If your device meets the [requirements](#system-requirements), mostly the same installation instructions as 
for regular Linux servers apply. Pay close attention to changed directory and environment variable names.

!!! tldr ""
    Darktable is not included in the ARMv7 version because it is not 32-bit compatible.

### Getting Updates ###

Open a terminal and change to the folder where the `docker-compose.yml` file was saved.
Now run the following commands to download the most recent image from Docker Hub and
restart your instance in the background:

```
docker-compose pull photoprism
docker-compose stop photoprism
docker-compose up -d photoprism
```

Pulling a new version can take several minutes, depending on your internet connection speed.

Advanced users can add this to a `Makefile` so that they only have to type a single
command like `make update`. See [Command-Line Interface](docker-compose.md#command-line-interface) 
to learn more about terminal commands.

!!! info ""
    Running an image with `:latest` tag does not cause Docker to automatically download new images.

### Is a Raspberry Pi fast enough? ###

This depends largely on your expectations and the number of files you have. Most users report that
PhotoPrism runs smoothly on their Raspberry Pi 4. However, the initial indexing typically takes longer
than even on 8-year-old standard desktop CPUs.

Also keep in mind that the hardware has limited video transcoding capabilities, so the conversion of video
file formats is not well-supported and software transcoding is generally slow.

Ideally, you can test a friend's device before you buy one, or make sure you can return it.

### Credits ###

A big thank you to [Guy Sheffer](https://github.com/guysoft) for helping us [build](https://github.com/photoprism/photoprism/issues/109)
a Raspberry Pi version!
