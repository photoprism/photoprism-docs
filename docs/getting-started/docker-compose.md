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

By default, a folder named `Photos` in your home directory will be used to store all images. You don't need to create it.

PhotoPrism will also create the following sub-directories in your `Photos` folder: `Import`, `Export` and `Originals`. Copy photos to `Import` and import them from there, if you want to avoid duplicates.
Files that can not be imported - like videos - will stay in the `Import` directory, nothing gets lost.

To enable read-only mode, set `PHOTOPRISM_READONLY` to `true`. You may additionally want to 
mount your originals directory with a `:ro` flag so that Docker prevents any write operations.
    
!!! info
    Your image files won't be deleted, modified or moved. We might later update metadata in 
    [XMP sidecar files](https://www.adobe.com/products/xmp.html) to
    sync with Adobe Lightroom.
    A JPEG representation might be created for RAW, HEIF, TIFF, PNG, BMP and GIF images in order to render 
    thumbnails. You can enable read-only mode to prevent this completely, but you will also lose the functionality.

### Step 2: Run ###

Open a terminal, go to the directory in which you saved the config file and run this command to start the server:

```
docker-compose up -d
```

Now open http://localhost:2342/ in a Web browser to see the user interface. The default password is "photoprism".

The port can be changed in `docker-compose.yml`. Remember to run `docker-compose restart` after changing the configuration. 

### Step 3: Import ###

Import photos from the Web UI or connect to the application container and run `photoprism import` after putting files in the `Import` folder:

```
docker-compose exec photoprism bash
photoprism import
```

!!! attention
    PhotoPrism and Web browsers in general can not display RAW image files. They need to be converted, 
    which is what our import and convert commands do. You'll find a checkbox for this step in our Web UI
    (disabled in read-only mode).

To index photos in the `Originals` folder:

```
photoprism index
```

!!! tip
    `photoprism index --all` will re-index existing files, for example after updates.

You should now be able to see your photos. You can continue using your favorite tools like Photoshop or Lightroom
to edit images in the `Originals` folder. Run `photoprism index` to reindex them as needed.
Even deleting and adding is possible. Easy, isn't it?
