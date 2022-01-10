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

!!! note ""
    Our [stable version](https://docs.photoprism.app/release-notes/) and development preview have been built into a 
    single [multi-arch image](https://hub.docker.com/r/photoprism/photoprism) for 64-bit AMD, Intel,
    and ARM processors. That means, [Raspberry Pi](raspberry-pi.md) 3 / 4, Apple M1, and other ARM64-based 
    devices can pull from the same repository, enjoy the exact same functionality, and can follow the regular 
    [installation instructions](docker-compose.md) after going through a short list of [requirements](raspberry-pi.md).

!!! tldr ""
    Downloadable installation packages are planned for a later release. Developers can build PhotoPrism from source
    by following the instructions in our [Developer Guide](../developer-guide/setup.md).

## Roadmap ##

Our vision is to provide the most user- and privacy-friendly solution to keep your pictures organized and accessible.
The [roadmap](https://github.com/photoprism/photoprism/projects/5) shows what tasks are in progress, 
what needs testing, and which features are going to be implemented next.

We have a zero bug policy and do our best to help users when they need support or have other questions.
This comes at a price, as we can't give exact deadlines for new features.

Having said that, funding really has the highest impact. So users can do their part and
[become a sponsor](../funding.md) to get their favorite features as soon as possible.

## System Requirements ##

We recommend hosting PhotoPrism on a server with **at least 2 cores** and **4 GB of memory**.
Also make sure it has at least 4 GB of swap configured, so that indexing doesn't cause 
restarts when there are memory usage spikes.
Beyond these minimum requirements, the amount of RAM should match the number of cores.

!!! note ""
    Indexing large photo and video collections significantly benefits from [local SSD storage](troubleshooting/performance.md#storage),
    and plenty of memory for caching. Especially the conversion of RAW images and the transcoding of
    videos are very demanding.

!!! info ""
    RAW file conversion and TensorFlow will be disabled on servers 
    with less than 2 GB of physical memory.
    If you're running out of memory - or other system resources - while indexing, try reducing the
    [number of workers](https://docs.photoprism.app/getting-started/config-options/)
    to a reasonably small value in `docker-compose.yml` (depending on the performance of the server).
    As a measure of last resort, you may disable using TensorFlow for image classification and facial recognition.

#### Browsers ####

Our Web UI works with most modern browsers, and runs best on Chrome, Chromium, Safari, Firefox, and Edge.
Opera and Samsung Internet have been reported to be compatible as well.
Note that not all [video formats](https://github.com/photoprism/photoprism/issues/707) may be played with 
every browser.

#### Databases ####

The backend is compatible with [SQLite 3](https://www.sqlite.org/) and [MariaDB 10.5.12+](https://mariadb.org/).
Older databases using the same dialect, such as MySQL 8, may work but are not officially supported.

#### HTTPS ####

If you install PhotoPrism on a public server outside your home network, please always run it behind 
a secure HTTPS reverse proxy such as [Traefik](proxies/traefik.md), [Caddy](proxies/caddy-2.md),
or [NGINX](proxies/nginx.md). Your files and passwords will otherwise be transmitted in clear text 
and can be intercepted by anyone, including your provider, hackers, and governments.
Backup tools and file sync apps like [FolderSync](https://www.tacit.dk/foldersync/faq/#i-can-not-connect-to-a-non-https-webdav-server-why) 
may refuse to connect as well.

## Getting Support ##

Before reporting a bug, please use our [Troubleshooting Checklists](../getting-started/troubleshooting/index.md)
to determine the cause of your problem. If this doesn't help, or you have other questions:

- you are welcome to ask in our [Community Chat](https://gitter.im/browseyourlife/community)
- and post your question in [GitHub Discussions](https://github.com/photoprism/photoprism/discussions)

In addition, [sponsors](../funding.md) receive direct [technical support](https://photoprism.app/contact) via email.

We'll do our best to answer all your questions. In return, we ask you to [back us](../funding.md) on [Patreon](https://www.patreon.com/photoprism) or [GitHub Sponsors](https://github.com/sponsors/photoprism).
Think of "free software" as in "free speech," not as in "free beer". Thank you! 💜

!!! tldr ""
    When reporting a problem, always include the software versions you are using and [other information about your environment](https://github.com/photoprism/photoprism/blob/develop/.github/ISSUE_TEMPLATE/bug_report.md) such as [browser](troubleshooting/browsers.md), browser plugins, operating system, storage type, memory size, and processor.

*[Web UI]: A Progressive Web App that can be installed on your home screen and provides a native app-like experience
