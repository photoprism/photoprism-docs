# Setting Up PhotoPrism on QNAP

Before setting up PhotoPrism on your NAS, we recommend that you check the [QNAP product database](https://www.qnap.com/en/product) for the CPU and memory configuration of your device.

For a good user experience, it should be a 64-bit system with [at least 2 cores and 3 GB of RAM](../index.md#system-requirements). Indexing large photo and video collections also benefits greatly from [using SSD storage](../troubleshooting/performance.md#storage), especially for the database and cache files.

!!! tldr ""
    Should you experience problems with the installation, we recommend that you ask the QNAP community for advice, as we cannot provide support for third-party software and services.
    Also note that [RAW image conversion and TensorFlow are disabled](../../user-guide/settings/advanced.md) on devices with 1 GB or less memory, and that high-resolution panoramic images may require [additional swap space](../troubleshooting/docker.md#adding-swap) and/or physical memory above the recommended minimum.

## Setup

You can follow this tutorial to install PhotoPrism on QNAP:

↪ <https://safjan.com/install-photoprism-on-qnap-nas-using-docker-compose/>

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-pencil: to send a pull request with your changes.
