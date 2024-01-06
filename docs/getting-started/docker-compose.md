# Setup Using Docker Compose

With [Docker Compose](https://docs.docker.com/compose/), you [use a YAML file](../developer-guide/technologies/yaml.md) to configure all application services so you can easily start them with a single command.
Before you proceed, make sure you have [Docker](https://store.docker.com/search?type=edition&offering=community) installed on your system. It is available for [Mac](https://docs.docker.com/desktop/install/mac-install/), [Linux](troubleshooting/docker.md#installation), and [Windows](https://docs.docker.com/desktop/install/windows-install/).

Alternatively, [Podman Compose](troubleshooting/docker.md#podman-compose) is supported as a drop-in replacement for Docker Compose on Red Hat-compatible Linux distributions like RHEL, CentOS, Fedora, AlmaLinux, and Rocky Linux.

### Step 1: Configure ###

=== "Linux"

    Download our [docker-compose.yml](https://dl.photoprism.app/docker/docker-compose.yml) example
    (right click and *Save Link As...* or use `wget`) to a folder of your choice,
    and change the [configuration](config-options.md) as needed:
    
    ```bash
    wget https://dl.photoprism.app/docker/docker-compose.yml
    ``` 
    
    Commands on Linux may have to be prefixed with `sudo` when not running as root.
    Note that this will point the home directory shortcut `~` to `/root` in the `volumes:` 
    section of your `docker-compose.yml`. Kernel security modules such as AppArmor and SELinux 
    have been [reported to cause issues](troubleshooting/docker.md#kernel-security).
    Ensure that your server has [at least 4 GB of swap](troubleshooting/docker.md#adding-swap) configured so that
    indexing doesn't cause restarts when there are memory usage spikes.

=== "Podman"

    Download our [docker-compose.yml](https://dl.photoprism.app/podman/docker-compose.yml) example
    (right click and *Save Link As...* or use `wget`) to a folder of your choice,
    and change the [configuration](config-options.md) as needed:
    
    ```bash
    wget https://dl.photoprism.app/podman/docker-compose.yml
    ``` 
 
    Alternatively, you can run these commands to install Podman and download the default configuration to `/opt/photoprism`:
    
    ```
    mkdir -p /opt/photoprism
    cd /opt/photoprism
    curl -sSf https://dl.photoprism.app/podman/install.sh | bash
    ```

    Please keep in mind to replace the `docker` and `docker compose` commands with `podman` and `podman-compose` when following the examples in our documentation.

=== "Raspberry Pi"

    Download our [docker-compose.yml](https://dl.photoprism.app/docker/arm64/docker-compose.yml) example for 
    the [Raspberry Pi](raspberry-pi.md) and other ARM64-based devices (right click and *Save Link As...* or use `wget`) to a folder of your choice,
    and change the [configuration](config-options.md) as needed:
    
    ```bash
    wget https://dl.photoprism.app/docker/arm64/docker-compose.yml
    ```

    Mostly the same installation instructions as for regular Linux servers apply.
    Commands may have to be prefixed with `sudo` when not running as root.
    Ensure your device meets the [requirements](raspberry-pi.md) and has
    [at least 4 GB of swap](troubleshooting/docker.md#adding-swap) configured before you continue.

=== "ARMv7"

    Download our [docker-compose.yml](https://dl.photoprism.app/docker/armv7/docker-compose.yml) example for 
    older ARMv7-based devices (right click and *Save Link As...* or use `wget`) to a folder of your choice,
    and change the [configuration](config-options.md) as needed:
    
    ```bash
    wget https://dl.photoprism.app/docker/armv7/docker-compose.yml
    ```

    Mostly the same installation instructions as for regular Linux servers apply.
    Commands may have to be prefixed with `sudo` when not running as root.
    Ensure your device meets the [requirements](raspberry-pi.md) and has
    [at least 4 GB of swap](troubleshooting/docker.md#adding-swap) configured before you continue.

=== "Windows"

    Download our [docker-compose.yml](https://dl.photoprism.app/docker/windows/docker-compose.yml) example for Windows
    (right click and *Save Link As...*) to a folder of your choice, and change the [configuration](config-options.md) as needed:
 
    [https://dl.photoprism.app/docker/windows/docker-compose.yml](https://dl.photoprism.app/docker/windows/docker-compose.yml) :material-download:

    On Windows Pro, you may need to [disable](img/docker-disable-wsl2.jpg) the WSL 2-based engine under *Docker Settings > General* 
    so that you can mount drives other than `C:`. [^1] This will enable Hyper-V, which 
    [Microsoft doesn't offer](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements) 
    to its Windows Home customers. [Docker Desktop](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
    uses dynamic memory allocation with WSL 2. It is important to explicitly [increase the Docker memory limit to 4 GB](img/docker-resources-advanced.jpg) or more when using 
    Hyper-V. The default of 2 GB can reduce indexing performance and cause unexpected restarts.
    Also, ensure that you configure at least 4 GB of swap space.

    !!! note ""
        Running the following commands will automatically download all required config files and start the server for you:
        
        ```bat
        curl.exe -o install.bat https://dl.photoprism.app/docker/windows/install.bat
        install.bat
        ```
        
        Before you run this, make sure you are in the directory where you want to install PhotoPrism and that [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) is installed and started on your PC.

=== "macOS"

    Download our [docker-compose.yml](https://dl.photoprism.app/docker/macos/docker-compose.yml) example for macOS
    (right click and *Save Link As...*) to a folder of your choice, and change the [configuration](config-options.md) as needed:

    [https://dl.photoprism.app/docker/macos/docker-compose.yml](https://dl.photoprism.app/docker/macos/docker-compose.yml) :material-download:
    
    It is important to [increase the Docker memory limit to 4 GB](img/docker-resources-advanced.jpg) or more,
    as the default of 2 GB can reduce indexing performance and cause unexpected restarts.
    Also, ensure that you configure at least 4 GB of swap space.

!!! note ""
    When editing the `docker-compose.yml` file, please make sure that [related values remain on the same indentation level](../developer-guide/technologies/yaml.md) and that [lists start with a dash](../developer-guide/technologies/yaml.md#multiple-values).
    If the value of an environment variable contains a literal `$` sign, for example in a password, it [must be escaped](../developer-guide/technologies/yaml.md#dollar-signs) with `$$` (a double dollar sign) so that e.g. `"compo$e"` becomes `"compo$$e"`.

!!! danger ""
    Always change `PHOTOPRISM_ADMIN_PASSWORD` so that the app **starts with a secure initial password**.
    Never use easy-to-guess passwords or default values like `insecure` on publicly accessible servers.
    There is no default [in case no password was provided](../user-guide/users/cli.md#changing-a-password). A minimum length of 8 characters is required.

#### Database ####

Our example includes a pre-configured [MariaDB](https://mariadb.com/) database server. If you remove it 
and provide no other database server credentials, SQLite database files will be created in the 
*storage* folder. Local [SSD storage is best](troubleshooting/performance.md#storage) for databases of any kind.

Never [store database files](troubleshooting/mariadb.md#corrupted-files) on an unreliable device such as a USB flash drive, SD card, or shared network folder. These may also have [unexpected file size limitations](https://thegeekpage.com/fix-the-file-size-exceeds-the-limit-allowed-and-cannot-be-saved/), which is especially problematic for databases that do not split data into smaller files.

!!! tldr ""
    It is **not possible to change the database password** with `MARIADB_PASSWORD` after MariaDB has been started for the first time. However, choosing a secure password is not essential if you don't [expose the database to other apps or hosts](troubleshooting/mariadb.md#cannot-connect). To enable [automatic schema updates](troubleshooting/mariadb.md#auto-upgrade) after upgrading to a new major version, make sure that  `MARIADB_AUTO_UPGRADE` is set to a non-empty value in your `docker-compose.yml`.

#### Volumes ####

You must explicitly [specify the directories](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes) you want to mount from your host, since PhotoPrism can't see files in folders that have not been shared. This is an important security feature and allows for a flexible configuration without having to change any other variables.

##### /photoprism/originals #####

The *originals* folder contains your original photo and video files. `~/Pictures` will be mounted by default, where `~` is a shortcut for your home directory:

```yaml
services:
  photoprism:
    volumes:
      - "~/Pictures:/photoprism/originals"
```

We recommend that you change `~/Pictures` to the directory where your existing media files are, for example:

```yaml
      - "/mnt/photos:/photoprism/originals"
```

Additional directories can be mounted as sub folders of `/photoprism/originals` (depending on [overlay filesystem support](troubleshooting/docker.md#overlay-volumes)):

```yaml
    volumes:
      - "/mnt/photos:/photoprism/originals"
      - "/mnt/videos:/photoprism/originals/videos"
```

On Windows, prefix the host path with the drive letter and use `/` instead of `\` as separator:

```yaml
    volumes:
      - "D:/Example/Pictures:/photoprism/originals"
```

!!! tldr ""
    If *read-only mode* is enabled, all features that require write permission to the *originals* folder 
    are disabled, e.g. [WebDAV](../user-guide/sync/webdav.md), uploading and deleting files. Set `PHOTOPRISM_READONLY` to `"true"`
    in `docker-compose.yml` for this. In addition, you can [mount volumes with the `:ro` flag](https://docs.docker.com/compose/compose-file/compose-file-v3/#short-syntax-3)
    so that writes are also blocked by Docker.

##### /photoprism/storage #####

The *storage* folder is used to save config, cache, thumbnail, and sidecar files. It must always be specified so that you do not lose these files after a restart or upgrade.
If available, we recommend you put the *storage* folder on a [local SSD drive](troubleshooting/performance.md#storage) for best performance. You can otherwise keep the default and store the files in a folder relative to the current directory:

```yaml
services:
  photoprism:
    volumes:
      - "./storage:/photoprism/storage"
```

!!! tldr ""
    Never configure the *storage* folder to be inside the *originals* folder unless the name starts with a `.` to indicate that it is hidden.
    Should you later want to move your instance to another host, the easiest and most time-saving way is to copy the entire *storage* folder along with your *originals* and *database*.

##### /photoprism/import #####

You can optionally mount an *import* folder from which files can be transferred to the *originals* folder in a structured way that avoids duplicates, for example:

```yaml
services:
  photoprism:
    volumes:
      - "/mnt/media/usb:/photoprism/import"
```

[Imported files](../user-guide/library/import.md) receive a canonical filename and will be organized by year and month. You should never configure the *import* folder to be inside the *originals* folder, as this will cause a loop by importing already indexed files.

!!! tldr ""
    Even if you don't specify an *import* folder, adding files via [Web Upload](../user-guide/library/upload.md) and [WebDAV](../user-guide/sync/webdav.md) remains possible unless [read-only mode](config-options.md) is enabled or the [features have been disabled](../user-guide/settings/general.md).

### Step 2: Start the server ###

Open a terminal and change to the folder in which the `docker-compose.yml` file has been saved.[^2]
Run this command to start the application and database services in the background:

```bash
docker compose up -d
```

*Note that our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible Linux distributions.*

Now open the Web UI by navigating to http://localhost:2342/. You should see a login screen.
Sign in with the user `admin` and the initial password configured via `PHOTOPRISM_ADMIN_PASSWORD`.
You may change it on the [account settings page](../user-guide/settings/account.md).
Enabling [public mode](config-options.md) will disable authentication.

!!! info ""
    It can be helpful to [keep Docker running in the foreground while debugging](troubleshooting/docker.md#viewing-logs) so that log messages are displayed directly. To do this, omit the `-d` parameter when restarting.

    Should the server already be running, or you see no errors, you may have started it
    on a different host and/or port. There could also be an [issue with your browser,
    ad blocker, or firewall settings](troubleshooting/index.md#connection-fails).

!!! tldr ""
    It is not possible to change the password via `PHOTOPRISM_ADMIN_PASSWORD` after the app has been 
    started for the first time. You may run `docker compose exec photoprism photoprism passwd [username]` 
    in a terminal to change an existing password. You can also reset your database for a clean start.

The server port and other [config options](config-options.md) can be changed in `docker-compose.yml` at any time.
Remember to restart the services for changes to take effect:

```bash
docker compose stop
docker compose up -d
```

### Step 3: Index Your Library ###

Our [First Steps 👣](../user-guide/first-steps.md) tutorial guides you through the user interface and settings to ensure your library is indexed according to your individual preferences.

<!--
!!! note ""
    Ensure [there is enough disk space available](troubleshooting/docker.md#disk-space) for creating thumbnails and [verify filesystem permissions](troubleshooting/docker.md#file-permissions)
    before starting to index: Files in the *originals* folder must be readable, while the *storage* folder
    including all subdirectories must be readable and writeable.

Open the Web UI, go to *Library* and click *Start* to start indexing your pictures.

While indexing, JPEG sidecar files may be created for originals in other formats such as RAW and HEIF. 
This is required for image classification, facial recognition, and for displaying them in a Web browser. 
Sidecar and thumbnail files will be added to the *storage* folder, so that your *originals* folder won't be modified.

Your [photos](../user-guide/organize/browse.md) and [videos](../user-guide/organize/video.md) will 
successively become visible in search results and other parts of the user interface. 
Open the *Logs* tab in *Library* to watch the indexer working.

Of course, you can continue using your favorite tools for processing RAW files, editing metadata, 
or importing new shots. Go to *Library* and click *Start* to update the index after files have been 
changed, added, or removed. This can also be automated using CLI commands and a [scheduler](https://dl.photoprism.app/docker/scheduler/).-->

Easy, isn't it?

### PhotoPrism® Plus ###

Our members can activate [additional features](https://link.photoprism.app/membership) by logging in with the [admin user created during setup](config-options.md#authentication) and then following the steps [described in our activation guide](https://www.photoprism.app/kb/activation). Thank you for your support, which has been and continues to be essential to the success of the project! :octicons-heart-fill-24:{ .heart .purple }

[Compare Memberships ›](https://link.photoprism.app/membership){ class="pr-3 block-xs" } [View Membership FAQ ›](https://www.photoprism.app/membership/faq) 

!!! example ""
    We recommend that new users install our free Community Edition before [signing up for a membership](https://link.photoprism.app/membership).

### Troubleshooting ###

If your server runs out of memory, the index is frequently locked, or other system resources are running low:

- [ ] Try [reducing the number of workers](config-options.md#index-workers) by setting `PHOTOPRISM_WORKERS` to a reasonably small value in `docker-compose.yml`, depending on the CPU performance and number of cores
- [ ] Make sure [your server has at least 4 GB of swap space](troubleshooting/docker.md#adding-swap) so that indexing doesn't cause restarts when memory usage spikes; RAW image conversion and video transcoding are especially demanding
- [ ] If you are using SQLite, switch to MariaDB, which is [better optimized for high concurrency](faq.md#should-i-use-sqlite-mariadb-or-mysql)
- [ ] As a last measure, you can [disable the use of TensorFlow](config-options.md#feature-flags) for image classification and facial recognition

Other issues? Our [troubleshooting checklists](troubleshooting/index.md) help you quickly diagnose and solve them.

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://www.photoprism.app/membership) receive direct [technical support](https://www.photoprism.app/contact) via email.
    Before [submitting a support request](index.md#getting-support), try to [determine the cause of your problem](troubleshooting/index.md).

### Command-Line Interface ###

#### Introduction

`photoprism help` lists all commands and [config options](config-options.md) available in the current version:

```bash
docker compose exec photoprism photoprism help
```

Use the `--help` flag to see a detailed command description, for example:

```bash
docker compose exec photoprism photoprism backup --help
```

PhotoPrism's command-line interface is also well suited for job automation using a
[scheduler](https://dl.photoprism.app/docker/scheduler/).

!!! tip ""
    When using *Docker Compose*, you can prepend commands like `docker compose exec [service] [command]` to run them in a service container.
    Should this fail with *no container found*, make sure the service has been started, you have specified an existing service (usually `photoprism`) and you are in the folder where the `docker-compose.yml` file is located.

#### Opening a Terminal

To open a terminal session as the [default user](https://docs.docker.com/compose/compose-file/05-services/#user):

```bash
docker compose exec photoprism bash
```

Since the above will open the terminal as root by default, we recommend that you pass the `-u` flag to explicitly open a non-root session if PhotoPrism is running under a specific user account, for example:

```bash
docker compose exec -u 1000 photoprism bash
```

This avoids potential [filesystem permission issues](troubleshooting/docker.md#file-permissions) that can occur when a command creates new files or folders, e.g. to store thumbnails.

#### Changing the User ID

Specifying a user with the `-u` flag is possible for all commands you run with [Docker](docker.md#command-line-interface) and Docker Compose. In the following examples, it is omitted for brevity.
Note, however, that commands that you run without an explicit user ID might be executed as root.
The currently supported user ID ranges are 0, 33, 50-99, 500-600, 900-1250, and 2000-2100.

!!! tip ""
    We recommend running the `photoprism` service as a non-root user by setting either the [user service property](https://docs.docker.com/compose/compose-file/05-services/#user) or the `PHOTOPRISM_UID` [environment variable](config-options.md#docker-image) in the `docker-compose.yml` file. Don't forget to update file permissions and/or ownership with the `chown` command when you make changes.

#### Examples

| Action                                                 | Command                                                       |
|--------------------------------------------------------|---------------------------------------------------------------|
| *Start Services*                                       | `docker compose up -d`                                        | 
| *Stop Services*                                        | `docker compose stop`                                         |
| *Download Updates*                                     | `docker compose pull`                                         |
| *Uninstall*                                            | `docker compose rm -s -v`                                     |
| [*Watch Logs*](troubleshooting/docker.md#viewing-logs) | `docker compose logs -f --tail=100`                           |
| *Display Config Values*                                | `docker compose exec photoprism photoprism show config`       |
| *Show Migration Status*                                | `docker compose exec photoprism photoprism migrations ls`     |
| *Repeat Failed Migrations*                             | `docker compose exec photoprism photoprism migrations run -f` |
| *Reset Database*                                       | `docker compose exec photoprism photoprism reset -y`          |
| *Backup Database*                                      | `docker compose exec photoprism photoprism backup -a -i`      |                      
| *Restore Database*                                     | `docker compose exec photoprism photoprism restore -a -i`     |                   
| *Change Password*                                      | `docker compose exec photoprism photoprism passwd [username]` |
| *Show User Management Commands*                        | `docker compose exec photoprism photoprism users help`        |
| *Reset Users*                                          | `docker compose exec photoprism photoprism users reset -y`    |
| *Show Face Recognition Commands*                       | `docker compose exec photoprism photoprism faces help`        |
| *Index Faces*                                          | `docker compose exec photoprism photoprism faces index`       |
| *Reset People & Faces*                                 | `docker compose exec photoprism photoprism faces reset -f`    |
| *Transcode Videos to AVC*                              | `docker compose exec photoprism photoprism convert`           |
| *Regenerate Thumbnails*                                | `docker compose exec photoprism photoprism thumbs -f`         |
| [*Update Index*](../user-guide/library/originals.md)   | `docker compose exec photoprism photoprism index --cleanup`   |                  
| [*Move to Originals*](../user-guide/library/import.md) | `docker compose exec photoprism photoprism import [path]`     |                  
| [*Copy to Originals*](../user-guide/library/import.md) | `docker compose exec photoprism photoprism cp [path]`         |                  

*Note that our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible Linux distributions.*

!!! info "Complete Rescan"
    `docker compose exec photoprism photoprism index -f` rescans all originals, including already indexed and unchanged files.
    This may be necessary after major upgrades and after migrations of the database schema, especially if search results are missing or incorrect. Note you can also start a [rescan from the user interface](../user-guide/library/originals.md) by navigating to *Library* > *Index*, checking "Complete Rescan" and then clicking "Start". Manually entered information such as labels, people, titles or descriptions will not be modified when indexing, even if you perform a "complete rescan".

*[home directory]: \user\username on Windows, /Users/username on macOS, and /root or /home/username on Linux
*[host]: Computer, Cloud Server, or VM that runs PhotoPrism
*[swap]: substitute for physical memory
*[root]: superuser account with the ID 0
*[HEIF]: High Efficiency Image File Format
*[RAW]: image format that contains unprocessed sensor data
*[SSD]: Solid-State Drive
*[CDN]: Content Delivery Network
*[UI]: User Interface
*[CLI]: Command-Line Interface
*[AVC]: MPEG-4 / H.264
*[FFmpeg]: transcodes video files
*[SQLite]: self-contained, serverless SQL database
*[read-only]: write protected
*[filesystem]: contains your files and folders
*[RHEL]: Red Hat Enterprise Linux®

[^1]: <https://rominirani.com/docker-on-windows-mounting-host-directories-d96f3f056a2c>
[^2]: The default filename for the [Docker Compose](https://docs.docker.com/compose/) configuration is `docker-compose.yml`. For simplicity, it does not need to be specified if you run commands in the same directory. Config files for other apps and instances should be placed in separate folders.