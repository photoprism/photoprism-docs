# Troubleshooting Checklists

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://www.photoprism.app/membership) receive direct [technical support](https://www.photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to determine the cause of your problem.

### Connection Fails ###

If [your browser](browsers.md) cannot connect to the Web UI even after waiting a few minutes, run this command to watch the logs including the last 100 messages (omit `--tail=100` to see them all, and `-f` to output only the last logs without watching them):

```bash
docker compose logs -f --tail=100
```

Before reporting a bug:

- [ ] Check the logs for messages like *disk full*, *disk quota exceeded*, *no space left on device*, *read-only file system*, *error creating path*, *wrong permissions*, *no route to host*, *connection failed*, and *killed*:
    - [ ] If a service has been "killed" or otherwise automatically terminated, this points to a [memory problem](docker.md#adding-swap) (add swap and/or memory; remove or increase usage limits)
    - [ ] In case the logs show "disk full", "quota exceeded", or "no space left" errors, either [the disk containing the *storage* folder is full](docker.md#disk-space) (add storage) or a disk usage limit is configured (remove or increase it)
    - [ ] Errors such as "read-only file system", "error creating path", "failed to create folder", "permission denied", or "wrong permissions" indicate a [filesystem permission problem](docker.md#file-permissions)
    - [ ] It may help to [add the `:z` mount flag to volumes](https://docs.docker.com/storage/bind-mounts/#configure-the-selinux-label) when using SELinux (Red Hat/Fedora)
    - [ ] Log messages that contain "no route to host" indicate a [problem with the database](mariadb.md) or Docker network configuration (follow our [examples](https://dl.photoprism.app/docker/))
- [ ] Make sure you are using the correct protocol (default is `http`), port (default is `2342`), and host (default is `localhost`):
    - [ ] Check if the server port you try to use [has been exposed](https://docs.docker.com/compose/compose-file/compose-file-v3/#ports) and [no firewall is blocking it](https://support.microsoft.com/en-us/windows/turn-microsoft-defender-firewall-on-or-off-ec0844f7-aebd-0583-67fe-601ecf5d774f)
    - [ ] Only use `localhost` or `127.0.0.1` if the server is running on the same computer (host)
    - [ ] Avoid using IP addresses other than `127.0.0.1` directly, as [they can change](https://github.com/photoprism/photoprism/discussions/2791#discussioncomment-3985376)
    - [ ] We recommend [configuring a local hostname](https://dl.photoprism.app/img/docs/pihole-local-dns.png) to access other hosts on your network
- [ ] If you use a [firewall](firewall.md), ensure that it is configured correctly and that [outgoing connections to our geocoding API are allowed](../index.md#maps-places)
- [ ] Note that HTTP security headers will prevent the app from loading in a frame (override them)
- [ ] Verify your computer meets the [system requirements](../index.md#system-requirements)
- [ ] Go through the [checklist for fatal server errors](#fatal-server-errors)

#### MariaDB

Should MariaDB get stuck in a restart loop and PhotoPrism cannot connect to it, this indicates a [memory](docker.md#adding-swap),
[filesystem](docker.md#file-permissions), or other [permission issue](docker.md#kernel-security):

```
mariadb: mysqld: ready for connections.
mariadb: mysqld (initiated by: unknown): Normal shutdown
photoprism: dial tcp 172.18.0.2:3306: connect: no route to host
mariadb: mysqld: Shutdown complete
```

[Learn more ›](mariadb.md)

#### Firewall

**Maps & Places:** As explained in our [Privacy Policy](https://www.photoprism.app/privacy#section-7), reverse geocoding and interactive world maps depend on retrieving the necessary information [from us](https://www.photoprism.app/contact) and [MapTiler AG](https://www.maptiler.com/contacts/), headquartered in Switzerland. You therefore need **allow requests to these API endpoints** if you have a firewall installed and make sure your Internet connection is working.

[Learn more ›](firewall.md)

**IPTables:** On Linux, Docker manipulates the `iptables` rules to provide network isolation. This does have some implications for what you need to do if you want to have your own policies in addition to the rules Docker manages.

[Learn more ›](https://docs.docker.com/network/iptables/)

#### Debug Mode

To [enable debug mode](../config-options.md#logging), set `PHOTOPRISM_LOG_LEVEL` to `"debug"` in the `environment:` section of the `photoprism` service (or use the `--debug` flag when running the `photoprism` command directly):

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_LOG_LEVEL: "debug"
```

If you need even more detailed logs for debugging, you can enable [trace log mode](../config-options.md#logging) by setting `PHOTOPRISM_LOG_LEVEL` to `“trace”` in the `environment:` section of the `photoprism` service (or use the `--trace` flag when running the `photoprism` command directly):

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_LOG_LEVEL: "trace"
```

Then restart all services for the changes to take effect. It can be helpful to keep Docker running in the foreground while debugging so that log messages are displayed directly. To do this, omit the `-d` parameter when restarting:

```bash
docker compose stop
docker compose up 
```

!!! note ""
    If you see no errors or no logs at all, you may have started the server on a different host
    and/or port. There could also be an [issue with your browser](browsers.md), browser plugins, [firewall settings](firewall.md),
    or other tools you may have installed.

!!! tldr ""
    The default [Docker Compose](https://docs.docker.com/compose/) config filename is `compose.yaml`. For simplicity, it doesn't need to be specified when running `docker compose` or `docker-compose` in the same directory. Config files for other apps or instances should be placed in separate folders.

### Docker Doesn't Work ###

Make sure you have [Docker](https://store.docker.com/search?type=edition&offering=community) or [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed, started, and properly configured on your system. It is available for Mac, Linux, and Windows. On Red Hat-compatible Linux distributions like RHEL, CentOS, Fedora, AlmaLinux, and Rocky Linux, you can [use Podman and Podman Compose as direct replacements](docker.md#podman-compose) for Docker and Docker Compose.

↪ [Getting Docker Up and Running](docker.md)

### Bad Performance ###

↪ [Performance Tips](performance.md)

↪ [Solving Windows-Specific Issues](windows.md)

### Fatal Server Errors ###

Fatal errors are often caused by one of the following conditions:

- [ ] Your (virtual) server [disk is full](docker.md#disk-space) (add storage)
- [ ] You have accidentally [mounted the wrong folders](../docker-compose.md#volumes) (update config and restart)
- [ ] There is disk space left, but a usage or the [inode limit](https://serverfault.com/questions/104986/what-is-the-maximum-number-of-files-a-file-system-can-contain) has been reached (change it)
- [ ] You are using a [filesystem or network drive with a file size limit](https://thegeekpage.com/fix-the-file-size-exceeds-the-limit-allowed-and-cannot-be-saved/) (change settings or storage)
- [ ] The *storage* folder [is not writable or mounted read-only](docker.md#file-permissions) (change [permissions](docker.md#file-permissions))
- [ ] [Symbolic links](https://en.wikipedia.org/wiki/Symbolic_link) were mounted or used within a *storage* folder (replace with actual paths)
- [ ] The service configuration is not supported, so startup [fails with an S6 overlay error](docker.md#s6-overlay-error)
- [ ] The [server is low on memory](../index.md#system-requirements) (add memory)
- [ ] You didn't [configure at least 4 GB of swap space](docker.md#adding-swap) (add swap)
- [ ] RAW images and/or high-resolution panoramas require [additional memory](performance.md#memory) above the [recommended minimum](../index.md#system-requirements) (add more swap or memory)
- [ ] The server CPU is overheating (improve cooling)
- [ ] The server has an outdated operating system that is not fully compatible (update)
- [ ] The server hardware is defective and [causes random panics](https://github.com/photoprism/photoprism/discussions/1984) (test on another server)
- [ ] The [database server](mariadb.md) is not running, [incompatible](../index.md#databases), or misconfigured (start, upgrade, or [fix it](mariadb.md))
- [ ] You've [upgraded the MariaDB server](mariadb.md#version-upgrade) without running `mariadb-upgrade`
- [ ] Files are [stored on an unreliable device such as a USB flash drive or a shared network folder](mariadb.md#corrupted-files)
- [ ] There are network problems caused by a bad configuration, [firewall](firewall.md), or unstable connection
- [ ] [Kernel security modules](docker.md#kernel-security) such as [AppArmor](https://wiki.ubuntu.com/AppArmor) and [SELinux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux) are blocking permissions
- [ ] Your Raspberry Pi has not been configured according to our [recommendations](../raspberry-pi.md#system-requirements)

We recommend checking your [Docker Logs](docker.md#viewing-logs) for messages like *disk full*, *disk quota exceeded*,
*no space left on device*, *read-only file system*, *error creating path*, *wrong permissions*, *no route to host*, *connection failed*, and *killed*:

- [ ] If a service has been "killed" or otherwise automatically terminated, this points to a [memory problem](docker.md#adding-swap) (add swap and/or memory; remove or increase usage limits)
- [ ] In case the logs show "disk full", "quota exceeded", or "no space left" errors, either [the disk containing the *storage* folder is full](docker.md#disk-space) (add storage) or a disk usage limit is configured (remove or increase it)
- [ ] Errors such as "read-only file system", "error creating path", "failed to create folder", "permission denied", or "wrong permissions" indicate a [filesystem permission problem](docker.md#file-permissions) 
- [ ] Log messages that contain "no route to host" indicate a [problem with the database](mariadb.md) or network configuration (follow our [examples](https://dl.photoprism.app/docker/))

*Start a full rescan if necessary, for example, if it looks like [thumbnails](index.md#broken-thumbnails) or [pictures are missing](index.md#missing-pictures).*

### App Not Loading ###

If the app doesn't load in your browser when you navigate to the server URL, you can [check the browser console](browsers.md#getting-error-details)
for helpful errors and warnings. Sometimes you just need to wait a moment, for example, if you are using a slow wireless
connection or the server was started only a few seconds ago. In case this does not help:

- [ ] You are using an [incompatible browser](browsers.md) (try another browser)
- [ ] JavaScript is disabled in your browser settings, so you only see the splash screen (enable it)
- [ ] JavaScript was disabled by a browser plugin (disable it or add an exception)
- [ ] Your browser cannot communicate properly with the server, e.g. because a [reverse proxy](../proxies/nginx.md), VPN, or CDN is configured incorrectly (check its configuration and try without)
- [ ] HTTP security headers prevent the app from loading in a frame (override them)
- [ ] An ad blocker or other plugins block requests (disable them or add an exception)
- [ ] There is a problem with your network connection (test if other sites work)
- [ ] You are connected to the wrong server, VPN, CDN, or a DNS record has not been updated yet

### Cannot Log In ###

If [password authentication is enabled](../config-options.md#authentication) and the user interface loads, but you cannot log in with what you assume is the correct password:

- [ ] There is a problem with the [integrity, stability or connection of the database](mariadb.md) that you should be able to diagnose by [watching the logs for errors and warnings](docker.md#viewing-logs)
- [ ] You had too many failed login attempts, therefore another attempt from your computer is temporarily not possible
- [ ] Caps Lock is enabled on your keyboard, your computer has the wrong input locale set, or somebody else might have changed the password without telling you
- [ ] `PHOTOPRISM_ADMIN_PASSWORD` does not have a minimum length of 8 characters, so PhotoPrism has been started without a password since there is no default
- [ ] Your password [contains one or more `$` signs that were not properly escaped](../../developer-guide/technologies/yaml.md#dollar-signs) in your `compose.yaml` or `docker-compose.yml` file ([escape them](../../developer-guide/technologies/yaml.md#dollar-signs) and [reset your database](../docker-compose.md#examples) or [manually set a new password](../../user-guide/users/cli.md#changing-a-password))
- [ ] The password may be correct, but the username is wrong and does not match `PHOTOPRISM_ADMIN_USER`
- [ ] There is a problem with the schema or data in the `auth_sessions` database table that can be resolved by running the `photoprism auth reset --yes` command [in a terminal](../docker-compose.md#command-line-interface) to reset it to a clean state and [force a re-login of all users](../../user-guide/users/cli.md#session-management) (this will also delete all [client access tokens](../../user-guide/users/client-credentials.md#access-tokens) and [app passwords](../../user-guide/settings/account.md#apps-and-devices) users may have created)
- [ ] You upgraded from an early test or [preview build](../updates.md#development-preview) and might need to run the `photoprism users reset --yes` command [in a terminal](../docker-compose.md#command-line-interface) after the upgrade, see [Known Issues](../../known-issues.md#authentication) for details (this resets the `auth_users` table to a clean state and requires accounts to be recreated)
- [ ] Your browser cannot communicate properly with the server, e.g. because a [reverse proxy](../proxies/nginx.md), VPN, or CDN is configured incorrectly (check its configuration and try without)
- [ ] You are connected to the wrong server, VPN, CDN, or a DNS record has not been updated yet
- [ ] Remember that the initial admin username and password cannot be changed after PhotoPrism has been started for the first time

We also recommend checking your [Docker Logs](docker.md#viewing-logs) for messages like *disk full*, *disk quota exceeded*, *no space left on device*, *read-only file system*, *error creating path*, *wrong permissions*, *no route to host*, *connection failed*, and *killed*:

- [ ] If a service has been "killed" or otherwise automatically terminated, this points to a [memory problem](docker.md#adding-swap) (add swap and/or memory; remove or increase usage limits)
- [ ] In case the logs show "disk full", "quota exceeded", or "no space left" errors, either [the disk containing the *storage* folder is full](docker.md#disk-space) (add storage) or a disk usage limit is configured (remove or increase it)
- [ ] Errors such as "read-only file system", "error creating path", "failed to create folder", "permission denied", or "wrong permissions" indicate a [filesystem permission problem](docker.md#file-permissions) 
- [ ] Log messages that contain "no route to host" indicate a [problem with the database](mariadb.md) or network configuration (follow our [examples](https://dl.photoprism.app/docker/))

To see [which user accounts exist](https://docs.photoprism.app/user-guide/users/cli/) on your instance, [open a terminal](../docker-compose.md#command-line-interface) and [run `photoprism users ls`](../../user-guide/users/cli.md#managing-user-accounts). A new password can be [set with `photoprism passwd [username]`](../../user-guide/users/cli.md#changing-a-password). You can then try to log in again. [Upgrade to the latest release](../updates.md#docker-compose), restart the server, and [check the logs for errors and warnings](docker.md#viewing-logs) if it still doesn't work.

### No WebDAV Access ###

If you [followed our step-by-step guide](../../user-guide/sync/webdav.md) and still have trouble connecting via WebDAV:

- [ ] WebDAV has been disabled for all users in the [advanced settings](../../user-guide/settings/advanced.md)
- [ ] WebDAV is unavailable because your instance is [running in public mode](../config-options.md#authentication) (disable it)
- [ ] You are trying to connect to an invalid path, try `/originals/` without omitting the `/` at the end, and read our [notes on installing PhotoPrism in a subdirectory](../../known-issues.md#shared-domain) on a shared domain 
- [ ] Your [user account role](../../user-guide/users/roles.md) is not permitted to use WebDAV (try as *User* or *Admin*)
- [ ] WebDAV access [has not been enabled](../../user-guide/users/index.md) for your user account (enable it)
- [ ] You are experiencing a [general authentication problem](#cannot-log-in), see *Cannot Log In*
- [ ] Your WebDAV client requires a secure connection ([connect via HTTPS](../index.md#https))
- [ ] Your instance or reverse proxy uses an invalid [HTTPS/TLS certificate](../config-options.md#web-server)
- [ ] As a Windows user, you may need to [change the basic authentication level](windows.md#connecting-via-webdav)
- [ ] Your browser cannot communicate properly with the server, e.g. because a [reverse proxy](../proxies/nginx.md), VPN, or CDN is configured incorrectly (check its configuration and try without)
- [ ] You are connected to the wrong server, VPN, or a DNS record has not been updated yet
- [ ] An upload path has been assigned to your user account, limiting write access to that specific path only (check user settings or remove the upload path restriction)
    - [ ] If an upload path is set, you need to synchronize with `.../originals/upload-path/` when using WebDAV to add files to the originals folder
    - [ ] When using WebDAV to sync to the import folder, you need to manually create a folder with the same name as the upload path in the import folder (if an upload path is configured)

### Missing Pictures ###

If you have indexed your library and some images or videos are missing, first [check *Library > Errors* for errors and warnings](logs.md).
In case the application logs do not contain anything helpful:

- [ ] The files exceed the [size limit in megabyte or the resolution limit in megapixels](../config-options.md#storage)
- [ ] The files have [bad filesystem permissions or the wrong owner](docker.md#file-permissions), so they cannot be opened
- [ ] The pictures are in [*Review*](../../user-guide/organize/review.md) due to low quality or incomplete metadata
- [ ] You are browsing the [*Calendar*](../../user-guide/organize/calendar.md) view, which only shows pictures that have a [valid creation date and time](../../user-guide/organize/edit.md#details) specified in their metadata or as part of their filename
- [ ] The [file type](../faq.md#what-media-file-types-are-supported) is generally unsupported
- [ ] The [file type](../faq.md#what-media-file-types-are-supported) is generally supported, but a specific feature or codec is not
- [ ] The indexer has skipped the files because they are exact duplicates
- [ ] The indexer has skipped the files because they have an incorrect extension that does not match their actual format, e.g. [JPEG images with a `.heic` extension](https://github.com/photoprism/photoprism-contrib/tree/main/scripts/Batch%20Rename)
- [ ] The files are [ignored based on pattern in a `.ppignore` file](../../user-guide/library/originals.md#ignoring-files-and-folders)
- [ ] They [are in *Library > Hidden*](https://try.photoprism.app/library/hidden) because thumbnails could not be created:
    - [ ] *Preview Images* are disabled under *Settings > Content* (enable them)
    - [ ] FFmpeg and/or RAW converters are [disabled under *Settings > Advanced*](../../user-guide/settings/advanced.md)
    - [ ] The file is broken, e.g. because of [*short Huffman data*](https://github.com/golang/go/issues/10447) (try to fix it)
    - [ ] Your [*storage* folder is full](docker.md#disk-space), or a quota/[inode limit](https://serverfault.com/questions/104986/what-is-the-maximum-number-of-files-a-file-system-can-contain) has been reached (increase it)
    - [ ] Your [*storage* folder is not writable or mounted read-only](docker.md#file-permissions) (change [permissions](docker.md#file-permissions))
- [ ] Multiple files were [stacked](../../user-guide/organize/stacks.md#for-what-reasons-can-files-be-stacked) based on their metadata or file names
- [ ] The [private](../../user-guide/organize/private.md) or [archived](../../user-guide/organize/archive.md) status was restored from a backup
- [ ] The NSFW filter is enabled, so they were marked as [private](../../user-guide/organize/private.md)
- [ ] You are not signed in as admin, so you cannot see everything
- [ ] You try to index a shared drive on a remote server, but the server is offline
- [ ] Somebody has deleted files without telling you
- [ ] Your server does not have [at least 4 GB of swap](docker.md#adding-swap) or a [hard memory limit](../faq.md#why-is-my-configured-memory-limit-exceeded-when-indexing-even-though-photoprism-doesnt-actually-seem-to-use-that-much-memory) is configured, which may cause unexpected restarts when the indexer temporarily needs more memory to process large files
    - [ ] Indexing RAW images and high-resolution panoramas may require additional [swap space](docker.md#adding-swap) and/or physical memory beyond the [recommended minimum](../index.md#system-requirements)
- [ ] You are connected to the wrong server, VPN, CDN, or a DNS record has not been updated yet

*Depending on the cause of the problem, you may need to perform a full rescan once the issue is resolved.*

#### Zip Archives ####

When you have tried to [download multiple pictures or albums](../../user-guide/organize/download.md) and found that some files are missing in the resulting zip archive or you got the error message "No files available for download":

- [ ] Your index may be out of sync with the file system ([reindex your library](../../user-guide/library/originals.md) and wait until the operation has been completed)
- [ ] In order to include RAW, XMP and/or generated sidecar files, your [download preferences](../../user-guide/settings/library.md#download) may need to be changed under *Settings > General*
- [ ] If this didn't help, you may need to [perform a complete rescan of your library](../../user-guide/library/originals.md#when-should-complete-rescan-be-selected), e.g. after [upgrading to a new release](../../release-notes.md) or restoring your index from a backup

Also make sure that there is [enough free disk space available](docker.md#disk-space), since the server creates a temporary zip file when multiple pictures are selected for download. Complete albums are compressed while downloading without needing temporary storage.

#### File Downloads ####

Follow the [steps to resolve zip download issues](#zip-archives) if you are having problems downloading selected pictures, individual files, or stacks of files that belong to a single photo.

If this didn't help, the problems might be caused by your [browser settings](browsers.md), e.g. insufficient permissions to download multiple files, [browser plugins](browsers.md), a firewall, VPN, CDN or [proxy that you use](https://chaos.social/@tanuva/111529644552218630) together with PhotoPrism.

### Wrong Search Results ###

If search results are incorrect, for example, in the wrong order or not filtered properly:

- [ ] Indexing [is still in progress](../../user-guide/library/originals.md) and has not been completed yet
- [ ] You need to [re-index your pictures](mariadb.md#complete-rescan), for example after updating PhotoPrism
- [ ] Previously [failed migrations must be re-run](mariadb.md#incompatible-schema) to update the index schema
- [ ] The database server is [incompatible or needs to be updated](../index.md#databases)

*It may be a bug if you cannot find any other reasons, such as a local configuration problem or a misunderstanding in how the software works. Please note that [reports must be reproducible](../../user-guide/index.md#getting-support) in order for us to provide a solution.*

### Broken Thumbnails ###

If some pictures have broken or missing thumbnails, first [check *Library > Errors* for errors and warnings](logs.md).
In case the application logs do not contain anything helpful:

- [ ] The issue can be resolved by reloading the page or clearing the browser cache
- [ ] You browse [non-JPEG](../faq.md#what-media-file-types-are-supported) files under *Library > Originals* which have an icon but no preview
- [ ] *Preview Images* are disabled under *Settings > Content* (enable them)
- [ ] *Dynamic Previews* are disabled under *Settings > Advanced* or your server is not powerful enough
- [ ] The sizes in *Settings > Advanced* have been changed so the request can't be fulfilled
- [ ] FFmpeg and/or RAW converters are disabled under *Settings > Advanced* (enable them)
- [ ] Your [*storage* folder is full](docker.md#disk-space), or a quota/[inode limit](https://serverfault.com/questions/104986/what-is-the-maximum-number-of-files-a-file-system-can-contain) has been reached (increase it)
- [ ] Your [*storage* folder is not writable or mounted read-only](docker.md#file-permissions) (change [permissions](docker.md#file-permissions))
- [ ] Your [cache *storage* folder](../docker-compose.md#photoprismstorage) is not accessible, has been renamed, or was [not mounted on a permanent volume](../advanced/docker-volumes.md#storage-folder), so the [cached thumbnails](../../user-guide/backups/folders.md#thumbnails) have been lost after a restart (run the `photoprism thumbs` command [in a terminal](../docker-compose.md#command-line-interface) to regenerate them after fixing this)
- [ ] Originals or thumbnail files were deleted manually, for example to free up disk space
- [ ] Files cannot be opened, e.g. because the file system permissions have been changed
- [ ] Files are stored on an unreliable device such as a USB flash drive or a shared network folder
- [ ] Some thumbnails could not be created because you didn't [configure at least 4 GB of swap](docker.md#adding-swap)
- [ ] Your browser cannot communicate properly with the server, e.g. because a [reverse proxy](../proxies/nginx.md), VPN, or CDN is configured incorrectly (check its configuration and try without)
- [ ] Your proxy, router, or [firewall](firewall.md) has a request rate limit, so some requests fail
- [ ] There are other network problems caused by a [firewall](firewall.md), router, or unstable connection
- [ ] An ad blocker or other plugins block requests (disable them or add an exception)
- [ ] You are connected to the wrong server, VPN, CDN, or a DNS record has not been updated yet

We also recommend checking your [Docker Logs](docker.md#viewing-logs) for messages like *disk full*, *disk quota exceeded*,
*no space left on device*, *read-only file system*, *error creating path*, *wrong permissions*, and *killed*:

- [ ] If a service has been "killed" or otherwise automatically terminated, this points to a
memory problem
- [ ] In case the logs show "disk full", "quota exceeded", or "no space left" errors, either [the disk containing the *storage* folder is full](docker.md#disk-space) (add storage) or a disk usage limit is configured (remove or increase it)
- [ ] Errors such as "read-only file system", "error creating path", "failed to create folder", "permission denied", or "wrong permissions" indicate a [filesystem permission problem](docker.md#file-permissions)

*Depending on the cause of the problem, you may need to perform a full rescan once the issue is resolved.*

### Videos Don't Play ###

In case [FFmpeg is disabled](../../user-guide/settings/advanced.md#disable-ffmpeg) or not installed, videos cannot be indexed because still images cannot be created. You should also have [ExifTool enabled](../config-options.md#feature-flags) to extract metadata such as duration, resolution, and codec.

If videos do not play and/or you only see a white/black area when you open a video:

- [ ] You are using an [incompatible browser](browsers.md), e.g. without AVC support (try another browser)
- [ ] AVC support or related JavaScript features have been disabled in your browser (check the settings and try another browser)
- [ ] It is a large non-AVC video that needs to be transcoded first (wait or [run `photoprism convert` to pre-transcode videos](../docker-compose.md#command-line-interface))
- [ ] An ad blocker or other plugins block requests (disable them or add an exception)
- [ ] [Your (virtual) server disk is full](docker.md#disk-space), or a quota/[inode limit](https://serverfault.com/questions/104986/what-is-the-maximum-number-of-files-a-file-system-can-contain) has been reached (increase it)
- [ ] The *storage* folder [is not writable or mounted read-only](docker.md#file-permissions) (change [permissions](docker.md#file-permissions))
- [ ] Files are stored on an unreliable device such as a USB flash drive or a shared network folder (check if the files are accessible)
- [ ] Your browser cannot communicate properly with the server, e.g. because a [reverse proxy](../proxies/nginx.md), VPN, or CDN is configured incorrectly (check its configuration and try without)
- [ ] There are other network problems caused by a proxy, [firewall](firewall.md), or unstable connection (try a direct connection)
- [ ] You are connected to the wrong server, VPN, CDN, or a DNS record has not been updated yet

We recommend that you check your [Docker Logs](docker.md#viewing-logs) and [the browser console](browsers.md#getting-error-details)
for messages related to *HTTP requests*, *permissions*, *security*, *FFmpeg*, *videos*, and *file conversion*.

Please note:

1. Not all [video and audio formats](https://caniuse.com/?search=video%20format) can be [played with every browser](browsers.md). For example, [AAC](https://caniuse.com/aac "Advanced Audio Coding") - the default audio codec for [MPEG-4 AVC / H.264](https://caniuse.com/avc "Advanced Video Coding") - is supported natively in Chrome, Safari, and Edge, while it is only optionally supported by the OS in Firefox and Opera.
2. HEVC/H.265 video files can have a `.mp4` file extension too, which is often associated with AVC only. This is because MP4 is a *container* format, meaning that the actual video content may be compressed with H.264, H.265, or something else. The file extension doesn't really tell you anything other than that it's probably a video file.
3. MPEG-4 AVC videos are not re-encoded if they exceed the [configured bitrate limit](../../getting-started/advanced/transcoding.md#bitrate-limit). To reduce the size of AVC videos, you can manually replace the original files with a smaller version or wait for a future release that offers this functionality.

!!! info ""
    **We kindly ask you not to report bugs via *GitHub Issues* unless you are certain to have found a fully reproducible and previously unreported issue that must be fixed directly in the app.**
    [Ask for technical support](../../user-guide/index.md#getting-support) if you need help, it could be a local
    configuration problem, or a misunderstanding in how the software works.

*[AVC]: MPEG-4 / H.264
*[CDN]: Content Delivery Network
*[VPN]: Virtual Private Network
*[CPU]: Central Processing Unit
*[DNS]: Domain Name System
*[HTTP]: Hypertext Transfer Protocol
*[SSD]: Solid-State Drive
*[RAW]: image format that contains unprocessed sensor data
*[URL]: Web Address
*[FFmpeg]: transcodes video files
*[HEVC]: High Efficiency Video Coding / H.265 
*[SQLite]: self-contained, serverless SQL database
*[NSFW]: Not Safe For Work
*[swap]: substitute for physical memory
*[host]: Computer, Cloud Server, or VM that runs PhotoPrism
*[read-only]: write protected
*[filesystem]: contains your files and folders
*[RHEL]: Red Hat Enterprise Linux®