# Performance Tips

!!! info ""
    You are welcome to ask for help in our [community chat](https://gitter.im/browseyourlife/community).
    [Sponsors](../../funding.md) receive direct [technical support](https://photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to determine the cause of your problem.

## MariaDB ##

The [InnoDB buffer pool](https://mariadb.com/kb/en/innodb-buffer-pool/) serves as a cache for data and indexes.
It is a key component for optimizing MariaDB performance. Its size should be as large as possible to keep frequently
used data in memory and reduce disk I/O - typically the biggest bottleneck.

Our [docker-compose.yml examples](https://dl.photoprism.app/docker/) have a default buffer pool size of 128 MB. 
You can change it using the `--innodb-buffer-pool-size` parameter (`M` means Megabyte, `G` stands for Gigabyte).
If your server has enough memory, we recommend increasing the size to 1 GB:

```yaml
services:
  mariadb:
    command: mysqld --innodb-buffer-pool-size=1G ...
```

## Storage ##

Local Solid-State Drives (SSDs) are [best for databases](https://mariadb.com/de/resources/blog/how-to-tune-mariadb-write-performance/)
of any kind:

- Database performance extremely benefits from high throughput which HDDs can't provide
- SSDs have more predictable performance and can handle more concurrent requests
- Due to the HDD seek time, HDDs only support 5% of the reads per second of SSDs
- The cost savings from using slow hard disks are minimal

Switching to SSDs makes a big difference, especially for write operations and when the read cache is not
big enough or can't be used.

Never store database files on an unreliable device such as a USB flash drive, an SD card, or a shared network folder.

## Server CPU ##

Last but not least, performance can be limited by your server CPU. While [NAS devices](https://kb.synology.com/en-us/DSM/tutorial/What_kind_of_CPU_does_my_NAS_have)
get faster with each generation, their hardware is optimized for minimal power consumption and low production costs.

[Benchmarks](https://www.google.com/search?q=cpu+benchmarks) prove that even 8-year-old standard desktop
CPUs are often many times faster. If you've tried everything else, then only moving your instance to a more
powerful server may help.

!!! note ""
    If your server runs out of memory, the index is frequently locked, or other system resources are running low
    while indexing, you should [try reducing the number of workers](../config-options.md#index-workers)
    by setting `PHOTOPRISM_WORKERS` to a reasonably small value in `docker-compose.yml` (depending on the performance
    of the server). Also, ensure that [your server has at least 4 GB of swap configured](docker.md#adding-swap) so that
    indexing doesn't cause restarts when there are memory usage spikes. Especially the conversion of RAW images and the
    transcoding of videos are very demanding. As a measure of last resort, you may [disable using TensorFlow](../config-options.md#feature-flags)
    for image classification and facial recognition.