# Running PhotoPrism on an Asustor NAS

Before setting up PhotoPrism, we recommend that you visit the [Asustor product database](https://www.asustor.com/en/product/product_list) to learn about the CPU and memory of your NAS device.

For a good user experience, a 64-bit system with [at least 2 cores and 3 GB of physical memory](../index.md#system-requirements) is recommended. Note that RAW image conversion and TensorFlow are disabled on devices with 1 GB or less memory, and that high-resolution panoramic images may require additional swap space and/or physical memory above the recommended minimum.

## Setup

This step-by-step guide explains how to set up a new PhotoPrism instance through App Central, the built-in app store.

### Step 1: Open App Central

Log in to the user interface of your Asustor device by navigating to `https://hostname:7001/` (change hostname and port as needed).

Open "App Central" on the home screen:

![Screenshot](img/asustor/asustor-home.jpg){ class="shadow" }

### Step 2: Install PhotoPrism

Type *PhotoPrism* in the search box in the upper right corner and press Enter to start the search. Now PhotoPrism should be displayed and you should be able to click "Install":

![Screenshot](img/asustor/asustor-step-1.jpg){ class="shadow" }

You will now be informed about dependencies like Docker that need to be installed, and you can decide if you want your instance to be accessible from the Internet (if you have this set up for your device and your Internet router is compatible):

![Screenshot](img/asustor/asustor-step-2.jpg){ class="shadow" }

If you want to [uninstall PhotoPrism](img/asustor/asustor-step-3.jpg) later, you can also do that in App Central.

### Step 3: Open PhotoPrism

Once the installation is complete, you'll find PhotoPrism on your home screen and can open it with a click:

![Screenshot](img/asustor/asustor-step-4.jpg){ class="shadow" }

You can also navigate to port 32770 on your device if you want to open PhotoPrism directly.
When you see the login screen, enter the username "admin" and password "admin321" to sign in:

![Screenshot](img/asustor/asustor-login.jpg){ class="shadow" }

Please remember to change your password after the first login. You can do this under Settings > Account.

The *originals* folder for your original media files is `/share/Docker/PhotoPrism/data`, so you can copy or move your files there.
It is also possible to import files from the shared folder of your NAS.

Our [First Steps 👣](../../user-guide/first-steps.md) tutorial guides you through the user interface and settings to ensure your library is indexed according to your individual preferences.

!!! tldr ""
    Note that the folders that PhotoPrism uses cannot be dynamically configured at the moment when using this app store version. However, we are working to make this possible.
