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
  -e PHOTOPRISM_ADMIN_PASSWORD="please-change" \
  -v /photoprism/storage \
  -v ~/Pictures:/photoprism/originals \
  photoprism/photoprism
```

!!! danger "Change Password"
    Please change `PHOTOPRISM_ADMIN_PASSWORD` so that PhotoPrism starts with a secure **initial password**.
    Never use `photoprism`, or other easy-to-guess passwords, on a public server.

Now open http://localhost:2342/ in a Web browser to see the user interface
and sign in using the password set in `PHOTOPRISM_ADMIN_PASSWORD`.
You may change it in Settings, or using the `photoprism passwd` command in a terminal.

This is a simplified configuration compared to our [Docker Compose](docker-compose.md) example:

* The `/photoprism/import` folder is not [mounted](https://docs.docker.com/storage/bind-mounts/) 
  so that you can't easily access it from your host machine. 
  Uploading files or mounting it via [WebDAV](../user-guide/sync/webdav.md) 
  is still possible.
* Settings, index, sidecar files, and thumbnails will be put 
  in `/photoprism/storage`. 
  You may also [mount](https://docs.docker.com/storage/bind-mounts/)
  this path to a local folder instead of an anonymous volume.

The default port 2342 and other configuration values may be changed as needed,
see [Config Options](config-options.md) for details.

Multiple folders can be indexed by mounting them as sub-folders of `/photoprism/originals`:

```
-v ~/Example:/photoprism/originals/Example
``` 

!!! info "Read-Only Mode"
    Running PhotoPrism in read-only mode disables all features that require write permissions,
    like importing, uploading, renaming, and deleting files.
    You may enable it by adding `-e PHOTOPRISM_READONLY="true"`.
    In addition, you may mount the *originals* folder with `:ro` flag so that Docker
    blocks write operations.

!!! attention
    Make sure there is enough disk space available and verify file system permissions before starting to index:
    The *originals* folder must be readable, while *storage* must be readable and writeable.

### Step 2: Index your library ###

Go to *Library* in our Web UI to start indexing or importing.
Alternatively, you can run this command in a terminal to index all files in your *originals* folder:

```
docker exec -ti photoprism photoprism index
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
    `PHOTOPRISM_WORKERS` to a value less than the number of logical CPU cores.
    Also make sure your server has [swap](https://opensource.com/article/18/9/swap-space-linux-systems) 
    configured so that indexing doesn't cause restarts when there are memory usage spikes.
    As a measure of last resort, you may additionally disable image classification using TensorFlow.

!!! info "Complete Rescan"
    `photoprism index --all` will re-index all originals, including already indexed and unchanged files. This may be
    necessary after upgrading, especially to new major versions.

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
