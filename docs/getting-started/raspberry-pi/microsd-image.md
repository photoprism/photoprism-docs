# MicroSD Image for the Raspberry Pi 

![](microsd-image/card.jpg){ class="w25 right" }
The easiest way to run PhotoPrism on a Raspberry Pi is with [PhotoPrismPi](https://dl.photoprism.app/nas/raspberry-pi/).[^1]
Simply flash the image to an SD card and boot your device with it.

We recommend using a fast MicroSD card with at least 64 GB so that you don't run out of storage space later on. These are usually sold with an adapter that fits into normal SD card slots.

## Step 1: Install Imager

With the [Raspberry Pi Imager](https://www.raspberrypi.com/software/), installing the image we provide to a microSD card is quick and easy. The card is then ready to use with your Raspberry Pi.

It is available for Ubuntu, Windows, and macOS, and can be downloaded for free at [raspberrypi.com/software/](https://www.raspberrypi.com/software/).

## Step 2: Download and Flash

After installing [Raspberry Pi Imager](https://www.raspberrypi.com/software/) or another SD card flash tool, you can download the latest version of [PhotoPrismPi](https://dl.photoprism.app/nas/raspberry-pi/) from [dl.photoprism.app/nas/raspberry-pi/latest.img.xz](https://dl.photoprism.app/nas/raspberry-pi/latest.img.xz). 

Then, use the Imager to write the file to an inserted SD card:

![](microsd-image/imager.png)

Once you have selected the downloaded image under "Operating System" and your SD card storage device, click "Next" to begin flashing the image. Depending on the speed of your SD card, this may take a few minutes.

## Step 3: Boot Your Device

Insert the SD card into your Raspberry Pi and ensure that it is connected to a wired network. Then, turn it on. After a few minutes, the operating system will update and download the latest release to your device.[^2]

You should then be able to access the web interface by navigating to `http://<IP address>:2342/` or <https://photoprism-pi.local/>![^3]

### User Accounts

When you first log in to PhotoPrism, the username for the initial super admin account is `admin` and the password is `photoprismpi`.

You can also [connect to the server via SSH](https://www.howtogeek.com/311287/how-to-connect-to-an-ssh-server-from-windows-macos-or-linux/) on standard port 22 using the username `pi` and password `raspberry`.

!!! danger "Danger"
    Since they can be easily guessed, **both passwords should be changed immediately**. This is especially important if your device is connected to the Internet or any other shared network.

### Storage Folders

Your pictures, uploads, sidecar files, and cache files are stored in subfolders of `/opt/photoprism`. You can also connect external drives via USB and access them as folders from `/mnt/a` to `/mnt/d` without further configuration.

Should you want to make changes to the [default settings](../config-options.md), you can find your `compose.yaml` file in `/opt/photoprism`.
After [connecting via SSH](https://www.howtogeek.com/311287/how-to-connect-to-an-ssh-server-from-windows-macos-or-linux/) with the credentials provided above, you can obtain root privileges by running `sudo -i`.

## Running Commands

After [connecting via SSH](https://www.howtogeek.com/311287/how-to-connect-to-an-ssh-server-from-windows-macos-or-linux/), navigate to `/opt/photoprism` to run commands or view logs:

```bash
cd /opt/photoprism
```

Run PhotoPrism commands:

```bash
sudo docker compose exec photoprism photoprism [command]
```

[Learn more ›](../docker-compose.md#command-line-interface)

### Viewing Logs

The following will watch the service logs for troubleshooting:

```bash
sudo docker compose logs -f photoprism
```

[Learn more ›](../troubleshooting/docker.md#viewing-logs)

## Traefik Reverse Proxy

[Traefik](https://traefik.io/traefik) is pre-installed as [a reverse proxy](../proxies/traefik.md) and can be configured in your `/opt/photoprism/compose.yml` file, as well as through the config files located in `/opt/photoprism/traefik`.

[Learn more ›](../proxies/traefik.md)

### Getting Updates

Make sure to use the [latest version tag](https://hub.docker.com/_/traefik) for Traefik in your `compose.yaml` file, e.g.:

```yaml
services:
  traefik:
    image: traefik:v3.6
```

Then run the following command to pull the latest image and restart the service:

```bash
sudo docker compose up -d --pull always
```

This ensures you receive the latest security updates and prevents [errors when upgrading Docker](https://github.com/photoprism/photoprism/discussions/5314) to the latest version.

[Learn more ›](../updates.md)

### Certificate Warnings

Web browsers do not recognize the default TLS certificate as valid, so a warning will appear when connecting over HTTPS.

To avoid this issue, use a valid certificate e.g. obtained for free via Let's Encrypt.

[Learn more ›](../using-https.md)

[^1]: [PhotoPrismPi](https://dl.photoprism.app/nas/raspberry-pi/) is based on [Ubuntu Server](https://cdimage.ubuntu.com/releases/24.04.3/release/).
[^2]: Download and installation time depends on the speed of your Internet connection.
[^3]: If you can't connect, try using the existing hostname or IP address instead.
