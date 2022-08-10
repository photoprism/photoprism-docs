# Using Apache 2.4 as Reverse Proxy

!!! tldr ""
    Should you experience problems with Apache, we recommend that you ask the Apache community for advice, as we cannot provide support for third-party software and services.

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

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-pencil: to send a pull request with your changes.
