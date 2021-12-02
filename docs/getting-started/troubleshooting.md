# Troubleshooting Installation Problems

!!! info ""
    You're welcome to ask for help in our [community chat](https://gitter.im/browseyourlife/community).
    [Sponsors](../funding.md) receive direct [technical support](https://photoprism.app/contact) via email.

### Docker Compose Logs ###

If you cannot connect to the Web UI even after waiting a few minutes, run this command to display 
the last 100 log messages (omit `--tail=100` to see all):

```
docker-compose logs --tail=100
```

Search them for messages like *disk full*, *wrong permissions*, and *database connection failed* 
before reporting a bug.

!!! note ""
    If you see no errors or no logs at all, you may have started the server on a different host
    and/or port. There could also be an issue with your browser, ad blocker, or firewall settings.

You can also try (re-)starting the app and database without `-d`. This keeps their containers running 
in the foreground and shows log messages for troubleshooting:

```
docker-compose stop
docker-compose up 
```

To enable [debug mode](config-options.md), add this to the environment variables of the `photoprism` 
service in your `docker-compose.yml` and restart for changes to take effect:

```
PHOTOPRISM_DEBUG: "true"
```

### Installing and Using Docker ###

If you can't use the `docker` and `docker-compose` commands at all, make sure [Docker](https://docs.docker.com/config/daemon/#start-the-daemon-manually)
is running on the host you are connected to and your current user has the permission to use it. The following guides explain how to install Docker:

- [Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04), [Mint](https://techviewleo.com/how-to-install-and-use-docker-in-linux-mint/), [Debian](https://www.linode.com/docs/guides/installing-and-using-docker-on-ubuntu-and-debian/), and [Fedora](https://docs.docker.com/engine/install/fedora/) Linux
- [Microsoft Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- [Apple macOS](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

Many Linux distributions require you to install `docker-compose` separately, for example by
running `sudo apt install docker-compose` in a terminal or using a graphical software package manager.

Commands on Linux may have to be prefixed with `sudo` when not running as root. Note that this will
point the home directory placeholder `~` to `/root` in volume mounts.

### Checklists ###

#### Missing Pictures ####

If you have indexed your library and some pictures are missing, first check *Library > Errors*
for errors and warnings. In case the logs don't contain anything helpful:

- [ ] The pictures are in [Review](../user-guide/organize/review.md) due to low quality or incomplete metadata
- [ ] Their [private](../user-guide/organize/private.md) or [archived](../user-guide/organize/archive.md) status was restored from a backup
- [ ] The NSFW (Not Safe For Work) filter is enabled, so they were marked as [private](../user-guide/organize/private.md)
- [ ] They are in *Library > Hidden* because a JPEG could not be created
- [ ] They were stacked based on their metadata or file names
- [ ] The indexer has skipped them because they are exact duplicates
- [ ] Their file types are unsupported
- [ ] The files have bad filesystem permissions, so they can't be opened by the indexer
- [ ] You are not signed in as admin, so you can't see everything
- [ ] You try to index a shared drive on a remote server, but the server is offline
- [ ] You are connected to the wrong server or a DNS entry hasn't been updated yet
- [ ] The indexer has crashed because you didn't configure 4 GB of swap
- [ ] Somebody has deleted files without telling you

#### App Not Loading ####

If you only see the logo when you navigate to the server URL and nothing else happens, even if you wait a moment:

- [ ] The user interface can't communicate properly with your server, for example, because a proxy is misconfigured (check its config and try without a proxy)
- [ ] JavaScript is disabled in your browser settings (enable it)
- [ ] JavaScript was disabled by a browser plugin (disable it or add an exception)
- [ ] An ad blocker is blocking requests (disable it or add an exception)
- [ ] You are using an incompatible browser (try a different browser)
- [ ] There is a problem with your network connection (test if other sites work)

#### Fatal Server Errors ####

Fatal errors are often caused by one of the following conditions:

- [ ] Your (virtual) server disk is full
- [ ] There is disk space left, but the [inode limit](https://serverfault.com/questions/104986/what-is-the-maximum-number-of-files-a-file-system-can-contain) has been reached
- [ ] The storage folder is not writable or there are other filesystem permission issues
- [ ] You have accidentally mounted the wrong folders
- [ ] The server is low on memory or swap
- [ ] The database server is not available, incompatible or incorrectly configured
- [ ] You've upgraded the MariaDB server version without running `mariadb-upgrade`
- [ ] There are network problems caused by a proxy, firewall or unstable connection
- [ ] Kernel security modules such as [AppArmor](https://wiki.ubuntu.com/AppArmor) and [SELinux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux) are blocking permissions
- [ ] Your Raspberry Pi has not been configured according to our [recommendations](raspberry-pi.md#system-requirements)

### Adding Swap ###

#### Linux ####

Open a terminal and run this command to check if your server has swap configured.

```
swapon --show
```

Example output:

```
NAME      TYPE SIZE USED PRIO
/swapfile file  64G  88M   -2
```

This means you have 64 GB of swap and don't need to add more. [Learn how much you need.](https://opensource.com/article/18/9/swap-space-linux-systems)

Otherwise, run these commands to permanently add 4 GB of swap (or more depending on how much physical memory you have):

```
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

```
docker-compose exec mariadb mariadb-upgrade -uroot -p
```

Enter the MariaDB "root" password specified in your `docker-compose.yml` when prompted.

Alternatively, you can downgrade to the previous version, create a database backup using the `photoprism backup`
command, start a new database instance based on the latest version, and then restore your index with
the `photoprism restore` command.

#### Lost Root Password ####

In case you forgot the MariaDB "root" password and the one specified in your configuration does not work,
you can start the server with the [`--skip-grant-tables`](https://mariadb.com/docs/reference/mdb/cli/mariadbd/skip-grant-tables/)
parameter added to the `mysqld` command in your `docker-compose.yml`. This will temporarily give full access
to all users after a restart:

```
services:
  mariadb:
    command: mysqld --skip-grant-tables
```

Restart the `mariadb` service for changes to take effect:

```
docker-compose stop mariadb
docker-compose up -d mariadb
```

Now open a database console:

```
docker-compose exec mariadb mysql -uroot
```

Enter the following commands to change the password for "root":

```
FLUSH PRIVILEGES;
ALTER USER 'root'@'%' IDENTIFIED BY 'new_password';
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
UPDATE mysql.user SET authentication_string = '' WHERE user = 'root';
UPDATE mysql.user SET plugin = '' WHERE user = 'root';
exit
```

When you are done, remove the `--skip-grant-tables` parameter again to restore the original
command and restart the `mariadb` service as described above.

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