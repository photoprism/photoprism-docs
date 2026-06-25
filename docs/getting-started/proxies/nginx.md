# Using NGINX as Reverse Proxy

!!! danger "Getting Support"
    Since [NGINX](https://www.nginx.com/) is [easy to misconfigure](https://www.nginx.com/nginx-wiki/build/dirhtml/start/topics/tutorials/config_pitfalls/), we cannot [provide individual support](https://www.photoprism.app/kb/getting-support/) for proxy-related issues such as [failed uploads](https://github.com/photoprism/photoprism/discussions/2698#discussioncomment-9056567), [connection errors](../troubleshooting/index.md#connection-fails), [broken thumbnails](../troubleshooting/index.md#broken-thumbnails), or [video playback problems](../troubleshooting/index.md#videos-dont-play). Please ask the NGINX community for help or consider [Traefik](traefik.md) when you prefer a simpler proxy.

NGINX sits in front of PhotoPrism to terminate TLS, enforce HTTP/2, and shield uploads and downloads with additional rate limiting or request filtering. Keep PhotoPrism’s internal TLS disabled (`PHOTOPRISM_DISABLE_TLS="true"`) so NGINX can manage certificates, and ensure the proxy host has enough free disk space for TLS assets and logs.

Also set [the public Site URL](../config-options.md#site-information) to your external `https://` address. If NGINX reaches PhotoPrism from an address outside Docker’s default internal range, add the proxy IP or CIDR to [`PHOTOPRISM_TRUSTED_PROXY`](../config-options.md#networking) so forwarded client and protocol headers are accepted.

## Requirements

- Install `nginx` plus `certbot` (or reuse an existing ACME client) on the proxy host.
- Expose only ports 80/443 to the internet; keep PhotoPrism’s internal port (2342 by default) private.
- Enable the `map` directive for `$connection_upgrade` (Ubuntu ships it in `/etc/nginx/nginx.conf`). Add `map $http_upgrade $connection_upgrade { default upgrade; '' close; }` if your distro does not.

## Example Server Blocks

The snippet below redirects HTTP→HTTPS, terminates TLS via Let’s Encrypt, and forwards requests to a Docker service named `photoprism`.

```nginx
upstream photoprism_app {
    server photoprism:2342;
}

server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    client_max_body_size 512M;        # Allow large uploads
    proxy_buffering off;              # Stream uploads directly
    proxy_read_timeout 600s;
    proxy_send_timeout 600s;

    location / {
        proxy_pass http://photoprism_app;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }
}
```

Adapt `server_name`, certificate paths, and the upstream address to match your environment. After editing, run `sudo nginx -t` followed by `sudo systemctl reload nginx` to apply the changes.

More examples are available in the [NGINX documentation](https://nginx.org/en/docs/). Also see our [advanced guide](../advanced/nginx-proxy-setup.md) when you need extra hardening tips, WebDAV notes, and operator checklists.

[View "Pitfalls and Common Mistakes" ›](https://www.nginx.com/nginx-wiki/build/dirhtml/start/topics/tutorials/config_pitfalls/)

### Why Use a Proxy? ###

If you install PhotoPrism on a public server outside your home network, **always run it behind a secure
HTTPS reverse proxy**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted
by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to
connect as well.

![](https://dl.photoprism.app/img/diagrams/reverse-proxy.svg){ class="w100" }

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
