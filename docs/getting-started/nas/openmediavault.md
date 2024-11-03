# Running PhotoPrism on OpenMediaVault

!!! tldr ""
    Should you experience problems with the installation, we recommend that you ask the [OpenMediaVault community](https://forum.openmediavault.org/) for advice, as we cannot provide support for third-party software and services. Also note that third-party integrations may not provide direct access to config files or the command line, so you might not be able to use all features and config options.

PhotoPrism can be conveniently installed using the OpenMediaVault [plugin](https://www.openmediavault.org/?p=3146).

![Screenshot](../img/omv_photoprism_plugin_ui.png){ class="shadow" }

## Getting Updates

To upgrade your instance, first connect to the server running OpenMediaVault via SSH or open a terminal from the web interface, then download the newest image from [Docker Hub](https://hub.docker.com/r/photoprism/photoprism/tags) and restart the service:

```bash
sudo podman pull docker.io/photoprism/photoprism:latest
sudo systemctl restart pod-photoprism.service
```

## Opening a Terminal

OpenMediaVault runs PhotoPrism as a containerized service with Podman, which means you can use the [`podman` command](../troubleshooting/docker.md#podman-compose) to open a terminal session.

To do this, first connect to the server running OpenMediaVault via SSH or open a terminal from the web interface and then check if PhotoPrism is running (and if so, under what name):

```bash
sudo podman ps
```

In the output, you should see PhotoPrism running under a name like `photoprism-app`, which you can specify to open a terminal session as follows:

```bash
sudo podman exec -ti photoprism-app /bin/bash
```

You should now be able to run terminal commands, such as those for [managing users](../../user-guide/users/cli.md). Running `photoprism help` will list all commands and [config options](../config-options.md) available in the current version:

```bash
photoprism help
```

Use the `--help` flag to see a detailed command description, for example:

```bash
photoprism backup --help
```

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
