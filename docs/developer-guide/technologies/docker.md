[Docker](https://www.docker.com/products/docker-desktop) is an open-source container virtualization application mainly written in Go (like PhotoPrism). It is ideal for running applications on any computer without extensive installation, configuration or performance overhead. All you need to do is download an image and start it. However, Docker is not commonly used by end users and more popular among developers / admins. For that reason, PhotoPrism must also be usable without running in a container, at least on Linux and OS X.

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
