# Using SWAG as Reverse Proxy

To make the setup of a Reverse Proxy much easier, Linuxserver.io developed [SWAG](https://github.com/linuxserver/docker-swag)  
SWAG - Secure Web Application Gateway (formerly known as letsencrypt, no relation to Let's Encrypt™) sets up an Nginx webserver and reverse proxy with php support and a built-in certbot client that automates free SSL server certificate generation and renewal processes (Let's Encrypt and ZeroSSL). It also contains fail2ban for intrusion prevention.

## Step 1: Get a domain

The first step is to grab a dynamic dns if you don't have your own subdomain already. You can get this from for example [DuckDNS](https://www.duckdns.org).

## Step 2: Set-up SWAG

Then you will need to setup SWAG, the variables of the  docker-compose are explained on the Github-page of [SWAG](https://github.com/linuxserver/docker-swag). This is an example on how to set it up using duckdns and docker-compose. 

!!! example "docker-compose.yml"
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
      		- SUBDOMAINS=www,
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

Don't forget to change the <mydomain.duckns> into your personal domain and the <duckdnstoken> into your token.

## Step 3: Change the config files

Navigate to the config folder of SWAG and head to <code>proxy-confs</code>. If you used the example above, you should navigate to: <code>/etc/config/swag/nginx/proxy-confs/ </code>.
Their are a lot of preconfigured files to use for different apps such as radarr,sonarr,overseerr,... 

To use the bundled configuration file, simply rename <code>photoprism.subdomain.conf.sample</code> in the proxy-confs folder to <code>photoprism.subdomain.conf</code>.
**It is possible that the config file isn't added yet. Please create the following file with your editor of choice.**
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

## Step 4: Port-forward port 443

Since SWAG allows you to set-up a secure connection, you will need to open port 443 on your router. This is way more secure then port 80.

## Step 5: Restart SWAG

When you change anything in the config of nginx, you will need to restart the containter using <code>docker restart swag</code>.
If everything went well, you can now access photoprism on the subdomain you configured: photoprism.<mydomain>.duckdns.org

!!! attention
    In some cases, the docker-container of photoprism won't be named "photoprism". To check this, execute <code>docker ps</code> and check wether it is named "photoprism". If it's not, execute <code>docker rename <currentcontainername> photoprism</code>. Restart swag afterwards.


