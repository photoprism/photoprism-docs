# Known Issues

This is a high-level overview of the currently unresolved issues. PhotoPrism follows a zero-bug policy, which means that we do our best to fix any issues we learn about. However, sometimes this is not immediately possible, for example due to dependencies on third-party libraries, other apps, or because it is a specific use case that we do not support at this time.

!!! tldr ""
    In order to improve readability and reduce maintenance, minor issues and those we plan to fix in the short term are not listed here. You can browse all reported bugs, ideas, and planned enhancements on [GitHub Issues](https://github.com/photoprism/photoprism/issues).

## Self-Hosted Setup

### Shared Domain

Installation in a sub-directory on a shared domain is generally possible if you run your instance behind a [reverse proxy](getting-started/proxies/traefik.md). At the moment, this method is experimental. We do not recommend it because technical expertise is required and a number of specific issues still need to be addressed:

- [Hosting: Resolve known issues when installing in a sub-directory on a shared domain #2391](https://github.com/photoprism/photoprism/issues/2391)

### Nested Storage Folder

It is not supported to configure the *storage* folder to be inside the *originals* folder unless the name starts with a `.` to indicate that it is hidden. Otherwise, this will result in increasingly longer indexing times and high disk usage, since such nesting causes a loop by re-indexing previously created thumbnails and sidecar files:

- [Config: Prevent nesting of "storage" folder inside "originals" unless hidden #1642](https://github.com/photoprism/photoprism/issues/1642)

In practice, this is not a problem as long as you [follow our documentation](getting-started/docker-compose.md#photoprismstorage) and [examples](https://dl.photoprism.app/docker/). We intend to automatically detect, report, and prevent such issues in the future. Due to the flexible mapping of folders within a Docker container to host directories, this has not yet been implemented.

### Symbolic Links

Symbolic [links to files and directories](https://github.com/photoprism/photoprism/issues/1049) within the *originals* folder are supported if they are accessible from the environment in which your instance is running. However, you cannot mount a symbolic link as a *storage* folder or use links within the *storage* folder.

## Face Recognition

### Asian Faces and Children

It is a known issue that children and Asian-looking faces cannot be recognized reliably. Detection without automatic recognition should not be affected by that.

This is because the model we use was trained with North American images, which unfortunately do not include many Asians. The absence of children in the training data comes from the fact that parents do not usually share such images under a public license (and may not have the right to do so).

*We will continue to improve our models over time as our resources allow.*

### Background Worker

[Face recognition](user-guide/organize/people.md) was developed and tested under the assumption that the [background worker](getting-started/config-options.md#index-workers) runs every 15 minutes, unless the backend is busy with other tasks like indexing. It has not been tested with much longer intervals and is not designed for that.

PhotoPrism's background worker groups new faces by similarity, compares faces with clusters, and optimizes existing clusters as needed. Without these routine tasks, the number of faces to be processed becomes too large. The first and next time the worker runs, it can then cause a heavy server load until all the faces, face clusters, and related pictures have been updated. The longer you wait, the more CPU is required and the longer it takes.

An important reason for the worker to run independently of actual changes in the main instance is that some users change the database content directly or run additional instances, for example for indexing. It is a problem that can be solved, but it takes time. If we were to ignore this and don't run the worker at all times, it could lead to many additional support requests, further reducing the amount of time we can spend on development. 

*The handling of changes in multiple instances will be improved over time so that the worker can be run less frequently in future releases.*

### Removing Merged Clusters Fails

Under certain conditions, inconsistent face assignments cannot be automatically resolved by the background worker, which can result in an unusually high CPU load when it is running:

- if you use multiple tabs when assigning faces and don't wait until saving changes is complete, you will likely experience this problem, especially if you enter inconsistent names for the same face in each tab
- another possible cause is running multiple instances (for example, parallel indexing workers started by a scheduler in the background) or modifying database content directly, as this may also lead to inconsistent faces, markers, and subjects
- see [Faces: Error "Failed removing merged clusters for subject" seems to cause tagging of faces to become slow #2806](https://github.com/photoprism/photoprism/issues/2806)

Running the following command [in a terminal](getting-started/docker-compose.md#command-line-interface) can resolve problems with inconsistent data:

```
docker compose exec photoprism photoprism faces audit --fix
```

It can also be helpful to manually check for inconsistent assignments and fix them in the user interface.

*Advanced users affected by this are welcome to [privately provide us](https://photoprism.app/contact) with a SQL dump of their subjects, faces, and markers database tables for debugging. Thank you very much!*

## User Authentication

Session and user management have been re-implemented in the latest [stable release](release-notes.md). If you are upgrading from a preview build, you will need to run the `photoprism users reset --yes` command [in a terminal](getting-started/docker-compose.md#command-line-interface) after the upgrade to recreate the new database tables so that they are compatible with the stable version. This will not affect your pictures or albums.

Upgrading from the last stable version should work without any problems. However, if you have already created additional accounts with the previously offered unofficial multi-user support, you will notice that only the main admin account is migrated automatically. Run `photoprism users legacy` [in a terminal](getting-started/docker-compose.md#command-line-interface) to display the legacy accounts so you can migrate them manually if needed.

Please note that the current release does not yet include support for user roles other than *Admin*, as we need to specify, create and test each new role before we can release it. Once this is done, we will also provide additional user management documentation.

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

## Reporting Bugs ##

Before reporting a bug, please use our [Troubleshooting Checklists](getting-started/troubleshooting/index.md)
to determine the cause of your problem. If you have a general question, need help, it could be a local configuration
issue, or a misunderstanding in how the software works:

- you are welcome to ask in our [Community Chat](https://link.photoprism.app/chat)
- or post your question in [GitHub Discussions](https://link.photoprism.app/discussions)

When reporting a problem, always include the software versions you are using and [other information about your environment](https://photoprism.app/kb/reporting-bugs)
such as [browser, browser plugins](getting-started/troubleshooting/browsers.md), operating system, storage type,
memory size, and processor.

We kindly ask you not to report bugs via GitHub Issues **unless you are certain to have found a fully reproducible and previously unreported issue** that must be fixed directly in the app.

Note that all issue **subscribers receive an email notification** from GitHub for each new comment, so these should only be used for sharing important information and not for personal discussions or questions.
