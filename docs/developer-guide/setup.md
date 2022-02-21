# Setting Up Your Development Environment

Before you start, make sure you have [Git](https://git-scm.com/downloads) and [Docker](https://store.docker.com/search?q=docker&type=edition&offering=community) installed on your system.
Instead of using Docker, you can create your own development environment based on our
[Dockerfile](https://github.com/photoprism/photoprism/blob/develop/docker/develop/Dockerfile) (not recommended).
You'll need [Go](https://golang.org/dl/) >= 1.17, [TensorFlow for C](https://www.tensorflow.org/install/lang_c), 
[Make](http://www.gnu.org/software/make//make.html), [NPM](https://nodejs.org/en/download/), and [MariaDB](https://mariadb.com/).
Without Docker, test results will be less reliable and you also won't be able to use our other Dockerfiles (e.g. for TensorFlow).

**Step 1:** Run [Git](https://git-scm.com/downloads) to clone (download) the source code

```
git clone git@github.com:photoprism/photoprism.git
```

!!! example ""
    If you're on windows, make sure to disable auto CR LF. Otherwise, the build won't work.
    `git config --global core.autocrlf false`
    

**Step 2:** Start the [Docker](https://www.docker.com/) services

```
cd photoprism
docker-compose up
```

*Note: This docker-compose configuration is for testing and development purposes only.*

**Step 3:** Open a terminal to run commands directly in the build and test environment

```
make terminal
```

Before you proceed, make sure that all dependencies, such as NPM packages for the frontend, are installed:

```
make all
```

Congratulations! You can now compile and run PhotoPrism in your local development environment:

```
make build
./photoprism start
```

Open the user interface by navigating to [localhost:2342](http://localhost:2342/) (HTTP) or 
[https://photoprism.localssl.dev](https://photoprism.localssl.dev/) (HTTPS). Authentication is disabled by default
in development environments. Use the `--public=false` parameter to enable it.

!!! example ""
    You can find a list of all `make` targets in the [Makefile](https://github.com/photoprism/photoprism/blob/develop/Makefile).
    For example, `make test` will run frontend and backend unit tests. Bad filesystem permissions can be fixed by
    running `make fix-permissions` in a container terminal.

**Optional:** Build the frontend in watch mode

The Go webserver will serve static assets in addition to providing the backend API. The static assets can be automatically
built whenever you change a file. In a new terminal window, outside the Docker container, run:

```
make dep-js
make watch-js
```

Questions?

* Radomir Sohlich wrote a [pragmatic introduction to Makefiles](https://sohlich.github.io/post/go_makefile/) for Go developers.
* we are using [Go Modules](https://github.com/golang/go/wiki/Modules) for managing our dependencies (new in 1.11).
* if you never used Go before and would like to learn it, you are welcome to [reach out](mailto:hello@photoprism.app). We might start organizing regular learning sessions for beginners in Berlin.
* this guide was not tested on Windows, you might need to change docker-compose.yml to make it work with Windows specific paths.

## Apple Silicon, Raspberry Pi, and ARM64 ##

Our development environment has been built into a single [multi-arch image](https://hub.docker.com/r/photoprism/development) for 64-bit AMD, Intel, and ARM processors.
That means, Apple Silicon, [Raspberry Pi](../getting-started/raspberry-pi.md) 3 / 4, and other ARM64-based devices can 
pull from the same repository.

## Multi-Arch Builds ##

This works out of the box with *Docker Desktop*. Just run `make docker-development-multiarch`. If you want to build those images for different architectures on Linux, 
you need to set up `docker buildx` builder instances or setup QEMU on your machine which shall run your builds. 
More info can be found in the docker docs: [Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/), [Leverage multi-CPU architecture support](https://docs.docker.com/desktop/multi-arch/)

### QEMU Quick Start ###

1. install qemu-user-static from docker hub: `docker run --rm --privileged multiarch/qemu-user-static --reset -p yes` [https://github.com/multiarch/qemu-user-static](https://github.com/multiarch/qemu-user-static)
2. verify that dockers buildx command is installed `docker buildx version`. if missing, follow install instructions [here](https://github.com/docker/buildx)
3. create buildx builder: `docker buildx create --name multiarch-builder && docker buildx inspect --builder multiarch-builder --bootstrap`
4. start building: `make docker-development-multiarch` or `make docker-photoprism-multiarch`

### Alternate Development Environments ###

The following are setup instructions for development and testing and should be avoided unless Docker is either not supported or not allowed in your environment:

* [Fedora 32](setup-fedora.md)
