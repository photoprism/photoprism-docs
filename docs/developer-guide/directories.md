# Project Directory Structure

The directory layout that we use for our [public project repository](https://github.com/photoprism/photoprism) is loosely based on https://github.com/golang-standards/project-layout:

- `/` contains a [Makefile](https://sohlich.github.io/post/go_makefile/), a readme, the license and various config files for dependency management, building and continuous integration
- `/assets` contains subdirectories for various assets such as photos, built JS/HTML/CSS files and server-side HTML templates
- `/cmd` contains the [application](https://github.com/photoprism/photoprism/blob/develop/cmd/photoprism/photoprism.go) source code (main package)
- `/docker` contains Dockerfiles and related assets, e.g. for Development, TensorFlow and ARM64
- `/frontend` contains our Web frontend JS/HTML/CSS source code
- `/internal` contains the source code of our internal Go packages
- `/pkg` contains the source code of our public Go packages
- `/scripts` contains shell scripts used for building, deployment and continuous integration
