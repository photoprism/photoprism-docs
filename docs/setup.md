# Setup and Configuration

## Installation ##

This is the official way to test our development snapshot. We just started working on the UI and features are neither complete or stable. Feedback early in development helps saving a lot of time. We're a small team and need to move fast.

Before you start, make sure you got [Docker](https://store.docker.com/search?type=edition&offering=community) installed on your system. It is available for Mac, Linux and Windows.
Developers can skip this and move on to the [Developer Guide](https://github.com/photoprism/photoprism/wiki).

### Step 1: Configure ###

Download the config file [docker-compose.yml](https://raw.githubusercontent.com/photoprism/photoprism/master/configs/docker-compose.yml) (right click and *Save Link As...*) to a directory of your choice.

By default, a folder named `Photos` in your home directory will be used to store all images. You don't need to create it.

PhotoPrism will also create the following sub-directories in your `Photos` folder: `Import`, `Export` and `Originals`. Copy existing photos to `Import`, not directly to `Originals` as they need to be renamed and indexed in order to remove duplicates.
Files that can not be imported - like videos - will stay in the `Import` directory, nothing gets lost.

If you prefer to use different directory names, you can change them in `docker-compose.yml`. See inline comments for instructions.

### Step 2: Run ###

Open a terminal, go to the directory in which you saved the config file and run this command to start the application:

```
docker-compose up -d
```

The Web frontend is now available at http://localhost:2342/. The port can be changed in `docker-compose.yml`. Remember to run `docker-compose restart` every time you touch the config.

### Step 3: Import ###

Connect to the application container and run `photoprism import` after putting files in the `Import` folder:

```
docker-compose exec photoprism bash
photoprism import
```

You should now be able to see your photos. You can continue using your favorite tools like Photoshop or Lightroom
to edit images in the `Originals` folder. Run `photoprism index` to reindex them as needed.
Even deleting and adding is possible, if you stick to the naming scheme. Easy, isn't it?

## Updating ##

Open a terminal, go to the directory in which you saved `docker-compose.yml` and run the following commands to update your version to the latest development snapshot:

```bash
docker-compose down
docker-compose pull photoprism
docker-compose up -d
```

Pulling a new version can take several minutes, depending on your internet connection. The final release will be smaller.

## Troubleshooting ##

If the application can not be opened in the browser or the container doesn't start at all, you might have found a bug,
you might be using an outdated container image or some of your directories are not readable or writable (check permissions).

Try **not** to start the app in detached mode (`-d`) to see errors:

```
docker-compose up
```

You're welcome to send a full report to hello@photoprism.org so that we can help you.
