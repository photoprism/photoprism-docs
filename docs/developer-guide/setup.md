# Setting Up Your Development Environment

### Step 1: Use [Git](https://git-scm.com/downloads) to Clone the Project from GitHub

Before running any commands, please make sure you have [Git](https://git-scm.com/downloads), [Make](https://www.gnu.org/software/make/), [Docker](https://store.docker.com/search?q=docker&type=edition&offering=community), and Docker Compose installed on your system. These are available for Mac, Linux, and Windows.[^1]

In case you are using Ubuntu Linux, you can run this script to [install the latest *Docker*](../getting-started/troubleshooting/docker.md) version including the *Compose Plugin* on your computer in one step:

```
bash <(curl -s https://setup.photoprism.app/ubuntu/install-docker.sh)
```

When working on [Microsoft Windows](faq.md#can-your-development-environment-be-used-under-windows) or [Apple macOS](https://docs.docker.com/desktop/setup/install/mac-install/), you need to install the latest version of [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) and also disable "autocrlf" in Git to avoid errors[^2]:

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
    Our standard development environment can also be used on Windows if you have [Git](https://git-scm.com/), [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/), and a suitable IDE like [GoLand](https://www.jetbrains.com/go/) installed. However, we recommend running the required `docker compose` commands manually instead of using `make docker-build` and `make terminal`. [Learn more ›](faq.md#can-your-development-environment-be-used-under-windows)

### Step 2: Launch Your Local Development Environment

Pull the latest Docker images and then launch the pre-configured build environment we provide to have an isolated development container pre-installed with all the tools you might need, including the latest versions of Go, NodeJS, and NPM:[^3]

```bash
make docker-build
docker compose up
```

*This environment is for testing and development purposes only — do not use it in production. The command examples assume [Docker Compose v2](../getting-started/troubleshooting/docker.md#docker-compose) (the `docker compose` plugin); on Red Hat-compatible distributions you can also use [`podman-compose`](../getting-started/troubleshooting/docker.md#podman-compose) as a drop-in replacement.*

If you want to change the default ports, bind services to a specific host interface, run multiple checkouts side-by-side, or enable optional services such as PostgreSQL, Ollama, or Keycloak, copy [`.env.example`](https://github.com/photoprism/photoprism/blob/develop/.env.example) to `.env` in the project root and uncomment the variables you want to override. See [Optional: Customize the Build Environment](#optional-customize-the-build-environment) below for an overview of the supported variables, optional services, and default ports.

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

- [http://localhost:2342/](http://localhost:2342/) (HTTP)
- [https://app.localssl.dev/](https://app.localssl.dev/) (HTTPS)

In the build environment, the default login is `admin` with the password `photoprism`. You can disable it with the `--public` command flag:

```bash
./photoprism --public start
```

You can find the default settings in [the `compose.yaml` file](https://github.com/photoprism/photoprism/blob/develop/compose.yaml) located in the root of the project. Keep them when [you run tests](tests.md). Otherwise, the tests may fail for others, even if they [succeed in your local environment](code-quality.md#test-automation-guidelines).

!!! example ""
    You can find a list of all `make` targets in the [Makefile](https://github.com/photoprism/photoprism/blob/develop/Makefile).
    For example, `make test` will run frontend and backend unit tests. Wrong filesystem permissions can be fixed by
    running `make fix-permissions` in a terminal.

### Optional: Build the Frontend in Watch Mode

The integrated web server provides the backend API and serves static assets. These assets can be automatically rebuilt (updated) when you change a file. Run the following command in a terminal either inside or outside the container:

```bash
make watch-js
```

### Optional: Customize the Build Environment

The development environment reads optional overrides from a `.env` file in the project root, next to `compose.yaml`. To enable, copy [`.env.example`](https://github.com/photoprism/photoprism/blob/develop/.env.example) to `.env` and uncomment the variables you want to change. This is useful when you need to free up port 80/443 on the host, restrict service ports to a specific interface, run several checkouts of the repository in parallel, or start optional services like PostgreSQL, Ollama, or Keycloak by default.

#### Supported Variables

| Variable               | Default                     | Purpose                                                                                                                                            |
|------------------------|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `COMPOSE_PROJECT_NAME` | `photoprism`                | Container, volume, and default network prefix. Set together with `COMPOSE_NETWORK_NAME` to run multiple checkouts side-by-side without collisions. |
| `COMPOSE_NETWORK_NAME` | `photoprism`                | Bridge-network name. Set together with `COMPOSE_PROJECT_NAME` to run multiple parallel environments.                                               |
| `COMPOSE_PROFILES`     | _(none)_                    | Comma-separated list of Compose profile names to start by default, e.g. `postgres,ollama` (no `--profile` flag required).                          |
| `TRAEFIK_BIND_HOST`    | `0.0.0.0`                   | Host interface Traefik binds to. Default exposes Traefik on every interface so `*.localssl.dev` is reachable from the LAN.                         |
| `SERVICES_BIND_HOST`   | `127.0.0.1`                 | Host interface direct service ports bind to. Default keeps them on loopback only.                                                                  |
| `TRAEFIK_HTTP_PORT`    | `80`                        | Traefik HTTP entrypoint port on the host.                                                                                                          |
| `TRAEFIK_HTTPS_PORT`   | `443`                       | Traefik HTTPS entrypoint port on the host.                                                                                                         |
| `PHOTOPRISM_SITE_URL`  | `https://app.localssl.dev/` | Public base URL used in share links, OIDC, and PWA URIs.                                                                                           |
| `MARIADB_PORT`         | `4001`                      | MariaDB port (exposed on the host and inside the Compose network).                                                                                 |
| `POSTGRES_PORT`        | `4002`                      | PostgreSQL port (only active with the `postgres` or `all` profile).                                                                                |

#### Services & Profiles

Some services are gated behind Compose profiles and stay stopped unless enabled. Activate them by listing one of their profile names in `COMPOSE_PROFILES` (e.g. `COMPOSE_PROFILES=postgres,vision`) or by passing `--profile <name>` to `docker compose`:

| Service             | Profiles                                | Purpose                                                 |
|---------------------|-----------------------------------------|---------------------------------------------------------|
| `postgres`          | `postgres`, `all`                       | PostgreSQL 18 database server (alternative to MariaDB). |
| `qdrant`            | `qdrant`, `all`                         | Qdrant vector database used by the Computer Vision API. |
| `ollama`            | `ollama`, `vision`, `all`               | Local large-language model runner.                      |
| `open-webui`        | `open-webui`, `ollama`, `vision`, `all` | Web interface for Ollama.                               |
| `photoprism-vision` | `vision`, `all`                         | PhotoPrism® Computer Vision API.                        |
| `keycloak`          | `keycloak`, `auth`, `all`               | Keycloak OIDC identity provider.                        |
| `prometheus`        | `prometheus`, `auth`, `all`             | Prometheus metrics server.                              |

The `photoprism`, `mariadb`, `traefik`, `dummy-webdav`, `dummy-oidc`, and `dummy-ldap` services have no profile and always start with `docker compose up`.

#### Default Host Ports

The following host ports are published by default. Traefik binds to every interface; all other ports bind to loopback only unless you override `SERVICES_BIND_HOST`:

| Port    | Service / Purpose                              | Bind                 |
|---------|------------------------------------------------|----------------------|
| `80`    | Traefik HTTP (redirects to HTTPS)              | `TRAEFIK_BIND_HOST`  |
| `443`   | Traefik HTTPS (`*.localssl.dev`)               | `TRAEFIK_BIND_HOST`  |
| `2342`  | PhotoPrism HTTP                                | `SERVICES_BIND_HOST` |
| `2443`  | PhotoPrism TLS                                 | `SERVICES_BIND_HOST` |
| `2343`  | PhotoPrism HTTP (acceptance tests)             | `SERVICES_BIND_HOST` |
| `40000` | Go debugger (Delve)                            | `SERVICES_BIND_HOST` |
| `4001`  | MariaDB (`MARIADB_PORT`)                       | `SERVICES_BIND_HOST` |
| `4002`  | PostgreSQL (`POSTGRES_PORT`, requires profile) | `SERVICES_BIND_HOST` |
| `8080`  | Open WebUI (requires profile)                  | `SERVICES_BIND_HOST` |
| `389`   | Dummy LDAP                                     | `SERVICES_BIND_HOST` |

#### Usage Examples

Bind Traefik to loopback only and move HTTP/HTTPS to non-privileged ports so the dev environment does not conflict with another web server on the host:

```dotenv
TRAEFIK_BIND_HOST=127.0.0.1
TRAEFIK_HTTP_PORT=8080
TRAEFIK_HTTPS_PORT=8443
```

Run a second checkout side-by-side without colliding on container names, volumes, the shared bridge network, or database ports:

```dotenv
COMPOSE_PROJECT_NAME=photoprism-feature
COMPOSE_NETWORK_NAME=photoprism-feature
MARIADB_PORT=4011
POSTGRES_PORT=4012
```

Always start with PostgreSQL and the Computer Vision API stack (Qdrant, Ollama, Open WebUI, and `photoprism-vision`) enabled:

```dotenv
COMPOSE_PROFILES=postgres,vision
```

After editing `.env`, recreate the affected containers so the new values take effect:

```bash
docker compose down
docker compose up
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
* this guide was not tested on Windows, you might need to edit your `compose.yaml` or `docker-compose.yml` to make it work with Windows specific paths

### ARM64-based Devices

Our development environment is published as a [multi-arch image](https://hub.docker.com/r/photoprism/develop) for 64-bit AMD, Intel, and ARM processors, so Apple Silicon, [Raspberry Pi](../getting-started/raspberry-pi.md) 4 / 5, and other ARM64-based devices can pull the same image. The companion services referenced in our [`compose.yaml`](https://github.com/photoprism/photoprism/blob/develop/compose.yaml) — [`photoprism/traefik`](https://hub.docker.com/r/photoprism/traefik), [`photoprism/vision`](https://hub.docker.com/r/photoprism/vision), [`photoprism/dummy-webdav`](https://hub.docker.com/r/photoprism/dummy-webdav), and [`photoprism/dummy-oidc`](https://hub.docker.com/r/photoprism/dummy-oidc) — are available for both architectures as well.

Note that the ARM64 development image ships [Chromium](https://www.chromium.org/) instead of Google Chrome, since Google only publishes Chrome for Linux on AMD64.

### Multi-Arch Docker Builds

For information about multi-architecture Docker builds, see the following documentation:

- [Docker Buildx](https://docs.docker.com/build/)
- [Leverage multi-CPU architecture support](https://docs.docker.com/build/building/multi-platform/)

#### QEMU Quick Start

1. install qemu-user-static from docker hub: `docker run --rm --privileged multiarch/qemu-user-static --reset -p yes` [https://github.com/multiarch/qemu-user-static](https://github.com/multiarch/qemu-user-static)
2. verify that dockers buildx command is installed `docker buildx version`. if missing, follow install instructions [here](https://github.com/docker/buildx)
3. create buildx builder: `docker buildx create --name multiarch-builder && docker buildx inspect --builder multiarch-builder --bootstrap`
4. start building: run `make docker-local-develop-<codename>` to build and push a multi-arch development image (e.g. `make docker-local-develop-resolute` for the current Ubuntu base); the underlying build script is [`scripts/docker/buildx-multi.sh`](https://github.com/photoprism/photoprism/blob/develop/scripts/docker/buildx-multi.sh)

[^1]: Instead of using Docker, you can also set up your own build environment based on the steps documented in the [Dockerfiles](https://github.com/photoprism/photoprism/tree/develop/docker/develop) we provide. For this, you should have at least Go 1.25, TensorFlow for C, Make, Node.js 22.15 (the minimum required by `frontend/scripts/precompress.js`, which uses the built-in `node:zlib` zstd API to emit `.gz`/`.zst` siblings during `make build-js`), NPM 11, and MariaDB 12 installed. Note that the test results will be unreliable without Docker. This method is therefore not well suited for contributors and we cannot provide support if something does not work as expected.
[^2]: If the Git config value "core.autocrlf" is set to "true", the following error may occur when trying to run shell scripts or Make targets: `env: bash\r: No such file or directory`
[^3]: Docker uses human-readable [Dockerfiles](https://github.com/photoprism/photoprism/tree/develop/docker) that contain all the commands a user would invoke in a terminal to assemble a complete application image.  
