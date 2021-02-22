# Using Caddy 2 as Reverse Proxy

WebSocket proxying automatically works in Caddy 2. There is no need to enable this as necessary for Caddy 1, Apache,
and NGINX. In addition, Caddy 2 may [automatically create](https://caddyserver.com/docs/caddyfile/directives/tls) 
and update [Let's Encrypt](https://letsencrypt.org/) HTTPS certificates.

!!! example
    ```
    example.com {
        reverse_proxy photoprism:2342
    }
    ```

Please refer to the [official documentation](https://caddyserver.com/docs/v2-upgrade#proxy)
for further details.

!!! attention
    When installing PhotoPrism on a public server outside your home network, please **always run it
    behind a secure HTTPS reverse proxy**.
    Your files and passwords will be transmitted in clear text otherwise, and can be intercepted
    by anyone in between including your provider, hackers, and governments.
