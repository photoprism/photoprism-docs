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
    Always change `PHOTOPRISM_ADMIN_PASSWORD` so that PhotoPrism starts with a **secure initial password**.
    Never use easy-to-guess passwords or default values like `insecure` on publicly accessible servers.
    A minimum length of 4 characters is required.

Now open http://localhost:2342/ in a Web browser to see the user interface.
Sign in with the user `admin` and the initial password configured via `PHOTOPRISM_ADMIN_PASSWORD`.
You may change it on the [account settings page](../user-guide/settings/account.md),
or using the `photoprism passwd` command in a terminal.
Enabling [public mode](config-options.md) will disable authentication.

!!! note ""
    It's not possible to **change the initial password** via `PHOTOPRISM_ADMIN_PASSWORD` after PhotoPrism
    has been started for the first time. You may run `docker exec -ti photoprism photoprism reset` in a terminal to
    reset your database for a clean start.

In case you can't connect, try starting the server without `-d` so that you see log messages for troubleshooting.
PhotoPrism will report specific issues like bad folder permissions, or when it can't connect to the database.

This is a simplified configuration compared to our [Docker Compose](docker-compose.md) example:

No host folder has been [mounted](https://docs.docker.com/storage/bind-mounts/) to `/photoprism/import`.
Importing files via Web upload or [WebDAV](../user-guide/sync/webdav.md) is still possible.

Cache, session, thumbnail, and sidecar files will be created in `/photoprism/storage`, which is mounted as 
an [anonymous volume](https://docs.docker.com/storage/bind-mounts/) in our example. You may want to 
mount a specific host directory instead. Never remove the volume completely so that you don't lose your 
index and other these files after restarting or upgrading the container.

The default port 2342 and other configuration values may be changed as needed,
see [Config Options](config-options.md) for details.

Multiple folders can be made accessible by mounting them as subfolders:

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

!!! attention ""
    Ensure there is enough disk space available for creating thumbnails and verify file system permissions
    before starting to index: Files in the *originals* folder must be readable, while the *storage* folder
    including all subdirectories must be readable and writeable.

Open the Web UI, go to *Library* and click *Start* to start indexing your pictures.

While indexing, JPEG sidecar files may be created for originals in other formats such as RAW and HEIF.
This is required for image classification, facial recognition, and for displaying them in a Web browser.
Sidecar and thumbnail files will be added to the *storage* folder, so that your *originals* folder won't be modified.

Pictures will become visible one after another. Open the *Logs* tab in *Library*
to watch the indexer working.

Of course, you can continue using your favorite tools for processing RAW files, editing metadata,
or importing new shots. Go to *Library* and click *Start* to update the index after files have been
changed, added, or removed. This can also be automated using terminal commands and a scheduler.

Easy, isn't it?

!!! example ""
    **This open-source project is made possible [thanks to our sponsors](https://github.com/photoprism/photoprism/blob/develop/SPONSORS.md).**
    If you enjoy using PhotoPrism, please consider backing us on [Patreon](https://www.patreon.com/photoprism)
    or [GitHub Sponsors](https://github.com/sponsors/photoprism).
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
