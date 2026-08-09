# Using Apache 2.4 as Reverse Proxy

!!! danger "Getting Support"
    If you run into Apache-specific issues we cannot reproduce, please reach out to the [Apache community](https://httpd.apache.org/userslist.html) for help. Our team cannot provide support for third-party modules or custom SSL setups.

Apache 2.4 can proxy HTTP/2 and WebSocket traffic for PhotoPrism as long as the required modules are enabled (`proxy`, `proxy_http`, `proxy_wstunnel`, `ssl`, `headers`, `http2`). Remember to keep `PHOTOPRISM_DISABLE_TLS="true"` so Apache terminates HTTPS instead of the app container.

Set [the public Site URL](../config-options.md#site-information) to your external `https://` address. If Apache reaches PhotoPrism from an address outside Docker’s default internal range, add the proxy IP or CIDR to [`PHOTOPRISM_TRUSTED_PROXY`](../config-options.md#networking) so forwarded client and protocol headers are accepted.

## Enable Required Modules

```bash
sudo a2enmod proxy proxy_http proxy_wstunnel headers ssl http2 rewrite
sudo systemctl restart apache2
```

## Example VirtualHost Configuration

The snippet below force-redirects HTTP→HTTPS, terminates TLS via Let’s Encrypt, and forwards both standard requests and WebSockets to PhotoPrism.

```apache
<VirtualHost *:80>
    ServerName photos.example.com
    Redirect permanent / https://photos.example.com/
</VirtualHost>

<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName photos.example.com

    SSLEngine on
    SSLCertificateFile    /etc/letsencrypt/live/photos.example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/photos.example.com/privkey.pem

    ProxyPreserveHost On
    ProxyRequests Off
    AllowEncodedSlashes NoDecode
    RequestHeader set X-Forwarded-Proto "https"
    Header always set Strict-Transport-Security "max-age=31536000;includeSubDomains"

    ProxyPass "/api/v1/ws"  "ws://photoprism:2342/api/v1/ws" retry=0 timeout=300
    ProxyPassReverse "/api/v1/ws"  "ws://photoprism:2342/api/v1/ws"

    ProxyPass "/"  "http://photoprism:2342/" connectiontimeout=5 timeout=600 keepalive=On
    ProxyPassReverse "/"  "http://photoprism:2342/"

    ProxyPassReverseCookieDomain photoprism photos.example.com
    ProxyPassReverseCookiePath / /

    ErrorLog ${APACHE_LOG_DIR}/photoprism_error.log
    CustomLog ${APACHE_LOG_DIR}/photoprism_access.log combined
</VirtualHost>
</IfModule>
```

After saving the file in `/etc/apache2/sites-available/`, enable it with `sudo a2ensite photoprism.conf && sudo systemctl reload apache2`.

Refer to the [Apache proxy guide](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html) and the [WebSocket tunnel module](https://httpd.apache.org/docs/2.4/mod/mod_proxy_wstunnel.html) for more detail.

### Why Use a Proxy? ###

If you install PhotoPrism on a public server outside your home network, **always run it behind a secure
HTTPS reverse proxy**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted
by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to
connect as well.

![](https://dl.photoprism.app/img/diagrams/reverse-proxy.svg){ class="w100" }

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
