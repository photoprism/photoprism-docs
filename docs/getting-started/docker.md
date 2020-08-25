# Running PhotoPrism with Docker

These instructions are for users who don't like Docker Compose for any reason and prefer pure Docker instead. If you are not
sure, try using [Docker Compose](docker-compose.md) first.

### Step 1: Start the server ###

Open a terminal and run this command after replacing `~/Pictures` with
the folder containing your personal photo and video collection:

```
docker run -d \
  --name photoprism \
  --security-opt seccomp=unconfined \
  --security-opt apparmor=unconfined \
  -p 2342:2342 \
  -e PHOTOPRISM_UPLOAD_NSFW="true" \
  -e PHOTOPRISM_ADMIN_PASSWORD="photoprism" \
  -v /photoprism/storage \
  -v ~/Pictures:/photoprism/originals \
  photoprism/photoprism
```

Now open http://localhost:2342/ in a Web browser to see the user interface.

The initial **password** is `photoprism`. You can change it in Settings or using 
the `photoprism passwd` command in a terminal.

This is a simplified configuration compared to our [Docker Compose](docker-compose.md) example:

* The `/photoprism/import` folder is not [mounted](https://docs.docker.com/storage/bind-mounts/) 
  so that you can't easily access it from your host machine. 
  Uploading files or mounting it via [WebDAV](../user-guide/backup/webdav.md) 
  is still possible.
* Settings, index, sidecar files, and generated thumbnails will be stored 
  in `/photoprism/storage`. 
  You may also [mount](https://docs.docker.com/storage/bind-mounts/)
  this path to a local folder instead of an anonymous volume.

The default port 2342 and other configuration values can be changed as needed,
see [Config Options](config-options.md). 

To enable the read-only mode, add `-e PHOTOPRISM_READONLY="true"`. You may additionally want to 
mount *originals* with a `:ro` flag so that Docker prevents any write operations. Note that this
automatically disables any features that require write permissions, like adding files via Web upload.

Multiple folders can be indexed by mounting them as subfolders e.g. 
`-v ~/Example:/photoprism/originals/Example`.

!!! info
    Your original media files won't be deleted, modified or moved. We might later update metadata in 
    [XMP sidecar files](https://www.adobe.com/products/xmp.html) to
    sync with Adobe Lightroom.
    A JPEG representation might be created for RAW, HEIF, TIFF, PNG, BMP and GIF images in order to render 
    thumbnails and display them in a browser. You can enable read-only mode to prevent this completely, but you will also lose the functionality.

### Step 2: Index your library ###

Go to Library in our Web UI to start indexing or importing.
Alternatively, you can run this command in a terminal to index all files in your *originals* folder:

```
docker exec -ti photoprism photoprism index
```

The index command will automatically create JPEGs from other file types when needed to display them in a browser.
They will be stored in the same folder next to the original using the best possible quality.
You can disable this in Settings. Converting is currently not possible in read-only mode.

Photos will become visible one after another. You can watch the indexer working in the terminal, or the logs tab in Library.

!!! tip
    `photoprism index --all` will re-index all originals, including already indexed and unchanged files. This can be
    useful after updates that add new features.

### Step 3: When you're done... ###

You can stop the server and start it again using the following commands:

```
docker stop photoprism
docker start photoprism
```

To remove the container completely:

```
docker rm -f photoprism
```
