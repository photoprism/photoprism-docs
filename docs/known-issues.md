# Known Issues

This is a high-level overview of the currently unresolved issues. PhotoPrism follows a zero-bug policy, which means that we do our best to fix any issues we learn about. However, sometimes this is not immediately possible, for example due to dependencies on third-party libraries, other apps, or because it is a specific use case that we do not support at this time.

!!! tldr ""
    In order to improve readability and reduce maintenance, minor issues and those we plan to fix in the short term are not listed here. You can browse all reported bugs, ideas, and planned enhancements on [GitHub Issues](https://github.com/photoprism/photoprism/issues).

## Self-Hosted Setup

### Shared Domain

Installation in a sub-directory on a shared domain is generally possible if you run your instance behind a [reverse proxy](getting-started/proxies/traefik.md). At the moment, this method is experimental. We do not recommend it because technical expertise is required and a number of specific issues still need to be addressed:

- [Hosting: Resolve known issues when installing in a sub-directory on a shared domain #2391](https://github.com/photoprism/photoprism/issues/2391)

### Nested Import Folder

You may not configure the *import* folder to be inside the *originals* folder, as this will cause a loop by importing already indexed files.

!!! tldr ""
    Inexperienced users are advised to closely follow our documentation and to use the config examples we provide, as this issue can only occur with a custom configuration.

### Nested Storage Folder

We recommend not to configure the *storage* folder to be inside the *originals* folder unless the name starts with a `.` to indicate that it is hidden.

In older releases prior to [240420-ef5f14bc4](https://docs.photoprism.app/release-notes/#april-20-2024), this could [lead to an indexing loop](https://github.com/photoprism/photoprism/issues/1642) in which thumbnails of already indexed files were indexed as if they were originals.

### Symbolic Links

Symbolic [links to files and directories](https://github.com/photoprism/photoprism/issues/1049) within the *originals* folder are supported if they are accessible from the environment in which your instance is running. However, you cannot mount a symbolic link as a *storage* folder or use links within the *storage* folder.

## User Authentication

Session and user management [had been reimplemented](release-notes.md#november-2-2022) in November 2022. If you are upgrading from a Development Preview with a build number between [221102-905925b4d](release-notes.md#november-2-2022) and [220901-f493607b0](https://docs.photoprism.app/release-notes/#september-1-2022), you will need to run the `photoprism users reset --yes` command [in a terminal](getting-started/docker-compose.md#command-line-interface) after the upgrade to recreate the new database tables so that they are compatible with the stable version. This will not affect your pictures or albums.

Upgrading from the last stable version should work without any problems. However, if you have already created additional accounts with the previously offered unofficial multi-user support, you will notice that only the main admin account is migrated automatically. Run `photoprism users legacy` [in a terminal](getting-started/docker-compose.md#command-line-interface) to display the legacy accounts so you can migrate them manually if needed.

!!! tldr ""
    Should you still experience problems after upgrading from a [previous release](release-notes.md) or [development preview](getting-started/updates.md#development-preview), we recommend running the `photoprism auth reset --yes` command [in a terminal](getting-started/docker-compose.md#command-line-interface) to [reset the sessions](user-guide/users/cli.md#session-management) table to a clean state and force a re-login of all users.

## Face Recognition

### Legacy Hardware ###

Face recognition can be slow (or even crash) on [old devices](getting-started/troubleshooting/performance.md#legacy-hardware) due to insufficient resources.

*Like most applications, PhotoPrism has [certain requirements](getting-started/index.md#system-requirements) and our development process does not include testing on unsupported or unusual hardware.*

### Asian Faces and Children

It is a known issue that children and Asian-looking faces cannot be recognized reliably. Detection without automatic recognition should not be affected by that.

This is because the model we use was trained with North American images, which unfortunately do not include many Asians. The absence of children in the training data comes from the fact that parents do not usually share such images under a public license (and may not have the right to do so).

*We will continue to improve our models over time as our resources allow.*

### Background Worker

[Face recognition](user-guide/organize/people.md) was developed and tested under the assumption that the [background worker](getting-started/config-options.md#index-workers) runs every 15 minutes, unless the backend is busy with other tasks like indexing. It has not been tested with much longer intervals and is not designed for that.

PhotoPrism's background worker groups new faces by similarity, compares faces with clusters, and optimizes existing clusters as needed. Without these routine tasks, the number of faces to be processed becomes too large. The first and next time the worker runs, it can then cause a heavy server load until all the faces, face clusters, and related pictures have been updated. The longer you wait, the more CPU is required and the longer it takes.

An important reason for the worker to run independently of actual changes in the main instance is that some users change the database content directly or run additional instances, for example for indexing. It is a problem that can be solved, but it takes time. If we were to ignore this and don't run the worker at all times, it could lead to many additional support requests, further reducing the amount of time we can spend on development. 

*The handling of changes in multiple instances will be improved over time so that the worker can be run less frequently in future releases.*

### Photos With All Faces Assigned Appear Under “New Faces”

This can happen when multiple image files are [grouped into a stack](user-guide/organize/stacks.md), for example, because they were taken at the same place and time, and stacking is enabled.

Secondary images are not searched for faces by default. So the problem is limited to specific cases where you have manually changed the primary image or the images are stacked after detection, which may indicate more fundamental problems, e.g. with the [metadata, filenames, or settings](user-guide/organize/stacks.md#for-what-reasons-can-files-be-stacked).

One possible solution is to change the primary image of a stack to assign faces to the other images in the stack. You can also manually unstack these files and disable stacking in [Settings > Library](user-guide/settings/library.md). Note that files that are already stacked are not automatically unstacked when you change the stacking settings, and that [Live Photos](user-guide/organize/video.md#live-photos) do not appear in [Stacks](user-guide/organize/stacks.md) because they are a special type of media that is always "stacked".

### Removing Merged Clusters Fails

Under certain conditions, inconsistent face assignments cannot be automatically resolved by the background worker, which can result in an unusually high CPU load when it is running:

- if you use multiple browser tabs or windows for assigning faces and don't wait until saving the changes is complete, the likelihood of this problem increases, especially if you accidentally enter different names for the same face
- another possible cause is running multiple instances (for example, parallel indexing workers started by a scheduler in the background) or modifying database content directly, as this may also lead to inconsistent faces, markers and subjects
- see [Faces: Error "Failed removing merged clusters for subject" seems to cause tagging of faces to become slow #2806](https://github.com/photoprism/photoprism/issues/2806)

Running the following command [in a terminal](getting-started/docker-compose.md#command-line-interface) can resolve problems with inconsistent data:

```
docker compose exec photoprism photoprism faces audit --fix
```

It can also be helpful to manually check for inconsistent assignments and fix them in the user interface.
Alternatively, you can use the `photoprism faces reset` command for a clean start if you haven't invested much time in assigning faces yet.

*Advanced users affected by this are welcome to [privately provide us](https://www.photoprism.app/contact) with a SQL dump of their subjects, faces, and markers database tables for debugging. Thank you very much!*

## File Compatibility

### JPEG: Bad RST Marker

This error can occur when decoding JPEG images that contain consecutive 0xFF bytes, e.g. images that have a "glich" (like a few lines of missing image information at the end) or were created with software that inserts them for padding, although this is based on an edge case of the specification and rather uncommon:

- [Bug: (invalid JPEG format: bad RST marker) #1673](https://github.com/photoprism/photoprism/issues/1673)
- [image/jpeg: "bad RST marker" error when decoding #40130](https://github.com/golang/go/issues/40130)
- [JPEG: Automatically check and repair broken/invalid images #2463](https://github.com/photoprism/photoprism/issues/2463)

## RAW Converters

### JPEG Size Limit

RawTherapee and "heif-convert" cannot limit the resolution of JPEG files when converting files from other formats such as RAW, DNG, HEIC or AVIF. In general, when converting images, the resolution of the generated JPEG files can be limited with the environment variable `PHOTOPRISM_JPEG_SIZE` or the CLI parameter `--jpeg-size`.

However, this does not work with certain converters because, unlike Darktable, they do not support CLI options to limit JPEG size:

- [RAW: PHOTOPRISM_JPEG_SIZE is ignored when converting RAW with RawTherapee #2446](https://github.com/photoprism/photoprism/issues/2446)

It would probably also hurt indexing performance and image quality if PhotoPrism reduced the size of the generated file after conversion, for example, by using a temporary file.

As a result, this option is ignored when generating JPEG files with these converters. Whether RawTherapee or "heif-convert" are used depends on additional settings such as `PHOTOPRISM_DARKTABLE_BLACKLIST`, `PHOTOPRISM_DISABLE_DARKTABLE`, `PHOTOPRISM_RAWTHERAPEE_BLACKLIST`, and `PHOTOPRISM_DISABLE_RAWTHERAPEE`.

## Docker Compose ##

### Dollar Signs ###

If a configuration value [in a `docker-compose.yml` file](getting-started/docker-compose.md) contains a literal `$` character, for example in a password, you must use `$$` (a double dollar sign) to escape it so that e.g. `"compo$e"` becomes `"compo$$e"`:

```yaml
services:
  mariadb:
    environment:
      # sets password to "compo$e"
      MARIADB_PASSWORD: "compo$$e"
```

Values that contain a `$` are otherwise [interpreted as a variable](https://docs.docker.com/compose/compose-file/12-interpolation/#interpolation). In this case, both the `$VARIABLE` and the `${VARIABLE}` syntax are supported. Further details on the use of variables can be found in the [file format reference](https://docs.docker.com/compose/compose-file/12-interpolation/#interpolation).

### True / False ###

Boolean variable values like "true", "false", "yes", "no", "on", or "off" must be enclosed in double or single quotes so that they are passed as intended:

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_DEFAULT_TLS: "true"
      PHOTOPRISM_READONLY: "false"
```

If you otherwise specify `true` as a value without quotes, [Docker Compose](https://docs.docker.com/compose/compose-file/compose-file-v3/) will pass the host variable of the same name to the container instead of setting the value to "true" (results in an empty string if no environment variable with the same name is set on the host):

```yaml
services:
  photoprism:
    environment:
      # evaluated as "" (false)
      PHOTOPRISM_READONLY: true
```

## Reporting Bugs ##

Before reporting a bug, please use our [Troubleshooting Checklists](getting-started/troubleshooting/index.md)
to determine the cause of your problem. If you have a general question, need help, it could be a local configuration
issue, or a misunderstanding in how the software works:

- you are welcome to ask in our [Community Chat](https://link.photoprism.app/chat)
- or post your question in [GitHub Discussions](https://link.photoprism.app/discussions)

When reporting a problem, always include the software versions you are using and [other information about your environment](https://www.photoprism.app/kb/reporting-bugs)
such as [browser, browser plugins](getting-started/troubleshooting/browsers.md), operating system, storage type,
memory size, and processor.

We kindly ask you not to report bugs via GitHub Issues **unless you are certain to have found a fully reproducible and previously unreported issue** that must be fixed directly in the app.

Note that all issue **subscribers receive an email notification** from GitHub whenever a new comment is added, so these should only be used for sharing important information and not for discussions, questions or expressing personal opinions.
