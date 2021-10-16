# Troubleshooting Installation Problems

### Docker Compose ###

If you cannot connect to the Web UI even after waiting for a while, run this command to display 
the last 100 log messages:

```
docker-compose logs --tail=100
```

Search them for messages like *disk full*, *wrong permissions*, and *database connection failed* 
before reporting a bug.

!!! info ""
    If you see no errors or no logs at all, you may have started the server on a different host
    and/or port. There could also be an issue with your browser, ad blocker, or firewall settings.

You can also try (re-)starting the app and database without `-d`. This keeps their containers running 
in the foreground and shows log messages for troubleshooting:

```
docker-compose stop
docker-compose up 
```

If you can't use `docker` or `docker-compose` at all, make sure [Docker](https://docs.docker.com/config/daemon/#start-the-daemon-manually)
is running on the host and your current user has the permission to use it. 
Many Linux distributions require you to install `docker-compose` separately, for example by
running `sudo apt install docker-compose` in a terminal or using a graphical software package manager.

Commands on Linux may have to be prefixed with `sudo` when not running as root. Note that this will 
point the home directory placeholder `~` to `/root` in volume mounts.

To enable [debug mode](config-options.md) in your `docker-compose.yml` file:

```
PHOTOPRISM_DEBUG: "true"
```

!!! info ""
    You're welcome to ask for help in our [community chat](https://gitter.im/browseyourlife/community).
    [Sponsors](../funding.md) receive direct [technical support](https://photoprism.app/contact) via email.

### Common Issues ###

Fatal errors are often caused by one of the following conditions:

1. Your (virtual) server disk is full
2. There is disk space left, but the [inode limit](https://serverfault.com/questions/104986/what-is-the-maximum-number-of-files-a-file-system-can-contain) has been reached
3. The storage folder is not writable or there are other filesystem permission issues
4. You have accidentally mounted the wrong folders
5. The server is low on memory
6. The database server is not available, incompatible or incorrectly configured
7. There are network problems caused by a proxy, firewall or unstable connection
8. Kernel security modules such as [AppArmor](https://wiki.ubuntu.com/AppArmor) and
   [SELinux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux) are blocking permissions

### Kernel Security ###

Linux kernel security can be disabled on private servers, especially if you do not have experience
with the configuration.

### Filesystem Permissions ###

Use a file manager, or the commands `chmod` and `chown` on Unix-like operating systems,
to verify and fix filesystem permissions.

### Disk Space ###

Available disk space can be displayed with `df -h`. The size of virtual disks and memory can be
increased in Docker and VM settings if needed. Please refer to the documentation.

*[home directory]: \user\username on Windows, /Users/username on macOS, and /root or /home/username on Linux
*[host]: A physical computer, cloud server, or virtual machine that runs Docker