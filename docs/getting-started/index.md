# Setup

We recommend running PhotoPrism with [Docker Compose](docker-compose.md).
All you need to have installed is a Web browser and 
[Docker](https://store.docker.com/search?type=edition&offering=community). 
It is available for Mac, Linux, and Windows.

When setup is complete, you can start [indexing your pictures](../user-guide/library/index.md).
Be patient, this may take a while depending on your server hardware and how many files you have.

Your [photos](../user-guide/organize/browse.md) and [videos](../user-guide/organize/video.md) 
will successively become visible in search results and other parts of the user interface.
The counts in the navigation are constantly updated, so you can follow the progress.

In case some of your pictures are still missing after indexing has been completed, 
they might be in [Review](../user-guide/organize/review.md) due to low quality or incomplete metadata. 
You can turn this and other features off in [Settings](../user-guide/settings/general.md), 
depending on your specific use case.

!!! tldr ""
    Our [stable version and development preview](https://docs.photoprism.app/release-notes/) have been built into a
    single [multi-arch Docker image](https://hub.docker.com/r/photoprism/photoprism) for 64-bit AMD, Intel,
    and ARM processors. That means, [Raspberry Pi](raspberry-pi.md) 3 / 4, Apple M1, and other ARM64-based
    devices can pull from the same repository, enjoy the exact same functionality, and can follow the regular
    [installation instructions](docker-compose.md) after going through a short list of [requirements](raspberry-pi.md).

!!! note ""
    Developers are invited to [contribute by building and testing standalone packages](https://docs.photoprism.app/developer-guide/)
    for Linux distributions and other operating systems. New versions are [released several times a month](../release-notes.md),
    so maintaining and testing the long list of dependencies in multiple environments would [consume much of our resources](../funding.md).
    An [unofficial port](https://docs.photoprism.app/getting-started/freebsd/) is available for FreeBSD / FreeNAS users.
    Advanced users [can build and install](faq.md#building-from-source) PhotoPrism from the [publicly available source code](https://github.com/photoprism/photoprism).

## Roadmap ##

Our vision is to provide the most user- and privacy-friendly solution to keep your pictures organized and accessible.
The [roadmap](https://github.com/photoprism/photoprism/projects/5) shows what tasks are in progress, 
what needs testing, and which features are going to be implemented next.

We have a zero bug policy and do our best to help users when they need support or have other questions.
This comes at a price, as we can't give exact deadlines for new features.

Having said that, funding really has the highest impact. So users can do their part and
[become a sponsor](../funding.md) to get their favorite features as soon as possible.

## System Requirements ##

We recommend hosting PhotoPrism on a server with **at least 2 cores**, **3 GB of physical memory**,[^1] and
a 64-bit operating system. Beyond these minimum requirements, the amount of RAM should [match the number of CPU cores](troubleshooting/performance.md#memory).

If your server has [less than 4 GB of swap space](troubleshooting/docker.md#adding-swap) or a manual
memory/swap limit is set, this can cause unexpected restarts, for example, when the indexer temporarily
needs more memory to process large files. High-resolution panoramic images may require additional swap space
and/or physical memory above the recommended minimum.

!!! note ""
    Indexing large photo and video collections significantly benefits from [local SSD storage](troubleshooting/performance.md#storage)
    and plenty of memory for caching. Especially the conversion of RAW images and the transcoding of videos are very demanding.
    We take no responsibility for instability or performance problems if your device does not meet the requirements.

#### Browsers ####

Our [Progressive Web App](../user-guide/pwa.md) (PWA) works with most modern browsers, and runs best on [Chrome](https://www.google.com/chrome/), [Chromium](https://www.chromium.org/getting-involved/download-chromium), [Safari](https://www.apple.com/safari/), [Firefox](https://www.mozilla.org/en-US/firefox/all/#product-desktop-release), and [Edge](https://www.microsoft.com/en-us/edge).
You can conveniently install it on the home screen of all major operating systems and mobile devices.

Opera and Samsung Internet have been reported to be compatible as well.
Note that not [all video formats](https://caniuse.com/?search=video%20format) can be [played with every browser](troubleshooting/browsers.md).

#### Databases ####

The backend is compatible with [SQLite 3](https://www.sqlite.org/) and [MariaDB 10.5.12+](https://mariadb.org/).
Official support for MySQL 8 is discontinued as Oracle seems to have stopped shipping [new features and improvements](https://github.com/photoprism/photoprism/issues/1764). As a result, the testing effort required before each release is no longer feasible.

#### HTTPS ####

If you install PhotoPrism on a public server outside your home network, please **always run it behind a secure HTTPS reverse proxy** such as [Traefik](proxies/traefik.md) or [Caddy](proxies/caddy-2.md).
Your files and passwords will otherwise be transmitted in clear text and can be intercepted by anyone, 
including your provider, hackers, and governments. Backup tools and file sync apps like [FolderSync](https://www.tacit.dk/foldersync/faq/#i-can-not-connect-to-a-non-https-webdav-server-why) 
may refuse to connect as well.

## Getting Support ##

Before submitting a support request, please use our [Troubleshooting Checklists](../getting-started/troubleshooting/index.md)
to determine the cause of your problem. If this doesn't help, or you have other questions:

- you are welcome to join us on [Reddit](https://www.reddit.com/r/photoprism/)
- post your question in [GitHub Discussions](https://github.com/photoprism/photoprism/discussions)
- or ask in our [Community Chat](https://gitter.im/browseyourlife/community)

In addition, [sponsors](../funding.md) receive direct [technical support](https://photoprism.app/contact) via email.

We'll do our best to answer all your questions. In return, we ask you to [back us](../funding.md) on [Patreon](https://www.patreon.com/photoprism) or [GitHub Sponsors](https://github.com/sponsors/photoprism).
Think of "free software" as in "free speech," not as in "free beer". Thank you!

!!! info ""
    We kindly ask you not to report bugs via *GitHub Issues* unless you are certain to have found a fully reproducible and previously unreported issue that must be fixed directly in the app.
    [Contact us](https://photoprism.app/contact) or [a community member](https://github.com/photoprism/photoprism/discussions)
    if you need help, it could be a local configuration problem, or a misunderstanding in how the software works.

[^1]: RAW image conversion and TensorFlow are disabled on systems with 1 GB or less memory