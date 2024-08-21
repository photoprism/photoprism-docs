# Setting Up Your Development Environment

### Step 1: Use [Git](https://git-scm.com/downloads) to Clone the Project from GitHub

Before running any commands, please make sure you have [Git](https://git-scm.com/downloads), [Make](https://www.gnu.org/software/make/), [Docker](https://store.docker.com/search?q=docker&type=edition&offering=community), and Docker Compose installed on your system. These are available for Mac, Linux, and Windows.[^1]

In case you are using Ubuntu Linux, you can run this script to [install the latest *Docker*](../getting-started/troubleshooting/docker.md) version including the *Compose Plugin* on your computer in one step:

```
bash <(curl -s https://setup.photoprism.app/ubuntu/install-docker.sh)
```

When working on [Microsoft Windows](faq.md#can-your-development-environment-be-used-under-windows) or [Apple macOS](https://docs.docker.com/desktop/install/mac-install/), you need to install the latest version of [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) and also disable "autocrlf" in Git to avoid errors[^2]:

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

!!! example "Developing on Windows"
    Our standard development environment can also be used on Windows if you have [Git](https://git-scm.com/), [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/), and a suitable IDE like [GoLand](https://www.jetbrains.com/go/) installed. However, we recommend running the required `docker compose` commands manually instead of using `make docker-build` and `make terminal`. [Learn more ›](faq.md#can-your-development-environment-be-used-under-windows)

### Step 2: Launch Your Local Development Environment

Pull the latest Docker images and then launch the pre-configured build environment we provide to have an isolated development container pre-installed with all the tools you might need, including the latest versions of Go, NodeJS, and NPM:[^3]

```bash
make docker-build
docker compose up
```

*This environment is for testing and development purposes only. Do not use it in production. Also note that our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible distributions.*

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

### Optional: Use a Go Debugger

To debug the backend Go code, first make sure you have built and run the containers as described above:

```bash
make docker-build
docker compose up
```

_Note:_ If you make changes in the `Dockerfile` to test things out, you can build and run the `photoprism` container individually:

```bash
docker compose build photoprism
docker compose up photoprism
```

Then open a terminal to the container as described above:

```bash
make terminal
```

and if you made code changes, make sure the rebuild the Go code:

```bash
make build-go
```

You can then run the [Delve](https://github.com/go-delve/delve/blob/master/Documentation/usage/dlv.md) command from inside the container to start the debugger - the command-line options can be customized based on your needs:

```bash
dlv --listen=:40000 --headless=true --log=true --log-output=debugger,debuglineerr,gdbwire,lldbout,rpc --accept-multiclient --api-version=2 exec ./photoprism -- start
```

Once you run this command, you can use VSCode or Goland to add breakpoints and step through breakpoints in the code. Follow the instructions [here](https://golangforall.com/en/post/go-docker-delve-remote-debug.html#visual-studio-code) to set up VSCode, and [here](https://golangforall.com/en/post/go-docker-delve-remote-debug.html#goland-ide) to set up Goland to connect to the debugger.

Once the debugger is running, you can view the app at `http://localhost:2342/` and debug the code.

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

[^1]: Instead of using Docker, you can also set up your own build environment based on the steps documented in the [Dockerfiles](https://github.com/photoprism/photoprism/tree/develop/docker/develop) we provide. For this, you should have at least Go 1.21, TensorFlow for C, Make, NPM 10 and MariaDB 11 installed. Note that the test results will be unreliable without Docker. This method is therefore not well suited for contributors and we cannot provide support if something does not work as expected.
[^2]: If the Git config value "core.autocrlf" is set to "true", the following error may occur when trying to run shell scripts or Make targets: `env: bash\r: No such file or directory`
[^3]: Docker uses human-readable [Dockerfiles](https://github.com/photoprism/photoprism/tree/develop/docker) that contain all the commands a user would invoke in a terminal to assemble a complete application image.  
