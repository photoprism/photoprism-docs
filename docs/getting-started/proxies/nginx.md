# Using NGINX as Reverse Proxy

This [tutorial](https://www.serverlab.ca/tutorials/linux/web-servers-linux/how-to-configure-nginx-for-websockets/) explains, how to configure NGINX WebSocket connections between your client and backend services.

!!! example
    ```
    http {
      server {
        server_name example.com
        client_max_body_size 500M;
    
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

Please refer to their [official documentation](https://nginx.org/en/docs/) for further details.

!!! attention
    When installing PhotoPrism on a public server outside your home network, please **always run it
    behind a secure HTTPS reverse proxy**.
    Your files and passwords will be transmitted in clear text otherwise, and can be intercepted
    by anyone in between including your provider, hackers, and governments.
