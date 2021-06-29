# Using Apache 2.4 as Reverse Proxy

!!! example
    ```
    ProxyPass /api/v1/ws ws://photoprism.lxd:2342/api/v1/ws
    ProxyPassReverse /api/v1/ws ws://photoprism.lxd:2342/api/v1/ws
    ProxyPass / http://photoprism:2342/
    ProxyPassReverse / http://photoprism:2342/
    ProxyRequests off
    ```

The [official documentation](https://httpd.apache.org/docs/2.4/mod/mod_proxy_wstunnel.html) explains in detail, how to configure Apache Web Server 2.4 to reverse proxy WebSockets.

!!! attention
    When installing PhotoPrism on a public server outside your home network, please **always run it
    behind a secure HTTPS reverse proxy**.
    Your files and passwords will be transmitted in clear text otherwise, and can be intercepted
    by anyone in between including your provider, hackers, and governments.
