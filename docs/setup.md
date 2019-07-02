# For the early birds

You are welcome to get an impression and provide early feedback.
We've set up a public demo at [demo.photoprism.org](https://demo.photoprism.org) for you to play with.

Note that we just started working on the UI and features are neither complete nor stable.
We're a small team and move fast. Leave your email to get a [release notification](https://goo.gl/forms/KBPVGl9PCsOKrAv33).

If you have a question, don't hesitate to ask in our [help forum](https://groups.google.com/a/photoprism.org/forum/#!forum/help)
or [contact us via email](mailto:hello@photoprism.org).

## Browse your photos ##

Before you start, make sure you have [Docker](https://store.docker.com/search?type=edition&offering=community) installed on your system. It is available for Mac, Linux and Windows.
Developers can skip this and move on to the [Developer Guide](https://github.com/photoprism/photoprism/wiki).
It also contains instructions for running our container image via [Docker Compose](https://github.com/photoprism/photoprism/wiki/Docker-Compose).
We plan to ship the final app as a single binary including all dependencies.

### Step 1: Start the server ###

Open a terminal and run this command after replacing *~/Pictures* with
the folder containing your photos:

```
docker run -p 2342:2342 -d --name photoprism \
  -v ~/Pictures:/home/photoprism/Pictures/Originals photoprism/photoprism
```

The default port 2342 can be changed as needed.

!!! info
    Your files won't be deleted or moved. You should still be careful
    as this software is not stable yet. A JPEG representation might be created
    for RAW images in order to render thumbnails. You can enable read-only mode 
    to prevent this completely.

Now open http://localhost:2342/ in a Web browser to see the user interface.

### Step 2: Index photos ###

There won't be any search results until you start indexing your photos:

```
docker exec -ti photoprism photoprism index
```

Photos will become visible one after another.
You can watch the indexer working in the terminal.

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

## Troubleshooting ##

If the application can not be opened in the browser or the container doesn't start at all, you might have found a bug,
you might be using an outdated container image or your folder is not readable (check permissions).

You're welcome to send a full report to help@photoprism.org so that we can assist you.
