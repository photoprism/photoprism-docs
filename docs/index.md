# Getting started with PhotoPrism

This is the official way to test our development snapshot. We just started working on the UI and features are neither complete or stable. Feedback early in development helps saving a lot of time. We're a small team and need to move fast.

Before you start, make sure you got [Docker](https://store.docker.com/search?type=edition&offering=community) installed on your system. It is available for Mac, Linux and Windows.
Developers can skip this and move on to the [Developer Guide](https://github.com/photoprism/photoprism/wiki/Developer-Guide) in our [Wiki](https://github.com/photoprism/photoprism/wiki).

**Step 1:** Download [docker-compose.yml](https://raw.githubusercontent.com/photoprism/photoprism/master/configs/docker-compose.yml) (right click and *Save Link As...*) to a directory of your choice.

By default, a folder named `Photos` in your home directory will be used to store all images. You don't need to create it.

PhotoPrism will also create the following sub-directories in your photo path: `Import`, `Export` and `Originals`. Copy existing photos to `Import`, not directly to `Originals` as they need to be renamed and indexed in order to remove duplicates.
Files that can not be imported - like videos - will stay in the `Import` directory, nothing gets lost.

If you prefer to use different directory names, you can change them in `docker-compose.yml`. See inline comments for instructions.

**Step 2:** Start PhotoPrism using `docker-compose` in the same directory:

```bash
docker-compose up -d
```

The Web frontend is now available at http://localhost:2342/. The port can be changed in `docker-compose.yml` if needed. Remember to run `docker-compose restart` every time you change the config.

**Step 3:** Open a terminal to import photos:

```bash
docker-compose exec photoprism bash
photoprism import
```

You should now be able to see your photos.

Contribute
----------

If you have a bug or an idea, read the [contributing guidelines](https://github.com/photoprism/photoprism/blob/master/CONTRIBUTING.md) before opening an issue.
Issues labeled `help wanted` or `good first issue` can be good first contributions.

The best way to get in touch is to write an email to hello@photoprism.org or join our [Telegram](https://t.me/joinchat/B8AmeBAUEugGszzuklsj5w) group. We'd love to hear from you!