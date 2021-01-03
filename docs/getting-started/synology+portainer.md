# Setup Using Synology NAS and Portainer

This guide will help you install Photoprism in your Synology NAS using [Portainer](https://www.portainer.io/), an open-source container manager system. The guide will cover the following steps:

- install Portainer in your Synology NAS using Task Manager;
- configure Portainer to use your Synology's docker endpoint;
- install Photoprism in your Synology NAS using Portainer, accessible over http / direct IP;
- (TO-DO) configure a reverse proxy in your Synology NAS to access Photoprism over https / custom domain name.

### Step 1: install Portainer in your Synology NAS using Task Manager ###

Synology's official docker app is quite limited in terms of functionality and that is the reason why we will install Portainer first. It will make managing docker containers inside Synology much more easier and functional while sharing the same local docker endpoint (i.e. the same docker images / containers / volumes / etc. will be manageable in both Synology's app and Portainer). We could install it using the terminal / SSH connection to the NAS but in this way everything can be done using Synology's Diskstation Manager UI.

To install Portainer:

1. install Synology's Docker app from the official package center;
2. open Synology's File Station app and browse to the newly created _docker_ shared folder;
3. create a folder named _portainer_ inside _docker_, which will persist relevant Portainer's data in our local filesystem.
4. open Synology's Control Panel > Task Scheduler and create a new Scheduled Task > User-defined script; you'll then need to fill in some details in the _General_, _Schedule_ and _Task Settings_ sections.

    4.1. in _General_ fill in:
    
      4.1.1. Task: use a meaningfull name, for eg. _Install Portainer_;
      
      4.1.2. User: keep this as _root_.

    4.2. in _Schedule_ fill in:
    
      4.2.1. Date: set the task to run on a specific date (for eg. today) and choose _Do not repeat_. This task will be used just once to install Portainer, we don't want to run it afterwards;
      
      4.2.2. Time: leave the default settings, they have no relevance;

    4.3. in _Task Settings_ fill in:
    
      4.3.1. Run command: copy/paste the user defined script below. Check if the ports are available on your NAS and that the path to the volume is correct (it should point to the folder created in step 3 above):
      ```
      docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v /volume1/docker/portainer:/data portainer/portainer-ce
      ```
5. click _OK_; then, on the list of scheduled tasks, select the newly created task and hit _Run_; follow the prompts to install Portainer; in the end you can delete the task or keep it – just uncheck the _enabled_ checkbox to disable the task.

6. Portainer should now be acessible in your local network in http://[YOUR-LOCAL-IP]:9000/.

### Step 2: configure Portainer to use your Synology's docker endpoint ###

7. Open Portainer by visiting http://[YOUR-LOCAL-IP]:9000/;
8. Choose and confirm a strong password; you will manage Portainer using this password and the _admin_ username;
9. Select _Docker - Manage the local Docker environment_ to link Portainer to your Synology's local docker endpoint and hit _Connect_; Portainer's admin page should open;
10. Click _Endpoint_ in the left menu, then _local_ and under _Public IP_ place your local NAS IP (it should be the same [YOUR-LOCAL-IP] of step 6.

### Step 3: install Photoprism in your Synology NAS using Portainer, accessible over http / direct IP ###

With Portainer installed we can use a docker-compose file to deploy a stack composed by Photoprism and MariaDB to quickly get Photoprism running in our NAS. We can use [Photoprism's default docker-compose yml file](https://dl.photoprism.org/docker/docker-compose.yml) but we need to make a few cosmetic changes since Portainer only understands docker-compose version 2 syntax in standalone docker hosts.

11. open Synology's File Station app and browse to the _docker_ shared folder;
12. create a folder named _photoprism_ inside _docker_, which will persist relevant Photoprism's data in our local filesystem;
13. inside _photoprism_ folder, create three more folders: _storage_, _originals_ and _database_.
14. Open Portainer by visiting http://[YOUR-LOCAL-IP]:9000/;
15. Click _Stacks_ in the left menu, then _Add stack_, give it a meaningfull name (for eg. Photoprism) and in the Web Editor place the below code, which was based on [Photoprism's default docker-compose yml file](https://dl.photoprism.org/docker/docker-compose.yml) but downgraded to compose version 2. **BE SURE TO USE YOUR OWN [LOCAL-PORT], [YOUR-ADMIN-PASS], [YOUR-DB-PASS] and [YOUR-LOCAL-IP] BY CHANGING THE VALUES ACCORDINGLY, AND CHECK THE LOCAL VOLUMES PATHS TO MATCH THOSE DEFINED IN STEP 13**.

```
version: '2'
services:
  photoprism:
    image: photoprism/photoprism:latest
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
    ports:
      - [LOCAL-PORT]:2342
    environment:
      - PHOTOPRISM_HTTP_PORT=2342
      - PHOTOPRISM_ADMIN_PASSWORD=[YOUR-ADMIN-PASS]
      - PHOTOPRISM_DEBUG=false
      - PHOTOPRISM_PUBLIC=false
      - PHOTOPRISM_READONLY=false
      - PHOTOPRISM_EXPERIMENTAL=true
      - PHOTOPRISM_DISABLE_WEBDAV=false
      - PHOTOPRISM_DISABLE_SETTINGS=false
      - PHOTOPRISM_DISABLE_TENSORFLOW=false
      - PHOTOPRISM_DETECT_NSFW=false
      - PHOTOPRISM_UPLOAD_NSFW=true
      - PHOTOPRISM_DATABASE_DRIVER=mysql
      - PHOTOPRISM_DATABASE_SERVER=mariadb:3306
      - PHOTOPRISM_DATABASE_NAME=photoprism
      - PHOTOPRISM_DATABASE_USER=photoprism
      - PHOTOPRISM_DATABASE_PASSWORD=[YOUR-DB-PASS]
      - PHOTOPRISM_SITE_URL=http://[YOUR-LOCAL-IP]:[LOCAL-PORT]
      - PHOTOPRISM_SITE_TITLE=PhotoPrism
      - PHOTOPRISM_SITE_CAPTION=Browse Your Life
      - PHOTOPRISM_SITE_DESCRIPTION=Photoprism
      - PHOTOPRISM_SITE_AUTHOR=Photoprism
    volumes:
      - /volume1/docker/photoprism/originals:/photoprism/originals
      - /volume1/docker/photoprism/storage:/photoprism/storage  
  mariadb:
    image: mariadb:10.5
    restart: unless-stopped
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
    command: mysqld --transaction-isolation=READ-COMMITTED --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --max-connections=512 --innodb-rollback-on-timeout=OFF --innodb-lock-wait-timeout=50
    volumes:
      - /volume1/docker/photoprism/database:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=[YOUR-DB-PASS]
      - MYSQL_DATABASE=photoprism
      - MYSQL_USER=photoprism
      - MYSQL_PASSWORD=[YOUR-DB-PASS]
```

16. Click _Deploy the stack_. Give it a few minutes and Photoprism should be acessible in http://[YOUR-LOCAL-IP]:[LOCAL-PORT]/.

**IMPORTANT: Synology automaticaly creates thumbnail files inside a special @eaDir directory when you upload media files such as images. To prevent Photoprism to index these files place a .ppignore file with the following content inside docker/photoprism/originals folder:**
```
@eaDir
```

### Step 4 (TO-DO): configure a reverse proxy in your Synology NAS to access Photoprism over https / custom domain name ###

Synology allows you to configure a nginx reverse proxy to serve your applications over HTTPS. Configurations can be made in Diskstation manager _Control Panel_, _Application Portal_, _Reverse proxy_. I was able to make Photoprism work over HTTPS but I am still getting the error:

> PhotoPrism uses WebSockets for two-way interactive communication between your browser and the server
> If the connection fails and can't be reestablished, your browser won't receive photo counts, log messages, or metadata updates.
> To fix this issue, please make sure you didn't block WebSocket connections in your browser or firewall and check the configuration of any Web server that is in front of PhotoPrism.

All help into sorting this out is greatly appreciated!

