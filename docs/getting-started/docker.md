# Running PhotoPrism with Docker

If you're not sure, try using [Docker Compose](docker-compose.md) first as it requires remembering
less command line parameters, and is generally easier to start with for beginners.

!!! info "Linux"
    Commands may have to be prefixed with `sudo` when not running as root.
    Note that this will point the home directory placeholder `~` to `/root` in your configuration.
    Kernel security modules such as SELinux have been reported to cause
    [issues](https://docs.photoprism.org/getting-started/faq/#why-is-photoprism-getting-stuck-in-a-restart-loop).

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
  -e PHOTOPRISM_ADMIN_PASSWORD="please_change" \
  -v /photoprism/storage \
  -v ~/Pictures:/photoprism/originals \
  photoprism/photoprism
```

!!! danger ""
    Please change `PHOTOPRISM_ADMIN_PASSWORD` so that PhotoPrism starts with a **secure initial password**.
    Never use `photoprism`, or other easy-to-guess passwords, on a public server.
    A minimum length of 4 characters is required.

!!! attention ""
    Make sure there is enough disk space available and verify file system permissions before starting to index:
    The *originals* folder must be readable, while *storage* must be readable and writeable.

Now open http://localhost:2342/ in a Web browser to see the user interface.
Sign in with the user `admin` and the initial password configured via `PHOTOPRISM_ADMIN_PASSWORD`.
You may change it on the [account settings page](../user-guide/settings/account.md),
or using the `photoprism passwd` command in a terminal.
A minimum length of 4 characters is required.

!!! note ""
    It's not possible to **change the initial password** via `PHOTOPRISM_ADMIN_PASSWORD` after PhotoPrism
    has been started for the first time. You may run `docker exec -ti photoprism photoprism reset` in a terminal to
    reset your database for a clean start.

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

Your photos and videos can now be browsed, organized in albums, and shared with others.
You may continue using your favorite tools, like Photoshop or Lightroom,
to edit, add and delete files in the *originals* folder.
Run `photoprism index`, or go to *Library* and click *Start*, to update the index as needed.

Easy, isn't it?

!!! example ""
    **This open-source project is made possible [thanks to our sponsors](https://github.com/photoprism/photoprism/blob/develop/SPONSORS.md).**
    If you enjoy using PhotoPrism, please consider backing us on [Patreon](https://www.patreon.com/photoprism)
    or [GitHub Sponsors](https://github.com/sponsors/photoprism) — especially if you have
    feature requests or need help with using our software.
    Your continued support helps us fund operating costs, provide services like satellite maps,
    and develop new features. Thank you very much! 💜

!!! tip "Reducing Server Load"
    If you're running out of memory - or other system resources - while indexing, please limit the
    [number of workers](https://docs.photoprism.org/getting-started/config-options/) by setting
    `PHOTOPRISM_WORKERS` to a value less than the number of logical CPU cores.
    Also make sure your server has at least 4 GB of [swap](https://opensource.com/article/18/9/swap-space-linux-systems)
    configured so that indexing doesn't cause restarts when there are memory usage spikes.
    Especially the conversion of RAW images and the transcoding of videos are very demanding.
    As a measure of last resort, you may disable using TensorFlow for image classification and facial recognition.

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

### Facial Recognition ###

Existing users may index faces in originals without performing a complete rescan:

```
docker exec -ti photoprism photoprism photoprism faces index
```

For a fresh start e.g. after upgrading from a development preview, remove 
known people and faces before re-indexing:

```
docker exec -ti photoprism photoprism faces reset -f`
```

### Command Reference ###

The help command shows a complete list of commands and config options.
Use the `--help` flag to see a detailed command info
like `docker exec -ti photoprism photoprism backup --help`.

| Action   | Command                                               |
|----------|-------------------------------------------------------|
| Update   | `docker pull photoprism`                              |
| Remove   | `docker rm -f photoprism`                             |
| Logs     | `docker logs --tail=25 -f photoprism`                 |
| Terminal | `docker exec -ti photoprism bash`                     |
| Help     | `docker exec -ti photoprism photoprism help`          |                
| Config   | `docker exec -ti photoprism photoprism config`        |                   
| Reset    | `docker exec -ti photoprism photoprism reset`         |                   
| Backup   | `docker exec -ti photoprism photoprism backup -a -i`  |                      
| Restore  | `docker exec -ti photoprism photoprism restore -a -i` |                   
| Index    | `docker exec -ti photoprism photoprism index`         |                  
| Re-index | `docker exec -ti photoprism photoprism index -f`      |                   
| Import   | `docker exec -ti photoprism photoprism import`        |                  

!!! info "Complete Rescan"
    `photoprism index -f` will re-index all originals, including already indexed and unchanged files. This may be
    necessary after upgrading, especially to new major versions.
