# **PikaPods** Open Source App Hosting

!!! verified "Trusted Partner"
    [PikaPods](https://prism.ws/pikapods-com) has partnered with us to offer you this **officially supported, cloud-hosted solution**.[^1] Your personal app instance is ready to use in just a few steps and [includes sponsor features](https://photoprism.app/editions#compare) like premium themes and high-resolution world maps - at no additional cost! New customers also receive a $5 welcome credit.

## Setup

This step-by-step guide explains how to set up a new PhotoPrism instance at PikaPods.

### 1. Create Account

Sign up at [www.pikapods.com/register](https://prism.ws/pikapods-register) with your contact details.
You will then receive a confirmation email with an activation link that you must click to continue.

Before proceeding, we recommend that you enter your credit card information first to avoid usage restrictions.

### 2. Start PhotoPrism

Go to [Available Apps](https://prism.ws/pikapods-apps) and select PhotoPrism, then click *Run Your Own*:

![Screenshot](img/pikapods-appstore.png)

Enter a Pod Name and select a Region:

![Screenshot](img/pikapods-step-1.png){ class="shadow" }

Click *ENV VARS* to specify the initial password for the "admin" user account:

![Screenshot](img/pikapods-step-2.png){ class="shadow" }

In *RESOURCES*, you can configure the storage space available for photos and videos, as well as the compute resources PhotoPrism can use, such as for indexing and face recognition.

!!! info ""
    PhotoPrism currently requires **at least 2 CPUs and 8 GB of memory**. We are working to lower these minimum requirements.

The approximate price per month is shown at the bottom:

![Screenshot](img/pikapods-step-3.png){ class="shadow" }

Finally, click *Add Pod* to complete the setup.

### 3. Add Your Files

PhotoPrism is now fully set up and ready to use. To log in, click *Open Pod*, enter the username "admin" and the password you have specified:

![Screenshot](img/pikapods-overview.png)

If you want to change your password, you can do so in [Settings > Account](../../user-guide/settings/account.md#change-password).
Our [First Steps 👣](../../user-guide/first-steps.md) tutorial will guide you through the user interface and settings to ensure your library is indexed according to your individual preferences.

[^1]: A share of the revenue [helps fund the development](https://photoprism.app/kb/oss) and maintenance of PhotoPrism
