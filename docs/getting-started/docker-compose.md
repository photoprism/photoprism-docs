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

!!! attention "Change Password"
    Please change `PHOTOPRISM_ADMIN_PASSWORD` so that PhotoPrism starts with a secure **initial password**.
    Never use `photoprism`, or other easy-to-guess passwords, on a public server.
    A minimum length of 4 characters is required.
	
Your personal photo and video collection will be mounted from `~/Pictures` by default,
where `~` is a placeholder for your [home directory](https://en.wikipedia.org/wiki/Home_directory).
We'll refer to this as the *originals* folder.

You may mount any folder accessible from your computer, including network drives.
Note that PhotoPrism won't be able to see folders that have not been mounted.
Multiple folders can be indexed by mounting them as sub-folders of `/photoprism/originals`:

```
volumes:
  - "~/friends:/photoprism/originals/friends"
  - "/media/photos:/photoprism/originals/media"
```

The *import* folder points to `~/Import` by default, so that you can easily access it.
If you don't need this feature, e.g. because you manage all files manually or 
use a different tool for importing, you can safely remove the volume. Using import is strictly 
optional.

Settings, index, sidecar files, and thumbnails will be put in `storage` by default. 
You may use an [anonymous volume](https://docs.docker.com/storage/bind-mounts/) or absolute path instead, 
just don't remove it completely so that you don't lose your index and albums after restarting or 
upgrading the container.

!!! info "Read-Only Mode"
    Running PhotoPrism in read-only mode disables all features that require write permissions,
    like importing, uploading, renaming, and deleting files.
    You may enable it by setting `PHOTOPRISM_READONLY` to `"true"`.
    In addition, you may mount the *originals* folder with `:ro` flag so that Docker 
    blocks write operations.

!!! attention
    Make sure there is enough disk space available and verify file system permissions before starting to index:
    The *originals* folder must be readable, while *storage* must be readable and writeable.

### Step 2: Start the server ###

Open a terminal, go to the folder in which you saved the config file and run this command to start the server:

```
docker-compose up -d
```

Now open http://localhost:2342/ in a Web browser to see the user interface
and sign in with `admin` as the user and the password set in `PHOTOPRISM_ADMIN_PASSWORD`.
You may change it in Settings, or using the `photoprism passwd` command in a terminal.
A minimum length of 4 characters is required.

The port and other basic settings may be changed in `docker-compose.yml`.
Remember to stop and re-create the container whenever configuration values have been changed:

```
docker-compose stop photoprism
docker-compose up -d photoprism
```

### Step 3: Index your library ###

Go to *Library* in our Web UI to start indexing or importing. Alternatively, you may run this command 
in a terminal to index all files in your *originals* folder:

```
docker-compose exec photoprism photoprism index
```

While indexing, a JPEG sidecar file may automatically be created for RAW, HEIF, TIFF, PNG, BMP, 
and GIF files. It is required for classification and resampling. By default, it will be created
in the *storage* folder, so that your originals can be mounted read-only.
You may configure PhotoPrism to store it in the same folder, next to the original, instead.

Pictures will become visible one after another. You can watch the indexer working in the terminal, 
or the *Logs* tab in *Library*.

Your photos and videos can now be browsed, organized in albums, and shared with others.
You may continue using your favorite tools, like Photoshop or Lightroom,
to edit, add and delete files in the *originals* folder.
Run `photoprism index`, or go to *Library* and click *Start*, to update the index as needed.

Easy, isn't it?

!!! info "This open-source project is made possible thanks to our generous sponsors 🌈"
    If you enjoy using PhotoPrism, please consider supporting us via [Patreon](https://www.patreon.com/photoprism)
    or [GitHub Sponsors](https://github.com/sponsors/photoprism) — especially if you have
    feature requests or need help with using our software.
    Your continued support helps us fund operating costs, external services like satellite maps,
    and develop new features. Thank you very much!

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
