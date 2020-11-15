# Development Environment

Before you start, make sure you have [Git](https://git-scm.com/downloads) and [Docker](https://store.docker.com/search?q=docker&type=edition&offering=community) installed on your system.
Instead of using Docker, you can create your own development environment
based on our [Dockerfile](https://github.com/photoprism/photoprism/blob/develop/docker/development/Dockerfile) (not recommended). You'll need [Go](https://golang.org/dl/) >= 1.11, [TensorFlow for C](https://www.tensorflow.org/install/lang_c), [Make](http://www.gnu.org/software/make//make.html), [NPM](https://nodejs.org/en/download/) and [MySQL](https://dev.mysql.com/downloads/mysql/). Without Docker, test results will be less reliable and you also won't be able to use our other Dockerfiles (e.g. for TensorFlow).

**Step 1:** Run [Git](https://git-scm.com/downloads) to clone this project:

```
git clone git@github.com:photoprism/photoprism.git
```

!!! tip
    If you're on windows, make sure to disable auto CR LF. Otherwise, the build won't work.
    `git config --global core.autocrlf false`
    

**Step 2:** Start [Docker](https://www.docker.com/) containers:

```
cd photoprism
docker-compose up
```

*Note: This docker-compose configuration is for testing and development purposes only.*

**Step 3:** Open a terminal to the photoprism container:

```
docker-compose exec photoprism bash
```

Now - inside this terminal - you can run tests and commands:

```
make all
make test
./photoprism start
```

You can see a list of all `make` targets in our [Makefile](https://github.com/photoprism/photoprism/blob/develop/Makefile). For example, `make install` will build a `photoprism` production binary without debug information and install it in the user's directory including all assets.

`./photoprism start` starts the built-in Web server. It will listen on [localhost:2342](http://localhost:2342/) by default, see [docker-compose.yml](https://github.com/photoprism/photoprism/blob/develop/docker-compose.yml).

Questions?

* Radomir Sohlich wrote a [pragmatic introduction to Makefiles](https://sohlich.github.io/post/go_makefile/) for Go developers.
* We are using [Go Modules](https://github.com/golang/go/wiki/Modules) for managing our dependencies (new in 1.11).
* If you never used Go before and would like to learn it, you are welcome to [reach out](mailto:hello@photoprism.pro). We might start organizing regular learning sessions for beginners in Berlin.
* This guide was not tested on Windows, you might need to change docker-compose.yml to make it work with Windows specific paths.

# Alternate Development Environment's

The following are setup instructions for development and testing and should be avoided unless docker is either not supported or not allowed in your environment:

* [Fedora 32](setup-fedora.md)
