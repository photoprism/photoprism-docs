# Frequently Asked Questions

### PhotoPrism does not work, what can I do? ###

If the application can not be opened in the browser or the container doesn't start at all, you might have found a bug,
you might be using an outdated container image or your folder is not readable (check permissions).

You're welcome to send a full report to help@photoprism.org so that we can assist you.

### Do you support Podman? ###

Currently, we have no experience with using [Podman](https://podman.io/) instead
of Docker. Please let us know if you do.

### Do you provide LXC images? ###

There is currently no [LXC](https://linuxcontainers.org/) build for
PhotoPrism, see [issue #147](https://github.com/photoprism/photoprism/issues/147) for details.

### How can I optimize caching for performance? ###

Some users might want to place the thumbnail cache on a separate, faster file
system while keeping the actual photo files on large, slow bulk storage. This
should result in faster access to the thumbnails. 

To do this, we add a further volume (`-v`) parameter to the docker script so we
use an _external_ path (outside the container) for the cache files. You can get
the _internal_ path with `photoprism config`, or as a docker command in a
running system (for Linux/BSD systems): 

```
sudo docker exec photoprism photoprism config | grep cache-path
```

This should return a line such as:

```
cache-path            /home/photoprism/.cache/photoprism
```

for the internal path. We now know to add a line like

```
  -v <MYCACHE_FOLDER>:/home/photoprism/.cache/photoprism \
```

to the docker invocation, with your actual path to the cache folder replacing
`<MYCACHE_FOLDER>`. 

As an example, let's assume a [ZFS
filesystem](https://en.wikipedia.org/wiki/ZFS) with two pools ("volumes" in
classical terminology): A pool _tank_ in a raidz2 (RAID6) configuration based on
hard drives that holds the original pictures, and a pool _dozer_ in a mirrored
(RAID1) configuration based on SSD or NVMe drives to store the thumbnails. Our
docker script could be:

```
docker run -d \
  --name photoprism \
  -p 2342:2342 \
  -v /tank/photos/:/home/photoprism/Pictures/Originals \
  -v /dozer/cache/:/home/photoprism/.cache/photoprism \
  photoprism/photoprism
```

In a case like this, you will probably also want to optimize the datasets ("file
systems") `tank/photos` and `dozer/cache` further. For instance, the
original photo files will call for a larger recordsize than the smaller cache
files.
