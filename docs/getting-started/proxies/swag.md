# Using SWAG as Reverse Proxy

!!! tldr ""
    Should you experience problems with Swag, we recommend that you ask the Swag community for advice, as we cannot provide support for third-party software and services.

To simplify the setup of a reverse HTTPS proxy, Linuxserver.io developed [SWAG](https://github.com/linuxserver/docker-swag).

SWAG - Secure Web Application Gateway (formerly known as *letsencrypt*, no relation to Let's Encrypt™) sets up a Nginx
web server and reverse proxy with PHP support and a built-in certbot client that automates free SSL server certificate
generation and renewal processes (Let's Encrypt and ZeroSSL). It also contains fail2ban for intrusion prevention.

## Setup ##

### Step 1: Get a domain ###

The first step is to grab a dynamic DNS if you don't have your own subdomain already. You can get this from for example [DuckDNS](https://www.duckdns.org).

### Step 2: Set-up SWAG ###

Then you will need to set up SWAG, the variables of the docker compose are explained on the Github page of [SWAG](https://github.com/linuxserver/docker-swag).
This is an example of how to set it up using duckdns and docker-compose. 

!!! example "compose.yaml"
    ```yaml
	version: "2.1"
	services:
	 swag:
   	 image: ghcr.io/linuxserver/swag
   	 container_name: swag
    		cap_add:
     		- NET_ADMIN
   		environment:
      		- PUID=1000
      		- PGID=1000
      		- TZ=Europe/Brussels
      		- URL=<mydomain.duckdns>
      		- SUBDOMAINS=wildcard
      		- VALIDATION=duckdns
      		- CERTPROVIDER= #optional
      		- DNSPLUGIN= #optional
      		- DUCKDNSTOKEN=<duckdnstoken> 
      		- EMAIL=<e-mail> #optional
      		- ONLY_SUBDOMAINS=false #optional
      		- EXTRA_DOMAINS=<extradomains> #optional
      		- STAGING=false #optional
    		volumes:
      		- /etc/config/swag:/config
    		ports:
      		- 443:443
    		restart: unless-stopped
    ```

Don't forget to change the <code>mydomain.duckdns</code> into your personal domain and the <code>duckdnstoken</code> into your token and remove the brackets.

### Step 3: Change the config files ###

Navigate to the config folder of SWAG and head to <code>proxy-confs</code>. If you used the example above, you should navigate to: <code>/etc/config/swag/nginx/proxy-confs/ </code>.
There are a lot of preconfigured files to use for different apps such as radarr,sonarr,overseerr,... 

To use the bundled configuration file, simply rename <code>photoprism.subdomain.conf.sample</code> in the proxy-confs folder to <code>photoprism.subdomain.conf</code>.
Alternatively, you can create a new file <code>photoprism.subdomain.conf</code> in proxy-confs with the following configuration:

!!! example "photoprism.subdomain.conf"
    ```yaml
	server {
    	listen 443 ssl http2;
    	listen [::]:443 ssl http2;

    	server_name photoprism.*;

    	include /config/nginx/ssl.conf;

    	client_max_body_size 0;

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

### Step 4: Port-forward port 443 ###

Since SWAG allows you to set up a secure connection, you will need to open port 443 on your router for encrypted traffic. This is way more secure than port 80 for http.

### Step 5: Restart SWAG ##

When you change anything in the config of Nginx, you will need to restart the container using <code>docker restart swag</code>.
If everything went well, you can now access photoprism on the subdomain you configured: photoprism.mydomain.duckdns.org

!!! attention
    The docker-container of photoprism won't be named "photoprism", it will be "name_photoprism".
    To check this, execute <code>docker ps</code> and check wether it is named "photoprism".
    If it's not, go to your docker-compose.yml file and add the following line to photoprism below 'image' <code>container_name=photoprism</code>. Restart swag afterwards.
    <b>Keep in mind to not have two photoprism containers with the same name!</b> 
    You could also change the config file of Swag with the right name in the proxy-confs directory.

## Why Use a Proxy? ##

If you install PhotoPrism on a public server outside your home network, **always run it behind a secure
HTTPS reverse proxy**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted
by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to
connect as well.

![](https://dl.photoprism.app/img/diagrams/reverse-proxy.svg){ class="w100" }

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
