# MicroSD Image for the Raspberry Pi 

![](microsd-image/card.jpg){ class="w25 right" }
The easiest way to run PhotoPrism on a Raspberry Pi is with [PhotoPrismPi](https://dl.photoprism.app/dist/photoprismpi/).[^1]
Simply flash the image to an SD card and boot your device with it.

We recommend using a fast MicroSD card with at least 64 GB so that you don't run out of storage space later on. These are usually sold with an adapter that fits into normal SD card slots.

!!! info "Raspberry Pi 5"
    Since our current [MicroSD image](https://dl.photoprism.app/dist/photoprismpi/) is based on Ubuntu 22.04 LTS, it is not yet compatible with the Raspberry Pi 5, which [requires Ubuntu 23.10+](https://ubuntu.com/download/raspberry-pi). As an alternative, you can download [Ubuntu 23.10](https://ubuntu.com/download/raspberry-pi/thank-you?version=23.10&architecture=server-arm64+raspi), install [Docker](../troubleshooting/docker.md#ubuntu-linux), and then follow our regular [Setup Guide](../docker-compose.md).

## Step 1: Install balenaEtcher

Etcher is a powerful OS image flasher that makes flashing an SD card a pleasant and safe experience.  You can download it from the official website or directly from GitHub.

- Homepage: <https://www.balena.io/etcher/>
- Intel / AMD: <https://github.com/balena-io/etcher/releases>
- Apple Silicon: <https://github.com/Augmentedjs/balena-io-etcher-builds/releases>

## Step 2: Flash from URL

Open balenaEtcher and enter the following URL as image source:

```url
https://dl.photoprism.app/dist/photoprismpi/latest.zip
```

![](microsd-image/flash-url.png)

When you have selected the image and inserted a suitable card into your computer, press **Flash!**.

## Step 3: Boot Your Device

Insert the MicroSD card into the Pi, make sure your device is connected to a wired network, and turn it on. After a few minutes,[^2] our latest release should be ready to use when you navigate to <http://photoprismpi.local/>![^3]

### User Accounts

When you first log in to PhotoPrism, the username for the initial super admin account is `admin` and the password is `photoprismpi`.

You can also connect to the server [via SSH](https://www.howtogeek.com/311287/how-to-connect-to-an-ssh-server-from-windows-macos-or-linux/) with the username `ubuntu` and password `ubuntu`.

!!! danger "Danger"
    Since they can be easily guessed, **both passwords should be changed immediately**. This is especially important if your device is connected to the Internet or any other shared network.

### Storage Folders

Uploads, sidecar and cache files are stored in `/opt/photoprism`. External drives can be connected via USB and accessed as folders `/mnt/a` to `/mnt/d` without further configuration.

Should you want to make changes to the [default settings](../config-options.md), you can find the `docker-compose.yml` file in `/boot/firmware/docker-compose/photoprism`.
After [connecting via SSH](https://www.howtogeek.com/311287/how-to-connect-to-an-ssh-server-from-windows-macos-or-linux/) with the credentials provided above, you can obtain root privileges by running `sudo -i`.

### HTTPS Proxy

[Caddy](https://caddyserver.com/docs/) is installed as a [reverse proxy](../proxies/caddy-2.md) that can be configured in `/etc/caddy/Caddyfile`. By default, the automatically generated certificates are not recognized as valid by browsers, so you will see a warning when connecting over HTTPS.

[^1]: [PhotoPrismPi](https://dl.photoprism.app/dist/photoprismpi/) is based on [Ubuntu Server](https://cdimage.ubuntu.com/releases/22.04/release/) and [CustomPiOS](https://github.com/guysoft/CustomPiOS). Special thanks to [Guy Sheffer](https://github.com/guysoft) who helped us build this!
[^2]: Download and installation time depends on the speed of your Internet connection.
[^3]: If you can't connect, try using the existing hostname or IP address instead.
