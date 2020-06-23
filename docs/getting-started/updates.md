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
You can use [Watchtower](https://github.com/containrrr/watchtower) to automatically update the image which is how our
[public demo](https://demo.photoprism.org/) stays up-to-date:

```docker
services:
  photoprism:
    restart: unless-stopped
    command: photoprism --public start
    image: photoprism/demo:latest
    environment:
      PHOTOPRISM_URL: "https://demo.photoprism.org/"
      PHOTOPRISM_TITLE: "PhotoPrism"
      PHOTOPRISM_SUBTITLE: "Try our demo"
      PHOTOPRISM_DESCRIPTION: "Personal Photo Management"
      PHOTOPRISM_AUTHOR: "PhotoPrism.org"
      PHOTOPRISM_TWITTER: "@browseyourlife"

  watchtower:
    restart: unless-stopped
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

!!! info
    Our database schema still changes a lot as we do performance optimizations and add features.
    Therefore we cannot provide a smooth upgrade path and you should be prepared
    to delete your current database and re-index.
    To spare you a disappointment, we kindly advise you not to index large photo 
    collections at the moment.
