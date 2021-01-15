# Using NGINX as Reverse Proxy

This [tutorial](https://www.serverlab.ca/tutorials/linux/web-servers-linux/how-to-configure-nginx-for-websockets/) explains, how to configure NGINX WebSocket connections between your client and backend services.

!!! example
    ```
    http {
      server {
        listen 80 ssl;
        listen [::]:80 ssl;
        server_name example.com
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
        }
      }
    }
    ```

At the very least you will need to adapt `server_name` and the `ssl_certificate`/`ssl_certificate_key` paths to match your setup. Please refer to their [official documentation](https://nginx.org/en/docs/) for further details.

!!! attention
    When installing PhotoPrism on a public server outside your home network, please **always run it
    behind a secure HTTPS reverse proxy**.
    Your files and passwords will be transmitted in clear text otherwise, and can be intercepted
    by anyone in between including your provider, hackers, and governments.
