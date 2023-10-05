# Optimizing Cache Performance

*While we believe this post may be helpful to advanced users, we have not yet reviewed it thoroughly. If you have any suggestions for improvement, please let us know by clicking :material-file-edit-outline: to submit a change request.*

*For advanced users only. This guide is maintained by the community and may contain inaccurate or incomplete advice. You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.*

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
(RAID1) configuration [based on SSD or NVMe drives](../troubleshooting/performance.md#storage) to store the thumbnails. Our
docker script could be:

```
docker run -d \
  --name photoprism \
  -p 2342:2342 \
  -v /tank/photos/:/home/photoprism/Pictures/Originals \
  -v /dozer/cache/:/home/photoprism/.cache/photoprism \
  photoprism/photoprism:latest
```

In a case like this, you will probably also want to optimize the datasets ("file
systems") `tank/photos` and `dozer/cache` further. For instance, the
original photo files will call for a larger recordsize than the smaller cache
files.
