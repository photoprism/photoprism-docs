# Setup Using Docker Compose

Before you start, make sure you have [Docker](https://store.docker.com/search?type=edition&offering=community) installed on your system. 
It is available for Mac, Linux and Windows.
Developers may skip this and move on to the [Developer Guide](../developer-guide/index.md).

We plan to provide downloadable installation packages for future releases.

!!! note "Windows"
    Windows users may need to [disable](img/docker-disable-wsl2.jpg) the WSL 2 based engine in *Docker Settings > General*
    to mount drives other than `C:`. Please use this [docker-compose.yml](https://dl.photoprism.org/docker/windows/docker-compose.yml)
    example to get started and [increase](img/docker-resources-advanced.jpg) the Docker memory limit 
    to 4 GB or more, as the default of 2 GB may reduce indexing performance or cause restarts.

!!! note "macOS"
    macOS users should [increase](img/docker-resources-advanced.jpg) the Docker memory limit to 4 GB or more,
    as the default of 2 GB may reduce indexing performance or cause restarts.
    Please use this [docker-compose.yml](https://dl.photoprism.org/docker/macos/docker-compose.yml)
    example to get started.

!!! note "Linux & Raspberry Pi"
    Our latest release comes as a single [multi-arch image](https://hub.docker.com/r/photoprism/photoprism)
    for AMD64, ARM64, and ARMv7. If your device meets the [system requirements](raspberry-pi.md),
    mostly the same installation instructions as for regular Linux servers apply. 
    ARMv7 users need an [alternative MariaDB image](https://hub.docker.com/r/linuxserver/mariadb) 
    as the [official image](https://hub.docker.com/_/mariadb) is available for AMD64 and ARM64 only.
    Commands may have to be prefixed with `sudo` when not running as root.
    Note that this will point the home directory placeholder `~` to `/root` in your configuration.
    Kernel security modules such as SELinux have been reported to cause 
    [issues](https://docs.photoprism.org/getting-started/faq/#why-is-photoprism-getting-stuck-in-a-restart-loop).

### Step 1: Configure ###

Download our [docker-compose.yml](https://dl.photoprism.org/docker/docker-compose.yml) file
(right click and *Save Link As...* or use `wget`) to a folder of your choice,
and change the [configuration](config-options.md) as needed:

```
wget https://dl.photoprism.org/docker/docker-compose.yml
```

!!! danger ""
    Always change `PHOTOPRISM_ADMIN_PASSWORD` so that PhotoPrism starts with a **secure initial password**.
    Never use easy-to-guess passwords or default values like `insecure` on publicly accessible servers.
    A minimum length of 4 characters is required.
	
Your pictures will be mounted from `~/Pictures` by default, where `~` is a placeholder 
for your [home directory](https://en.wikipedia.org/wiki/Home_directory). Its absolute path depends on your
operating system and username.
We'll refer to `/photoprism/originals` as the *originals* folder as it points to your original photo and video files.

You may connect it to any folder accessible from the host, including network drives.
Since PhotoPrism is running inside a container, it won't be able to see folders that have not been mounted.
That's an important security feature.

Multiple folders can be made accessible by mounting them as subfolders like this:

```
volumes:
  - "~/friends:/photoprism/originals/friends"
  - "/media/photos:/photoprism/originals/media"
```

Mounting an *import* folder for adding new files to your library is optional. If you prefer a different workflow 
or read-only mode is enabled, you can skip this.

Cache, session, thumbnail, and sidecar files will be created in the *storage* folder. Never remove the volume from
your `docker-compose.yml` file so that you don't lose these files after restarting or upgrading the container.

!!! info "Read-Only Mode"
    Running PhotoPrism in read-only mode disables all features that require write permissions,
    like importing, uploading, renaming, and deleting files.
    You may enable it by setting `PHOTOPRISM_READONLY` to `"true"`.
    In addition, you may mount the *originals* folder with `:ro` flag so that Docker 
    blocks write operations.

### Step 2: Start the server ###

Open a terminal and change to the directory in which the `docker-compose.yml` file has been saved.
Use this command to start the server in the background and keep it running:

```
docker-compose up -d
```
 
Now open http://localhost:2342/ in a browser to see the Web UI.
Sign in with the user `admin` and the initial password configured via `PHOTOPRISM_ADMIN_PASSWORD`.
You may change it on the [account settings page](../user-guide/settings/account.md), 
or using the `photoprism passwd` command in a terminal.
Enabling [public mode](config-options.md) will disable authentication.

!!! note ""
    It's not possible to **change the initial password** via `PHOTOPRISM_ADMIN_PASSWORD` after PhotoPrism 
    has been started for the first time. The terminal command `docker-compose exec photoprism photoprism reset`
    will reset your database for a clean start. Ensure you're in the right directory and the container is running 
    before using it.

In case you can't connect, try starting the server without `-d` so that you see log messages for troubleshooting.
PhotoPrism will report specific issues like bad folder permissions, or when it can't connect to the database.

The server port and other basic settings may be changed in `docker-compose.yml` at any time.
Remember to properly restart the container whenever it has been changed:

```
docker-compose stop photoprism
docker-compose up -d photoprism
```

### Step 3: Index your library ###

!!! attention ""
    Ensure there is enough disk space available for creating thumbnails and verify file system permissions
    before starting to index: Files in the *originals* folder must be readable, while the *storage* folder
    including all subdirectories must be readable and writeable.

Go to *Library* in the Web UI to start indexing your pictures.

While indexing, JPEG sidecar files may be created for originals in other formats such as RAW and HEIF. 
This is required for image classification, facial recognition, and for displaying them in a Web browser. 
Sidecar and thumbnail files will be added to the *storage* folder, so that your *originals* folder won't be modified.

Pictures will become visible one after another. Open the *Logs* tab in *Library* 
to watch the indexer working.

Of course, you can continue using your favorite tools for processing RAW files, editing metadata, 
or importing new shots. Go to *Library* and click *Start* to update the index after files have been 
changed, added, or removed. This can also be automated using a scheduler and PhotoPrism's CLI commands.

Easy, isn't it?

!!! example ""
    **This open-source project is made possible [thanks to our sponsors](https://github.com/photoprism/photoprism/blob/develop/SPONSORS.md).**
    If you enjoy using PhotoPrism, please consider backing us on [Patreon](https://www.patreon.com/photoprism)
    or [GitHub Sponsors](https://github.com/sponsors/photoprism).
    Your continued support helps us fund operating costs, provide services like satellite maps,
    and develop new features. Thank you very much! 💜

!!! tip "Reducing Server Load"
    If you're running out of memory - or other system resources - while indexing, please limit the 
    [number of workers](https://docs.photoprism.org/getting-started/config-options/) by setting
    `PHOTOPRISM_WORKERS` to a value less than the number of logical CPU cores in `docker-compose.yml`.
    Also make sure your server has at least 4 GB of [swap](https://opensource.com/article/18/9/swap-space-linux-systems) 
    configured so that indexing doesn't cause restarts when there are memory usage spikes.
    Especially the conversion of RAW images and the transcoding of videos are very demanding.
    As a measure of last resort, you may disable using TensorFlow for image classification and facial recognition.

### Facial Recognition ###

Existing users may index faces in originals without performing a complete rescan:

```
docker-compose exec photoprism photoprism faces index
```

For a fresh start e.g. after upgrading from a development preview, remove
known people and faces before re-indexing:

```
docker-compose exec photoprism photoprism faces reset -f
```

### Command Reference ###

The help command shows a complete list of commands and config options.
Use the `--help` flag to see a detailed command info 
like `docker-compose exec photoprism photoprism backup --help`.

| Action   | Command                                                   |
|----------|-----------------------------------------------------------|
| Start    | `docker-compose up -d`                                    |
| Stop     | `docker-compose stop`                                     |
| Update   | `docker-compose pull`                                     |
| Logs     | `docker-compose logs --tail=25 -f`                        |
| Terminal | `docker-compose exec photoprism bash`                     |
| Help     | `docker-compose exec photoprism photoprism help`          |                
| Config   | `docker-compose exec photoprism photoprism config`        |
| Reset    | `docker-compose exec photoprism photoprism reset`         |                   
| Backup   | `docker-compose exec photoprism photoprism backup -a -i`  |                      
| Restore  | `docker-compose exec photoprism photoprism restore -a -i` |                   
| Index    | `docker-compose exec photoprism photoprism index`         |                  
| Re-index | `docker-compose exec photoprism photoprism index -f`      |                   
| Import   | `docker-compose exec photoprism photoprism import`        |                  

!!! info "Complete Rescan"
    `photoprism index -f` will re-index all originals, including already indexed and unchanged files. This may be
    necessary after upgrading, especially to new major versions.
