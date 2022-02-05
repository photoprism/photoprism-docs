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

### Why Use a Proxy? ###

If you install PhotoPrism on a public server outside your home network, **always run it behind a secure
HTTPS reverse proxy**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted 
by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to 
connect as well.
