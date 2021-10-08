# Setup

To simplify running PhotoPrism on a server, we strongly recommend using [Docker Compose](docker-compose.md).
It is available for Mac, Linux and Windows.

Next, you'll have to [index](../user-guide/library/index.md) 
your library. Please be patient, this will take a while depending on the size of your photo collection.

Already indexed photos can be browsed in [Photos](../user-guide/organize/browse.md) 
while videos show up in [Videos](../user-guide/organize/video.md).
Counts are getting continuously updated in the navigation.

If files are missing, they might be in [Review](../user-guide/organize/review.md) due to low quality
or incomplete metadata. You can turn this and other features off in [Settings](../user-guide/settings/general.md), 
depending on your specific use case.

!!! important "New Release"
    Our [latest release](../release-notes.md) comes as a single [multi-arch image](https://hub.docker.com/r/photoprism/photoprism)
    for AMD64, ARM64, and ARMv7. That means you don't need to pull from different Docker repositories anymore.
    We recommend updating your existing `docker-compose.yml` config based on [our examples](https://dl.photoprism.org/docker/).

## Roadmap ##

Our vision is to provide the most user-friendly solution for browsing, organizing, and sharing your photo collection.
The [roadmap](https://github.com/photoprism/photoprism/projects/5) shows what tasks are in progress, 
what needs testing, and which feature requests are going to be implemented next.

Please give ideas you like a thumbs-up, so that we know what is most popular.
Ideas backed by one or more eligible [sponsors](../funding.md) 
will be prioritized as well.

## System Requirements ##

We recommend hosting PhotoPrism on a server with **at least 2 cores** and **4 GB of memory**.
Also make sure it has at least 4 GB of swap configured, so that indexing doesn't cause 
restarts when there are memory usage spikes.
Beyond these minimum requirements, the amount of RAM should match the number of cores.

!!! note ""
    Indexing large photo and video collections significantly benefits from fast, local SSD storage,
    and plenty of memory for caching. Especially the conversion of RAW images and the transcoding of
    videos are very demanding.

!!! info ""
    RAW file conversion and TensorFlow will be disabled on servers 
    with less than 2 GB of physical memory.
    If you're running out of memory - or other system resources - while indexing, please reduce the
    [number of workers](https://docs.photoprism.org/getting-started/config-options/)
    to a value less than the number of logical CPU cores.
    As a measure of last resort, you may disable using TensorFlow for image classification and facial recognition.

Our Web UI works with most modern browsers, and runs best on Chrome, Chromium, Safari, Firefox, and Edge.
Opera and Samsung Internet have been reported to be compatible as well.
Note that not all [video formats](https://github.com/photoprism/photoprism/issues/707) may be played with every browser.

The backend is compatible with [MariaDB 10.5.10+](https://mariadb.org/) (earlier versions
see [MDEV-25362](https://jira.mariadb.org/browse/MDEV-25362)), [MySQL 8](https://www.mysql.com/),
and [SQLite 3](https://www.sqlite.org/)

!!! danger ""
    When installing PhotoPrism on a public server outside your home network, please **always run it
    behind a secure HTTPS reverse proxy** like [Traefik](proxies/traefik.md), 
    [Caddy](proxies/caddy-2.md), or [NGINX](proxies/nginx.md).
    Your files and passwords will be transmitted in clear text otherwise, and can be intercepted 
    by anyone in between including your provider, hackers, and governments. Backup tools and file sync apps
    like [FolderSync](https://www.tacit.dk/foldersync/faq/#i-can-not-connect-to-a-non-https-webdav-server-why) 
    may refuse to connect as well.
