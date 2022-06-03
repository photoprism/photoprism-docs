# Known Issues

This is a high-level overview of unresolved technical problems in our stable release.

Note that PhotoPrism has a zero-bug policy, which means that we do our best to fix all issues we learn about. However, sometimes this is not immediately possible, for example because they need to be fixed in third-party libraries over which we have no direct control.

!!! tldr ""
    In order to improve readability and reduce maintenance, minor issues and those we plan to fix in the short term are not listed here. You can browse all reported bugs, ideas, and planned improvements on [GitHub Issues](https://github.com/photoprism/photoprism/issues).

## Self-Hosted Setup

### Installation on a Shared Domain

Setting up PhotoPrism behind a [reverse proxy](../proxies/traefik.md) in a sub-directory on a shared domain is possible in principle. This method is experimental, however, and not generally recommended because a number of detailed issues remain to be addressed and technical expertise is required:

- [Hosting: Resolve known issues when installing in a sub-directory on a shared domain #2391](https://github.com/photoprism/photoprism/issues/2391)

## Files & Metadata

### JPEG: Bad RST Marker

This error can occur when decoding JPEG images that contain consecutive 0xFF bytes, e.g. images that have a "glich" (like a few lines of missing image information at the end) or were created with software that inserts them for padding, although this is based on an edge case of the specification and rather uncommon:

- [Bug: (invalid JPEG format: bad RST marker) #1673](https://github.com/photoprism/photoprism/issues/1673)
- [image/jpeg: "bad RST marker" error when decoding #40130](https://github.com/golang/go/issues/40130)

## Reporting Bugs ##

Before reporting a bug, please use our [Troubleshooting Checklists](index.md)
to determine the cause of your problem. If you have a general question, need help, it could be a local configuration
issue, or a misunderstanding in how the software works:

- you are welcome to ask in our [Community Chat](https://link.photoprism.app/chat)
- or post your question in [GitHub Discussions](https://link.photoprism.app/discussions)

When reporting a problem, always include the software versions you are using and [other information about your environment](https://github.com/photoprism/photoprism/blob/develop/.github/ISSUE_TEMPLATE/bug_report.md)
such as [browser, browser plugins](browsers.md), operating system, storage type,
memory size, and processor.

We kindly ask you not to report bugs via GitHub Issues **unless you are certain to have found a fully reproducible and previously unreported issue** that must be fixed directly in the app.

Note that all issue **subscribers receive an email notification** from GitHub for each new comment, so these should only be used for sharing important information and not for personal discussions/questions.
