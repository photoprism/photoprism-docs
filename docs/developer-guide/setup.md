# Setting Up Your Development Environment

### Step 1: Use [Git](https://git-scm.com/downloads) to Clone the Project from GitHub

Before running any commands, please make sure you have [Git](https://git-scm.com/downloads), [Make](https://www.gnu.org/software/make/), [Docker](https://store.docker.com/search?q=docker&type=edition&offering=community), and Docker Compose installed on your system. These are available for Mac, Linux, and Windows.[^1]

If you are working with Windows, you must also disable "autocrlf" in Git to avoid errors:

```bash
git config --global core.autocrlf false
```

Now change to the directory where you usually keep your development projects, and run this command to download the project from GitHub:

```bash
git clone git@github.com:photoprism/photoprism.git
```

Once all code has been downloaded, change to the project directory which should now exist:

```bash
cd photoprism
```

### Step 2: Launch Your Local Development Environment

Pull the latest Docker images and then launch the pre-configured build environment we provide to have an isolated development container pre-installed with all the tools you might need, including the latest versions of Go, NodeJS, and NPM:[^2]

```bash
make docker-build
docker compose up
```

If your version of Docker doesn't support `docker compose`, use `docker-compose` instead and call `DOCKER_COMPOSE='docker-compose'` before calling `make`.

*This environment is for testing and development purposes only. Do not use it in production. Also note that our guides now use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose`.*

### Step 3: Install the Dependencies and Start Developing

Open a terminal to run commands directly in your local development environment:

```bash
make terminal
```

Before starting to build, make sure all dependencies, such as NPM packages and TensorFlow models, are installed:

```bash
make dep
```

**Congratulations!** You can now build the frontend assets (JS), compile the backend binary (Go) and then run a custom PhotoPrism version in your local environment:

```bash
make build-js
make build-go
./photoprism start
```

After PhotoPrism has been started as shown above, the user interface can be opened in a web browser by navigating to one of these URLs:

- [http://localhost:2342/](http://photoprism.me:2342/) (HTTP)
- [https://localssl.dev/](https://localssl.dev/) (HTTPS)

In the build environment, the default login is `admin` with the password `photoprism`. You can disable it with the `--public` command flag:

```bash
./photoprism --public start
```

You can find the default settings in [the docker-compose.yml file](https://github.com/photoprism/photoprism/blob/develop/docker-compose.yml) located in the root of the project. Keep them when [you run tests](tests.md). Otherwise, the tests may fail for others, even if they [succeed in your local environment](code-quality.md#test-automation-guidelines).

!!! example ""
    You can find a list of all `make` targets in the [Makefile](https://github.com/photoprism/photoprism/blob/develop/Makefile).
    For example, `make test` will run frontend and backend unit tests. Wrong filesystem permissions can be fixed by
    running `make fix-permissions` in a terminal.

### Optional: Build the Frontend in Watch Mode

The integrated web server not only provides the backend API, but is also used to serve static assets. These can be
automatically rebuilt (updated) when you change a file. To do this, run the following command in a terminal, either
inside or outside the container (outside is faster if your host is not running Linux):

```bash
make watch-js
```

Alternatively, you can change to the `frontend` directory and run NPM directly:

```bash
cd frontend
npm run watch
```

To update the frontend dependencies, also change to the `frontend` directory and run:

```bash
npm update
```

**Questions?**

* Radomir Sohlich wrote a [pragmatic introduction to Makefiles](https://sohlich.github.io/post/go_makefile/) for Go developers
* we are using [Go Modules](https://github.com/golang/go/wiki/Modules) for managing our dependencies (new in 1.11)
* this guide was not tested on Windows, you might need to change docker-compose.yml to make it work with Windows specific paths

### Apple Silicon, Raspberry Pi, and ARM64

Our development environment has been built into a single [multi-arch image](https://hub.docker.com/r/photoprism/development)
for 64-bit AMD, Intel, and ARM processors. That means, Apple Silicon, [Raspberry Pi](../getting-started/raspberry-pi.md)
3 / 4, and other ARM64-based devices can pull from the same repository.

### Multi-Arch Docker Builds

For information about multi-architecture Docker builds, see the following documentation:

- [Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/)
- [Leverage multi-CPU architecture support](https://docs.docker.com/desktop/multi-arch/)

#### QEMU Quick Start

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

[^1]: Instead of using Docker, you can also set up your own build environment, for example, based on the steps documented in the [Dockerfiles](https://github.com/photoprism/photoprism/tree/develop/docker) we provide. You need at least Go 1.19, TensorFlow for C, Make, NPM 8 and MariaDB 10.9. Note that test results are unreliable without Docker. As a result, this method is not suitable for contributors and we cannot provide support if something does not work as expected.
[^2]: Docker uses human-readable [Dockerfiles](https://github.com/photoprism/photoprism/tree/develop/docker) that contain all the commands a user would invoke in a terminal to assemble a complete application image.  
