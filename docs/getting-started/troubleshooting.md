# Troubleshooting Installation Problems

!!! info ""
    You're welcome to ask for help in our [community chat](https://gitter.im/browseyourlife/community).
    [Sponsors](../funding.md) receive direct [technical support](https://photoprism.app/contact) via email.

### Installing and Using Docker ###

If you can't use the `docker` and `docker-compose` commands at all, make sure [Docker](https://docs.docker.com/config/daemon/#start-the-daemon-manually)
is running on the host you are connected to and your current user has the permission to use it. The following guides explain how to install Docker:

- [Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04), [Mint](https://techviewleo.com/how-to-install-and-use-docker-in-linux-mint/), [Debian](https://www.linode.com/docs/guides/installing-and-using-docker-on-ubuntu-and-debian/), [Arch](https://wiki.archlinux.org/title/docker#Installation), and [Fedora](https://docs.docker.com/engine/install/fedora/) Linux
- [Microsoft Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- [Apple macOS](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

!!! info "Docker Compose"
    Linux distributions may require you to install the `docker-compose` command separately, for example by
    running `sudo apt install docker-compose` in a terminal or using a graphical software package manager.

#### Cannot Connect ####

If you see the error message "Cannot connect to the Docker daemon", it means that Docker is not installed or 
not running yet. Before you try anything else, it may help to simply restart your computer.

On many Linux distributions, this command will start the Docker daemon manually if needed:

```bash
sudo systemctl start docker.service
```

On other operating systems, start Docker Desktop and enable the "Start Docker Desktop when you log in" 
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

Note that this will point the home directory placeholder `~` to `/root` in the `volumes:` section 
of your `docker-compose.yml`.

### Docker Compose Logs ###

If you cannot connect to the Web UI even after waiting a few minutes, run this command to display
the last 100 log messages (omit `--tail=100` to see all):

```bash
docker-compose logs --tail=100
```

Check them for messages like *disk full*, *wrong permissions*, *no route to host*, *connection failed*, and *killed*
before reporting a bug. If a service has been killed or otherwise automatically terminated, this points to a memory problem.

Should MariaDB get stuck in a restart loop and PhotoPrism can't connect to it, this indicates a memory, filesystem,
or permission issue:

```
mariadb: mysqld: ready for connections.
mariadb: mysqld (initiated by: unknown): Normal shutdown
photoprism: dial tcp 172.18.0.2:3306: connect: no route to host
mariadb: mysqld: Shutdown complete
```

We recommend going through the [checklist for fatal server errors](#fatal-server-errors) and to verify that
your computer meets the [system requirements](index.md#system-requirements).

!!! tldr ""
    The default [Docker Compose](https://docs.docker.com/compose/) config filename is `docker-compose.yml`. For simplicity, it doesn't need to be specified when running the `docker-compose` command in the same directory. Config files for other apps or instances should be placed in separate folders.

!!! note ""
    If you see no errors or no logs at all, you may have started the server on a different host
    and/or port. There could also be an issue with your browser, ad blocker, or firewall settings.

You can also try (re-)starting the app and database without `-d`. This keeps their containers running
in the foreground and shows log messages for troubleshooting:

```bash
docker-compose stop
docker-compose up 
```

To enable [debug mode](config-options.md), add this to the environment variables of the `photoprism`
service in your `docker-compose.yml` and restart for changes to take effect:

```
PHOTOPRISM_DEBUG: "true"
```

### Checklists ###

#### Missing Pictures ####

If you have indexed your library and some images or videos are missing, first check *Library > Errors*
for errors and warnings. In case the application logs don't contain anything helpful:

- [ ] The pictures are in [Review](../user-guide/organize/review.md) due to low quality or incomplete metadata
- [ ] The [file type](faq.md#which-file-types-are-supported) is generally unsupported
- [ ] The [file type](faq.md#which-file-types-are-supported) is generally supported, but a specific feature or codec is not
- [ ] The files have bad filesystem permissions, so they can't be opened by the indexer
- [ ] The indexer has skipped the files because they are exact duplicates
- [ ] They are in *Library > Hidden* because thumbnails could not be created:
    - [ ] *Convert to JPEG* is disabled in *Settings > Library*
    - [ ] FFmpeg and/or RAW converters are disabled in *Settings > Advanced*
    - [ ] The file is broken and cannot be opened
    - [ ] The sidecar and/or cache folders are not writable
- [ ] Multiple files were [stacked](../user-guide/organize/stacks.md#for-what-reasons-can-files-be-stacked) based on their metadata or file names
- [ ] The [private](../user-guide/organize/private.md) or [archived](../user-guide/organize/archive.md) status was restored from a backup
- [ ] The NSFW (Not Safe For Work) filter is enabled, so they were marked as [private](../user-guide/organize/private.md)
- [ ] You are not signed in as admin, so you can't see everything
- [ ] You try to index a shared drive on a remote server, but the server is offline
- [ ] The indexer has crashed because you didn't configure at least 4 GB of swap
- [ ] Somebody has deleted files without telling you
- [ ] You are connected to the wrong server or CDN, or a DNS record has not been updated yet

#### Broken Thumbnails ####

If some pictures have broken or missing thumbnails, first check *Library > Errors* for errors and warnings.
In case the application logs don't contain anything helpful:

- [ ] The issue can be resolved by reloading the page or clearing the browser cache
- [ ] You browse [non-JPEG](faq.md#which-file-types-are-supported) files in *Library > Originals* which have an icon but no preview
- [ ] *Dynamic Previews* are enabled in *Settings > Advanced*, but the server is not powerful enough
- [ ] The sizes in *Settings > Advanced* have been changed so the request can't be fulfilled
- [ ] FFmpeg and/or RAW converters are disabled in *Settings > Advanced*
- [ ] *Convert to JPEG* is disabled in *Settings > Library*
- [ ] Your (virtual) server disk is full
- [ ] Your sidecar and/or cache folders are not writable (anymore)
- [ ] Files were deleted manually, for example to free up disk space
- [ ] Files can't be opened, e.g. because the file system permissions have been changed
- [ ] Files are stored on an unreliable device such as a USB flash drive or a shared network folder
- [ ] Some thumbnails could not be created because you didn't configure at least 4 GB of swap
- [ ] The user interface can't communicate properly with your server, for example, because a proxy is misconfigured (check its config and try without a proxy)
- [ ] Your proxy, router, or firewall has a request rate limit, so some requests fail
- [ ] There are other network problems caused by a firewall, router, or unstable connection
- [ ] An ad blocker blocks requests (disable it or add an exception)
- [ ] You are connected to the wrong server or CDN, or a DNS record has not been updated yet

We also recommend checking your Docker logs for messages like *disk full*, *wrong permissions*, and *killed* as
described above. If a service has been killed or otherwise automatically terminated, this points to a memory problem.

#### Videos Don't Play ####

If videos do not play and/or you only see a white/black area when you open a video:

- [ ] You are using an [incompatible browser](index.md#browsers), e.g. without AVC support (try another browser)
- [ ] AVC support or related JavaScript features have been disabled in your browser (check the settings and try another browser)
- [ ] It is a large non-AVC video that needs to be transcoded first (wait or pre-transcode with the [convert command](http://localhost:8000/getting-started/docker-compose/#command-line-interface))
- [ ] An ad blocker blocks requests (disable it or add an exception)
- [ ] Files are stored on an unreliable device such as a USB flash drive or a shared network folder (check if the files are accessible)
- [ ] There are network problems caused by a proxy, firewall, or unstable connection (try a direct connection)
- [ ] You are connected to the wrong server or CDN, or a DNS record has not been updated yet

We also recommend checking your logs as described above.

#### App Not Loading ####

If you only see the logo when you navigate to the server URL and nothing else happens, even if you wait a moment:

- [ ] The user interface can't communicate properly with your server, for example, because a proxy is misconfigured (check its config and try without a proxy)
- [ ] JavaScript is disabled in your browser settings (enable it)
- [ ] JavaScript was disabled by a browser plugin (disable it or add an exception)
- [ ] An ad blocker blocks requests (disable it or add an exception)
- [ ] You are using an [incompatible browser](index.md#browsers) (try another browser)
- [ ] There is a problem with your network connection (test if other sites work)

#### Fatal Server Errors ####

Fatal errors are often caused by one of the following conditions:

- [ ] Your (virtual) server disk is full
- [ ] There is disk space left, but the [inode limit](https://serverfault.com/questions/104986/what-is-the-maximum-number-of-files-a-file-system-can-contain) has been reached
- [ ] The storage folder is not writable or there are other filesystem permission issues
- [ ] You have accidentally mounted the wrong folders
- [ ] The server is low on memory
- [ ] You didn't configure at least 4 GB of swap
- [ ] The server CPU is overheating
- [ ] The server has an outdated operating system that is not fully compatible
- [ ] The database server is not available, [incompatible](index.md#databases), or incorrectly configured
- [ ] You've upgraded the MariaDB server version without running `mariadb-upgrade`
- [ ] Files are stored on an unreliable device such as a USB flash drive or a shared network folder
- [ ] There are network problems caused by a proxy, firewall, or unstable connection
- [ ] Kernel security modules such as [AppArmor](https://wiki.ubuntu.com/AppArmor) and [SELinux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux) are blocking permissions
- [ ] Your Raspberry Pi has not been configured according to our [recommendations](raspberry-pi.md#system-requirements)

We recommend checking your Docker logs for messages like *disk full*, *wrong permissions*, *no route to host*, 
*connection failed*, and *killed* as described above. If a service has been killed or otherwise automatically terminated, 
this points to a memory problem.

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

Windows Pro users should [disable](img/docker-disable-wsl2.jpg) the *WSL 2* based engine in *Docker Settings > General*
so that they can mount drives other than `C:`. This will enable *Hyper-V*, which
[Microsoft doesn't offer](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements)
to its Windows Home customers. Docker Desktop uses dynamic memory allocation with *WSL 2*.

It's important to explicitly [increase the Docker memory limit](img/docker-resources-advanced.jpg) to 4 GB or more 
when using *Hyper-V*. The default of 2 GB may reduce indexing performance and cause unexpected restarts. 
Also make sure to configure at least 4 GB of swap.

#### macOS ####

It's important to [increase the Docker memory limit](img/docker-resources-advanced.jpg) to 4 GB or more,
as the default of 2 GB may reduce indexing performance and cause unexpected restarts. Also make sure to
configure at least 4 GB of swap.

### MariaDB ###

#### Version Upgrade ####

If the database doesn't start properly after upgrading from an earlier MySQL or MariaDB version,
you may need to run this command in a terminal:

```bash
docker-compose exec mariadb mariadb-upgrade -uroot -p
```

Enter the MariaDB "root" password specified in your `docker-compose.yml` when prompted.

Alternatively, you can downgrade to the previous version, create a database backup using the `photoprism backup`
command, start a new database instance based on the latest version, and then restore your index with
the `photoprism restore` command.

#### Lost Root Password ####

In case you forgot the MariaDB "root" password and the one specified in your configuration does not work,
you can [start the server with the `--skip-grant-tables` flag](https://mariadb.com/docs/reference/mdb/cli/mariadbd/skip-grant-tables/)
added to the `mysqld` command in your `docker-compose.yml`. This will temporarily give full access
to all users after a restart:

```yaml
services:
  mariadb:
    command: mysqld --skip-grant-tables
```

Restart the `mariadb` service for changes to take effect:

```bash
docker-compose stop mariadb
docker-compose up -d mariadb
```

Now open a database console:

```bash
docker-compose exec mariadb mysql -uroot
```

Enter the following commands to change the password for "root":

```sql
FLUSH PRIVILEGES;
ALTER USER 'root'@'%' IDENTIFIED BY 'new_password';
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
UPDATE mysql.user SET authentication_string = '' WHERE user = 'root';
UPDATE mysql.user SET plugin = '' WHERE user = 'root';
exit
```

When you are done, remove the `--skip-grant-tables` flag again to restore the original
command and restart the `mariadb` service as described above.

#### Corrupted Files ####

If your database files get corrupted frequently, it is usually because they are stored on an unreliable device such 
as a USB flash drive, an SD card, or a shared network folder.

- Never use the same database files with more than one server instance
- To share a database over a network, run the database server directly on the remote server instead of sharing database files
- To repair your tables after you have moved the files to a local disk, you can [start MariaDB with `--innodb-force-recovery=1`](https://mariadb.com/kb/en/innodb-recovery-modes/), similar to how you recover a lost root password as described above

### Linux Kernel Security ###

We recommend disabling kernel security on private servers, especially if you do not have experience
with the configuration.

### Filesystem Permissions ###

Use a file manager, or the commands `chmod` and `chown` on Unix-like operating systems,
to verify and fix filesystem permissions.

### Disk Space ###

Available disk space can be displayed with `df -h` on Linux and other Unix-like operating systems. 
The size of virtual disks and memory can be increased in Docker and VM settings if needed. Please refer to the documentation.

*[home directory]: \user\username on Windows, /Users/username on macOS, and /root or /home/username on Linux
*[host]: A physical computer, cloud server, or virtual machine that runs Docker
