[Docker](https://www.docker.com/) is an Open Source container virtualization tool. It is ideal for running
applications on any computer without extensive installation, configuration, or performance overhead.

We are aware Docker is not widely used by end users despite its many advantages. For this reason, we aim
to provide native binaries for common operating systems at a later time.

### What are the benefits of using Docker?

**(1) Docker uses standard features of the Linux kernel.** Containers are nothing new; [Solaris Zones](https://en.wikipedia.org/wiki/Solaris_Containers) were released about 20 years ago and the chroot system call was introduced during [development of Version 7 Unix in 1979](https://en.wikipedia.org/wiki/Chroot). It is used ever since for hosting applications exposed to the public Internet. Modern Linux containers are an incremental improvement of this, based on standard functionality that is part of the kernel.

**(2) Docker saves time through simplified deployment and testing.** A main advantage of Docker is that application images can be [easily made available](https://hub.docker.com/r/photoprism/photoprism) to users via Internet. It provides a common standard across most operating systems and devices, which saves our team a lot of time that we can then spend [more effectively](https://docs.photoprism.app/developer-guide/code-quality/#effectiveness-efficiency), for example, providing support and developing one of the many features that users are waiting for.

**(3) Dockerfiles are part of the source code repository.** [Human-readable](https://docs.docker.com/reference/dockerfile/) and [versioned Dockerfiles](https://github.com/photoprism/photoprism/tree/develop/docker) that are part of our public source code help avoid "works for me" moments and other unwelcome surprises by enabling us to have the exact [same environment](https://docs.photoprism.app/developer-guide/setup/) everywhere in [development](https://github.com/photoprism/photoprism/tree/develop/docker/develop), [staging, and production](https://github.com/photoprism/photoprism/tree/develop/docker/photoprism).

**(4) Running applications in containers is more secure.** Last but not least, virtually all file format parsers have vulnerabilities that just haven't been discovered yet. This is a known risk that can affect you even if your computer is not directly connected to the Internet. Running apps in a container with limited host access is an easy way to improve security without compromising performance and usability.

!!! tldr ""
    A virtual machine with a dedicated operating system environment provides even more security, but usually has side effects such as lower performance and more difficult handling. Using a VM, however, doesn't prevent you from running containerized apps to get the best of both worlds. This is essentially what happens when you install Docker on [virtual cloud servers](../../getting-started/cloud/digitalocean.md) and operating systems other than Linux.

## Running Docker Images

Assuming you have Docker installed and want to test Debian 12 "Bookworm", you can simply run this command to open a terminal:

```bash
docker run --rm -v ${PWD}:/test -w /test -ti debian:bookworm bash
```

This will mount the current working directory as `/test`. Of course, you can also specify a full path instead of `${PWD}`.

The available Ubuntu, Debian and PhotoPrism images can be found on Docker Hub:

- https://hub.docker.com/_/ubuntu
- https://hub.docker.com/_/debian
- https://hub.docker.com/r/photoprism/photoprism/tags

Additional packages can be installed via `apt`:

```bash
apt update
apt install -y exiftool libheif-examples
```

## Continuous Integration / Deployment ##

Container images are built and published to [Docker Hub](https://hub.docker.com/r/photoprism/photoprism/tags/) automatically from the `develop` branch once tests pass. We don't use semantic versioning for our preview binaries and images; a version string typically looks like `260520-12dbe82d3` (date + commit hash). The multi-arch build script that drives these publishes is [`scripts/docker/buildx-multi.sh`](https://github.com/photoprism/photoprism/blob/develop/scripts/docker/buildx-multi.sh), and the dev container image used for testing is published as [`photoprism/develop`](https://hub.docker.com/r/photoprism/develop/), see the main [`Dockerfile`](https://github.com/photoprism/photoprism/blob/develop/Dockerfile).

## Multi-Stage Build ##

Docker supports so-called multi-stage builds, which means you can compile an application like PhotoPrism in a container that includes all development dependencies (source code, debugger, compiler, …) and then copy only the resulting binary into a fresh runtime image. This keeps the published runtime image much smaller than the build image; most of the runtime size comes from Darktable, TensorFlow, ONNX Runtime, and the base OS layer, while the `photoprism` binary itself is around 20 MB.

Example:

```Dockerfile
FROM photoprism/develop:resolute AS build

# Build PhotoPrism
WORKDIR "/go/src/github.com/photoprism/photoprism"
COPY . .
RUN make all install DESTDIR=/opt/photoprism

# Same base image family as photoprism/develop
FROM ubuntu:resolute

WORKDIR /opt/photoprism

# Copy built binaries and assets to this image
COPY --from=build /usr/local/bin/photoprism /usr/local/bin/photoprism
COPY --from=build /opt/photoprism /opt/photoprism

# Expose HTTP port
EXPOSE 2342

# Start PhotoPrism server
CMD photoprism start
```

## Kubernetes ##
- https://forge.sh/ - Define and deploy multi-container apps in Kubernetes, from source
- https://www.telepresence.io/ - a local development environment for a remote Kubernetes cluster

## External Resources ##
- https://github.com/estesp/manifest-tool
- https://github.com/docker/app
- https://github.com/moby/moby
- https://hub.docker.com/r/multiarch/qemu-user-static/ - quemu for building multiarch images with Docker
- [https://github.com/opencontainers/image-spec](https://github.com/opencontainers/image-spec/blob/master/annotations.md#pre-defined-annotation-keys) - standard labels for Docker image metadata
- https://github.com/Yelp/dumb-init - A minimal init system for Linux containers
