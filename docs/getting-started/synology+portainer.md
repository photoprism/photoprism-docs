# Setup Using Synology NAS and Portainer

This guide will help you install Photoprism in your Synology NAS using [Portainer](https://www.portainer.io/), an open-source container manager system. The guide will cover the following steps:

- install Portainer in your Synology NAS using Task Manager;
- install Photoprism in your Synology NAS using Portainer, accessible over http / direct IP;
- configure a reverse proxy in your Synology NAS to access Photoprism over https / custom domain name.

### Step 1: install Portainer in your Synology NAS using Task Manager ###

Synology's official docker app is quite limited in terms of functionality and that is the reason why we will install Portainer first. It will make managing docker containers inside Synology much more easier and functional while sharing the same local docker endpoint (i.e. the same docker images / containers / volumes / etc. will be manageable in both Synology's app and Portainer). With Portainer we will use a docker-compose file to deploy a stack composed by Photoprism and MariaDB to quickly get Photoprism running in our NAS.



### Step 2: install Photoprism in your Synology NAS using Portainer, accessible over http / direct IP ###




### Step 3 (TO-DO): configure a reverse proxy in your Synology NAS to access Photoprism over https / custom domain name ###
