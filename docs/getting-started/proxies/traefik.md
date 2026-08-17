# Using Traefik as Reverse Proxy

!!! success "Best Choice"
    - No custom middleware required for WebSockets or HTTP/2
    - [Traefik](https://doc.traefik.io/traefik/) issues and renews [Let’s Encrypt](https://letsencrypt.org/) certificates automatically
    - Integrates cleanly with Docker labels, Kubernetes ingress, and static config files

To run PhotoPrism behind Traefik, create a `traefik.yaml` configuration and then add a `traefik` service to your `compose.yaml` or `docker-compose.yml` file, as shown in the following example. Set [the public Site URL](../config-options.md#site-information) to the external `https://` address. If Traefik reaches PhotoPrism from an address outside Docker’s default internal range, also add its IP or CIDR to [`PHOTOPRISM_TRUSTED_PROXY`](../config-options.md#networking).

!!! example "compose.yaml"
    ```yaml
    services:
      traefik:
        image: traefik:v3.7
        restart: unless-stopped
        ports:
          - "80:80"
          - "443:443"
        volumes:
          - "./traefik.yaml:/etc/traefik/traefik.yaml"
          - "./traefik/data:/data"
          - "/var/run/docker.sock:/var/run/docker.sock:ro"

      photoprism:
        image: photoprism/photoprism:latest
        restart: unless-stopped
        labels:
          - "traefik.enable=true"
          - "traefik.http.routers.photoprism.rule=Host(`photos.example.com`)"
          - "traefik.http.routers.photoprism.entrypoints=websecure"
          - "traefik.http.routers.photoprism.tls=true"
          - "traefik.http.routers.photoprism.tls.certresolver=myresolver"
          - "traefik.http.services.photoprism.loadbalancer.server.port=2342"
        volumes:
          - "./originals:/photoprism/originals"
          - "./storage:/photoprism/storage"
        environment:
          PHOTOPRISM_SITE_URL: "https://photos.example.com/"
          PHOTOPRISM_DISABLE_TLS: "true"
    ```

!!! example "traefik.yaml"
    ```yaml
    log:
      level: INFO

    global:
      sendAnonymousUsage: false

    entryPoints:
      web:
        address: ":80"
        http:
          encodedCharacters:
            allowEncodedSlash: true
            allowEncodedPercent: true
            allowEncodedHash: true
            allowEncodedQuestionMark: true
            allowEncodedSemicolon: true
          redirections:
            entryPoint:
              to: websecure
              scheme: https
      websecure:
        address: ":443"
        http:
          encodedCharacters:
            allowEncodedSlash: true
            allowEncodedPercent: true
            allowEncodedHash: true
            allowEncodedQuestionMark: true
            allowEncodedSemicolon: true
        transport:
          respondingTimeouts:
            readTimeout: "3h"
            writeTimeout: "0s"

    providers:
      docker:
        exposedByDefault: false
        watch: true

    api:
      insecure: false
      dashboard: false
      debug: false

    certificatesResolvers:
      myresolver:
        acme:
          email: ssl-admin@example.com
          storage: /data/certs.json
          httpChallenge:
            entryPoint: web
    ```

Note that you must disable [HTTPS/TLS](../using-https.md#1-https-reverse-proxy) in PhotoPrism by setting `PHOTOPRISM_DISABLE_TLS` to `"true"`, because Traefik is already handling TLS termination. The service label `traefik.http.services.photoprism.loadbalancer.server.port=2342` tells Traefik which internal port to use.

!!! tip "Timeouts & Encoded Characters"
    Two settings in the example above are easy to leave out and cause problems that look unrelated to the proxy:

    - **`respondingTimeouts`** raises the limits for slow requests. Without a generous `readTimeout`, large uploads and long downloads are cut off mid-transfer; `writeTimeout: "0s"` disables the write limit so streaming a large original or video is not interrupted.
    - **`encodedCharacters`** lets percent-encoded characters through to PhotoPrism instead of having Traefik reject the request. File and folder names legitimately contain `/`, `%`, `#`, `?`, and `;`, which appear percent-encoded in request paths, so blocking them makes the affected files fail to load. These options require **Traefik v3.6 or later**.

    Set them on **both** entry points, since a request can arrive on either before the redirect to HTTPS.

Further `traefik.yaml` examples and a detailed description of the Traefik configuration can be found in the [corresponding documentation](https://doc.traefik.io/traefik/user-guides/docker-compose/basic-example/).

### Why Use a Proxy? ###

If you install PhotoPrism on a public server outside your home network, **always run it behind a secure
HTTPS reverse proxy**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted
by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to
connect as well.

![](https://dl.photoprism.app/img/diagrams/reverse-proxy.svg){ class="w100" }

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
