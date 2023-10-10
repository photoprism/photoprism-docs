# Getting Docker Up and Running

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://www.photoprism.app/membership) receive direct [technical support](https://www.photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to [determine the cause of your problem](index.md).

## Installation

If you cannot use the `docker` and `docker compose` (or `docker-compose`) commands, make sure [Docker](https://docs.docker.com/config/daemon/#start-the-daemon-manually) is running on the host you are connected to and your current user has permission to use it.
The following instructions explain how to install Docker:

- [Ubuntu](https://docs.docker.com/engine/install/ubuntu/), [Mint](https://techviewleo.com/how-to-install-and-use-docker-in-linux-mint/), [Debian](https://www.linode.com/docs/guides/installing-and-using-docker-on-ubuntu-and-debian/), and [Arch Linux](https://wiki.archlinux.org/title/docker#Installation)
- [Microsoft Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- [Apple macOS](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

### Ubuntu Linux

If you are using Ubuntu Linux, you can run this script to install the latest *Docker* version, including the *Compose Plugin*, on your server in one step:

```bash
bash <(curl -s https://setup.photoprism.app/ubuntu/install-docker.sh)
```

### Docker Compose

The examples in our guides now use the new `docker compose` command by default. However, if your *Docker* version does not yet support the *Compose Plugin*, you can still use the standalone `docker-compose` command.

On some Linux distributions, you may need to install an additional package. To do so, you can use a graphical software package manager or run the following command in a terminal to install the *Compose Plugin* for *Docker* on Ubuntu and Debian:

```bash
sudo apt update
sudo apt install docker-compose-plugin
```

If that does not work, this will install the legacy `docker-compose` command:

```bash
sudo apt update
sudo apt install docker-compose
```

Running the following commands will add a `docker-compose` alias for the new Compose plugin so that older scripts don't break:

```bash
echo 'docker compose "$@"' | sudo tee /bin/docker-compose
sudo chmod +x /bin/docker-compose
```

### Podman Compose

[Podman](https://podman.io/) is supported as a replacement for Docker on **Red Hat-compatible** Linux distributions** like RHEL, CentOS, Fedora, AlmaLinux, and Rocky Linux. The following installs the `podman` and `podman-compose` commands if they are not already installed:

```bash
sudo dnf update -y
sudo dnf install epel-release -y
sudo dnf install netavark aardvark-dns podman podman-docker podman-compose -y
sudo systemctl start podman
sudo systemctl enable podman
podman --version
```

We also provide a setup script that conveniently installs Podman and downloads the default configuration to a directory of your choice:

```bash
mkdir -p /opt/photoprism
cd /opt/photoprism
curl -sSf https://dl.photoprism.app/podman/install.sh | bash
```

!!! note ""
    Please keep in mind to replace the `docker` and `docker compose` commands with `podman` and `podman-compose` when following the examples in our documentation.

## Using Docker
### Cannot Connect

If you see the error message "Cannot connect to the Docker daemon", it means that Docker is not installed or
not running yet. Before you try anything else, it may help to simply restart your computer.

On many Linux distributions, this command will start the Docker daemon manually if needed:

```bash
sudo systemctl start docker.service
```

On other operating systems, start *Docker Desktop* and enable the "Start Docker Desktop when you log in"
option in its settings.

### Connection Aborted

If you see the error message "Connection aborted" or "Connection denied", it usually means that your
current user does not have permission to use Docker.

On Linux, this command grants permission by adding a user to the `docker` group (relogin for changes to take effect):

```bash
sudo usermod -aG docker [username]
```

Alternatively, you can prefix the `docker` and `docker-compose` commands with `sudo` when not running as root,
for example:

```bash
sudo docker compose stop
sudo docker compose up -d
```

Note that this will point the home directory shortcut `~` to `/root` in the `volumes:` section
of your `docker-compose.yml`.

### IPTables Firewall

On Linux, Docker manipulates the `iptables` rules to provide network isolation. This does have some implications for what you need to do if you want to have your own policies in addition to the rules Docker manages.

[Learn more ›](https://docs.docker.com/network/iptables/)

## Viewing Logs

You can run this command to watch the Docker service logs, including the last 100 messages (omit `--tail=100` to see them all, and `-f` to output only the last logs without watching them):

```bash
docker compose logs -f --tail=100 
```

A good way to troubleshoot configuration issues is to increase the log level. To enable [trace log mode](../config-options.md), set `PHOTOPRISM_LOG_LEVEL` to `"trace"` in the `environment:` section of the `photoprism` service (or use the `--trace` flag when running the `photoprism` command directly):


```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_LOG_LEVEL: "trace"
      ...
```

Now [restart all services](../docker-compose.md#step-2-start-the-server) for your changes to take effect:

```bash
docker compose stop
docker compose up -d
```

It can also be helpful to keep Docker running in the foreground while debugging, so that log messages are displayed directly. To do this, omit the `-d` parameter when (re)starting:

```bash
docker compose stop
docker compose up
```

!!! note ""
    If you see no errors or no logs at all, you may have started the server on a different host
    and/or port. There could also be an [issue with your browser](browsers.md), browser plugins, firewall settings,
    or other tools you may have installed.

!!! tldr ""
    The default [Docker Compose](https://docs.docker.com/compose/) config filename is `docker-compose.yml`. For simplicity, it doesn't need to be specified when running `docker compose` or `docker-compose` in the same directory. Config files for other apps or instances should be placed in separate folders.

## Adding Swap

*Note that high-resolution panoramic images may require additional swap space and/or [physical memory](performance.md#memory) above the [recommended minimum](../index.md#system-requirements).*

### Linux

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


### Raspbian 

Open a terminal on your [Raspberry Pi](../raspberry-pi.md) and run the following command to verify if it has swap configured:

```bash
swapon --show
```

Example output:

```
NAME      TYPE SIZE USED PRIO
/swapfile file  100M  0B   -2
```

If no swap has been configured or the command only shows 100 MB, open `/etc/dphys-swapfile` with a text editor, search for `CONF_SWAPSIZE=100` and increase the value to `2048` if your device has 4 GB of physical memory, and `4096` otherwise:

```bash
sudo nano /etc/dphys-swapfile
```

Then restart for the changes to take effect:

```bash
sudo reboot
```

In addition, you can reduce memory usage and improve stability by setting `PHOTOPRISM_WORKERS` to `1` in your `docker-compose.yml` file to limit the number of indexing workers.

### Windows

On Windows Pro, you may need to [disable](../img/docker-disable-wsl2.jpg) the WSL 2-based engine under *Docker Settings > General* 
so that you can mount drives other than `C:` This will enable *Hyper-V*, which
[Microsoft doesn't offer](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements)
to its Windows Home customers. [Docker Desktop](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
uses dynamic memory allocation with *WSL 2*.

It is important to explicitly [increase the Docker memory limit](../img/docker-resources-advanced.jpg) to 4 GB or more
when using *Hyper-V*. The default of 2 GB can reduce indexing performance and cause unexpected restarts.
Also, ensure that you configure at least 4 GB of swap space.

### macOS

It is important to [increase the Docker memory limit](../img/docker-resources-advanced.jpg) to 4 GB or more, as the
default of 2 GB can reduce indexing performance and cause unexpected restarts. Also, ensure that you configure
at least 4 GB of swap space.

## Kernel Security

We recommend disabling Linux kernel security modules like *SELinux* (Red Hat/Fedora) on private servers, especially if you have no experience configuring them.

If you have working configuration rules for a particular Linux distribution, feel free to share the instructions with the community so that less experienced users can harden their installation without running into problems.

## File Permissions

Errors such as "read-only file system", "error creating path", or "wrong permissions" indicate a filesystem permission problem:

- [ ] Use a file manager, or the commands `ls -alh`, `chmod`, and `chown` on Unix-like operating systems, to [check and change filesystem permissions](https://kb.iu.edu/d/abdb) so all files and folders are accessible
- [ ] The app and database *storage* folders must be writable as well: Verify that the services have write permissions and that you have **not** mounted the folders read-only on your host or [via Docker using the `:ro` flag](https://docs.docker.com/compose/compose-file/compose-file-v3/#short-syntax-3)
- [ ] If you have configured specific user and group IDs for a service, make sure they match
- [ ] If [symbolic links](https://en.wikipedia.org/wiki/Symbolic_link) are mounted or used within *storage* folders, replace them with actual paths
- [ ] It may help to [add the `:z` mount flag to volumes](https://docs.docker.com/storage/bind-mounts/#configure-the-selinux-label) when using *SELinux* (Red Hat/Fedora)
- [ ] When mounting folders that only root has access to, you may have to prefix the `docker` and `docker-compose` commands with `sudo` on Linux if you are not already logged in as root

An easy way to test for missing permissions is to (temporarily) remove restrictions and make the entire folder accessible to everyone:

```bash
sudo chmod -R a+rwx [folder]
```
*Start a full rescan once all issues have been resolved, especially if it looks like [thumbnails](index.md#broken-thumbnails) or [pictures are missing](index.md#missing-pictures).*

!!! danger ""
    **Be very careful when changing permissions in shared hosting environments.** If you are using PhotoPrism on corporate
    or university servers, we recommend that you ask your IT help desk for advice.

## Overlay Volumes

Depending on overlay file system support, it is possible to mount additional host folders as sub folders of `/photoprism/originals` (or other storage folders), for example:

```yaml
volumes:
  - "/home/username/Pictures:/photoprism/originals"
  - "/example/friends:/photoprism/originals/friends"
  - "/mnt/photos:/photoprism/originals/media"
```

For this to work, you should have the `cgroupfs-mount` package installed, as shown in the [installation script we provide](https://github.com/photoprism/photoprism/blob/develop/scripts/dist/install-docker.sh).
You may otherwise find that files added to the mounted folders are not visible on the host, and data loss may occur.

!!! note ""
    We recommend that you start with a simple configuration without overlay volume mounts or path placeholders like `~`, and only move on to a more complex setup once this works.

## Disk Space

In case the logs show "disk full", "quota exceeded", or "no space left" errors, either the disk containing the
*storage* folder is full (get a new one or use a different disk) or a disk usage limit is configured, for example
in the Docker, Kubernetes, or Virtual Machine configuration (remove or increase it):

- on Linux and other Unix-like operating systems, the [available disk space](https://opensource.com/article/18/7/how-check-free-disk-space-linux) can be viewed by running `df -h` in a terminal
- if you are using *Kubernetes*, *Docker Desktop*, *Hyper-V*, or a Virtual Machine, they have their own settings to adjust the size of [storage](../docker-compose.md#volumes), [RAM](../index.md#system-requirements), and [swap](#adding-swap)
- for details, refer to the corresponding documentation

*Start a full rescan if necessary, for example, if it looks like [thumbnails](index.md#broken-thumbnails) or [pictures are missing](index.md#missing-pictures).*

## Network Storage

Shared folders that have already been mounted on your host can be mounted like any local drive or directory.
Alternatively, you can mount network storage with [Docker Compose](https://docs.docker.com/compose/compose-file/compose-file-v3/#driver_opts).
Please never store database files on an unreliable device such as a USB stick, SD card, or network drive.

### Unix / NFS

Follow this `docker-compose.yml` example to mount Network File System (NFS) shares e.g. from Unix servers or NAS devices:

```yaml
services:
  photoprism:
    # ...
    volumes:
      # Map named volume "originals"
      # to "/photoprism/originals":
      - "originals:/photoprism/originals"     
  mariadb:
    # ...

# Specify named volumes:
volumes:
  originals:
    driver_opts:
      type: nfs
      # Authentication and other mounting options:
      o: "addr=1.2.3.4,username=user,password=secret,soft,rw,nfsvers=4"
      # Mount this path:
      device: ":/mnt/example"
```

`device` should contain the path to the share on the NFS server, note the `:` at the beginning. In the above example, the share can be mounted as the named volume `originals`. You can also choose another name as long as it is consistent.

Driver-specific options can be set after the server address in `o`, see the [nfs manual page](https://man7.org/linux/man-pages/man5/nfs.5.html). Here are some examples of commonly used options:

- `nfsvers=3` or `nfsvers=4` to specify the NFS version
- `nolock` (optional): Remote applications on the NFS server are not affected by lock files inside the Docker container (only other processes inside the container are affected by locks)
- `timeo=n` (optional, default 600): The NFS client waits `n` tenths of a second before retrying an NFS request
- `soft` (optional): The NFS client aborts an NFS request after `retrans=n` unsuccessful retries, otherwise it retries indefinitely
- `retrans=n` (optional, default 2): Sets the number of retries for NFS requests, only relevant when using `soft`

### SMB / CIFS

Follow this `docker-compose.yml` example to mount [CIFS network shares](https://en.wikipedia.org/wiki/Server_Message_Block), e.g. **from Windows**, NAS devices or Linux servers with [Samba](https://www.samba.org/):

```yaml
services:
  photoprism:
    # ...
    volumes:
      # Map named volume "originals"
      # to "/photoprism/originals":
      - "originals:/photoprism/originals"     
  mariadb:
    # ...

# Specify named volumes:
volumes:
  originals:
    driver_opts:
      type: cifs
      o: "username=user,password=secret,rw"
      device: "//host/folder"
```

Then restart all services for the changes to take effect. Note that related values must start at the same indentation level [in YAML](../../developer-guide/technologies/yaml.md) and that **tabs are not allowed for indentation**. We recommend using 2 spaces, but any number will do as long as it is consistent.

!!! info ""
    **We kindly ask you not to report bugs via *GitHub Issues* unless you are certain to have found a fully reproducible and previously unreported issue that must be fixed directly in the app.**
    [Ask for technical support](../../user-guide/index.md#getting-support) if you need help, it could be a local
    configuration problem, or a misunderstanding in how the software works.

*[home directory]: \user\username on Windows, /Users/username on macOS, and /root or /home/username on Linux
*[host]: Computer, Cloud Server, or VM that runs PhotoPrism
*[swap]: substitute for physical memory
*[read-only]: write protected
*[filesystem]: contains your files and folders
*[RHEL]: Red Hat Enterprise Linux®