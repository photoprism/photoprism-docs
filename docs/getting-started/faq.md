# Frequently Asked Questions

### I'm having issues understanding the difference between the import and originals folders? ###

Import is a temporary folder from which you can move or copy files to originals in a structured way that avoids duplicates.
Most users with existing collections will want to index their originals directly without importing them, 
so that existing file and directory names stay the same. On the other hand, importing is more efficient when
adding files as you don't need to re-index all originals to find new photos and videos.

### What exactly does read-only mode? ###

There are users who don't want us to modify their original files and folders in any way, so we've added
a configuration option for this use case. It will disable uploads, import and all other features
that might rename or delete files in the originals folder.

### I could not find a good documentation of the config parameters in the docker-compose.yml file? ###

Our example configuration files are continuously maintained and documentation has been added:
https://dl.photoprism.org/docker/docker-compose.yml

Let us know if you're missing something.

### I'm using an operating system without Docker support. How to install and use PhotoPrism without Docker? ###

In general, you would build / install it like a [developer](../developer-guide/setup.md) since we don't have packages 
for specific operating systems yet.

Instead of using Docker, you can manually type the commands listed in our development 
[Dockerfile](https://github.com/photoprism/photoprism/blob/develop/docker/development/Dockerfile) and replace packages with 
what is available in your environment. You often don't need to use the exact same versions for dependencies.

If your operating system has Docker support, we recommend learning Docker as it vastly simplifies installation
and upgrading.

### Do you support Podman? ###

Podman works just fine both in rootless and under root. Mind the SELinux which is enabled on 
Red Hat compatible systems, you may hit permission error problems. 

More details on on how to run PhotoPrism with [Podman](https://podman.io/) on CentOS in 
[this blog post](https://lukas.zapletalovi.com/2020/01/deploy-photoprism-in-centos-80.html), 
it includes all the details including root and rootless modes, user mapping and SELinux.

### Do you provide LXC images? ###

There is currently no [LXC](https://linuxcontainers.org/) build for
PhotoPrism, see [issue #147](https://github.com/photoprism/photoprism/issues/147) for details.
