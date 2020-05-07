# Setup using Docker Compose

To simplify running PhotoPrism on a server, we strongly recommend using [Docker Compose](https://docs.docker.com/compose/).

Before you start, make sure you have [Docker](https://store.docker.com/search?type=edition&offering=community) installed on your system. It is available for Mac, Linux and Windows.
Developers can skip this and move on to the [Developer Guide](https://github.com/photoprism/photoprism/wiki).

In addition, we plan to ship the final app as a single binary for users that don't know or like Docker.
An image for the [Raspberry Pi](raspberry-pi.md) is now available too.

### Step 1: Configure ###

Download [docker-compose.yml](https://dl.photoprism.org/docker/docker-compose.yml) (right click and *Save Link As...* or use `wget`) to a directory of your choice and edit directory names as needed:

```
wget https://dl.photoprism.org/docker/docker-compose.yml
```

By default, a folder named `Pictures` in your home directory will be used to store all images and sidecar files. You don't need to create it.

PhotoPrism will also create `Import` and `Originals` in this folder: You may copy photos to *import* and copy or move them from there to avoid duplicates.
Files that cannot be imported will stay in the *import* directory, nothing gets lost. Using import is strictly optional and can be disabled in Settings.

To enable read-only mode, set `PHOTOPRISM_READONLY` to `true`. You may additionally want to 
mount your *originals* directory with a `:ro` flag so that Docker prevents any write operations.
    
!!! info
    Your image files won't be deleted, modified or moved. We might later update metadata in 
    [XMP sidecar files](https://www.adobe.com/products/xmp.html) to
    sync with Adobe Lightroom.
    A JPEG representation might be created for RAW, HEIF, TIFF, PNG, BMP and GIF images in order to render 
    thumbnails. You can enable read-only mode to prevent this completely, but you will also lose the functionality.

### Step 2: Start the server ###

Open a terminal, go to the directory in which you saved the config file and run this command to start the server:

```
docker-compose up -d
```

Now open http://localhost:2342/ in a Web browser to see the user interface. The default password is "photoprism".

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

Go to Library in our Web UI to start indexing or importing. Alternatively, you can run this command 
in a terminal to index all files in your *originals* folder:

```
docker-compose exec photoprism photoprism index -c
```

The `-c` flag will automatically create JPEGs from other file types when needed to display them in a browser.
They will be stored in the same folder next to the original using the best possible quality.
Converting is currently not possible in read-only mode.

Photos will become visible one after another. You can watch the indexer working in the terminal, or the logs tab in Library.

!!! tip
    `index --all` will re-index existing files, for example after updates.

To import files, run `photoprism import` after putting them in the *import* folder:

```
docker-compose exec photoprism photoprism import
```

For a list of commands and config options run

```
docker-compose exec photoprism photoprism help
```

You should now be able to see your photos. You can continue using your favorite tools like Photoshop or Lightroom
to edit images in the *originals* folder. Run `photoprism index` to reindex them as needed.
Even deleting and adding is possible. Easy, isn't it?
