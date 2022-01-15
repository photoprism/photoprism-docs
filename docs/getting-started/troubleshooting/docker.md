# Getting Docker Up and Running

!!! info ""
    You are welcome to ask for help in our [community chat](https://gitter.im/browseyourlife/community).
    [Sponsors](../../funding.md) receive direct [technical support](https://photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to determine the cause of your problem.

### Installation ###

If you can't use the `docker` and `docker-compose` commands at all, make sure [Docker](https://docs.docker.com/config/daemon/#start-the-daemon-manually)
is running on the host you are connected to and your current user has the permission to use it. The following guides explain how to install Docker:

- [Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04), [Mint](https://techviewleo.com/how-to-install-and-use-docker-in-linux-mint/), [Debian](https://www.linode.com/docs/guides/installing-and-using-docker-on-ubuntu-and-debian/), [Arch](https://wiki.archlinux.org/title/docker#Installation), and [Fedora](https://docs.docker.com/engine/install/fedora/) Linux
- [Microsoft Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- [Apple macOS](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

!!! info "Docker Compose"
    Linux distributions may require you to install the `docker-compose` command separately, for example by
    running `sudo apt install docker-compose` in a terminal or using a graphical software package manager.

### Using Docker ###
#### Cannot Connect ####

If you see the error message "Cannot connect to the Docker daemon", it means that Docker is not installed or
not running yet. Before you try anything else, it may help to simply restart your computer.

On many Linux distributions, this command will start the Docker daemon manually if needed:

```bash
sudo systemctl start docker.service
```

On other operating systems, start *Docker Desktop* and enable the "Start Docker Desktop when you log in"
option in its settings.

#### Connection Aborted ####

If you see the error message "Connection aborted" or "Connection denied", it usually means that your
current user does not have permission to use Docker.

On Linux, this command grants permission by adding a user to the `docker` group (relogin for changes to take effect):

```bash
sudo usermod -aG docker [username]
```

Alternatively, you can prefix the `docker` and `docker-compose` commands with `sudo` when not running as root,
for example:

```bash
sudo docker-compose stop
sudo docker-compose up -d
```

Note that this will point the home directory shortcut `~` to `/root` in the `volumes:` section
of your `docker-compose.yml`.

### Viewing Logs ###

Run this command to display the last 100 log messages (omit `--tail=100` to see all):

```bash
docker-compose logs --tail=100
```

To enable [debug mode](../config-options.md), set `PHOTOPRISM_DEBUG` to `true` in the `environment:` section
of the `photoprism` service (or use the `--debug` flag when running the `photoprism` command directly):

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_DEBUG: "true"
```

Then restart all services for the changes to take effect. It can be helpful to keep Docker running in the foreground
while debugging so that log messages are displayed directly. To do this, omit the `-d` parameter when restarting:

```bash
docker-compose stop
docker-compose up 
```

!!! note ""
    If you see no errors or no logs at all, you may have started the server on a different host
    and/or port. There could also be an [issue with your browser](browsers.md), browser plugins, firewall settings,
    or other tools you may have installed.

!!! tldr ""
    The default [Docker Compose](https://docs.docker.com/compose/) config filename is `docker-compose.yml`. For simplicity, it doesn't need to be specified when running the `docker-compose` command in the same directory. Config files for other apps or instances should be placed in separate folders.

### Adding Swap ###

#### Linux ####

Open a terminal and run this command to check if your server has swap configured.

```bash
swapon --show
```

Example output:

```
NAME      TYPE SIZE USED PRIO
/swapfile file  64G  88M   -2
```

This means you have 64 GB of swap and don't need to add more. [Learn how much you need.](https://opensource.com/article/18/9/swap-space-linux-systems)

Otherwise, run these commands to permanently add 4 GB of swap (or more depending on how much physical memory you have):

```bash
sudo -i
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab
```

!!! note ""
    You can skip `sudo -i` if you are already logged in as root.

#### Windows ####

Windows Pro users should [disable](../img/docker-disable-wsl2.jpg) the *WSL 2* based engine in *Docker Settings > General*
so that they can mount drives other than `C:`. This will enable *Hyper-V*, which
[Microsoft doesn't offer](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements)
to its Windows Home customers. [Docker Desktop](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
uses dynamic memory allocation with *WSL 2*.

It is important to explicitly [increase the Docker memory limit](../img/docker-resources-advanced.jpg) to 4 GB or more
when using *Hyper-V*. The default of 2 GB can reduce indexing performance and cause unexpected restarts.
Also, ensure that you configure at least 4 GB of swap space.

#### macOS ####

It is important to [increase the Docker memory limit](../img/docker-resources-advanced.jpg) to 4 GB or more, as the
default of 2 GB can reduce indexing performance and cause unexpected restarts. Also, ensure that you configure
at least 4 GB of swap space.

### Kernel Security ###

We recommend disabling Linux kernel security on private servers, especially if you do not have experience with the
configuration.

!!! info ""
    If you have working configuration rules for a particular Linux distribution, feel free to share instructions
    with the community so that less experienced users can harden their installation without running into issues.

### File Permissions ###

Use a file manager, or the commands `chmod` and `chown` on Unix-like operating systems, to [change file and folder permissions](https://kb.iu.edu/d/abdb)
so that the app container can access them. If you have configured specific user and group IDs, make sure they match.

*Start a full rescan if necessary, for example, if it looks like [thumbnails](index.md#broken-thumbnails) or [pictures are missing](index.md#missing-pictures).*

### Disk Space ###

In case the logs show "disk full", "quota exceeded", or "no space left" errors, either the disk containing the
*storage* folder is full (get a new one or use a different disk) or a disk usage limit is configured, for example
in the Docker, Kubernetes, or Virtual Machine configuration (remove or increase it).

On Linux and other Unix-like operating systems, the [available disk space](https://opensource.com/article/18/7/how-check-free-disk-space-linux)
can be viewed by running `df -h` in a terminal.

If you use *Docker Desktop* on operating systems other than Linux and/or a virtual machine, they have their own
settings to adjust the size of virtual disks and memory. For details, refer to the corresponding documentation.

*Start a full rescan if necessary, for example, if it looks like [thumbnails](index.md#broken-thumbnails) or [pictures are missing](index.md#missing-pictures).*

*[home directory]: \user\username on Windows, /Users/username on macOS, and /root or /home/username on Linux
*[host]: physical computer, cloud server, or virtual machine that runs Docker
*[swap]: substitute for physical memory