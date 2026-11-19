# Using SWAG as Reverse Proxy

!!! tldr ""
    SWAG bundles NGINX, Certbot, and fail2ban in one container. If you encounter SWAG-specific issues, please contact the [LinuxServer.io community](https://docs.linuxserver.io/general/faq/#support) for assistance.

[SWAG](https://github.com/linuxserver/docker-swag) (Secure Web Application Gateway) automates TLS certificates and delivers a hardened NGINX reverse proxy on Docker. Keep PhotoPrism’s internal TLS off (`PHOTOPRISM_DISABLE_TLS="true"`) so SWAG can terminate HTTPS.

Set [the public Site URL](../config-options.md#site-information) to your external `https://` address. If SWAG reaches PhotoPrism from an address outside Docker’s default internal range, add the proxy IP or CIDR to [`PHOTOPRISM_TRUSTED_PROXY`](../config-options.md#networking) so forwarded client and protocol headers are accepted.

## Step 1: Prepare a Domain or DynDNS Record

Obtain a fully qualified domain name that points to your public IP. DuckDNS works well for home networks; set up port forwarding for TCP 80/443 on your router.

## Step 2: Start SWAG via Docker Compose

Configure SWAG with your domain and preferred validation method. The snippet below uses DuckDNS:

```yaml
services:
  swag:
    image: ghcr.io/linuxserver/swag
    container_name: swag
    restart: unless-stopped
    ports:
      - 80:80
      - 443:443
    cap_add:
      - NET_ADMIN
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Brussels
      - URL=mydomain.duckdns.org
      - SUBDOMAINS=photoprism
      - VALIDATION=duckdns
      - DUCKDNSTOKEN=your-duckdns-token
      - EMAIL=admin@example.com
    volumes:
      - /etc/config/swag:/config
```

Persist `/config` so certificates and fail2ban state survive container restarts.

Since SWAG faces the internet directly, pull its latest image regularly (`docker compose pull swag && docker compose up -d swag`) so you receive NGINX security updates promptly. The [NGINX security advisories](https://nginx.org/en/security_advisories.html) list affected and fixed versions.

## Step 3: Enable the PhotoPrism Proxy Config

Inside `/etc/config/swag/nginx/proxy-confs/` rename `photoprism.subdomain.conf.sample` to `photoprism.subdomain.conf`. Custom deployments can create their own file with settings similar to:

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name photoprism.mydomain.duckdns.org;

    include /config/nginx/ssl.conf;
    client_max_body_size 512M;

    location / {
        include /config/nginx/proxy.conf;
        resolver 127.0.0.11 valid=30s;
        set $upstream_app photoprism;
        set $upstream_port 2342;
        set $upstream_proto http;
        proxy_pass $upstream_proto://$upstream_app:$upstream_port;
    }
}
```

Adjust `server_name` and the upstream container name or IP as needed. If your PhotoPrism container is not called `photoprism`, update both the SWAG config and your Compose file (`container_name: photoprism`) so the DNS lookup succeeds.

## Step 4: Reload SWAG

Apply configuration changes with `docker restart swag` or by sending `docker exec swag nginx -s reload`. Watch the container logs for certificate renewal or proxy errors.

## Step 5: Test Access

Browse to `https://photoprism.mydomain.duckdns.org/` and verify you can log in, upload large files, and browse thumbnails. Use `docker logs swag` if uploads fail—messages like `client intended to send too large body` indicate `client_max_body_size` must be raised.

!!! attention
    PhotoPrism’s container name is prefixed by the project directory (e.g., `photoprism-photoprism-1`) when you rely on Compose defaults. Either set `container_name: photoprism` in your `compose.yaml` or update SWAG’s `set $upstream_app` value so the proxy can resolve the container.

## Why Use a Proxy? ##

If you install PhotoPrism on a public server outside your home network, **always run it behind a secure
HTTPS reverse proxy**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted
by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to
connect as well.

![](https://dl.photoprism.app/img/diagrams/reverse-proxy.svg){ class="w100" }

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
