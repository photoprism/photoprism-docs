# Known Issues

PhotoPrism generally follows a zero-bug policy, which means that we do our best to provide a fix for every technical problem we learn about.
However, sometimes this is not possible right away, for example because it needs to be fixed in a third-party library that our software depends on, or because it is a specific use case that we do not support at this time.

!!! example "GitHub Issues"
    In order to improve readability and reduce maintenance effort, minor issues and [recently reported bugs](https://github.com/photoprism/photoprism/issues?q=is%3Aissue+is%3Aopen+label%3Abug) that we plan to fix in the short term are not listed here, but [only in GitHub Issues](https://github.com/photoprism/photoprism/issues). When [browsing issues](developer-guide/issues.md), please note that **our team and all issue subscribers receive an email notification** whenever a new comment is added, so these should only be used for sharing important information and not for [discussions, questions](https://github.com/photoprism/photoprism/discussions), or [expressing personal opinions](https://www.photoprism.app/code-of-conduct/). Thank you very much!

## Self-Hosted Setup

### Nested Import Folder

You must not configure the *import* folder to be inside the *originals* folder, as this will cause a loop by importing already indexed files.

Inexperienced users are advised to closely follow our documentation and to use the config examples we provide, as this issue can only occur with a custom setup.

### Nested Storage Folder

We recommend not to configure the *storage* folder to be inside the *originals* folder unless the name starts with a `.` to indicate that it is hidden.

In older releases prior to [240420-ef5f14bc4](https://docs.photoprism.app/release-notes/#april-20-2024), this could [lead to an indexing loop](https://github.com/photoprism/photoprism/issues/1642) by indexing thumbnails of already indexed files.

### Symbolic Links

Symbolic [links to files and directories](https://github.com/photoprism/photoprism/issues/1049) within the *originals* folder are supported if they are accessible from the environment in which your instance is running. However, you cannot mount a symbolic link as a *storage* folder or use links within the *storage* folder.

## Authentication

### Upgrading From Previous Releases

Should you experience problems after upgrading from a [previous release](release-notes.md) or [development preview](getting-started/updates.md#development-preview), we recommend running the `photoprism auth reset --yes` command [in a terminal](getting-started/docker-compose.md#command-line-interface) to [reset the `auth_sessions` table](user-guide/users/cli.md#session-management) to a clean state and force a re-login of all users. Note that this will also delete all client access tokens and any [app passwords](user-guide/users/2fa.md#step-3-app-passwords) that users may have created.

### Legacy User Accounts

The session and user management was [reimplemented in November 2022](release-notes.md#november-2-2022). If you created additional accounts with the unofficial multi-user support offered before that, only the main admin account is migrated automatically. Run `photoprism users legacy` [in a terminal](getting-started/docker-compose.md#command-line-interface) to display the legacy accounts so you can migrate them manually if needed.

### OpenID Connect (OIDC)

Changing the [authentication of an existing user account](getting-started/advanced/openid-connect.md#existing-accounts) to *OIDC* does not remove a previously set password, so that it can still be used to log in (optionally also in combination with [2FA](user-guide/users/2fa.md)).

If a [local password](user-guide/users/cli.md#changing-a-password) has been set for an account, you can remove it by running the `photoprism passwd --rm [username]` command [in a terminal](user-guide/users/cli.md#removing-a-password). Alternatively, [super admins](user-guide/users/roles.md) can set the account password to a long random value through the [UI](user-guide/users/index.md#changing-passwords) or [CLI](user-guide/users/cli.md#changing-a-password) to effectively prevent local authentication.

Please also note that you cannot [change the authentication provider](user-guide/users/cli.md#command-options) of your own account [through the Admin UI](user-guide/users/index.md#editing-user-details), so you don't accidentally lock yourself out e.g. by setting it to "none".

## Face Recognition

### Legacy Hardware ###

Face recognition can be slow (or even crash) on [old devices](getting-started/troubleshooting/performance.md#legacy-hardware) due to insufficient resources.

*Like most applications, PhotoPrism has [certain requirements](getting-started/index.md#system-requirements) and our development process does not include testing on unsupported or unusual hardware.*

### Children and Pictures Taken Years Apart

Automatic recognition is less reliable for young children, and for pictures of the same person taken many years apart, than it is for adults photographed within a few years of each other. This is a property of the [embedding model](user-guide/ai/face-recognition.md#face-embeddings) and not of detection, so the faces are still found, displayed, and searchable — they are just less likely to be grouped into one person automatically, and more likely to form several clusters that you can merge by hand.

The model used for new libraries is a substantial improvement over the one PhotoPrism shipped previously, which was in addition unreliable for Asian faces because it had been trained largely on North American images. That particular weakness has been resolved. Children remain [an open issue](https://github.com/photoprism/photoprism/issues/1587).

*Libraries created before the new model became available keep the previous one until they are migrated, so they are still affected by both limitations — see [Face Model After an Upgrade](#face-model-after-an-upgrade) below.*

### Rotated Faces

Face detection expects upright faces. The detection rate drops as a face is rotated in the image plane, and a face rotated by roughly 90° — someone lying down, or a picture taken with the camera held sideways and no matching orientation tag — is generally not detected at all.

Because no face is reported in the first place, this cannot be compensated for by lowering `FACE_SIZE` or `FACE_SCORE`. Rotating the affected pictures so that they are displayed upright and then [re-indexing them](user-guide/library/originals.md) is the practical workaround.

### Face Model After an Upgrade

Libraries created before the current [embedding model](user-guide/ai/face-recognition.md#face-embeddings) became available continue to use the previous one after an upgrade, because vectors generated by different models cannot be compared, and switching automatically would make every face you have already assigned to a person incomparable with newly indexed ones. Setting `PHOTOPRISM_FACE_MODEL` does not change this either.

Run [`photoprism faces migrate`](user-guide/ai/face-recognition.md#upgrading-an-existing-library) [in a terminal](getting-started/docker-compose.md#command-line-interface) to re-embed an existing library with the current model and benefit from the improved recognition quality. Your people and their names are preserved. You do not need to stop your instance beforehand, though you should start the migration when no indexing or import is under way, and do restart the instance once it has finished so that the new model is loaded. Expect it to take a while on a large library.

A few related notes for upgrades:

- Run `photoprism faces status` to see which model is in use, and whether anything is currently preventing faces from being clustered.
- Run `photoprism faces update --force` after a migration, or whenever faces have been detected but no cluster has formed for them. It runs a clustering and matching pass regardless of how many faces are new, and matches every face against the existing clusters again. Faces that already belong to a cluster keep it, and faces below `FACE_CLUSTER_SIZE` are not clustered either way.
- `FACE_CLUSTER_SIZE`, the minimum size a face must have to help form a new person, has been raised and is now measured on the picture the face was sampled from rather than on the detection thumbnail. A library with many small faces therefore forms fewer people than before. The faces themselves are still detected, displayed, and searchable, and you can assign them by hand.
- The development-only options `--face-skip-children` and `--face-allow-background` have been removed. The matching environment variables are ignored, but an instance that still passes either as a **command-line flag** in its `compose.yaml` will not start, because unknown flags are rejected.

### Background Worker

[Face recognition](user-guide/organize/people.md) was developed and tested under the assumption that the [background worker](getting-started/config-options.md#indexing) runs every 15 minutes, unless the backend is busy with other tasks like indexing. It has not been tested with much longer intervals and is not designed for that.

PhotoPrism's background worker groups new faces by similarity, compares faces with clusters, and optimizes existing clusters as needed. Without these routine tasks, the number of faces to be processed becomes too large. The first and next time the worker runs, it can then cause a heavy server load until all the faces, face clusters, and related pictures have been updated. The longer you wait, the more CPU is required and the longer it takes.

An important reason for the worker to run independently of actual changes in the main instance is that some users change the database content directly or run additional instances, for example for indexing. It is a problem that can be solved, but it takes time. If we were to ignore this and don't run the worker at all times, it could lead to many additional support requests, further reducing the amount of time we can spend on development.

*The handling of changes in multiple instances will be improved over time so that the worker can be run less frequently in future releases.*

### Photos With All Faces Assigned Appear Under “New Faces”

This can happen when multiple image files are [grouped into a stack](user-guide/organize/stacks.md), for example, because they were taken at the same place and time, and stacking is enabled.

Secondary images are not searched for faces by default. So the problem is limited to specific cases where you have manually changed the primary image or the images are stacked after detection, which may indicate more fundamental problems, e.g. with the [metadata, filenames, or settings](user-guide/organize/stacks.md#for-what-reasons-can-files-be-stacked).

One possible solution is to change the primary image of a stack to assign faces to the other images in the stack. You can also manually unstack these files and disable stacking in [Settings > Content](user-guide/settings/library.md). Note that files that are already stacked are not automatically unstacked when you change the stacking settings, and that [Live Photos](user-guide/organize/video.md#live-photos) do not appear in [Stacks](user-guide/organize/stacks.md) because they are a special type of media that is always "stacked".

### Inconsistent Face Assignments

Under certain conditions, inconsistent face assignments cannot be automatically resolved by the background worker, which can result in an unusually high CPU load when it is running:

- if you use multiple browser tabs or windows for assigning faces and don't wait until saving the changes is complete, the likelihood of this problem increases, especially if you accidentally enter different names for the same face
- another possible cause is running multiple instances (for example, parallel indexing workers started by a scheduler in the background) or modifying database content directly, as this may also lead to inconsistent faces, markers and subjects

Running the following command [in a terminal](getting-started/docker-compose.md#command-line-interface) can resolve problems with inconsistent data:

```
docker compose exec photoprism photoprism faces audit --fix
```

It can also be helpful to manually check for inconsistent assignments and fix them in the user interface.
Alternatively, you can use the `photoprism faces reset` command for a clean start if you haven't invested much time in assigning faces yet.

*Advanced users affected by this are welcome to [privately provide us](https://www.photoprism.app/contact/) with a SQL dump of their subjects, faces, and markers database tables for debugging. Thank you very much!*

## File Compatibility

### JPEG: Bad RST Marker

Decoding can fail with `invalid JPEG format: bad RST marker` for images that contain consecutive 0xFF bytes, for example files with a "glitch" such as a few lines of missing image information at the end, or files created by software that inserts these bytes for padding. This is based on an edge case of the specification and rather uncommon.

PhotoPrism [detects affected files and re-encodes them automatically](https://github.com/photoprism/photoprism/issues/2463) with ImageMagick when generating thumbnails, so they are indexed and displayed normally. Your original files are not modified. If ImageMagick has been disabled with `PHOTOPRISM_DISABLE_IMAGEMAGICK`, the repair cannot be performed and the error resurfaces.

## Web Browsers

### Maps Require WebGL 2

Rendering the map in [Places](user-guide/organize/places.md) and in the location picker requires a browser with **WebGL 2** support. Where it is unavailable, the rest of PhotoPrism works normally and only the map is replaced with a message telling you to try another browser or device.

Practically all [supported browsers](getting-started/troubleshooting/browsers.md) provide WebGL 2. The most common reasons for it to be missing are hardware acceleration having been disabled in the browser settings, an outdated graphics driver, or a privacy extension that blocks the WebGL API.

## RAW Converters

### JPEG Size Limit

RawTherapee and the libheif decoder (`heif-dec`, called `heif-convert` in earlier libheif versions) cannot limit the resolution of JPEG files when converting files from other formats such as RAW, DNG, HEIC or AVIF. In general, when converting images, the resolution of the generated JPEG files can be limited with the environment variable `PHOTOPRISM_JPEG_SIZE` or the CLI parameter `--jpeg-size`.

However, this does not work with certain converters because, unlike Darktable, they do not support CLI options to limit JPEG size:

- [RAW: PHOTOPRISM_JPEG_SIZE is ignored when converting RAW with RawTherapee #2446](https://github.com/photoprism/photoprism/issues/2446)

It would probably also hurt indexing performance and image quality if PhotoPrism reduced the size of the generated file after conversion, for example, by using a temporary file.

As a result, this option is ignored when generating JPEG files with these converters. Whether RawTherapee or the libheif decoder are used depends on additional settings such as `PHOTOPRISM_DARKTABLE_BLACKLIST`, `PHOTOPRISM_DISABLE_DARKTABLE`, `PHOTOPRISM_RAWTHERAPEE_BLACKLIST`, and `PHOTOPRISM_DISABLE_RAWTHERAPEE`.

## Docker Compose ##

### Dollar Signs ###

If a configuration value [in a `compose.yaml` or `docker-compose.yml` file](getting-started/docker-compose.md) contains a literal `$` character, for example in a password, you must use `$$` (a double dollar sign) to escape it so that e.g. `"compo$e"` becomes `"compo$$e"`:

```yaml
services:
  mariadb:
    environment:
      # sets password to "compo$e"
      MARIADB_PASSWORD: "compo$$e"
```

Values that contain a `$` are otherwise [interpreted as a variable](https://docs.docker.com/reference/compose-file/interpolation/). In this case, both the `$VARIABLE` and the `${VARIABLE}` syntax are supported. Further details on the use of variables can be found in the [file format reference](https://docs.docker.com/reference/compose-file/interpolation/).

### True / False ###

Boolean variable values like "true", "false", "yes", "no", "on", or "off" must be enclosed in double or single quotes so that they are passed as intended:

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_DEFAULT_TLS: "true"
      PHOTOPRISM_READONLY: "false"
```

If you otherwise specify `true` as a value without quotes, [Docker Compose](https://docs.docker.com/compose/) will pass the host variable of the same name to the container instead of setting the value to "true" (results in an empty string if no environment variable with the same name is set on the host):

```yaml
services:
  photoprism:
    environment:
      # evaluated as "" (false)
      PHOTOPRISM_READONLY: true
```

## Reporting Bugs ##

Before [reporting a bug](https://www.photoprism.app/kb/reporting-bugs/), first use our [Troubleshooting Checklists](getting-started/troubleshooting/index.md) to determine the cause of your problem. If you have a general question, need help, it could be a configuration issue, or a misunderstanding in how the software works:

- you are welcome to ask in our [Community Chat](https://link.photoprism.app/chat)
- or post your question in [GitHub Discussions](https://link.photoprism.app/discussions)

In order for us to investigate [new bug reports](https://www.photoprism.app/kb/reporting-bugs/), they must include **a complete list of steps to reproduce the problem**, the software versions used and information about the environment in which the problem occurred, such as [browser type, browser version, browser plug-ins](https://docs.photoprism.app/getting-started/troubleshooting/browsers/), operating system, [storage type](https://docs.photoprism.app/getting-started/troubleshooting/performance/#storage), [processor type](https://docs.photoprism.app/getting-started/troubleshooting/performance/#server-cpu), and [memory size](https://docs.photoprism.app/getting-started/troubleshooting/performance/#memory).

A template for creating bug reports can be found at [photoprism.app/kb/reporting-bugs](https://www.photoprism.app/kb/reporting-bugs/). We kindly ask you not to report bugs via [GitHub Issues](developer-guide/issues.md) **unless you are certain to have found a fully reproducible and previously unreported issue** that must be fixed directly in the app.

!!! info ""
    When [browsing issues](https://github.com/photoprism/photoprism/issues), please note that **our team and all issue subscribers receive an email notification** from GitHub whenever a new comment is added, so these should only be used for sharing important information and not for [discussions, questions](https://github.com/photoprism/photoprism/discussions), or [expressing personal opinions](https://www.photoprism.app/code-of-conduct/). Thank you very much!
