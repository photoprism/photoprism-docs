# Using Traefik as Reverse Proxy

WebSocket proxying automatically works with [Traefik](https://doc.traefik.io/traefik/). 
There is no need to enable this as necessary for Caddy 1, Apache,
and NGINX. In addition, Traefik may [automatically create](https://doc.traefik.io/traefik/user-guides/docker-compose/acme-http/) and update 
[Let's Encrypt](https://letsencrypt.org/) HTTPS certificates.

Our example shows a working configuration, excluding general PhotoPrism [config options](../config-options.md) 
documented in [Setup Using Docker Compose](../docker-compose.md):

!!! example "docker-compose.yml"
    ```yaml
    services:
      traefik:
        image: traefik:v2.2
        restart: unless-stopped
        ports:
          - "80:80"
          - "443:443"
        volumes:
          - "./traefik.yaml:/etc/traefik/traefik.yaml"
          - "./traefik/data:/data"
          - "/var/run/docker.sock:/var/run/docker.sock"

      photoprism:
        image: photoprism/photoprism:latest
        restart: unless-stopped
        labels:
          - "traefik.http.routers.photoprism.rule=Host(`example.com`)"
          - "traefik.http.routers.photoprism.tls=true"
          - "traefik.http.routers.photoprism.tls.certresolver=myresolver"
        volumes:
          - "./originals:/photoprism/originals"
          - "./storage:/photoprism/storage"
        environment:
            PHOTOPRISM_SITE_URL: "https://example.com/"
    ```


!!! example "traefik.yaml"
    ```yaml
    entryPoints:
      web:
        address: ":80"
        http:
          redirections:
            entryPoint:
              to: websecure
      websecure:
        address: ":443"
    
    providers:
      docker: {}
        
    certificatesResolvers:
      myresolver:
        acme:
          email: you@example.com
          storage: /data/letsencrypt.json
          httpChallenge:
            entryPoint: web
    ```

Please refer to the [official documentation](https://doc.traefik.io/traefik/user-guides/docker-compose/basic-example/)
for further details.

!!! important ""
    When installing PhotoPrism on a public server outside your home network, please **always run it
    behind a secure HTTPS reverse proxy**.
    Your files and passwords will be transmitted in clear text otherwise, and can be intercepted
    by anyone in between including your provider, hackers, and governments.
