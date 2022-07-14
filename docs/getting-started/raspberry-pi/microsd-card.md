# MicroSD Image for the Raspberry Pi 

The easiest way to run PhotoPrism on a Raspberry Pi is with [PhotoPrismPi](https://dl.photoprism.app/raspberrypi/).[^1]
Simply flash the image to an SD card and boot your device with it.

## Step 1: Install balenaEtcher

Etcher is a powerful OS image flasher that makes flashing an SD card a pleasant and safe experience. You can download it from the official website or GitHub:

- <https://www.balena.io/etcher/>
- <https://github.com/balena-io/etcher/releases>

## Step 2: Flash from URL

Open balenaEtcher and enter the following URL as image source:

```url
https://dl.photoprism.app/raspberry-pi/microsd-card.zip
```

![](microsd-card/flash-from-url.png)

When you have selected the image and inserted a suitable card into your computer, press **Flash!**.

We recommend using a fast MicroSD card with at least 16 GB. These are usually sold with an adapter that fits into normal SD card slots.

## Step 3: Boot Your Device

Insert the MicroSD card into the Pi, make sure your device is connected to a wired network, and turn it on. After a few minutes,[^2] our latest release should be ready to use when you navigate to `http://photoprismpi.local/` (or the IP address, depending on your local network)!

External drives can be connected via USB and accessed as folders `/mnt/a` to `/mnt/d`.

!!! note ""
    The default password for the `admin` user is `photoprismpi`. You can also connect via SSH with the user and password `ubuntu`. Be sure to change both passwords immediately if your Pi is connected to a public network.

[^1]: A big thank you to [Guy Sheffer](https://github.com/guysoft) for helping us [build](https://github.com/photoprism/photoprism/issues/109) a Raspberry Pi version!
[^2]: Installation time depends on the download speed of your internet connection.
[^3]: You may need to use the existing hostname (if any) or IP address instead.