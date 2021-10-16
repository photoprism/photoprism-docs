# Running PhotoPrism with Docker

We recommend using [Docker Compose](docker-compose.md) as it is easier to start with for beginners
and provides more comfort than the pure Docker command-line interface.

!!! info ""
    You're welcome to ask for help in our [community chat](https://gitter.im/browseyourlife/community).
    [Sponsors](../funding.md) receive direct [technical support](https://photoprism.app/contact) via email.

### Step 1: Start the server ###

=== "Linux"

    Open a terminal and run this command to start the app after replacing `~/Pictures` with
    the folder containing your pictures:
    
    ```
    docker run -d \
      --name photoprism \
      --security-opt seccomp=unconfined \
      --security-opt apparmor=unconfined \
      -p 2342:2342 \
      -e PHOTOPRISM_UPLOAD_NSFW="true" \
      -e PHOTOPRISM_ADMIN_PASSWORD="insecure" \
      -v /photoprism/storage \
      -v ~/Pictures:/photoprism/originals \
      photoprism/photoprism
    ```
    
The server port and app [config options](config-options.md) may be changed as needed.
If you provide no database server credentials, a SQLite database file will be created in the
*storage* folder.

!!! danger ""
    Always change `PHOTOPRISM_ADMIN_PASSWORD` so that the app starts with a **secure initial password**.
    Never use easy-to-guess passwords or default values like `insecure` on publicly accessible servers.
    There is no default in case no password was provided. A minimum length of 4 characters is required.

Commands on Linux may have to be prefixed with `sudo` when not running as root.
Note that this will point the home directory placeholder `~` to `/root` in volume mounts.
Kernel security modules such as AppArmor and SELinux have been reported to cause
[issues](troubleshooting.md).

When the app has been started, open the Web UI by navigating to http://localhost:2342/. You should see a login screen.
Sign in with the user `admin` and the password configured via `PHOTOPRISM_ADMIN_PASSWORD`.
You may change it on the [account settings page](../user-guide/settings/account.md).
Enabling [public mode](config-options.md) will disable authentication.

!!! info ""
    If you can't connect, try starting the app without `-d`. This keeps it in the foreground
    and shows log messages for [troubleshooting](troubleshooting.md).
    Should the server already be running, or you see no errors, you may have started it 
    on a different host and/or port. There could also be an issue with your browser, 
    ad blocker, or firewall settings.

!!! tldr ""
    It is not possible to change the password via `PHOTOPRISM_ADMIN_PASSWORD` after the app has been 
    started for the first time. You may run `docker exec -ti photoprism photoprism passwd`
    in a terminal to change an existing password. You can also reset your database for a clean start. 

#### Volumes ####

Since the app is running inside a container, you have to explicitly mount the host folders you want to use.
PhotoPrism won't be able to see folders that have not been mounted. That's an important security feature.

##### /photoprism/originals #####

The *originals* folder contains your original photo and video files.
They are mounted from `~/Pictures` in the example above, where `~` is a placeholder for 
your home directory. Other folders accessible from the host may be [mounted](https://docs.docker.com/storage/bind-mounts/) instead, 
including network drives. 

Multiple folders can be made accessible by mounting them as subfolders:

```
-v ~/Example:/photoprism/originals/Example
``` 

!!! tldr ""
    When you enable *read-only mode*, all features that require write permission to the *originals* folder
    are disabled, in particular import, upload, and delete. Run the app with `-e PHOTOPRISM_READONLY="true"` 
    for this. You can mount a folder with the `:ro` flag to make Docker block write operations as well.

##### /photoprism/storage #####

Cache, session, thumbnail, and sidecar files will be created the *storage* folder, which is mounted as 
an [anonymous volume](https://docs.docker.com/storage/bind-mounts/) in our example. You may want to 
mount a specific host folder instead. Never remove the volume completely so that you don't lose 
these files after restarting or upgrading the container. We recommend placing the *storage* folder 
on a local SSD drive for best performance.

##### /photoprism/import #####

You may optionally mount an *import* folder from which files can be transferred to the *originals* folder
in a structured way that avoids duplicates. Imported files receive a canonical filename and will be
organized by year and month.

!!! tldr ""
    You can safely skip this. Adding files via [Web Upload](../user-guide/library/upload.md)
    and [WebDAV](../user-guide/sync/webdav.md) remains possible, unless [read-only mode](config-options.md)
    is enabled or the [features have been disabled](../user-guide/settings/general.md).

### Step 2: Index your library ###

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
changed, added, or removed. This can also be automated using CLI commands and a [scheduler](https://dl.photoprism.org/docker/scheduler/).

Easy, isn't it?

!!! info ""
    If you're running out of memory - or other system resources - while indexing, try reducing the
    [number of workers](https://docs.photoprism.org/getting-started/config-options/) by setting
    `PHOTOPRISM_WORKERS` to a reasonably small value (depending on the performance of the server).
    Also make sure your server has at least 4 GB of [swap](https://opensource.com/article/18/9/swap-space-linux-systems)
    configured so that indexing doesn't cause restarts when there are memory usage spikes.
    Especially the conversion of RAW images and the transcoding of videos are very demanding.
    As a measure of last resort, you may disable using TensorFlow for image classification and facial recognition.

### Step 3: When you're done... ###

You can stop PhotoPrism and start it again using the following commands:

```
docker stop photoprism
docker start photoprism
```

To remove the container completely:

```
docker rm -f photoprism
```

!!! example ""
    **Back us on [Patreon](https://www.patreon.com/photoprism) or [GitHub Sponsors](https://github.com/sponsors/photoprism).**
    Your continued support helps us provide services like satellite maps and develop new features. Thank you very much! 💜

### Command-Line Interface ###

`photoprism help` lists all commands and [config options](config-options.md) available in the current version:

```
docker exec -ti photoprism photoprism help
```

Use the `--help` flag to see a detailed command description, for example:

```
docker exec -ti photoprism photoprism backup --help
```

!!! info ""
    Prefixing commands with `docker exec -ti [container name]` runs them inside an app container.
    If this fails with *no container found*, make sure the app has been started and 
    its container has the same name.

PhotoPrism's command-line interface is well suited for job automation using a
[scheduler](https://dl.photoprism.org/docker/scheduler/).

#### Examples ####

| Action                        | Command                                                  |
| ----------------------------- | -------------------------------------------------------- |
| *Start App*                   | `docker start photoprism`                                |
| *Stop App*                    | `docker stop photoprism`                                 |
| *Update Container Image*      | `docker pull photoprism/photoprism:latest`               |
| *Uninstall*                   | `docker rm -f photoprism`                                |
| *Show Server Logs*            | `docker logs --tail=100 -f photoprism`                   |
| *Show Config Values*          | `docker exec -ti photoprism photoprism config`           |
| *Reset Database*              | `docker exec -ti photoprism photoprism reset`            |                   
| *Backup Database*             | `docker exec -ti photoprism photoprism backup -a -i`     |                      
| *Restore Database*            | `docker exec -ti photoprism photoprism restore -a -i`    |                   
| *Change Admin Password*       | `docker exec -ti photoprism photoprism passwd`           | 
| *Show User Management Commands*    | `docker exec -ti photoprism photoprism users help`  |
| *Show Facial Recognition Commands* | `docker exec -ti photoprism photoprism faces help`  |
| *Index Faces*                 | `docker exec -ti photoprism photoprism faces index`      |
| *Reset People & Faces*        | `docker exec -ti photoprism photoprism faces reset -f`   |
| *Transcode Videos to AVC*     | `docker exec -ti photoprism photoprism convert`          |
| *Update Index*                | `docker exec -ti photoprism photoprism index --cleanup`  |                  
| *Import Files*                | `docker exec -ti photoprism photoprism import [path]`    |

!!! info "Complete Rescan"
    `docker exec -ti photoprism photoprism index -f` rescans all originals, including already indexed and unchanged files.
    This may be necessary after major upgrades.

*[home directory]: \user\username on Windows, /Users/username on macOS, and /root or /home/username on Linux
*[host]: A physical computer, cloud server, or virtual machine that runs Docker
*[HEIF]: High Efficiency Image File Format
*[RAW]: RAW files contain image data captured during exposure in an unprocessed format
*[Web UI]: A Progressive Web App that can be installed on your home screen and provides a native app-like experience
*[CLI]: Command-Line Interface
*[AVC]: MPEG-4 AVC video compression standard, also known as H.264