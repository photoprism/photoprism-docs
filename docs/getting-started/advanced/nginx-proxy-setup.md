# Advanced NGINX Proxy Setup

*Note: This is contributed content and may be outdated. Click the edit link to perform changes and send a pull request.*

Using a reverse proxy in front of PhotoPrism has various benefits:

 * Make use of HTTP/2
 * Add encryption
 * Perform traffic optimization
 * Enhance security (NGINX may block dangerous request patterns the embedded Go-based HTTP server does not know about)

**If you consider exposing your PhotoPrism instance to the evil internet, you should at least secure it with a proper HTTPS encryption.**

This guide aims for a little more advanced setup, with good security in mind.

**Trough the entire guide we use `photoprism.example.com` as domain. You have to change all these occurrences with your own domain / DynDNS.**

Also, this was all tested on `ubuntu/20.04` - But the commands should work on a lot of other versions as well.
If you use CentOS, SuSE, or any other distro, look up the commands for your package manager.

## Setup

### Domain setup

First, we need to decide what we want to use as domain / address. We will use a proper domain in this guide, but it will technically also work with just a static IP address. 

If you're lucky enough to have your own domain, just create a subdomain and use this for PhotoPrism.

If you want to expose your instance hosted at home, just use a **DynDNS**  provider (just duckduckgo it, there a multiple ones that are free).
!!! tip 
    if you're new to DynDNS it might be good to know that most routers do support DynDNS. 
    Therefore only minimal setup is required.
    Just search for `your router name + DynDNS` ;)
    
### Install NGINX on your machine
If not already done, install the webserver on your machine which you wish to use as proxy. 
This also can be the same host that is running the docker container.
```bash
apt-get update && apt-get install -y nginx apache2-utils
``` 

!!! info
    We use `apache2-utils` later for the password generation of the optional extra security with http basic auth.
    
### Acquire a certificate
#### Install cerbot
Luckily nowadays there is a free certificate authority called [Let's Encrypt](https://letsencrypt.org/).
You can just use  their `certbot` tool and acquire a new certificate in seconds.

For Ubuntu / Debian the package is directly in the repository.
Therefore, you can easily install it using this command: 
```bash
apt-get update && apt-get install -y certbot python3-certbot-nginx
```
#### Generate the certificate
Now, just request a new certificate by using this command: 
```bash
certbot -d photoprism.example.com
```

After that you should have a new certificate in: `/etc/letsencrypt/live/photoprism.example.com/`
!!! note
    In order for Let's Encrypt to work, the server has to be accessible from the internet on port 443

!!! tip 
    Please refer to Let's Encrypts [documentation](https://certbot.eff.org/docs/using.html#renewing-certificates) for automated certificate renewal. The certificates are valid for around 90 days.

### Setup NGINX
Now that we have our certificate its time to setup the NGINX itself.
Since it is best practice to create a configuration file per application / domain, this is exactly what we gonna do.

Create a new file `/etc/nginx/sites-enabled/photoprism.example.com` and put the following content in it.
**Keep in mind to change the domain (there a multiple entries!)**
```nginx
# PhotoPrism Nginx config with SSL HTTP/2 and reverse proxy
# This file gives you an example on how to secure you PP instance with SSL
server {
    # listen 80; # If you really need HTTP (unsecure) remove the "#" on the beginning. Not recommended!
    # listen [::]:80; # HTTP IPv6

    listen 443 ssl http2; # Listen on port 443 and enable ssl and HTTP/2
    listen [::]:443 ssl http2; # Same for IPv6

    # Put your domain name in here.
    server_name  photoprism.example.com;

    # - - - - - - - - - -
    # SSL security
    # - - - - - - - - - -
    ssl_certificate          /etc/letsencrypt/live/photoprism.example.com/fullchain.pem;
    ssl_certificate_key      /etc/letsencrypt/live/photoprism.example.com/privkey.pem;

    # Since the PP API is also used on Android, we have to keep TLS1.2 in here for a while.
    # A lot of the older Android devices do not support TLS1.3 yet :/
    ssl_protocols            TLSv1.2 TLSv1.3;

    # Use good and strong ciphers, disable weak and old ciphers
    ssl_ciphers              HIGH:!RC4:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS;

    # Enable HSTS (https://developer.mozilla.org/en-US/docs/Security/HTTP_Strict_Transport_Security)
    add_header Strict-Transport-Security "max-age=172800; includeSubdomains";

    # This checks if the certificate has been invalidated by the certificate authority
    # You can remove this section if you use self-singed certificates...
    # Enable OCSP stapling (http://blog.mozilla.org/security/2013/07/29/ocsp-stapling-in-firefox)
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/photoprism.example.com/fullchain.pem;

    # DNS Servers to use for OCSP lookups
    resolver 8.8.8.8 1.1.1.1 9.9.9.9 valid=300s;
    resolver_timeout 5s;

    # - - - - - - - - -
    # Reverse Proxy
    # - - - - - - - - -
    proxy_redirect           off;
    proxy_set_header         X-Real-IP $remote_addr;                        # Let PP know the clients real IP
    proxy_set_header         X-Forwarded-For $proxy_add_x_forwarded_for;    # Let PP know that a proxy did forward this request
    proxy_set_header         Host $http_host;                               # Set Proxy host info

    proxy_http_version 1.1;                                                 # Required for WebSocket connection
    proxy_set_header Upgrade $http_upgrade;                                 # Allow protocol switch to websocket
    proxy_set_header Connection "upgrade";                                  # Do protocol switch
    proxy_set_header X-Forwarded-Proto $scheme;                             # Let PP know that this connection used HTTP or HTTPS

    client_max_body_size 500M;                                              # Bump the max body size, you may want to upload huge stuff via the upload GUI
    proxy_buffering off;                                                    # Do not hold back the request while the client sends data, give the stream directly to PP

    location / {
            # Optional; additional protection with Basic Auth.
            # Note: This breaks WebDAV without additional configuration
            #       You also have to create a .htpasswd file using the command:
            #       "htpasswd -c /etc/nginx/.pp_htpasswd my_secret_user"
            # - - -
            # auth_basic           "PhotoPrism Pre Auth";
            # auth_basic_user_file /etc/nginx/.pp_htpasswd;

            # pipes the traffic to PhotoPrism
            # Change this to your PhotoPrisms IP / DNS
            proxy_pass http://docker.homenet:2342;
    }
}
```

Have a look at the individual comments in the configuration for a further description.

!!!tip
    Don't forget to change the PhotoPrism IP / DNS on the bottom of the config... ;)
   
   
Once you've changed everything you need, let's restart `nginx`:

```bash
service nginx restart
```
Now, you should have access to PhotoPrism.

!!! warning
    Make sure to setup proper firewalling on the machine that is running PhotoPrism.
    Have a look at [ufw](https://help.ubuntu.com/community/UFW) for simple firewall rules.
