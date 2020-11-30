# Getting Started

To simplify running PhotoPrism on a server, we strongly recommend using [Docker Compose](docker-compose.md).
It is available for Mac, Linux and Windows.

Next, you'll have to [index](../user-guide/library/import-vs-index.md) 
your library. Please be patient, this will take a while depending on the size of your photo collection.

Already indexed photos can be browsed in [Photos](../user-guide/organize/browse.md) 
while videos show up in [Videos](../user-guide/organize/video.md).
Counts are getting continuously updated in the navigation.

If files are missing, they might be in [Review](../user-guide/organize/review.md) due to low quality
or incomplete metadata. You can turn this and other features off in [Settings](../user-guide/settings/ui.md), 
depending on your specific use case.

!!! info
    We do our best to provide a complete, stable version very soon. Check the 
    [roadmap](https://github.com/photoprism/photoprism/projects/5) for open issues.
    Leave your email to get a [release notification](https://goo.gl/forms/KBPVGl9PCsOKrAv33).

## Roadmap ##

Our vision is to provide the most user-friendly solution for browsing, organizing and sharing your personal photo collection.
The [roadmap](https://github.com/photoprism/photoprism/projects/5) shows what tasks are in progress, 
what needs testing, and which feature requests are going to be implemented next.

Please give ideas you like a thumbs-up, so that we know what is most popular.
Ideas backed by one or more eligible [sponsors](../funding.md) 
will be prioritized as well.

## System Requirements ##

We recommend a modern computer with **at least 2 cores** and **4 GB of memory** for running PhotoPrism. Indexing large photo and 
video collections significantly benefits from **fast, local SSD storage** and enough memory for caching. 

If you're running out of memory or system load is too high, limit the 
[number of workers](https://docs.photoprism.org/getting-started/config-options/),
and make sure the server has [swap](https://opensource.com/article/18/9/swap-space-linux-systems) 
configured, so that indexing doesn't stop when there are memory usage spikes.
As a measure of last resort, you may additionally disable image classification using TensorFlow.

PhotoPrism is compatible with [SQLite 3](https://www.sqlite.org/), [MariaDB 10](https://mariadb.org/), 
and [MySQL 8](https://www.mysql.com/).

!!! attention
    When installing PhotoPrism on a public server outside your home network, please **always run it
    behind a secure HTTPS reverse proxy** like [Caddy](https://caddyserver.com/), 
    [Traefik](https://containo.us/traefik/), or [Nginx](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/).
    Your files and passwords will be transmitted in clear text otherwise, and can be intercepted 
    by anyone in between including your provider, hackers, and governments.
