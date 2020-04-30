# Running PhotoPrism with Docker

These instructions are for users who don't like Docker Compose for any reason and prefer pure Docker instead. If you are not
sure, try using [Docker Compose](docker-compose.md) first.

### Step 1: Start the server ###

Open a terminal and run this command after replacing *~/Pictures* with
the folder containing your photos:

```
docker run -d \
  --name photoprism \
  -p 2342:2342 \
  -v ~/Pictures:/photoprism/originals \
  photoprism/photoprism
```

The default port 2342 can be changed as needed. Adding a `:ro` flag to the `-v` volume 
mounts it read only. 

!!! info
    Your image files won't be deleted, modified or moved. We might later update metadata in 
    [XMP sidecar files](https://www.adobe.com/products/xmp.html) to
    sync with Adobe Lightroom.
    A JPEG representation might be created for RAW, HEIF, TIFF, PNG, BMP and GIF images in order to render 
    thumbnails. You can enable read-only mode to prevent this completely, but you will also lose the functionality.

Now open http://localhost:2342/ in a Web browser to see the user interface. The default password is "photoprism".

### Step 2: Index photos ###

There won't be any search results before you have indexed your photos. You can either do this using
our comfortable Web UI or in a terminal:

```
docker exec -ti photoprism photoprism index
```

Photos will become visible one after another. You can watch the indexer working in the terminal 
or the logs tab (Library).

!!! attention
    PhotoPrism and Web browsers in general can not display RAW image files. They need to be converted, 
    which is what our import and convert commands do. You'll find a checkbox for this step in our Web UI
    (disabled in read-only mode).

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
