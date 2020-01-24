# Frequently Asked Questions

### Do you support Podman? ###

Podman works just fine both in rootless and under root. Mind the SELinux which is enabled on 
Red Hat compatible systems, you may hit permission error problems. 

More details on on how to run PhotoPrism with [Podman](https://podman.io/) on CentOS in 
[this blog post](https://lukas.zapletalovi.com/2020/01/deploy-photoprism-in-centos-80.html), 
it includes all the details including root and rootless modes, user mapping and SELinux.

### Do you provide LXC images? ###

There is currently no [LXC](https://linuxcontainers.org/) build for
PhotoPrism, see [issue #147](https://github.com/photoprism/photoprism/issues/147) for details.

### Mapping database directory ###

Everytime a container with PhotoPrism is removed, the database is lost. To prevent unwanted reindex process, map the database directory to directory on the host similarly like folder with original photos:

```
docker run -d --name photoprism -p 2342:2342 ... \
  -v /srv/photoprism/db:/home/photoprism/.local/share/photoprism/resources/database \
  photoprism/photoprism:latest
```

!!! info
    Our database schema still changes a lot as we do performance optimizations and add features.
    Therefore we cannot provide a smooth upgrade path and you should be prepared
    to delete your current database and re-index.
    To spare you a disappointment, we kindly advise you not to index large photo 
    collections at the moment.
