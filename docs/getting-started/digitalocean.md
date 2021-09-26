# Using our DigitalOcean 1-Click App #

PhotoPrism can be deployed at DigitalOcean with just a few clicks.
If you have no DigitalOcean account yet, you may use this sign-up link to receive a $100, 60-day account credit:

<p style="text-align: center; padding: 10px 4px 5px 4px;">
<a class="md-button" style="background-color: #0052ff; font-size: 0.66rem; font-weight: normal; color: white" href="https://m.do.co/c/ca260247b5c2">Sign up at DigitalOcean</a>
</p>

## Install PhotoPrism ##

- [Sign Up](https://m.do.co/c/ca260247b5c2) or [Log In](https://cloud.digitalocean.com/login) at DigitalOcean
- Open the [PhotoPrism listing](https://marketplace.digitalocean.com/apps/photoprism) in the marketplace
- Click *Create PhotoPrism Droplet*

![Screenshot](img/create-photoprism-droplet.png)

### Configure Your Droplet ###
#### Choose an image ####

The PhotoPrism image will be pre-selected

![Screenshot](img/1-do-setup.png)

#### Choose a plan ####

We recommend hosting PhotoPrism on a server with at least 2 cores and 4 GB of memory. 
Indexing and searching may be slow on smaller Droplets, depending on how many and what types of files you upload.

![Screenshot](img/2-do-setup.png)

#### Choose a datacenter region ####

![Screenshot](img/3-do-setup.png)

![Screenshot](img/4-do-setup.png)

#### Choose an authentication mode ####

![Screenshot](img/5-do-setup.png)

#### Finalize your droplet ####

Finalize your droplet and click *Create Droplet*
![Screenshot](img/6-do-setup-edited.png)

![Screenshot](img/7-do-setup.png)

Your droplet is now being created.

## Admin Password ##

- Click *More*

![Screenshot](img/do-more-options-edited.png)

- Click *Access console*

![Screenshot](img/do-access-console-edited.png)

- Launch the console as root

![Screenshot](img/do-launch-droplet-console.png)

- Within the console type ```cat /root/.initial-password.txt``` and click enter
- Copy your initial password

## Open PhotoPrism ##

- Click *Get started*

![Screenshot](img/do-get-started-edited.png)

- Click *Quick access*

![Screenshot](img/do-quick-access.png)

!!!info
    In case you have no domain and let's encrypt set up you will see the notice "Your connection is not private". 
    Click *Advanced* and click *Open page*.

- Use username "admin" and your initial password to sign in
- You may [change your password](../user-guide/settings/account.md) using the Web UI

## Adding Files ##

- Decide whether you want to [index or import your files](../user-guide/library/index.md)
- [Add files to your import or originals folder via WebDAV](../user-guide/library/webdav.md), or upload via [Web UI](../user-guide/library/upload.md)
- Set up [syncing automatically](../user-guide/sync/mobile-devices.md) from mobile devices

