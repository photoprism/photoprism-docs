# Known Issues

This is a high-level overview of the currently unresolved issues. PhotoPrism generally follows a zero-bug policy, which means that we do our best to fix any issues we learn about. However, sometimes this is not immediately possible, for example due to dependencies on third-party libraries, other apps, or because it is a specific use case that we do not support at this time.

!!! tldr ""
    In order to improve readability and reduce maintenance, minor issues and those we plan to fix in the short term are not listed here. You can browse all reported bugs, ideas, and planned improvements on [GitHub Issues](https://github.com/photoprism/photoprism/issues).

## Self-Hosted Setup

### Shared Domain

Installation in a sub-directory on a shared domain is generally possible if you run your instance behind a [reverse proxy](getting-started/proxies/traefik.md). At the moment, this method is experimental. We do not recommend it because technical expertise is required and a number of specific issues still need to be addressed:

- [Hosting: Resolve known issues when installing in a sub-directory on a shared domain #2391](https://github.com/photoprism/photoprism/issues/2391)

## User Authentication

### Session Invalidation

User authentication sessions expire automatically after 7 days. In some cases, you may want to ensure that all sessions expire immediately to require re-login, for example, after a password change if the previously used password is known to people who should no longer be able to access your instance:

- [Security: Changing password doesn't invalidate existing auth tokens #1935](https://github.com/photoprism/photoprism/issues/1935)

This is a known limitation with the current implementation. One of the reasons for this trade-off is that the account may be used by background processes that are synchronizing files. Invalidating the session immediately could then lead to data loss, which we consider unacceptable. At the very least, immediate invalidation would require more complex client logic and additional documentation to help developers implement it correctly.

While our team is working on a new implementation as part of full multi-user support, you can manually delete `storage/config/sessions.json` and then restart your instance to revoke all sessions and require re-login.

## File Format Support

### JPEG: Bad RST Marker

This error can occur when decoding JPEG images that contain consecutive 0xFF bytes, e.g. images that have a "glich" (like a few lines of missing image information at the end) or were created with software that inserts them for padding, although this is based on an edge case of the specification and rather uncommon:

- [Bug: (invalid JPEG format: bad RST marker) #1673](https://github.com/photoprism/photoprism/issues/1673)
- [image/jpeg: "bad RST marker" error when decoding #40130](https://github.com/golang/go/issues/40130)

## Conversion

### PHOTOPRISM_JPEG_SIZE / jpeg-size

PhotoPrism supports limiting the size of generated JPEG images when converting from RAW files using the environment variable `PHOTOPRISM_JPEG_SIZE` or the CLI option `jpeg-size`. However this currently does not work if Rawtherapee is used as converter, as it does not support any CLI options to limit the JPEG size (unlike Darktable). It would be bad for indexing performance if PhotoPrism would downsample the generated file after Rawtherapee finishes converting, therefore this option is ignored when a RAW file is converted with Rawtherapee. Depending on your settings such as `PHOTOPRISM_DARKTABLE_BLACKLIST` (default: .raf and .cr3 files) or `PHOTOPRISM_DISABLE_DARKTABLE` (default: false) you may or may not run into this issue. If you really need to limit the generated JPEG size the only available workaround for now is to not use Rawtherappee as converter.

- [RAW: PHOTOPRISM_JPEG_SIZE is ignored when converting RAW with RawTherapee](https://github.com/photoprism/photoprism/issues/2446)

## Reporting Bugs ##

Before reporting a bug, please use our [Troubleshooting Checklists](getting-started/troubleshooting/index.md)
to determine the cause of your problem. If you have a general question, need help, it could be a local configuration
issue, or a misunderstanding in how the software works:

- you are welcome to ask in our [Community Chat](https://link.photoprism.app/chat)
- or post your question in [GitHub Discussions](https://link.photoprism.app/discussions)

When reporting a problem, always include the software versions you are using and [other information about your environment](https://github.com/photoprism/photoprism/blob/develop/.github/ISSUE_TEMPLATE/bug_report.md)
such as [browser, browser plugins](getting-started/troubleshooting/browsers.md), operating system, storage type,
memory size, and processor.

We kindly ask you not to report bugs via GitHub Issues **unless you are certain to have found a fully reproducible and previously unreported issue** that must be fixed directly in the app.

Note that all issue **subscribers receive an email notification** from GitHub for each new comment, so these should only be used for sharing important information and not for personal discussions or questions.
