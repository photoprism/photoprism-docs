# Setup Using Docker Compose

[Docker Compose](https://docs.docker.com/compose/) works with [human-readable YAML files](../developer-guide/technologies/yaml.md) 
that define application services, networks, and storage volumes, so you don't have to remember complicated commands and parameters.
Before you start, make sure you have [Docker](https://store.docker.com/search?type=edition&offering=community)
installed on your system. It is available for Mac, Linux, and Windows.

!!! info ""
    You're welcome to ask for help in our [community chat](https://gitter.im/browseyourlife/community).
    [Sponsors](../funding.md) receive direct [technical support](https://photoprism.app/contact) via email.

### Step 1: Configure ###

=== "Linux"

    Download our [docker-compose.yml](https://dl.photoprism.app/docker/docker-compose.yml) example
    (right click and *Save Link As...* or use `wget`) to a folder of your choice,
    and change the [configuration](config-options.md) as needed:
    
    ```bash
    wget https://dl.photoprism.app/docker/docker-compose.yml
    ``` 
    
    Commands on Linux may have to be prefixed with `sudo` when not running as root.
    Note that this will point the home directory placeholder `~` to `/root` in the `volumes:` 
    section of your `docker-compose.yml`. Kernel security modules such as AppArmor and SELinux 
    have been reported to cause [issues](troubleshooting.md#linux-kernel-security).

=== "Raspberry Pi"

    Download our [docker-compose.yml](https://dl.photoprism.app/docker/arm64/docker-compose.yml) example for 
    the Raspberry Pi 3 / 4 and other ARM64-based devices (right click and *Save Link As...* or use `wget`) to a folder of your choice,
    and change the [configuration](config-options.md) as needed:
    
    ```bash
    wget https://dl.photoprism.app/docker/arm64/docker-compose.yml
    ```

    Mostly the same installation instructions as for regular Linux servers apply.
    Commands may have to be prefixed with `sudo` when not running as root.
    Ensure your device meets the [requirements](raspberry-pi.md) before you continue.

=== "ARMv7"

    Download our [docker-compose.yml](https://dl.photoprism.app/docker/armv7/docker-compose.yml) example for 
    older ARMv7-based devices (right click and *Save Link As...* or use `wget`) to a folder of your choice,
    and change the [configuration](config-options.md) as needed:
    
    ```bash
    wget https://dl.photoprism.app/docker/armv7/docker-compose.yml
    ```

    Mostly the same installation instructions as for regular Linux servers apply.
    Commands may have to be prefixed with `sudo` when not running as root.
    Ensure your device meets the [requirements](raspberry-pi.md) before you continue.

=== "Windows"

    Download our [docker-compose.yml](https://dl.photoprism.app/docker/windows/docker-compose.yml) example for Windows
    (right click and *Save Link As...*) to a folder of your choice, and change the [configuration](config-options.md) as needed:
 
    [https://dl.photoprism.app/docker/windows/docker-compose.yml](https://dl.photoprism.app/docker/windows/docker-compose.yml) :material-download:

    Windows Pro users should [disable](img/docker-disable-wsl2.jpg) the WSL 2 based engine in *Docker Settings > General* 
    so that they can mount drives other than `C:`. This will enable Hyper-V, which 
    [Microsoft doesn't offer](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements) 
    to its Windows Home customers. Docker Desktop uses dynamic memory allocation with WSL 2. It's important 
    to explicitly [increase the Docker memory limit](img/docker-resources-advanced.jpg) to 4 GB or more when using 
    Hyper-V. The default of 2 GB may reduce indexing performance and cause unexpected restarts.

=== "macOS"

    Download our [docker-compose.yml](https://dl.photoprism.app/docker/macos/docker-compose.yml) example for macOS
    (right click and *Save Link As...*) to a folder of your choice, and change the [configuration](config-options.md) as needed:

    [https://dl.photoprism.app/docker/macos/docker-compose.yml](https://dl.photoprism.app/docker/macos/docker-compose.yml) :material-download:
    
    It's important to [increase the Docker memory limit](img/docker-resources-advanced.jpg) to 4 GB or more,
    as the default of 2 GB may reduce indexing performance and cause unexpected restarts.

!!! danger ""
    Always change `PHOTOPRISM_ADMIN_PASSWORD` so that the app starts with a **secure initial password**.
    Never use easy-to-guess passwords or default values like `insecure` on publicly accessible servers.
    There is no default in case no password was provided. A minimum length of 4 characters is required.

#### Database ####

Our example includes a pre-configured [MariaDB](https://mariadb.com/) database server. If you remove it 
and provide no other database server credentials, a SQLite database file will be created in the 
*storage* folder. Local [SSD storage is best](performance.md#storage) for databases of any kind.
Never [store](troubleshooting.md#corrupted-files) database files on an unreliable device such as a USB flash drive,
an SD card, or a shared network folder.

!!! tldr ""
    It is not possible to change the password via `MYSQL_PASSWORD` after the database has been started 
    for the first time. Choosing a secure password is not essential if you don't expose the database 
    to other apps and hosts.


#### Volumes ####

Since the app is running inside a container, you have to explicitly mount the host folders you want to use.
PhotoPrism won't be able to see folders that have not been mounted. That's an important security feature.

##### /photoprism/originals #####

The *originals* folder contains your original photo and video files. 

`~/Pictures` will be mounted by default, where `~` is a placeholder for your home directory:

```yaml
volumes:
  - "~/Pictures:/photoprism/originals"
```

Other folders accessible from the host may be [mounted](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes) instead, 
including network drives. Multiple folders can be made accessible by mounting them as subfolders
of `/photoprism/originals`, for example:

```yaml
volumes:
  - "/home/username/Pictures:/photoprism/originals"
  - "/mnt/friends:/photoprism/originals/friends"
  - "/mnt/photos:/photoprism/originals/media"
```

!!! tldr ""
    When you enable *read-only mode*, all features that require write permission to the *originals* folder 
    are disabled, in particular import, upload, and delete. Set `PHOTOPRISM_READONLY` to `"true"`
    in `docker-compose.yml` for this. You can mount a folder with the `:ro` flag to make Docker block 
    write operations as well.

##### /photoprism/storage #####

Cache, session, thumbnail, and sidecar files will be created in the *storage* folder. Never remove the volume from
your `docker-compose.yml` file so that you don't lose these files after restarting or upgrading the container.
We recommend placing the *storage* folder on a [local SSD drive](performance.md#storage) for best performance.

##### /photoprism/import #####

You may optionally mount an *import* folder from which files can be transferred to the *originals* folder
in a structured way that avoids duplicates. Imported files receive a canonical filename and will be
organized by year and month.

!!! tldr ""
    You can safely skip this. Adding files via [Web Upload](../user-guide/library/upload.md)
    and [WebDAV](../user-guide/sync/webdav.md) remains possible, unless [read-only mode](config-options.md)
    is enabled or the [features have been disabled](../user-guide/settings/general.md).

### Step 2: Start the server ###

Open a terminal and change to the folder in which the `docker-compose.yml` file has been saved.[^1]
Run this command to start the app and database in the background:

```bash
docker-compose up -d
```

Now open the Web UI by navigating to http://localhost:2342/. You should see a login screen.
Sign in with the user `admin` and the initial password configured via `PHOTOPRISM_ADMIN_PASSWORD`.
You may change it on the [account settings page](../user-guide/settings/account.md).
Enabling [public mode](config-options.md) will disable authentication.

!!! info ""
    If you can't connect, try starting the app without `-d`: `docker-compose up photoprism`. 
    This keeps it in the foreground and shows log messages for [troubleshooting](troubleshooting.md).
    Should the server already be running, or you see no errors, you may have started it
    on a different host and/or port. There could also be an issue with your browser,
    ad blocker, or firewall settings.

!!! tldr ""
    It is not possible to change the password via `PHOTOPRISM_ADMIN_PASSWORD` after the app has been 
    started for the first time. You may run `docker-compose exec photoprism photoprism passwd` 
    in a terminal to change an existing password. You can also reset your database for a clean start.

The server port and app [config options](config-options.md) may be changed in `docker-compose.yml` at any time.
Remember to restart the app for changes to take effect:

```bash
docker-compose stop photoprism
docker-compose up -d photoprism
```

### Step 3: Index your library ###

!!! note ""
    Ensure there is enough disk space available for creating thumbnails and verify file system permissions
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
changed, added, or removed. This can also be automated using CLI commands and a [scheduler](https://dl.photoprism.app/docker/scheduler/).

Easy, isn't it?

!!! info ""
    If you're running out of memory - or other system resources - while indexing, try reducing the 
    [number of workers](https://docs.photoprism.app/getting-started/config-options/) by setting
    `PHOTOPRISM_WORKERS` to a reasonably small value in `docker-compose.yml` (depending on the performance of the server).
    Also make sure your server has at least 4 GB of [swap](https://opensource.com/article/18/9/swap-space-linux-systems) 
    configured so that indexing doesn't cause restarts when there are memory usage spikes.
    Especially the conversion of RAW images and the transcoding of videos are very demanding.
    As a measure of last resort, you may disable using TensorFlow for image classification and facial recognition.

!!! example ""
    **Back us on [Patreon](https://www.patreon.com/photoprism) or [GitHub Sponsors](https://github.com/sponsors/photoprism).**
    Your continued support [helps us](../funding.md) provide [regular updates](https://docs.photoprism.app/release-notes/)
    and services like [world maps](https://demo.photoprism.app/places). Thank you! 💜

### Command-Line Interface ###

`photoprism help` lists all commands and [config options](config-options.md) available in the current version:

```bash
docker-compose exec photoprism photoprism help
```

Use the `--help` flag to see a detailed command description, for example:

```bash
docker-compose exec photoprism photoprism backup --help
```

!!! info ""
    Prefixing commands with `docker-compose exec [service name]` runs them inside an app container.
    If this fails with *no container found*, make sure the app has been started,
    its service name is the same, and you are in the folder in which the `docker-compose.yml` 
    file has been saved.

PhotoPrism's command-line interface is well suited for job automation using a
[scheduler](https://dl.photoprism.app/docker/scheduler/).

#### Examples ####

| Action                          | Command                                                     |
| ------------------------------- | ----------------------------------------------------------- |
| *Start App & Database*          | `docker-compose up -d`                                      | 
| *Stop App & Database*           | `docker-compose stop`                                       |
| *Update Container Images*       | `docker-compose pull`                                       |
| *Uninstall*                     | `docker-compose rm -s -v`                                   |
| *Show Server Logs*              | `docker-compose logs --tail=100 -f`                         |
| *Show Config Values*            | `docker-compose exec photoprism photoprism config`          |
| *Reset Database*                | `docker-compose exec photoprism photoprism reset`           |                   
| *Backup Database*               | `docker-compose exec photoprism photoprism backup -a -i`    |                      
| *Restore Database*              | `docker-compose exec photoprism photoprism restore -a -i`   |                   
| *Change Admin Password*         | `docker-compose exec photoprism photoprism passwd`          |
| *Show User Management Commands*    | `docker-compose exec photoprism photoprism users help`   |
| *Show Facial Recognition Commands* | `docker-compose exec photoprism photoprism faces help`   |
| *Index Faces*                   | `docker-compose exec photoprism photoprism faces index`     |
| *Reset People & Faces*          | `docker-compose exec photoprism photoprism faces reset -f`  |
| *Transcode Videos to AVC*       | `docker-compose exec photoprism photoprism convert`         |
| *Regenerate Thumbnails*         | `docker-compose exec photoprism photoprism thumbs -f`       |
| *Update Index*                  | `docker-compose exec photoprism photoprism index --cleanup` |                  
| *Import Files*                  | `docker-compose exec photoprism photoprism import [path]`   |                  

!!! info "Complete Rescan"
    `docker-compose exec photoprism photoprism index -f` rescans all originals, including already indexed and unchanged files. 
    This may be necessary after major upgrades.

*[home directory]: \user\username on Windows, /Users/username on macOS, and /root or /home/username on Linux
*[host]: A physical computer, cloud server, or virtual machine that runs Docker
*[HEIF]: High Efficiency Image File Format
*[RAW]: RAW files contain image data captured during exposure in an unprocessed format
*[Web UI]: A Progressive Web App that can be installed on your home screen and provides a native app-like experience
*[CLI]: Command-Line Interface
*[AVC]: MPEG-4 AVC video compression standard, also known as H.264

[^1]: The default [Docker Compose](https://docs.docker.com/compose/) config filename is `docker-compose.yml`. For simplicity, it doesn't need to be specified when running the `docker-compose` command in the same directory. Config files for other apps or instances should be placed in separate folders.
