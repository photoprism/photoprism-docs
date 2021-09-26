# Running PhotoPrism on a Raspberry Pi

Our latest release comes as a single [multi-arch image](https://hub.docker.com/r/photoprism/photoprism) 
for AMD64, ARM64, and ARMv7. If your device meets the system requirements, 
the same [installation instructions](docker-compose.md) as for regular Linux servers apply.

### System Requirements ###

It's important to [boot](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
your Raspberry Pi 3 / 4 with the parameter `arm_64bit=1` in `config.txt` in order to use our Docker image.
Alternatively, you may run the image on [UbuntuDockerPi](https://github.com/guysoft/UbuntuDockerPi).
It's a 64bit Ubuntu Server with Docker pre-installed.

Your device should have at least 4 GB of memory. Also make sure it has at least
4 GB of [swap](https://opensource.com/article/18/9/swap-space-linux-systems)
configured, so that indexing doesn't cause restarts when there are memory usage spikes.

Indexing large photo and video collections significantly benefits from fast, local SSD storage,
and lots of memory for caching. Especially the conversion of RAW images and the transcoding of
videos are very demanding.

To avoid permission issues, your [docker-compose.yml](https://dl.photoprism.org/docker/arm64/docker-compose.yml) 
should include the following security options:

```yaml
  photoprism:
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
```

Big thank you to [Guy Sheffer](https://github.com/guysoft) for
[building](https://github.com/photoprism/photoprism/issues/109) this!

!!! info "Reducing Server Load"
    If you're running out of memory - or other system resources - while indexing, please limit the
    [number of workers](https://docs.photoprism.org/getting-started/config-options/) by setting
    `PHOTOPRISM_WORKERS` to a value less than the number of logical CPU cores in `docker-compose.yml`.
    As a measure of last resort, you may disable using TensorFlow for image classification and facial recognition.
