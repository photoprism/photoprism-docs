# Using HTTPS

*This guide shows you how to enable HTTPS/TLS, configure existing server certificates, and obtain new certificates as needed. If you have suggestions for improvement, please let us know by clicking :material-file-edit-outline: to send a pull request.*

## Why Use Encryption?

If you install PhotoPrism on a shared server so that it is not only accessible to the local host, always **secure the connection using HTTPS**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted by anyone, including your provider, hackers, and governments. Backup tools and file synchronization apps may also refuse to connect.

![](https://dl.photoprism.app/img/diagrams/reverse-proxy.svg){ class="w100" }

!!! tldr ""
    HTTPS connections use Transport Layer Security (TLS) for encryption. TLS is a network protocol that establishes an encrypted connection to an authenticated peer over an untrusted network.

## How To Enable HTTPS

You have the following options to enable HTTPS/TLS when using our [latest stable release](../release-notes.md).
Note that after adding or updating certificates, it is required to restart PhotoPrism for the changes to take effect.

### 1. HTTPS Reverse Proxy

To run your instance behind an [HTTPS reverse proxy like Traefik](proxies/traefik.md), we recommend that you explicitly disable TLS in PhotoPrism by setting `PHOTOPRISM_DISABLE_TLS` to `"true"` in your `docker-compose.yml` configuration:

```yaml
services:
  photoprism:
    # ...
    environment:
      PHOTOPRISM_SITE_URL: "https://www.example.com/"
      PHOTOPRISM_DISABLE_TLS: "true"
```

!!! note ""
    Especially if your server also has other web applications installed and/or a proxy with working HTTPS is already in place, this may be the best option.

### 2. Self-Signed Certificate

```yaml
services:
  photoprism:
    # ...
    environment:
      PHOTOPRISM_SITE_URL: "https://www.example.com/"
      PHOTOPRISM_DISABLE_TLS: "false"
      PHOTOPRISM_DEFAULT_TLS: "true"
      PHOTOPRISM_INIT: "https"
```

### 3. Custom Certificate

To use your own certificates, you can add a custom TLS certificate and private key to the `storage/config/certificates` folder with the filenames `www.example.com.crt` and `www.example.com.key`, replacing `www.example.com` with the actual server domain. For this, you can set the same config options as when using a self-signed certificate (see above).

Alternatively, you can specify a custom TLS certificate (`*.crt`) and private key (`*.key`) filename within the `storage/config/certificates` folder using the `PHOTOPRISM_TLS_CERT` and `PHOTOPRISM_TLS_KEY` [environment variables](config-options.md) in your `docker-compose.yml`, or use the corresponding [command flags](config-options.md):

```yaml
services:
  photoprism:
    # ...
    environment:
      PHOTOPRISM_SITE_URL: "https://www.example.com/"
      PHOTOPRISM_TLS_CERT: "site.crt"
      PHOTOPRISM_TLS_KEY: "site.key"
      PHOTOPRISM_DISABLE_TLS: "false"
      PHOTOPRISM_DEFAULT_TLS: "true"
      PHOTOPRISM_INIT: "https"
```

!!! note ""
    We recommend that you keep the `PHOTOPRISM_DEFAULT_TLS` option enabled so that you can always connect securely over HTTPS even if there is a problem with your custom certificates.

## Obtaining Certificates

Valid server certificates can be obtained either from a commercial [Certificate Authority](https://en.wikipedia.org/wiki/Certificate_authority) (CA) like [ZeroSSL](#zerossl) or free of charge from [Let's Encrypt](#lets-encrypt):

### Let’s Encrypt

![Let’s Encrypt](img/letsencrypt.svg){ class='md right' }
[Let's Encrypt](https://letsencrypt.org/) is an automatic certificate authority that provides you with free HTTPS/TLS certificates. Many web servers and reverse proxies such as [Traefik](proxies/traefik.md) and [Caddy](proxies/caddy-2.md) have integrated support for obtaining single-domain certificates if your server is accessible on port 80 over the public Internet.

The creation of certificates for servers that are not publicly reachable or that are valid for all subdomains (wildcard) is alternatively possible with the [LEGO Let's Encrypt client](https://go-acme.github.io/lego/usage/cli/obtain-a-certificate/). If you use Docker and [DigitalOcean's free DNS service](https://m.do.co/c/f9725a28bb6b), the [command to run](https://go-acme.github.io/lego/usage/cli/obtain-a-certificate/) will look as follows (replace the certificate path, access token, domain names, and email address with the appropriate values):

```bash
docker run --rm -v "/path/to/certificates:/data/" \
-e DO_AUTH_TOKEN=YOUR_ACCESS_TOKEN goacme/lego -a --path=/data \
--email="tls@example.com" --dns=digitalocean --dns-timeout=180 \
-d "example.com" -d "*.example.com" run
```

Note that this verification method only works if you use a [supported DNS provider](https://go-acme.github.io/lego/dns/) that LEGO can access through an API. Please refer to [its documentation](https://go-acme.github.io/lego/dns/) for details, as each provider requires different authentication credentials. If you are [using DigitalOcean](https://m.do.co/c/f9725a28bb6b), you can create the required access token in [your customer dashboard](https://cloud.digitalocean.com/account/api/tokens) and replace `YOUR_ACCESS_TOKEN` with it.

### ZeroSSL

[![ZeroSSL](img/zerossl.svg){ class='md right' }](https://link.photoprism.app/zerossl)
[ZeroSSL](https://link.photoprism.app/zerossl) is a trusted European certificate authority headquartered in Vienna, Austria.

Compared to Let's Encrypt, ZeroSSL also offers a user-friendly web interface, you can create certificates that are valid for longer than 90 days, and you may choose additional domain verification methods depending on your plan.

[Learn more ›](https://link.photoprism.app/zerossl)

## Troubleshooting

### Enabling Trace Log Mode

A good way to troubleshoot configuration issues is to increase the log level. To enable [trace log mode](config-options.md), set `PHOTOPRISM_LOG_LEVEL` to `"trace"` in the `environment:` section of the `photoprism` service (or use the `--trace` flag when running the `photoprism` command directly):


```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_LOG_LEVEL: "trace"
      ...
```

Then [restart all services](docker-compose.md#step-2-start-the-server) for your changes to take effect:

```bash
docker compose stop
docker compose up -d
```

### Viewing Docker Service Logs

You can run this command to check the server logs for warnings and errors, including the last 100 messages (omit `--tail=100` to see them all, and `-f` to output only the last logs without watching them):

```bash
docker compose logs -f --tail=100 
```

[Learn more ›](troubleshooting/docker.md#viewing-logs)

### Failed to Find Any PEM Data in Key Input

This error can indicate that your key file starts with an unexpected Byte Order Mark (BOM):

- https://www.google.com/search?q=failed+to+find+any+pem+data+tls+golang
- https://stackoverflow.com/questions/57596920/failed-to-find-any-pem-data-in-key

While BOMs are not strictly forbidden, there is only one way to encode UTF-8, and so they are not needed and extremely rare. As a result, a lot of software has problems with them.

You should be able to fix this by opening the file with a regular text or code editor (not Notepad) and then saving it again. Finally, restart all services for the changes to take effect:

```bash
docker compose stop
docker compose up -d
```

!!! tldr ""
    Our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible Linux distributions.