# Getting started with PhotoPrism

This is the official way to test our development snapshot. We just started working on the UI and features are neither complete or stable. Feedback early in development helps saving a lot of time. We're a small team and need to move fast.

Before you start, make sure you got [Docker](https://store.docker.com/search?type=edition&offering=community) installed on your system. It is available for Mac, Linux and Windows.
Developers can skip this and move on to the [Developer Guide](https://github.com/photoprism/photoprism/wiki/Developer-Guide) in our [Wiki](https://github.com/photoprism/photoprism/wiki).

**Step 1:** Download [docker-compose.prod.yml](https://github.com/photoprism/photoprism/blob/master/docker-compose.prod.yml), rename it to `docker-compose.yml` and set the default photo path `~/Photos` to whatever directory you want to use on your local computer:

```yaml
    volumes:
        - ~/Photos:/Photos
```

PhotoPrism will create the following sub-directories in your photo path: `Import`, `Export` and `Originals`. Copy existing photos to `Import`, not directly to `Originals` as they need to be renamed and indexed in order to remove duplicates.
Files that can not be imported - like videos - will stay in the `Import` directory, nothing gets lost.

**Step 2:** Start PhotoPrism using `docker-compose` in the same directory:

```bash
docker-compose up -d
```

The Web frontend is now available at http://localhost/. The port can be changed in `docker-compose.yml` if needed. Remember to run `docker-compose restart` every time you change the config.

**Step 3:** Open a terminal to import photos:

```bash
docker-compose exec photoprism bash
photoprism import
```