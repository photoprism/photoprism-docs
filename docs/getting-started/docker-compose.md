# Setup Using Docker Compose

Before you start, make sure you have [Docker](https://store.docker.com/search?type=edition&offering=community) installed on your system. 
It is available for Mac, Linux and Windows.
Developers can skip this and move on to the [Developer Guide](../developer-guide/index.md).

An image for the [Raspberry Pi](raspberry-pi.md) is available as well.
In addition, we plan to provide a single binary.

!!! info "Windows"
    Windows users may need to [disable](img/docker-disable-wsl2.jpg) the WSL 2 based engine in *Docker Settings > General*
    to mount drives other than `C:`. Please use this [docker-compose.yml](https://dl.photoprism.org/docker/windows/docker-compose.yml)
    example to get started and [increase](img/docker-resources-advanced.jpg) the Docker memory limit 
    to 4 GB or more, as the default of 2 GB may reduce indexing performance or cause restarts.

!!! info "macOS"
    macOS users should [increase](img/docker-resources-advanced.jpg) the Docker memory limit to 4 GB or more,
    as the default of 2 GB may reduce indexing performance or cause restarts.
    Please use this [docker-compose.yml](https://dl.photoprism.org/docker/macos/docker-compose.yml)
    example to get started.

### Step 1: Configure ###

Download our [docker-compose.yml](https://dl.photoprism.org/docker/docker-compose.yml) file
(right click and *Save Link As...* or use `wget`) to a folder of your choice,
and change the [configuration](config-options.md) as needed:

```
wget https://dl.photoprism.org/docker/docker-compose.yml
```

!!! attention
    Please change `PHOTOPRISM_ADMIN_PASSWORD` so that PhotoPrism starts with a secure **initial password**.
    Never use `photoprism` or `insecure` as password if you're running it on a public server.
	
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

Settings, index, sidecar files, and thumbnails will be stored in a `storage` sub-folder by default. 
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
    Please verify file system permissions before starting to index: 
    The *originals* folder must be readable, while *storage* must be readable and writeable.

### Step 2: Start the server ###

Open a terminal, go to the folder in which you saved the config file and run this command to start the server:

```
docker-compose up -d
```

Now open http://localhost:2342/ in a Web browser to see the user interface
and sign in using the password set in `PHOTOPRISM_ADMIN_PASSWORD`.
You may change it in Settings, or using the `photoprism passwd` command in a terminal.

The port and other basic settings can be changed in `docker-compose.yml`.
Remember to stop and re-create the container whenever configuration values changed:

```
docker-compose stop photoprism
docker-compose up -d --no-deps photoprism
```

To also update the Docker image:

```
docker-compose pull photoprism
docker-compose stop photoprism
docker-compose up -d --no-deps photoprism
```

Be aware that later builds may expect more or different configuration values.
We always keep our [example configuration](https://dl.photoprism.org/docker/) up to date for reference.
In addition, you can run `photoprism help` inside the container to see all options incl. 
environment variable names and a short description.

### Step 3: Index your library ###

Go to *Library* in our Web UI to start indexing or importing. Alternatively, you can run this command 
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

!!! tip "Reducing Server Load"
    If you're running out of memory - or other system resources - while indexing, please limit the 
    [number of workers](https://docs.photoprism.org/getting-started/config-options/) by setting
    a value less than the number of logical CPU cores for `PHOTOPRISM_WORKERS` in `docker-compose.yml`.
    Also make sure your server has [swap](https://opensource.com/article/18/9/swap-space-linux-systems) 
    configured so that indexing doesn't cause restarts when there are memory usage spikes.
    As a measure of last resort, you may additionally disable image classification using TensorFlow.

!!! info "Complete Rescan"
    `photoprism index --all` will re-index all originals, including already indexed and unchanged files. This may be
    necessary after upgrading, especially to new major versions.
    
To import files, run `photoprism import` after putting them in the *import* folder:

```
docker-compose exec photoprism photoprism import
```

For a list of commands and config options run:

```
docker-compose exec photoprism photoprism help
```

Your photos and videos can now be browsed, organized in albums, and shared with others.
You may continue using your favorite tools, like Photoshop or Lightroom,
to edit, add and delete files in the *originals* folder. 
Run `photoprism index`, or go to *Library* and click *Start*, to update the index as needed.
Easy, isn't it?
