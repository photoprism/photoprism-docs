# Setup Using Docker Compose

Before you start, make sure you have [Docker](https://store.docker.com/search?type=edition&offering=community) 
installed on your system. It is available for Mac, Linux, and Windows.

### Step 1: Configure ###

=== "Linux"

    Download our standard [docker-compose.yml](https://dl.photoprism.org/docker/docker-compose.yml) example
    (right click and *Save Link As...* or use `wget`) to a folder of your choice,
    and change the [configuration](config-options.md) as needed:
    
    ```
    wget https://dl.photoprism.org/docker/docker-compose.yml
    ``` 
    
    Commands on Linux may have to be prefixed with `sudo` when not running as root.
    Note that this will point the home directory placeholder `~` to `/root` in volume mounts.
    Kernel security modules such as AppArmor and SELinux have been reported to cause
    [issues](https://docs.photoprism.org/getting-started/faq/#why-is-photoprism-getting-stuck-in-a-restart-loop).

=== "Raspberry Pi"

    Download our [docker-compose.yml](https://dl.photoprism.org/docker/arm64/docker-compose.yml) example for 
    the Raspberry Pi (right click and *Save Link As...* or use `wget`) to a folder of your choice,
    and change the [configuration](config-options.md) as needed:
    
    ```
    wget https://dl.photoprism.org/docker/arm64/docker-compose.yml
    ```

    Mostly the same installation instructions as for regular Linux servers apply.
    Commands may have to be prefixed with `sudo` when not running as root.
    Ensure your device meets the [system requirements](raspberry-pi.md) before you continue.

    !!! missing ""
        Owners of ARMv7-based devices have to revert to an [alternative image](https://hub.docker.com/r/linuxserver/mariadb)
        if they want to use MariaDB. The [official image](https://hub.docker.com/_/mariadb) is available for AMD64 and ARM64 only.
        Pay close attention to changed directory and environment variable names.

=== "Windows"

    Download our [docker-compose.yml](https://dl.photoprism.org/docker/windows/docker-compose.yml) example for Windows
    (right click and *Save Link As...*) to a folder of your choice, and change the [configuration](config-options.md) as needed:
 
    [https://dl.photoprism.org/docker/windows/docker-compose.yml :material-download:](https://dl.photoprism.org/docker/windows/docker-compose.yml)

    Windows Pro users should [disable](img/docker-disable-wsl2.jpg) the WSL 2 based engine in *Docker Settings > General* 
    so that they can mount drives other than `C:`. This will enable Hyper-V, which 
    [Microsoft doesn't offer](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements) 
    to its Windows Home customers. Docker Desktop uses dynamic memory allocation with WSL 2. It's important 
    to explicitly [increase the Docker memory limit](img/docker-resources-advanced.jpg) to 4 GB or more when using 
    Hyper-V. The default of 2 GB may reduce indexing performance and cause unexpected restarts.

=== "macOS"

    Download our [docker-compose.yml](https://dl.photoprism.org/docker/macos/docker-compose.yml) example for macOS
    (right click and *Save Link As...*) to a folder of your choice, and change the [configuration](config-options.md) as needed:

    [https://dl.photoprism.org/docker/macos/docker-compose.yml :material-download:](https://dl.photoprism.org/docker/macos/docker-compose.yml)
    
    It's important to [increase the Docker memory limit](img/docker-resources-advanced.jpg) to 4 GB or more,
    as the default of 2 GB may reduce indexing performance and cause unexpected restarts.

!!! danger ""
    Always change `PHOTOPRISM_ADMIN_PASSWORD` so that PhotoPrism starts with a **secure initial password**.
    Never use easy-to-guess passwords or default values like `insecure` on publicly accessible servers.
    For security reasons, there also is no default in case no password was provided.
    A minimum length of 4 characters is required.

#### Volumes ####

##### /photoprism/originals #####

The *originals* folder contains your original photo and video files.

They will be mounted from `~/Pictures` by default, where `~` is a placeholder for 
your [home directory](https://en.wikipedia.org/wiki/Home_directory). 

All folders accessible from the host [may be mounted](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes), 
including network drives. Since PhotoPrism is running inside a container, it won't be able to see 
folders that have not been mounted. That's an important security feature.

Multiple folders can be made accessible by mounting them as subfolders:

```
volumes:
  - "~/friends:/photoprism/originals/friends"
  - "/media/photos:/photoprism/originals/media"
```

##### /photoprism/import #####

You may optionally mount an *import* folder from which files can be transferred to the *originals* folder
in a structured way that avoids duplicates. Imported files receive a canonical filename and will be
organized by year and month.

!!! note ""
    You can safely skip this. Adding files via [Web Upload](../user-guide/library/upload.md)
    and [WebDAV](../user-guide/sync/webdav.md) remains possible, unless [read-only mode](config-options.md)
    is enabled, or the [features have been disabled](../user-guide/settings/general.md).

##### /photoprism/storage #####

Cache, session, thumbnail, and sidecar files will be created in the *storage* folder. Never remove the volume from
your `docker-compose.yml` file so that you don't lose these files after restarting or upgrading the container.

!!! info "Read-Only Mode"
    Running PhotoPrism in read-only mode disables all features that require write permissions,
    like importing, uploading, renaming, and deleting files.
    You may enable it by setting `PHOTOPRISM_READONLY` to `"true"`.
    In addition, you may mount the *originals* folder with `:ro` flag so that Docker 
    blocks write operations.

### Step 2: Start the server ###

Open a terminal and change to the folder in which the `docker-compose.yml` file has been saved.
Run this command to start the app container in the background and keep it running:

```
docker-compose up -d
```

Now open the Web UI by navigating to http://localhost:2342/. You should see a login screen.

!!! hint ""
    If you can't connect, try starting the server without `-d`. This keeps it in the foreground
    and shows log messages for troubleshooting. You're welcome to ask for help in our [community chat](https://gitter.im/browseyourlife/community).
    Should the server already be running, or you see no errors, you may have started it
    on a different host and/or port. There could also be an issue with your browser,
    ad blocker or firewall settings.

Sign in with the user `admin` and the initial password configured via `PHOTOPRISM_ADMIN_PASSWORD`.
You may change it on the [account settings page](../user-guide/settings/account.md), 
or using the `photoprism passwd` command in a terminal.
Enabling [public mode](config-options.md) will disable authentication.

!!! note ""
    For security reasons, it is **not possible to change an existing admin password via `PHOTOPRISM_ADMIN_PASSWORD`** after 
    your instance has been started for the first time. The terminal command `docker-compose exec photoprism photoprism reset`
    can reset your database for a clean start if needed. Ensure you're in the folder in which the `docker-compose.yml` 
    file has been saved and the container is running before using it or other CLI commands. Alternatively, you can 
    drop and recreate the database or manually delete database files from its storage folder before restarting your instance.

The server port and other basic settings may be changed in `docker-compose.yml` at any time.
Remember to restart the container whenever it has been changed:

```
docker-compose stop photoprism
docker-compose up -d photoprism
```

### Step 3: Index your library ###

!!! attention ""
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
changed, added, or removed. This can also be automated using CLI commands and a [scheduler](https://dl.photoprism.org/docker/scheduler/).

Easy, isn't it?

!!! example ""
    **This open-source project is made possible [thanks to our sponsors](https://github.com/photoprism/photoprism/blob/develop/SPONSORS.md).**
    If you enjoy using PhotoPrism, please consider backing us on [Patreon](https://www.patreon.com/photoprism)
    or [GitHub Sponsors](https://github.com/sponsors/photoprism).
    Your continued support helps us fund operating costs, provide services like satellite maps,
    and develop new features. Thank you very much! 💜

!!! info "Reducing Server Load"
    If you're running out of memory - or other system resources - while indexing, try limiting the 
    [number of workers](https://docs.photoprism.org/getting-started/config-options/) by setting
    `PHOTOPRISM_WORKERS` to a reasonably small value in `docker-compose.yml` (depending on your CPU and expectations).
    Also make sure your server has at least 4 GB of [swap](https://opensource.com/article/18/9/swap-space-linux-systems) 
    configured so that indexing doesn't cause restarts when there are memory usage spikes.
    Especially the conversion of RAW images and the transcoding of videos are very demanding.
    As a measure of last resort, you may disable using TensorFlow for image classification and facial recognition.

### Command-Line Interface ###

`photoprism help` lists all commands and config options available in the current version:

```
docker-compose exec photoprism photoprism help
```

Use the `--help` flag to see a detailed command description, for example:

```
docker-compose exec photoprism photoprism backup --help
```

!!! tip ""
    Prefixing commands with `docker-compose exec [service name]` runs them inside an app container.
    If this fails with *no container found*, make sure the app has been started,
    its service name is the same, and you are in the folder in which the `docker-compose.yml` 
    file has been saved.

PhotoPrism's command-line interface is well suited for job automation using a
[scheduler](https://dl.photoprism.org/docker/scheduler/).

#### Examples ####

| Action                    | Command                                                   |
| ------------------------- | --------------------------------------------------------- |
| *Start App*               | `docker-compose up -d`                                    |
| *Stop App*                | `docker-compose stop`                                     |
| *Remove App*              | `docker-compose down`                                     |
| *Update App Image*        | `docker-compose pull`                                     |
| *Show App Logs*           | `docker-compose logs --tail=25 -f`                        |
| *Open Terminal*           | `docker-compose exec photoprism bash`                     |
| *Show Config Values*      | `docker-compose exec photoprism photoprism config`        |
| *Show Facial Recognition Subcommands* | `docker-compose exec photoprism photoprism faces help`    |
| *Show User Management Subcommands*    | `docker-compose exec photoprism photoprism users help`    |
| *Reset Database*          | `docker-compose exec photoprism photoprism reset`         |                   
| *Backup Database*         | `docker-compose exec photoprism photoprism backup -a -i`  |                      
| *Restore Database*        | `docker-compose exec photoprism photoprism restore -a -i` |                   
| *Update Index*            | `docker-compose exec photoprism photoprism index`         |                  
| *Import Files*            | `docker-compose exec photoprism photoprism import [path]` |                  

!!! info "Complete Rescan"
    `docker-compose exec photoprism photoprism index -f` rescans all originals, including already indexed and unchanged files. 
    This may be necessary after major upgrades.

*[CLI]: Command-Line Interface