# For the early birds

You are welcome to get an impression and provide early feedback.
We've set up a public demo at [demo.photoprism.org](https://demo.photoprism.org) for you to play with.

Note that this is work in progress. We do our best to provide a complete, stable version. 

[Financial support](../funding.md) makes a huge difference and enables us to spend more time with this project.

Leave your email to get a [release notification](https://goo.gl/forms/KBPVGl9PCsOKrAv33).

## System Requirements ##

We recommend a modern computer with **at least 2 cores** and **4 GB of memory** for running PhotoPrism. Indexing large photo and 
video collections significantly benefits from **fast, local SSD storage** and enough memory for caching. 

If you're running out of memory, it often helps to limit the [number of workers](https://docs.photoprism.org/getting-started/config-options/).
Make sure the server has [swap](https://opensource.com/article/18/9/swap-space-linux-systems) 
configured so that indexing doesn't stop when there are memory usage spikes.
As a measure of last resort, you can additionally disable image classification using TensorFlow.

!!! attention
    When installing PhotoPrism on a public server outside your home network, please **always run it
    behind a secure HTTPS reverse proxy** like [Caddy](https://caddyserver.com/), 
    [Traefik](https://containo.us/traefik/), or [Nginx](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/).
    Your files and passwords will be transmitted in clear text otherwise, and can be intercepted 
    by anyone in between including your provider, hackers, and governments.
