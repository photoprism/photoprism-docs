# For the early birds

You are welcome to get an impression and provide early feedback.
We've set up a public demo at [demo.photoprism.org](https://demo.photoprism.org) for you to play with.

Note that this is work in progress. We do our best to provide a complete, stable version. 
[Financial support](funding.md) makes a huge difference and enables us to spend more time with this project.

Leave your email to get a [release notification](https://goo.gl/forms/KBPVGl9PCsOKrAv33).

If you have a question, don't hesitate to ask in our [help forum](https://groups.google.com/a/photoprism.org/forum/#!forum/help)
or [contact us via email](mailto:hello@photoprism.org).

## Browse your photos ##

Before you start, make sure you have [Docker](https://store.docker.com/search?type=edition&offering=community) installed on your system. It is available for Mac, Linux and Windows.
Developers can skip this and move on to the [Developer Guide](https://github.com/photoprism/photoprism/wiki).
It also contains instructions for running our container image via [Docker Compose](https://github.com/photoprism/photoprism/wiki/Docker-Compose).

In addition, we plan to ship the final app as a single binary for users that don't know or like Docker.
An [ARM image](https://github.com/photoprism/photoprism/issues/109) for Raspberry Pi users is in the works.

### Step 1: Start the server ###

Open a terminal and run this command after replacing *~/Pictures* with
the folder containing your photos:

```
docker run -d \
  --name photoprism \
  -p 2342:2342 \
  -v ~/Pictures:/home/photoprism/Pictures/Originals \
  photoprism/photoprism
```

The default port 2342 can be changed as needed. Also, you can add the `:ro` (read
only) parameters to the `-v` volume line if you want to. 

!!! info
    Your image files won't be deleted, modified or moved. We might later update metadata in XMP sidecar files to
    sync with Adobe Lightroom. You should still be careful as this software is not stable yet. 
    A JPEG representation might be created for RAW images in order to render thumbnails. You can enable read-only mode 
    to prevent this completely.

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
    
!!! info    
    Due to popular request, our latest release supports PNG, BMP, GIF and TIFF files. 
    Be aware that files those formats often don't contain useful metadata and are typically 
    used for screenshots, charts, graphs and icons only.

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

## Run our demo ##

For a quick test, you can start a demo that comes with pre-indexed photos:

```
docker run -p 2342:2342 -d --name demo photoprism/demo
```

After running the command, open http://localhost:2342/ in a Web browser.
It may take a few seconds to become available.

To stop and remove the container:

```
docker rm -f demo
```

## Updating ##

Open a terminal and run the following command to pull the latest container image:

```
docker pull photoprism/photoprism:latest
```

Pulling a new version can take several minutes, depending on your internet connection.
You can use [Watchtower](https://github.com/containrrr/watchtower) to automatically update the image which is how our
[public demo](https://demo.photoprism.org/) stays up-to-date.

!!! info
    Our database schema still changes a lot as we do performance optimizations and add features.
    Therefore we cannot provide a smooth upgrade path and you should be prepared
    to delete your current database and re-index.
    To spare you a disappointment, we kindly advise you not to index large photo 
    collections at the moment.
