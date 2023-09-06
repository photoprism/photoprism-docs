# Running PhotoPrism on OpenMediaVault

!!! tldr ""
    Should you experience problems with the installation, we recommend that you ask the [OpenMediaVault community](https://forum.openmediavault.org/) for advice, as we cannot provide support for third-party software and services. Also note that third-party integrations may not provide direct access to config files or the command line, so you might not be able to use all features and config options.

PhotoPrism can be conveniently installed using the OpenMediaVault [plugin](https://www.openmediavault.org/?p=3146).

![Screenshot](../img/omv_photoprism_plugin_ui.png){ class="shadow" }

## Getting Updates

To upgrade your instance, open a terminal, download our newest image from Docker Hub, and then restart the service:

```bash
podman pull docker.io/photoprism/photoprism:latest
systemctl restart pod-photoprism.service
```

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
