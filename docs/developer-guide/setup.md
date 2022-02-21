# Setting Up Your Development Environment

Before you proceed, make sure you have [Git](https://git-scm.com/downloads) and [Docker](https://store.docker.com/search?q=docker&type=edition&offering=community)
installed on your system. It is available for Mac, Linux, and Windows.

Instead of using Docker, you can create your own development environment based on our [Dockerfiles](https://github.com/photoprism/photoprism/tree/develop/docker)
(not recommended). These are text documents that contain all commands a user could call in a terminal to assemble
an application image. At a minimum, you need Go >= 1.17, TensorFlow for C, Make, NPM, and MariaDB.
Note that test results are unreliable without Docker, so this method is not suitable for contributors.

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

The user interface can be opened in a browser by navigating to... 

- [http://localhost:2342/](http://localhost:2342/) (HTTP)
- or [https://photoprism.localssl.dev/](https://photoprism.localssl.dev/) (HTTPS)
 
Authentication is disabled by default in development environments. Use the `--public=false` parameter to enable it.

Default settings can be found in the `docker-compose.yml` file in the root directory of the project. Keep them unchanged
[when running tests](tests.md), otherwise the tests may fail for others, even if they [pass in your local environment](code-quality.md#code-that-cannot-be-tested-is-flawed).

!!! example ""
    You can find a list of all `make` targets in the [Makefile](https://github.com/photoprism/photoprism/blob/develop/Makefile).
    For example, `make test` will run frontend and backend unit tests. Bad filesystem permissions can be fixed by
    running `make fix-permissions` in a container terminal.

**Optional:** Build the frontend in watch mode

The integrated web server not only provides the backend API, but is also used to serve static assets. These can be
automatically rebuilt (updated) when you change a file. To do this, run the following command in a terminal, either
inside or outside the container (outside is faster if your host is not running Linux):

```
make watch-js
```

Alternatively, you can change to the `frontend` directory and run NPM directly:

```
cd fronend
npm run watch
```

To update the frontend dependencies, also change to the `frontend` directory and run:

```
npm update
```

**Questions?**

* Radomir Sohlich wrote a [pragmatic introduction to Makefiles](https://sohlich.github.io/post/go_makefile/) for Go developers
* we are using [Go Modules](https://github.com/golang/go/wiki/Modules) for managing our dependencies (new in 1.11)
* this guide was not tested on Windows, you might need to change docker-compose.yml to make it work with Windows specific paths

## Apple Silicon, Raspberry Pi, and ARM64 ##

Our development environment has been built into a single [multi-arch image](https://hub.docker.com/r/photoprism/development)
for 64-bit AMD, Intel, and ARM processors. That means, Apple Silicon, [Raspberry Pi](../getting-started/raspberry-pi.md)
3 / 4, and other ARM64-based devices can pull from the same repository.

## Multi-Arch Docker Builds ##

For information about multi-architecture Docker builds, see the following documentation:

- [Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/)
- [Leverage multi-CPU architecture support](https://docs.docker.com/desktop/multi-arch/)

### QEMU Quick Start ###

1. install qemu-user-static from docker hub: `docker run --rm --privileged multiarch/qemu-user-static --reset -p yes` [https://github.com/multiarch/qemu-user-static](https://github.com/multiarch/qemu-user-static)
2. verify that dockers buildx command is installed `docker buildx version`. if missing, follow install instructions [here](https://github.com/docker/buildx)
3. create buildx builder: `docker buildx create --name multiarch-builder && docker buildx inspect --builder multiarch-builder --bootstrap`
4. start building: `make docker-development-multiarch` or `make docker-photoprism-multiarch`

<!--
### Alternate Development Environments ###

The following are setup instructions for development and testing and should be avoided unless Docker is either
not supported or not allowed in your environment:

* [Fedora 32](setup-fedora.md)
-->