[Docker](https://www.docker.com/) is an Open Source container virtualization tool. It is ideal for running 
applications on any computer without extensive installation, configuration, or performance overhead.

We are aware Docker is not widely used by end users despite its many advantages. For this reason, we aim 
to provide native binaries for common operating systems at a later time.

### Why are we using Docker? ###

Containers are nothing new; [Solaris Zones](https://en.wikipedia.org/wiki/Solaris_Containers) have been around for
about 15 years, first released publicly in 2004. The chroot system call was introduced during
[development of Version 7 Unix in 1979](https://en.wikipedia.org/wiki/Chroot). It is used ever since for hosting
applications exposed to the public Internet.

Modern Linux containers are an incremental improvement. A main advantage of Docker is that application images
can be easily made available to users via the Internet. It provides a common standard across most operating
systems and devices, which saves our team a lot of time that we can then spend more effectively, for example,
providing support and developing one of the many features that users are waiting for.

Human-readable and versioned Dockerfiles as part of our public source code also help avoid surprises and
"works for me" moments by enabling us to have the exact same environment everywhere in development and production.

Last but not least, virtually all file format parsers have vulnerabilities that just haven't been discovered yet.
This is a known risk that can affect you even if your computer is not directly connected to the Internet.
Running apps in a container with limited host access is an easy way to improve security without
compromising performance and usability.

## Continuous Integration / Deployment ##

Build and push of an updated container image to [Docker Hub](https://hub.docker.com/r/photoprism/photoprism/tags/) is automatically performed by [Travis CI](https://travis-ci.org/photoprism/photoprism) whenever develop is merged into master and the tests are all green. For that reason, we don't use semantic versioning for our binaries and container images. A version string might look like `181112-edc7c2f-Darwin-i386-DEBUG` instead. Travis CI uses the [photoprism/development](https://hub.docker.com/r/photoprism/development/) image for running unit and integration tests on all branches and for pull requests, see [Dockerfile](https://github.com/photoprism/photoprism/blob/develop/Dockerfile).

## Multi-Stage Build ##

When creating new images, Docker supports so called multi-stage builds, that means you can compile an application like PhotoPrism in a container that contains all development dependencies (like source code, debugger, compiler,...) and later copy the binary to a fresh container. This way we could reduce the compressed container size from ~1 GB to less than 200 MB. Most of that is used by Darktable, TensorFlow and Ubuntu 18.04. Our `photoprism` binary is smaller than 20 MB.

Example:

```Dockerfile
FROM photoprism/development:20181112 as build

# Build PhotoPrism
WORKDIR "/go/src/github.com/photoprism/photoprism"
COPY . .
RUN make all install

# Base base image as photoprism/development
FROM ubuntu:18.04

WORKDIR /srv/photoprism

# Copy built binaries and assets to this image
COPY --from=build /usr/local/bin/photoprism /usr/local/bin/photoprism
COPY --from=build /srv/photoprism /srv/photoprism

# Expose HTTP port
EXPOSE 80

# Start PhotoPrism server
CMD photoprism start
```

## Kubernetes ##
- https://forge.sh/ - Define and deploy multi-container apps in Kubernetes, from source
- https://www.telepresence.io/ - a local development environment for a remote Kubernetes cluster

## Links ##
- https://github.com/estesp/manifest-tool
- https://github.com/docker/app
- https://github.com/moby/moby
- https://hub.docker.com/r/multiarch/qemu-user-static/ - quemu for building multiarch images with Docker
- [https://github.com/opencontainers/image-spec](https://github.com/opencontainers/image-spec/blob/master/annotations.md#pre-defined-annotation-keys) - standard labels for Docker image metadata
- https://github.com/Yelp/dumb-init - A minimal init system for Linux containers
