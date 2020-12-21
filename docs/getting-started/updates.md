# Getting Updates

Open a terminal and run the following command to pull the latest container image:

```
docker pull photoprism/photoprism:latest
```

For our Raspberry Pi version:

```
docker pull photoprism/photoprism-arm64:latest
```

Pulling a new version can take several minutes, depending on your internet connection.
You can use [Watchtower](https://github.com/containrrr/watchtower) to automatically keep images up-to-date:

```docker
services:
  watchtower:
  image: containrrr/watchtower
  restart: unless-stopped
  volumes:
    - "/var/run/docker.sock:/var/run/docker.sock"
```