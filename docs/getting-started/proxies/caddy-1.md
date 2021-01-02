# Using Caddy 1 as Reverse Proxy

For PhotoPrism to work properly, you need to enable websockets and transparent proxying:

!!! example
    ```
    example.com {
        proxy / photoprism:2342 {
            websocket
            transparent
        }
    }
    ```

Please refer to their [official documentation](https://caddyserver.com/v1/docs/websocket)
for further details.

!!! attention
    When installing PhotoPrism on a public server outside your home network, please **always run it
    behind a secure HTTPS reverse proxy**.
    Your files and passwords will be transmitted in clear text otherwise, and can be intercepted
    by anyone in between including your provider, hackers, and governments.
