# Getting Started

To simplify running PhotoPrism on a server, we strongly recommend using [Docker Compose](docker-compose.md).
It is available for Mac, Linux and Windows.

Next, you'll have to [index](../user-guide/library/import-vs-index.md) 
your library. Please be patient, this will take a while depending on the size of your photo collection.

Already indexed photos can be browsed in [Photos](../user-guide/organize/browse.md) 
while videos show up in [Videos](../user-guide/organize/video.md).
Counts are continuously updated in the navigation.

If files are missing, they might be in [Review](../user-guide/organize/review.md) due to low quality or missing metadata.
You can turn this and other features off in [Settings](../user-guide/settings/ui.md), depending on
your specific use case.

### Roadmap ###

Our [roadmap](https://github.com/photoprism/photoprism/projects/5) shows what tasks are in progress, 
what needs testing, and which feature requests are going to be implemented next.

Please give ideas you like a thumbs-up 👍  , so that we know what is most popular.
Ideas supported by one or more [sponsors](https://docs.photoprism.org/funding/) will be prioritized as well.

## System Requirements ##

We recommend a modern computer with **at least 2 cores** and **4 GB of memory** for running PhotoPrism. Indexing large photo and 
video collections significantly benefits from **fast, local SSD storage** and enough memory for caching. 

If you're running out of memory, limit the [number of workers](https://docs.photoprism.org/getting-started/config-options/)
and make sure the server has [swap](https://opensource.com/article/18/9/swap-space-linux-systems) 
configured, so that indexing doesn't stop when there are memory usage spikes.
As a measure of last resort, you may additionally disable image classification using TensorFlow.

!!! attention
    When installing PhotoPrism on a public server outside your home network, please **always run it
    behind a secure HTTPS reverse proxy** like [Caddy](https://caddyserver.com/), 
    [Traefik](https://containo.us/traefik/), or [Nginx](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/).
    Your files and passwords will be transmitted in clear text otherwise, and can be intercepted 
    by anyone in between including your provider, hackers, and governments.
