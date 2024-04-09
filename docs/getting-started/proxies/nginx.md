# Using NGINX as Reverse Proxy

!!! danger "Getting Support"
    Since [NGINX](https://www.nginx.com/) is [notoriously difficult](https://github.com/photoprism/photoprism/issues?q=is%3Aissue+nginx) to [configure](https://www.nginx.com/nginx-wiki/build/dirhtml/start/topics/tutorials/config_pitfalls/), we are unable to [provide technical support](https://www.photoprism.app/kb/getting-support) for NGINX-related issues such as [failed uploads](https://github.com/photoprism/photoprism/discussions/2698#discussioncomment-9056567), [connection errors](../troubleshooting/index.md#connection-fails), [broken thumbnails](../troubleshooting/index.md#broken-thumbnails), and [video playback problems](../troubleshooting/index.md#videos-dont-play). If you cannot resolve these on your own, we recommend that you [ask their community for advice](https://www.nginx.com/support/) or [use Traefik instead](traefik.md), which is easier to configure and more convenient to handle overall.

This [tutorial](https://www.serverlab.ca/tutorials/linux/web-servers-linux/how-to-configure-nginx-for-websockets/) explains, how to configure NGINX WebSocket connections between your client and backend services.

!!! example
    ```
    http {
      server {
        listen 80 ssl;
        listen [::]:80 ssl;
        server_name example.com;
        client_max_body_size 500M;
    
        # With SSL via Let's Encrypt
        ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

        location / {
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header Host $host;
    
          proxy_pass http://photoprism:2342;
    
          proxy_buffering off;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
          
          client_max_body_size 500M;
        }
      }
    }
    ```

At the very least you will need to adapt `server_name` and the `ssl_certificate`/`ssl_certificate_key` paths to match your setup. Please refer to their [official documentation](https://nginx.org/en/docs/) for further details.

[View "Pitfalls and Common Mistakes" ›](https://www.nginx.com/nginx-wiki/build/dirhtml/start/topics/tutorials/config_pitfalls/)

### Why Use a Proxy? ###

If you install PhotoPrism on a public server outside your home network, **always run it behind a secure
HTTPS reverse proxy**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted
by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to
connect as well.

![](https://dl.photoprism.app/img/diagrams/reverse-proxy.svg){ class="w100" }

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
