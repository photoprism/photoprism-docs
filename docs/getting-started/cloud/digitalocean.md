# Using our DigitalOcean 1-Click App #

PhotoPrism can be deployed at DigitalOcean with just a few clicks.
If you have no DigitalOcean account yet, you may use this sign-up link to receive a $100, 60-day account credit:

<p style="text-align: center; padding: 10px 4px 5px 4px;">
<a class="md-button shadow" style="background-color: #0052ff; font-size: 0.66rem; font-weight: normal; color: white" href="https://m.do.co/c/f9725a28bb6b">Sign up at DigitalOcean</a>
</p>

## Install PhotoPrism ##

- [Sign Up](https://m.do.co/c/f9725a28bb6b) or [Log In](https://cloud.digitalocean.com/login) at DigitalOcean
- Open the [PhotoPrism listing](https://marketplace.digitalocean.com/apps/photoprism) in the marketplace
- Click *Create PhotoPrism Droplet*

![Screenshot](img/create-photoprism-droplet.png){ class="shadow indent" }

### Configure Your Droplet ###
#### Choose an Image ####

The PhotoPrism image will be pre-selected

![Screenshot](img/1-do-setup.png){ class="shadow indent" }

#### Choose a Plan ####

We recommend hosting PhotoPrism on a server with at least 2 cores and 3 GB of physical memory. Indexing and searching can be slow on smaller Droplets, depending on how many and what types of files you upload.

!!! info ""
    While PhotoPrism has been reported to work on Droplets with less memory, we take no responsibility for instability or performance problems. RAW image conversion and TensorFlow are disabled on Droplets with 1 GB or less memory.

![Screenshot](img/2-do-setup.png){ class="shadow indent" }

#### Choose a Datacenter Region ####

![Screenshot](img/3-do-setup.png){ class="shadow indent" }

![Screenshot](img/4-do-setup.png){ class="shadow indent" }

#### Choose an Authentication Mode ####

![Screenshot](img/5-do-setup.png){ class="shadow indent" }

#### Finalize Your Droplet ####

Finalize your droplet and click *Create Droplet*
![Screenshot](img/6-do-setup-edited.png){ class="shadow indent" }

![Screenshot](img/7-do-setup.png){ class="shadow indent" }

Your droplet is now being created.

## Admin Password ##

- Click *More*

![Screenshot](img/do-more-options-edited.png){ class="shadow indent" }

- Click *Access console*

![Screenshot](img/do-access-console-edited.png){ class="shadow indent" }

- Launch the console as root

![Screenshot](img/do-launch-droplet-console.png){ class="shadow indent" }

- Within the console type ```cat /root/.initial-password.txt``` and click enter
- Copy your initial password

## Open PhotoPrism ##

- Click *Get started*

![Screenshot](img/do-get-started-edited.png){ class="shadow indent" }

- Click *Quick access*

![Screenshot](img/do-quick-access.png){ class="shadow indent" }

!!!info
    In case you have no domain and let's encrypt set up you will see the notice "Your connection is not private". 
    Click *Advanced* and click *Open page*.

- Use username "admin" and your initial password to sign in
- You may [change your password](../../user-guide/settings/account.md) using the Web UI

## Setting Up Your Devices

1. [Choose](../../user-guide/library/index.md) whether you want to [index your originals](../../user-guide/library/originals.md) so that the existing file and folder names are preserved, or [import them](../../user-guide/library/import.md) so that they are automatically organized by year and month.
2. To add pictures, you can either copy them to the *import* or *originals* folder using [WebDAV](../../user-guide/sync/webdav.md), or [upload them](../../user-guide/library/upload.md) with the web user interface, which will import them automatically after upload.
3. Finally, set up [automatic syncing](../../user-guide/sync/mobile-devices.md) from your mobile phone and install the [Progressive Web App (PWA)](../../user-guide/pwa.md) on your desktop, tablet, and phone home screens as needed.


