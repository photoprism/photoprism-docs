# Running PhotoPrism on a Raspberry Pi

Big thank you to [Guy Sheffer](https://github.com/guysoft) for 
[building](https://github.com/photoprism/photoprism/issues/109) this!

Download our [docker-compose.yml](https://dl.photoprism.org/docker/arm64/docker-compose.yml) file
(right click and *Save Link As...* or use `wget`) to a folder of your choice, 
change the [configuration](config-options.md) as needed, and run `sudo docker-compose up` to start PhotoPrism:

```
wget https://dl.photoprism.org/docker/arm64/docker-compose.yml
sudo docker-compose up
```

See [Setup Using Docker Compose](docker-compose.md) for details.

Image name on Docker Hub: [`photoprism/photoprism-arm64`](https://hub.docker.com/r/photoprism/photoprism-arm64)

## Operating System and Hardware Requirements ##

You need to boot your Raspberry Pi 3 / 4 with the parameter `arm_64bit=1` in `config.txt`
to be able to use this image.
A fast SD card and 4 GB of RAM are recommended, in addition you might want to add swap for large photo collections.

!!! tip
    If you're running out of memory while indexing, it often helps to limit the 
    [number of workers](https://docs.photoprism.org/getting-started/config-options/) by setting
    an explicit value for `PHOTOPRISM_WORKERS` in `docker-compose.yml`.
    Make sure the server has [swap](https://opensource.com/article/18/9/swap-space-linux-systems) 
    configured so that indexing doesn't stop when there are memory usage spikes.
    As a measure of last resort, you can additionally disable image classification using TensorFlow.

Make sure your docker compose configuration contains the following setting:

```
  photoprism:
    security_opt:
      - seccomp:unconfined
```

Alternatively, you can run the image on [UbuntuDockerPi](https://github.com/guysoft/UbuntuDockerPi). It's a 64bit Ubuntu Server with Docker pre-installed.

See also:
https://www.raspberrypi.org/documentation/installation/installing-images/README.md

