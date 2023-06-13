# Using Traefik as Reverse Proxy

!!! success "Best Choice"
    - No special settings required in combination with modern web applications
    - WebSocket proxying automatically works
    - [Traefik](https://doc.traefik.io/traefik/) can [create and update](https://doc.traefik.io/traefik/user-guides/docker-compose/acme-http/)  [Let's Encrypt](https://letsencrypt.org/) HTTPS certificates for you

Our example shows a working configuration, excluding general PhotoPrism [config options](../config-options.md) 
documented in [Setup Using Docker Compose](../docker-compose.md):

!!! example "docker-compose.yml"
    ```yaml
    services:
      traefik:
        image: traefik:v2.5
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

### Why Use a Proxy? ###

If you install PhotoPrism on a public server outside your home network, **always run it behind a secure
HTTPS reverse proxy**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted
by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to
connect as well.

![](https://dl.photoprism.app/img/diagrams/reverse-proxy.svg){ class="w100" }

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
