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

Please refer to the [official documentation](https://caddyserver.com/v1/docs/websocket)
for further details.

### Why Use a Proxy? ###

If you install PhotoPrism on a public server outside your home network, **always run it behind a secure
HTTPS reverse proxy**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted
by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to
connect as well.