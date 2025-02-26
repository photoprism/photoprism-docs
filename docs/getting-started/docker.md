# Running PhotoPrism with Docker

We recommend using [Docker Compose](docker-compose.md) because it is easier and provides more convenience for running multiple services than the [pure Docker command-line interface](https://docs.docker.com/engine/reference/commandline/cli/).
Before you proceed, make sure you have [Docker](https://store.docker.com/search?type=edition&offering=community) installed on your system. It is available for Mac, Linux, and Windows.

Alternatively, [Podman](https://podman.io/) is supported as a drop-in replacement for Docker on Red Hat-compatible Linux distributions like RHEL, CentOS, Fedora, AlmaLinux, and Rocky Linux.

### Step 1: Start the server

=== "Linux"

    Open a terminal and run this command to start the app after replacing `~/Pictures` with
    the folder containing your pictures:
    
    ```bash
    docker run -d \
      --name photoprism \
      --security-opt seccomp=unconfined \
      --security-opt apparmor=unconfined \
      -p 2342:2342 \
      -e PHOTOPRISM_UPLOAD_NSFW="true" \
      -e PHOTOPRISM_ADMIN_PASSWORD="insecure" \
      -v /photoprism/storage \
      -v ~/Pictures:/photoprism/originals \
      photoprism/photoprism:latest
    ```

=== "Podman"

    Open a terminal and run this command to start the app after replacing `~/Pictures` with
    the folder containing your pictures:
    
    ```bash
    podman run -d \
      --name photoprism \
      --privileged \
      --security-opt seccomp=unconfined \
      --security-opt apparmor=unconfined \
      -p 2342:2342 \
      -e PHOTOPRISM_UPLOAD_NSFW="true" \
      -e PHOTOPRISM_ADMIN_PASSWORD="insecure" \
      -v /photoprism/storage \
      -v ~/Pictures:/photoprism/originals \
      photoprism/photoprism:latest
    ```

    Please keep in mind to replace the `docker` command with `podman` when following the examples in our documentation.

The server port and other [config options](config-options.md) can be changed as needed. If you provide no database server credentials, SQLite database files will be created in the *storage* folder. Note, however, that SQLite is not a good choice for users who require scalability and high performance. We therefore do not recommend using this example to set up a production environment without modifying it, e.g. to connect it to an existing MariaDB database instance.

!!! danger ""
    Always change `PHOTOPRISM_ADMIN_PASSWORD` so that the app starts with a **secure initial password**.
    Never use easy-to-guess passwords or default values like `insecure` on publicly accessible servers.
    There is no default [in case no password was provided](../user-guide/users/cli.md#changing-a-password). A minimum length of 8 characters is required.

Commands on Linux may have to be prefixed with `sudo` when not running as root.
Note that this will point the home directory shortcut `~` to `/root` in volume mounts.
Kernel security modules such as AppArmor and SELinux have been reported to cause
[issues](troubleshooting/index.md).

When the app has been started, open the Web UI by navigating to http://localhost:2342/. You should see a login screen.
Sign in with the user `admin` and the password configured via `PHOTOPRISM_ADMIN_PASSWORD`.
You may change it on the [account settings page](../user-guide/settings/account.md).
Enabling [public mode](config-options.md) will disable authentication.

!!! info ""
    It can be helpful to keep Docker running in the foreground while debugging
    so that log messages are displayed directly. To do this, omit the `-d` parameter when restarting.
    
    Should the server already be running, or you see no errors, you may have started it
    on a different host and/or port. There could also be an [issue with your browser,
    ad blocker, or firewall settings](troubleshooting/index.md#connection-fails).

!!! tldr ""
    You cannot change the password with `PHOTOPRISM_ADMIN_PASSWORD` after the app has been started for the first time. To change the *admin* password, run the `docker exec -ti photoprism photoprism passwd [username]` command in a terminal. You can also run `docker exec -ti photoprism photoprism reset` to delete the existing index database and start from scratch.

#### Volumes

Since the app is running inside a container, you have to explicitly [mount the host folders](https://docs.docker.com/storage/bind-mounts/) you want to use.
PhotoPrism won't be able to see folders that have not been mounted. That's an important security feature.

##### /photoprism/originals

The *originals* folder contains your original photo and video files. They are mounted from `~/Pictures` in the example
above, where `~` is a shortcut for your home directory.

You may [mount any folder accessible from the host](https://docs.docker.com/storage/bind-mounts/) instead,
including [network drives](faq.md#how-can-i-mount-network-shares-with-docker). Additional directories can
be mounted as sub folders of `/photoprism/originals`:

```bash
-v ~/Example:/photoprism/originals/Example
``` 

!!! tldr ""
    When *read-only mode* is enabled, all features that require write permission to the *originals* folder are disabled, e.g. [WebDAV](../user-guide/sync/webdav.md), uploading and deleting files. To do this, add the `-e PHOTOPRISM_READONLY="true"` command flag. You can additionally [mount volumes with the `:ro` flag](https://docs.docker.com/storage/bind-mounts/#use-a-read-only-bind-mount) so that writes are also blocked by Docker.

##### /photoprism/storage

SQLite, config, cache, backup, thumbnail and sidecar files are saved in the *storage* folder:

- a *storage* folder must always be mounted so that you do not lose these files after a restart or upgrade
- never configure the *storage* folder to be inside the *originals* folder unless the name starts with a `.` to indicate that it is hidden
- we recommend placing the *storage* folder on a [local SSD drive](troubleshooting/performance.md#storage) for best performance
- mounting [symbolic links](https://en.wikipedia.org/wiki/Symbolic_link) or using them inside the *storage* folder is currently not supported

Using our example, an [anonymous volume](https://docs.docker.com/storage/bind-mounts/) is created and mounted as *storage* folder. You can mount a specific host folder instead, just as with *originals*, which is better for production environments.

!!! tldr ""
    Should you later want to move your instance to another host, the easiest and most time-saving way is to copy the entire *storage* folder along with your originals and database.

##### /photoprism/import

You can optionally mount an *import* folder from which files can be transferred to the *originals* folder
in a structured way that avoids duplicates:

- [imported files](../user-guide/library/import.md) receive a canonical filename and will be organized by year and month
- never configure the *import* folder to be inside the *originals* folder, as this will cause a loop by importing already indexed files

!!! tldr ""
    You can safely skip this. Adding files via [Web Upload](../user-guide/library/upload.md)
    and [WebDAV](../user-guide/sync/webdav.md) remains possible, unless [read-only mode](config-options.md)
    is enabled or the [features have been disabled](../user-guide/settings/general.md).

### Step 2: First steps

Our [First Steps 👣](../user-guide/first-steps.md) tutorial guides you through the user interface and settings to ensure your library is indexed according to your individual preferences.

<!-- !!! note ""
    Ensure [there is enough disk space available](troubleshooting/docker.md#disk-space) for creating thumbnails and [verify filesystem permissions](troubleshooting/docker.md#file-permissions)
    before starting to index: Files in the *originals* folder must be readable, while the *storage* folder
    including all subdirectories must be readable and writeable.

Open the Web UI, go to *Library* and click *Start* to start indexing your pictures.

While indexing, JPEG sidecar files may be created for originals in other formats such as RAW and HEIF.
This is required for image classification, facial recognition, and for displaying them in a Web browser.
Sidecar and thumbnail files will be added to the *storage* folder, so that your *originals* folder won't be modified.

Your [photos](../user-guide/organize/browse.md) and [videos](../user-guide/organize/video.md) will
successively become visible in search results and other parts of the user interface.
Open the *Logs* tab in *Library* to watch the indexer working.

Of course, you can continue using your favorite tools for processing RAW files, editing metadata,
or importing new shots. Go to *Library* and click *Start* to update the index after files have been
changed, added, or removed. This can also be automated using CLI commands and a [scheduler](https://dl.photoprism.app/docker/scheduler/). -->

Easy, isn't it?

### Step 3: When you're done...

You can stop PhotoPrism and start it again using the following commands:

```bash
docker stop photoprism
docker start photoprism
```

To remove the container completely:

```bash
docker rm -f photoprism
```

### PhotoPrism® Plus

Our members can activate [additional features](https://link.photoprism.app/membership) by logging in with the [admin user created during setup](config-options.md#authentication) and then following the steps [described in our activation guide](https://www.photoprism.app/kb/activation). Thank you for your support, which has been and continues to be essential to the success of the project! :octicons-heart-fill-24:{ .heart .purple }

[Compare Memberships ›](https://link.photoprism.app/membership){ class="pr-3 block-xs" } [View Membership FAQ ›](https://www.photoprism.app/membership/faq) 

!!! example ""
    We recommend that new users install our free Community Edition before [signing up for a membership](https://link.photoprism.app/membership).

### Troubleshooting

If your server runs out of memory, the index is frequently locked, or other system resources are running low:

- [ ] Try [reducing the number of workers](config-options.md#indexing) by setting `PHOTOPRISM_WORKERS` to a reasonably small value, depending on the CPU performance and number of cores
- [ ] Ensure that your server has [at least 4 GB of swap](troubleshooting/docker.md#adding-swap) configured and avoid setting a [hard memory limit](faq.md#why-is-my-configured-memory-limit-exceeded-when-indexing-even-though-photoprism-doesnt-actually-seem-to-use-that-much-memory) as this can cause unexpected restarts when the indexer temporarily needs more memory to process large files
- [ ] If you are using SQLite, switch to MariaDB, which is [better optimized for high concurrency](faq.md#should-i-use-sqlite-mariadb-or-mysql)
- [ ] As a last measure, you can [disable the use of TensorFlow](config-options.md#feature-flags) for image classification and facial recognition

Other issues? Our [troubleshooting checklists](troubleshooting/index.md) help you quickly diagnose and resolve them.

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://www.photoprism.app/membership) receive direct [technical support](https://www.photoprism.app/contact) via email.
    Before [submitting a support request](index.md#getting-support), try to [determine the cause of your problem](troubleshooting/index.md).

### Command-Line Interface

#### Introduction

`photoprism help` lists all commands and [config options](config-options.md) available in the current version:

```bash
docker exec -ti photoprism photoprism help
```

Use the `--help` flag to see a detailed command description, for example:

```bash
docker exec -ti photoprism photoprism backup --help
```

PhotoPrism's command-line interface is also well suited for job automation using a [scheduler](https://dl.photoprism.app/docker/scheduler/).

!!! tip ""
    When using *Docker*, you can prepend commands like `docker exec -ti [container] [command]` to run them in a container. Should this fail with *no container found*, make sure the container has been started and you have specified an existing container name or id.

#### Opening a Terminal

To open a terminal session, you can run the following (replace `$UID` with the user ID to be used or omit the `-u` flag altogether to open the terminal as root):

```bash
docker exec -ti -u $UID photoprism bash
```

Passing the `-ti` flag is important for interactive commands to work, for example if you need to confirm an action.

#### Changing the User ID

Specifying a user with the `-u` flag is possible for all commands you run with Docker. In the following examples, it is omitted for brevity.
Note, however, that commands that you run without an explicit user ID might be executed as root.
The currently supported user ID ranges are 0, 33, 50-99, 500-600, 900-1250, and 2000-2100.

#### Examples

| Action                                                 | Command                                                   |
|--------------------------------------------------------|-----------------------------------------------------------|
| *Start PhotoPrism*                                     | `docker start photoprism`                                 |
| *Stop PhotoPrism*                                      | `docker stop photoprism`                                  |
| *Download Update*                                      | `docker pull photoprism/photoprism:latest`                |
| *Uninstall*                                            | `docker rm -f photoprism`                                 |
| *View Logs*                                            | `docker logs --tail=100 -f photoprism`                    |
| *Display Config Values*                                | `docker exec -ti photoprism photoprism show config`       |
| *Show Migration Status*                                | `docker exec -ti photoprism photoprism migrations ls`     |
| *Repeat Failed Migrations*                             | `docker exec -ti photoprism photoprism migrations run -f` |
| *Reset Database*                                       | `docker exec -ti photoprism photoprism reset --yes`       |
| *Backup Database*                                      | `docker exec -ti photoprism photoprism backup -i -f`      |
| *Restore Database*                                     | `docker exec -ti photoprism photoprism restore -i -f`     |
| *Change Password*                                      | `docker exec -ti photoprism photoprism passwd [username]` |
| *Show User Management Commands*                        | `docker exec -ti photoprism photoprism users help`        |
| *Reset User Accounts*                                  | `docker exec -ti photoprism photoprism users reset --yes` |
| *Reset Sessions and Access Tokens*                     | `docker exec -ti photoprism photoprism auth reset --yes`  |
| *Show Face Recognition Commands*                       | `docker exec -ti photoprism photoprism faces help`        |
| *Index Faces*                                          | `docker exec -ti photoprism photoprism faces index`       |
| *Reset People & Faces*                                 | `docker exec -ti photoprism photoprism faces reset -f`    |
| *Transcode Videos to AVC*                              | `docker exec -ti photoprism photoprism convert`           |
| *Regenerate Thumbnails*                                | `docker exec -ti photoprism photoprism thumbs -f`         |
| *Update Index*                                         | `docker exec -ti photoprism photoprism index --cleanup`   |
| [*Move to Originals*](../user-guide/library/import.md) | `docker exec -ti photoprism photoprism import [path]`     |
| [*Copy to Originals*](../user-guide/library/import.md) | `docker exec -ti photoprism photoprism cp [path]`         |

*You can alternatively use `podman` as a drop-in replacement for `docker` on Red Hat-compatible distributions.*

!!! info "Complete Rescan"
    `docker exec -ti photoprism photoprism index -f` rescans all originals, including already indexed and unchanged files.
    This may be necessary after major upgrades and after migrations of the database schema, especially if search results are missing or incorrect. Note You can also start a [rescan from the user interface](../user-guide/library/originals.md) by navigating to *Library* > *Index*, checking "Full Rescan" and then clicking "Start". Manually entered information such as labels, people, titles or descriptions will not be modified when indexing, even if you perform a "complete rescan".

*[home directory]: \user\username on Windows, /Users/username on macOS, and /root or /home/username on Linux
*[host]: Computer, Cloud Server, or VM that runs PhotoPrism
*[HEIF]: High Efficiency Image File Format
*[RAW]: image format that contains unprocessed sensor data
*[UI]: User Interface
*[CLI]: Command-Line Interface
*[AVC]: MPEG-4 / H.264
*[read-only]: write protected
*[filesystem]: contains your files and folders
*[SQLite]: self-contained, serverless SQL database
*[RHEL]: Red Hat Enterprise Linux®