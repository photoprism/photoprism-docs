# Advanced NGINX Proxy Setup

*While we believe this contributed content may be helpful to advanced users, we have not yet thoroughly reviewed it. If you have suggestions for improvement, please let us know by clicking :material-file-edit-outline: to submit a change request.*

!!! danger "Getting Support"
    Since [NGINX](../proxies/nginx.md) can be [tricky to configure](https://www.nginx.com/nginx-wiki/build/dirhtml/start/topics/tutorials/config_pitfalls/) we cannot [provide individual support](https://www.photoprism.app/kb/getting-support/) for proxy-related errors such as [failed uploads](https://github.com/photoprism/photoprism/discussions/2698#discussioncomment-9056567), [connection issues](../troubleshooting/index.md#connection-fails), [broken thumbnails](../troubleshooting/index.md#broken-thumbnails), or [video playback problems](../troubleshooting/index.md#videos-dont-play). Please reach out to the NGINX community or switch to [Traefik](../proxies/traefik.md) if you prefer an easier reverse proxy.

Running PhotoPrism behind a hardened reverse proxy adds TLS, HTTP/2, request filtering, and long-request buffering that our embedded Go HTTP server intentionally keeps minimal. If you expose PhotoPrism to the public internet, you **must** terminate HTTPS properly and keep the host patched.

Before you start, set [the public Site URL](../config-options.md#site-information) to your external `https://` address. If NGINX connects from an address outside Docker’s default internal range, add the proxy IP or CIDR to [`PHOTOPRISM_TRUSTED_PROXY`](../config-options.md#networking) so PhotoPrism accepts forwarded client and protocol headers.

The examples below use `photoprism.example.com`; replace it with your own domain or DynDNS record. Commands target Ubuntu 20.04+, but the concepts apply to other distributions.

## Prerequisites

- A domain or DynDNS record that resolves to the proxy host.
- PhotoPrism running on the local network (container, VM, or bare metal).
- Shell access with `sudo` privileges.
- Open TCP ports 80 and 443 on the proxy plus a firewall rule that only exposes those services externally.

!!! tip
    Most consumer routers include a DynDNS client. Consult your router manual or search for `your-router-model dyndns` to keep DNS records updated automatically.

## Step 1: Install NGINX and Helper Packages

Install the proxy (can be the same host that runs Docker) and a utility package for optional HTTP basic authentication:

```bash
sudo apt update && sudo apt install -y nginx apache2-utils
```

Enable and start the service if systemd did not do it automatically:

```bash
sudo systemctl enable --now nginx
```

## Step 2: Obtain TLS Certificates with Let's Encrypt

Install Certbot plus the NGINX plugin:

```bash
sudo apt install -y certbot python3-certbot-nginx
```

Request a certificate (the host must be reachable on TCP 80/443 during issuance):

```bash
sudo certbot certonly --nginx -d photoprism.example.com
```

Certificates appear under `/etc/letsencrypt/live/photoprism.example.com/`. Certbot installs a systemd timer for automatic renewal; verify it with `sudo certbot renew --dry-run` and monitor `/var/log/letsencrypt/` for errors.

## Step 3: Create the NGINX Site Configuration

Create `/etc/nginx/sites-available/photoprism.example.com` with content similar to the snippet below. Adjust the upstream address (`docker.homenet:2342` in this example) to point at your PhotoPrism container or VM.

```nginx
upstream photoprism_app {
    server docker.homenet:2342;   # PhotoPrism service or load balancer
}

server {
    listen 80;
    listen [::]:80;
    server_name photoprism.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name photoprism.example.com;

    ssl_certificate     /etc/letsencrypt/live/photoprism.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/photoprism.example.com/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5:!3DES;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    ssl_stapling on;
    ssl_stapling_verify on;

    resolver 1.1.1.1 8.8.8.8 9.9.9.9 valid=300s;
    resolver_timeout 5s;

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

        # Optional: uncomment to require basic auth (breaks WebDAV without extra config)
        # auth_basic           "Additional Authentication";
        # auth_basic_user_file /etc/nginx/.photoprism_htpasswd;
    }
}
```

!!! warning
    Always adjust `photoprism_app` to the correct backend address (Docker service, Kubernetes service, or another host). Leaving it at the example value will expose the proxy without a working backend.

`connection_upgrade` is provided by NGINX’s `map` directive in `/etc/nginx/nginx.conf` on current Ubuntu releases. If your distribution does not define it, add `map $http_upgrade $connection_upgrade { default upgrade; '' close; }` to the main configuration.

If you proxy PhotoPrism under a subdirectory, test WebDAV copy and move operations as well. Some NGINX rewrites break absolute `Destination` headers unless the external host and path are forwarded consistently.

## Step 4: Enable the Site and Reload NGINX

```bash
sudo ln -s /etc/nginx/sites-available/photoprism.example.com \
           /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Visit `https://photoprism.example.com/` to confirm the certificate, login page, and uploads work. Use `curl -I https://photoprism.example.com/` to verify the redirect and response headers.

## Step 5: Optional Hardening

- **Firewall**: Allow inbound TCP 80/443 only. Restrict PhotoPrism’s internal port (2342 by default) to the proxy host.
- **Basic Authentication**: `sudo htpasswd -c /etc/nginx/.photoprism_htpasswd user1` adds a second login layer. Keep in mind that WebDAV and API clients must support it.
- **Rate Limiting**: NGINX’s `limit_req` module can slow brute-force attempts. Combine it with PhotoPrism’s own throttling options (`PHOTOPRISM_PASSWORD_LENGTH`, `PHOTOPRISM_LOGIN_LIMIT`).
- **Monitoring**: Tail `/var/log/nginx/access.log` and `/var/log/nginx/error.log` after configuration changes. Failed uploads typically show up as `413 Request Entity Too Large`, which signals that `client_max_body_size` needs to be increased.

!!! warning
    Keep your operating system, NGINX packages, and Certbot up to date. Unpatched proxies are a common attack vector even when PhotoPrism itself is isolated behind the service.
